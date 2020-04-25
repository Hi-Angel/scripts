#!/usr/bin/python3

import sys
import subprocess

if len(sys.argv) != 3:
    print("""Usage: %s dev physical_offset_inside_btrfs_partition""" % sys.argv[0])
    exit(1)

device = sys.argv[1]
phys_offset = int(sys.argv[2])

# data ParseState UInt = Searching | KeyFound | SizeFound UInt
class ParseState:
    # a hackish way to make an ADT in python
    # state == 0 = Searching
    # state == 1 = KeyFound
    # state == 2 = SizeFound
    def __init__(self, state, size = None):
        self.state = state
        self.size = size

    def Searching():
        return ParseState(0)

    def KeyFound():
        return ParseState(1)

    def SizeFound(sz):
        assert isinstance(sz, int)
        return ParseState(2, sz)

    def isSearching(self):
        return self.state == 0

    def isKeyFound(self):
        return self.state == 1

    def isSizeFound(self):
        return self.state == 2

class Range:
    def __init__(self, start, past_end):
        self.start = start
        self.past_end = past_end

# data Parser = Parser [Range] ParseState
class Parser:
    def __init__(self, ranges, state):
        self.ranges = ranges
        self.state = state

# String -> [String]
def run_cmd(cmd):
    proc = subprocess.run(cmd.split(), encoding='utf-8', stdout=subprocess.PIPE)
    output = [line for line in proc.stdout.split('\n')]
    if proc.returncode != 0:
        print(f"Command failed, exiting. Failing cmd is: {cmd}, output is {output}")
        exit(1)
    return output

def build_ranges(cmd_out, parser):
    for line in cmd_out:
        if parser.state.isSearching():
            if "FIRST_CHUNK_TREE" in line:
                parser.state = ParseState.KeyFound()
        elif parser.state.isKeyFound():
            if "length" in line: # it's the 1st word, the second is the number
                parser.state = ParseState.SizeFound(int(line.split()[1]))
            elif "FIRST_CHUNK_TREE" in line:
                print("WRN: there was a key without the length")
        elif parser.state.isSizeFound():
            if "offset" in line:
                offset = int(line.split()[-1])
                parser.ranges.append(Range(offset, offset + parser.state.size))
            elif "FIRST_CHUNK_TREE" in line:
                parser.state = ParseState.KeyFound()
        else:
            assert False, 'BUG: unknown state'
    return parser.ranges

cmd_out = run_cmd(f"btrfs ins dump-tree -t 3 {device}")
ranges = build_ranges(cmd_out, Parser([], ParseState.Searching()))
ranges.sort(key=lambda r: r.start)

found = False
for r in ranges:
    if phys_offset >= r.start and phys_offset < r.past_end:
        if found:
            print("INF: this is odd, but there's more than one offset matches")
        found = True
        print(f"It's in range ({r.start}, {r.past_end})")
    if phys_offset < r.start:
        break # we sorted it by "start"

if not found:
    print("Offset was not found")

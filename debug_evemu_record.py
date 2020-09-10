#!/usr/bin/python3
import sys
import re

# original splitlines() has a bug that a '\n' makes two lines, but splitlines
# returns just one empty string, i.e. [''] instead of ['', '']
def splitlines(text):
    return text.splitlines() + \
        ([''] if text[-1] == '\n' else [])

# use this instead of `fd.readlines()` because the latter does not remove newlines
def readlines(fd):
    return splitlines(fd.read())

def print_word_value(fd, mt_slot: int, word_to_search: str):
    curr_slot = None
    curr_line = 0
    for line in readlines(fd):
        curr_line += 1
        if match := re.search('.*ABS_MT_SLOT\s+(\w+)', line):
            curr_slot = int(match.group(1))
            continue
        elif curr_slot == mt_slot:
            if match := re.search(f'.*{word_to_search}\s+(\w+)', line):
                print(f'{curr_line}: {match.group(1)}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"""Usage:
        {sys.argv[0]} <filepath>""")
        exit(1)
    filepath = sys.argv[1]
    with open(filepath, 'r') as fd:
        print_word_value(fd, 1, 'ABS_MT_POSITION_Y')

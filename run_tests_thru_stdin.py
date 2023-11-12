#!/usr/bin/env python3

# A helper script to run an executable and pass some lines via stdin in to it, then
# get the stdout and compare to the expected output. A usecase: Yandex contest tests
# require passing them via stdin, so this script solves the problem of easily running
# many tests over a single executable.
#
# Runs as `run_tests_thru_stdin.py ./my_app`, and the input is expected to be inside
# `input.txt` file as repeated forms of the following shape (without empty lines):
#
#     Test:
#     <test lines>
#     Expected:
#     <expected lines>

import argparse
import subprocess
import sys
from typing import List, Tuple, Optional
from enum import Enum

def run_cmd_no_fail(cmd: str, stdin: str) -> Tuple[List[str], int]:
    ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         input = stdin, text=True)
    return (ret.stdout.rstrip() # remove last newline
            .split('\n'), ret.returncode)

def read_tests(tests_file: str) -> List[str]:
    with open(tests_file, 'r') as f:
        return f.read().splitlines()

class OneTest:
    def __init__(self, test: List[str], expected: List[str]):
        self.test     = test
        self.expected = expected

    def __repr__(self):
        return f'{{test = {self.test}, ' \
            + f'expected = {self.expected}}}'

    def run_test(self, exe: str) -> Optional[List[str]]:
        out, errcode = run_cmd_no_fail(exe, '\n'.join(self.test))
        return None if (errcode == 0 and out == self.expected) \
            else out

class ParseState(Enum):
    InTest     = 1
    InExpected = 2

def parse_tests(tests_file: str) -> List[OneTest]:
    ret                       = []
    test_lines: List[str]     = []
    expected_lines: List[str] = []
    lines_list = read_tests(tests_file)
    assert lines_list[0] == 'Test:'
    lines_list = lines_list[1:]
    state = ParseState.InTest
    for line in lines_list:
        match state:
            case ParseState.InTest:
                if line == 'Expected:':
                    state = ParseState.InExpected
                else:
                    assert line != 'Test:'
                    test_lines.append(line)
            case ParseState.InExpected:
                if line == 'Test:':
                    ret.append(OneTest(test_lines, expected_lines))
                    test_lines     = []
                    expected_lines = []
                    state = ParseState.InTest
                else:
                    assert line != 'Expected:'
                    expected_lines.append(line)
    ret.append(OneTest(test_lines, expected_lines))
    return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('executable', help = 'Path to the executable to run tests on')
    parser.add_argument('tests', help = 'Path to the file with tests')
    args = parser.parse_args()
    tests: List[OneTest] = parse_tests(args.tests)
    failed_tests: List[str] = []
    for i in range(len(tests)):
        ret = tests[i].run_test(args.executable)
        if ret is None:
            print('✓', end='')
        else:
            print('❌', end='')
            failed_tests.append(f'Test {i + 1} failed, expected: {tests[i].expected}, actual {ret}')
    print()
    for fail in failed_tests:
        print(fail, file=sys.stderr)
    exit(0 if len(failed_tests) == 0 else 1)

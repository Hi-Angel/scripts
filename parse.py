#!/usr/bin/python

from pyparsing import Regex, Word, alphanums, LineStart, LineEnd, ParserElement, locatedExpr # type: ignore
from sys import argv

ParserElement.setDefaultWhitespaceChars('') # must be before any pyparsing usage

Ident = Word(alphanums)
# Quote = Or(['"', "'"])
empty_init = Regex('\n\s+def __init__\(self\):') + '\n' \
    + Regex('\s+pass\s*\n')

# return ARG infix and the string value
def parse(text):
    r = locatedExpr(empty_init)('empty_init')
    return [match for match in r.scanString(text)]

def read_text(filename) -> str:
    with open(filename, 'r', encoding="utf8", errors='ignore') as f:
        return f.read()

def overwrite_file(filename, new_content):
    with open(filename, 'w', encoding="utf8", errors='ignore') as f:
        f.seek(0)
        f.write(new_content)
        f.truncate()

if __name__ == "__main__":
    for filename in argv[1:]:
        print(f'Processing {filename}')
        text = read_text(filename)
        matches = parse(text)
        print(f'Got matches: {matches}')
        for m in reversed(matches): # overwrite it starting from the bottom
            print()
            start = m[0]['empty_init']['locn_start']
            past_end = m[0]['empty_init']['locn_end']
            text = text[:start+1] + text[past_end:]
        overwrite_file(filename, text)

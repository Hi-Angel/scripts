#!/usr/bin/python

from pyparsing import Regex, Word, alphanums, LineStart, LineEnd, ParserElement, locatedExpr # type: ignore
from sys import argv

ParserElement.setDefaultWhitespaceChars('') # must be before any pyparsing usage

Ident = Word(alphanums)
# Quote = Or(['"', "'"])
regex_to_find \
    = locatedExpr(Regex(r'if\s*\(.+?= foo\(\w+\)\).*\n\s*{\n'))('pattern1') \
    + locatedExpr(Regex('\s*sts\s*=\s*ERR_SOME.*'))('line_to_del')

def parse(text):
    r = locatedExpr(regex_to_find)('regex_to_find')
    r.parseWithTabs() # a work around for tabs conversion, see https://github.com/pyparsing/pyparsing/issues/293
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
        if not matches:
            continue
        print('Replacing…\n')
        for m in reversed(matches): # overwrite it starting from the bottom
            start = m[0]['regex_to_find']['line_to_del']['locn_start']-1  # -1 to get index
            past_end = m[0]['regex_to_find']['line_to_del']['locn_end']-1 # -1 to get index
            text = text[:start] + text[past_end+1:]
        overwrite_file(filename, text)

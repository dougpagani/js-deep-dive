from io import BufferedReader
import os
from pprint import pprint
import sys

class Token(object):
    pass

# foo(+3)
class Plus(Token):
    pass

class Number(Token):
    def __init__(self, n):
        self.n = n

class SemiColon(Token):
    pass

def tokenize(buf):
    peek = buf.peek(1) # see what's up next
    if peek == ';':
        buf.read1(1) # consume the semicolon
        return SemiColon()
    if peek == '+':
        buf.read1(1) # consume the +
        return Plus()
    if peek in range(0,10):
        buf.read1(1) # consume the +
        return Number(peek)
    if peek == ' ':
        buf.read1(1)
        # just consume and move on

def main(argv):
    f = open(argv[1], 'rb') if len(argv) > 1 else sys.stdin
    buf = BufferedReader(f)
    pprint(tokenize(buf))

if __name__ == "__main__":
    main(sys.argv)


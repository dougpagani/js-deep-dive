from io import BufferedReader
import os
from pprint import pprint
import sys

class Token(object):
    pass

# foo(+3)
class Plus(Token):
    def __repr__(self):
        return 'Plus()'

class Number(Token):
    def __repr__(self):
        return 'Number(%d)' % (self.n,)
    def __init__(self, n):
        if not isinstance(n, int):
            raise ValueError('Number must be initialised with a number')
        self.n = n

class SemiColon(Token):
    def __repr__(self):
        return 'SemiColon()'

class TokenizerError(Exception):
    pass

def isNumberChar(b):
    return b in b'0123456789'

def peek1(buf):
    return buf.peek(1)[:1]

def tokenize(buf):
    while True:
        peek = peek1(buf) # see what's up next
        if peek == b'':
            break
        if peek == b';':
            buf.read1(1) # consume the semicolon
            yield SemiColon()
            continue
        if peek == b'+':
            buf.read1(1) # consume the +
            yield Plus()
            continue
        if isNumberChar(peek):
            l = []
            while isNumberChar(peek):
                l.append(buf.read1(1))
                peek = peek1(buf)
            nl = tuple(map(int, l))
            n = map(lambda x: x[1] * 10**x[0], enumerate(reversed(nl)))
            yield Number(sum(n))
            continue
        if peek == b' ':
            buf.read1(1)
            continue
            # just consume and move on
        if peek == b'\n':
            buf.read1(1)
            continue
            # just consume and move on
        raise TokenizerError("Unexpected character: %s" % (peek,))

def main(argv):
    f = open(argv[1], 'rb') if len(argv) > 1 else sys.stdin
    buf = BufferedReader(f)
    pprint(list(tokenize(buf)))

if __name__ == "__main__":
    main(sys.argv)


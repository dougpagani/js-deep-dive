from io import BufferedReader
import os
from pprint import pprint
import sys

class Token(object):
    pass

class Symbol(Token):
    def __init__(self, s):
        if not isinstance(s, str):
            raise ValueError('Symbol must be initialised with a string')
        self.s = s
    def __repr__(self):
        return 'Symbol(%r)' % (self.s,)

# foo(+3)
class Plus(Token):
    def __repr__(self):
        return 'Plus()'

class EqualsSign(Token):
    def __repr__(self):
        return 'EqualsSign()'

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

class Comma(Token):
    def __repr__(self):
        return 'Comma()'

class CurlyLeft(Token):
    def __repr__(self):
        return 'CurlyLeft()'

class CurlyRight(Token):
    def __repr__(self):
        return 'CurlyRight()'

class Colon(Token):
    def __repr__(self):
        return 'Colon()'

class TokenizerError(Exception):
    pass

def _isNumberChar(b):
    return b in b'0123456789'

def _peek1(buf):
    return buf.peek(1)[:1]

def _isCharChar(c):
    return c in b'abcdefghijklmnopqrstuvwxyz'

def tokenize(buf):
    while True:
        peek = _peek1(buf) # see what's up next
        if peek == b'':
            break
        if peek == b';':
            buf.read1(1) # consume the semicolon
            yield SemiColon()
            continue
        if peek == b',':
            buf.read1(1) # consume the semicolon
            yield Comma()
            continue
        if peek == b'{':
            buf.read1(1) # consume the semicolon
            yield CurlyLeft()
            continue
        if peek == b'}':
            buf.read1(1) # consume the semicolon
            yield CurlyRight()
            continue
        if peek == b':':
            buf.read1(1) # consume the semicolon
            yield Colon()
            continue
        if peek == b'=':
            buf.read1(1)
            yield EqualsSign()
            continue
        if peek == b'+':
            buf.read1(1) # consume the +
            yield Plus()
            continue
        if _isNumberChar(peek):
            l = []
            while _isNumberChar(peek):
                l.append(buf.read1(1))
                peek = _peek1(buf)
            nl = tuple(map(int, l))
            n = map(lambda x: x[1] * 10**x[0], enumerate(reversed(nl)))
            yield Number(sum(n))
            continue
        if peek in (b' ', b'\n'):
            buf.read1(1)
            continue
        if _isCharChar(peek):
            l = []
            while _isCharChar(peek):
                l.append(buf.read1(1))
                peek = _peek1(buf)
            yield Symbol(''.join(map(lambda b: b.decode('utf-8'), l)))
            continue

        raise TokenizerError("Unexpected character: %s" % (peek,))


def main(argv):
    f = open(argv[1], 'rb') if len(argv) > 1 else sys.stdin
    buf = BufferedReader(f)
    pprint(list(tokenize(buf)))

if __name__ == "__main__":
    main(sys.argv)


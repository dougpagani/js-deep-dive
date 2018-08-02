from io import BufferedReader
import sys

import tokenize as tok

class AstNode(object):
    def __str__(self):
        return self.__class__.__name__
    pass

class StatementList(AstNode):
    def children(self):
        return self.statements
    def __init__(self, statements):
        if not all(map(lambda x: isinstance(x, AstNode), statements)):
            raise ValueError('All statements must be AstNodes')
        self.statements = statements

class NumberLiteral(AstNode):
    def children(self):
        return []
    def __str__(self):
        return 'NumberLiteral(%r)' % (self.n,)
    def __init__(self, n):
        if not isinstance(n, tok.Number):
            raise ValueError('A NumberLiteral must be passed a number token')
        self.n = n

class PlusBinary(AstNode):
    def children(self):
        return [self.left, self.right]

    def __init__(self, left, right):
        if not isinstance(left, AstNode) or not isinstance(right, AstNode):
            raise ValueError('PlusBinary should add AstNodes');
        self.left = left
        self.right = right

class NopStatement(AstNode):
    def children(self):
        return []
    pass

def full_tree(ast):
    return (str(ast), list(map(full_tree, ast.children())))

# [Number(1), Plus(), Number(23281129398), SemiColon()]
# Takes a list

def parse_expression(tokens, stack=None):
    if stack is None:
        stack = []
    if not hasnext(tokens):
        raise Exception('Expected expression, found nothing')
    token = tokens.pop(0)
    if isinstance(token, tok.Number):
        if hasnext(tokens):
            stack.append(token)
            return parse_expression(tokens, stack)
        else:
            return NumberLiteral(token)
    if isinstance(token, tok.Plus):
        return parse_plus(tokens, stack)
    raise Exception('Unknown token in expression: %r' % (token,))

def parse_plus(tokens, stack):
    # First parse the rest, because we need that anyway
    right = parse_expression(tokens)
    if len(stack) == 0:
        return PlusUnary(right)
    else:
        left = parse_expression(stack)
        # TODO: check stack = empty
        return PlusBinary(left, right)

# function ( ) { a(); b(); } ; 
def parse_statement(tokens, stack=None):
    if stack is None:
        stack = []
    if not hasnext(tokens):
        if len(stack) == 0:
            return None
        else:
            return parse_expression(stack)
    token = tokens.pop(0)
    if isinstance(token, tok.SemiColon):
        if len(stack) == 0:
            return None
        else:
            return parse_expression(stack)
    if isinstance(token, tok.Number):
        stack.append(token)
        return parse_statement(tokens, stack)
    if isinstance(token, tok.Plus):
        return parse_plus(tokens, stack)

def hasnext(tokens):
    return len(tokens) > 0

def parse_statement_list(tokens):
    l = []
    while hasnext(tokens):
        stmt = parse_statement(tokens)
        if stmt is not None:
            l.append(stmt)
    return StatementList(l)

def main(argv):
    f = open(argv[1], 'rb') if len(argv) > 1 else sys.stdin
    buf = BufferedReader(f)
    toks = tok.tokenize(buf)
    toks = list(toks) # whatever
    ast = parse_statement_list(toks)
    import pprint
    pprint.pprint(full_tree(ast))
    #ast = parse(toks)

if __name__ == '__main__':
    main(sys.argv)

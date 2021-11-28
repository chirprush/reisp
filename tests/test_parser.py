from reisp.parser.parser import Parser, ParserErr
from reisp.ast.node import Node
from reisp.lexer.lexer import Lexer, LexErrType
from reisp.lexer.token import TokenType
from reisp.loc import Loc

class StringBuffer:
    def __init__(self, string):
        self.string = string
        self.loc = Loc(0, -1)

    def __next__(self):
        self.loc.col += 1
        if self.loc.col >= len(self.string):
            return None
        char = self.string[self.loc.col]
        return char

    def __repr__(self):
        return f"StringBuffer('{self.string[self.loc.col:]}')"

def test_parse_nil():
    buffer = StringBuffer("\nnil")
    parser = Parser(buffer)
    node = parser.parse_nil()
    assert not node.is_err()
    assert isinstance(node, Node.Nil)

def test_parse_bool():
    buffer = StringBuffer("\nfalse   true")
    parser = Parser(buffer)
    node = parser.parse_bool()
    assert not node.is_err()
    assert isinstance(node, Node.Bool)
    assert node.value == False
    node = parser.parse_bool()
    assert not node.is_err()
    assert isinstance(node, Node.Bool)
    assert node.value == True

def test_parse_int():
    buffer = StringBuffer("   1234")
    parser = Parser(buffer)
    node = parser.parse_int()
    assert not node.is_err()
    assert isinstance(node, Node.Int)
    assert node.value == 1234

def test_parse_str():
    buffer = StringBuffer('  "hello\\nhi"')
    parser = Parser(buffer)
    node = parser.parse_str()
    assert not node.is_err()
    assert isinstance(node, Node.Str)
    assert node.value == "hello\nhi"

def test_parse_ident():
    buffer = StringBuffer("foo qwerty1234__v**")
    parser = Parser(buffer)
    node = parser.parse_ident()
    assert not node.is_err()
    assert isinstance(node, Node.Ident)
    assert node.value == "foo"
    node = parser.parse_ident()
    assert not node.is_err()
    assert isinstance(node, Node.Ident)
    assert node.value == "qwerty1234__v**"

def test_parse_sym():
    buffer = StringBuffer("\t 1234 'hello '(2 1 1)")
    parser = Parser(buffer)
    node = parser.parse_sym()
    assert node.is_err()
    node = parser.parse_int()
    assert not node.is_err()
    assert isinstance(node, Node.Int)
    assert node.value == 1234
    node = parser.parse_sym()
    assert not node.is_err()
    assert isinstance(node, Node.Quote)
    assert isinstance(node.value, Node.Ident)
    assert node.value.value == "hello"
    node = parser.parse_sym()
    assert not node.is_err()
    assert isinstance(node, Node.Quote)
    assert not node.value.is_err()
    assert isinstance(node.value, Node.List)

def test_parse_list():
    buffer = StringBuffer("\n(test (1 2 3) 1 nil true 'a \"test\")")
    parser = Parser(buffer)
    node = parser.parse_list()
    assert not node.is_err()
    assert isinstance(node, Node.List)
    assert len(node.values) == 7
    for child in node.values:
        assert not child.is_err()

def test_parse_expr():
    buffer = StringBuffer("\ntest (1 2 3) 1 nil true 'a \"test\"")
    parser = Parser(buffer)
    for i in range(7):
        node = parser.parse_expr()
        assert not node.is_err()

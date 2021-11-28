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

def test_string_buffer():
    buffer = StringBuffer("qwertyuiop")
    assert next(buffer) == "q"
    assert next(buffer) == "w"
    assert next(buffer) == "e"
    assert buffer.loc == Loc(0, 2)

def test_eof():
    buffer = StringBuffer("  ")
    lexer = Lexer(buffer)
    token = next(lexer)
    assert token.type == TokenType.Eof
    assert token.value is None

def test_nil():
    buffer = StringBuffer("\tnil")
    lexer = Lexer(buffer)
    token = next(lexer)
    assert token.type == TokenType.Nil
    assert token.value == "nil"

def test_bool():
    buffer = StringBuffer("\ttrue\n\nfalse")
    lexer = Lexer(buffer)
    token = next(lexer)
    assert token.type == TokenType.Bool
    assert token.value == "true"
    token = next(lexer)
    assert token.type == TokenType.Bool
    assert token.value == "false"
    token = next(lexer)
    assert token.type == TokenType.Eof
    assert token.value is None

def test_str():
    buffer = StringBuffer('  "he\nllo"')
    lexer = Lexer(buffer)
    token = next(lexer)
    assert token.type == TokenType.Str
    assert token.value == "he\nllo"

def test_str_eof():
    buffer = StringBuffer('  "he\\')
    lexer = Lexer(buffer)
    err = next(lexer)
    assert err.type == LexErrType.StrEof

def test_sym():
    buffer = StringBuffer("'hello")
    lexer = Lexer(buffer)
    token = next(lexer)
    assert token.type == TokenType.Sym
    assert token.value == "'"
    token = next(lexer)
    assert token.type == TokenType.Ident
    assert token.value == "hello"

def test_str_escp():
    buffer = StringBuffer('  "he\\g"')
    lexer = Lexer(buffer)
    err = next(lexer)
    assert err.type == LexErrType.StrEsc

def test_int():
    buffer = StringBuffer('3 235 1234')
    lexer = Lexer(buffer)
    values = ["3", "235", "1234"]
    for val in values:
        token = next(lexer)
        assert token.type == TokenType.Int
        assert token.value == val
    token = next(lexer)
    assert token.type == TokenType.Eof
    assert token.value is None

def test_ident():
    buffer = StringBuffer(" foo bar asdf")
    lexer = Lexer(buffer)
    values = ["foo", "bar", "asdf"]
    for val in values:
        token = next(lexer)
        assert token.type == TokenType.Ident
        assert token.value == val
    token = next(lexer)
    assert token.type == TokenType.Eof
    assert token.value is None

def test_whitespace():
    buffer = StringBuffer("   \n\t\t\t(")
    lexer = Lexer(buffer)
    token = next(lexer)
    assert token.type == TokenType.Paren
    assert token.value == "("

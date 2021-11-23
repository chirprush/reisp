from src.parser.node import Node
from src.lexer.lexer import Lexer
from src.lexer.token import Token, TokenType
from src.loc import Loc
from enum import Enum, auto
from dataclasses import dataclass
from copy import copy

@dataclass
class ParserErrBase:
    line: str
    loc: Loc

class ParserErr:
    @dataclass
    class ExpectedType(ParserErrBase):
        type: TokenType

    @dataclass
    class ExpectedValue(ParserErrBase):
        value: str

class Parser:
    def __init__(self, source):
        self.source = Lexer(source)

    def expect_type(self, type: TokenType):
        token = next(self.source)
        if token.is_err():
            return token
        elif token.type != type:
            return ParserErr.ExpectedType(type=type, line=self.source.current, loc=token.loc)
        return token

    def expect_value(self, type: TokenType, value: str):
        token = next(self.source)
        if token.is_err():
            return token
        elif token.type != type:
            return ParserErr.ExpectedType(type=type, line=self.source.current, loc=token.loc)
        elif token.value != value:
            return ParserErr.ExpectedValue(value=value, line=self.source.current, loc=token.loc)

    def parse_nil(self):
        if (result := self.expect_type(TokenType.Nil)).is_err():
            return result
        return Node.Nil(loc=result.loc)

    def parse_bool(self):
        if (result := self.expect_type(TokenType.Bool)).is_err():
            return result
        if result.value == "true":
            return Node.Bool(value=True, loc=result.loc)
        elif result.value == "false":
            return Node.Bool(value=False, loc=result.loc)
        raise ValueError("This shouldn't happen")

    def parse_int(self):
        if (result := self.expect_type(TokenType.Int)).is_err():
            return result
        return Node.Int(value=int(result.value), loc=result.loc)

    def parse_str(self):
        if (result := self.expect_type(TokenType.Str)).is_err():
            return result
        return Node.Str(value=result.value, loc=result.loc)

    def parse_ident(self):
        if (result := self.expect_type(TokenType.Ident)).is_err():
            return result
        return Node.Ident(name=result.value, loc=result.loc)

    def parse_sym(self):
        if (result := self.expect_type(TokenType.Symbol)).is_err():
            return result
        return self.parse_expr()

    def parse_list(self):
        if (result := self.expect_value(TokenType.Paren, "(")).is_err():
            return result
        values = []
        # TODO: How do we recover from a error and keep on parsing?
        # Maybe try storing the failed token from expect_*() in a
        # buffer instead of just getting rid of it. We also have to
        # restore the state back if the entire parse_list fails

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
            return ParserErr.ExpectedType(type=type, line=self.source.current, loc=copy(self.source.loc))
        return token

    def parse_int(self):
        if (result := self.expect_type(TokenType.Int)).is_err():
            return result
        return Node.Int(value=int(result.value), loc=result.loc)

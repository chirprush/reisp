from reisp.loc import Loc
from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    Eof = auto()
    Nil = auto()
    Bool = auto()
    Int = auto()
    # Float = auto()
    Str = auto()
    Ident = auto()
    Sym = auto()
    Paren = auto()

    def show(self):
        if self == TokenType.Eof:
            return "an end of file"
        elif self == TokenType.Nil:
            return "a nil"
        elif self == TokenType.Bool:
            return "a boolean"
        elif self == TokenType.Int:
            return "an integer"
        elif self == TokenType.Str:
            return "a string"
        elif self == TokenType.Ident:
            return "an identifier"
        elif self == TokenType.Sym:
            return "a symbol quote"
        elif self == TokenType.Paren:
            return "a parenthesis"
        raise ValueError("This shouldn't happen")

@dataclass
class Token:
    type: TokenType
    value: str
    loc: Loc

    def is_err(self):
        return False

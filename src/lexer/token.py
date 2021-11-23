from src.loc import Loc
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

@dataclass
class Token:
    type: TokenType
    value: str
    loc: Loc

    def is_err(self):
        return False

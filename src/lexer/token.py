from src.loc import Loc
from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    Eof = auto()
    Nil = auto()
    Bool = auto()
    Ident = auto()
    Int = auto()
    Str = auto()
    # Float = auto()
    Paren = auto()
    Sym = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    loc: Loc

    def is_err(self):
        return False

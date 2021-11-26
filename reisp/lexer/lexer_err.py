from reisp.loc import Loc
from dataclasses import dataclass
from enum import Enum, auto

class LexErrType(Enum):
    StrEof = auto()
    StrEsc = auto()

@dataclass
class LexErr:
    type: LexErrType
    loc: Loc

    def is_err(self):
        return True


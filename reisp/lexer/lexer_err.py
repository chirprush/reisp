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

    def show(self):
        if self.type == LexErrType.StrEof:
            return "Unexpected end of file while parsing string"
        elif self.type == LexErrType.StrEsc:
            return "Invalid escape character found in string"
        raise ValueError("This shouldn't happen")

    def is_err(self):
        return True


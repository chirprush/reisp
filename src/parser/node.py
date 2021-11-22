from src.loc import Loc
from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class BaseNode:
    loc: Loc

    def is_err(self):
        return False

class Node:
    class ErrType(Enum):
        ZeroDiv = auto()

    @dataclass
    class Err(BaseNode):
        type: 'Node.ErrType'
        line: str
        loc: Loc

        def is_err(self):
            return True

    @dataclass
    class Int(BaseNode):
        value: int

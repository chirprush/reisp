from reisp.loc import Loc
from dataclasses import dataclass
from enum import Enum, auto

class NodeErrType(Enum):
    ZeroDiv = auto()
    NotCallable = auto()
    IdentNotFound = auto()
    InvalidArgsNum = auto()
    
@dataclass
class NodeErr:
    type: NodeErrType
    node: 'BaseNode'

    def show(self):
        if self.type == NodeErrType.ZeroDiv:
            return "Division by zero"
        elif self.type == NodeErrType.NotCallable:
            return "Cannot call a non-function value"
        elif self.type == NodeErrType.IdentNotFound:
            return f"Invalid identifier: '{self.node.value}'"
        elif self.type == NodeErrType.InvalidArgsNum:
            return "Invalid number of arguments to function"
        raise ValueError("This shouldn't happen")

    def is_err(self):
        return True

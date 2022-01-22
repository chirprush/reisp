from reisp.loc import Loc
from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class BaseNodeErr:
    loc: Loc

    def is_err(self):
        return True

class NodeErr:
    @dataclass
    class ZeroDiv(BaseNodeErr):
        def show(self):
            return "Division by zero"

    @dataclass
    class NotCallable(BaseNodeErr):
        value: 'BaseNode'

        def show(self):
            return f"Cannot call a non-function value (got {self.value.show()})"

    @dataclass
    class IdentNotFound(BaseNodeErr):
        name: str

        def show(self):
            return f"Identifier '{self.name}' does not exist"

    @dataclass
    class VarAlreadyExists(BaseNodeErr):
        name: str

        def show(self):
            return f"Cannot set variable '{self.name}' because it already exists"

    @dataclass
    class InvalidArgsNum(BaseNodeErr):
        got: int
        expected: int

        def show(self):
            return f"Invalid number of arguments to function (got {self.got}, expected {self.expected})"

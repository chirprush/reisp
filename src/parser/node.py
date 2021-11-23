from src.loc import Loc
from typing import Callable
from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class BaseNode:
    loc: Loc

    def is_err(self):
        return False

class ErrType(Enum):
    ZeroDiv = auto()

class Node:
    @dataclass
    class Err(BaseNode):
        type: ErrType
        line: str
        loc: Loc

        def is_err(self):
            return True

    class Nil(BaseNode):
        pass

    @dataclass
    class Bool(BaseNode):
        value: bool

    @dataclass
    class Int(BaseNode):
        value: int

    @dataclass
    class Str(BaseNode):
        value: str

    @dataclass
    class Ident(BaseNode):
        name: str

    @dataclass
    class Sym(BaseNode):
        value: BaseNode

    @dataclass
    class List(BaseNode):
        values: list[BaseNode]

    @dataclass
    class BuiltinFunc(BaseNode):
        func: Callable

    @dataclass
    class UserFunc(BaseNode):
        args: list[str]
        body: BaseNode

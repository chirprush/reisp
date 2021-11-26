from reisp.loc import Loc
from dataclasses import dataclass
from enum import Enum, auto

class NodeErrType:
    ZeroDiv = auto()
    NotCallable = auto()
    IdentNotFound = auto()
    InvalidArgsNum = auto()
    
@dataclass
class NodeErr:
    type: NodeErrType
    node: 'BaseNode'

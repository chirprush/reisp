from reisp.loc import Loc
from reisp.ast.node import Node

def builtin_func(name, arity):
    def inner(f):
        # TODO: Is there a better way to handle the location of a
        # builtin function?
        return Node.BuiltinFunc(Loc(-1, -1), name, arity, f)
    return inner

from reisp.loc import Loc
from reisp.ast.node_err import NodeErrType, NodeErr
from typing import Callable, List as TList
from dataclasses import dataclass

@dataclass
class BaseNode:
    loc: Loc

    def is_err(self):
        return False

    def is_callable(self):
        return False

class Node:
    class Nil(BaseNode):
        def eval(self, env):
            return self

    @dataclass
    class Bool(BaseNode):
        value: bool

        def eval(self, env):
            return self

    @dataclass
    class Int(BaseNode):
        value: int

        def eval(self, env):
            return self

    @dataclass
    class Str(BaseNode):
        value: str

        def eval(self, env):
            return self

    @dataclass
    class Ident(BaseNode):
        value: str

        def eval(self, env):
            if (result := env.get(self.value)) is None:
                return NodeErr(NodeErrType.IdentNotFound, self)
            return result

    @dataclass
    class Sym(BaseNode):
        value: BaseNode

        def eval(self, env):
            return self

    @dataclass
    class List(BaseNode):
        values: TList[BaseNode]

        def eval(self, env):
            if len(self.values) == 0:
                return self
            if (func := self.values[0].eval(env)).is_err():
                return func
            elif not func.is_callable():
                return NodeErr(NodeErrType.NotCallable, self.values[0])
            return func.call(self, env, self.values[1:])

    @dataclass
    class BuiltinFunc(BaseNode):
        func: Callable

        def eval(self, env):
            return env

        def call(self, source, env, args):
            return self.func(source, env, args)

        def is_callable(self):
            return True

    @dataclass
    class UserFunc(BaseNode):
        args: TList[str]
        body: BaseNode

        def call(self, source, env, args):
            if len(args) != len(self.args):
                return NodeErr(NodeErrType.InvalidArgsNum, source)
            self.env.push()
            for i, arg in enumerate(self.args):
                if (value := args[i].eval(env)).is_err():
                    self.env.pop()
                    return value
                self.env.add(arg, value)
            result = self.body.eval(env)
            self.env.pop()
            return result

        def eval(self, env):
            return self

        def is_callable(self):
            return True

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

        def show(self):
            return "nil"

    @dataclass
    class Bool(BaseNode):
        value: bool

        def eval(self, env):
            return self

        def show(self):
            return "true" if self.value else "false"

    @dataclass
    class Int(BaseNode):
        value: int

        def eval(self, env):
            return self

        def show(self):
            return str(self.value)

    @dataclass
    class Str(BaseNode):
        value: str

        def eval(self, env):
            return self

        def show(self):
            result = '"'
            for i in self.value:
                if i in '"\\':
                    result += "\\"
                elif i == "\n":
                    result += "\\n"
                    continue
                result += i
            return result + '"'

    @dataclass
    class Ident(BaseNode):
        value: str

        def eval(self, env):
            if (result := env.get(self.value)) is None:
                return NodeErr(NodeErrType.IdentNotFound, self)
            return result

        def show(self):
            return self.value

    @dataclass
    class Sym(BaseNode):
        value: BaseNode

        def eval(self, env):
            return self

        def show(self):
            if isinstance(self.value, Node.Sym):
                return "'" + self.value.show()
            return self.value.show()

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

        def show(self):
            result = "("
            for i, value in enumerate(self.values):
                result += value.show()
                if i != len(self.values) - 1:
                    result += " "
            return result + ")"

    @dataclass
    class BuiltinFunc(BaseNode):
        name: str
        func: Callable

        def eval(self, env):
            return env

        def show(self):
            return f"#<func {self.name}>"

        def call(self, source, env, args):
            return self.func(source, env, args)

        def is_callable(self):
            return True

    @dataclass
    class UserFunc(BaseNode):
        name: str
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

        def show(self):
            return f"#<func {self.name}>"

        def is_callable(self):
            return True

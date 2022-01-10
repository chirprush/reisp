from reisp.loc import Loc
from reisp.ast.node_err import NodeErr
from reisp.types.type import BaseType, Type, resolve_type
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
        def type(self):
            return Type.Nil()

        def eval(self, env):
            return self

        def show(self):
            return "nil"

    @dataclass
    class Type(BaseNode):
        value: BaseType

        def type(self):
            return Type.Type()

        def eval(self, env):
            return self

        def show(self):
            if isinstance(self.value, Type.Union):
                return "$(" + self.value.show() + ")"
            return "$" + self.value.show()

    @dataclass
    class Bool(BaseNode):
        value: bool

        def type(self):
            return Type.Bool()

        def eval(self, env):
            return self

        def show(self):
            return "true" if self.value else "false"

    @dataclass
    class Int(BaseNode):
        value: int

        def type(self):
            return Type.Int()

        def eval(self, env):
            return self

        def show(self):
            return str(self.value)

    @dataclass
    class Str(BaseNode):
        value: str

        def type(self):
            return Type.Str()

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

        def type(self):
            return Type.Sym()

        def eval(self, env):
            if (result := env.get(self.value)) is None:
                return NodeErr.IdentNotFound(self.loc, self.value)
            return result

        def show(self):
            return self.value

    @dataclass
    class Quote(BaseNode):
        value: BaseNode

        def type(self):
            return Type.Quote(self.value.type())

        def eval(self, env):
            if isinstance(self.value, Node.Quote):
                return self
            return self.value

        def show(self):
            if isinstance(self.value, Node.Quote):
                return "'" + self.value.show()
            return self.value.show()

    @dataclass
    class List(BaseNode):
        values: TList[BaseNode]

        def type(self):
            return Type.List(resolve_type(self.values))

        def eval(self, env):
            if len(self.values) == 0:
                return self
            if (func := self.values[0].eval(env)).is_err():
                return func
            elif not func.is_callable():
                return NodeErr.NotCallable(self.values[0].loc, func)
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
        arity: int
        func: Callable

        def is_callable(self):
            return True

        def call(self, source, env, args):
            if len(args) != self.arity:
                return NodeErr.InvalidArgsNum(source.values[0].loc, len(args), self.arity)
            return self.func(source, env, args)

        def type(self):
            return Type.Func()

        def eval(self, env):
            return env

        def show(self):
            return f"#<func {self.name}>"

    @dataclass
    class UserFunc(BaseNode):
        name: str
        args: TList[str]
        body: BaseNode

        def is_callable(self):
            return True

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

        def type(self):
            return Type.Func()

        def eval(self, env):
            return self

        def show(self):
            return f"#<func {self.name}>"

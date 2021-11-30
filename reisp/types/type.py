from dataclasses import dataclass

class BaseType:
    pass

def resolve_type(values):
    return Type.Any()

type_keywords = [
    "nil",
    "type",
    "bool",
    "int",
    "str",
    "sym",
    "func",
    "any"
]

class Type:
    @dataclass
    class Nil(BaseType):
        def show(self):
            return "nil"

    @dataclass
    class Type(BaseType):
        def show(self):
            return "type"

    @dataclass
    class Bool(BaseType):
        def show(self):
            return "bool"

    @dataclass
    class Int(BaseType):
        def show(self):
            return "int"

    @dataclass
    class Str(BaseType):
        def show(self):
            return "str"

    @dataclass
    class Sym(BaseType):
        def show(self):
            return "sym"

    @dataclass
    class Func(BaseType):
        def show(self):
            return "func"

    @dataclass
    class Quote(BaseType):
        subtype: BaseType

        def show(self):
            return "'" + self.subtype.show()

    @dataclass
    class List(BaseType):
        subtype: BaseType

        def show(self):
            return "[" + self.subtype.show() + "]"

    @dataclass
    class Infer(BaseType):
        name: str

        def show(self):
            return name + "?"

    @dataclass
    class Union(BaseType):
        left: BaseType
        right: BaseType

        def show(self):
            return self.left.show() + " | " + self.right.show()

    @dataclass
    class Any(BaseType):
        def show(self):
            return "any"

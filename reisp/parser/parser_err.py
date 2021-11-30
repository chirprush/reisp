from reisp.loc import Loc
from reisp.lexer.token import TokenType
from dataclasses import dataclass

@dataclass
class ParserErrBase:
    loc: Loc

    def is_err(self):
        return True

class ParserErr:
    @dataclass
    class ExpectedType(ParserErrBase):
        type: TokenType

        def show(self):
            return f"Expected {self.type.show()} token"

    @dataclass
    class ExpectedValue(ParserErrBase):
        value: str

        def show(self):
            return f"Expected text {str(self.value)}"

    @dataclass
    class TypeKeyword(ParserErrBase):
        def show(self):
            return "Type keyword found outside type expression"

    @dataclass
    class ExpectedExpr(ParserErrBase):
        def show(self):
            return f"Expected an expression"


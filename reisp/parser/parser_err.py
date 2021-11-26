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

    @dataclass
    class ExpectedValue(ParserErrBase):
        value: str

    @dataclass
    class ExpectedExpr(ParserErrBase):
        pass


from reisp.ast.node import Node
from reisp.lexer.lexer import Lexer
from reisp.lexer.token import Token, TokenType
from reisp.parser.parser_err import ParserErr
from reisp.types.type import Type
from reisp.loc import Loc
from dataclasses import dataclass
from copy import copy

def parser_func(f):
    def inner(parser):
        save = []
        parser.save = save
        result = f(parser)
        if result.is_err():
            while save:
                parser.restore.append(save.pop())
            return result
        return result
    return inner

class Parser:
    def __init__(self, source):
        self.source = source
        self.lexer = Lexer(source)
        # Tokens saved for backtracking
        self.save = None
        # Tokens that were restored during backtracking
        self.restore = []

    def is_eol(self):
        return self.source.is_eol() and not self.restore

    def skip_line(self):
        self.source.skip_line()
        self.restore = []

    def next_token(self):
        if self.restore:
            return self.restore.pop()
        token = next(self.lexer)
        return token

    def expect_type(self, type: TokenType):
        token = self.next_token()
        if token.is_err():
            return token
        self.save.append(token)
        if token.type != type:
            return ParserErr.ExpectedType(type=type, loc=token.loc)
        return token

    def expect_value(self, type: TokenType, value: str):
        token = self.next_token()
        if token.is_err():
            return token
        self.save.append(token)
        if token.type != type:
            return ParserErr.ExpectedType(type=type, loc=token.loc)
        elif token.value != value:
            return ParserErr.ExpectedValue(value=value, loc=token.loc)
        return token

    @parser_func
    def parse_nil(self):
        if (result := self.expect_type(TokenType.Nil)).is_err():
            return result
        return Node.Nil(loc=result.loc)

    @parser_func
    def parse_type_expr(self):
        if (paren := self.expect_value(TokenType.Paren, "[")).is_err():
            return paren
        if (value := self.parse_type()).is_err():
            return value
        if (result := self.expect_value(TokenType.Paren, "]")).is_err():
            return result
        return value

    @parser_func
    def parse_type_atom(self):
        if (result := self.expect_type(TokenType.Type)).is_err():
            if (result_inner := self.expect_type(TokenType.Nil)).is_err():
                return result
            result = result_inner
        if result.type == TokenType.Nil:
            return Node.Type(value=Type.Nil(), loc=result.loc)
        elif result.value == "type":
            return Node.Type(value=Type.Type(), loc=result.loc)
        elif result.value == "bool":
            return Node.Type(value=Type.Bool(), loc=result.loc)
        elif result.value == "int":
            return Node.Type(value=Type.Int(), loc=result.loc)
        elif result.value == "str":
            return Node.Type(value=Type.Str(), loc=result.loc)
        elif result.value == "sym":
            return Node.Type(value=Type.Sym(), loc=result.loc)
        elif result.value == "func":
            return Node.Type(value=Type.Func(), loc=result.loc)
        elif result.value == "any":
            return Node.Type(value=Type.Any(), loc=result.loc)
        raise ValueError("This shouldn't happen")

    @parser_func
    def parse_type(self):
        if (result := self.parse_type_atom()).is_err():
            return result
        return result

    @parser_func
    def parse_bool(self):
        if (result := self.expect_type(TokenType.Bool)).is_err():
            return result
        if result.value == "true":
            return Node.Bool(value=True, loc=result.loc)
        elif result.value == "false":
            return Node.Bool(value=False, loc=result.loc)
        raise ValueError("This shouldn't happen")

    @parser_func
    def parse_int(self):
        if (result := self.expect_type(TokenType.Int)).is_err():
            return result
        return Node.Int(value=int(result.value), loc=result.loc)

    @parser_func
    def parse_str(self):
        if (result := self.expect_type(TokenType.Str)).is_err():
            return result
        return Node.Str(value=result.value, loc=result.loc)

    @parser_func
    def parse_ident(self):
        if (result := self.expect_type(TokenType.Ident)).is_err():
            return result
        return Node.Ident(value=result.value, loc=result.loc)

    @parser_func
    def parse_quote(self):
        if (result := self.expect_type(TokenType.Quote)).is_err():
            return result
        elif (result := self.parse_expr()).is_err():
            return result
        return Node.Quote(value=result, loc=result.loc)

    @parser_func
    def parse_list(self):
        if (paren := self.expect_value(TokenType.Paren, "(")).is_err():
            return paren
        values = []
        while True:
            if (result := self.parse_expr()).is_err():
                break
            values.append(result)
        if (result := self.expect_value(TokenType.Paren, ")")).is_err():
            return result
        return Node.List(values=values, loc=paren.loc)

    @parser_func
    def parse_expr(self):
        if not (result := self.parse_nil()).is_err():
            return result
        elif not (result := self.parse_type_expr()).is_err():
            return result
        elif not (result := self.parse_bool()).is_err():
            return result
        elif not (result := self.parse_int()).is_err():
            return result
        elif not (result := self.parse_str()).is_err():
            return result
        elif not (result := self.parse_ident()).is_err():
            return result
        elif not (result := self.parse_quote()).is_err():
            return result
        elif not (result := self.parse_list()).is_err():
            return result
        return ParserErr.ExpectedExpr(loc=result.loc)

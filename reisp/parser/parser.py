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
        self.lexer.skip_line()
        self.restore = []

    def next_token(self):
        if self.restore:
            return self.restore.pop()
        token = next(self.lexer)
        return token

    def peek(self):
        if not self.restore:
            self.restore.append(next(self.lexer))
        return self.restore[-1]

    # TODO: If we add the token to self.restore on fail, do we even need @parser_func?
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
        if (quote := self.expect_type(TokenType.Quote)).is_err():
            return quote
        if (result := self.parse_expr()).is_err():
            return result
        return Node.Quote(value=result, loc=quote.loc)

    @parser_func
    def parse_list(self):
        if (paren := self.expect_value(TokenType.Paren, "(")).is_err():
            return paren
        if self.peek().value == ")":
            self.restore.pop()
            return Node.List(values=[], loc=paren.loc)
        values = []
        while True:
            if self.peek().value == ")":
                break
            elif (result := self.parse_expr()).is_err():
                return result
            values.append(result)
        if (result := self.expect_value(TokenType.Paren, ")")).is_err():
            return result
        return Node.List(values=values, loc=paren.loc)

    @parser_func
    def parse_expr(self):
        loc = self.source.loc
        if self.peek().type == TokenType.Nil:
            return self.parse_nil()
        elif self.peek().value == "[":
            return self.parse_type_expr()
        elif self.peek().type == TokenType.Bool:
            return self.parse_bool()
        elif self.peek().type == TokenType.Int:
            return self.parse_int()
        elif self.peek().type == TokenType.Str:
            return self.parse_str()
        elif self.peek().type == TokenType.Ident:
            return self.parse_ident()
        elif self.peek().type == TokenType.Quote:
            return self.parse_quote()
        elif self.peek().value == "(":
            return self.parse_list()
        if self.restore:
            loc = self.restore[-1].loc
        if self.peek().type == TokenType.Type:
            return ParserErr.TypeKeyword(loc=copy(loc))
        return ParserErr.ExpectedExpr(loc=copy(loc))

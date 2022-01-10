from reisp.loc import Loc
from reisp.lexer.token import TokenType, Token
from reisp.lexer.lexer_err import LexErrType, LexErr
from reisp.types.type import type_keywords
from copy import copy

def is_int(word):
    return word.isnumeric() or (word[0] in "-+" and word[1:].isnumeric())

class Lexer:
    def __init__(self, source):
        """
        Note: `source` should be a generator that implements __next__
        and yields a character. It should also supply a `loc`
        attribute of type token.Loc that keeps track of the line and
        column number.
        """
        self.source = source
        self.restore = []

    def skip_line(self):
        self.restore = []

    def get_char(self):
        if self.restore:
            return self.restore.pop()
        return next(self.source)

    def __next__(self):
        char = None
        while (char := self.get_char()) is not None and char in " \n\t":
            pass
        start = copy(self.source.loc)
        if char is None:
            return Token(TokenType.Eof, None, start)
        elif char in "?|$":
            return Token(TokenType.Special, char, start)
        elif char in "()[]":
            return Token(TokenType.Paren, char, start)
        elif char == "'":
            return Token(TokenType.Quote, char, start)
        elif char == '"':
            value = ""
            while True:
                new = self.get_char()
                if new is None:
                    return LexErr(LexErrType.StrEof, start)
                elif new == "\\":
                    escape_char = self.get_char()
                    if escape_char is None:
                        return LexErr(LexErrType.StrEof, copy(self.source.loc))
                    elif escape_char == "n":
                        value += "\n"
                    elif escape_char == "\\":
                        value += "\\"
                    elif escape_char == "\"":
                        value += "\""
                    else:
                        return LexErr(LexErrType.StrEsc, copy(self.source.loc))
                elif new == '"':
                    return Token(TokenType.Str, value, start)
                else:
                    value += new
        word = char
        while True:
            new = self.get_char()
            if new is None:
                break
            elif new in " \t\n":
                break
            elif new in "()[]?|":
                self.restore.append(new)
                break
            word += new
        if word == "nil":
            return Token(TokenType.Nil, word, start)
        elif word in type_keywords:
            return Token(TokenType.Type, word, start)
        elif word in ["true", "false"]:
            return Token(TokenType.Bool, word, start)
        elif is_int(word):
            return Token(TokenType.Int, word, start)
        return Token(TokenType.Ident, word, start)

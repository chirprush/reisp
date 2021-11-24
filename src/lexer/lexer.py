from src.loc import Loc
from src.lexer.token import TokenType, Token
from dataclasses import dataclass
from enum import Enum, auto
from copy import copy

class LexErrType(Enum):
    StrEof = auto()
    StrEsc = auto()

@dataclass
class LexErr:
    type: LexErrType
    line: str
    loc: Loc

    def is_err(self):
        return True

def is_int(word):
    # TODO: Add support for negative numbers
    return word.isnumeric()

class Lexer:
    def __init__(self, source):
        """
        Note: `source` should be a generator that implements __next__
        and yields a character. The buffer should also keep track of
        the current line in `current`. In addition, it should also
        supply a `loc` attribute of type token.Loc that keeps track of
        the line and column number.
        """
        self.source = source
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
        elif char == "(" or char == ")":
            return Token(TokenType.Paren, char, start)
        elif char == "'":
            return Token(TokenType.Sym, char, start)
        elif char == '"':
            value = ""
            while True:
                new = self.get_char()
                if new is None:
                    return LexErr(LexErrType.StrEof, self.source.current, start)
                elif new == "\\":
                    escape_char = self.get_char()
                    if escape_char is None:
                        return LexErr(LexErrType.StrEof, self.source.current, copy(self.source.loc))
                    elif escape_char not in "n":
                        return LexErr(LexErrType.StrEsc, self.source.current, copy(self.source.loc))
                    elif escape_char == "n":
                        value += "\n"
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
            elif new in "()":
                self.restore.append(new)
                break
            word += new
        if word == "nil":
            return Token(TokenType.Nil, word, start)
        elif word in ["true", "false"]:
            return Token(TokenType.Bool, word, start)
        elif is_int(word):
            return Token(TokenType.Int, word, start)
        return Token(TokenType.Ident, word, start)

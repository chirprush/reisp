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

    def __next__(self):
        char = None
        while (char := next(self.source)) is not None and char in " \n\t":
            pass
        if char is None:
            return Token(TokenType.Eof, None, copy(self.source.loc))
        elif char == "(" or char == ")":
            return Token(TokenType.Paren, char, copy(self.source.loc))
        elif char == "'":
            return Token(TokenType.Sym, char, copy(self.source.loc))
        elif char == '"':
            start = copy(self.source.loc)
            value = ""
            while True:
                new = next(self.source)
                if new is None:
                    return LexErr(LexErrType.StrEof, self.source.current, start)
                elif new == "\\":
                    escape_char = next(self.source)
                    if escape_char is None:
                        return LexErr(LexErrType.StrEof, self.source.current, copy(self.source.loc))
                    elif escape_char not in "n":
                        return LexErr(LexErrType.StrEsc, self.source.current, copy(self.source.loc))
                    elif escape_char == "n":
                        value += "\n"
                elif new == '"':
                    return Token(TokenType.Str, value, copy(self.source.loc))
                else:
                    value += new
        word = char
        while True:
            new = next(self.source)
            if new is None:
                break
            elif new in " \t\n":
                break
            word += new
        if word == "nil":
            return Token(TokenType.Nil, word, copy(self.source.loc))
        elif word in ["true", "false"]:
            return Token(TokenType.Bool, word, copy(self.source.loc))
        elif is_int(word):
            return Token(TokenType.Int, word, copy(self.source.loc))
        return Token(TokenType.Ident, word, copy(self.source.loc))

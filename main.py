from reisp.parser.parser import Parser
from reisp.env.env import Env
from reisp.loc import Loc

from argparse import ArgumentParser

class ReplBuffer:
    def __init__(self):
        self.lines = []
        self.loc = Loc(0, 0)

    def is_eol(self):
        if not self.lines:
            return True
        return not self.lines[-1][self.loc.col:].strip()

    def skip_line(self):
        self.loc.col = len(self.lines[-1])

    def __next__(self):
        if not self.lines or self.loc.col >= len(self.lines[-1]):
            self.lines.append(input("> ") + "\n")
            self.loc.line += 1
            self.loc.col = 0
        char = self.lines[-1][self.loc.col]
        self.loc.col += 1
        return char

arg_parser = ArgumentParser(prog="reisp", description="A statically typed, interpreted, custom flavor of Lisp")
arg_parser.add_argument("file", nargs="?")

args = arg_parser.parse_args()

env = Env()

if args.file:
    # Parse and run the file
    pass
else:
    # Run the REPL
    input_buffer = ReplBuffer()
    parser = Parser(input_buffer)
    while True:
        try:
            if (node := parser.parse_expr()).is_err():
                print(node.loc.show() + node.show())
                parser.skip_line()
                continue
            if not parser.is_eol():
                print(input_buffer.loc.show() + "Unexpected text after expression")
                parser.skip_line()
                continue
            if (value := node.eval(env)).is_err():
                print(node.loc.show() + value.show())
                continue
            print(value.show())
        except EOFError:
            print("\nExiting...")
            break

from reisp.parser.parser import Parser
from reisp.env.env import Env
from reisp.loc import Loc

from argparse import ArgumentParser

class ReplBuffer:
    def __init__(self):
        self.lines = []
        self.current = ""
        self.loc = Loc(0, 0)

    def __next__(self):
        if not self.lines or self.loc.col >= len(self.lines[-1]):
            self.lines.append(input("> ") + "\n")
            self.current = self.lines[-1]
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
        # TODO: Due to the way the ReplBuffer is implemented, it
        # allows for multiple expressions on one line. Make sure to
        # stop the parsing after the first expression and see if it is
        # at the end of a line.
        try:
            if (node := parser.parse_expr()).is_err():
                print(node)
                continue
            if (value := node.eval(env)).is_err():
                print(value)
                continue
            print(value.show())
        except EOFError:
            print("\nExiting...")
            break

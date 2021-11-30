from reisp.parser.parser import Parser
from reisp.env.env import Env
from reisp.loc import Loc
from sys import stderr
from argparse import ArgumentParser

class ReplBuffer:
    def __init__(self):
        self.lines = []
        self.loc = Loc(0, -1)

    def is_eol(self):
        if not self.lines:
            return True
        return not self.lines[-1][self.loc.col+1:].strip()

    def skip_line(self):
        self.loc.col = len(self.lines[-1])

    def get_line(self, linenr):
        return self.lines[linenr - 1]

    def __next__(self):
        self.loc.col += 1
        if not self.lines or self.loc.col >= len(self.lines[-1]):
            self.lines.append(input("> ") + "\n")
            self.loc.line += 1
            self.loc.col = -1
        char = self.lines[-1][self.loc.col]
        return char

# TODO: Might want to change this depending on whether the terminal
# supports colors or not
RED = "\x01\033[31m\x02"
BLUE = "\x01\033[34m\x02"
RESET = "\x01\033[0m\x02"

def show_err(buffer, loc, message):
    # TODO: Maybe add an 'end' attribute to Node's which is of type
    # Loc as well. This would allow for the entire error-causing
    # string to be highlighted
    stderr.write(f"{loc.show()}{message}\n")
    line = buffer.get_line(loc.line)
    stderr.write(f"    {line[:loc.col]}{RED}{line[loc.col]}{RESET}{line[loc.col + 1:]}")
    stderr.write(f"    {' ' * loc.col}{BLUE}^{RESET}\n")

def run_file(f):
    pass

def run_repl():
    env = Env()
    input_buffer = ReplBuffer()
    parser = Parser(input_buffer)
    while True:
        try:
            if (node := parser.parse_expr()).is_err():
                show_err(input_buffer, node.loc, node.show())
                parser.skip_line()
                continue
            if not parser.is_eol():
                show_err(input_buffer, input_buffer.loc, "Unexpected text after expression")
                parser.skip_line()
                continue
            if (value := node.eval(env)).is_err():
                show_err(input_buffer, value.node.loc, value.show())
                continue
            parser.restore = []
            print(value.show())
        except EOFError:
            stderr.write("\nExiting...\n")
            break

arg_parser = ArgumentParser(prog="reisp", description="A statically typed, interpreted, custom flavor of Lisp")
arg_parser.add_argument("file", nargs="?")

args = arg_parser.parse_args()

if args.file:
    run_file(args.file)
else:
    run_repl()

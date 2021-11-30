from dataclasses import dataclass

@dataclass
class Loc:
    line: int
    col: int

    def show(self):
        return f"{self.line}:{self.col + 1}:"

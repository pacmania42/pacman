from .models import Edible


class Cell:
    def __init__(self, val: int, row: int, col: int) -> None:
        self.row = row
        self.col = col

        self.val = val
        self.n = bool(self.val & 0b0001)
        self.e = bool(self.val & 0b0010)
        self.s = bool(self.val & 0b0100)
        self.w = bool(self.val & 0b1000)

        self.edible: Edible | None = None

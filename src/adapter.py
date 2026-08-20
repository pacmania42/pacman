from mazegenerator import MazeGenerator


class AdapterError(Exception):
    pass


class Cell:
    row: int
    col: int
    n: bool
    e: bool
    s: bool
    w: bool

    def __init__(self, col: int, row: int, val: int) -> None:
        self.row = row
        self.col = col

        self.n = bool(val & 0b0001)
        self.e = bool(val & 0b0010)
        self.s = bool(val & 0b0100)
        self.w = bool(val & 0b1000)


class Adapter:
    width: int
    height: int
    seed: int
    gen: MazeGenerator
    maze: list[list[Cell]]

    def __init__(self, width: int, height: int, seed: int):
        self.height = height
        self.width = width
        self.seed = seed
        self.maze: list[list[Cell]] = []
        try:
            self.gen = MazeGenerator(
                size=(self.width, self.height),
                perfect=False,
                seed=seed,
            )
            self._convert_cells()
        except Exception as e:
            raise AdapterError(e) from e

    def generate(self) -> None:
        try:
            self.gen.generate(self.seed)
            self._convert_cells()
        except Exception as e:
            raise AdapterError(e) from e

    def _convert_cells(self) -> None:
        if not self.gen.maze:
            return
        self.maze = []
        for row in range(self.height):
            row_cells: list[Cell] = []
            for col in range(self.width):
                row_cells.append(Cell(col, row, self.gen.maze[row][col]))
            self.maze.append(row_cells)

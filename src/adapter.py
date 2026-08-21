from mazegenerator import MazeGenerator


class MazeAdapterError(Exception):
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


class Maze:
    width: int
    height: int
    grid: list[list[Cell]]
    pacgum_positions: list[tuple[int, int]]
    super_pacgum_positions: list[tuple[int, int]]
    ghost_corners: list[tuple[int, int]]
    player_start: tuple[int, int]

    def __init__(self, grid: list[list[Cell]]):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)


class MazeAdapter:
    seed: int
    gen: MazeGenerator

    def __init__(self, width: int, height: int, seed: int):
        self.height = height
        self.width = width
        self.seed = seed
        try:
            self.gen = MazeGenerator(
                size=(self.width, self.height),
                perfect=False,
                seed=seed,
            )
        except Exception as e:
            raise MazeAdapterError(e) from e

    def generate(self) -> Maze:
        try:
            self.gen.generate(self.seed)
            grid = MazeAdapter._convert_cells(self.gen.maze)
        except MazeAdapterError as e:
            raise MazeAdapterError(e) from e
        return Maze(grid=grid)

    @staticmethod
    def _convert_cells(raw_maze: list[list[int]]) -> list[list[Cell]]:
        grid = []
        for row in range(len(raw_maze)):
            row_cells: list[Cell] = []
            for col in range(len(raw_maze[row])):
                row_cells.append(Cell(col, row, raw_maze[row][col]))
            grid.append(row_cells)
        return grid

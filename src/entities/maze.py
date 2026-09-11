from mazegenerator import MazeGenerator


class Cell:
    def __init__(self, val: int, row: int, col: int) -> None:
        self.row = row
        self.col = col

        self.val = val
        self.n = bool(self.val & 0b0001)
        self.e = bool(self.val & 0b0010)
        self.s = bool(self.val & 0b0100)
        self.w = bool(self.val & 0b1000)


class MazeError(Exception):
    pass


class Maze:
    gen: MazeGenerator
    grid: list[list[Cell]]
    cells: list[Cell]
    height: int
    width: int

    def generate(self, width: int, height: int) -> None:
        self.gen = MazeGenerator(size=(width, height))
        self.gen.generate(42)
        self.grid = self._create_grid(self.gen.maze)
        self.cells = [cell for row in self.grid for cell in row]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def _create_grid(self, maze: list[list[int]]) -> list[list[Cell]]:
        grid: list[list[Cell]] = []
        for row in range(len(maze)):
            row_cells: list[Cell] = []
            for col in range(len(maze[0])):
                cell = Cell(maze[row][col], row, col)
                row_cells.append(cell)
            grid.append(row_cells)
        return grid

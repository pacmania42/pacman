from mazegenerator import MazeGenerator

from .cell import Cell


class MazeError(Exception):
    pass


class Maze:
    grid: list[list[Cell]]
    height: int
    width: int
    pattern_ranges: tuple[int, int, int, int]
    center: tuple[int, int]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def generate(self, seed: int) -> None:
        self._gen = MazeGenerator(size=(self.width, self.height))
        self._gen.generate(seed)
        self.grid = self._create_grid(self._gen.maze)
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.pattern_ranges = self._get_pattern_ranges()
        self.center = self._get_center()

    def _create_grid(self, maze: list[list[int]]) -> list[list[Cell]]:
        grid: list[list[Cell]] = []
        for row in range(len(maze)):
            row_cells: list[Cell] = []
            for col in range(len(maze[0])):
                cell = Cell(maze[row][col], row, col)
                row_cells.append(cell)
            grid.append(row_cells)
        return grid

    def _get_pattern_ranges(self) -> tuple[int, int, int, int]:
        pattern_coords = [
            (cell.col, cell.row)
            for row in self.grid
            for cell in row
            if cell.val == 15
        ]

        if pattern_coords:
            min_x = min([x for (x, _) in pattern_coords])
            max_x = max([x for (x, _) in pattern_coords])
            min_y = min([y for (_, y) in pattern_coords])
            max_y = max([y for (_, y) in pattern_coords])
        else:
            min_x = self.width // 4
            max_x = self.width - 1 - min_x
            min_y = self.height // 4
            max_y = self.height - 1 - min_y

        return (min_x, min_y, max_x, max_y)

    def _get_center(self) -> tuple[int, int]:
        min_x, min_y, *_ = self.pattern_ranges

        return min_x + 7 // 2, min_y + 5 // 2

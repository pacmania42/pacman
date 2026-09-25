from mazegenerator import MazeGenerator


class MazeError(Exception):
    """Raised when an error occurs while creating or handling a maze."""

    pass


class Cell:
    """Represents a single cell in the maze grid.

    A cell stores its position, encoded wall information, and references
    to its neighboring cells.

    Args:
        val: Bitmask representing the walls of the cell.
        row: Row index of the cell in the maze grid.
        col: Column index of the cell in the maze grid.

    Attributes:
        row: Row index of the cell.
        col: Column index of the cell.
        val: Bitmask describing which walls are present.
        n: Northern neighboring cell, or ``None`` if there is a wall.
        s: Southern neighboring cell, or ``None`` if there is a wall.
        e: Eastern neighboring cell, or ``None`` if there is a wall.
        w: Western neighboring cell, or ``None`` if there is a wall.
    """

    def __init__(self, val: int, row: int, col: int) -> None:
        """Initialize a maze cell.

        Args:
            val: Bitmask representing the cell's walls.
            row: Row index of the cell.
            col: Column index of the cell.
        """
        self.row = row
        self.col = col
        self.val = val

    def set_neighbors(self, grid: list[list["Cell"]]) -> None:
        """Set references to neighboring cells based on the wall bitmask.

        A neighboring cell is set to ``None`` when the corresponding wall
        is present. Otherwise, the reference points to the adjacent cell
        in the supplied grid.

        The wall bits are interpreted as follows:

        - ``0b0001``: north wall
        - ``0b0010``: east wall
        - ``0b0100``: south wall
        - ``0b1000``: west wall

        Args:
            grid: Two-dimensional maze grid containing this cell and its
                neighboring cells.
        """
        self.n = None if (self.val & 0b0001) else grid[self.row - 1][self.col]
        self.s = None if (self.val & 0b0100) else grid[self.row + 1][self.col]
        self.e = None if (self.val & 0b0010) else grid[self.row][self.col + 1]
        self.w = None if (self.val & 0b1000) else grid[self.row][self.col - 1]


class Maze:
    """Represents a generated maze and its derived regions.

    The maze is generated using :class:`MazeGenerator` and converted into
    a two-dimensional grid of :class:`Cell` objects. Pattern boundaries
    and important maze regions are then calculated from the generated grid.

    Args:
        width: Width of the maze in cells.
        height: Height of the maze in cells.
        seed: Optional seed used by the maze generator.

    Attributes:
        grid: Two-dimensional collection of maze cells.
        height: Maze height in cells.
        width: Maze width in cells.
        pattern_ranges: Bounding coordinates of the maze pattern in the
            form ``(min_x, min_y, max_x, max_y)``.
        center: Coordinates of the center region.
        top_left: Coordinates of the top-left region.
        top_right: Coordinates of the top-right region.
        bottom_left: Coordinates of the bottom-left region.
        bottom_right: Coordinates of the bottom-right region.
    """

    grid: list[list[Cell]]
    height: int
    width: int
    pattern_ranges: tuple[int, int, int, int]
    center: tuple[int, int]
    top_left: tuple[int, int]
    top_right: tuple[int, int]
    bottom_left: tuple[int, int]
    bottom_right: tuple[int, int]

    def __init__(self, width: int, height: int, seed: int | None) -> None:
        """Generate and initialize a maze.

        Args:
            width: Width of the maze in cells.
            height: Height of the maze in cells.
            seed: Optional seed used to initialize maze generation.
                A falsey seed results in ``0`` being passed to the
                generator.
        """
        self.width = width
        self.height = height

        try:
            self._gen = MazeGenerator(size=(self.width, self.height))
            self._gen.generate(seed if seed else 0)
        except Exception as e:
            raise MazeError(f"maze generator failed: {e}") from e
        self.grid = self._create_grid(self._gen.maze)

        self.pattern_ranges = self._get_pattern_ranges()
        self._set_regions()

    def _create_grid(self, maze: list[list[int]]) -> list[list[Cell]]:
        """Convert a raw maze representation into a grid of cells.

        Each integer in the input maze is converted into a :class:`Cell`.
        Once all cells have been created, their neighboring-cell references
        are initialized.

        Args:
            maze: Two-dimensional list containing the encoded maze cells.

        Returns:
            A two-dimensional list of initialized :class:`Cell` objects.
        """
        grid: list[list[Cell]] = []
        for row in range(len(maze)):
            row_cells: list[Cell] = []
            for col in range(len(maze[0])):
                cell = Cell(maze[row][col], row, col)
                row_cells.append(cell)
            grid.append(row_cells)
        for row_cells in grid:
            for cell in row_cells:
                cell.set_neighbors(grid)
        return grid

    def _get_pattern_ranges(self) -> tuple[int, int, int, int]:
        """Determine the bounding coordinates of the maze pattern.

        Cells with a value of ``15`` are treated as pattern cells. If any
        are present, their minimum and maximum x/y coordinates define the
        pattern bounds.

        If no pattern cells are found, the bounds default to an area based
        on one quarter of the maze dimensions.

        Returns:
            A tuple ``(min_x, min_y, max_x, max_y)`` describing the pattern
            boundaries.
        """
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

    def _set_regions(self) -> None:
        """Calculate the important regions of the maze.

        The method sets the center and four corner region coordinates based
        on the maze dimensions and detected pattern boundaries.
        """
        min_x, min_y, *_ = self.pattern_ranges

        self.center = (min_x + 7 // 2, min_y + 5 // 2)
        self.top_left = (1, 0)
        self.top_right = (self.width - 2, 0)
        self.bottom_left = (1, self.height - 1)
        self.bottom_right = (self.width - 2, self.height - 1)

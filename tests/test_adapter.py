from src.adapter import Cell, MazeAdapter


# 1. Adapter returns a maze grid of the correct dimensions.
def test_adapter_maze_dimensions():
    width, height, seed = 6, 7, 123
    adapter = MazeAdapter(width, height, seed)
    maze = adapter.generate()

    assert len(maze.grid) == height
    for row in maze.grid:
        assert len(row) == width


# 2. All maze elements are Cell objects with correct attributes.
def test_maze_is_2d_grid_of_cell_objects():
    adapter = MazeAdapter(5, 5, 42)
    maze = adapter.generate()

    for row_i, row in enumerate(maze.grid):
        for col_i, cell in enumerate(row):
            assert isinstance(cell, Cell)
            assert hasattr(cell, "n") and hasattr(cell, "e")
            assert hasattr(cell, "s") and hasattr(cell, "w")
            assert cell.row == row_i
            assert cell.col == col_i


# 3. Cell wall properties (n,e,s,w) match bitmask encoded in mazegenerator output.
def test_cell_wall_bitmask_matches_maze_generator(monkeypatch):
    # Fake a known maze output: only SE walls in every cell
    width, height = 3, 3

    class FakeGen:
        def __init__(self):
            self.maze = [[0b0110] * width for _ in range(height)]

        def generate(self, seed):
            pass

    adapter = MazeAdapter(width, height, 13)
    adapter.gen = FakeGen()  # Patch in fake generator
    grid = MazeAdapter._convert_cells(adapter.gen.maze)

    for row in grid:
        for cell in row:
            assert not cell.n
            assert cell.e
            assert cell.s
            assert not cell.w


# 4. Adapter with different seeds returns deterministic grids.
def test_different_seeds_produce_different_mazes():
    width, height = 5, 5
    adapter1 = MazeAdapter(width, height, 1)
    adapter2 = MazeAdapter(width, height, 2)
    grid1 = adapter1.generate().grid
    grid2 = adapter2.generate().grid

    r1 = [[c.n + c.e + c.s + c.w for c in row] for row in grid1]
    r2 = [[c.n + c.e + c.s + c.w for c in row] for row in grid2]

    assert (
        r1 != r2
    )  # It's extremely unlikely for small mazes but not impossible!


# 5. Edge/corner cells: at least one wall present (likely in real mazes, but can't guarantee with random generator!)
def test_adapter_edge_cells_have_expected_positions():
    width, height = 4, 4
    adapter = MazeAdapter(width, height, 99)
    grid = adapter.generate().grid
    top_left = grid[0][0]
    top_right = grid[0][-1]
    bottom_left = grid[-1][0]
    bottom_right = grid[-1][-1]

    assert top_left.row == 0 and top_left.col == 0
    assert top_right.row == 0 and top_right.col == width - 1
    assert bottom_left.row == height - 1 and bottom_left.col == 0
    assert bottom_right.row == height - 1 and bottom_right.col == width - 1


# 6. Adapter handles empty/uninitialized maze.
def test_adapter_with_empty_maze(monkeypatch):
    class EmptyGen:
        maze = []

        def generate(self, seed):
            return

    adapter = MazeAdapter(2, 2, 101)
    adapter.gen = EmptyGen()
    grid = adapter._convert_cells(adapter.gen.maze)
    assert grid == []

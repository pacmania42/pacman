from src.adapter import Adapter, Cell


# 1. Adapter returns a maze grid of the correct dimensions.
def test_adapter_maze_dimensions():
    width, height, seed = 6, 7, 123
    adapter = Adapter(width, height, seed)
    adapter.generate()
    assert len(adapter.maze) == height
    for row in adapter.maze:
        assert len(row) == width


# 2. All maze elements are Cell objects with correct attributes.
def test_maze_is_2d_grid_of_cell_objects():
    adapter = Adapter(5, 5, 42)
    adapter.generate()
    for row_i, row in enumerate(adapter.maze):
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

    adapter = Adapter(width, height, 13)
    adapter.gen = FakeGen()  # Patch in fake generator
    adapter._convert_cells()
    for row in adapter.maze:
        for cell in row:
            assert not cell.n
            assert cell.e
            assert cell.s
            assert not cell.w


# 4. Adapter with different seeds returns deterministic grids.
def test_different_seeds_produce_different_mazes():
    width, height = 5, 5
    adapter1 = Adapter(width, height, 1)
    adapter2 = Adapter(width, height, 2)
    adapter1.generate()
    adapter2.generate()
    grid1 = [[c.n + c.e + c.s + c.w for c in row] for row in adapter1.maze]
    grid2 = [[c.n + c.e + c.s + c.w for c in row] for row in adapter2.maze]
    assert (
        grid1 != grid2
    )  # It's extremely unlikely for small mazes but not impossible!


# 5. Edge/corner cells: at least one wall present (likely in real mazes, but can't guarantee with random generator!)
def test_adapter_edge_cells_have_expected_positions():
    width, height = 4, 4
    adapter = Adapter(width, height, 99)
    adapter.generate()
    top_left = adapter.maze[0][0]
    top_right = adapter.maze[0][-1]
    bottom_left = adapter.maze[-1][0]
    bottom_right = adapter.maze[-1][-1]
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

    adapter = Adapter(2, 2, 101)
    adapter.gen = EmptyGen()
    # clear previous conversion, then test fresh conversion with empty maze
    adapter.maze = []
    adapter._convert_cells()
    assert adapter.maze == []

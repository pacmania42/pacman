from src.adapter import Adapter
from src.maze_view import MazeView
from src.settings import Settings


def main() -> None:
    adp = Adapter()
    adp.generate(15, 15)
    maze = MazeView(adp, Settings())
    maze.mlx_loop(maze.mlx_ptr)

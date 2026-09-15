from src.core.config import Config

from .maze import Maze
from .models import Edible


class Pacgum(Edible):
    """"""

    def __init__(
        self, position: tuple[int, int], maze: Maze, config: Config
    ) -> None:
        value = config.points_per_pacgum
        super().__init__(lives=1, value=value, position=position, maze=maze)


class SuperPacgum(Pacgum):
    """"""

    def __init__(
        self, position: tuple[int, int], maze: Maze, config: Config
    ) -> None:
        super().__init__(position=position, config=config, maze=maze)
        self.value = config.points_per_pacgum

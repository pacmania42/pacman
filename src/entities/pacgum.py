from src.core.config import Config
from src.core.settings import Settings

from .maze import Maze
from .models import Edible


class Pacgum(Edible):
    """"""

    def __init__(
        self, position: tuple[int, int], maze: Maze, config: Config
    ) -> None:
        value = config.points_per_pacgum
        size = Settings.pacgum_size
        super().__init__(
            lives=1, value=value, position=position, size=size, maze=maze
        )

    def eat(self, edible: "Edible") -> None:
        return

    def get_eaten(self) -> None:
        self.lives -= 1


class SuperPacgum(Pacgum):
    """"""

    def __init__(
        self, position: tuple[int, int], maze: Maze, config: Config
    ) -> None:
        super().__init__(position=position, config=config, maze=maze)
        self.width, self.height = Settings.superpacgum_size
        self.value = config.points_per_superpacgum

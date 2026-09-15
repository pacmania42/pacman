import math

from src.core.config import Config

from .maze import Maze
from .models import Actor


class Ghost(Actor):
    can_eat: bool = True

    def __init__(
        self, cfg: Config, position: tuple[int, int], maze: Maze
    ) -> None:
        value = cfg.points_per_ghost
        lives = math.inf
        spawn_delay = 2  # TODO: get from config

        super().__init__(
            maze=maze,
            value=value,
            lives=lives,
            position=position,
            spawn_delay=spawn_delay,
        )

    def get_eaten(self) -> None:
        self.respawn_cell = self.cell
        self.cell.edibles.remove(self)
        self.lives -= 1
        self.respawn()

    def respawn(self) -> None:
        if self.lives:
            self.cell = self.respawn_cell
            self.cell.edibles.add(self)

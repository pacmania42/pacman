from src.core.config import Config

from .maze import Maze
from .models import Actor, Direction


class PlayerError(Exception):
    pass


class Player(Actor):
    def __init__(
        self, position: tuple[int, int], cfg: Config, maze: Maze
    ) -> None:
        value = 0
        lives = cfg.lives
        spawn_position = position
        spawn_delay = 2  # TODO: get from config

        super().__init__(
            maze=maze,
            value=value,
            lives=lives,
            position=spawn_position,
            spawn_delay=spawn_delay,
        )
        self.moving = False  # TODO: derive, once movement exists
        self.facing = Direction.EAST  # TODO: set by movement
        self.respawn_cell = self.cell

    def get_eaten(self) -> None:
        self.cell.edibles.remove(self)
        self.lives -= 1
        self.respawn()

    def respawn(self) -> None:
        if self.lives:
            self.cell = self.respawn_cell
            self.cell.edibles.add(self)

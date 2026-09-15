from src.core.config import Config
from src.core.settings import Settings

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
        size = Settings.player_size

        super().__init__(
            maze=maze,
            value=value,
            lives=lives,
            position=spawn_position,
            size=size,
            spawn_delay=spawn_delay,
        )
        self.moving = False  # TODO: derive, once movement exists
        self.facing = Direction.EAST  # TODO: set by movement
        self.respawn_center = self.center

    def get_eaten(self) -> None:
        self.lives -= 1
        if self.lives:
            self.center = self.respawn_center

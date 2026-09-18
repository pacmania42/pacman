from src.core.config import Config
from src.core.settings import Settings

from .maze import Maze
from .models import Actor


class PlayerError(Exception):
    pass


class Player(Actor):
    def __init__(
        self, position: tuple[int, int], cfg: Config, maze: Maze
    ) -> None:
        value = 0
        lives = cfg.lives
        spawn_position = position
        spawn_delay = 1.2
        size = Settings.player_size

        super().__init__(
            maze=maze,
            value=value,
            lives=lives,
            position=spawn_position,
            size=size,
            spawn_delay=spawn_delay,
        )
        self.speed = Settings.player_speed

    def get_eaten(self) -> None:
        self.lives -= 1
        if self.lives:
            self.die()

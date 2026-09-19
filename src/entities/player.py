from src.core.config import Config
from src.core.settings import Settings

from .maze import Maze
from .models import Actor, Region


class PlayerError(Exception):
    pass


class Player(Actor):
    def __init__(self, cfg: Config) -> None:
        value = 0
        lives = cfg.lives
        spawn_delay = 1.2
        size = Settings.player_size
        region = Region.CENTER
        speed = Settings.player_speed

        maze = Maze(14, 14, 0)
        super().__init__(
            maze=maze,
            value=value,
            lives=lives,
            region=region,
            size=size,
            spawn_delay=spawn_delay,
            speed=speed,
        )

    def get_eaten(self) -> None:
        self.lives -= 1
        if self.lives:
            self.die()

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
        region = Region.CENTER
        spawn_delay = Settings.player_spawn_delay
        size = Settings.player_size

        speed, acc = (
            (Settings.player_speed_init, Settings.player_acc)
            if not cfg.speedy_player_cheat
            else (Settings.ch_player_speed_init, Settings.ch_player_acc)
        )

        maze = Maze(14, 14, 0)
        super().__init__(
            maze=maze,
            value=value,
            lives=lives,
            region=region,
            size=size,
            spawn_delay=spawn_delay,
            speed=speed,
            acc=acc,
        )

    def get_eaten(self) -> None:
        self.lives -= 1
        if self.lives:
            self.die()

import math

from src.core.config import Config
from src.core.settings import Settings

from .maze import Maze
from .models import Actor, Direction


class Ghost(Actor):
    can_eat: bool = True

    def __init__(
        self, cfg: Config, position: tuple[int, int], maze: Maze
    ) -> None:
        value = cfg.points_per_ghost
        lives = math.inf
        spawn_delay = 2  # TODO: get from config
        size = Settings.ghost_size

        super().__init__(
            maze=maze,
            value=value,
            lives=lives,
            position=position,
            size=size,
            spawn_delay=spawn_delay,
        )
        self.moving = False  # TODO: derive, once movement exists
        self.facing = Direction.EAST  # TODO: set by movement

    def get_eaten(self) -> None:
        self.respawn_loc = self.center
        self.lives -= 1
        if self.lives:
            self.cell = self.respawn_loc

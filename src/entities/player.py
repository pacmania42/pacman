from src.core.config import Config

from .maze import Maze
from .models import Actor, ActorStatus, Direction, Edible


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
            status=ActorStatus.FLEEING,
            spawn_position=spawn_position,
            spawn_delay=spawn_delay,
        )
        self.moving = False  # TODO: derive, once movement exists
        self.facing = Direction.EAST  # TODO: set by movement

    def eat(self, edible: Edible) -> None:
        self.value += edible.value
        # TODO: implement eat

    def respawn(self) -> None:
        self.status = ActorStatus.FLEEING
        self.position = self.spawn_position

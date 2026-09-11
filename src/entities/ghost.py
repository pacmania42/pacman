import math
import random

from src.core.config import Config

from .maze import Maze
from .models import Actor, ActorStatus, Direction


class Ghost(Actor):
    all_ghost_status: ActorStatus = ActorStatus.CHASING

    def __init__(
        self, cfg: Config, position: tuple[int, int], maze: Maze
    ) -> None:
        value = cfg.points_per_ghost
        lives = math.inf
        x, y = position
        spawn_position = x, y
        spawn_delay = 2  # TODO: get from config

        super().__init__(
            value=value,
            lives=lives,
            status=ActorStatus.CHASING,
            spawn_position=spawn_position,
            spawn_delay=spawn_delay,
        )

        maze.grid[y][x].edible = self

    def eat(self, actor: "Actor") -> None:
        pass

    def get_eaten(self) -> None:
        self.lives -= 1
        if self.value > 0:
            self.respawn()

    def move(self, dt: float, direction: Direction | None) -> None:
        if direction is not None:
            raise GhostMovementError("Player movement needs direction")
        direction = random.choice([*Direction])
        x, y = direction.value
        x = self.position[0] + round(x * dt)
        y = self.position[1] + round(y * dt)

        if not (0 < x < 100) or not (0 < y < 100):
            return

        self.position = (x, y)

    def respawn(self) -> None:
        self.status = Ghost.all_ghost_status
        self.position = self.spawn_position


class GhostMovementError(Exception):
    pass

import math

from src.core.config import Config

from .maze import Maze
from .models import Actor, ActorStatus


class GhostMovementError(Exception):
    pass


class Ghost(Actor):
    all_ghost_status: ActorStatus = ActorStatus.CHASING

    def __init__(
        self, cfg: Config, position: tuple[int, int], maze: Maze
    ) -> None:
        value = cfg.points_per_ghost
        lives = math.inf
        spawn_position = position
        spawn_delay = 2  # TODO: get from config

        super().__init__(
            maze=maze,
            value=value,
            lives=lives,
            status=Ghost.all_ghost_status,
            spawn_position=spawn_position,
            spawn_delay=spawn_delay,
        )

    def respawn(self) -> None:
        self.status = Ghost.all_ghost_status
        self.position = self.spawn_position

from src.pacman.core.config import Config
from src.pacman.state.maze import Maze
from src.pacman.state.models import Actor, ActorStatus, Direction


class Player(Actor):
    def __init__(self, cfg: Config, maze: Maze) -> None:
        value = 0
        lives = cfg.lives
        spawn_position = (0, 0)
        spawn_delay = 2  # TODO: get from config
        super().__init__(
            value=value,
            lives=lives,
            status=ActorStatus.FLEEING,
            spawn_position=spawn_position,
            spawn_delay=spawn_delay,
        )

    def eat(self, actor: "Actor") -> None:
        self.value += actor.value

    def get_eaten(self) -> None:
        self.status = ActorStatus.SPAWNING
        self.lives -= 1
        if self.value > 0:
            self.respawn()

    def move(self, dt: float, direction: Direction | None) -> None:
        if direction is None:
            raise PlayerError("Player movement needs direction")
        x, y = direction.value
        x = self.position[0] + round(x * dt)
        y = self.position[1] + round(y * dt)

        if not (0 < x < 100) or not (0 < y < 100):
            return

        self.position = (x, y)

    def respawn(self) -> None:
        self.status = ActorStatus.FLEEING
        self.position = self.spawn_position


class PlayerError(Exception):
    pass

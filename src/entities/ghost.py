import math
import random

from src.core.config import Config
from src.core.settings import Settings

from .maze import Maze
from .models import Actor, Direction, Location


class Ghost(Actor):
    can_eat: bool = True

    def __init__(
        self, cfg: Config, position: tuple[int, int], maze: Maze
    ) -> None:
        value = cfg.points_per_ghost
        lives = math.inf
        spawn_delay = 2  # TODO: get from config
        size = Settings.ghost_size

        self.ignore_turn_probability = random.uniform(0.1, 0.4)

        super().__init__(
            maze=maze,
            value=value,
            lives=lives,
            position=position,
            size=size,
            spawn_delay=spawn_delay,
        )

    def get_eaten(self) -> None:
        self.lives -= 1
        if self.lives:
            self.die()

    def chase(self, player: Location, maze: Maze) -> Direction | None:
        """pick a direction on cell middle

        at every crossing take the open way nearest to the player,
        dont turn back.
        When frightened take the farthest direction instead
        """
        cell = Location.to_cell(self.center, maze)
        middle = Location.from_grid((cell.col, cell.row))
        if Location.distance(self.center, middle) >= Settings.speed:
            return None
        self.center = middle  # changing center TODO fix when BUG fixed

        back = self.direction.opposite if self.direction else None
        options = [d for d in Direction if getattr(cell, d.value[1])]
        if len(options) > 1:
            options = [d for d in options if d is not back]
        if random.random() < self.ignore_turn_probability:
            return random.choice(options)

        def gap(direction: Direction) -> float:
            nxt = getattr(cell, direction.value[1])
            return Location.distance(
                Location.from_grid((nxt.col, nxt.row)), player
            )

        pick = min if Ghost.can_eat else max
        return pick(options, key=gap)

import math
import random

from src.core.config import Config
from src.core.settings import Settings

from .maze import Maze
from .models import Actor, Direction, Location, Region


class Ghost(Actor):
    can_eat: bool = True

    def __init__(self, cfg: Config, region: Region) -> None:
        value = cfg.points_per_ghost
        lives = math.inf
        spawn_delay = 1.2
        size = Settings.ghost_size
        speed = Settings.ghost_speed

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

        self.ignore_turn_probability = random.uniform(0.1, 0.4)

    def next_level(self, maze: Maze) -> None:
        self.maze = maze
        region: tuple[int, int] = getattr(maze, self.region.value)
        self.center = Location.cell_center(region)
        self.respawn_loc = Location.cell_center(region)
        self.speed += 1

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
        middle = Location.cell_center((cell.col, cell.row))
        if Location.distance(self.center, middle) >= self.speed:
            return None

        back = self.direction.opposite if self.direction else None
        options = [d for d in Direction if getattr(cell, d.value[1])]
        if len(options) > 1:
            options = [d for d in options if d is not back]
        if random.random() < self.ignore_turn_probability:
            return random.choice(options)

        def gap(direction: Direction) -> float:
            nxt = getattr(cell, direction.value[1])
            return Location.distance(
                Location.cell_center((nxt.col, nxt.row)), player
            )

        pick = min if Ghost.can_eat else max
        return pick(options, key=gap)

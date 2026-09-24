import random

from src.core.config import Config
from src.core.settings import Settings

from .maze import Maze
from .models import Actor, Direction, Location, Region


class Ghost(Actor):
    """Represents a ghost enemy controlled by maze navigation logic.

    A ghost inherits movement and actor behavior from :class:`Actor` and
    uses the maze to choose directions while pursuing or avoiding the
    player.

    Args:
        cfg: Game configuration containing ghost-related settings.
        region: Maze region in which the ghost operates.

    Attributes:
        can_eat: Whether ghosts currently chase the player by choosing the
            direction closest to the player. When false, ghosts choose the
            direction farthest from the player.
        ignore_turn_probability: Probability of choosing a random available
            direction instead of actively pursuing the player.
    """

    can_eat: bool = True

    def __init__(self, cfg: Config, region: Region) -> None:
        """Initialize a ghost using the configured game settings.

        The ghost's speed and acceleration depend on whether the frozen-ghost
        cheat is enabled. A separate maze is created for the ghost's actor
        state, using a fixed seed.

        Args:
            cfg: Game configuration used to determine ghost speed,
                acceleration, and point value.
            region: Region in which the ghost is spawned.
        """
        value = cfg.points_per_ghost
        spawn_delay = Settings.ghost_spawn_delay
        size = Settings.ghost_size

        lives = Settings.ghost_lives
        speed, acc = (
            (Settings.ghost_speed_init, Settings.ghost_acc)
            if not cfg.frozen_ghost_cheat
            else (Settings.ch_ghost_speed_init, Settings.ch_ghost_acc)
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
        self.ignore_turn_probability = random.uniform(0.1, 0.4)

    def get_eaten(self) -> None:
        """Handle the ghost being eaten by the player.

        One life is removed from the ghost. If it still has remaining lives,
        the ghost is reset using its inherited death behavior.

        Returns:
            None.
        """
        self.lives -= 1
        if self.lives:
            self.die()

    def chase(self, player: Location, maze: Maze) -> Direction | None:
        """Choose the next direction for the ghost.

        Direction changes are only considered when the ghost is sufficiently
        close to the center of its current maze cell. At intersections, the
        ghost normally chooses the available direction that minimizes its
        distance to the player. When frightened, the farthest direction is
        selected instead.

        The ghost normally avoids reversing its current direction. However,
        with ``ignore_turn_probability`` probability, it chooses randomly
        from the available directions.

        Args:
            player: Player location used as the target for path selection.
            maze: Maze containing the ghost and player.

        Returns:
            The selected direction, or ``None`` if the ghost is not currently
            close enough to the center of its cell to make a turn.
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
            """Calculate the distance from a candidate cell to the player.

            Args:
                direction: Candidate movement direction.

            Returns:
                Euclidean distance between the candidate cell's center and
                the player's location.
            """
            nxt = getattr(cell, direction.value[1])
            return Location.distance(
                Location.cell_center((nxt.col, nxt.row)), player
            )

        pick = min if Ghost.can_eat else max
        return pick(options, key=gap)

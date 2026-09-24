from dataclasses import dataclass
from enum import IntEnum, auto

from src.core.config import Config
from src.core.settings import Settings
from src.entities import (
    ActorState,
    Direction,
    Edible,
    Ghost,
    Location,
    Maze,
    Pacgum,
    Player,
    Region,
    SuperPacgum,
)


class GameStatus(IntEnum):
    """Represents the current status of a game."""

    ACTIVE = auto()
    PAUSED = auto()
    OVER = auto()


@dataclass(frozen=True)
class GameResult:
    """Contains the result of a completed game.

    Attributes:
        won: Whether the player completed all available levels.
        score: Final score achieved by the player.
    """

    won: bool
    score: int


class GameState:
    """Manages the complete state of an active game.

    The game state controls level progression, player and ghost entities,
    collectibles, timers, collisions, frightened mode, and game status.

    Args:
        config: Configuration containing game rules, level definitions,
            scoring values, timing values, and cheat settings.

    Attributes:
        config: Configuration used by the game.
        levels: Configured levels available to play.
        level_max_time: Maximum time allowed for each level.
        curr_level_no: Zero-based index of the currently active level.
        won: Whether the player has completed all levels.
        player: Player-controlled actor.
        ghosts: Set of ghosts in the game.
        pacgums: Set of regular pacgums currently present.
        superpacgums: Set of super pacgums currently present.
        curr_level: Configuration of the currently active level.
        maze: Maze generated for the current level.
        time_left: Remaining time for the current level.
        frightened_left: Remaining duration of frightened ghost mode.
        status: Current :class:`GameStatus` of the game.
    """

    def __init__(self, config: Config) -> None:
        """Initialize a new game.

        The player and ghosts are created and the first level is started.

        Args:
            config: Configuration used to initialize the game.
        """
        self.config = config

        self.levels = self.config.levels
        self.level_max_time = self.config.level_max_time
        self.curr_level_no = -1
        self.won = False

        self.player = Player(cfg=self.config)
        self.ghosts = self._create_ghosts()
        self.pacgums: set[Pacgum] = set()
        self.superpacgums: set[SuperPacgum] = set()

        self._start_level()

    def _start_level(self, next_level: bool = True) -> None:
        """Start or restart a game level.

        When ``next_level`` is true, the current level number is advanced.
        If all configured levels have already been completed, the game is
        marked as won and over.

        A new maze and set of collectibles are created for each level, and
        all actors are repositioned.

        Args:
            next_level: Whether to advance to the next level before starting
                it. Defaults to ``True``.
        """
        if next_level:
            if self.curr_level_no == len(self.levels) - 1:
                self.won = True
                self.status = GameStatus.OVER
                return
            self.curr_level_no += 1

        self.curr_level = self.levels[self.curr_level_no]
        self.maze = Maze(
            self.curr_level.width,
            self.curr_level.height,
            seed=self.config.seed if self.curr_level_no == 0 else None,
        )
        self.player.next_level(self.maze)
        for ghost in self.ghosts:
            ghost.next_level(self.maze)
        self.superpacgums = self._create_superpacgums()
        self.pacgums = self._create_pacgums()
        self.time_left = float(self.level_max_time)
        self.frightened_left = 0.0
        self.status = GameStatus.ACTIVE

    def pause_game(self) -> None:
        """Pause the game if it is currently active.

        The game status is changed from :attr:`GameStatus.ACTIVE` to
        :attr:`GameStatus.PAUSED`. Calling this method while the game is
        already paused or over has no effect.
        """
        if self.status == GameStatus.ACTIVE:
            self.status = GameStatus.PAUSED

    def resume_game(self) -> None:
        """Resume the game if it is currently paused.

        The game status is changed from :attr:`GameStatus.PAUSED` to
        :attr:`GameStatus.ACTIVE`. Calling this method when the game is
        active or over has no effect.
        """
        if self.status == GameStatus.PAUSED:
            self.status = GameStatus.ACTIVE

    def update(self, dt: float, wanted: Direction | None) -> None:
        """Advance the game state by one update.

        Timers, actor states, movement, collisions, and game status are
        updated. Actors that are not alive do not move during their
        death/rebirth sequence.

        Args:
            dt: Elapsed time in seconds since the previous update.
            wanted: Direction requested by the player, or ``None`` when no
                direction is requested.
        """
        self.time_left -= dt
        self.frightened_left = max(0.0, self.frightened_left - dt)
        Ghost.can_eat = self.frightened_left <= 0
        self.player.advance_state(dt)
        if self.player.state is not ActorState.ALIVE:
            return  # waits death play
        self.player.move(dt, wanted)
        for ghost in self.ghosts:
            ghost.advance_state(dt)
            if ghost.state is not ActorState.ALIVE:
                continue
            ghost.move(dt, ghost.chase(self.player.center, self.maze))

        collided_entities = self._check_collision()
        self._handle_collision(collided_entities)
        self._update_status()

    def _check_collision(self) -> set[Edible]:
        """Find all active edible entities colliding with the player.

        Only entities with remaining lives and a distance less than or equal
        to the configured collision threshold are considered.

        Returns:
            Set of pacgums, super pacgums, and ghosts currently colliding
            with the player.
        """
        ghosts = [g for g in self.ghosts if g.state is ActorState.ALIVE]
        all_edibles = [*self.pacgums, *self.superpacgums, *ghosts]
        return set(
            [
                edible
                for edible in all_edibles
                if edible.lives
                and Location.distance(self.player.center, edible.center)
                <= Settings.collision_threshold
            ]
        )

    def _handle_collision(self, collided: set[Edible]) -> None:
        """Process all collisions detected during the current update.

        Eating a super pacgum activates frightened mode. A collision with
        a ghost causes the player to lose a life unless frightened mode or
        the invincibility cheat prevents it. All remaining collided
        collectibles are consumed by the player.

        Args:
            collided: Set of edible entities currently colliding with the
                player.
        """
        collided_spgs = collided.intersection(self.superpacgums)
        collided_ghosts = collided.intersection(self.ghosts)

        if collided_spgs:
            self.frightened_left = Settings.eating_duration
            Ghost.can_eat = False

        if (
            collided_ghosts
            and Ghost.can_eat
            and not self.config.invincibility_cheat
        ):
            self.player.get_eaten()
            return

        for edible in collided:
            self.player.eat(edible)

    def _update_status(self) -> None:
        """Update the game status based on level completion and failure.

        The next level is started when all pacgums and super pacgums have
        been consumed. The game is marked as over if the player has no
        remaining lives or the level timer reaches zero.
        """
        all_pacgums = [
            edible
            for edible in [*self.pacgums, *self.superpacgums]
            if edible.lives
        ]

        if len(all_pacgums) == 0:
            self._start_level(next_level=True)

        if not self.player.lives or self.time_left <= 0:
            self.status = GameStatus.OVER

    def _create_ghosts(self) -> set[Ghost]:
        """Create the ghosts and assign their starting regions.

        Returns:
            Set containing the four ghosts used by the game.
        """
        cyan = Ghost(region=Region.TOP_LEFT, cfg=self.config)
        yellow = Ghost(region=Region.TOP_RIGHT, cfg=self.config)
        green = Ghost(region=Region.BOTTOM_LEFT, cfg=self.config)
        red = Ghost(region=Region.BOTTOM_RIGHT, cfg=self.config)

        return set([cyan, yellow, green, red])

    def _create_pacgums(self) -> set[Pacgum]:
        """Create regular pacgums throughout the maze.

        Pacgums are placed outside the maze's pattern area and are not
        placed in cells already occupied by super pacgums.

        Returns:
            Set containing all regular pacgums for the current level.
        """
        min_x, min_y, max_x, max_y = self.maze.pattern_ranges
        pacgums: set[Pacgum] = set()

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if (min_x <= x <= max_x) and (min_y <= y <= max_y):
                    continue
                if any(
                    [
                        Location.to_cell(spg.center, self.maze)
                        == self.maze.grid[y][x]
                        for spg in self.superpacgums
                    ]
                ):
                    continue
                pacgum = Pacgum(
                    position=(x, y),
                    config=self.config,
                    maze=self.maze,
                )
                pacgums.add(pacgum)
        return set(pacgums)

    def _create_superpacgums(self) -> set[SuperPacgum]:
        """Create the four super pacgums at the maze corners.

        Returns:
            Set containing four super pacgums positioned at the four
            corners of the current maze.
        """
        red = SuperPacgum(
            position=(0, 0),
            config=self.config,
            maze=self.maze,
        )
        pink = SuperPacgum(
            position=(0, self.maze.height - 1),
            config=self.config,
            maze=self.maze,
        )
        cyan = SuperPacgum(
            position=(self.maze.width - 1, 0),
            config=self.config,
            maze=self.maze,
        )
        yellow = SuperPacgum(
            position=(self.maze.width - 1, self.maze.height - 1),
            config=self.config,
            maze=self.maze,
        )

        return set([red, pink, cyan, yellow])

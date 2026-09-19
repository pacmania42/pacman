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
    ACTIVE = auto()
    PAUSED = auto()
    OVER = auto()


@dataclass(frozen=True)
class GameResult:
    """How a game ended, gameplay pass this to the game over screen"""

    def __init__(self, won: bool, score: int) -> None:
        self.won: bool = won
        self.score: int = score


class GameState:
    def __init__(self, config: Config) -> None:
        self.config = config

        self.levels = self.config.levels
        self.level_max_time = self.config.level_max_time
        self.curr_level_no = -1

        self.player = Player(cfg=self.config)
        self.ghosts = self._create_ghosts()
        self.pacgums = set()
        self.superpacgums = set()

        self._start_level()

    def _start_level(self, next_level: bool = True) -> None:
        if self.curr_level_no == len(self.levels) - 1:
            self.status = GameStatus.OVER
            return

        if next_level:
            self.curr_level_no += 1

        self.curr_level = self.levels[self.curr_level_no]
        self.maze = Maze(
            self.curr_level.width, self.curr_level.height, self.curr_level.seed
        )
        self.player.next_level(self.maze)
        for ghost in self.ghosts:
            ghost.next_level(self.maze)
        self.superpacgums = self._create_superpacgums()
        self.pacgums = self._create_pacgums()
        self.elapsed = 0.0
        self.time_left = float(self.level_max_time)
        self.frightened_left = 0.0
        self.status = GameStatus.ACTIVE

    def pause_game(self) -> None:
        if self.status == GameStatus.ACTIVE:
            self.status = GameStatus.PAUSED

    def resume_game(self) -> None:
        if self.status == GameStatus.PAUSED:
            self.status = GameStatus.ACTIVE

    def update(self, dt: float, wanted: Direction | None) -> None:
        self.elapsed += dt
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
        if collided_entities:
            self._handle_collision(collided_entities)

    def _check_collision(self) -> set[Edible]:
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
        collided_spgs = collided.intersection(self.superpacgums)
        collided_ghosts = collided.intersection(self.ghosts)

        if collided_spgs:
            self.frightened_left = Settings.eating_duration
            Ghost.can_eat = False

        if collided_ghosts and Ghost.can_eat:
            self.player.get_eaten()

        for edible in collided:
            self.player.eat(edible)

        self._update_status()

    def _update_status(self) -> None:
        all_pacgums = [
            edible
            for edible in [*self.pacgums, *self.superpacgums]
            if edible.lives
        ]

        if len(all_pacgums) == 0:
            self._start_level(next_level=True)

        if self.player.lives == 0:
            self.status = GameStatus.OVER

    def _create_ghosts(self) -> set[Ghost]:
        cyan = Ghost(region=Region.TOP_LEFT, cfg=self.config)
        yellow = Ghost(region=Region.TOP_RIGHT, cfg=self.config)
        green = Ghost(region=Region.BOTTOM_LEFT, cfg=self.config)
        red = Ghost(region=Region.BOTTOM_RIGHT, cfg=self.config)

        return set([cyan, yellow, green, red])

    def _create_pacgums(self) -> set[Pacgum]:
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

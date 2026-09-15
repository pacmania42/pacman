from enum import IntEnum, auto
from random import choice

from src.core.config import Config
from src.core.settings import Settings
from src.entities import (
    Direction,
    Ghost,
    Maze,
    Pacgum,
    Player,
    SuperPacgum,
)


class GameStatus(IntEnum):
    ACTIVE = auto()
    PAUSED = auto()
    OVER = auto()


class GameState:
    def __init__(self, config: Config, settings: Settings) -> None:
        self.config = config
        self.levels = config.levels
        self.settings = settings
        self.start_game()

    def start_game(self) -> None:
        self.curr_level = self.levels[0]
        self.status = GameStatus.ACTIVE
        self.elapsed = 0.0
        self.time_left = float(self.config.level_max_time)
        self._init_entities()

    def restart_level(self) -> None:
        self.status = GameStatus.ACTIVE
        # TODO: wip

    def pause_game(self) -> None:
        if self.status == GameStatus.ACTIVE:
            self.status = GameStatus.PAUSED

    def resume_game(self) -> None:
        if self.status == GameStatus.PAUSED:
            self.status = GameStatus.PAUSED

    def update(self, dt: float, wanted: Direction | None) -> None:
        self.elapsed += dt
        self.time_left -= dt
        self.player.move(dt, wanted)
        # TODO: move ghosts
        # if wanted:
        #     for ghost in self.ghosts:
        #         ghost.move(dt, choice([*Direction, None]))

        self._check_collision()

        # check for game over
        if self.player.lives == 0:
            self.status = GameStatus.OVER
            return

    def _init_entities(self) -> None:
        height = self.curr_level.height
        width = self.curr_level.width

        self.maze = Maze(width=width, height=height)
        self.maze.generate(42)
        self.player = Player(
            position=self.maze.center,
            cfg=self.config,
            maze=self.maze,
        )
        self.ghosts = self._create_ghosts()
        self.superpacgums = self._create_superpacgums()
        self.pacgums = self._create_pacgums()

    def _check_collision(self) -> None:
        entities = self.player.cell.edibles - set([self.player])
        superpacgums = entities & self.superpacgums
        ghosts = entities & self.ghosts

        if superpacgums:
            Ghost.can_eat = False

        if ghosts and Ghost.can_eat:
            self.player.get_eaten()
            return

        for entity in entities:
            self.player.eat(entity)

    def _create_ghosts(self) -> set[Ghost]:
        cyan = Ghost(
            position=(1, 0),
            cfg=self.config,
            maze=self.maze,
        )
        yellow = Ghost(
            position=(self.maze.width - 2, 0),
            cfg=self.config,
            maze=self.maze,
        )
        green = Ghost(
            position=(1, self.maze.height - 1),
            cfg=self.config,
            maze=self.maze,
        )
        red = Ghost(
            position=(self.maze.width - 2, self.maze.height - 1),
            cfg=self.config,
            maze=self.maze,
        )

        return set([cyan, yellow, green, red])

    def _create_pacgums(self) -> set[Pacgum]:
        min_x, min_y, max_x, max_y = self.maze.pattern_ranges
        pacgums: set[Pacgum] = set()

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if (min_x <= x <= max_x) and (min_y <= y <= max_y):
                    continue
                if self.maze.grid[y][x].edibles:
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

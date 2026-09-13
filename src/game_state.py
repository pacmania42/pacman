from enum import IntEnum, auto

from src.core.config import Config, Level
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
    status: GameStatus
    player: Player
    maze: Maze
    ghosts: tuple[Ghost, Ghost, Ghost, Ghost]
    superpacgums: tuple[SuperPacgum, SuperPacgum, SuperPacgum, SuperPacgum]
    pacgums: list[Pacgum]
    levels: list[Level]
    curr_level: Level
    elapsed: float
    time_left: float

    def __init__(self, config: Config, settings: Settings) -> None:
        self.config = config
        self.levels = config.levels
        self.settings = settings
        self.start_game()

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
        self._init_superpacgums()
        self._init_ghosts()
        self._init_pacgums()

    def start_game(self) -> None:
        self.curr_level = self.levels[0]
        self.status = GameStatus.ACTIVE
        self.elapsed = 0.0
        self.time_left = float(self.config.level_max_time)
        self._init_entities()

    def restart_level(self) -> None:
        self.status = GameStatus.ACTIVE
        # TODO: wip

    def update(self, dt: float, wanted: Direction | None) -> None:
        self.elapsed += dt
        self.time_left -= dt
        # TODO move player / ghosts
        # TODO collisions...

    def _init_superpacgums(self) -> None:
        red = SuperPacgum(position=(0, 0), cfg=self.config, maze=self.maze)
        pink = SuperPacgum(
            position=(0, self.maze.height - 1), cfg=self.config, maze=self.maze
        )
        cyan = SuperPacgum(
            position=(self.maze.width - 1, 0), cfg=self.config, maze=self.maze
        )
        yellow = SuperPacgum(
            position=(self.maze.width - 1, self.maze.height - 1),
            cfg=self.config,
            maze=self.maze,
        )

        self.superpacgums = (red, pink, cyan, yellow)

    def _init_ghosts(self) -> None:
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

        self.ghosts = (cyan, yellow, green, red)

    def _init_pacgums(self) -> None:
        min_x, min_y, max_x, max_y = self.maze.pattern_ranges
        pacgums: list[Pacgum] = []

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if min_x > x and x < max_x and (min_y > y < max_y):
                    continue
                if not self.maze.grid[y][x].edible:
                    pacgums.append(
                        Pacgum(
                            position=(x, y),
                            cfg=self.config,
                            maze=self.maze,
                        )
                    )
        self.pacgums = pacgums

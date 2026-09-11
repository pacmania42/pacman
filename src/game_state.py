from enum import IntEnum, auto

from src.core.config import Config
from src.core.settings import Settings
from src.entities import Ghost, Maze, Pacgum, Player, SuperPacgum


class GameStatus(IntEnum):
    ACTIVE = auto()
    PAUSED = auto()
    OVER = auto()


class GameState:
    status: GameStatus
    pacman: Player
    maze: Maze
    ghosts: tuple[Ghost, Ghost, Ghost, Ghost]
    superpacgums: tuple[SuperPacgum, SuperPacgum, SuperPacgum, SuperPacgum]
    pacgums: list[Pacgum]

    def __init__(self, config: Config, settings: Settings) -> None:
        self.config = config
        self.settings = settings
        self.status = GameStatus.ACTIVE
        self.maze = Maze()
        self.pacman = Player(
            position=self.maze.center,
            cfg=config,
            maze=self.maze,
        )
        self._init_superpacgums()
        self._init_ghosts()
        self._init_pacgums()

    def _init_superpacgums(self) -> None:
        red = SuperPacgum(
            position=(0, 0),
            cfg=self.config,
        )
        pink = SuperPacgum(
            position=(0, self.maze.height - 1),
            cfg=self.config,
        )
        cyan = SuperPacgum(
            position=(self.maze.width - 1, 0),
            cfg=self.config,
        )
        yellow = SuperPacgum(
            position=(self.maze.width - 1, self.maze.height - 1),
            cfg=self.config,
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
        height = self.maze.height
        width = self.maze.width

        pacgums = []

        for y in list(range(0, min_y)) + list(range(max_y + 1, height)):
            for x in list(range(0, min_x)) + list(range(max_x + 1, width)):
                if not self.maze.grid[y][x].edible:
                    pacgums.append(
                        Pacgum(
                            position=(x, y),
                            cfg=self.config,
                            maze=self.maze,
                        )
                    )

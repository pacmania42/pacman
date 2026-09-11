from enum import IntEnum, auto
from random import randint

from src.pacman.core.config import Config
from src.pacman.core.settings import Settings
from src.pacman.state.ghost import Ghost
from src.pacman.state.maze import Maze
from src.pacman.state.models import Pacgum, SuperPacgum
from src.pacman.state.player import Player


class GameStatus(IntEnum):
    ACTIVE = auto()
    PAUSED = auto()
    OVER = auto()


class GameState:
    status: GameStatus
    pacman: Player
    maze: Maze
    ghosts: list[Ghost]
    pacgums: list[Pacgum]
    superpacgums: list[SuperPacgum]

    def __init__(self, config: Config, settings: Settings) -> None:
        self.config = config
        self.settings = settings
        self.status = GameStatus.ACTIVE
        self.maze = Maze()
        self.pacman = Player(config, self.maze)
        self.superpacgums = [
            SuperPacgum(
                position=(0, 0),
                cfg=self.config,
            ),
        ]
        self.pacgums = [
            Pacgum(
                position=(
                    randint(0, self.maze.width),
                    randint(0, self.maze.height),
                ),
                cfg=self.config,
            )
        ]
        self.ghosts = [
            Ghost(  # TODO: create a ghost house
                cfg=self.config,
                pos=(
                    randint(0, self.maze.width),
                    randint(0, self.maze.height),
                ),
            ),
            Ghost(  # TODO: create a ghost house
                cfg=self.config,
                pos=(
                    randint(0, self.maze.width),
                    randint(0, self.maze.height),
                ),
            ),
            Ghost(  # TODO: create a ghost house
                cfg=self.config,
                pos=(
                    randint(0, self.maze.width),
                    randint(0, self.maze.height),
                ),
            ),
            Ghost(  # TODO: create a ghost house
                cfg=self.config,
                pos=(
                    randint(0, self.maze.width),
                    randint(0, self.maze.height),
                ),
            ),
        ]

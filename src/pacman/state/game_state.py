from enum import IntEnum, auto

from src.pacman.core.config import Config
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

    def __init__(self, config: Config) -> None:
        self.status = GameStatus.ACTIVE
        self.maze = Maze()
        self.pacman = Player(config, self.maze)
        self.superpacgums = [
            SuperPacgum((0, 0), config),
        ]
        self.ghosts = [
            Ghost((0, 0)),
            Ghost((0, self.maze.height - 1)),
            Ghost((self.maze.width - 1, 0)),
            Ghost((self.maze.width - 1, self.maze.height - 1)),
        ]

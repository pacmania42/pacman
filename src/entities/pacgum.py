from src.core.config import Config

from .ghost import Ghost
from .maze import Maze
from .models import Actor, ActorStatus, Edible


class Pacgum(Edible):
    def __init__(
        self, position: tuple[int, int], cfg: Config, maze: Maze
    ) -> None:
        value = cfg.points_per_pacgum
        super().__init__(maze=maze, position=position, value=value)

    def eat(self, actor: Actor) -> None:
        pass

    def get_eaten(self) -> None:
        self.is_active = False


class SuperPacgum(Edible):
    def __init__(
        self, position: tuple[int, int], cfg: Config, maze: Maze
    ) -> None:
        value = cfg.points_per_pacgum
        super().__init__(maze=maze, position=position, value=value)

    def eat(self, actor: "Actor") -> None:
        pass

    def get_eaten(self) -> None:
        self.is_active = False
        Ghost.all_ghost_status = ActorStatus.FLEEING

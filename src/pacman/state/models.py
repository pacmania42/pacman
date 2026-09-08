from abc import ABC, abstractmethod
from enum import Enum, IntEnum, auto

from src.pacman.core.config import Config


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


class Edible(ABC):
    position: tuple[int, int]
    value: int
    is_active: bool

    def __init__(self, position: tuple[int, int], value: int) -> None:
        self.position = position
        self.value = value
        self.is_active = True

    @abstractmethod
    def eat(self, actor: "Actor") -> None: ...

    @abstractmethod
    def get_eaten(self) -> None: ...


class Pacgum(Edible):
    def __init__(self, position: tuple[int, int], cfg: Config) -> None:
        position = position
        value = cfg.points_per_pacgum
        super().__init__(position=position, value=value)

    def eat(self, actor: "Actor") -> None:
        pass

    def get_eaten(self) -> None:
        self.is_active = False


class SuperPacgum(Edible):
    def __init__(self, position: tuple[int, int], cfg: Config) -> None:
        position = position
        value = cfg.points_per_pacgum
        super().__init__(position=position, value=value)

    def eat(self, actor: "Actor") -> None:
        pass

    def get_eaten(self) -> None:
        self.is_active = False
        # TODO: make ghosts edible


class ActorStatus(IntEnum):
    FLEEING = auto()
    CHASING = auto()
    EATEN = auto()
    SPAWNING = auto()


class Actor(Edible):
    lives: float
    status: ActorStatus
    spawn_position: tuple[int, int]
    spawn_delay: int

    def __init__(
        self,
        value: int,
        lives: float,
        status: ActorStatus,
        spawn_position: tuple[int, int],
        spawn_delay: int,
    ):
        super().__init__(spawn_position, value)
        self.lives = lives
        self.status = status
        self.spawn_position = spawn_position
        self.spawn_delay = spawn_delay

    @abstractmethod
    def move(self, dt: float, direction: Direction | None) -> None: ...

    @abstractmethod
    def respawn(self) -> None: ...

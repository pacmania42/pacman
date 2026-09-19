import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from math import floor

from src.core.settings import Settings

from .maze import Cell, Maze


class Direction(Enum):
    NORTH = ((0, -1), "n")
    EAST = ((1, 0), "e")
    SOUTH = ((0, 1), "s")
    WEST = ((-1, 0), "w")

    @property
    def opposite(self) -> "Direction":
        (dx, dy), _ = self.value
        return next(d for d in Direction if d.value[0] == (-dx, -dy))


class ActorState(Enum):
    ALIVE = auto()
    DYING = auto()
    REBORN = auto()


class Region(Enum):
    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"


@dataclass
class Location:
    x: float
    y: float

    @staticmethod
    def cell_center(pos: tuple[int, int]) -> "Location":
        col, row = pos
        x = (col + 0.5) * Settings.cell_dim
        y = (row + 0.5) * Settings.cell_dim

        return Location(x, y)

    @staticmethod
    def to_cell(center: "Location", maze: Maze) -> Cell:
        col = floor(center.x / Settings.cell_dim)
        row = floor(center.y / Settings.cell_dim)

        return maze.grid[row][col]

    @staticmethod
    def distance(a: "Location", b: "Location") -> float:
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


class Edible(ABC):
    center: Location
    lives: float
    value: int
    maze: Maze
    width: int
    height: int

    def __init__(
        self,
        lives: float,
        value: int,
        position: tuple[int, int],
        size: tuple[int, int],
        maze: Maze,
    ) -> None:
        self.lives = lives
        self.value = value
        self.maze = maze
        self.width = size[0]
        self.height = size[1]
        self.center = Location.cell_center(position)

    @abstractmethod
    def eat(self, edible: "Edible") -> None: ...

    @abstractmethod
    def get_eaten(self) -> None: ...


class Actor(Edible):
    spawn_delay: float
    direction: Direction | None

    def __init__(
        self,
        lives: float,
        value: int,
        maze: Maze,
        region: Region,
        size: tuple[int, int],
        spawn_delay: float,
        speed: int,
    ):
        position = getattr(maze, region.value)

        super().__init__(
            lives=lives, value=value, position=position, size=size, maze=maze
        )
        self.spawn_delay: float = spawn_delay
        self.direction: Direction | None = None
        self.next_direction: Direction | None = None
        self.is_moving: bool = False
        self.facing: Direction = Direction.EAST
        self.respawn_loc = Location(self.center.x, self.center.y)
        self.state = ActorState.ALIVE
        self.state_left = 0.0  # seconds before the current state ends
        self.speed = speed
        self.region = region

    def next_level(self, maze: Maze) -> None:
        self.maze = maze
        region: tuple[int, int] = getattr(maze, self.region.value)
        self.center = Location.cell_center(region)
        self.respawn_loc = Location.cell_center(region)

    def die(self) -> None:
        """start dying (timed)"""
        self.state = ActorState.DYING
        self.state_left = self.spawn_delay
        self.is_moving = False
        self.direction = None
        self.next_direction = None

    def advance_state(self, dt: float) -> None:
        """advance dying and rebirth"""
        if self.state is ActorState.ALIVE:
            return
        self.state_left -= dt
        if self.state_left > 0:
            return
        if self.state is ActorState.DYING:
            self.state = ActorState.REBORN
            self.state_left = self.spawn_delay
            self.center.x = self.respawn_loc.x
            self.center.y = self.respawn_loc.y
        else:
            self.state = ActorState.ALIVE

    def move(self, dt: float, direction: Direction | None) -> None:
        if direction and direction != self.direction:
            self.next_direction = direction

        turn_point = self.end_of_path()

        if self.center == turn_point:
            self.direction = self.next_direction
            self.next_direction = None
            self.is_moving = False
            turn_point = self.end_of_path()
            if self.direction:
                self.facing = self.direction

        if not self.direction:
            return

        self.is_moving = True
        dx, dy = self.direction.value[0]
        next_x = self.center.x + dx * self.speed
        next_y = self.center.y + dy * self.speed

        self.center.x = self._clip(next_x, (self.center.x, turn_point.x))
        self.center.y = self._clip(next_y, (self.center.y, turn_point.y))

    def _clip(self, val: float, boundries: tuple[float, float]) -> float:
        min_boundry = min(boundries)
        max_boundry = max(boundries)
        return max(min_boundry, min(val, max_boundry))

    def end_of_path(self) -> Location:
        cell = Location.to_cell(self.center, self.maze)
        cell_center = Location.cell_center((cell.col, cell.row))

        if self.direction:
            dx, dy = self.direction.value[0]
            passed = (dx * (self.center.x - cell_center.x) > 0) or (
                dy * (self.center.y - cell_center.y) > 0
            )
            if passed and getattr(cell, self.direction.value[1]):
                cell = getattr(cell, self.direction.value[1])

        while self.direction and getattr(cell, self.direction.value[1]):
            if self.next_direction and getattr(
                cell, self.next_direction.value[1]
            ):
                break
            cell = getattr(cell, self.direction.value[1])

        return Location.cell_center((cell.col, cell.row))

    def eat(self, edible: Edible) -> None:
        self.value += edible.value
        edible.get_eaten()

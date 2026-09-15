import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from math import floor

from src.core.settings import Settings

from .maze import Cell, Maze


class Direction(Enum):
    NORTH = ((0, -1), "n")
    EAST = ((1, 0), "e")
    SOUTH = ((0, 1), "s")
    WEST = ((-1, 0), "w")


@dataclass
class Location:
    x: int
    y: int

    @staticmethod
    def from_grid(pos: tuple[int, int]) -> "Location":
        col, row = pos
        x = floor((col + 0.5) * Settings.cell_dim)
        y = floor((row + 0.5) * Settings.cell_dim)

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
        self.center = Location.from_grid(position)

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
        position: tuple[int, int],
        size: tuple[int, int],
        spawn_delay: int,
    ):
        super().__init__(
            lives=lives, value=value, position=position, size=size, maze=maze
        )
        self.spawn_delay: float = spawn_delay
        self.direction: Direction | None = None
        self.facing: Direction = Direction.WEST

    def move(self, dt: float, direction: Direction | None) -> None:
        if not direction:  # continue on the same direction
            direction = self.direction
        else:  # change direction
            self.direction = direction

        if direction is None:
            return

        cell = Location.to_cell(self.center, self.maze)

        # calculate the next position
        dx, dy = direction.value[0]
        next_x = self.center.x + dx * Settings.speed
        next_y = self.center.y + dy * Settings.speed

        next_x = self._clip_x(cell, direction, next_x)
        next_y = self._clip_y(cell, direction, next_y)

        next_center = Location(next_x, next_y)
        self.center = next_center

    def _clip_x(self, cell: Cell, direction: Direction, x: int) -> int:
        if direction == Direction.WEST:
            limit_cell = self._farthest_cell(cell, direction)
            limit = limit_cell.col * Settings.cell_dim + self.width // 2
            return max(limit, x)
        if direction == Direction.EAST:
            limit_cell = self._farthest_cell(cell, direction)
            limit = (limit_cell.col + 1) * Settings.cell_dim - self.width // 2
            return min(x, limit)
        return x

    def _clip_y(self, cell: Cell, direction: Direction, y: int) -> int:
        if direction == Direction.NORTH:
            limit_cell = self._farthest_cell(cell, direction)
            limit = limit_cell.row * Settings.cell_dim + self.height // 2
            return max(limit, y)
        if direction == Direction.SOUTH:
            limit_cell = self._farthest_cell(cell, direction)
            limit = (limit_cell.row + 1) * Settings.cell_dim - self.height // 2
            return min(y, limit)
        return y

    def _farthest_cell(self, cell: Cell, direction: Direction) -> Cell:
        limit_cell = cell
        while getattr(limit_cell, direction.value[1]):
            limit_cell = getattr(limit_cell, direction.value[1])
        return limit_cell

    def eat(self, edible: Edible) -> None:
        self.value += edible.value
        edible.get_eaten()

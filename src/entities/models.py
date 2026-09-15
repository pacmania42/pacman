from abc import ABC, abstractmethod
from enum import Enum

from .maze import Maze


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


class Edible(ABC):
    def __init__(
        self, lives: float, value: int, position: tuple[int, int], maze: Maze
    ) -> None:
        self.lives = lives
        self.value = value
        self.maze = maze

        col, row = position
        self.cell = self.maze.grid[row][col]
        self.cell.edibles.add(self)

    @abstractmethod
    def eat(self, edible: "Edible") -> None: ...

    @abstractmethod
    def get_eaten(self) -> None: ...


class Actor(Edible):
    def __init__(
        self,
        lives: float,
        value: int,
        maze: Maze,
        position: tuple[int, int],
        spawn_delay: int,
    ):
        super().__init__(
            lives=lives, value=value, maze=maze, position=position
        )
        self.spawn_delay = spawn_delay

    def move(self, dt: float, direction: Direction | None) -> None:
        if not direction or not self.cell:
            return

        prev_cell = self.cell

        if direction == Direction.NORTH and self.cell.n:
            curr_cell = self.cell.n

        elif direction == Direction.EAST and self.cell.e:
            curr_cell = self.cell.e

        elif direction == Direction.SOUTH and self.cell.s:
            curr_cell = self.cell.s

        elif direction == Direction.WEST and self.cell.w:
            curr_cell = self.cell.w
        else:
            return

        if not curr_cell:
            return

        prev_cell.edibles.remove(self)
        curr_cell.edibles.add(self)
        self.cell = curr_cell

    def eat(self, edible: Edible) -> None:
        self.value += edible.value
        edible.get_eaten()

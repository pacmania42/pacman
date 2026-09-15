from enum import Enum, IntEnum, auto

from .maze import Maze


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


class Edible:
    lives: float
    value: int
    position: tuple[int, int]
    maze: Maze

    def __init__(
        self, lives: float, value: int, position: tuple[int, int], maze: Maze
    ) -> None:
        col, row = position

        self.lives = lives
        self.value = value
        self.position = position
        self.maze = maze

        # update the cell
        curr_cell = self.maze.grid[row][col]
        curr_cell.edibles.append(self)


class ActorStatus(IntEnum):
    FLEEING = auto()
    CHASING = auto()
    SPAWNING = auto()


class Actor(Edible):
    status: ActorStatus
    spawn_position: tuple[int, int]
    spawn_delay: int

    def __init__(
        self,
        maze: Maze,
        value: int,
        lives: float,
        status: ActorStatus,
        spawn_position: tuple[int, int],
        spawn_delay: int,
    ):
        super().__init__(
            lives=lives, value=value, position=spawn_position, maze=maze
        )

        self.status = status
        self.spawn_position = spawn_position
        self.spawn_delay = spawn_delay

    def move(self, dt: float, direction: Direction | None) -> None:
        # TODO: implement time-based movement calculation
        col, row = self.position
        prev_cell = self.maze.grid[row][col]

        if direction == Direction.NORTH and not prev_cell.n:
            row -= 1
        elif direction == Direction.SOUTH and not prev_cell.s:
            row += 1
        elif direction == Direction.EAST and not prev_cell.e:
            col += 1
        elif direction == Direction.WEST and not prev_cell.w:
            col -= 1
        else:
            return

        col = max(0, min(col, self.maze.width - 1))
        row = max(0, min(row, self.maze.height - 1))
        curr_cell = self.maze.grid[row][col]

        prev_cell.edibles.remove(self)
        self.position = (col, row)
        curr_cell.edibles.append(self)

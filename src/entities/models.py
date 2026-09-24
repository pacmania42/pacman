import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from math import floor

from src.core.settings import Settings

from .maze import Cell, Maze


class Direction(Enum):
    """Represents the four cardinal movement directions."""

    NORTH = ((0, -1), "n")
    EAST = ((1, 0), "e")
    SOUTH = ((0, 1), "s")
    WEST = ((-1, 0), "w")

    @property
    def opposite(self) -> "Direction":
        """Return the direction opposite to this direction.

        Returns:
            The :class:`Direction` pointing in the opposite direction.
        """
        (dx, dy), _ = self.value
        return next(d for d in Direction if d.value[0] == (-dx, -dy))


class ActorState(Enum):
    """Represents the current lifecycle state of an actor."""

    ALIVE = auto()
    DYING = auto()
    REBORN = auto()


class Region(Enum):
    """Identifies predefined spawn and respawn regions in the maze."""

    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"


@dataclass
class Location:
    """Represents a two-dimensional position in the game world.

    Attributes:
        x: Horizontal position in pixels.
        y: Vertical position in pixels.
    """

    x: float
    y: float

    @staticmethod
    def cell_center(pos: tuple[int, int]) -> "Location":
        """Calculate the pixel coordinates of a maze cell's center.

        Args:
            pos: Cell coordinates as ``(column, row)``.

        Returns:
            The pixel location at the center of the specified cell.
        """
        col, row = pos
        x = (col + 0.5) * Settings.cell_dim
        y = (row + 0.5) * Settings.cell_dim

        return Location(x, y)

    @staticmethod
    def to_cell(center: "Location", maze: Maze) -> Cell:
        """Find the maze cell containing a pixel location.

        Args:
            center: Pixel location to convert into cell coordinates.
            maze: Maze containing the target location.

        Returns:
            The :class:`Cell` containing the supplied location.
        """
        col = floor(center.x / Settings.cell_dim)
        row = floor(center.y / Settings.cell_dim)

        return maze.grid[row][col]

    @staticmethod
    def distance(a: "Location", b: "Location") -> float:
        """Calculate the Euclidean distance between two locations.

        Args:
            a: First location.
            b: Second location.

        Returns:
            The distance between ``a`` and ``b`` in pixels.
        """
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


class Edible(ABC):
    """Abstract base class for objects that can interact through eating.

    An edible object has a position, score value, number of lives, size,
    and an associated maze.

    Args:
        lives: Number of lives associated with the object.
        value: Score value awarded when the object is eaten.
        position: Initial maze position as ``(column, row)``.
        size: Object dimensions as ``(width, height)``.
        maze: Maze containing the object.

    Attributes:
        center: Current center position of the object.
        lives: Number of remaining lives.
        value: Score value associated with the object.
        maze: Maze in which the object exists.
        width: Object width in pixels.
        height: Object height in pixels.
    """

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
        """Initialize an edible game object.

        Args:
            lives: Initial number of lives.
            value: Score value of the object.
            position: Initial maze position as ``(column, row)``.
            size: Object dimensions as ``(width, height)``.
            maze: Maze containing the object.
        """
        self.lives = lives
        self.value = value
        self.maze = maze
        self.width = size[0]
        self.height = size[1]
        self.center = Location.cell_center(position)

    @abstractmethod
    def eat(self, edible: "Edible") -> None:
        """Consume another edible object.

        Args:
            edible: Object being consumed.
        """
        ...

    @abstractmethod
    def get_eaten(self) -> None:
        """Handle this object being eaten."""
        ...


class Actor(Edible):
    """Base class for movable entities in the maze.

    Actors can move through the maze, change direction, transition between
    lifecycle states, and interact with other edible objects.

    Args:
        lives: Initial number of lives.
        value: Score value of the actor.
        maze: Maze containing the actor.
        region: Region where the actor is initially spawned.
        size: Actor dimensions as ``(width, height)``.
        spawn_delay: Duration in seconds used for dying and rebirth states.
        speed: Initial movement speed.
        acc: Amount added to the speed when advancing to the next level.

    Attributes:
        spawn_delay: Duration of the spawn/rebirth delay.
        direction: Current movement direction.
        next_direction: Direction requested for the next turn.
        is_moving: Whether the actor is currently moving.
        facing: Direction the actor is visually facing.
        respawn_loc: Position where the actor returns after dying.
        state: Current :class:`ActorState`.
        state_left: Remaining time in the current non-alive state.
        speed: Current movement speed.
        acc: Speed increase applied on the next level.
        region: Region associated with the actor.
    """

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
        speed: float,
        acc: float,
    ):
        """Initialize a movable actor.

        Args:
            lives: Initial number of lives.
            value: Score value of the actor.
            maze: Maze containing the actor.
            region: Initial spawn region.
            size: Actor dimensions as ``(width, height)``.
            spawn_delay: Duration of the dying and rebirth states.
            speed: Initial movement speed.
            acc: Speed increase applied when advancing to a new level.
        """
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
        self.state: ActorState = ActorState.ALIVE
        self.state_left = 0.0  # seconds before the current state ends
        self.speed: float = speed
        self.acc: float = acc
        self.region: Region = region

    def next_level(self, maze: Maze) -> None:
        """Move the actor to a new maze and increase its speed.

        The actor is repositioned at its region's location in the new maze,
        movement state is reset, and speed is increased by the configured
        acceleration.

        Args:
            maze: New maze to associate with the actor.
        """
        self.maze = maze
        region: tuple[int, int] = getattr(maze, self.region.value)
        self.center = Location.cell_center(region)
        self.respawn_loc = Location.cell_center(region)
        self.is_moving = False
        self.direction = None
        self.next_direction = None
        self.speed += self.acc

    def die(self) -> None:
        """Put the actor into the timed dying state.

        Movement and pending direction changes are stopped while the actor
        waits for the configured spawn delay.
        """
        self.state = ActorState.DYING
        self.state_left = self.spawn_delay
        self.is_moving = False
        self.direction = None
        self.next_direction = None

    def advance_state(self, dt: float) -> None:
        """Advance the actor through its dying and rebirth states.

        While the actor is not alive, the remaining state timer is reduced
        by ``dt``. Once the timer expires, the actor transitions from
        ``DYING`` to ``REBORN`` and is moved to its respawn location.
        After the rebirth timer expires, the actor becomes ``ALIVE``.

        Args:
            dt: Elapsed time in seconds since the previous update.
        """
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
        """Move the actor along the maze path.

        A requested direction is stored as the next direction and applied
        when the actor reaches the end of its current path. Movement is
        constrained so the actor cannot move past the next valid turn point.

        Args:
            dt: Elapsed time since the previous update. The current
                implementation does not directly use this value.
            direction: Requested movement direction, if any.
        """
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
        """Clamp a value between two boundary values.

        Args:
            val: Value to constrain.
            boundries: Two values defining the minimum and maximum bounds.

        Returns:
            ``val`` constrained to the inclusive range defined by
            ``boundries``.
        """
        min_boundry = min(boundries)
        max_boundry = max(boundries)
        return max(min_boundry, min(val, max_boundry))

    def end_of_path(self) -> Location:
        """Find the center of the furthest reachable cell in the current
        direction.

        The path continues through connected cells while the actor can keep
        moving in its current direction. A pending direction can stop the
        search when a turn becomes available.

        Returns:
            The location at the center of the actor's current path endpoint.
        """
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
        """Eat another edible object and gain its score value.

        The consumed object's value is added to this actor's value, and
        the consumed object's :meth:`Edible.get_eaten` method is called.

        Args:
            edible: Object to consume.
        """
        self.value += edible.value
        edible.get_eaten()

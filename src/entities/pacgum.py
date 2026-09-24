from src.core.config import Config
from src.core.settings import Settings

from .maze import Maze
from .models import Edible


class Pacgum(Edible):
    """Represents a standard collectible pacgum in the maze.

    A pacgum awards points when eaten and is removed from play by reducing
    its remaining lives.

    Args:
        position: Maze position of the pacgum as ``(column, row)``.
        maze: Maze containing the pacgum.
        config: Game configuration containing the pacgum score value.
    """

    def __init__(
        self, position: tuple[int, int], maze: Maze, config: Config
    ) -> None:
        """Initialize a standard pacgum.

        Args:
            position: Maze position of the pacgum as ``(column, row)``.
            maze: Maze containing the pacgum.
            config: Game configuration used to determine the pacgum value.
        """
        value = config.points_per_pacgum
        size = Settings.pacgum_size
        super().__init__(
            lives=1, value=value, position=position, size=size, maze=maze
        )

    def eat(self, edible: "Edible") -> None:
        """Handle the pacgum eating another edible object.

        Pacgums do not consume other edible objects, so this method has
        no effect.

        Args:
            edible: Edible object that would be consumed.
        """
        return

    def get_eaten(self) -> None:
        """Remove the pacgum after it has been eaten.

        The pacgum's remaining lives are reduced by one.
        """
        self.lives -= 1


class SuperPacgum(Pacgum):
    """Represents a larger, higher-value pacgum.

    A super pacgum behaves like a regular :class:`Pacgum`, but uses a
    different size and awards the configured super-pacgum score.

    Args:
        position: Maze position of the super pacgum as ``(column, row)``.
        maze: Maze containing the super pacgum.
        config: Game configuration containing the super pacgum score value.
    """

    def __init__(
        self, position: tuple[int, int], maze: Maze, config: Config
    ) -> None:
        """Initialize a super pacgum.

        Args:
            position: Maze position of the super pacgum as ``(column, row)``.
            maze: Maze containing the super pacgum.
            config: Game configuration used to determine the score value.
        """
        super().__init__(position=position, config=config, maze=maze)
        self.width, self.height = Settings.superpacgum_size
        self.value = config.points_per_superpacgum

from src.core.config import Config
from src.core.settings import Settings

from .maze import Maze
from .models import Actor, Region


class PlayerError(Exception):
    """Raised when an error occurs while handling the player."""

    pass


class Player(Actor):
    """Represents the player-controlled actor in the maze.

    The player starts in the center region of the maze and uses the
    configured number of lives, movement speed, and acceleration.

    Args:
        cfg: Game configuration containing player settings and cheat options.
    """

    def __init__(self, cfg: Config) -> None:
        """Initialize the player.

        The player's initial speed and acceleration depend on whether the
        speedy-player cheat is enabled.

        Args:
            cfg: Game configuration used to determine the player's lives,
                movement settings, and cheat state.
        """
        value = 0
        lives = cfg.lives
        region = Region.CENTER
        spawn_delay = Settings.player_spawn_delay
        size = Settings.player_size

        speed, acc = (
            (Settings.player_speed_init, Settings.player_acc)
            if not cfg.speedy_player_cheat
            else (Settings.ch_player_speed_init, Settings.ch_player_acc)
        )

        maze = Maze(14, 14, 0)
        super().__init__(
            maze=maze,
            value=value,
            lives=lives,
            region=region,
            size=size,
            spawn_delay=spawn_delay,
            speed=speed,
            acc=acc,
        )

    def get_eaten(self) -> None:
        """Handle the player being eaten.

        One life is removed from the player. If the player still has
        remaining lives, the player enters the dying state and will
        subsequently respawn.
        """
        self.lives -= 1
        if self.lives:
            self.die()

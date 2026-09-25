import time
from typing import Any

from src.core.config import ConfigError, ConfigLoader
from src.core.context import Context
from src.core.highscore import HighScore
from src.core.input import EventBuffer, InputTracker
from src.core.scene_stack import SceneStack
from src.core.settings import Settings
from src.core.window import Window, WindowError
from src.entities.maze import MazeError


class Game:
    """Main application controller.

    The game initializes the application context, input handling, scene
    stack, and rendering window. It then enters the MLX event loop and
    updates and renders the active scene at the configured tick rate.

    Args:
        ctx: Application context containing shared game resources and
            configuration.

    Attributes:
        ctx: Application-wide context.
        scenes: Stack containing the currently active game scenes.
        input: Tracks and processes user input.
        window: MLX window used for rendering.
        last_tick: Monotonic timestamp of the previous game update.
    """

    def __init__(self, ctx: Context) -> None:
        """Initialize the game and start the main window loop.

        Args:
            ctx: Application context containing configuration and shared
                resources.
        """
        self.ctx = ctx
        self.scenes = SceneStack(self.ctx)
        events = EventBuffer()
        self.input = InputTracker(Settings.bindings, events)
        self.window = Window(events, self.game_loop)
        self.last_tick = 0.0
        self.window.show()

    def game_loop(self, _: Any) -> None:
        """Process one iteration of the application event loop.

        The game loop limits updates according to the configured tick
        interval. When an update is due, input is processed, the active
        scenes are updated and drawn, and the resulting back buffer is
        displayed.

        If the scene stack requests termination, the MLX window is closed.

        Args:
            _: Event parameter supplied by MLX. It is intentionally unused.
        """
        now = time.monotonic()
        if now >= self.last_tick + Settings.tick:
            self.last_tick = now
            try:
                self.scenes.update(self.input.begin_frame())
            except MazeError as e:
                print(f"Error: {e}")
                self.scenes.quit()
            if self.scenes.should_quit:
                self.window.exit(None)
                return
            self.window.fill(Settings.off_color)
            self.scenes.draw(self.window)
            self.window.draw_image()


def main() -> None:
    """Load configuration and start the game.

    Configuration errors are printed and prevent the game from starting.
    When configuration loading succeeds, the application context is created
    with the configured highscore storage and passed to :class:`Game`.
    """
    try:
        config = ConfigLoader().load()
    except ConfigError as e:
        print(e)
        return

    try:
        Game(
            Context(
                config=config,
                highscore=HighScore(config.highscore_filename),
            )
        )
    except WindowError as e:
        print(f"Error: {e}")

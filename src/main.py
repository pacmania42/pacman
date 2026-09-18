import time
from typing import Any

from src.core.config import ConfigError, ConfigLoader
from src.core.context import Context
from src.core.highscore import HighScore
from src.core.input import EventBuffer, InputTracker
from src.core.scene_stack import SceneStack
from src.core.settings import Settings
from src.core.window import Window


class Game:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.scenes = SceneStack(self.ctx)
        events = EventBuffer()
        self.input = InputTracker(Settings.bindings, events)
        self.window = Window(events, self.game_loop)
        self.last_tick = 0.0
        self.window.show()

    def game_loop(self, _: Any) -> None:
        now = time.monotonic()
        if now >= self.last_tick + Settings.tick:
            self.last_tick = now
            self.scenes.update(self.input.begin_frame())
            if self.scenes.should_quit:
                self.window.exit(None)
                return
            self.window.fill(Settings.off_color)
            self.scenes.draw(self.window)
            self.window.draw_image()


def main() -> None:
    try:
        config = ConfigLoader().load()
    except ConfigError as e:
        print(e)
        return

    Game(
        Context(
            config=config,
            highscore=HighScore(config.highscore_filename),
        )
    )

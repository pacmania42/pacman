from typing import Any

from src.core.config import Config, ConfigError, ConfigLoader
from src.core.highscore import HighScore
from src.core.input import EventBuffer, InputTracker
from src.core.scene_stack import SceneStack
from src.core.settings import Settings
from src.core.window import Window


class Game:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.scenes = SceneStack(config)
        events = EventBuffer()
        self.input = InputTracker(Settings.bindings, events)
        self.window = Window(events, self.game_loop)
        self.window.show()

    def game_loop(self, _: Any) -> None:
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
    try:
        highscore = HighScore(config.highscore_filename)
    except Exception as e:
        print(f"Error by loading highscore: {e}")
        return

    Game(config)

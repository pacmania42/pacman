from typing import Any

from src.pacman.core.config import Config, ConfigError, ConfigLoader
from src.pacman.core.input import EventBuffer, InputTracker
from src.pacman.core.settings import Settings
from src.pacman.core.window import Window
from src.pacman.ui.scene_id import SceneId
from src.pacman.ui.scene_stack import SceneStack, build_scene_stack


class Game:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.scenes: SceneStack = build_scene_stack()
        self.scenes.push(SceneId.MENU)
        events = EventBuffer()
        self.input = InputTracker(Settings.bindings, events)
        self.window = Window(events, self.game_loop)
        self.window.show()

    def game_loop(self, _: Any) -> None:
        self.window.clear()
        self.scenes.update(self.input.begin_frame())
        if self.scenes.should_quit:
            self.window.exit(None)
            return
        self.scenes.draw(self.window)


def main() -> None:
    try:
        config = ConfigLoader().load()
    except ConfigError as e:
        print(e)
        return

    Game(config)

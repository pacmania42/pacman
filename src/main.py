from typing import Any

from src.core.config import Config, ConfigError, ConfigLoader
from src.core.input import EventBuffer, InputTracker
from src.core.scene_id import SceneId
from src.core.scene_stack import SceneStack, build_scene_stack
from src.core.settings import Settings
from src.core.window import Window


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

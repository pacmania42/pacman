from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Generator

from src.pacman.config import ConfigLoader, ParserError
from src.pacman.input import EventBuffer, InputTracker
from src.pacman.scene_id import SceneId
from src.pacman.scene_stack import SceneStack, build_scene_stack
from src.pacman.settings import Settings
from src.pacman.window import Window


class Game:
    def __init__(self) -> None:
        self.stg = Settings()
        self.scenes: SceneStack = build_scene_stack()
        self.scenes.push(SceneId.MENU)
        events = EventBuffer()
        self.input = InputTracker(self.stg.bindings, events)
        self.window = Window(self.stg, events, self.game_loop)
        self.testc = TestScene(self.window)
        self.window.show()

    def game_loop(self, _: Any) -> None:
        self.window.clear()
        self.scenes.update(self.input.begin_frame())
        if self.scenes.should_quit:
            self.window.exit(None)
            return
        self.scenes.draw(self.window)


class TestScene:
    def __init__(self, window: Window) -> None:
        self.window = window
        self.counter = self.test_counter()
        self.val = 0

    def update(self) -> None:
        try:
            self.val = next(self.counter)
        except StopIteration:
            pass

    def draw(self) -> None:
        self.window.write(0, 0, 0x0000FF, str(self.val))

    def test_counter(self) -> Generator[int, None, None]:
        count = 0
        while True:
            count += 1
            yield count


def parse_cmd_args() -> Namespace:
    parser = ArgumentParser(
        prog="uv run python pac-man.py",
        description="Pacman clone.",
    )
    parser.add_argument("config", metavar="<CONFIG>")
    return parser.parse_args()


def main() -> None:
    args = parse_cmd_args()
    try:
        config = ConfigLoader().load(Path(args.config))
    except ParserError as e:
        print(e)
        return
    print(config.model_dump_json(indent=4))

    Game()

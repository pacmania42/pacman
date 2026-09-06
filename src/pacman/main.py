from typing import Any, Dict, Generator

from src.pacman.scene_id import SceneId
from src.pacman.scene_stack import SceneStack, build_scene_stack
from src.pacman.settings import Settings
from src.pacman.window import Window


class Game:
    def __init__(self) -> None:
        self.stg = Settings()
        self.inputs: Dict[str, bool] = {
            "UP": False,
            "LEFT": False,
            "RIGHT": False,
            "DOWN": False,
            "SPACE": False,
            "ENTER": False,
            "ESCAPE": False,
            "P": False
        }
        self.scenes: SceneStack = build_scene_stack()
        self.scenes.push(SceneId.MENU)
        self.window = Window(self.stg, self.game_loop)
        self.testc = TestScene(self.window)
        self.window.show()

    def game_loop(self, _: Any) -> None:
        self.window.clear()
        self.scenes.update(self.inputs)
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


def main() -> None:
    Game()

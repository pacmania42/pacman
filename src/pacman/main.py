from typing import Any, Callable, Generator

from mlx.mlx import Mlx

from src.pacman.settings import Settings
from src.pacman.window import Window


class Game:
    def __init__(self) -> None:
        self.stg = Settings()
        self.window = Window(self.stg, self.game_loop)
        self.testc = TestScene(self.window)
        self.window.show()

    def game_loop(self, _: Any) -> None:
        self.testc.update()
        self.testc.draw()
        self.window.clear()



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

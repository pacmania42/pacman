from src.pacman.core.input import Action, InputState
from src.pacman.core.window import Window
from src.pacman.ui.scene import Scene
from src.pacman.ui.scene_id import SceneId
from src.pacman.ui.transitions import Push, Quit, Replace, Transition


class Menu:
    def __init__(self) -> None:
        self.items: list[str] = ["Start", "Instructions", "Highscore", "Exit"]
        self.current: int = 0

    def _move(self, n: int) -> None:
        self.current = (n + self.current) % len(self.items)

    def move_down(self) -> None:
        self._move(1)

    def move_up(self) -> None:
        self._move(-1)

    def get_items(self) -> list[str]:
        return self.items

    def get_item(self) -> str:
        return self.items[self.current]


class MenuScene(Scene):
    def __init__(self) -> None:
        super().__init__()

        self.menu = Menu()

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.DOWN):
            self.menu.move_down()
        elif inputs.was_pressed(Action.UP):
            self.menu.move_up()
        elif inputs.was_pressed(Action.BACK):
            return Quit()
        elif inputs.was_pressed(Action.CONFIRM):
            action = self.menu.get_item()
            if action == "Start":
                return Replace(SceneId.GAMEPLAY)
            if action == "Instructions":
                return Push(SceneId.INSTRUCTIONS)
            if action == "Highscore":
                return Push(SceneId.HIGHSCORE)
            if action == "Exit":
                return Quit()
        return None

    def draw(self, window: Window) -> None:
        COLOR_WHITE = 0xFFFFFF
        COLOR_RED = 0x0000FF

        for i, item in enumerate(self.menu.get_items()):
            color = COLOR_RED if self.menu.current == i else COLOR_WHITE
            window.write(100, 300 + i * 20, color, item)

        window.write(50, 50, COLOR_WHITE, "Main Menu")
        window.write(50, 100, COLOR_WHITE, "Press ESC to Exit")

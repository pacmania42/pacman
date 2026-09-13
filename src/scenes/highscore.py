from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.transitions import Pop, Transition
from src.core.window import Window


class HighScoreScene(Scene):
    def update(self, inputs: InputState) -> Transition:
        if inputs.any_pressed(Action.CONFIRM, Action.BACK):
            return Pop()
        return None

    def draw(self, window: Window) -> None:
        window.write(50, 50, 0xFFFFFF, "High Scores")

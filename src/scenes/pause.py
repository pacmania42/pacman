from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.transitions import Pop, Transition
from src.core.window import Window


class PauseScene(Scene):
    is_overlay = True

    def update(self, inputs: InputState) -> Transition:
        if inputs.any_pressed(Action.PAUSE, Action.BACK):
            return Pop()
        return None

    def draw(self, window: Window) -> None:
        window.put_text(400, 400, color=0xFFFF00, text="PAUSED")

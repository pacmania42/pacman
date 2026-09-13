from typing import Any, Optional

from src.core.context import Context
from src.core.highscore import HighscoreItem
from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.transitions import Pop, Transition
from src.core.window import Window


class HighScoreScene(Scene):
    def __init__(self, ctx: Context) -> None:
        super().__init__()
        self.ctx = ctx
        self.fresh: Optional[HighscoreItem] = None

    def on_enter(self, payload: Optional[Any] = None) -> None:
        """Select the highscore entry passed as payload"""
        self.fresh = payload if isinstance(payload, HighscoreItem) else None

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.BACK):
            return Pop()

        return None

    def draw(self, window: Window) -> None:
        return None

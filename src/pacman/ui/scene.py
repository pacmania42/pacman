from typing import Any, Optional

from src.pacman.core.input import InputState
from src.pacman.core.window import Window
from src.pacman.ui.transitions import Transition


class Scene:
    """Base class for stackable scenes."""

    is_overlay: bool = False
    """This scene does not cover the screen: draw the one below
    it first."""

    def __init__(self) -> None:
        pass

    def on_enter(self, payload: Optional[Any] = None) -> None:
        """Called when this scene is added to the stack."""
        pass

    def on_exit(self) -> None:
        """Called when this scene is removed from the stack."""
        pass

    def on_resume(self, result: Optional[Any] = None) -> None:
        """Called when the scene above this one is popped.

        `result` is whatever that scene handed back through `Pop`.
        """
        pass

    def on_suspend(self) -> None:
        """Called when a new scene is pushed on top of this one."""
        pass

    def update(self, inputs: InputState) -> Transition:
        """Advance one frame and return the transition we want, if any."""
        return None

    def draw(self, window: Window) -> None:
        pass

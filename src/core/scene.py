from typing import Any, Optional

from src.core.input import InputState
from src.core.transitions import Transition
from src.core.window import Window


class Scene:
    """Base class for stackable scenes."""

    is_overlay: bool = False
    """This scene does not cover the screen: draw the one below
    it first."""

    clock: float
    """how long has this screen been on view, resets when
    the scene is rebuilt
    """

    def __init__(self) -> None:
        """Create a scene with its animation clock set to zero"""
        self.clock = 0.0

    def advance(self, dt: float) -> None:
        """Increment the animation clock by one frame.

        Args:
            dt: Time elapsed since the previous frame"""
        self.clock += dt

    def on_enter(self, payload: Optional[Any] = None) -> None:
        """Called when this scene is added to the stack.

        Args:
            payload: Optional data passed to the scene"""
        pass

    def on_exit(self) -> None:
        """Called when this scene is removed from the stack"""
        pass

    def on_resume(self, result: Optional[Any] = None) -> None:
        """Called when the scene above this one is popped.

        `result` is whatever that scene handed back through `Pop`.

        Args:
            result: Optional result returned by the popped scene"""
        pass

    def on_suspend(self) -> None:
        """Called when a new scene is pushed on top of this one"""
        pass

    def update(self, inputs: InputState) -> Transition:
        """Advance one frame and return the transition we want, if any.

        Args:
            inputs: Current input state.

        Returns:
            The requested scene transition, or None.
        """
        return None

    def draw(self, window: Window) -> None:
        """Draw the scene to the window.

        Args:
            window: Window used for drawing
        """
        pass

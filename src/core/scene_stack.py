from typing import Any, Callable, Dict, List, Optional

from src.core.context import Context
from src.core.input import InputState
from src.core.scene import Scene
from src.core.scene_id import SceneId
from src.core.transitions import Pop, Push, Quit, Replace, Transition
from src.core.window import Window
from src.scenes import (
    GameplayScene,
    HighScoreScene,
    InstructionsScene,
    MenuScene,
    PauseScene,
)


class SceneStack:
    """A Last-In-First-Out stack of scenes."""

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.factories: Dict[SceneId, Callable[[Context], Scene]] = {}
        self.stack: List[Scene] = []
        self.should_quit = False

        self.register(SceneId.GAMEPLAY, GameplayScene)
        self.register(SceneId.PAUSE, PauseScene)
        self.register(SceneId.HIGHSCORE, HighScoreScene)
        self.register(SceneId.INSTRUCTIONS, InstructionsScene)
        self.register(SceneId.MENU, MenuScene)

        self.push(SceneId.MENU)

    def register(
        self, name: SceneId, factory: Callable[[Context], Scene]
    ) -> None:
        """Bind an id to the factory that builds that scene."""
        self.factories[name] = factory

    def _build(self, name: SceneId) -> Scene:
        """Build a fresh instance, so state never leaks between visits."""
        if name not in self.factories:
            raise ValueError(f"Scene '{name.value}' is not registered.")
        return self.factories[name](self.ctx)

    def push(self, name: SceneId, payload: Optional[Any] = None) -> None:
        """Pushes a new scene to the top of the stack"""
        # Build first: an unknown scene must not disturb the stack.
        new_scene = self._build(name)

        # Suspend the current top scene if it exists
        if self.stack:
            self.stack[-1].on_suspend()

        self.stack.append(new_scene)
        new_scene.on_enter(payload)

    def pop(self, result: Optional[Any] = None) -> None:
        """Removes the top scene, returning to the previous one"""
        if not self.stack:
            return

        # Clean up the exiting scene
        exiting_scene: Scene = self.stack.pop()
        exiting_scene.on_exit()

        # Resume the scene underneath
        if self.stack:
            self.stack[-1].on_resume(result)

    def replace(self, name: SceneId, payload: Optional[Any] = None) -> None:
        """Swaps the top scene for another, keeping the stack depth.

        The scene below is never resumed, so it gets no callback.
        """
        new_scene = self._build(name)

        if self.stack:
            self.stack.pop().on_exit()

        self.stack.append(new_scene)
        new_scene.on_enter(payload)

    def quit(self) -> None:
        """Unwinds the whole stack and flags the game to stop."""
        while self.stack:
            self.stack.pop().on_exit()
        self.should_quit = True

    def apply_transition(self, intent: Transition) -> None:
        """Carries out what a scene asked for, once its update returned."""
        if intent is None:
            return
        if isinstance(intent, Push):
            self.push(intent.name, intent.payload)
        elif isinstance(intent, Replace):
            self.replace(intent.name, intent.payload)
        elif isinstance(intent, Pop):
            self.pop(intent.result)
        elif isinstance(intent, Quit):
            self.quit()

    def update(self, inputs: InputState) -> None:
        """Only update the top-most scene on the stack"""
        if not self.stack:
            return

        # The stack is only ever mutated here, never mid-update.
        intent = self.stack[-1].update(inputs)
        self.apply_transition(intent)

    def draw(self, window: Window) -> None:
        """Render the top scene, plus any scenes it overlays."""
        if not self.stack:
            return

        bottom = len(self.stack) - 1
        while bottom > 0 and self.stack[bottom].is_overlay:
            bottom -= 1

        for scene in self.stack[bottom:]:
            scene.draw(window)

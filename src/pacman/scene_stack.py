from typing import Any, Callable, Dict, List, Optional

from src.pacman.input import Action, InputState
from src.pacman.scene import Scene
from src.pacman.scene_id import SceneId
from src.pacman.transitions import Pop, Push, Quit, Replace, Transition
from src.pacman.window import Window


class GameplayScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.current_level = 1

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.PAUSE):
            return Push(SceneId.PAUSE)
        return None

    def draw(self, window: Window) -> None:
        window.write(50, 50, 0xFFFFFF, f"Level: {self.current_level}")

    def on_resume(self, result: Optional[Any] = None) -> None:
        print("Resume gameplay")


class PauseScene(Scene):
    is_overlay = True

    def update(self, inputs: InputState) -> Transition:
        if inputs.any_pressed(Action.PAUSE, Action.BACK):
            return Pop()
        return None

    def draw(self, window: Window) -> None:
        window.write(400, 400, 0xFFFF00, "PAUSED")


class HighScoreScene(Scene):
    def update(self, inputs: InputState) -> Transition:
        if inputs.any_pressed(Action.CONFIRM, Action.BACK):
            return Pop()
        return None

    def draw(self, window: Window) -> None:
        window.write(50, 50, 0xFFFFFF, "High Scores")


class InstructionsScene(Scene):
    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.BACK):
            return Pop()
        return None

    def draw(self, window: Window) -> None:
        window.write(50, 50, 0xFFFFFF, "Instructions Scene")


class MenuScene(Scene):
    def update(self, inputs: InputState) -> Transition:
        return None

    def draw(self, window: Window) -> None:
        window.write(50, 50, 0xFFFFFF, "Menu Scene")


class SceneStack:
    """A Last-In-First-Out stack of scenes."""

    def __init__(self) -> None:
        self.factories: Dict[SceneId, Callable[[], Scene]] = {}
        self.stack: List[Scene] = []
        self.should_quit = False

    def register(self, name: SceneId, factory: Callable[[], Scene]) -> None:
        """Bind an id to the factory that builds that scene."""
        self.factories[name] = factory

    def _build(self, name: SceneId) -> Scene:
        """Build a fresh instance, so state never leaks between visits."""
        if name not in self.factories:
            raise ValueError(f"Scene '{name.value}' is not registered.")
        return self.factories[name]()

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

    def replace(
        self, name: SceneId, payload: Optional[Any] = None
    ) -> None:
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


def build_scene_stack() -> SceneStack:
    """Registers every scene. The caller decides which one starts."""
    scenes = SceneStack()

    scenes.register(SceneId.GAMEPLAY, GameplayScene)
    scenes.register(SceneId.PAUSE, PauseScene)
    scenes.register(SceneId.HIGHSCORE, HighScoreScene)
    scenes.register(SceneId.INSTRUCTIONS, InstructionsScene)
    scenes.register(SceneId.MENU, MenuScene)

    return scenes

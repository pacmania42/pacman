from typing import Any, Dict, List, Optional


# tmp Context for test this should be in Game file
class Context:
    def __init__(self, mlx_instance, mlx_ptr, mlx_win) -> None:
        self.m = mlx_instance
        self.mlx_ptr: Any = mlx_ptr
        self.mlx_win = mlx_win



class Scene:
    """Base class for stackable scenes."""

    def __init__(self, manager: "SceneStackManager") -> None:
        self.manager: SceneStackManager = manager

    def on_push(self, payload: Optional[Dict[str, Any]] = None) -> None:
        """Called when this scene is added to the stack."""
        pass

    def on_pop(self) -> None:
        """Called when this scene is removed from the stack."""
        pass

    def on_focus_gained(self) -> None:
        """Called when a scene above this one is popped, returning focus here."""
        pass

    def on_focus_lost(self) -> None:
        """Called when a new scene is pushed on top of this one."""
        pass

    def update(self, inputs: Dict[str, bool]) -> None:
        pass

    def draw(self, context: Context) -> None:
        pass


class GameplayScene(Scene):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.current_level = 1

    def update(self, inputs: Dict[str, bool]) -> None:
        print(f"Level: {self.current_level}")

        if inputs["P"]:
            print("Pause pressed, Pushing PauseScene...")
            self.manager.push("Pause")

    def draw(self, context: Context) -> None:
        pass

    def on_focus_gained(self) -> None:
        print("Resume gameplay")


class PauseScene(Scene):
    def update(self, inputs: Dict[str, bool]) -> None:
        print("Game Paused")

        if inputs["P"]:
            self.manager.pop()

    def draw(self, context: Context) -> None:
        pass


class HighScoreScene(Scene):
    def update(self, inputs: Dict[str, bool]) -> None:
        pass

    def draw(self, context: Context) -> None:
        pass


class InstructionsScene(Scene):
    def update(self, inputs: Dict[str, bool]) -> None:
        pass

    def draw(self, context: Context) -> None:
        pass


class MenuScene(Scene):
    def update(self, inputs: Dict[str, bool]) -> None:
        pass

    def draw(self, context: Context) -> None:
        #self.m, self.mlx_ptr, self.mlx_win
        pass


class SceneStackManager:
    """Manages scenes using a Stack (Last-In, First-Out)"""

    def __init__(self) -> None:
        self.registered_scenes: Dict[str, Scene] = {}
        self.stack: List[Scene] = []

    def register(self, name: str, scene: Scene) -> None:
        self.registered_scenes[name] = scene

    def push(
        self, name: str, payload: Optional[Dict[str, Any]] = None
    ) -> None:
        """Pushes a new scene to the top of the stack"""
        if name not in self.registered_scenes:
            raise ValueError(f"Scene '{name}' is not registered.")

        # Blur the current top scene if it exists
        if self.stack:
            self.stack[-1].on_focus_lost()

        # Get the new scene and add it to the stack
        new_scene: Scene = self.registered_scenes[name]
        self.stack.append(new_scene)

        # Initialize it
        new_scene.on_push(payload)

    def pop(self) -> None:
        """Removes the top scene, returning to the previous one"""
        if not self.stack:
            return

        # Clean up the exiting scene
        exiting_scene: Scene = self.stack.pop()
        exiting_scene.on_pop()

        # Restore focus to the underlying scene
        if self.stack:
            self.stack[-1].on_focus_gained()

    def update(self, inputs: Dict[str, bool]) -> None:
        """Only update the top-most scene on the stack"""
        if self.stack:
            self.stack[-1].update(inputs)

    def draw(self, context: Context) -> None:
        """
        Render scenes
        """
        if not self.stack:
            return

        # Simple approach: If we want the pause menu to overlay the game,
        # we can draw the last two scenes if the top one is a popup/pause.
        if len(self.stack) > 1:
            self.stack[-2].draw(context)

        self.stack[-1].draw(context)


###################################### TODO remove or refactor after this, this is to test purpose

from mlx import Mlx


def close_window() -> None:
    m.mlx_loop_exit(mlx_ptr)


def keypress(keycode, data) -> None:
    print(f"k {keycode}")
    if keycode == 97:
        print("mmmmmm")
    if keycode == 65307:  # ESC
        close_window()


def event(event) -> None:
    if event == "close":
        close_window()


class Game:
    def __init__(self, context: Context) -> None:
        self.context = context

        self.inputs: Dict[str, bool] = {
            "W": False,
            "A": False,
            "S": False,
            "D": False,
            "SPACE": False,
            "ENTER": False,
            "ESCAPE": False,
            "P": False,
        }

        self.manager = SceneStackManager()

        self.manager.register("Gameplay", GameplayScene(self.manager))
        self.manager.register("Pause", PauseScene(self.manager))
        self.manager.register("HighScore", HighScoreScene(self.manager))
        self.manager.register("Instructions", InstructionsScene(self.manager))
        self.manager.register("Menu", MenuScene(self.manager))

        self.manager.push("Gameplay")

    def updateKeypress(self, key, b):
        print(key)
        print(b)
        if key == 112:
            self.inputs["P"] = not self.inputs["P"]
        pass

    def gameloopUpdate(self, param) -> None:
        self.manager.update(self.inputs)
        self.manager.draw(self.context)


if __name__ == "__main__":

    m = Mlx()
    mlx_ptr = m.mlx_init()
    win_ptr = m.mlx_new_window(mlx_ptr, 800, 800, "jjjjj")

    game = Game(Context(m, mlx_ptr, win_ptr))

    m.mlx_key_hook(win_ptr, keypress, None)
    m.mlx_hook(win_ptr, 2, 1 << 0, keypress, None)  # keydown
    m.mlx_hook(win_ptr, 33, 0, event, "close")  # win x icon

    m.mlx_hook(
        win_ptr,
        2,
        1 << 0,
        lambda input, b: game.updateKeypress(input, b),
        None,
    )

    m.mlx_loop_hook(mlx_ptr, game.gameloopUpdate, None)

    m.mlx_loop(mlx_ptr)

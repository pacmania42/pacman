from typing import Any, Optional

from src.core.config import Config
from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.scene_id import SceneId
from src.core.settings import Settings
from src.core.transitions import Push, Transition
from src.core.window import Window
from src.game_state import GameState
from src.ui.game_view import GameView


class GameplayScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.stg = Settings()
        self.config = Config()  # TODO: get the instance
        self.game = GameState(config=self.config, settings=self.stg)
        self.view = GameView(self.stg)

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.PAUSE):
            return Push(SceneId.PAUSE)
        self.game.update(Settings.tick, None)
        self.view.tick(Settings.tick)
        return None

    def draw(self, window: Window) -> None:
        self.view.draw(window, self.game)

    def on_resume(self, result: Optional[Any] = None) -> None:
        print("Resume gameplay")

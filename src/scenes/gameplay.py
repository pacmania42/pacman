from typing import Any, Optional

from src.core.context import Context
from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.scene_id import SceneId
from src.core.settings import Settings
from src.core.transitions import Push, Quit, Transition
from src.core.window import Window
from src.entities import Direction
from src.game_state import GameState
from src.ui.game_view import GameView


class GameplayScene(Scene):
    def __init__(self, ctx: Context) -> None:
        super().__init__()
        self.stg = Settings()
        self.config = ctx.config
        self.game = GameState(config=self.config, settings=self.stg)
        self.view = GameView(self.stg)

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.PAUSE):
            self.game.pause_game()
            return Push(SceneId.PAUSE)
        elif inputs.was_pressed(Action.BACK):
            return Quit()

        elif inputs.was_pressed(Action.UP):
            self.game.move_player(direction=Direction.NORTH)
        elif inputs.was_pressed(Action.DOWN):
            self.game.move_player(direction=Direction.SOUTH)
        elif inputs.was_pressed(Action.RIGHT):
            self.game.move_player(direction=Direction.EAST)
        elif inputs.was_pressed(Action.LEFT):
            self.game.move_player(direction=Direction.WEST)

        self.game.update(Settings.tick, None)
        self.view.tick(Settings.tick)
        return None

    def draw(self, window: Window) -> None:
        self.view.draw(window, self.game)

    def on_resume(self, result: Optional[Any] = None) -> None:
        self.game.resume_game()

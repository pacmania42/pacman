from typing import Any, Optional

from src.core.context import Context
from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.scene_id import SceneId
from src.core.settings import Settings
from src.core.transitions import Pop, Push, Replace, Transition
from src.core.window import Window
from src.entities import Direction
from src.game_state import GameResult, GameState, GameStatus
from src.scenes.pause import PauseChoice
from src.ui.game_view import GameView


class GameplayScene(Scene):
    def __init__(self, ctx: Context) -> None:
        super().__init__()
        self.stg = Settings()
        self.config = ctx.config
        self.game = GameState(ctx.config)
        self.view = GameView(self.stg)
        self.leaving = False

    def update(self, inputs: InputState) -> Transition:
        if self.game.status == GameStatus.OVER:
            return Replace(
                SceneId.GAMEOVER,
                GameResult(self.game.won, self.game.player.value),
            )
        if self.leaving:
            return Pop()
        if inputs.was_pressed(Action.PAUSE):
            self.game.pause_game()
            return Push(SceneId.PAUSE)
        elif inputs.was_pressed(Action.BACK):
            self.game.pause_game()
            return Push(SceneId.PAUSE)

        wanted_direction = None
        if inputs.was_pressed(Action.UP):
            wanted_direction = Direction.NORTH
        elif inputs.was_pressed(Action.DOWN):
            wanted_direction = Direction.SOUTH
        elif inputs.was_pressed(Action.RIGHT):
            wanted_direction = Direction.EAST
        elif inputs.was_pressed(Action.LEFT):
            wanted_direction = Direction.WEST

        self.game.update(Settings.tick, wanted_direction)
        self.view.tick(Settings.tick)
        return None

    def draw(self, window: Window) -> None:
        self.view.draw(window, self.game)

    def on_resume(self, result: Optional[Any] = None) -> None:
        if result is PauseChoice.MAIN_MENU:
            self.leaving = True
        else:
            self.game.resume_game()

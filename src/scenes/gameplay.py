from typing import Any, Optional

from src.core.config import Config
from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.scene_id import SceneId
from src.core.settings import Settings
from src.core.transitions import Push, Quit, Transition
from src.core.window import Window
from src.entities import Direction, Ghost, Maze, Pacgum, Player, SuperPacgum
from src.game_state import GameState
from src.ui.game_view import GameView


class GameplayScene(Scene):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.stg = Settings()
        self.config = config
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

    def _draw_maze(self, window: Window, maze: Maze) -> None:
        maze_width = maze.width * self.stg.cell_dim
        maze_height = maze.height * self.stg.cell_dim

        window.put_box(0, 0, maze_width, maze_height, 0xFFFFFF)
        window.put_box(
            self.stg.wall_thickness,
            self.stg.wall_thickness,
            maze_width - 2 * self.stg.wall_thickness,
            maze_height - 2 * self.stg.wall_thickness,
            0,
        )
        cells = [cell for row in self.game.maze.grid for cell in row]
        for cell in cells:
            x_offset = cell.col * self.stg.cell_dim
            y_offset = cell.row * self.stg.cell_dim
            if all([cell.n, cell.e, cell.s, cell.w]):
                window.put_box(
                    x_offset + self.stg.wall_thickness,
                    y_offset + self.stg.wall_thickness,
                    self.stg.cell_dim - 2 * self.stg.wall_thickness,
                    self.stg.cell_dim - 2 * self.stg.wall_thickness,
                    0xFF0000,
                )
            if cell.n:
                window.put_box(
                    x_offset,
                    y_offset,
                    self.stg.cell_dim,
                    self.stg.wall_thickness,
                    0xFFFFFF,
                )
            if cell.e:
                window.put_box(
                    x_offset + self.stg.cell_dim - self.stg.wall_thickness,
                    y_offset,
                    self.stg.wall_thickness,
                    self.stg.cell_dim,
                    0xFFFFFF,
                )

    def _draw_player(self, window: Window, player: Player) -> None:
        width = 20
        height = 20
        col, row = player.position

        x = col * self.stg.cell_dim + (self.stg.cell_dim - width) // 2
        y = row * self.stg.cell_dim + (self.stg.cell_dim - height) // 2

        window.put_box(x, y, width, height, 0xFFFF00)

    def _draw_ghosts(
        self, window: Window, ghosts: tuple[Ghost, Ghost, Ghost, Ghost]
    ) -> None:
        width = 20
        height = 20
        colors = [0x00FFFF, 0xFFA500, 0x00FF00, 0xFF0000]
        for ghost, color in zip(ghosts, colors, strict=True):
            col, row = ghost.position
            x = col * self.stg.cell_dim + (self.stg.cell_dim - width) // 2
            y = row * self.stg.cell_dim + (self.stg.cell_dim - height) // 2

            window.put_box(x, y, width, height, color)

    def _draw_superpacgums(
        self,
        window: Window,
        superpacgums: tuple[
            SuperPacgum, SuperPacgum, SuperPacgum, SuperPacgum
        ],
    ) -> None:
        width = 25
        height = 25
        for spg in superpacgums:
            col, row = spg.position
            x = col * self.stg.cell_dim + (self.stg.cell_dim - width) // 2
            y = row * self.stg.cell_dim + (self.stg.cell_dim - height) // 2

            window.put_box(x, y, width, height, 0xDDDDDD)

    def _draw_pacgums(self, window: Window, pacgums: list[Pacgum]) -> None:
        width = 10
        height = 10
        for pg in pacgums:
            col, row = pg.position
            x = col * self.stg.cell_dim + (self.stg.cell_dim - width) // 2
            y = row * self.stg.cell_dim + (self.stg.cell_dim - height) // 2

            window.put_box(x, y, width, height, 0xAA5555)

from typing import Any, Optional

from src.core.config import Config
from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.scene_id import SceneId
from src.core.settings import Settings
from src.core.transitions import Push, Transition
from src.core.window import Window
from src.entities import Ghost, Maze, Pacgum, Player, SuperPacgum
from src.game_state import GameState


class GameplayScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.stg = Settings()
        self.config = Config()  # TODO: get the instance
        self.game = GameState(config=self.config, settings=self.stg)
        self.maze = self.game.maze
        self.player = self.game.player
        self.superpacgums = self.game.superpacgums
        self.pacgums = self.game.pacgums
        self.ghosts = self.game.ghosts

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.PAUSE):
            return Push(SceneId.PAUSE)
        return None

    def draw(self, window: Window) -> None:
        self._draw_maze(window, self.maze)
        self._draw_player(window, self.player)
        self._draw_ghosts(window, self.ghosts)
        self._draw_superpacgums(window, self.superpacgums)
        self._draw_pacgums(window, self.pacgums)

    def on_resume(self, result: Optional[Any] = None) -> None:
        print("Resume gameplay")

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

        x = col * self.stg.cell_dim + (self.stg.cell_dim // 2) - width
        y = row * self.stg.cell_dim + (self.stg.cell_dim // 2) - height

        window.put_box(x, y, width, height, 0xFFFF00)

    def _draw_ghosts(
        self, window: Window, ghosts: tuple[Ghost, Ghost, Ghost, Ghost]
    ) -> None:
        width = 20
        height = 20
        colors = [0x00FFFF, 0xFFA500, 0x00FF00, 0xFF0000]
        for ghost, color in zip(ghosts, colors, strict=True):
            col, row = ghost.position
            x = col * self.stg.cell_dim + (self.stg.cell_dim // 2) - width
            y = row * self.stg.cell_dim + (self.stg.cell_dim // 2) - height

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
            x = col * self.stg.cell_dim + (self.stg.cell_dim // 2) - width
            y = row * self.stg.cell_dim + (self.stg.cell_dim // 2) - height

            window.put_box(x, y, width, height, 0xDDDDDD)

    def _draw_pacgums(self, window: Window, pacgums: list[Pacgum]) -> None:
        width = 10
        height = 10
        for pg in pacgums:
            col, row = pg.position
            x = col * self.stg.cell_dim + (self.stg.cell_dim // 2) - width
            y = row * self.stg.cell_dim + (self.stg.cell_dim // 2) - height

            window.put_box(x, y, width, height, 0xAA5555)

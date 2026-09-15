"""Draws a GameState onto a Window"""

from src.core.settings import Settings
from src.core.sprite import Animation, SpriteId
from src.core.window import Window
from src.entities import (
    Edible,
    Ghost,
    Maze,
    Pacgum,
    Player,
    SuperPacgum,
)
from src.game_state import GameState

PLAYER_IDLE = Animation(SpriteId.SHROOM_IDLE, fps=6)
PLAYER_WALK = Animation(SpriteId.SHROOM_WALK, fps=10)

GHOST_COLORS = (0x00FFFF, 0xFFA500, 0x00FF00, 0xFF0000)


class GameView:
    """Renders the gameplay"""

    def __init__(self, stg: Settings) -> None:
        self.stg = stg
        self.clock = 0.0
        self.player_anim: Animation | None = None
        self.player_anim_start = 0.0
        self.player_flip = False

    def tick(self, dt: float) -> None:
        """Advance the animation clock"""
        self.clock += dt

    def draw(self, window: Window, game: GameState) -> None:
        self._draw_maze(window, game.maze)
        cells = [cell for row in game.maze.grid for cell in row]
        for cell in cells:
            for entity in cell.edibles:
                self._draw_entity(entity, window)

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
        cells = [cell for row in maze.grid for cell in row]
        for cell in cells:
            x_offset = cell.col * self.stg.cell_dim
            y_offset = cell.row * self.stg.cell_dim

            if not any([cell.n, cell.e, cell.s, cell.w]):
                window.put_box(
                    x_offset + self.stg.wall_thickness,
                    y_offset + self.stg.wall_thickness,
                    self.stg.cell_dim - 2 * self.stg.wall_thickness,
                    self.stg.cell_dim - 2 * self.stg.wall_thickness,
                    0x0000FF,
                )

            if not cell.n:
                window.put_box(
                    x_offset,
                    y_offset,
                    self.stg.cell_dim,
                    self.stg.wall_thickness,
                    0xFFFFFF,
                )
            if not cell.e:
                window.put_box(
                    x_offset + self.stg.cell_dim - self.stg.wall_thickness,
                    y_offset,
                    self.stg.wall_thickness,
                    self.stg.cell_dim,
                    0xFFFFFF,
                )

    def _draw_entity(self, entity: Edible, window: Window) -> None:
        if type(entity) is Player:
            color, width, height = (0xFFFF00, 25, 25)
        elif type(entity) is Ghost:
            color, width, height = (0xFF0000, 25, 25)
        elif type(entity) is SuperPacgum:
            color, width, height = (0x0000FF, 20, 20)
        elif type(entity) is Pacgum:
            color, width, height = (0xFFFFFF, 15, 15)

        col, row = entity.cell.col, entity.cell.row
        x = col * self.stg.cell_dim + (self.stg.cell_dim // 2) - width
        y = row * self.stg.cell_dim + (self.stg.cell_dim // 2) - height

        window.put_box(x, y, width, height, color)

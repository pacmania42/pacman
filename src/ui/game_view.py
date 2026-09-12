"""Draws a GameState onto a Window"""

from src.core.settings import Settings
from src.core.sprite import Animation, SpriteId
from src.core.window import Window
from src.entities import Ghost, Maze, Pacgum, Player, SuperPacgum
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

    def tick(self, dt: float) -> None:
        """Advance the animation clock"""
        self.clock += dt

    def draw(self, window: Window, game: GameState) -> None:
        self._draw_maze(window, game.maze)
        self._draw_pacgums(window, game.pacgums)
        self._draw_superpacgums(window, game.superpacgums)
        self._draw_ghosts(window, game.ghosts)
        self._draw_player(window, game.player)

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
        anim = PLAYER_WALK if player.moving else PLAYER_IDLE
        if anim is not self.player_anim:  # state changed: restart at frame 0
            self.player_anim = anim
            self.player_anim_start = self.clock
        t = self.clock - self.player_anim_start
        frame = window.sprites.frame(anim, t)

        col, row = player.position
        x = col * self.stg.cell_dim + (self.stg.cell_dim - frame.width) // 2
        y = row * self.stg.cell_dim + (self.stg.cell_dim - frame.height) // 2

        window.blit(frame, x, y)

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

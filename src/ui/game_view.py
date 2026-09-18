"""Draws a GameState onto a Window"""

import math
from math import floor

from src.core.settings import Settings
from src.core.sprite import Animation, Frame, SpriteId
from src.core.window import Window
from src.entities import Ghost, Maze, Player
from src.entities.models import Direction
from src.entities.pacgum import Pacgum, SuperPacgum
from src.game_state import GameState
from src.ui import theme, ui

PLAYER_IDLE = Animation(SpriteId.SCOUT_IDLE, fps=10)
PLAYER_WALK = Animation(SpriteId.SCOUT_WALK, fps=10)

GHOST_ANIMS: tuple[tuple[Animation, Animation], ...] = tuple(
    (Animation(idle, fps=10), Animation(walk, fps=10))
    for idle, walk in (
        (SpriteId.GHOST_C_IDLE, SpriteId.GHOST_C_WALK),
        (SpriteId.GHOST_O_IDLE, SpriteId.GHOST_O_WALK),
        (SpriteId.GHOST_P_IDLE, SpriteId.GHOST_P_WALK),
        (SpriteId.GHOST_R_IDLE, SpriteId.GHOST_R_WALK),
    )
)

SUPERGUM = Animation(SpriteId.SUPERGUM, fps=6)


class ActorAnim:
    def __init__(self) -> None:
        self.anim: Animation | None = None
        self.start = 0.0
        self.flip = False

    def frame(
        self, window: Window, clock: float, anim: Animation, facing: Direction
    ) -> Frame:
        if anim is not self.anim:  # state changed: restart at frame 0
            self.anim = anim
            self.start = clock
        if facing is Direction.WEST:
            self.flip = True
        elif facing is Direction.EAST:
            self.flip = False
        return window.sprites.frame(anim, clock - self.start)


class GameView:
    """Renders the gameplay"""

    def __init__(self, stg: Settings) -> None:
        self.stg = stg
        self.clock = 0.0
        self.player_anim = ActorAnim()
        self.ghost_anims = tuple(ActorAnim() for _ in GHOST_ANIMS)

    def tick(self, dt: float) -> None:
        """Advance the animation clock"""
        self.clock += dt

    def draw(self, window: Window, game: GameState) -> None:
        self._draw_maze(window, game.maze)
        self._draw_pacgums(window, game.pacgums)
        self._draw_superpacgums(window, game.superpacgums)
        self._draw_ghosts(window, game.ghosts)
        self._draw_player(window, game.player)
        self._draw_hud(window, game)

    def _draw_hud(self, window: Window, game: GameState) -> int:
        """draw score, lives and time

        returns the y of the next line
        """
        top = window.height - 35
        pad = theme.GAP // 2
        band = window.text_height(theme.SCALE_BODY)
        width = window.width
        text_y = pad + (band - window.ink_height(theme.SCALE_BODY)) // 2

        self._draw_info(window, top + text_y, game.player.value, 1)
        self._draw_lives(window, top + pad, band, width, game.player.lives)
        self._draw_time(window, top + text_y, width, game.time_left)
        return top + pad + band + pad

    def _draw_info(
        self, window: Window, y: int, score: int, level: int
    ) -> None:
        window.put_text(0, y, "SCORE", theme.MUTED, theme.SCALE_BODY)
        window.put_text(
            window.text_width("SCORE ", theme.SCALE_BODY),
            y,
            f"{score:06d}",
            theme.TITLE,
            theme.SCALE_BODY,
        )

        x_next = window.text_width("   SCORE 000000", theme.SCALE_BODY)
        window.put_text(
            x_next, y, " |    LEVEL", theme.MUTED, theme.SCALE_BODY
        )
        window.put_text(
            window.text_width(" |    LEVEL ", theme.SCALE_BODY) + x_next,
            y,
            f"{level:02d}",
            theme.TITLE,
            theme.SCALE_BODY,
        )

    def _draw_lives(
        self, window: Window, y: int, band: int, width: int, lives: float
    ) -> None:
        heart = window.sprites.still(SpriteId.HEART)
        count = max(0, int(lives))
        slot = heart.width + theme.GAP // 2
        x = (width - count * slot) // 2
        top = y + (band - heart.height) // 2
        for i in range(count):
            window.blit(heart, x + i * slot, top)

    def _draw_time(
        self, window: Window, y: int, width: int, left: float
    ) -> None:
        left = max(0.0, left)
        color = theme.TEXT
        if left <= 10:  # last 10 seconds
            color = ui.pulse(self.clock, theme.DANGER)

        whole = math.ceil(left)
        text = f"{whole // 60:02d}:{whole % 60:02d}"
        x = width - window.text_width(text, theme.SCALE_BODY)
        window.put_text(x, y, text, color, theme.SCALE_BODY)
        window.put_text(
            x - window.text_width("TIME ", theme.SCALE_BODY),
            y,
            "TIME",
            theme.MUTED,
            theme.SCALE_BODY,
        )

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

    def _draw_actor(
        self,
        window: Window,
        actor: Player | Ghost,
        state: ActorAnim,
        idle: Animation,
        walk: Animation,
    ) -> None:
        """draw blit of the actor's current frame"""
        if not actor.lives:
            return
        anim = walk if actor.moving else idle
        frame = state.frame(
            window,
            self.clock,
            anim,
            actor.direction if actor.direction else Direction.EAST,
        )

        col = actor.center.x
        row = actor.center.y
        x = col - frame.width // 2
        y = row
        y -= frame.height // 2

        window.blit(frame, floor(x), floor(y), flip=state.flip)

    def _draw_player(self, window: Window, player: Player) -> None:
        self._draw_actor(
            window, player, self.player_anim, PLAYER_IDLE, PLAYER_WALK
        )

    def _draw_ghosts(self, window: Window, ghosts: set[Ghost]) -> None:
        for ghost, state, (idle, walk) in zip(
            ghosts, self.ghost_anims, GHOST_ANIMS, strict=True
        ):
            self._draw_actor(window, ghost, state, idle, walk)

    def _draw_superpacgums(
        self,
        window: Window,
        superpacgums: set[SuperPacgum],
    ) -> None:
        frame = window.sprites.frame(SUPERGUM, self.clock)
        x_pad = frame.width // 2
        y_pad = frame.height // 2
        for spg in [spg for spg in superpacgums if spg.lives]:
            x = spg.center.x - x_pad
            y = spg.center.y - y_pad

            window.blit(frame, floor(x), floor(y))

    def _draw_pacgums(self, window: Window, pacgums: set[Pacgum]) -> None:
        gum = window.sprites.still(SpriteId.GUM)
        x_pad = gum.width // 2
        y_pad = gum.height // 2
        for pg in [pg for pg in pacgums if pg.lives]:
            x = pg.center.x - x_pad
            y = pg.center.y - y_pad

            window.blit(gum, floor(x), floor(y))

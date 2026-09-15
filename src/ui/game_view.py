"""Draws a GameState onto a Window"""

from src.core.settings import Settings
from src.core.sprite import Animation, Frame, SpriteId
from src.core.window import Window
from src.entities import Direction, Ghost, Maze, Pacgum, Player, SuperPacgum
from src.game_state import GameState

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

    def _draw_actor(
        self,
        window: Window,
        actor: Player | Ghost,
        state: ActorAnim,
        idle: Animation,
        walk: Animation,
    ) -> None:
        """draw blit of the actor's current frame"""
        anim = walk if actor.moving else idle
        frame = state.frame(window, self.clock, anim, actor.facing)

        col, row = actor.position
        x = col * self.stg.cell_dim + (self.stg.cell_dim - frame.width) // 2
        y = row * self.stg.cell_dim + (self.stg.cell_dim - frame.height) // 2

        window.blit(frame, x, y, flip=state.flip)

    def _draw_player(self, window: Window, player: Player) -> None:
        self._draw_actor(
            window, player, self.player_anim, PLAYER_IDLE, PLAYER_WALK
        )

    def _draw_ghosts(
        self, window: Window, ghosts: tuple[Ghost, Ghost, Ghost, Ghost]
    ) -> None:
        for ghost, state, (idle, walk) in zip(
            ghosts, self.ghost_anims, GHOST_ANIMS, strict=True
        ):
            self._draw_actor(window, ghost, state, idle, walk)

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

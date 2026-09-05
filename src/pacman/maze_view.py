import time
from functools import partial
from random import randint
from typing import Any, Generator

from mlx import Mlx

from src.adapter import Adapter
from src.settings import Settings


class MazeView(Mlx):  # type: ignore[misc]
    def __init__(self, adapter: Adapter, stg: Settings) -> None:
        super().__init__()
        self.adp = adapter
        self.stg = stg

        self.text_animation = self.render_text()
        self.maze_animation = self.render_maze()
        self.animator: Generator[None, None, None] | None = self.animate()
        self.last_tick = 0.0
        self.animation_enabled = True
        self.show_path = True
        self.color_idx = 0

        self.maze_width = len(self.adp.grid[0]) * self.stg.cell_dim
        self.maze_height = len(self.adp.grid) * self.stg.cell_dim
        self.win_height = self.maze_height
        self.win_width = self.maze_width + self.stg.txt_pane_width

        self.mlx_ptr = self.mlx_init()
        self.win_ptr = self.mlx_new_window(
            self.mlx_ptr,
            self.win_width,
            self.win_height,
            self.stg.window_title,
        )
        self.img_ptr = self.mlx_new_image(
            self.mlx_ptr, self.maze_width, self.maze_height
        )
        data_addr, bpp, ll, _ = self.mlx_get_data_addr(self.img_ptr)
        self.data_addr: memoryview = data_addr
        self.bpp: int = bpp // 8
        self.ll: int = ll

        self.mlx_key_hook(self.win_ptr, self._on_keypress, None)
        self.mlx_hook(self.win_ptr, 0x21, 0, self.exit, None)
        self.mlx_loop_hook(self.mlx_ptr, self.app_loop, None)
        self.put_image = partial(
            self.mlx_put_image_to_window,
            self.mlx_ptr,
            self.win_ptr,
            self.img_ptr,
            self.stg.txt_pane_width,
            0,
        )
        self.write = partial(
            self.mlx_string_put,
            mlx_ptr=self.mlx_ptr,
            win_ptr=self.win_ptr,
            x=self.stg.x_offset,
            color=self.stg.text_color,
        )

    def app_loop(self, _: Any) -> None:
        if self.animator is None:
            return
        now = time.perf_counter()
        if not self.animation_enabled or now - self.last_tick > self.stg.tick:
            self.last_tick = now
            try:
                next(self.animator)
            except StopIteration:
                self.animator = None

    def animate(self) -> Generator[None, None, None]:
        yield from self.text_animation
        yield from self.maze_animation

    def reset_animation(self) -> None:
        self.maze_animation = self.render_maze()
        self.animator = self.animate()
        self.last_tick = 0.0

    def exit(self, _: Any) -> None:
        self.mlx_loop_exit(self.mlx_ptr)

    def _on_keypress(self, key: int, _: Any) -> None:
        if key == self.stg.close_win:
            self.exit(None)
        elif key == self.stg.toggle_animation:
            self.animation_enabled = not self.animation_enabled
        elif key == self.stg.new_maze:
            self.adp.generate(randint(5, 15), randint(5, 15))
            self.reset_animation()
        elif key == self.stg.change_color:
            self.color_idx = (self.color_idx + 1) % len(self.stg.colors)
            self.reset_animation()

    def render_maze(self) -> Generator[None, None, None]:
        color = self.stg.colors[self.color_idx][0]

        self._put_box(0, 0, self.maze_width, self.maze_height, color)
        self._put_box(
            self.stg.wall_thickness,
            self.stg.wall_thickness,
            self.maze_width - 2 * self.stg.wall_thickness,
            self.maze_height - 2 * self.stg.wall_thickness,
            0,
        )

        for cell in self.adp.cells:
            x_offset = cell.col * self.stg.cell_dim
            y_offset = cell.row * self.stg.cell_dim
            if cell.n:
                self._put_box(
                    x_offset,
                    y_offset,
                    self.stg.cell_dim,
                    self.stg.wall_thickness,
                    color,
                )
            if cell.e:
                self._put_box(
                    x_offset + self.stg.cell_dim - self.stg.wall_thickness,
                    y_offset,
                    self.stg.wall_thickness,
                    self.stg.cell_dim,
                    color,
                )
            if (cell.col, cell.row) in self.adp.non_empty_corners:
                self._put_box(
                    x_offset + self.stg.cell_dim - self.stg.wall_thickness,
                    y_offset,
                    self.stg.wall_thickness,
                    self.stg.wall_thickness,
                    color,
                )
        self.put_image()
        yield

    def render_text(self) -> Generator[None, None, None]:
        yield  # workaround to solve X11 buffering issue
        self.write(y=self.stg.y_offset + 300, string="KEYBINDINGS")
        self.write(y=self.stg.y_offset + 330, string="M | New (M)aze")
        self.write(y=self.stg.y_offset + 360, string="P | Toggle (P)ath")
        self.write(y=self.stg.y_offset + 390, string="C | Change (C)olors")
        self.write(y=self.stg.y_offset + 420, string="A | Toggle (A)nimation")
        self.write(y=self.stg.y_offset + 450, string="ESC | Quit")
        yield

    def _put_box(
        self, x: int, y: int, width: int, height: int, color: int
    ) -> None:
        pixel = bytes(
            ((color & 0xFF), (color >> 8 & 0xFF), (color >> 16 & 0xFF), 0xFF)
        )
        row_bytes = pixel * width
        start = x * self.bpp
        end = start + width * self.bpp

        for r in range(height):
            offset = (y + r) * self.ll
            self.data_addr[slice(offset + start, offset + end)] = row_bytes

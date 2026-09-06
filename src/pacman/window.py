from typing import Any, Callable

from mlx.mlx import Mlx

from src.pacman.settings import Settings


class Window:
    mlx: Mlx
    mlx_ptr: int | None
    win_ptr: int | None
    pixels: memoryview
    bpp: int
    line_size: int
    format: int

    def __init__(
        self, stg: Settings, game_loop: Callable[[Any], None]
    ) -> None:
        stg = stg
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, stg.win_width, stg.win_height, stg.window_title
        )

        self.img_ptr = self.mlx.mlx_new_image(
            self.mlx_ptr, stg.win_width, stg.win_height
        )
        pixels, bpp, ll, format = self.mlx.mlx_get_data_addr(self.img_ptr)
        self.pixels = pixels
        self.bpp = bpp
        self.line_size = ll
        self.format = format

        self.mlx.mlx_hook(self.win_ptr, 0x21, 0, self.exit, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, game_loop, None)

    def show(self) -> None:
        self.mlx.mlx_loop(self.mlx_ptr)

    def exit(self, _: Any) -> None:
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def write(self, x: int, y: int, color: int, string: str) -> None:
        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win_ptr, x, y, color, string
        )

    def clear(self) -> None:
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)

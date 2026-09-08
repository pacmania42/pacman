from typing import Any, Callable, Protocol

from mlx.mlx import Mlx

from src.pacman.core.settings import Settings


class EventSink(Protocol):
    """Protocol to hands off the events out of mlx"""

    def on_key_down(self, keycode: int, param: object, /) -> None: ...

    def on_key_up(self, keycode: int, param: object, /) -> None: ...

    def on_focus_out(self, param: object, /) -> None: ...


class Window:
    mlx: Mlx
    mlx_ptr: int | None
    win_ptr: int | None
    pixels: memoryview
    bpp: int
    line_size: int
    format: int

    def __init__(
        self, sink: EventSink, game_loop: Callable[[Any], None]
    ) -> None:
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            Settings.win_width,
            Settings.win_height,
            Settings.window_title,
        )

        self.img_ptr = self.mlx.mlx_new_image(
            self.mlx_ptr, Settings.win_width, Settings.win_height
        )
        pixels, bpp, ll, format = self.mlx.mlx_get_data_addr(self.img_ptr)
        self.pixels = pixels
        self.bpp = bpp
        self.line_size = ll
        self.format = format

        # key press
        self.mlx.mlx_hook(self.win_ptr, 2, 1, sink.on_key_down, None)
        # key release
        self.mlx.mlx_hook(self.win_ptr, 3, 2, sink.on_key_up, None)
        # focus lost
        self.mlx.mlx_hook(self.win_ptr, 10, 1 << 21, sink.on_focus_out, None)

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

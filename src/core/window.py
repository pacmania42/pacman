from typing import Any, Callable, Protocol

from mlx.mlx import Mlx

from src.core.settings import Settings


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
    bytes_pp: int
    line_size: int
    format: int

    def __init__(
        self, sink: EventSink, game_loop: Callable[[Any], None]
    ) -> None:
        self.width = Settings.win_width
        self.height = Settings.win_height
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
        self.bytes_pp = bpp // 8
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

    def fill(self, color: int) -> None:
        """Repaint the whole back buffer, wiping the previous frame."""
        self.put_box(0, 0, self.width, self.height, color)

    def _to_pixel(self, color: int) -> bytes:
        """Pack an 0xRRGGBB color into one buffer pixel."""
        return bytes(
            ((color & 0xFF), (color >> 8 & 0xFF), (color >> 16 & 0xFF), 0xFF)
        )

    def put_box(
        self, x: int, y: int, width: int, height: int, color: int
    ) -> None:
        """Fill a rectangle of the back buffer, clipped to the window."""
        if x < 0:
            width += x
            x = 0
        if y < 0:
            height += y
            y = 0
        width = min(width, self.width - x)
        height = min(height, self.height - y)
        if width <= 0 or height <= 0:
            return

        row_bytes = self._to_pixel(color) * width
        start = x * self.bytes_pp
        end = start + width * self.bytes_pp

        for r in range(height):
            offset = (y + r) * self.line_size
            self.pixels[slice(offset + start, offset + end)] = row_bytes

    def draw_image(self) -> None:
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
        )

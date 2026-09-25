import os
import sys
from typing import Any, Callable, Optional, Protocol

from mlx.mlx import Mlx

from src.core.font import PixelFont
from src.core.image import Image, ImageError
from src.core.settings import Settings
from src.core.sprite import Frame, Sprites


class WindowError(Exception):
    """Raised when the mlx context or the window cannot be created."""


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
        """Create the window and set up event and game loop hooks.

        Args:
            sink: Object that receives window events.
            game_loop: Function called on each game loop iteration
        """
        self.width = Settings.win_width
        self.height = Settings.win_height
        # mlx segfaults when no X server is reachable
        # we don't cover a wrong DISPLAY (this would segfaults anyway)
        on_linux = sys.platform.startswith("linux")
        if on_linux and not os.environ.get("DISPLAY"):
            raise WindowError("no display available (DISPLAY is not set)")
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        if not self.mlx_ptr:
            raise WindowError("cannot initialize mlx")
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            Settings.win_width,
            Settings.win_height,
            Settings.window_title,
        )
        if not self.win_ptr:
            raise WindowError("cannot create the game window")

        self.img_ptr = self.mlx.mlx_new_image(
            self.mlx_ptr, Settings.win_width, Settings.win_height
        )
        pixels, bpp, ll, format = self.mlx.mlx_get_data_addr(self.img_ptr)
        self.pixels = pixels
        self.bytes_pp = bpp // 8
        self.line_size = ll
        self.format = format

        self.font = PixelFont(self.mlx, self.mlx_ptr)
        self.sprites = Sprites(self.png_file_to_image)
        self.text_scale = Settings.text_scale

        # key press
        self.mlx.mlx_hook(self.win_ptr, 2, 1, sink.on_key_down, None)
        # key release
        self.mlx.mlx_hook(self.win_ptr, 3, 2, sink.on_key_up, None)
        # focus lost
        self.mlx.mlx_hook(self.win_ptr, 10, 1 << 21, sink.on_focus_out, None)

        self.mlx.mlx_hook(self.win_ptr, 0x21, 0, self.exit, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, game_loop, None)

    def show(self) -> None:
        """Start the window event loop"""
        self.mlx.mlx_loop(self.mlx_ptr)

    def exit(self, _: Any) -> None:
        """Destroy the window resources and stop the event loop.

        Args:
            _: Event data passed by MLX.

        Returns:
            None.
        """
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def write(self, x: int, y: int, color: int, string: str) -> None:
        """Draw a string directly on the window.

        Args:
            x: Horizontal position.
            y: Vertical position.
            color: Text color.
            string: Text to draw.

        Returns:
            None.
        """
        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win_ptr, x, y, color, string
        )

    def png_file_to_image(self, filename: str) -> Image:
        """Load a PNG file and return it as an image.

        Args:
            filename: Path to the PNG file.

        Returns:
            The loaded image.

        Raises:
            ImageError: If the image cannot be loaded.
        """
        img, width, height = self.mlx.mlx_png_file_to_image(
            self.mlx_ptr, filename
        )
        if img is None:
            raise ImageError(f"cannot load image: {filename}")
        pixels, bpp, line_size, _ = self.mlx.mlx_get_data_addr(img)
        return Image(pixels, bpp // 8, line_size, width, height)

    def fill(self, color: int) -> None:
        """Repaint the whole back buffer, wiping the previous frame

        Args:
            color: 0xRRGGBB fill color
        """
        size = self.height * self.width
        self.pixels[slice(0, size * self.bytes_pp)] = (
            self._to_pixel(color) * size
        )

    def _to_pixel(self, color: int) -> bytes:
        """Pack a 0xRRGGBB color into one buffer pixel.

        Args:
            color: 0xRRGGBB color.

        Returns:
            The packed pixel bytes.
        """
        return bytes(
            ((color & 0xFF), (color >> 8 & 0xFF), (color >> 16 & 0xFF), 0xFF)
        )

    def put_box(
        self, x: int, y: int, width: int, height: int, color: int
    ) -> None:
        """Fill a rectangle of the back buffer, clipped to the window

        Args:
            x: Left position
            y: Top position
            width: Rectangle width
            height: Rectangle height
            color: 0xRRGGBB fill color
        """
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

    def _scale(self, scale: Optional[int]) -> int:
        """Return the effective text scale.

        Args:
            scale: Requested scale, or None for the default.

        Returns:
            The scale, with a minimum value of 1.
        """
        return max(1, self.text_scale if scale is None else scale)

    def text_width(self, text: str, scale: Optional[int] = None) -> int:
        """Return the width `text` occupies once drawn, in pixels

        Args:
            text: Text to measure.
            scale: Text scale, or None for the default.

        Returns:
            The text width in pixels.
        """
        return self.font.measure(text, self._scale(scale))

    def text_height(self, scale: Optional[int] = None) -> int:
        """Return the line height in pixels.

        Args:
            scale: Text scale, or None for the default.

        Returns:
            The line-to-line height in pixels.
        """
        return self.font.line_height * self._scale(scale)

    def ink_height(self, scale: Optional[int] = None) -> int:
        """Return the height of the glyphs without leading.

        Use this to sit a rule or a box tight against a line of text;
        use `text_height()` to stack lines.

        Args:
            scale: Text scale, or None for the default.

        Returns:
            The glyph height in pixels.
        """
        return self.font.ink_height * self._scale(scale)

    def put_text(
        self,
        x: int,
        y: int,
        text: str,
        color: int = 0xFFFFFF,
        scale: Optional[int] = None,
    ) -> None:
        """Put `text` into the back buffer, over whatever is there.

        Nothing reaches the screen until `draw_image()` is called, so
        several calls compose on top of each other

        Args:
            x: Left edge of the first glyph
            y: Top edge of the line
            text: The string to draw
            color: 0xRRGGBB ink color
            scale: Whole-number magnification
        """
        factor = self._scale(scale)
        pixel = self._to_pixel(color)
        for row, col, length in self.font.layout(x, y, text, factor):
            if col < 0:
                length += col
                col = 0
            length = min(length, self.width - col)
            if length <= 0:
                continue
            row_bytes = pixel * length
            start = col * self.bytes_pp
            end = start + length * self.bytes_pp
            for step in range(factor):
                if 0 <= row + step < self.height:
                    offset = (row + step) * self.line_size
                    self.pixels[slice(offset + start, offset + end)] = (
                        row_bytes
                    )

    def draw_image(self) -> None:
        """Draw the back buffer to the window"""
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
        )

    def blit(
        self,
        frame: Frame,
        x: int,
        y: int,
        flip: bool = False,
        alpha_min: int = 128,
        tint: int | None = None,
    ) -> None:
        """Copy a frame into the back buffer (Block image transfer)

        Args:
            frame: frame to copy
            x: Destination x position
            y: Destination y position
            flip: Flip the frame horizontally
            alpha_min: Minimum alpha value to draw a pixel
            tint: Optional color applied to all opaque pixels
        """
        pixel = self._to_pixel(tint) if tint is not None else None
        src, sbpp, sll = (
            frame.sheet.pixels,
            frame.sheet.bytes_pp,
            frame.sheet.line_size,
        )
        last = frame.width - 1
        for row in range(frame.height):
            ty = y + row
            if not 0 <= ty < self.height:
                continue
            sbase = row * sll + frame.x0 * sbpp
            dbase = ty * self.line_size
            for col in range(frame.width):
                tx = x + col
                if not 0 <= tx < self.width:
                    continue
                s = sbase + (last - col if flip else col) * sbpp
                if src[s + 3] < alpha_min:
                    continue
                d = dbase + tx * self.bytes_pp
                self.pixels[slice(d, d + 4)] = pixel or src[slice(s, s + 4)]

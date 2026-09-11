"""Draw text using a bitmap font.

The font is a PNG image (the "atlas") that contains every character.
Where each character sits inside that PNG is listed in
PEABERRY_FONT_DATA
"""

from pathlib import Path
from typing import Iterator, Optional

from mlx.mlx import Mlx

import src.assets.fonts as fonts

ATLAS_PATH = Path(fonts.__path__[0]) / "WhitePeaberry.png"

# Atlas positions of all glyphs of WhitePeaberry.png
# Format: id: (x, y, width, height, xoffset, yoffset, xadvance)
PEABERRY_FONT_DATA: dict[int, tuple[int, int, int, int, int, int, int]] = {
    32:  (20,  208, 0,  0,  0,  27, 5),   # space
    33:  (198, 2,   14, 23, -2, 5,  7),   # !
    34:  (109, 188, 17, 15, -3, 5,  9),   # "
    35:  (149, 29,  20, 21, -4, 6,  11),  # #
    36:  (178, 2,   18, 23, -3, 5,  10),  # $
    37:  (126, 29,  21, 21, -4, 6,  12),  # %
    38:  (134, 53,  19, 21, -3, 6,  11),  # &
    39:  (77,  188, 14, 16, 0,  5,  9),   # '
    40:  (56,  2,   15, 25, -2, 5,  8),   # (
    41:  (73,  2,   15, 25, -2, 5,  8),   # )
    42:  (134, 145, 18, 19, -2, 5,  11),  # *
    43:  (45,  168, 18, 18, -2, 7,  11),  # +
    44:  (93,  188, 14, 16, -3, 14, 6),   # ,
    45:  (2,   208, 16, 12, -1, 12, 10),  # -
    46:  (167, 188, 14, 14, -3, 13, 6),   # .
    47:  (42,  29,  16, 22, -4, 5,  7),   # /
    48:  (176, 53,  18, 21, -3, 6,  10),  # 0
    49:  (2,   76,  18, 21, -3, 6,  10),  # 1
    50:  (22,  76,  18, 21, -3, 6,  10),  # 2
    51:  (42,  76,  18, 21, -3, 6,  10),  # 3
    52:  (62,  76,  18, 21, -3, 6,  10),  # 4
    53:  (82,  76,  18, 21, -3, 6,  10),  # 5
    54:  (102, 76,  18, 21, -3, 6,  10),  # 6
    55:  (122, 76,  18, 21, -3, 6,  10),  # 7
    56:  (142, 76,  18, 21, -3, 6,  10),  # 8
    57:  (162, 76,  18, 21, -3, 6,  10),  # 9
    58:  (118, 145, 14, 20, -3, 8,  6),   # :
    59:  (78,  29,  14, 22, -3, 8,  6),   # ;
    60:  (42,  145, 17, 21, -3, 5,  9),   # <
    61:  (58,  188, 17, 16, -3, 8,  9),   # =
    62:  (61,  145, 17, 21, -3, 5,  9),   # >
    63:  (136, 2,   18, 24, -3, 5,  10),  # ?
    64:  (171, 29,  20, 21, -4, 8,  11),  # @
    65:  (193, 29,  20, 21, -4, 6,  11),  # A
    66:  (182, 76,  18, 21, -3, 6,  10),  # B
    67:  (2,   99,  18, 21, -3, 6,  10),  # C
    68:  (22,  99,  18, 21, -3, 6,  10),  # D
    69:  (42,  99,  18, 21, -3, 6,  10),  # E
    70:  (62,  99,  18, 21, -3, 6,  10),  # F
    71:  (82,  99,  18, 21, -3, 6,  10),  # G
    72:  (102, 99,  18, 21, -3, 6,  10),  # H
    73:  (122, 99,  18, 21, -3, 6,  10),  # I
    74:  (142, 99,  18, 21, -3, 6,  10),  # J
    75:  (155, 53,  19, 21, -3, 6,  11),  # K
    76:  (162, 99,  18, 21, -3, 6,  10),  # L
    77:  (2,   53,  20, 21, -4, 6,  11),  # M
    78:  (182, 99,  18, 21, -3, 6,  10),  # N
    79:  (24,  53,  20, 21, -4, 6,  11),  # O
    80:  (2,   122, 18, 21, -3, 6,  10),  # P
    81:  (156, 2,   20, 23, -4, 6,  11),  # Q
    82:  (22,  122, 18, 21, -3, 6,  10),  # R
    83:  (42,  122, 18, 21, -3, 6,  10),  # S
    84:  (62,  122, 18, 21, -3, 6,  10),  # T
    85:  (82,  122, 18, 21, -3, 6,  10),  # U
    86:  (46,  53,  20, 21, -4, 6,  11),  # V
    87:  (68,  53,  20, 21, -4, 6,  11),  # W
    88:  (90,  53,  20, 21, -4, 6,  11),  # X
    89:  (112, 53,  20, 21, -4, 6,  11),  # Y
    90:  (102, 122, 18, 21, -3, 6,  10),  # Z
    91:  (90,  2,   14, 25, -3, 5,  6),   # [
    92:  (60,  29,  16, 22, -4, 5,  7),   # \
    93:  (106, 2,   14, 25, -3, 5,  6),   # ]
    94:  (154, 145, 20, 18, -4, 5,  11),  # ^
    95:  (183, 188, 18, 12, -3, 18, 10),  # _
    96:  (150, 188, 15, 14, -4, 5,  6),   # `
    97:  (24,  168, 19, 18, -4, 9,  10),  # a
    98:  (122, 122, 18, 21, -3, 6,  10),  # b
    99:  (2,   188, 17, 18, -3, 9,  9),   # c
    100: (142, 122, 18, 21, -3, 6,  10),  # d
    101: (21,  188, 17, 18, -3, 9,  9),   # e
    102: (162, 122, 18, 21, -3, 6,  10),  # f
    103: (2,   29,  18, 22, -3, 9,  10),  # g
    104: (182, 122, 18, 21, -3, 6,  10),  # h
    105: (94,  29,  14, 22, -1, 5,  8),   # i
    106: (2,   2,   16, 25, -2, 5,  9),   # j
    107: (80,  145, 17, 21, -2, 6,  10),  # k
    108: (110, 29,  14, 22, -1, 5,  8),   # l
    109: (176, 145, 20, 18, -4, 9,  11),  # m
    110: (65,  168, 18, 18, -3, 9,  10),  # n
    111: (85,  168, 18, 18, -3, 9,  10),  # o
    112: (2,   145, 18, 21, -3, 9,  10),  # p
    113: (22,  145, 18, 21, -3, 9,  10),  # q
    114: (105, 168, 18, 18, -3, 9,  10),  # r
    115: (40,  188, 16, 18, -2, 9,  9),   # s
    116: (99,  145, 17, 21, -3, 6,  9),   # t
    117: (125, 168, 18, 18, -3, 9,  10),  # u
    118: (145, 168, 18, 18, -3, 9,  10),  # v
    119: (2,   168, 20, 18, -4, 9,  11),  # w
    120: (165, 168, 18, 18, -3, 9,  10),  # x
    121: (22,  29,  18, 22, -3, 9,  10),  # y
    122: (185, 168, 18, 18, -3, 9,  10),  # z
    123: (20,  2,   16, 25, -4, 5,  7),   # {
    124: (122, 2,   12, 25, -3, 5,  4),   # |
    125: (38,  2,   16, 25, -4, 5,  7),   # }
    126: (128, 188, 20, 14, -4, 10, 11),  # ~
}

Glyph = tuple[int, int, int, int, int, int, int]
"""Atlas entry: (x, y, width, height, xoffset, yoffset, xadvance)."""

Run = tuple[int, int, int]
"""
A horizontal line of visible pixels: (dy, dx, length), relative to the pen.
"""


class FontError(Exception):
    """Raised when the glyph atlas cannot be loaded."""


class PixelFont:
    """A bitmap font loaded from a PNG.

    When the font is loaded, each character is converted once into a
    list of horizontal pixel runs. Drawing text is then just copying
    those runs into the target image at the right place.

    Characters that are not in the font are drawn as "?"
    """

    def __init__(
        self,
        mlx: Mlx,
        mlx_ptr: Optional[int],
        path: Path = ATLAS_PATH,
        data: dict[int, Glyph] = PEABERRY_FONT_DATA,
        line_height: Optional[int] = None,
        leading: int = 6,
        alpha_min: int = 128,
    ) -> None:
        """
        Args:
            mlx: MLX wrapper, used to read the PNG.
            mlx_ptr: MLX context returned by mlx_init.
            path: PNG atlas holding the glyphs.
            data: Position of each character inside the PNG, keyed by
                character code (ord(char)).
            line_height: Line-to-line advance. Defaults to the measured
                ink height plus `leading`.
            leading: Empty rows between two lines of text. Only used
                when line_height is None.
            alpha_min: A pixel is visible if its alpha is >= this value.

        Raises:
            FontError: The PNG is missing or cannot be read.
        """
        self._glyphs: dict[int, tuple[list[Run], int]] = {}

        img, _, _ = mlx.mlx_png_file_to_image(mlx_ptr, str(path))
        if img is None:
            raise FontError(f"cannot load font atlas: {path}")
        pixels, bpp, line_size, _ = mlx.mlx_get_data_addr(img)
        try:
            bpp //= 8
            for code, glyph in data.items():
                runs = self._bake(pixels, bpp, line_size, glyph, alpha_min)
                self._glyphs[code] = (runs, glyph[6])
        finally:
            pixels.release()
            mlx.mlx_destroy_image(mlx_ptr, img)

        self.ink_height = self._anchor_to_ink()
        self.line_height = (
            self.ink_height + leading if line_height is None else line_height
        )
        self._fallback = self._glyphs.get(
            ord("?"), ([], self.line_height // 2)
        )

    def _anchor_to_ink(self) -> int:
        """Move every run up so that dy == 0 is the first row with pixels.

        In the PNG each character has a few empty rows above and below
        it. Without this shift, `y` in layout() would point at empty
        space and lines of text would be further apart than needed.

        Returns the height of the tallest character after the shift.
        """
        rows = [run[0] for runs, _ in self._glyphs.values() for run in runs]
        if not rows:
            return 0
        top, bottom = min(rows), max(rows) + 1
        for code, (runs, advance) in self._glyphs.items():
            shifted = [(dy - top, dx, length) for dy, dx, length in runs]
            self._glyphs[code] = (shifted, advance)
        return bottom - top

    @staticmethod
    def _bake(
        pixels: memoryview,
        bytes_pp: int,
        line_size: int,
        glyph: Glyph,
        alpha_min: int,
    ) -> list[Run]:
        """Goes through the rectangle row by row and records each group
        of adjacent visible pixels as (dy, dx, length)
        """
        x, y, width, height, xoffset, yoffset, _ = glyph
        runs: list[Run] = []
        for row in range(height):
            base = (y + row) * line_size + x * bytes_pp + 3  # alpha byte
            col = 0
            while col < width:
                if pixels[base + col * bytes_pp] < alpha_min:
                    col += 1
                    continue
                start = col
                while (
                    col < width
                    and pixels[base + col * bytes_pp] >= alpha_min
                ):
                    col += 1
                runs.append((yoffset + row, xoffset + start, col - start))
        return runs

    def measure(self, text: str, scale: int = 1) -> int:
        """Return the width of `text` in pixels when drawn at `scale`"""
        advances = (self._glyphs.get(ord(c), self._fallback)[1] for c in text)
        return sum(advances) * scale

    def layout(
        self, x: int, y: int, text: str, scale: int = 1
    ) -> Iterator[Run]:
        """Yield the runs needed to draw `text` starting at (x, y).

        Each run is (y, x, length) in image coordinates, ready to draw.

        `scale` makes the text bigger by multiplying positions and
        lengths, so the pixels stay sharp. Note that with scale > 1
        each run is yielded only once: the caller has to draw it
        `scale` times, one row under the other.
        """
        for char in text:
            runs, advance = self._glyphs.get(ord(char), self._fallback)
            for dy, dx, length in runs:
                yield (y + dy * scale, x + dx * scale, length * scale)
            x += advance * scale

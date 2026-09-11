"""Small drawing primitives shared by every screen.

A scene describes what it wants ( e.g. "a title",
"a section heading", "a menu entry") instead of repeating color, scale, ...
Each helper returns the next free `y`
"""

from src.core.window import Window
from src.ui import theme


def line(
    window: Window,
    x: int,
    y: int,
    text: str,
    color: int = theme.TEXT,
    scale: int = theme.SCALE_BODY,
) -> int:
    """Draw one left-aligned line; return the next free y."""
    window.put_text(x, y, text, color, scale)
    return y + window.text_height(scale)


def centered(
    window: Window,
    y: int,
    text: str,
    color: int = theme.TEXT,
    scale: int = theme.SCALE_BODY,
) -> int:
    """Draw one line centred on the window; return the next free y."""
    x = (window.width - window.text_width(text, scale)) // 2
    return line(window, x, y, text, color, scale)


def block_left(window: Window, lines: list[tuple[str, int]]) -> int:
    """Return the x that centres a ragged block of mixed-scale lines.

    Lines stay left-aligned with each other -- only the block as a whole
    is centred, which keeps a wide screen from stranding text on one
    side.
    """
    widest = max(
        (window.text_width(text, scale) for text, scale in lines), default=0
    )
    return max(theme.MARGIN, (window.width - widest) // 2)


def block_top(window: Window, top: int, height: int) -> int:
    """Return the y that centres a block between `top` and the footer.

    A screen that does not fill its window should sit in the middle of
    what is left rather than hugging the title, so short and long
    screens feel like the same design.
    """
    footer_top = (
        window.height - theme.MARGIN - window.text_height(theme.SCALE_BODY)
    )
    return top + max(0, (footer_top - top - height) // 2)


def ghost_rule(window: Window, x: int, y: int, width: int) -> int:
    """Draw the four-ghost colour bar; return the next free y."""
    segment = width // len(theme.GHOSTS)
    for i, color in enumerate(theme.GHOSTS):
        window.put_box(x + i * segment, y, segment, theme.RULE_HEIGHT, color)
    return y + theme.RULE_HEIGHT


def screen_title(window: Window, y: int, text: str) -> int:
    """Draw a screen title over its divider; return the next free y."""
    centered(window, y, text, theme.TITLE, theme.SCALE_TITLE)
    rule_y = y + window.ink_height(theme.SCALE_TITLE) + theme.GAP
    y = ghost_rule(
        window, theme.MARGIN, rule_y, window.width - 2 * theme.MARGIN
    )
    return y + 2 * theme.GAP


def footer(window: Window, text: str) -> None:
    """Draw the hint line that sits at the bottom of every screen."""
    y = window.height - theme.MARGIN - window.text_height(theme.SCALE_BODY)
    centered(window, y, text, theme.MUTED, theme.SCALE_BODY)

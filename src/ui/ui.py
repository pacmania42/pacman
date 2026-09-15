"""Small drawing primitives shared by every screen.

A scene describes what it wants ( e.g. "a title",
"a section heading", "a menu entry") instead of repeating color, scale, ...
Each helper returns the next free `y`
"""

import math

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


def ghost_rule(
    window: Window, x: int, y: int, width: int, shift: int = 0
) -> int:
    """Draw the four-ghost colour bar, return the next free y

    `shift` animate the rule, if 0 the rule is static
    """
    count = len(theme.GHOSTS)
    segment = max(1, width // count)
    shift %= segment * count
    band, offset = divmod(shift, segment)

    i, cursor = 0, x - offset
    while cursor < x + width:
        start, end = max(x, cursor), min(x + width, cursor + segment)
        if start < end:
            window.put_box(
                start,
                y,
                end - start,
                theme.RULE_HEIGHT,
                theme.GHOSTS[(i + band) % count],
            )
        cursor += segment
        i += 1
    return y + theme.RULE_HEIGHT


def screen_title(window: Window, y: int, text: str, shift: int = 0) -> int:
    """Draw a screen title over its divider, return the next free y

    `shift` is handed to `ghost_rule`
    """
    centered(window, y, text, theme.TITLE, theme.SCALE_TITLE)
    rule_y = y + window.ink_height(theme.SCALE_TITLE) + theme.GAP
    y = ghost_rule(
        window,
        theme.MARGIN,
        rule_y,
        window.width - 2 * theme.MARGIN,
        shift,
    )
    return y + 2 * theme.GAP


def footer(window: Window, text: str) -> None:
    """Draw the hint line that sits at the bottom of every screen."""
    y = window.height - theme.MARGIN - window.text_height(theme.SCALE_BODY)
    centered(window, y, text, theme.MUTED, theme.SCALE_BODY)


def reveal(color: int, index: int, clock: float) -> int:
    """Fade-in, clock starts at zero and the sequence replays
    on each visit
    """
    elapsed = clock - index * theme.REVEAL_STEP
    return theme.mix(theme.BG, color, elapsed / theme.REVEAL_FADE)


def pulse(clock: float, color: int = theme.TITLE) -> int:
    """For a breathe `color` animation to white"""
    phase = math.tau * clock / theme.PULSE_PERIOD
    return theme.mix(color, theme.WHITE, (1.0 - math.cos(phase)) / 2.0)


def rule_shift(clock: float) -> int:
    """The `shift` to scroll a screen title's colour rule"""
    return int(clock * theme.RULE_SPEED)

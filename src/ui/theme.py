"""The game's visual design system

Palette
    The hues are the authentic Namco arcade colors: Pac-Man's yellow,
    the four ghosts, the maze blue and the pellet peach.

Hierarchy
    The bitmap font has a single weight, so rank is carried by size and
    color rather than by boldness. A larger scale and a warmer hue mean
    "more important". Body copy is TEXT at SCALE_BODY; anything bigger
    is a heading; MUTED is for lines the player need not read.

Grid
    Vertical rhythm is always a multiple of the font's line height, read
    from `Window.text_height()`, so mixing scales never breaks spacing.
    Horizontal insets are multiples of MARGIN.

Contrast
    These colors assume a black background. BLUE, SURFACE and HIGHLIGHT
    are fills only, never text: they are too dark to read against BG.
    RED is reserved for danger, never for body copy.
"""

from typing import Final

# ---------------------------------------------------------------- palette

BLACK: Final[int] = 0x000000
WHITE: Final[int] = 0xFFFFFF
YELLOW: Final[int] = 0xFFFF00
"""Pac-Man."""
RED: Final[int] = 0xFF0000
"""Blinky."""
PINK: Final[int] = 0xFFB8FF
"""Pinky."""
CYAN: Final[int] = 0x00FFFF
"""Inky."""
ORANGE: Final[int] = 0xFFB851
"""Clyde."""
BLUE: Final[int] = 0x2121FF
"""Maze walls. Fill only, far too dark for text."""
PEACH: Final[int] = 0xFFB897
"""Pellets and ghost eyes."""
FRIGHT: Final[int] = 0x2121DE
"""Frightened ghosts."""
NAVY: Final[int] = 0x0A0A28
"""Panel ground, one step off black."""
INDIGO: Final[int] = 0x1C1C5A
"""Selected-row bar."""
SLATE: Final[int] = 0x8B8BB0
"""De-emphasised text, still readable on black."""

GHOSTS: Final[tuple[int, ...]] = (RED, PINK, CYAN, ORANGE)
"""The four ghosts, in their arcade release order."""

HEADINGS: Final[tuple[int, ...]] = (CYAN, PINK, ORANGE)
"""Cycled across the section headings of a screen, so consecutive
sections stay visually distinct. Blinky's red is left out on purpose:
it belongs to DANGER."""

# ------------------------------------------------------------------ roles

BG: Final[int] = BLACK
SURFACE: Final[int] = NAVY
HIGHLIGHT: Final[int] = INDIGO

TEXT: Final[int] = WHITE
MUTED: Final[int] = SLATE
TITLE: Final[int] = YELLOW
SELECTED: Final[int] = YELLOW
DANGER: Final[int] = RED

# ------------------------------------------------------------- type scale

SCALE_BODY: Final[int] = 1
SCALE_HEADING: Final[int] = 2
"""One tick above body: section headings inside a screen."""
SCALE_TITLE: Final[int] = 3
"""Screen titles."""
SCALE_HERO: Final[int] = 5
"""The main-menu wordmark. Used once, on one screen."""

SCALE_ITEM: Final[int] = 2
"""A menu entry at rest."""
SCALE_ITEM_ACTIVE: Final[int] = 3
"""The menu entry under the cursor: one tick up, and recolored."""

# ------------------------------------------------------------------- grid

MARGIN: Final[int] = 60
"""Horizontal inset from the window edge."""
GAP: Final[int] = 12
"""The small space that separates related blocks."""
RULE_HEIGHT: Final[int] = 6
"""Thickness of the four-ghost divider."""
CURSOR: Final[str] = ">"
"""Marker drawn beside the active menu entry."""

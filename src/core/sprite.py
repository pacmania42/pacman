from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable

import src.assets.sprites as sprites_pkg
from src.core.image import Image, ImageError

SPRITES_DIR = Path(sprites_pkg.__path__[0])

Loader = Callable[[str], Image]
"""Turns a file path into a decoded Image (e.g. Window.png_file_to_image)."""


class SpriteId(Enum):
    SHROOM_IDLE = ("shroom_idle_32.png", 4)  # (file, frame count)
    SHROOM_WALK = ("shroom_walk_32.png", 4)


class SpriteError(Exception):
    """Raised when a sprite cannot be loaded"""


@dataclass(frozen=True)
class Frame:
    """One cell of a sheet"""

    sheet: Image
    x0: int
    width: int
    height: int


@dataclass(frozen=True)
class Animation:

    sheet: SpriteId
    fps: float
    loop: bool = True

    def frame_index(self, t: float, count: int) -> int:
        i = int(t * self.fps)
        return i % count if self.loop else min(i, count - 1)


class SpriteSheet:
    def __init__(self, sheet: Image, count: int) -> None:
        w = sheet.width // count
        self.frames = tuple(
            Frame(sheet, i * w, w, sheet.height) for i in range(count)
        )

    def __getitem__(self, i: int) -> Frame:
        return self.frames[i % len(self.frames)]

    def __len__(self) -> int:
        return len(self.frames)


class Sprites:
    """Load all spritesheets"""

    def __init__(self, load: Loader, base: Path = SPRITES_DIR) -> None:
        self.sheets: dict[SpriteId, SpriteSheet] = {}
        for sid in SpriteId:
            filename, count = sid.value
            try:
                img = load(str(base / filename))
            except ImageError as e:
                raise SpriteError(f"{sid.name}: {e}") from e
            self.sheets[sid] = SpriteSheet(img, count)

    def __getitem__(self, sid: SpriteId) -> SpriteSheet:
        return self.sheets[sid]

    def frame(self, anim: Animation, t: float) -> Frame:
        sheet = self.sheets[anim.sheet]
        return sheet[anim.frame_index(t, len(sheet))]

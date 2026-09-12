from dataclasses import dataclass


class ImageError(Exception):
    """Raised when an image cannot be loaded."""


@dataclass(frozen=True)
class Image:
    pixels: memoryview
    bytes_pp: int
    line_size: int
    width: int
    height: int

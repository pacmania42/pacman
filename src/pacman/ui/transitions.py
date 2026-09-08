from dataclasses import dataclass
from typing import Any, Optional, Union

from src.pacman.ui.scene_id import SceneId


@dataclass(frozen=True)
class Push:
    """Suspend the running scene and put `name` on top of it."""

    name: SceneId
    payload: Optional[Any] = None


@dataclass(frozen=True)
class Pop:
    """Leave the running scene, handing `result` to the one below."""

    result: Optional[Any] = None


@dataclass(frozen=True)
class Replace:
    """Swap the running scene for `name` without growing the stack."""

    name: SceneId
    payload: Optional[Any] = None


@dataclass(frozen=True)
class Quit:
    """Unwind the whole stack and stop the game."""


Transition = Union[Push, Pop, Replace, Quit, None]
"""What a scene asks the manager to do once its update returns."""

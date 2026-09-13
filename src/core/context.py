from dataclasses import dataclass

from src.core.config import Config
from src.core.highscore import HighScore


@dataclass(frozen=True)
class Context:
    """Long-lived services, built once at startup and shared by
    every scene

    New services as audio, save manager, ... belong here,
    if introduced in the future :)
    """

    config: Config
    highscore: HighScore

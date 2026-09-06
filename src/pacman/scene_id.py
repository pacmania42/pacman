from enum import Enum


class SceneId(Enum):
    """Identifier for every scene the manager can build"""

    MENU = "Menu"
    GAMEPLAY = "Gameplay"
    PAUSE = "Pause"
    HIGHSCORE = "HighScore"
    INSTRUCTIONS = "Instructions"

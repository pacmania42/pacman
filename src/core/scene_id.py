from enum import Enum


class SceneId(Enum):
    """Identifier for every scene the manager can build"""

    MENU = "Menu"
    GAMEPLAY = "Gameplay"
    PAUSE = "Pause"
    GAMEOVER = "GameOver"
    HIGHSCORE = "HighScore"
    INSTRUCTIONS = "Instructions"

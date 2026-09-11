from typing import List

from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.transitions import Pop, Transition
from src.core.window import Window


class InstructionsScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.instructions: List[str] = [
            "HOW TO PLAY",
            "Eat every dot in the maze to clear the level.",
            "Ghosts chase you. Touching one costs a life.",
            "Power pellets scare the ghosts for a few seconds:",
            "eat them while they are scared for bonus points.",
            "You start with 3 lives. No lives, game over.",
            "",
            "POINTS",
            "dot ............ 10      ghost ........  200",
            "power pellet ... 50",
            "",
            "CONTROLS",
            "move ..... Arrows  or  W A S D",
            "select ... SPACE  or  ENTER",
            "pause .... P  (during play)",
            "back ..... ESC   (ESC in the main menu quits)",
        ]

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.BACK):
            return Pop()
        return None

    def draw(self, window: Window) -> None:
        window.write(50, 50, 0xFFFFFF, "Instructions")
        window.write(50, 100, 0xFFFFFF, "Press ESC to Go Back")

        for i, item in enumerate(self.instructions):
            window.write(100, 300 + i * 20, 0xFFFFFF, item)

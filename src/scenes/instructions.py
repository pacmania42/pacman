from itertools import cycle

from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.transitions import Pop, Transition
from src.core.window import Window
from src.ui import theme, ui


class InstructionsScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.instructions: list[str] = [
            "HOW TO PLAY",
            "Eat every dot in the maze to clear the level.",
            "Ghosts chase you. Touching one costs a life.",
            "Power pellets scare the ghosts for a few seconds:",
            "eat them while they are scared for bonus points.",
            "You start with 3 lives. No lives, game over.",
            "",
            "POINTS",
            "dot ................ 10      ghost ........  200",
            "power pellet ... 50",
            "",
            "CONTROLS",
            "move ..... Arrows  or  W A S D",
            "select ... SPACE  or  ENTER",
            "pause .... P  (during play)",
            "back ...... ESC   (ESC in the main menu quits)",
        ]

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.BACK):
            return Pop()
        return None

    def draw(self, window: Window) -> None:
        top = ui.screen_title(window, theme.MARGIN // 2, "INSTRUCTIONS")
        rows = self._rows()
        height = sum(
            gap + (window.text_height(scale) if text else 0)
            for text, _, scale, gap in rows
        )
        x = ui.block_left(window, [(t, s) for t, _, s, _ in rows])
        y = ui.block_top(window, top, height)

        for text, color, scale, gap in rows:
            y += gap
            if text:
                y = ui.line(window, x, y, text, color, scale)

        ui.footer(window, "ESC   back to menu")

    def _rows(self) -> list[tuple[str, int, int, int]]:
        """Style every line, an all-caps line is drawn a tick larger
        and in different colors
        """
        headings = cycle(theme.HEADINGS)
        rows: list[tuple[str, int, int, int]] = []
        for entry in self.instructions:
            if not entry:
                rows.append(("", theme.TEXT, theme.SCALE_BODY, theme.GAP))
            elif entry.isupper():
                rows.append(
                    (entry, next(headings), theme.SCALE_HEADING, theme.GAP)
                )
            else:
                rows.append((entry, theme.TEXT, theme.SCALE_BODY, 0))
        return rows

from enum import Enum
from typing import Final

from src.core.context import Context
from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.transitions import Pop, Transition
from src.core.window import Window
from src.scenes.menu import Menu
from src.ui import theme, ui

TITLE: Final[str] = "PAUSED"
HINT: Final[str] = "ARROWS  move      SPACE  select      P  resume"


class PauseChoice(Enum):
    """Options available in the pause menu."""

    RESUME = "Resume"
    MAIN_MENU = "Main menu"


class PauseScene(Scene):
    """Display the game pause menu as an overlay."""

    is_overlay = True

    def __init__(self, ctx: Context) -> None:
        """Create the pause scene.

        Args:
            ctx: Shared game context.
        """
        super().__init__()
        self.menu = Menu([choice.value for choice in PauseChoice])

    def update(self, inputs: InputState) -> Transition:
        """Handle pause menu input and return a transition.

        Args:
            inputs: Current input state.

        Returns:
            The requested scene transition, or None.
        """
        if inputs.any_pressed(Action.PAUSE, Action.BACK):
            return Pop(PauseChoice.RESUME)
        if inputs.was_pressed(Action.DOWN):
            self.menu.move_down()
        elif inputs.was_pressed(Action.UP):
            self.menu.move_up()
        elif inputs.was_pressed(Action.CONFIRM):
            return Pop(PauseChoice(self.menu.get_item()))
        return None

    def draw(self, window: Window) -> None:
        """Draw the pause menu overlay.

        Args:
            window: Window used for drawing.
        """
        items = self.menu.get_items()
        title_height = window.ink_height(theme.SCALE_TITLE)
        menu_height = ui.menu_height(window, len(items))
        hint_height = window.text_height(theme.SCALE_BODY)

        width = max(
            ui.menu_width(window, items),
            window.text_width(HINT, theme.SCALE_BODY) + 2 * theme.MARGIN,
        )
        height = (
            2 * theme.RULE_HEIGHT
            + title_height
            + menu_height
            + hint_height
            + 7 * theme.GAP
        )
        x = (window.width - width) // 2
        y = (window.height - height) // 2
        shift = ui.rule_shift(self.clock)

        window.put_box(x, y, width, height, theme.SURFACE)
        y = ui.ghost_rule(window, x, y, width, shift) + 2 * theme.GAP
        ui.centered(window, y, TITLE, ui.pulse(self.clock), theme.SCALE_TITLE)
        y += title_height + 3 * theme.GAP
        y = ui.menu(window, y, items, self.menu.current)
        y = ui.centered(window, y, HINT, theme.MUTED) + 2 * theme.GAP
        ui.ghost_rule(window, x, y, width, -shift)

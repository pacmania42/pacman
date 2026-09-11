from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.scene_id import SceneId
from src.core.transitions import Push, Quit, Replace, Transition
from src.core.window import Window
from src.ui import theme, ui


class Menu:
    def __init__(self) -> None:
        self.items: list[str] = ["Start", "Instructions", "Highscore", "Exit"]
        self.current: int = 0

    def _move(self, n: int) -> None:
        self.current = (n + self.current) % len(self.items)

    def move_down(self) -> None:
        self._move(1)

    def move_up(self) -> None:
        self._move(-1)

    def get_items(self) -> list[str]:
        return self.items

    def get_item(self) -> str:
        return self.items[self.current]


class MenuScene(Scene):
    def __init__(self) -> None:
        super().__init__()

        self.menu = Menu()

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.DOWN):
            self.menu.move_down()
        elif inputs.was_pressed(Action.UP):
            self.menu.move_up()
        elif inputs.was_pressed(Action.BACK):
            return Quit()
        elif inputs.was_pressed(Action.CONFIRM):
            action = self.menu.get_item()
            if action == "Start":
                return Replace(SceneId.GAMEPLAY)
            if action == "Instructions":
                return Push(SceneId.INSTRUCTIONS)
            if action == "Highscore":
                return Push(SceneId.HIGHSCORE)
            if action == "Exit":
                return Quit()
        return None

    def draw(self, window: Window) -> None:
        top = self._draw_wordmark(window)
        self._draw_items(window, top)
        ui.footer(window, "ARROWS  move      SPACE  select      ESC  quit")

    def _draw_wordmark(self, window: Window) -> int:
        """The oversized title, underlined by the four colors"""
        title = "PAC-MAN"
        top = 90
        width = window.text_width(title, theme.SCALE_HERO)
        ui.centered(window, top, title, theme.TITLE, theme.SCALE_HERO)
        rule_y = top + window.ink_height(theme.SCALE_HERO) + theme.GAP
        return ui.ghost_rule(
            window, (window.width - width) // 2, rule_y, width
        ) + 2 * theme.GAP

    def _draw_items(self, window: Window, top: int) -> None:
        items = self.menu.get_items()
        row_height = window.ink_height(theme.SCALE_ITEM_ACTIVE)
        pitch = row_height + 2 * theme.GAP
        top = ui.block_top(window, top, len(items) * pitch)

        bar_width = max(
            window.text_width(item.upper(), theme.SCALE_ITEM_ACTIVE)
            for item in items
        ) + 2 * theme.MARGIN
        bar_x = (window.width - bar_width) // 2

        for i, item in enumerate(items):
            active = i == self.menu.current
            scale = theme.SCALE_ITEM_ACTIVE if active else theme.SCALE_ITEM
            color = theme.SELECTED if active else theme.TEXT
            label = item.upper()

            row_y = top + i * pitch
            x = (window.width - window.text_width(label, scale)) // 2
            y = row_y + (row_height - window.ink_height(scale)) // 2

            if active:
                window.put_box(
                    bar_x,
                    row_y - theme.GAP // 2,
                    bar_width,
                    row_height + theme.GAP,
                    theme.HIGHLIGHT,
                )
                cursor_w = window.text_width(theme.CURSOR, scale)
                window.put_text(
                    x - cursor_w - theme.GAP,
                    y + 10,
                    theme.CURSOR,
                    color,
                    scale
                )

            window.put_text(x, y + scale * 2, label, color, scale)

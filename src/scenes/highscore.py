from itertools import cycle
from typing import Any, Optional

from src.core.context import Context
from src.core.highscore import HighscoreItem
from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.transitions import Pop, Transition
from src.core.window import Window
from src.ui import theme, ui

GUTTER = theme.MARGIN // 2
"""Space between rank, name and score columns"""

RIGHT_ALIGNED = (True, False, True)
"""Rank and score right aligned. name left aligned"""


class HighScoreScene(Scene):
    def __init__(self, ctx: Context) -> None:
        super().__init__()
        self.ctx = ctx
        self.fresh: Optional[HighscoreItem] = None

    def on_enter(self, payload: Optional[Any] = None) -> None:
        """Select the highscore entry passed as payload"""
        self.fresh = payload if isinstance(payload, HighscoreItem) else None

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.BACK):
            return Pop()

        return None

    def draw(self, window: Window) -> None:
        top = ui.screen_title(
            window,
            theme.MARGIN // 2,
            "HIGH SCORES",
            ui.rule_shift(self.clock),
        )
        scale = theme.SCALE_HEADING
        ranked = self._ranked()

        if ranked:
            self._draw_table(window, top, ranked, scale)
        else:
            y = ui.block_top(window, top, window.text_height(scale))
            ui.centered(window, y, "NO SCORES YET", theme.MUTED, scale)

        ui.footer(window, "ESC   back to menu")

    def _ranked(self) -> list[HighscoreItem]:
        """Sort the scores, highests first"""
        return sorted(
            self.ctx.highscore.data,
            key=lambda item: item.score,
            reverse=True,
        )

    def _cells(self, ranked: list[HighscoreItem]) -> list[tuple[str, ...]]:
        """One cell per column, unpadded: the layout aligns them"""
        return [
            (str(rank), item.name, str(item.score))
            for rank, item in enumerate(ranked, start=1)
        ]

    def _widths(
        self, window: Window, cells: list[tuple[str, ...]], scale: int
    ) -> list[int]:
        """The width of the widest cell in each column"""
        return [
            max(window.text_width(row[col], scale) for row in cells)
            for col in range(len(RIGHT_ALIGNED))
        ]

    def _pulsed_row(self, ranked: list[HighscoreItem]) -> int:
        """Index of the row that should pulsate"""
        for index, item in enumerate(ranked):
            if item is self.fresh:
                return index
        return 0

    def _draw_table(
        self,
        window: Window,
        top: int,
        ranked: list[HighscoreItem],
        scale: int,
    ) -> None:
        """Draw the table centered"""
        cells = self._cells(ranked)
        widths = self._widths(window, cells, scale)
        table_width = sum(widths) + GUTTER * (len(widths) - 1)
        left = max(theme.MARGIN, (window.width - table_width) // 2)

        row_height = window.text_height(scale)
        y = ui.block_top(window, top, len(cells) * row_height)
        colors = cycle(theme.HEADINGS)
        pulsed = self._pulsed_row(ranked)

        for index, row in enumerate(cells):
            base = ui.pulse(self.clock) if index == pulsed else next(colors)
            color = ui.reveal(base, index, self.clock)
            x = left
            for col, text in enumerate(row):
                pad = widths[col] - window.text_width(text, scale)
                window.put_text(
                    x + pad if RIGHT_ALIGNED[col] else x,
                    y,
                    text,
                    color,
                    scale,
                )
                x += widths[col] + GUTTER
            y += row_height

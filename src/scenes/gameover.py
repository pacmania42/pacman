from typing import Any, Final, Optional

from src.core.context import Context
from src.core.highscore import LIST_MAX_SIZE, NAME_MAX_LENGTH
from src.core.input import Action, InputState
from src.core.scene import Scene
from src.core.scene_id import SceneId
from src.core.transitions import Pop, Replace, Transition
from src.core.window import Window
from src.game_state import GameResult
from src.ui import theme, ui
from src.ui.game_view import PLAYER_IDLE, PLAYER_WALK

WHEEL: Final[str] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "

BLANK: Final[int] = WHEEL.index(" ")

REPEAT_DELAY: Final[float] = 0.4
"""seconds after a key press become held"""

REPEAT_RATE: Final[float] = 0.08
"""seconds between repetitions fired"""


class GameOverScene(Scene):
    """Game over screen, won or lost"""

    def __init__(self, ctx: Context) -> None:
        super().__init__()
        self.highscore = ctx.highscore
        self.won = False
        self.score = 0
        self.slots = [BLANK] * NAME_MAX_LENGTH
        self.cursor = 0
        self.repeat_at = REPEAT_DELAY

    def on_enter(self, payload: Optional[Any] = None) -> None:
        if isinstance(payload, GameResult):
            self.won, self.score = payload.won, payload.score

    @property
    def name(self) -> str:
        return "".join(WHEEL[index] for index in self.slots).strip()

    @property
    def done(self) -> bool:
        return (
            self.slots[self.cursor] == BLANK
            or self.cursor == NAME_MAX_LENGTH - 1
        )

    @property
    def qualifies(self) -> bool:
        return self.highscore.qualifies(self.score)

    def update(self, inputs: InputState) -> Transition:
        if inputs.was_pressed(Action.BACK):
            return Pop()
        if not self.qualifies:
            return Pop() if inputs.was_pressed(Action.CONFIRM) else None

        if inputs.was_pressed(Action.CONFIRM):
            if self.done:
                return self._save() if self.name else None
            self.cursor += 1
        elif inputs.was_pressed(Action.RIGHT):
            self.cursor = min(self.cursor + 1, NAME_MAX_LENGTH - 1)
        elif inputs.was_pressed(Action.LEFT):
            self.cursor = max(self.cursor - 1, 0)
        else:
            self._turn(inputs)
        return None

    def _save(self) -> Transition:
        """record the entry and show it in the highscore"""
        item = self.highscore.add(self.name, self.score)
        self.highscore.save_to_file()
        return Replace(SceneId.HIGHSCORE, item)

    def _turn(self, inputs: InputState) -> None:
        """turn the wheel under the cursor"""
        for action, step in ((Action.DOWN, 1), (Action.UP, -1)):
            if inputs.was_pressed(action):
                self._step(step)
                self.repeat_at = self.clock + REPEAT_DELAY
                return
            if inputs.is_held(action) and self.clock >= self.repeat_at:
                self._step(step)
                self.repeat_at = self.clock + REPEAT_RATE
                return

    def _step(self, step: int) -> None:
        self.slots[self.cursor] = (self.slots[self.cursor] + step) % len(WHEEL)

    def draw(self, window: Window) -> None:
        top = self._draw_banner(window)
        if self.qualifies:
            self._draw_entry(window, top)
            ui.footer(window, self._hint())
        else:
            self._draw_score_only(window, top)
            ui.footer(window, "ENTER   back to menu")

    def _draw_banner(self, window: Window) -> int:
        if self.won:
            return self._draw_victory(window)
        return self._draw_defeat(window)

    def _draw_victory(self, window: Window) -> int:
        word, scale = "VICTORY", theme.SCALE_HERO
        x, width = theme.MARGIN, window.width - 2 * theme.MARGIN
        shift = ui.rule_shift(self.clock * 2)

        y = ui.ghost_rule(window, x, theme.MARGIN // 2, width, shift)
        y += theme.GAP
        ui.centered(window, y + 10, word, ui.pulse(self.clock), scale)

        frame = window.sprites.frame(PLAYER_WALK, self.clock)
        half = window.text_width(word, scale) // 2 + 2 * theme.GAP

        y += window.ink_height(scale) + theme.GAP
        sprite_y = y - frame.height + 35
        window.blit(
            frame, window.width // 2 - half - frame.width, sprite_y, flip=True
        )
        window.blit(frame, window.width // 2 + half, sprite_y, flip=True)
        y = ui.ghost_rule(window, x, y, width, -shift) + 2 * theme.GAP
        y = ui.centered(
            window,
            y,
            "CONGRATULATIONS",
            ui.reveal(theme.HEADINGS[2], 0, self.clock),
            theme.SCALE_HEADING,
        )
        return y + theme.GAP

    def _draw_defeat(self, window: Window) -> int:
        y = ui.screen_title(window, theme.MARGIN // 2, "GAME OVER")
        frame = window.sprites.frame(PLAYER_IDLE, self.clock)
        window.blit(frame, (window.width - frame.width) // 2, y)
        y = ui.centered(
            window,
            y + frame.height + theme.GAP,
            "THE GHOSTS GOT YOU",
            ui.reveal(theme.MUTED, 0, self.clock),
            theme.SCALE_HEADING,
        )
        return y + theme.GAP

    def _draw_score(self, window: Window, y: int) -> int:
        y = ui.centered(
            window,
            y,
            "SCORE",
            ui.reveal(theme.HEADINGS[0], 0, self.clock),
            theme.SCALE_HEADING,
        )
        return ui.centered(
            window,
            y,
            str(self.score),
            ui.reveal(theme.TITLE, 1, self.clock),
            theme.SCALE_TITLE,
        )

    def _score_height(self, window: Window) -> int:
        return window.text_height(theme.SCALE_HEADING) + window.text_height(
            theme.SCALE_TITLE
        )

    def _draw_score_only(self, window: Window, top: int) -> None:
        """no name to ask for, score did't make to top highscores"""
        note = f"not enough for the top {LIST_MAX_SIZE}"
        height = (
            self._score_height(window)
            + theme.GAP
            + window.text_height(theme.SCALE_BODY)
        )
        y = ui.block_top(window, top, height)
        y = self._draw_score(window, y) + theme.GAP
        ui.centered(window, y, note, ui.reveal(theme.MUTED, 2, self.clock))

    def _draw_entry(self, window: Window, top: int) -> None:
        prompt_height = window.text_height(theme.SCALE_HEADING)
        height = (
            self._score_height(window)
            + theme.GAP
            + prompt_height
            + theme.GAP
            + self._reel_height(window)
        )
        y = ui.block_top(window, top, height)
        y = self._draw_score(window, y) + theme.GAP
        y = ui.centered(
            window,
            y,
            "ENTER YOUR NAME",
            ui.reveal(theme.HEADINGS[1], 2, self.clock),
            theme.SCALE_HEADING,
        )
        self._draw_reel(window, y + theme.GAP)

    def _reel_rows(self, window: Window) -> tuple[int, int, int, int]:
        """heights of the four rows of the reel:
        letter above, letter itself, underline, letter below
        """
        above = 0
        letter = above + window.text_height(theme.SCALE_TITLE)
        rule = letter + window.ink_height(theme.SCALE_HERO) + theme.GAP // 2
        below = rule + theme.RULE_HEIGHT + theme.GAP
        return above, letter, rule, below

    def _reel_height(self, window: Window) -> int:
        return self._reel_rows(window)[-1] + window.text_height(
            theme.SCALE_TITLE
        )

    def _draw_reel(self, window: Window, top: int) -> None:
        """letter above, letter itself, underline, letter below"""
        big, small = theme.SCALE_HERO, theme.SCALE_TITLE
        above, letter, rule, below = self._reel_rows(window)
        width = max(window.text_width(char, big) for char in WHEEL)
        pitch = width + 2 * theme.GAP
        left = (window.width - NAME_MAX_LENGTH * pitch + 2 * theme.GAP) // 2

        text = ui.reveal(theme.TEXT, 3, self.clock)
        muted = ui.reveal(theme.MUTED, 3, self.clock)
        active = ui.reveal(ui.pulse(self.clock, theme.SELECTED), 3, self.clock)

        for slot, index in enumerate(self.slots):
            x = left + slot * pitch
            editing = slot == self.cursor
            color = active if editing else text
            self._glyph(
                window, x, top + letter, width, WHEEL[index], color, big
            )
            window.put_box(x, top + rule, width, theme.RULE_HEIGHT, color)
            if editing:
                prev, next = WHEEL[index - 1], WHEEL[(index + 1) % len(WHEEL)]
                self._glyph(window, x, top + above, width, prev, muted, small)
                self._glyph(window, x, top + below, width, next, muted, small)

    @staticmethod
    def _glyph(
        window: Window,
        x: int,
        y: int,
        width: int,
        char: str,
        color: int,
        scale: int,
    ) -> None:
        """draw one character, centered"""
        pad = (width - window.text_width(char, scale)) // 2
        window.put_text(x + pad, y, char, color, scale)

    def _hint(self) -> str:
        confirm = "save" if self.done else "next"
        return (
            "UP DOWN  letter      LEFT RIGHT  slot      "
            f"ENTER  {confirm}      ESC  skip"
        )

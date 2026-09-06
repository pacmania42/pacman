from typing import Dict

from src.pacman.input import Action


class Settings:
    def __init__(self) -> None:
        #
        self.tick = 1 / 60
        self.win_width = 1200
        self.win_height = 800
        self.window_title: str = "Pac-Man"

        # spacings
        self.cell_dim = 72
        self.wall_thickness = self.cell_dim // 10
        self.txt_pane_width = 350
        self.x_offset = 30
        self.y_offset = 30

        # colors
        self.off_color = 0x000000
        self.text_color = 0x00FF00
        self.colors = (
            (0x1E51A4, 0xFFFF00),
            (0xBD632F, 0xABC4FF),
            (0x52528C, 0xFF8500),
            (0x32746D, 0xFFFFFF),
        )

        # actions
        self.bindings: Dict[int, Action] = {
            0xFF52: Action.UP,
            0xFF54: Action.DOWN,
            0xFF51: Action.LEFT,
            0xFF53: Action.RIGHT,
            0x77: Action.UP,
            0x73: Action.DOWN,
            0x61: Action.LEFT,
            0x64: Action.RIGHT,
            0xFF0D: Action.CONFIRM,
            0x20: Action.CONFIRM,
            0xFF1B: Action.BACK,
            0x70: Action.PAUSE,
        }

        # keybindings
        self.close_win = 0xFF1B
        self.new_maze = 0x6D
        self.toggle_path = 0x70
        self.change_color = 0x63
        self.toggle_animation = 0x61

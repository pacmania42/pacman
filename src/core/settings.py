from typing import Dict

from src.core.input import Action


class Settings:
    #
    tick = 1 / 60
    win_width = 1200
    win_height = 800
    window_title: str = "Pac-Man"

    # spacings
    cell_dim = 72
    wall_thickness = cell_dim // 10
    txt_pane_width = 350
    x_offset = 30
    y_offset = 30

    # colors
    off_color = 0x000000
    text_color = 0x00FF00
    colors = (
        (0x1E51A4, 0xFFFF00),
        (0xBD632F, 0xABC4FF),
        (0x52528C, 0xFF8500),
        (0x32746D, 0xFFFFFF),
    )

    # actions
    bindings: Dict[int, Action] = {
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
    close_win = 0xFF1B
    new_maze = 0x6D
    toggle_path = 0x70
    change_color = 0x63
    toggle_animation = 0x61

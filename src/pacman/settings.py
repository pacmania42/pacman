class Settings:
    def __init__(self) -> None:
        #
        self.tick = 1 / 60
        self.window_title: str = "Pac-Man"

        # spacings
        self.cell_dim = 72
        self.wall_thickness = self.cell_dim // 10
        self.txt_pane_width = 350
        self.x_offset = 30
        self.y_offset = 30

        # colors
        self.off_color = 0x000000
        self.pattern_color = 0x800080
        self.entry_color = 0xFF0000
        self.exit_color = 0x00FF00
        self.text_color = 0x00FF00
        self.colors = (
            (0x1E51A4, 0xFFFF00),
            (0xBD632F, 0xABC4FF),
            (0x52528C, 0xFF8500),
            (0x32746D, 0xFFFFFF),
        )

        # keybindings
        self.close_win = 0xFF1B
        self.new_maze = 0x6D
        self.toggle_path = 0x70
        self.change_color = 0x63
        self.toggle_animation = 0x61

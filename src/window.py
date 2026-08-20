import arcade


class Window(arcade.Window):
    def __init__(self) -> None:
        super().__init__(width=1200, height=800, title="Pac-Man")

from typing import Any

from mlx import Mlx
from enum import Enum, auto

class BaseState:
    """Interface that every distinct game state must implement."""
    def handle_keypress(self, keycode, game_engine):
        raise NotImplementedError

    def draw(self, mlx_instance, win_instance, game_engine):
        """Every state handles its own rendering layout."""
        raise NotImplementedError

class Menu:

    def __init__(self) -> None:
        self.items: list[str] = ["Start", "Highscore", "Exit"]
        self.current: int = 0

    def _move(self, n: int) -> None:
        self.current = (n + self.current) % len(self.items)

    def move_down(self) -> None:
        self._move(1)

    def move_up(self) -> None:
        self._move(-1)

    def get_items(self) -> list[str]:
        return self.items

    def get_item(self):
        return self.items[self.current]



class MenuState(BaseState):
    def handle_keypress(self, keycode, game_engine) -> None:
        if keycode == 115 or keycode == 65364:  
            game_engine.menu.move_down()
        elif keycode == 119 or keycode == 65362: 
            game_engine.menu.move_up()
        elif keycode == 65293: #select
            action = game_engine.menu.get_item()
            if("Exit"):
                close_window()

    def draw(self, m, mlx_ptr, win_ptr, game_engine):
        COLOR_WHITE = 0xFFFFFF
        COLOR_BLUE = 0xFFFF00
        COLOR_RED = 0x0000FF

        m.mlx_clear_window(mlx_ptr, win_ptr)
        for i, item in enumerate(game_engine.menu.get_items()):
            color = COLOR_RED if game_engine.menu.current == i else COLOR_WHITE
            m.mlx_string_put(mlx_ptr, win_ptr, 100, 300 + i*20, color, item)

        m.mlx_string_put(mlx_ptr, win_ptr, 50, 50, COLOR_WHITE, "Main Menu")
        m.mlx_string_put(mlx_ptr, win_ptr, 50, 100, COLOR_WHITE, "Press ESC to Exit")

class GameContext(Enum):
    MENU = auto()
    GAMEPLAY = auto()
    PAUSE = auto()

class GameEngine:
    def __init__(self, mlx_instance, mlx_ptr, mlx_win):
        self.m = mlx_instance
        self.mlx_ptr: Any = mlx_ptr
        self.mlx_win = mlx_win

        self.states = {
            GameContext.MENU: MenuState(),
            GameContext.GAMEPLAY: None
        }
        # Set the starting state
        self.current_context: Literal[GameContext.MENU] = GameContext.MENU
        self.menu = Menu()

    def update_and_render(self, param):
        active_state = self.states[self.current_context]
        
        active_state.draw(self.m, self.mlx_ptr, self.mlx_win, self)


def close_window() -> None:
    m.mlx_loop_exit(mlx_ptr)

def keypress(keycode, data) -> None:
    print(f"k {keycode}")
    if keycode == 97:
        print("mmmmmm")
    if keycode == 65307: #ESC
        close_window()

def event(event) -> None:
    if event == "close":
        close_window()

m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 800, 800, "jjjjj")

m.mlx_key_hook(win_ptr, keypress, None)
m.mlx_hook(win_ptr, 2, 1<<0, keypress, None) # keydown
m.mlx_hook(win_ptr, 33, 0, event, "close") # win x icon

game = GameEngine(m, mlx_ptr, win_ptr)

m.mlx_hook(win_ptr, 2, 1<<0, lambda keycode, p: game.states[game.current_context].handle_keypress(keycode, game), None)

m.mlx_loop_hook(mlx_ptr, game.update_and_render, None)

m.mlx_loop(mlx_ptr)
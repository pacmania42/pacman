from mlx import mlx


def main() -> None:
    m = mlx.Mlx()
    mlx_ptr = m.mlx_init()
    win_ptr = m.mlx_new_window(mlx_ptr, 600, 400, "New Window")
    m.mlx_hook(win_ptr, 0x21, 0, lambda _: m.mlx_loop_exit(mlx_ptr), None)
    m.mlx_loop(mlx_ptr)

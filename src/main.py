from argparse import ArgumentParser, Namespace
from pathlib import Path

from src.adapter import MazeAdapterError
from src.config import ConfigLoader, ParserError
from src.models import Level
from src.window import Window


def main() -> None:
    args = parse_cmd_args()
    try:
        config = ConfigLoader().load(Path(args.config))
    except ParserError as e:
        print(e)
        return
    levels: list[Level] = []
    for rank, lvl in enumerate(config.levels):
        try:
            levels.append(
                Level(
                    rank=rank,
                    width=lvl.width,
                    height=lvl.height,
                )
            )
        except MazeAdapterError as e:
            print(e)
            return

        _ = levels[-1]

    win = Window()
    win.run()


def parse_cmd_args() -> Namespace:
    parser = ArgumentParser(
        prog="uv run python pac-man.py",
        description="Pacman clone.",
    )

    parser.add_argument("config")
    return parser.parse_args()

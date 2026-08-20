from src.adapter import AdapterError
from src.config import Parser, ParserError
from src.models import Level


def main() -> None:
    try:
        config = Parser().get_config()
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
            except AdapterError as e:
                print(e)
                return

            lv = levels[-1]
            print(lv.rank, lv.width, lv.height, lv.seed, lv.generator)
    except ParserError as e:
        print(e)
        return

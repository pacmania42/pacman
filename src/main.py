from src.config import Parser, ParserError


def main() -> None:
    try:
        config = Parser().get_config()
        print(config)
    except ParserError as e:
        print(e)
        return

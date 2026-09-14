import os
from pathlib import Path
from typing import Annotated, Final

from pydantic import BaseModel, Field, TypeAdapter, ValidationError

LIST_MAX_SIZE: Final[int] = 10

NAME_MAX_LENGTH: Final[int] = 10


class HighscoreItem(BaseModel):
    name: str = Field(max_length=NAME_MAX_LENGTH, pattern=r"^[A-Za-z0-9 ]+$")
    score: int = Field(ge=0)


class HighScore:
    def __init__(self, filename: str):
        self.file = Path(filename)
        self.data = self.loadfile()

    def loadfile(self) -> list[HighscoreItem]:
        try:
            content = self.file.read_text(encoding="utf-8")
        except FileNotFoundError as e:
            path = Path(self.file)
            path.write_text("[]", encoding="utf-8")
            print(f"File not found ({e}), creating new one")
            return []
        except OSError as e:
            print(f"Cannot read highscores ({e}), starting empty")
            return []

        try:
            items: list[HighscoreItem] = TypeAdapter(
                Annotated[list[HighscoreItem], Field(max_length=LIST_MAX_SIZE)]
            ).validate_json(content)
        except ValidationError as e:
            print(e)
            return self.backup()

        return items

    def backup(self) -> list[HighscoreItem]:
        backup = self.file.with_name(self.file.name + ".bak")
        print(f"Invalid highscore file, moved to {backup.name}")
        try:
            self.file.replace(backup)
        except OSError:
            pass
        return []

    def add(self, name: str, score: int) -> HighscoreItem:
        item = HighscoreItem(name=name, score=score)
        self.data.append(item)
        self.data.sort(key=lambda x: x.score, reverse=True)
        del self.data[LIST_MAX_SIZE:]
        return item

    def qualifies(self, score: int) -> bool:
        """if a `score` would stay in the table once added.

        On a tie the older entry keeps its place
        """
        if len(self.data) < LIST_MAX_SIZE:
            return True
        return score > min(item.score for item in self.data)

    def save_to_file(self) -> None:
        json_data = TypeAdapter(list[HighscoreItem]).dump_json(
            self.data, indent=2
        )

        tmp = self.file.with_name(self.file.name + ".tmp")
        try:
            tmp.write_bytes(json_data)
            os.replace(tmp, self.file)
        except OSError as e:
            print(f"Cannot save highscores: {e}")

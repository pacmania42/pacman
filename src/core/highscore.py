import os
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, TypeAdapter, ValidationError


class HighscoreItem(BaseModel):
    name: str = Field(max_length=10, pattern=r"^[A-Za-z0-9 ]+$")
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
                Annotated[list[HighscoreItem], Field(max_length=10)]
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
        del self.data[10:]
        return item

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

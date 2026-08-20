import json

from pydantic import BaseModel, Field, ValidationError


class LevelConfig(BaseModel):
    width: int = Field(ge=6, le=20, default=10)
    height: int = Field(ge=6, le=20, default=10)


class Config(BaseModel):
    highscore_filename: str = Field(default="highscore.json")
    lives: int = Field(ge=1, default=3)
    pacgum: int = Field(ge=0, default=42)
    points_per_pacgum: int = Field(ge=0, default=50)
    points_per_ghost: int = Field(ge=0, default=200)
    seed: int = Field(default=42)
    level_max_time: int = Field(gt=0, default=90)
    levels: list[LevelConfig] = Field(min_length=1)


class ParserError(Exception):
    pass


class Parser:
    def read_config_file(self, filename: str) -> list[str]:
        try:
            with open(filename) as file:
                return file.readlines()
        except OSError as e:
            raise ParserError(e) from e

    def strip_comment_lines(self, lines: list[str]) -> str:
        res = []
        for line in lines:
            if line.lstrip().startswith("#"):
                continue
            res.append(line)
        return "".join(res)

    def get_config(self) -> Config:
        lines = self.read_config_file("config.json")
        content = self.strip_comment_lines(lines)

        try:
            data = json.loads(content)
            return Config(**data)
        except json.JSONDecodeError as e:
            raise ParserError(f"Malformed config file: {e}") from e
        except ValidationError as e:
            raise ParserError(
                f"Validation Error: {e}"
            ) from e  # TODO: clamp to defs

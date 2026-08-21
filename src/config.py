import json
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    ValidationInfo,
    field_validator,
)


class LevelConfig(BaseModel):
    width: int = Field(ge=6, le=20, default=10)
    height: int = Field(ge=6, le=20, default=10)

    @field_validator("width", "height", mode="before")
    @classmethod
    def clamp_fields(cls, v: int, info: ValidationInfo) -> int:
        if not info.field_name:
            return 10
        default: int = cls.model_fields[info.field_name].default
        try:
            v = int(v)
            if v < 6 or v > 20:
                v = default
            return v
        except (TypeError, ValueError):
            print(f"Invalid {info.field_name}={v}, using {default}")
            return default


class Config(BaseModel):
    highscore_filename: str = Field(default="highscore.json")
    lives: int = Field(ge=1, default=3)
    pacgum: int = Field(ge=0, default=42)
    points_per_pacgum: int = Field(ge=0, default=50)
    points_per_ghost: int = Field(ge=0, default=200)
    seed: int = Field(default=42)
    level_max_time: int = Field(gt=0, default=90)
    levels: list[LevelConfig] = Field(
        min_length=1, default_factory=lambda: [LevelConfig()]
    )


class ParserError(Exception):
    pass


class ConfigLoader:
    def parse_cmd_args(self) -> Namespace:
        parser = ArgumentParser(
            prog="uv run python pac-man.py",
            description="Pacman clone.",
        )

        parser.add_argument("config")
        return parser.parse_args()

    def read_config_file(self, filename: Path) -> list[str]:
        try:
            with open(filename) as file:
                return file.readlines()
        except OSError as e:
            raise ParserError(e) from e

    def strip_comments(self, lines: list[str]) -> str:
        res = []
        for line in lines:
            if line.lstrip().startswith("#"):
                continue
            res.append(line)
        return "".join(res)

    def load(self, filename: Path) -> Config:
        # filename = self.parse_cmd_args().config
        lines = self.read_config_file(filename)
        content = self.strip_comments(lines)

        try:
            data: dict[str, Any] = json.loads(content)
        except json.JSONDecodeError as err:
            raise ParserError(f"Malformed config file: {err}") from err
        else:
            while True:
                try:
                    return Config(**data)
                except ValidationError as err:
                    for e in err.errors():
                        key: str = str(e["loc"][0])
                        print(f"Invalid {key}, using default value.")
                        data.pop(key)

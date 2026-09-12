import json
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    ValidationInfo,
    field_validator,
)


class Level(BaseModel):
    width: int = Field(ge=6, le=20, default=10)
    height: int = Field(ge=6, le=20, default=10)
    seed: int | None = Field(default=None)

    @field_validator("width", "height", mode="before")
    @classmethod
    def clamp_fields(cls, v: int, info: ValidationInfo) -> int:
        if not info.field_name:
            return 10
        default: int = cls.model_fields[info.field_name].default
        try:
            v = int(v)
            if v < 6 or v > 20:
                raise ValueError
            return v
        except (TypeError, ValueError, OverflowError):
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
    levels: list[Level] = Field(
        min_length=1, default_factory=lambda: [Level()]
    )


class ConfigError(Exception):
    pass


class ConfigLoader:
    def load(self) -> Config:
        parser = ArgumentParser(
            prog="uv run python pac-man.py",
            description="Pacman clone.",
        )
        parser.add_argument("config", metavar="<CONFIG>")
        args = parser.parse_args()
        return self.parse(Path(args.config))

    def read_config_file(self, filename: Path) -> list[str]:
        try:
            with open(filename, encoding="utf-8") as file:
                return file.readlines()
        except OSError as e:
            raise ConfigError(e) from e

    def strip_comments(self, lines: list[str]) -> str:
        res = []
        for line in lines:
            if line.lstrip().startswith("#"):
                line = "\n"
            res.append(line)
        return "".join(res)

    def parse(self, filename: Path) -> Config:
        lines = self.read_config_file(filename)
        content = self.strip_comments(lines)

        # validate and adjust the JSON
        try:
            data: dict[str, Any] = json.loads(content)
        except json.JSONDecodeError as err:
            raise ConfigError(
                f"Malformed config: line {err.lineno}, column {err.colno}"
            ) from err

        data = self.coerce_to_dict(data)

        # validate levels
        levels = data.get("levels", [])
        if not isinstance(levels, list):
            levels = []
        for level in levels.copy():
            if not isinstance(level, dict):
                levels.remove(level)

        for rank in range(len(levels), 10):
            levels.append({"width": 11 + rank, "height": 11 + rank})

        data["levels"] = levels

        # validate the entire config
        while True:
            try:
                return Config(**data)
            except ValidationError as err:
                for e in err.errors():
                    key: str = str(e["loc"][0])
                    print(f"Invalid {key}, using default value.")
                    data.pop(key)

    def coerce_to_dict(self, data: Any) -> dict[str, Any]:
        if isinstance(data, list):
            data = {"levels": data}
        if isinstance(data, dict):
            return data
        else:
            raise ConfigError(f"Invalid config: {data}")

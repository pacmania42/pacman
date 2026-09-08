import json
import os
import tempfile
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from src.pacman.core.config import (
    Config,
    ConfigError,
    ConfigLoader,
    LevelConfig,
)


def build_valid_config_dict(
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    base = {
        "highscore_filename": "highscore.json",
        "lives": 3,
        "pacgum": 42,
        "points_per_pacgum": 50,
        "points_per_ghost": 200,
        "seed": 42,
        "level_max_time": 90,
        "levels": [{"width": 10, "height": 10}],
    }
    if overrides:
        base.update(overrides)
    return base


# Helper to write a temp config file
def write_tempfile(content: str) -> Path:
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return Path(path)


def test_parser_reads_valid_config() -> None:
    config_data = build_valid_config_dict()
    config_json = json.dumps(config_data)
    path = write_tempfile(config_json)
    cfg = ConfigLoader().parse(path)

    assert isinstance(cfg, Config)
    assert cfg.lives == 3
    assert cfg.levels[0].width == 10


def test_valid_array_json() -> None:
    config_json = '[ { "width": 12, "height": 12 } ]'
    path = write_tempfile(config_json)
    cfg = ConfigLoader().parse(path)

    assert isinstance(cfg, Config)
    assert cfg.lives == 3
    assert cfg.levels[0].width == 12


def test_nonlist_levels() -> None:
    config_json = '{"levels": 2}'
    path = write_tempfile(config_json)
    cfg = ConfigLoader().parse(path)

    assert isinstance(cfg, Config)
    assert cfg.lives == 3
    assert cfg.levels[0].width == 11


def test_nondict_json() -> None:
    config_json = "2"
    path = write_tempfile(config_json)

    with pytest.raises(ConfigError):
        ConfigLoader().parse(path)


def test_nondict_level() -> None:
    config_json = '{"levels": [ "a","b"]}'
    path = write_tempfile(config_json)
    cfg = ConfigLoader().parse(path)

    assert isinstance(cfg, Config)
    assert cfg.lives == 3
    assert len(cfg.levels) == 10


def test_levels_with_nondict() -> None:
    config_json = (
        '{"levels": [ { "width": 12, "height": 12 }, '
        '{ "width": 12, "height": 12 }, "invalid"   ]}'
    )
    path = write_tempfile(config_json)
    cfg = ConfigLoader().parse(path)

    assert isinstance(cfg, Config)
    assert cfg.lives == 3
    assert len(cfg.levels) == 10
    assert cfg.levels[0].height == 12


def test_parser_handles_file_not_found() -> None:
    with pytest.raises(ConfigError):
        ConfigLoader().parse(Path("____file_not_found____"))


def test_parser_handles_malformed_json() -> None:
    path = write_tempfile(" { invalid json}")

    with pytest.raises(ConfigError):
        ConfigLoader().parse(path)


def test_strip_comment_lines() -> None:
    lines = ["# comment 1\n", '{"a": 1},\n', "  # comment 2\n"]
    result = ConfigLoader().strip_comments(lines)

    assert result.strip() == '{"a": 1},'


def test_config_with_unknown_key() -> None:
    base = build_valid_config_dict()
    base["unknown_key"] = "should be ignored"
    path = write_tempfile(json.dumps(base))
    cfg = ConfigLoader().parse(path)

    assert hasattr(cfg, "lives")
    assert not hasattr(cfg, "unknown_key")


def test_config_with_missing_optional_keys() -> None:
    base = {"levels": [{"width": 10, "height": 10}]}
    path = write_tempfile(json.dumps(base))
    cfg = ConfigLoader().parse(path)

    assert cfg.highscore_filename == "highscore.json"
    assert cfg.lives == 3
    assert cfg.levels[0].width == 10
    assert cfg.level_max_time == 90


def test_config_with_only_comments() -> None:
    lines = ["# Just a comment\n", "   # another one\n"]
    path = write_tempfile("".join(lines))

    with pytest.raises(ConfigError):
        ConfigLoader().parse(path)


def test_config_missing_fields() -> None:
    config: dict[str, Any] = {}
    path = write_tempfile(json.dumps(config))
    cfg = ConfigLoader().parse(path)

    assert cfg.lives == Config.model_fields["lives"].default


def test_config_invalid_fields() -> None:
    config = {"lives": "invalid_lives"}
    path = write_tempfile(json.dumps(config))
    cfg = ConfigLoader().parse(path)

    assert cfg.lives == Config.model_fields["lives"].default


# LevelConfig tests
def test_levelconfig_missing_field() -> None:
    res = LevelConfig(width=10)
    assert res.height == LevelConfig.model_fields["height"].default


def test_levelconfig_invalid_field() -> None:
    res = LevelConfig(
        width=10,
        height="invalid",  # type: ignore
    )
    assert res.height == LevelConfig.model_fields["height"].default


def test_config_levels_min_length() -> None:
    with pytest.raises(ValidationError):
        Config(levels=[])

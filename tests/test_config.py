import json
import os
import tempfile
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError
from pytest import MonkeyPatch

from src.config import Config, LevelConfig, Parser, ParserError


@pytest.fixture(autouse=True)
def patch_parse_cmd_args(monkeypatch: MonkeyPatch) -> None:
    from argparse import Namespace

    monkeypatch.setattr(
        Parser,
        "parse_cmd_args",
        lambda self: Namespace(config="dummy.json"),
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
def write_tempfile(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return path


def test_parser_reads_valid_config(
    tmp_path: "Path", monkeypatch: MonkeyPatch
) -> None:
    config_data = build_valid_config_dict()
    config_json = json.dumps(config_data)
    file_path = tmp_path / "config.json"
    file_path.write_text(config_json)

    p = Parser()
    monkeypatch.setattr(
        p, "read_config_file", lambda _: config_json.splitlines(True)
    )
    cfg = p.get_config()
    assert isinstance(cfg, Config)
    assert cfg.lives == 3
    assert cfg.levels[0].width == 10


def test_parser_handles_file_not_found(monkeypatch: MonkeyPatch) -> None:
    p = Parser()
    monkeypatch.setattr(
        p,
        "read_config_file",
        lambda filename: (_ for _ in ()).throw(ParserError("not found")),
    )
    with pytest.raises(ParserError):
        p.get_config()


def test_parser_handles_malformed_json(monkeypatch: MonkeyPatch) -> None:
    p = Parser()
    monkeypatch.setattr(
        p, "read_config_file", lambda filename: ["{ invalid json"]
    )
    with pytest.raises(ParserError):
        p.get_config()


def test_strip_comment_lines() -> None:
    lines = ["# comment 1\n", '{"a": 1},\n', "  # comment 2\n"]
    p = Parser()
    result = p.strip_comment_lines(lines)
    assert result.strip() == '{"a": 1},'


def test_config_with_unknown_key(monkeypatch: MonkeyPatch) -> None:
    base = build_valid_config_dict()
    base["unknown_key"] = "should be ignored"
    monkeypatch.setattr(
        Parser, "read_config_file", lambda _, f=None: [json.dumps(base)]
    )
    cfg = Parser().get_config()
    assert hasattr(cfg, "lives")
    assert not hasattr(cfg, "unknown_key")


def test_config_with_missing_optional_keys(monkeypatch: MonkeyPatch) -> None:
    base = {"levels": [{"width": 10, "height": 10}]}
    monkeypatch.setattr(
        Parser, "read_config_file", lambda _, f=None: [json.dumps(base)]
    )
    cfg = Parser().get_config()
    assert cfg.highscore_filename == "highscore.json"
    assert cfg.lives == 3
    assert cfg.levels[0].width == 10
    assert cfg.level_max_time == 90


def test_config_with_only_comments(monkeypatch: MonkeyPatch) -> None:
    lines = ["# Just a comment\n", "   # another one\n"]
    monkeypatch.setattr(Parser, "read_config_file", lambda _, f=None: lines)
    with pytest.raises(ParserError):
        Parser().get_config()


def test_config_missing_fields(monkeypatch: MonkeyPatch) -> None:
    config: dict[str, Any] = {}
    monkeypatch.setattr(
        Parser,
        "read_config_file",
        lambda _, f=None: [json.dumps(config)],
    )
    cfg = Parser().get_config()
    assert cfg.lives == Config.model_fields["lives"].default


def test_config_invalid_fields(monkeypatch: MonkeyPatch) -> None:
    config = {"lives": "invalid_lives"}
    monkeypatch.setattr(
        Parser,
        "read_config_file",
        lambda _, f=None: [json.dumps(config)],
    )
    cfg = Parser().get_config()
    assert cfg.lives == Config.model_fields["lives"].default


# LevelConfig tests
def test_levelconfig_missing_field() -> None:
    res = LevelConfig(width=10)
    assert res.height == LevelConfig.model_fields["height"].default


def test_levelconfig_invalid_field() -> None:
    res = LevelConfig(
        width=10,
        height="invalid",  # ty:ignore[invalid-argument-type]
    )
    assert res.height == LevelConfig.model_fields["height"].default


def test_config_levels_min_length() -> None:
    with pytest.raises(ValidationError):
        Config(levels=[])

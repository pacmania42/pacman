import pytest

from src.main import main


def test_main_returns_none() -> None:
    assert main() is None

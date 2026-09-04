import inspect

from src.main import main


def test_main_signature() -> None:
    sig = inspect.signature(main)
    assert sig.return_annotation is None

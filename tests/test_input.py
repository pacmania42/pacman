from src.core.input import FOCUS_LOST, EventBuffer
from src.core.window import EventSink

UP_ARROW = 0xFF52


def test_every_sink_method_records_an_event() -> None:
    """Check that each hook adds its event to the buffer.

    An empty method body would still pass the type check, so test
    what each one writes: True for a key down, False for a key up,
    and a None keycode for focus loss.
    """
    buffer = EventBuffer()
    sink: EventSink = buffer  # Window only sees these three methods

    sink.on_key_down(UP_ARROW, None)
    sink.on_key_up(UP_ARROW, None)
    sink.on_focus_out(None)

    assert buffer.drain() == [
        (UP_ARROW, True),
        (UP_ARROW, False),
        (FOCUS_LOST, False),
    ]
    # drain empties the buffer
    assert buffer.drain() == []

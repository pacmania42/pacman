from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

# Used in place of a keycode to mark where the window lost focus
FOCUS_LOST = None


class Action(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CONFIRM = auto()
    BACK = auto()
    PAUSE = auto()


@dataclass(frozen=True)
class InputState:
    """One frame's view of the keyboard.

    It handles actions, not keys
    """

    pressed: FrozenSet[Action]
    held: FrozenSet[Action]
    released: FrozenSet[Action]

    @classmethod
    def empty(cls) -> "InputState":
        """A frame in which nothing happened. Handy in tests."""
        return cls(frozenset(), frozenset(), frozenset())

    def was_pressed(self, action: Action) -> bool:
        return action in self.pressed

    def any_pressed(self, *actions: Action) -> bool:
        return not self.pressed.isdisjoint(actions)

    def is_held(self, action: Action) -> bool:
        return action in self.held

    def was_released(self, action: Action) -> bool:
        return action in self.released


class EventBuffer:
    """Holds events from mlx until the next frame reads them.

    mlx calls its hooks at any point inside its own loop, so this just
    stores what arrives. Nothing is interpreted here.

    `Window` hooks the three `on_*` methods. Those are its `EventSink`.
    """

    def __init__(self) -> None:
        self._events: List[Tuple[Optional[int], bool]] = []

    def on_key_down(self, keycode: int, _: object) -> None:
        self._events.append((keycode, True))

    def on_key_up(self, keycode: int, _: object) -> None:
        self._events.append((keycode, False))

    def on_focus_out(self, _: object) -> None:
        """The window lost focus.

        Goes in the buffer instead of clearing anything right away, so
        it keeps its place in the order. A key down that arrived just
        before it has to be dropped too.
        """
        self._events.append((FOCUS_LOST, False))

    def drain(self) -> List[Tuple[Optional[int], bool]]:
        """Hand over everything buffered since the last call"""
        events, self._events = self._events, []
        return events


class InputTracker:
    """Turns buffered key events into a per-frame `InputState`"""

    def __init__(
        self, bindings: Dict[int, Action], events: EventBuffer
    ) -> None:
        self.bindings = bindings
        self.events = events
        self._held: Set[Action] = set()
        self._pending_up: Set[Action] = set()

    def begin_frame(self) -> InputState:
        """Drain the buffer and put it into the state of current frame.

        Called once per frame, before any scene reads the inputs
        """
        pressed: Set[Action] = set()

        # X11 implements auto-repeat by rapidly firing multiple
        # Release event and a Press event for the same key.
        # We need to know when is held down instead.
        # Our solution is let a release waits one frame before being
        # reported: if the key comes back in that time it was a repeat,
        # not a release, and nothing is reported. What is still waiting
        # at the end of the frame was a real release.
        carried, self._pending_up = self._pending_up, set()

        for keycode, is_down in self.events.drain():
            if keycode is FOCUS_LOST:
                # An unfocused window gets no key events, so a key
                # held now would never get its release. Drop
                # everything, including what came earlier this frame.
                self.clear()
                carried.clear()
                pressed.clear()
                continue
            action: Optional[Action] = self.bindings.get(keycode)
            if action is None:
                continue
            if not is_down:
                self._pending_up.add(action)
                continue
            # a down cancels a waiting release, from either frame
            carried.discard(action)
            self._pending_up.discard(action)
            if action not in self._held:
                pressed.add(action)
                self._held.add(action)

        released = carried & self._held
        self._held -= released

        return InputState(
            pressed=frozenset(pressed),
            held=frozenset(self._held),
            released=frozenset(released),
        )

    def clear(self) -> None:
        """Forget every key without reporting a press or release.

        Also useful when a scene wants to start with nothing held
        """
        self._held.clear()
        self._pending_up.clear()

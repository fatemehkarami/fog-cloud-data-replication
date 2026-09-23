"""Deterministic simulation clock and event queue."""

from dataclasses import dataclass, field
import heapq
from typing import Any, Callable, List, Optional, Tuple


@dataclass
class SimulationClock:
    time: float = 0.0

    def advance_to(self, timestamp: float) -> None:
        if timestamp < self.time:
            raise ValueError("clock cannot move backwards")
        self.time = timestamp


@dataclass(frozen=True)
class Event:
    timestamp: float
    event_type: str
    sequence: int = 0
    payload: Any = None
    priority: int = 3


class EventQueue:
    def __init__(self) -> None:
        self._events: List[Tuple[float, int, int, Event]] = []
        self._next_sequence = 0

    def schedule(self, event: Event) -> Event:
        sequence = self._next_sequence
        self._next_sequence += 1
        scheduled = Event(event.timestamp, event.event_type, sequence, event.payload, event.priority)
        heapq.heappush(self._events, (scheduled.timestamp, scheduled.priority, scheduled.sequence, scheduled))
        return scheduled

    def pop(self) -> Optional[Event]:
        if not self._events:
            return None
        return heapq.heappop(self._events)[3]

    def __len__(self) -> int:
        return len(self._events)

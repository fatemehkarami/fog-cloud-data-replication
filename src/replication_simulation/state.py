"""Authoritative simulator state and scenario freeze/clone support."""

from copy import deepcopy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Dict, Mapping
from typing import Callable

from .domain import MetricRecord, Scenario


@dataclass
class SimulationState:
    scenario: Scenario
    current_time: float = 0.0
    event_sequence: int = 0
    observations: list = field(default_factory=list)
    frozen: bool = False

    def freeze(self) -> "SimulationState":
        self.frozen = True
        return self

    def clone(self) -> "SimulationState":
        cloned = deepcopy(self)
        cloned.frozen = False
        return cloned

    def record(self, observation: Any) -> None:
        self._ensure_mutable()
        self.observations.append(observation)

    def record_metric(self, metric: MetricRecord) -> None:
        self._ensure_mutable()
        self.observations.append(metric)

    def apply_mutation(self, mutation: Callable[["SimulationState"], None]) -> None:
        self._ensure_mutable()
        mutation(self)

    def _ensure_mutable(self) -> None:
        if self.frozen:
            raise RuntimeError("frozen simulation state cannot be mutated")

    def read_only_view(self) -> Mapping[str, Any]:
        return MappingProxyType(
            {
                "scenario": deepcopy(self.scenario),
                "current_time": self.current_time,
                "event_sequence": self.event_sequence,
                "observations": tuple(deepcopy(self.observations)),
            }
        )

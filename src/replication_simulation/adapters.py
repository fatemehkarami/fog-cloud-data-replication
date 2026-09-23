"""Read-only adapter boundary for future method implementations."""

from dataclasses import dataclass, field
from types import MappingProxyType
from dataclasses import is_dataclass, asdict
from typing import Any, Mapping, Optional, Tuple

from .decisions import DecisionEnvelope, DecisionKind
from .state import SimulationState


def _read_only(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _read_only(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_read_only(item) for item in value)
    if is_dataclass(value):
        return _read_only(asdict(value))
    return value


@dataclass(frozen=True)
class AdapterCapabilities:
    decisions: Tuple[DecisionKind, ...] = ()

    def supports(self, kind: DecisionKind) -> bool:
        return kind in self.decisions


@dataclass(frozen=True)
class AdapterSnapshot:
    scenario_id: str
    run_id: Optional[str]
    current_time: float
    scenario: Mapping[str, Any]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_state(
        cls, state: SimulationState, run_id: Optional[str] = None
    ) -> "AdapterSnapshot":
        view = state.read_only_view()
        return cls(
            scenario_id=state.scenario.scenario_id,
            run_id=run_id,
            current_time=state.current_time,
            scenario=_read_only(view["scenario"]),
            metadata=MappingProxyType({}),
        )


class SimulationAdapter:
    """Base contract: READ -> COMPUTE -> RETURN."""

    method_id = "unassigned"

    @property
    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities()

    def compute(self, snapshot: AdapterSnapshot) -> DecisionEnvelope:
        raise NotImplementedError("algorithm-specific adapter behavior is not implemented")

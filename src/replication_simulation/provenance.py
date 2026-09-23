"""Run provenance and raw observation records."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class RunMetadata:
    experiment_id: str
    scenario_id: str
    run_id: str
    method_id: str
    source_version: Optional[str] = None
    implementation_version: Optional[str] = None
    seed_identity: Optional[str] = None
    random_stream_identity: Optional[str] = None
    configuration_identity: Optional[str] = None
    clock_metadata: Tuple[Tuple[str, Any], ...] = ()
    decision_provenance: Tuple[Tuple[str, Any], ...] = ()
    interpretation_status: Optional[str] = None


@dataclass(frozen=True)
class RawObservation:
    observation_type: str
    timestamp: Optional[float]
    payload: Tuple[Tuple[str, Any], ...] = ()
    provenance: Optional[RunMetadata] = None


class RawRecorder:
    def __init__(self) -> None:
        self._observations = []

    def record(self, observation: RawObservation) -> None:
        self._observations.append(observation)

    @property
    def observations(self) -> Tuple[RawObservation, ...]:
        return tuple(self._observations)

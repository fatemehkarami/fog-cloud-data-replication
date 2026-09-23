"""Lightweight typed raw-result records for the common pilot/runner."""

from dataclasses import dataclass
from typing import Any, Optional, Tuple


MISSING_STATUSES = ("NOT_OBSERVED", "NOT_APPLICABLE", "UNRESOLVED", "FAILED_MEASUREMENT", "UNAVAILABLE")


@dataclass(frozen=True)
class EventRecord:
    event_id: str
    timestamp: float
    event_type: str
    sequence: int
    status: str = "VALID"
    payload: Tuple[Tuple[str, Any], ...] = ()


@dataclass(frozen=True)
class TransitionRecord:
    transition_id: str
    event_id: Optional[str]
    action: str
    status: str
    payload: Tuple[Tuple[str, Any], ...] = ()


@dataclass(frozen=True)
class RequestObservation:
    request_id: str
    sequence: Optional[int]
    arrival_time: float
    outcome: str
    completion_time: Optional[float] = None
    response_time: Optional[float] = None
    failure_reason: Optional[str] = None
    status: str = "VALID"


@dataclass(frozen=True)
class FailureObservation:
    failure_id: str
    failure_class: str
    target_id: str
    timestamp: float
    status: str = "VALID"


@dataclass(frozen=True)
class RecoveryObservation:
    recovery_id: str
    failure_id: str
    target_id: str
    timestamp: float
    status: str = "VALID"


@dataclass(frozen=True)
class ReplicaObservation:
    replica_id: str
    file_id: str
    node_id: str
    timestamp: float
    valid: bool
    active: bool
    status: str = "VALID"


@dataclass(frozen=True)
class TransferObservation:
    transfer_id: str
    purpose: str
    bytes_transferred: int
    timestamp: float
    status: str = "VALID"
    path: Tuple[str, ...] = ()


@dataclass(frozen=True)
class DecisionObservation:
    decision_id: str
    method_id: str
    duration_ms: Optional[float]
    status: str
    timestamp: float
    clock_type: str = "wall_clock"


@dataclass(frozen=True)
class MetricObservation:
    metric_id: str
    name: str
    value: Any
    unit: str
    status: str
    scope: str = "run"


@dataclass(frozen=True)
class RunSummaryRecord:
    run_id: str
    attempt_id: str
    status: str
    workload_id: str
    failure_id: str
    repetition_id: str
    method_id: str
    metrics: Tuple[Tuple[str, Any], ...]
    provenance: Tuple[Tuple[str, Any], ...]

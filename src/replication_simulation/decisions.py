"""Common decision envelopes and validation results."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, Tuple


class DecisionKind(str, Enum):
    PLACEMENT = "placement"
    PROVIDER_SELECTION = "provider_selection"
    REPLICA_CREATION = "replica_creation"
    REPLICA_DELETION = "replica_deletion"
    REPLICA_MOVEMENT = "replica_movement"
    REPLICA_COUNT = "replica_count"
    FAILURE_RESPONSE = "failure_response"
    NO_OP = "no_op"
    UNRESOLVED = "unresolved"


class DecisionStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INVALID = "invalid"
    UNSUPPORTED = "unsupported"
    UNRESOLVED = "unresolved"
    NO_OP = "no_op"


@dataclass(frozen=True)
class DecisionEnvelope:
    kind: DecisionKind
    status: DecisionStatus
    payload: Tuple[Tuple[str, Any], ...] = ()
    reason: Optional[str] = None
    provenance: Tuple[Tuple[str, Any], ...] = ()

    @classmethod
    def unresolved(cls, kind: DecisionKind, reason: str) -> "DecisionEnvelope":
        return cls(kind=kind, status=DecisionStatus.UNRESOLVED, reason=reason)

    @classmethod
    def no_op(cls, reason: Optional[str] = None) -> "DecisionEnvelope":
        return cls(kind=DecisionKind.NO_OP, status=DecisionStatus.ACCEPTED, reason=reason)


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    reason: Optional[str] = None
    errors: Tuple[str, ...] = ()

    @classmethod
    def ok(cls) -> "ValidationResult":
        return cls(valid=True)

    @classmethod
    def invalid(cls, *errors: str) -> "ValidationResult":
        return cls(valid=False, reason=errors[0] if errors else None, errors=tuple(errors))

"""Simulator-owned validation and execution boundary."""

from typing import Any, Callable, Dict, Optional

from .decisions import DecisionEnvelope, DecisionKind, DecisionStatus, ValidationResult
from .provenance import RawObservation, RawRecorder
from .state import SimulationState


class StateValidator:
    def validate(self, state: SimulationState, decision: DecisionEnvelope) -> ValidationResult:
        if decision.status is DecisionStatus.UNRESOLVED:
            return ValidationResult.invalid("decision is unresolved")
        payload: Dict[str, Any] = dict(decision.payload)
        file_id = payload.get("file_id")
        node_id = payload.get("node_id")
        if file_id is not None and file_id not in state.scenario.files:
            return ValidationResult.invalid("file reference is invalid")
        if node_id is not None:
            node = state.scenario.nodes.get(node_id)
            if node is None:
                return ValidationResult.invalid("node reference is invalid")
            if not node.healthy or not node.reachable:
                return ValidationResult.invalid("target node is unhealthy or unreachable")
        if decision.kind is DecisionKind.REPLICA_CREATION and file_id is not None and node_id is not None:
            if any(
                replica.file_id == file_id
                and replica.node_id == node_id
                and replica.valid
                for replica in state.scenario.replicas.values()
            ):
                return ValidationResult.invalid("duplicate replica placement")
            size = payload.get("size")
            node = state.scenario.nodes[node_id]
            if size is not None and node.available_storage is not None and size > node.available_storage:
                return ValidationResult.invalid("storage capacity exceeded")
        return ValidationResult.ok()


class ExecutionPipeline:
    """VALIDATE -> EXECUTE -> MUTATE -> RECORD.

    The mutation callback is simulator-owned and intentionally supplied by the
    caller; this foundation does not define algorithm-specific mutations.
    """

    def __init__(
        self,
        validator: Optional[StateValidator] = None,
        recorder: Optional[RawRecorder] = None,
    ) -> None:
        self.validator = validator or StateValidator()
        self.recorder = recorder or RawRecorder()

    def process(
        self,
        state: SimulationState,
        decision: DecisionEnvelope,
        mutate: Callable[[SimulationState, DecisionEnvelope], None],
    ) -> ValidationResult:
        validation = self.validator.validate(state, decision)
        self.recorder.record(
            RawObservation(
                observation_type="validation",
                timestamp=state.current_time,
                payload=(("valid", validation.valid), ("reason", validation.reason)),
            )
        )
        if not validation.valid:
            return validation
        state.apply_mutation(lambda current: mutate(current, decision))
        self.recorder.record(
            RawObservation(
                observation_type="execution",
                timestamp=state.current_time,
                payload=(("kind", decision.kind.value),),
            )
        )
        return validation

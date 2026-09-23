"""Generic simulator execution infrastructure.

This module owns orchestration and state mutation only. It contains no
method-specific scientific logic.
"""

from copy import deepcopy
import heapq
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Sequence, Tuple

from .adapters import AdapterSnapshot, SimulationAdapter
from .decisions import DecisionEnvelope, DecisionKind, DecisionStatus, ValidationResult
from .domain import Replica, Request, Scenario
from .events import Event, EventQueue, SimulationClock
from .pipeline import StateValidator
from .provenance import RawObservation, RawRecorder, RunMetadata
from .state import SimulationState

CANONICAL_METHODS = ("Proposed", "HRS", "DPRS", "OGSA", "EIMORM")


@dataclass(frozen=True)
class MethodRegistration:
    method_id: str
    adapter_factory: Callable[..., SimulationAdapter]
    capabilities: Tuple[DecisionKind, ...] = ()


class MethodRegistry:
    def __init__(self) -> None:
        self._registrations: Dict[str, MethodRegistration] = {}

    def register(self, registration: MethodRegistration) -> None:
        if registration.method_id not in CANONICAL_METHODS:
            raise ValueError("method is outside the canonical comparison roster")
        if registration.method_id in self._registrations:
            raise ValueError("method is already registered")
        self._registrations[registration.method_id] = registration

    def get(self, method_id: str) -> MethodRegistration:
        try:
            return self._registrations[method_id]
        except KeyError as error:
            raise KeyError("method is not registered") from error

    @property
    def method_ids(self) -> Tuple[str, ...]:
        return tuple(method_id for method_id in CANONICAL_METHODS if method_id in self._registrations)


@dataclass(frozen=True)
class ReplayTrace:
    events: Tuple[Event, ...] = ()
    scenario_id: Optional[str] = None
    seed_identity: Optional[str] = None
    random_stream_identity: Optional[str] = None


@dataclass(frozen=True)
class FrozenScenario:
    scenario: Scenario
    trace: ReplayTrace = ReplayTrace()
    metadata: Tuple[Tuple[str, Any], ...] = ()

    @classmethod
    def capture(
        cls,
        state: SimulationState,
        trace: ReplayTrace = ReplayTrace(),
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> "FrozenScenario":
        return cls(deepcopy(state.scenario), trace, tuple((metadata or {}).items()))

    def clone_state(self) -> SimulationState:
        return SimulationState(deepcopy(self.scenario))


@dataclass(frozen=True)
class PlacementTranslation:
    node_ids: Tuple[str, ...]
    source_payload: Tuple[Tuple[str, Any], ...]


class PlacementTranslator:
    """Translate explicit node/site placement payloads without choosing ambiguity."""

    def translate(self, state: SimulationState, decision: DecisionEnvelope) -> PlacementTranslation:
        payload = dict(decision.payload)
        node_ids = payload.get("placement_node_ids")
        if node_ids is not None:
            if not node_ids or any(node_id not in state.scenario.nodes for node_id in node_ids):
                raise ValueError("placement contains an invalid node")
            return PlacementTranslation(tuple(node_ids), decision.payload)
        node_id = payload.get("node_id")
        if node_id is not None:
            if node_id not in state.scenario.nodes:
                raise ValueError("placement contains an invalid node")
            return PlacementTranslation((node_id,), decision.payload)
        site_id = payload.get("site_id")
        if site_id is not None:
            matches = tuple(node.node_id for node in state.scenario.nodes.values() if node.site_id == site_id)
            if len(matches) != 1:
                raise ValueError("site placement requires an unambiguous node mapping")
            return PlacementTranslation(matches, decision.payload)
        raise ValueError("placement does not contain a node or site target")


@dataclass(frozen=True)
class ExecutionResult:
    status: DecisionStatus
    validation: ValidationResult
    reason: Optional[str] = None
    transition: Optional[Tuple[Tuple[str, Any], ...]] = None


@dataclass(frozen=True)
class RequestExecutionResult:
    request_id: str
    outcome: str
    arrival_time: float
    completion_time: Optional[float] = None
    response_time: Optional[float] = None
    serving_replica_id: Optional[str] = None
    path_node_ids: Tuple[str, ...] = ()
    bytes_transferred: Optional[int] = None
    reason: Optional[str] = None


class RequestServiceExecutor:
    """Deterministic common read-service execution for end-to-end runs."""

    def __init__(self, recorder: Optional[RawRecorder] = None, cache_enabled: bool = True) -> None:
        self.recorder = recorder or RawRecorder()
        self.cache_enabled = cache_enabled
        self._path_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
        self.cache_invalidations = 0

    def invalidate_paths(self) -> None:
        self.cache_invalidations += 1
        self._path_cache.clear()

    def _cached_path_valid(self, state: SimulationState, path: Tuple[str, ...]) -> bool:
        if not path:
            return False
        if any(not state.scenario.nodes.get(node_id, None) or not state.scenario.nodes[node_id].healthy or not state.scenario.nodes[node_id].reachable for node_id in path):
            return False
        for source, target in zip(path, path[1:]):
            if not any(link.source_node_id == source and link.target_node_id == target and link.available for link in state.scenario.network_links.values()):
                return False
        return True

    def _path(self, state: SimulationState, source: str, target: str) -> Tuple[float, Tuple[str, ...]]:
        cache_key = (source, target)
        if self.cache_enabled and cache_key in self._path_cache:
            cached = self._path_cache[cache_key]
            if self._cached_path_valid(state, cached[1]):
                self.cache_hits += 1
                return cached
            del self._path_cache[cache_key]
        self.cache_misses += 1
        if source == target:
            result = (0.0, (source,))
            if self.cache_enabled:
                self._path_cache[cache_key] = result
            return result
        adjacency = {}
        for link in state.scenario.network_links.values():
            if link.available and link.bandwidth is not None and link.latency is not None:
                adjacency.setdefault(link.source_node_id, []).append(link)
        distances = {node_id: float("inf") for node_id in state.scenario.nodes}
        paths = {source: (source,)}
        distances[source] = 0.0
        queue = [(0.0, source)]
        while queue:
            distance, node_id = heapq.heappop(queue)
            if distance != distances[node_id]:
                continue
            for link in sorted(adjacency.get(node_id, ()), key=lambda item: item.target_node_id):
                target_node = state.scenario.nodes.get(link.target_node_id)
                if target_node is None or not target_node.healthy or not target_node.reachable:
                    continue
                candidate = distance + link.latency
                if candidate < distances[link.target_node_id]:
                    distances[link.target_node_id] = candidate
                    paths[link.target_node_id] = paths[node_id] + (link.target_node_id,)
                    heapq.heappush(queue, (candidate, link.target_node_id))
        result = (distances.get(target, float("inf")), paths.get(target, ()))
        if self.cache_enabled:
            self._path_cache[cache_key] = result
        return result

    def serve(self, state: SimulationState, request: Request, metadata: Optional[RunMetadata] = None) -> RequestExecutionResult:
        source = request.source_node_id or next(iter(state.scenario.nodes), None)
        file = state.scenario.files.get(request.file_id)
        if source is None or source not in state.scenario.nodes or file is None or file.size is None:
            result = RequestExecutionResult(request.request_id, "FAILED", request.arrival_time, reason="request source or file is unavailable")
            self.recorder.record(RawObservation("request", request.arrival_time, (("request_id", request.request_id), ("outcome", result.outcome), ("reason", result.reason)), metadata))
            return result
        candidates = []
        for replica in state.scenario.replicas.values():
            node = state.scenario.nodes.get(replica.node_id)
            if replica.file_id != request.file_id or not replica.valid or node is None or not node.healthy or not node.reachable:
                continue
            latency, path = self._path(state, source, replica.node_id)
            if path:
                candidates.append((latency, path, replica))
        if not candidates:
            result = RequestExecutionResult(request.request_id, "FAILED", request.arrival_time, reason="no serviceable replica")
            self.recorder.record(RawObservation("request", request.arrival_time, (("request_id", request.request_id), ("outcome", result.outcome), ("reason", result.reason)), metadata))
            return result
        latency, path, replica = min(candidates, key=lambda item: (item[0], item[2].node_id, item[2].replica_id))
        transfer_seconds = (file.size * 1024 ** 3) / 1e9 if len(path) > 1 else 0.0
        completion = request.arrival_time + transfer_seconds
        result = RequestExecutionResult(request.request_id, "SUCCESS", request.arrival_time, completion, completion - request.arrival_time, replica.replica_id, path, int(file.size * 1024 ** 3))
        self.recorder.record(RawObservation("request", request.arrival_time, (("request_id", request.request_id), ("outcome", result.outcome), ("completion_time", completion), ("response_time", result.response_time), ("replica_id", replica.replica_id), ("path", path), ("bytes", result.bytes_transferred)), metadata))
        return result


class DecisionExecutor:
    """Runtime integration decision (not a change to source algorithm semantics):

    a successful PLACEMENT decision means "create an additional replica of the
    decision's file on each accepted placement target node", transferred from an
    existing valid source replica over the common network/path model. This
    closes the causal gap between an algorithm's placement decision and the
    authoritative simulation state consumed by RequestServiceExecutor.
    """

    def __init__(
        self,
        validator: Optional[StateValidator] = None,
        recorder: Optional[RawRecorder] = None,
        path_resolver: Optional["RequestServiceExecutor"] = None,
    ) -> None:
        self.validator = validator or StateValidator()
        self.recorder = recorder or RawRecorder()
        self.translator = PlacementTranslator()
        self.path_resolver = path_resolver or RequestServiceExecutor()

    def execute(self, state: SimulationState, decision: DecisionEnvelope, metadata: Optional[RunMetadata] = None) -> ExecutionResult:
        if decision.status is DecisionStatus.UNRESOLVED:
            return self._record_rejection(state, decision, "decision is unresolved", metadata)
        try:
            if decision.kind is DecisionKind.PLACEMENT:
                return self._placement(state, decision, metadata)
            if decision.kind is DecisionKind.REPLICA_CREATION:
                return self._create(state, decision, metadata)
            if decision.kind is DecisionKind.REPLICA_DELETION:
                return self._delete(state, decision, metadata)
            if decision.kind is DecisionKind.REPLICA_MOVEMENT:
                return self._move(state, decision, metadata)
            if decision.kind is DecisionKind.NO_OP:
                return self._record_success(state, decision, (("action", "no_op"),), metadata)
            return self._record_rejection(state, decision, "decision kind is unsupported by the common executor", metadata)
        except (ValueError, KeyError) as error:
            return self._record_rejection(state, decision, str(error), metadata)

    def _placement(self, state: SimulationState, decision: DecisionEnvelope, metadata: Optional[RunMetadata]) -> ExecutionResult:
        try:
            translation = self.translator.translate(state, decision)
        except ValueError as error:
            return self._record_rejection(state, decision, str(error), metadata)
        file_id = dict(decision.payload).get("file_id")
        if not file_id or file_id not in state.scenario.files:
            return self._record_rejection(state, decision, "file reference is invalid", metadata)
        file = state.scenario.files[file_id]
        if file.size is None:
            return self._record_rejection(state, decision, "replica size is unresolved", metadata)
        node_results = []
        any_accepted = False
        for node_id in translation.node_ids:
            node = state.scenario.nodes.get(node_id)
            if node is None:
                node_results.append((("node_id", node_id), ("status", "rejected"), ("reason", "node reference is invalid")))
                continue
            if not node.healthy or not node.reachable:
                node_results.append((("node_id", node_id), ("status", "rejected"), ("reason", "placement target is unhealthy or unreachable")))
                continue
            source = self._select_replication_source(state, file_id, node_id)
            if source is None:
                node_results.append((("node_id", node_id), ("status", "rejected"), ("reason", "no serviceable source replica available for replication transfer")))
                continue
            source_replica, path = source
            replica_id = f"placement-{file_id}-{node_id}"
            creation = DecisionEnvelope(
                kind=DecisionKind.REPLICA_CREATION,
                status=DecisionStatus.ACCEPTED,
                payload=(("replica_id", replica_id), ("file_id", file_id), ("node_id", node_id), ("size", file.size)),
                provenance=decision.provenance,
            )
            creation_result = self._create(state, creation, metadata)
            if creation_result.status is not DecisionStatus.ACCEPTED:
                node_results.append((("node_id", node_id), ("status", "rejected"), ("reason", creation_result.reason or "placement creation rejected")))
                continue
            bytes_transferred = int(file.size * 1024 ** 3)
            self.recorder.record(RawObservation(
                "transfer",
                state.current_time,
                (
                    ("purpose", "replication_movement"),
                    ("replica_id", replica_id),
                    ("source_replica_id", source_replica.replica_id),
                    ("bytes", bytes_transferred),
                    ("path", path),
                ),
                metadata,
            ))
            node_results.append((
                ("node_id", node_id), ("status", "accepted"), ("replica_id", replica_id),
                ("source_replica_id", source_replica.replica_id), ("bytes_transferred", bytes_transferred), ("path", path),
            ))
            any_accepted = True
        transition = (("action", "placement_executed"), ("file_id", file_id), ("placements", tuple(node_results)))
        if not any_accepted:
            self.recorder.record(RawObservation("validation", state.current_time, transition, metadata))
            return ExecutionResult(DecisionStatus.REJECTED, ValidationResult.invalid("no placement target was executable"), reason="no placement target was executable", transition=transition)
        self.recorder.record(RawObservation("execution", state.current_time, transition, metadata))
        return ExecutionResult(DecisionStatus.ACCEPTED, ValidationResult.ok(), transition=transition)

    def _select_replication_source(
        self, state: SimulationState, file_id: str, target_node_id: str,
    ) -> Optional[Tuple[Replica, Tuple[str, ...]]]:
        """Find the closest existing valid replica able to transfer to target_node_id."""
        candidates = []
        for replica in state.scenario.replicas.values():
            if replica.file_id != file_id or not replica.valid or replica.node_id == target_node_id:
                continue
            node = state.scenario.nodes.get(replica.node_id)
            if node is None or not node.healthy or not node.reachable:
                continue
            latency, path = self.path_resolver._path(state, replica.node_id, target_node_id)
            if path and len(path) > 1:
                candidates.append((latency, path, replica))
        if not candidates:
            return None
        latency, path, replica = min(candidates, key=lambda item: (item[0], item[2].node_id, item[2].replica_id))
        return replica, path

    def _create(self, state: SimulationState, decision: DecisionEnvelope, metadata: Optional[RunMetadata]) -> ExecutionResult:
        payload = dict(decision.payload)
        replica_id = payload.get("replica_id")
        file_id = payload.get("file_id")
        node_id = payload.get("node_id")
        if not replica_id or not file_id or not node_id:
            return self._record_rejection(state, decision, "replica creation requires replica, file, and node identifiers", metadata)
        validation = self.validator.validate(state, decision)
        if not validation.valid:
            return self._record_rejection(state, decision, validation.reason or "creation rejected", metadata)
        file = state.scenario.files[file_id]
        if file.size is None:
            return self._record_rejection(state, decision, "replica size is unresolved", metadata)
        before = state.scenario.nodes[node_id].storage_used
        replica = Replica(replica_id, file_id, node_id, True)
        state.apply_mutation(lambda current: self._apply_create(current, replica, file.size, node_id))
        transition = (("action", "replica_created"), ("replica_id", replica_id), ("storage_before", before), ("storage_after", state.scenario.nodes[node_id].storage_used))
        return self._record_success(state, decision, transition, metadata)

    @staticmethod
    def _apply_create(state: SimulationState, replica: Replica, size: float, node_id: str) -> None:
        state.scenario.replicas[replica.replica_id] = replica
        state.scenario.nodes[node_id].storage_used += size

    def _delete(self, state: SimulationState, decision: DecisionEnvelope, metadata: Optional[RunMetadata]) -> ExecutionResult:
        payload = dict(decision.payload)
        replica_id = payload.get("replica_id")
        replica = state.scenario.replicas.get(replica_id)
        if replica is None or not replica.valid:
            return self._record_rejection(state, decision, "replica is missing or invalid", metadata)
        valid_replicas = [item for item in state.scenario.replicas.values() if item.file_id == replica.file_id and item.valid]
        if len(valid_replicas) <= 1:
            return self._record_rejection(state, decision, "deletion would remove the last valid replica", metadata)
        file = state.scenario.files.get(replica.file_id)
        if file is None or file.size is None:
            return self._record_rejection(state, decision, "replica size is unresolved", metadata)
        state.apply_mutation(lambda current: self._apply_delete(current, replica_id, replica.node_id, file.size))
        return self._record_success(state, decision, (("action", "replica_deleted"), ("replica_id", replica_id)), metadata)

    @staticmethod
    def _apply_delete(state: SimulationState, replica_id: str, node_id: str, size: float) -> None:
        del state.scenario.replicas[replica_id]
        state.scenario.nodes[node_id].storage_used -= size

    def _move(self, state: SimulationState, decision: DecisionEnvelope, metadata: Optional[RunMetadata]) -> ExecutionResult:
        payload = dict(decision.payload)
        source_replica_id = payload.get("replica_id")
        target_node_id = payload.get("target_node_id")
        replica = state.scenario.replicas.get(source_replica_id)
        if replica is None or not target_node_id:
            return self._record_rejection(state, decision, "replica movement requires a replica and target node", metadata)
        if target_node_id not in state.scenario.nodes:
            return self._record_rejection(state, decision, "movement target node is invalid", metadata)
        file = state.scenario.files.get(replica.file_id)
        if file is None or file.size is None:
            return self._record_rejection(state, decision, "replica size is unresolved", metadata)
        if any(item.file_id == replica.file_id and item.node_id == target_node_id and item.valid for item in state.scenario.replicas.values()):
            return self._record_rejection(state, decision, "movement would create a duplicate replica", metadata)
        if not state.scenario.nodes[target_node_id].healthy or not state.scenario.nodes[target_node_id].reachable:
            return self._record_rejection(state, decision, "movement target is unhealthy or unreachable", metadata)
        available = state.scenario.nodes[target_node_id].available_storage
        if available is not None and available < file.size:
            return self._record_rejection(state, decision, "movement target lacks capacity", metadata)
        state.apply_mutation(lambda current: self._apply_move(current, replica, target_node_id, file.size))
        return self._record_success(state, decision, (("action", "replica_moved"), ("replica_id", source_replica_id), ("target_node_id", target_node_id)), metadata)

    @staticmethod
    def _apply_move(state: SimulationState, replica: Replica, target_node_id: str, size: float) -> None:
        state.scenario.nodes[replica.node_id].storage_used -= size
        state.scenario.nodes[target_node_id].storage_used += size
        replica.node_id = target_node_id

    def _record_success(self, state: SimulationState, decision: DecisionEnvelope, transition: Tuple[Tuple[str, Any], ...], metadata: Optional[RunMetadata]) -> ExecutionResult:
        self.recorder.record(RawObservation("execution", state.current_time, transition, metadata))
        return ExecutionResult(DecisionStatus.ACCEPTED, ValidationResult.ok(), transition=transition)

    def _record_rejection(self, state: SimulationState, decision: DecisionEnvelope, reason: str, metadata: Optional[RunMetadata]) -> ExecutionResult:
        transition = (("action", "rejected"), ("reason", reason), ("kind", decision.kind.value))
        self.recorder.record(RawObservation("validation", state.current_time, transition, metadata))
        return ExecutionResult(DecisionStatus.REJECTED, ValidationResult.invalid(reason), reason=reason, transition=transition)


@dataclass(frozen=True)
class DispatchResult:
    decision: DecisionEnvelope
    execution: Optional[ExecutionResult]


class AdapterDispatcher:
    def __init__(self, registry: MethodRegistry, executor: DecisionExecutor) -> None:
        self.registry = registry
        self.executor = executor

    def dispatch(self, method_id: str, state: SimulationState, adapter: SimulationAdapter, run_id: Optional[str] = None) -> DispatchResult:
        registration = self.registry.get(method_id)
        if adapter.method_id != registration.method_id:
            raise ValueError("adapter identity does not match registered method")
        snapshot = AdapterSnapshot.from_state(state, run_id=run_id)
        decision = adapter.compute(snapshot)
        execution = self.executor.execute(state, decision)
        return DispatchResult(decision, execution)


class SimulationEventLoop:
    def __init__(self, state: SimulationState, executor: DecisionExecutor) -> None:
        self.state = state
        self.clock = SimulationClock(state.current_time)
        self.queue = EventQueue()
        self.executor = executor
        self.handlers: Dict[str, Callable[[Event], None]] = {}

    def register_handler(self, event_type: str, handler: Callable[[Event], None]) -> None:
        self.handlers[event_type] = handler

    def schedule(self, event: Event) -> Event:
        return self.queue.schedule(event)

    def run(self, horizon: Optional[float] = None) -> int:
        processed = 0
        while len(self.queue):
            event = self.queue.pop()
            if event is None or (horizon is not None and event.timestamp > horizon):
                break
            self.clock.advance_to(event.timestamp)
            self.state.current_time = event.timestamp
            handler = self.handlers.get(event.event_type)
            if handler is None:
                raise ValueError("event has no registered handler")
            handler(event)
            processed += 1
        return processed


class FailureRecoveryExecutor:
    """Apply only externally supplied node failure/recovery state changes."""

    def __init__(self, recorder: Optional[RawRecorder] = None) -> None:
        self.recorder = recorder or RawRecorder()

    def fail_node(self, state: SimulationState, node_id: str, metadata: Optional[RunMetadata] = None) -> ExecutionResult:
        node = state.scenario.nodes.get(node_id)
        if node is None:
            result = ExecutionResult(DecisionStatus.INVALID, ValidationResult.invalid("node reference is invalid"), reason="node reference is invalid")
            self.recorder.record(RawObservation("failure", state.current_time, (("node_id", node_id), ("status", "invalid")), metadata))
            return result
        def fail(current: SimulationState) -> None:
            current.scenario.nodes[node_id].healthy = False
            current.scenario.nodes[node_id].reachable = False
            for link in current.scenario.network_links.values():
                if link.source_node_id == node_id or link.target_node_id == node_id:
                    link.available = False
        state.apply_mutation(fail)
        transition = (("action", "node_failure"), ("node_id", node_id))
        self.recorder.record(RawObservation("failure", state.current_time, transition, metadata))
        return ExecutionResult(DecisionStatus.ACCEPTED, ValidationResult.ok(), transition=transition)

    def recover_node(self, state: SimulationState, node_id: str, metadata: Optional[RunMetadata] = None) -> ExecutionResult:
        node = state.scenario.nodes.get(node_id)
        if node is None:
            result = ExecutionResult(DecisionStatus.INVALID, ValidationResult.invalid("node reference is invalid"), reason="node reference is invalid")
            self.recorder.record(RawObservation("recovery", state.current_time, (("node_id", node_id), ("status", "invalid")), metadata))
            return result
        def recover(current: SimulationState) -> None:
            current.scenario.nodes[node_id].healthy = True
            current.scenario.nodes[node_id].reachable = True
            for link in current.scenario.network_links.values():
                if link.source_node_id == node_id or link.target_node_id == node_id:
                    link.available = True
        state.apply_mutation(recover)
        transition = (("action", "node_recovery"), ("node_id", node_id))
        self.recorder.record(RawObservation("recovery", state.current_time, transition, metadata))
        return ExecutionResult(DecisionStatus.ACCEPTED, ValidationResult.ok(), transition=transition)

    def fail_link(self, state: SimulationState, link_id: str, metadata: Optional[RunMetadata] = None) -> ExecutionResult:
        link = state.scenario.network_links.get(link_id)
        if link is None:
            return ExecutionResult(DecisionStatus.INVALID, ValidationResult.invalid("link reference is invalid"), reason="link reference is invalid")
        state.apply_mutation(lambda current: setattr(current.scenario.network_links[link_id], "available", False))
        transition = (("action", "link_failure"), ("link_id", link_id))
        self.recorder.record(RawObservation("failure", state.current_time, transition, metadata))
        return ExecutionResult(DecisionStatus.ACCEPTED, ValidationResult.ok(), transition=transition)

    def recover_link(self, state: SimulationState, link_id: str, metadata: Optional[RunMetadata] = None) -> ExecutionResult:
        link = state.scenario.network_links.get(link_id)
        if link is None:
            return ExecutionResult(DecisionStatus.INVALID, ValidationResult.invalid("link reference is invalid"), reason="link reference is invalid")
        state.apply_mutation(lambda current: setattr(current.scenario.network_links[link_id], "available", True))
        transition = (("action", "link_recovery"), ("link_id", link_id))
        self.recorder.record(RawObservation("recovery", state.current_time, transition, metadata))
        return ExecutionResult(DecisionStatus.ACCEPTED, ValidationResult.ok(), transition=transition)


@dataclass(frozen=True)
class PreparedRun:
    method_id: str
    state: SimulationState
    metadata: RunMetadata


class MatchedRunOrchestrator:
    def prepare_runs(self, frozen: FrozenScenario, registry: MethodRegistry, metadata_factory: Callable[[str], RunMetadata]) -> Tuple[PreparedRun, ...]:
        return tuple(
            PreparedRun(method_id, frozen.clone_state(), metadata_factory(method_id))
            for method_id in registry.method_ids
        )

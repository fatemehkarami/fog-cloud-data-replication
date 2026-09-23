"""Configurable frozen-matrix runner with a small default pilot.

The runner is intentionally straightforward: common artifacts are built once
per repetition, cloned per method, and method decisions are executed through
the common executor. Full-matrix mode is explicit and is not run by default.
"""

from dataclasses import dataclass
import hashlib
import json
from time import perf_counter
from random import Random
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple

from .domain import File, NetworkLink, Node, Replica, Request, Scenario, Site, User
from .events import Event, EventQueue
from .provenance import RawObservation, RawRecorder, RunMetadata
from .runtime import (
    AdapterDispatcher, DecisionExecutor, FailureRecoveryExecutor, FrozenScenario,
    MethodRegistration, MethodRegistry, ReplayTrace, RequestExecutionResult,
    RequestServiceExecutor,
)
from .state import SimulationState
from .result_records import (
    DecisionObservation, EventRecord, FailureObservation, MetricObservation,
    RecoveryObservation, ReplicaObservation, RequestObservation, RunSummaryRecord,
    TransferObservation, TransitionRecord,
)
from .pilot import _adapter as _pilot_adapter
from .proposed import OisInput, OisWeights, ProposedAdapter, ProposedRequest
from .hrs import HRSAdapter, HrsRequest, HrsSite, HrsWeights
from .dprs import DPRSAdapter, DprsConnection, DprsDataset, DprsNodeTiming, DprsRequest
from .eimorm import EIMORMAdapter, EimormContext, EimormRequest
from .ogsa import OGSAAdapter, OgsaAssignment, OgsaConfig, OgsaObjectiveContext, OgsaRequest, OgsaWeights

METHODS = ("Proposed", "HRS", "DPRS", "OGSA", "EIMORM")
WORKLOADS = ("W01", "W02", "W03")
FAILURES = ("F0", "F1", "F2", "F3", "F4")


@dataclass(frozen=True)
class RunnerConfig:
    master_seed: str = "phase17-master-seed"
    configuration_id: str = "cmp-rd-002-common-env-v1"
    experiment_id: str = "phase17-frozen-experiment-v1"
    pilot: bool = True
    request_limit: Optional[int] = 12
    request_sequences: Optional[Tuple[int, ...]] = None
    progress: bool = False
    path_cache_enabled: bool = True

    @property
    def workloads(self) -> Tuple[str, ...]:
        return ("W01",) if self.pilot else WORKLOADS

    @property
    def failures(self) -> Tuple[str, ...]:
        return ("F0",) if self.pilot else FAILURES

    @property
    def repetitions(self) -> Tuple[str, ...]:
        return ("rep-01", "rep-02") if self.pilot else tuple(f"rep-{index:02d}" for index in range(1, 31))

    @property
    def effective_request_limit(self) -> int:
        if not self.pilot:
            return 1200
        return self.request_limit if self.request_limit is not None else 1200


@dataclass(frozen=True)
class RunSummary:
    experiment_id: str
    configuration_id: str
    scenario_id: str
    workload_id: str
    failure_scenario_id: str
    repetition_id: str
    method_id: str
    run_id: str
    attempt_id: str
    status: str
    requests_total: int
    requests_successful: int
    requests_failed: int
    decisions: int
    observations: int
    provenance: Tuple[Tuple[str, object], ...]
    response_time_mean: Optional[float] = None
    reliability: Optional[float] = None
    service_availability: Optional[float] = None
    active_replica_count: Optional[int] = None
    network_transfer_volume: Optional[int] = None
    algorithm_decision_time: Optional[float] = None
    replication_transfer_volume: Optional[int] = None
    records: Tuple[object, ...] = ()


class AvailabilityLedger:
    """Event-sampled availability ledger over the fixed admission interval."""

    def __init__(self, state: SimulationState, end_time: float = 7200.0) -> None:
        self.state = state
        self.end_time = end_time
        self._last_time: Dict[Tuple[str, str], float] = {}
        self._available_seconds: Dict[Tuple[str, str], float] = {}
        self._serviceable: Dict[Tuple[str, str], bool] = {}

    def register(self, file_id: str, source_node_id: str) -> None:
        key = (file_id, source_node_id)
        self._last_time.setdefault(key, 0.0)
        self._available_seconds.setdefault(key, 0.0)
        self._serviceable.setdefault(key, False)

    def _is_serviceable(self, file_id: str, source_node_id: str) -> bool:
        from .runtime import RequestServiceExecutor
        for replica in self.state.scenario.replicas.values():
            if replica.file_id != file_id or not replica.valid:
                continue
            node = self.state.scenario.nodes.get(replica.node_id)
            if node is None or not node.healthy or not node.reachable:
                continue
            latency, path = RequestServiceExecutor()._path(self.state, source_node_id, replica.node_id)
            if path:
                return True
        return False

    def advance(self, timestamp: float) -> None:
        timestamp = min(self.end_time, max(0.0, timestamp))
        for key in tuple(self._last_time):
            if self._serviceable.get(key, False):
                self._available_seconds[key] += max(0.0, timestamp - self._last_time[key])
            self._last_time[key] = timestamp
            self._serviceable[key] = self._is_serviceable(*key)

    def observe(self, file_id: str, timestamp: float, serviceable: bool) -> None:
        self.register(file_id, next(iter(self.state.scenario.nodes)))
        self.advance(timestamp)

    def finalize(self, file_id: str) -> float:
        self.advance(self.end_time)
        values = [value / self.end_time for (tracked_file, _), value in self._available_seconds.items() if tracked_file == file_id]
        return sum(values) / len(values) if values else 0.0


@dataclass(frozen=True)
class FrozenArtifacts:
    state: SimulationState
    requests: Tuple[Request, ...]
    failure_events: Tuple[Event, ...]
    scenario_id: str
    workload_id: str
    failure_id: str
    scenario_digest: str
    workload_digest: str
    failure_digest: str


def _digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(encoded).hexdigest()


def derive_seed(master: str, *parts: str) -> int:
    return int(_digest((master,) + parts)[:16], 16)


def build_frozen_state(scenario_id: str, seed: int) -> SimulationState:
    sites = {f"site-{index:02d}": Site(f"site-{index:02d}", tuple(f"site-{index:02d}-{role}" for role in ("edge", "data", "cloud"))) for index in range(1, 5)}
    nodes: Dict[str, Node] = {}
    for site_id, site in sites.items():
        for role, capacity in (("edge", 80.0), ("data", 160.0), ("cloud", 320.0)):
            nodes[f"{site_id}-{role}"] = Node(f"{site_id}-{role}", site_id, storage_capacity=capacity)
    links: Dict[str, NetworkLink] = {}
    link_number = 1
    for site_id in sites:
        edge, data, cloud = (f"{site_id}-{role}" for role in ("edge", "data", "cloud"))
        for source, target in ((edge, data), (data, edge), (cloud, data), (data, cloud)):
            links[f"link-{link_number:03d}"] = NetworkLink(f"link-{link_number:03d}", source, target, 10.0, 1.0)
            link_number += 1
    gateways = [f"site-{index:02d}-data" for index in range(1, 5)]
    for source in gateways:
        for target in gateways:
            if source != target:
                links[f"link-{link_number:03d}"] = NetworkLink(f"link-{link_number:03d}", source, target, 2.5, 20.0)
                link_number += 1
    files = {}
    replicas = {}
    rng = Random(seed)
    for index in range(1, 101):
        size = 1.0 if index <= 17 else 2.0 if index <= 34 else 3.0 if index <= 45 else 4.0 if index <= 56 else 5.0 if index <= 67 else 6.0 if index <= 78 else 7.0 if index <= 89 else 8.0
        file_id = f"file-{index:03d}"
        files[file_id] = File(file_id, size)
        site_id = f"site-{rng.randrange(1, 5):02d}"
        replicas[f"primary-{index:03d}"] = Replica(f"primary-{index:03d}", file_id, f"{site_id}-data", True)
    state = SimulationState(Scenario(scenario_id, sites, nodes, files=files, replicas=replicas, users={f"client-{index:02d}": User(f"client-{index:02d}", f"site-{((index - 1) // 4) + 1:02d}") for index in range(1, 17)}, network_links=links))
    for replica in state.scenario.replicas.values():
        state.scenario.nodes[replica.node_id].storage_used += state.scenario.files[replica.file_id].size or 0.0
    return state


def build_workload(workload_id: str, file_ids: Tuple[str, ...]) -> Tuple[Request, ...]:
    requests: List[Request] = []
    for sequence in range(1, 1201):
        if workload_id == "W01":
            file_id = file_ids[(sequence - 1) % len(file_ids)]
        else:
            cohort = (sequence - 1) % 10
            if workload_id == "W03" and sequence > 600:
                active = file_ids[20:40]
            else:
                active = file_ids[:20]
            if cohort < 6:
                file_id = active[(sequence - 1) % len(active)]
            elif cohort < 9:
                file_id = file_ids[40 + ((sequence - 1) % 30)]
            else:
                file_id = file_ids[70 + ((sequence - 1) % 30)]
        client_index = ((sequence - 1) % 16) + 1
        site_index = ((sequence - 1) % 4) + 1
        requests.append(Request(f"request-{sequence:06d}", f"client-{client_index:02d}", file_id, sequence * 6.0, sequence=sequence, operation="read", source_site_id=f"site-{site_index:02d}", source_node_id=f"site-{site_index:02d}-edge"))
    return tuple(requests)


def build_failures(failure_id: str, state: SimulationState, seed: int) -> Tuple[Event, ...]:
    if failure_id == "F0":
        return ()
    rng = Random(seed)
    if failure_id in ("F1", "F4"):
        nodes = sorted(state.scenario.nodes)
        target = nodes[rng.randrange(len(nodes))]
        start, end = (1800.0, 2400.0) if failure_id == "F1" else (5400.0, None)
        events = [Event(start, "node_failure", payload=target, priority=0)]
        if end is not None:
            events.append(Event(end, "node_recovery", payload=target, priority=0))
        return tuple(events)
    if failure_id == "F2":
        site_id = sorted(state.scenario.sites)[rng.randrange(len(state.scenario.sites))]
        return tuple(Event(timestamp, event_type, payload=node_id, priority=0) for timestamp, event_type in ((3600.0, "node_failure"), (4500.0, "node_recovery")) for node_id in state.scenario.sites[site_id].node_ids)
    pairs = [(source, target) for source in sorted(state.scenario.nodes) if source.endswith("-data") for target in sorted(state.scenario.nodes) if target.endswith("-data") and source < target]
    source, target = pairs[rng.randrange(len(pairs))]
    link_ids = tuple(sorted(link_id for link_id, link in state.scenario.network_links.items() if {link.source_node_id, link.target_node_id} == {source, target}))
    return tuple(Event(timestamp, event_type, payload=link_id, priority=0) for timestamp, event_type in ((4800.0, "link_failure"), (5400.0, "link_recovery")) for link_id in link_ids)


def build_artifacts(config: RunnerConfig, workload_id: str, failure_id: str, repetition_id: str) -> FrozenArtifacts:
    scenario_seed = derive_seed(config.master_seed, "scenario", config.experiment_id, config.configuration_id, repetition_id)
    state = build_frozen_state(f"scenario-{repetition_id}", scenario_seed)
    file_ids = tuple(sorted(state.scenario.files))
    requests = build_workload(workload_id, file_ids)
    failures = build_failures(failure_id, state, derive_seed(config.master_seed, "failure", failure_id, repetition_id))
    return FrozenArtifacts(state, requests, failures, state.scenario.scenario_id, workload_id, failure_id, _digest(state.scenario.metadata), _digest([request.__dict__ for request in requests]), _digest([event.__dict__ for event in failures]))


def _adapter(method_id: str, state: SimulationState, request: Request):
    file_id = request.file_id
    if method_id == "Proposed":
        return ProposedAdapter(ProposedRequest(file_id, OisInput(((request.arrival_time, 1.0),), request.arrival_time, 0.0001, state.scenario.files[file_id].size, 1.0, 1.0, 1.0, 1.0, OisWeights()), 2.0, 1.0, sum(replica.file_id == file_id and replica.valid for replica in state.scenario.replicas.values())))
    if method_id == "HRS":
        sites = tuple(HrsSite(site_id, normalized_accesses=1.0 if site_id == request.source_site_id else 0.5, normalized_centrality=1.0 if site_id == request.source_site_id else 0.5) for site_id in sorted(state.scenario.sites))
        return HRSAdapter(HrsRequest(file_id, sites, weights=HrsWeights()))
    if method_id == "DPRS":
        timings = tuple(DprsNodeTiming(node_id, 0.5, 1.0, 10.0) for node_id in state.scenario.nodes)
        connections = tuple(DprsConnection(link.source_node_id, link.target_node_id, link.bandwidth or 1.0, 1.0) for link in state.scenario.network_links.values())
        return DPRSAdapter(DprsRequest(DprsDataset(file_id, state.scenario.files[file_id].size or 0.0), timings, connections, 1.0, 1.0))
    node_count = len(state.scenario.nodes)
    if method_id == "OGSA":
        assignment = OgsaAssignment((tuple([1] + [0] * (node_count - 1)),), (state.scenario.files[file_id].size or 1.0,), (100.0,) * node_count)
        context = OgsaObjectiveContext((0.1,), (tuple([1.0] * node_count),), (tuple([1.0] + [0.0] * (node_count - 1)),), (1.0,) * node_count, (tuple([1.0] + [0.0] * (node_count - 1)),), (10.0,) * node_count, (2.0,) * node_count, 2.0, (1.0,))
        return OGSAAdapter(OgsaRequest(assignment, context, OgsaWeights.source_reported_equal(), OgsaConfig(population_size=4, generations=1), file_id=file_id))
    if method_id == "EIMORM":
        return EIMORMAdapter(EimormRequest(EimormContext(file_id, request.arrival_time, 0.0, 1, 1.0, 1.0, 12.0, 10.0)))
    raise ValueError("unknown runner method")


def run_pilot_matrix(
    config: Optional[RunnerConfig] = None,
    completed_run_ids: Optional[Set[str]] = None,
    on_complete: Optional[Callable[[RunSummary], None]] = None,
) -> Tuple[RunSummary, ...]:
    config = config or RunnerConfig()
    completed_run_ids = completed_run_ids or set()
    summaries = []
    completed_attempts = 0
    expected_attempts = len(config.workloads) * len(config.failures) * len(config.repetitions) * len(METHODS)
    for workload_id in config.workloads:
        for failure_id in config.failures:
            for repetition_id in config.repetitions:
                artifacts = build_artifacts(config, workload_id, failure_id, repetition_id)
                for method_id in METHODS:
                    run_id = f"{method_id}-{workload_id}-{failure_id}-{repetition_id}"
                    if run_id in completed_run_ids:
                        continue
                    state = artifacts.state.clone()
                    recorder = RawRecorder()
                    metadata = RunMetadata(config.experiment_id, config.configuration_id, run_id, method_id, seed_identity=config.master_seed, configuration_identity=config.configuration_id)
                    service_executor = RequestServiceExecutor(recorder, cache_enabled=config.path_cache_enabled)
                    executor = DecisionExecutor(recorder=recorder, path_resolver=service_executor)
                    dispatcher = AdapterDispatcher(_registry(method_id), executor)
                    decisions = 0
                    try:
                        failure_executor = FailureRecoveryExecutor(recorder=recorder)
                        event_records = []
                        transition_records = []
                        request_records = []
                        failure_records = []
                        recovery_records = []
                        replica_records = []
                        transfer_records = []
                        decision_records = []
                        metric_records = []
                        availability = AvailabilityLedger(state)
                        admitted_event_count = min(config.effective_request_limit, len(artifacts.requests)) + len(artifacts.failure_events)
                        drain_budget = 100 * (admitted_event_count + 1)
                        drain_event_count = 0
                        failures_applied = set()
                        response_times = []
                        transfer_volume = 0
                        replication_transfer_volume = 0
                        success_count = 0
                        requests_processed = 0
                        requests_successful = 0
                        requests_failed = 0
                        selected_requests = artifacts.requests
                        if config.request_sequences is not None:
                            selected_requests = tuple(artifacts.requests[index - 1] for index in config.request_sequences)
                        else:
                            selected_requests = artifacts.requests[:config.effective_request_limit]
                        availability_keys = set()
                        for request in selected_requests:
                            availability_keys.add((request.file_id, request.source_node_id or next(iter(state.scenario.nodes))))
                            availability.register(request.file_id, request.source_node_id or next(iter(state.scenario.nodes)))
                        queue = EventQueue()
                        for failure_event in artifacts.failure_events:
                            queue.schedule(failure_event)
                        for request in selected_requests:
                            queue.schedule(Event(request.arrival_time, "request_arrival", payload=request, priority=1))
                        baseline_event_count = len(selected_requests) + len(artifacts.failure_events)
                        drain_budget = 100 * (baseline_event_count + 1)
                        while len(queue):
                            event = queue.pop()
                            if event is None:
                                break
                            state.current_time = event.timestamp
                            availability.advance(event.timestamp)
                            if event.event_type == "node_failure":
                                event_records.append(EventRecord(f"event-{event.sequence:06d}", event.timestamp, event.event_type, event.sequence, payload=(("target_id", event.payload),)))
                                failure_executor.fail_node(state, event.payload, metadata)
                                service_executor.invalidate_paths()
                                failure_records.append(FailureObservation(event.event_type, failure_id, event.payload, event.timestamp))
                                continue
                            if event.event_type == "node_recovery":
                                event_records.append(EventRecord(f"event-{event.sequence:06d}", event.timestamp, event.event_type, event.sequence, payload=(("target_id", event.payload),)))
                                failure_executor.recover_node(state, event.payload, metadata)
                                service_executor.invalidate_paths()
                                recovery_records.append(RecoveryObservation(event.event_type, failure_id, event.payload, event.timestamp))
                                continue
                            if event.event_type == "link_failure":
                                event_records.append(EventRecord(f"event-{event.sequence:06d}", event.timestamp, event.event_type, event.sequence, payload=(("target_id", event.payload),)))
                                failure_executor.fail_link(state, event.payload, metadata)
                                service_executor.invalidate_paths()
                                failure_records.append(FailureObservation(event.event_type, failure_id, event.payload, event.timestamp))
                                continue
                            if event.event_type == "link_recovery":
                                event_records.append(EventRecord(f"event-{event.sequence:06d}", event.timestamp, event.event_type, event.sequence, payload=(("target_id", event.payload),)))
                                failure_executor.recover_link(state, event.payload, metadata)
                                service_executor.invalidate_paths()
                                recovery_records.append(RecoveryObservation(event.event_type, failure_id, event.payload, event.timestamp))
                                continue
                            request = event.payload
                            event_records.append(EventRecord(request.request_id, request.arrival_time, "request_arrival", request.sequence or 0, payload=(("file_id", request.file_id),)))
                            availability.advance(request.arrival_time)
                            adapter = _adapter(method_id, state, request)
                            decision_start = perf_counter()
                            dispatch = dispatcher.dispatch(method_id, state, adapter, metadata.run_id)
                            decision_ms = (perf_counter() - decision_start) * 1000.0
                            decision_records.append(DecisionObservation(f"decision-{request.request_id}", method_id, decision_ms, dispatch.decision.status.value, request.arrival_time))
                            if dispatch.execution is not None:
                                transition = dispatch.execution.transition or ()
                                transition_records.append(TransitionRecord(f"transition-{request.request_id}", request.request_id, dict(transition).get("action", "none"), dispatch.execution.status.value, transition))
                                if dict(transition).get("action") == "placement_executed":
                                    for node_result in dict(transition).get("placements", ()):
                                        node_result_map = dict(node_result)
                                        if node_result_map.get("status") == "accepted":
                                            replication_bytes = node_result_map.get("bytes_transferred") or 0
                                            replication_transfer_volume += replication_bytes
                                            transfer_records.append(TransferObservation(
                                                f"replication-{request.request_id}-{node_result_map.get('replica_id')}",
                                                "replication_movement",
                                                replication_bytes,
                                                request.arrival_time,
                                                path=node_result_map.get("path", ()),
                                            ))
                            request_result = service_executor.serve(state, request, metadata)
                            requests_processed += 1
                            requests_successful += int(request_result.outcome == "SUCCESS")
                            requests_failed += int(request_result.outcome != "SUCCESS")
                            success_count += int(request_result.outcome == "SUCCESS")
                            if request_result.response_time is not None:
                                response_times.append(request_result.response_time)
                            transfer_volume += request_result.bytes_transferred or 0
                            request_records.append(RequestObservation(request.request_id, request.sequence, request.arrival_time, request_result.outcome, request_result.completion_time, request_result.response_time, request_result.reason))
                            if request_result.bytes_transferred:
                                transfer_records.append(TransferObservation(f"transfer-{request.request_id}", "request_service", request_result.bytes_transferred, request_result.completion_time or request.arrival_time, path=request_result.path_node_ids))
                            for replica in state.scenario.replicas.values():
                                if replica.file_id == request.file_id:
                                    node = state.scenario.nodes.get(replica.node_id)
                                    replica_records.append(ReplicaObservation(replica.replica_id, replica.file_id, replica.node_id, request.arrival_time, replica.valid, bool(node and node.healthy and node.reachable)))
                            availability.observe(request.file_id, request.arrival_time, request_result.outcome == "SUCCESS")
                            decisions += 1
                        # The current runner emits no deferred method events; keep the
                        # fixed CMP-RD-006 budget explicit for future causal events.
                        if drain_event_count > drain_budget:
                            raise TimeoutError("causal drain budget exceeded")
                        availability_value = sum(availability.finalize(file_id) for file_id, _ in availability_keys) / len(availability_keys) if availability_keys else 0.0
                        metric_records.extend((MetricObservation("reliability", "request_reliability", success_count / requests_processed if requests_processed else None, "proportion", "VALID" if requests_processed else "NOT_OBSERVED"), MetricObservation("availability", "service_availability", availability_value, "proportion", "VALID")))
                        records = tuple(event_records + transition_records + request_records + failure_records + recovery_records + replica_records + transfer_records + decision_records + metric_records)
                        summary = RunSummary(config.experiment_id, config.configuration_id, artifacts.scenario_id, workload_id, failure_id, repetition_id, method_id, metadata.run_id, f"attempt-{metadata.run_id}", "VALID", requests_processed, requests_successful, requests_failed, decisions, len(recorder.observations), (("scenario_digest", artifacts.scenario_digest), ("workload_digest", artifacts.workload_digest), ("failure_digest", artifacts.failure_digest), ("master_seed_identity", config.master_seed), ("scenario_seed_identity", str(derive_seed(config.master_seed, "scenario", artifacts.scenario_id, repetition_id))), ("workload_seed_identity", str(derive_seed(config.master_seed, "workload", workload_id, repetition_id))), ("failure_seed_identity", str(derive_seed(config.master_seed, "failure", failure_id, repetition_id))), ("method_seed_identity", str(derive_seed(config.master_seed, "method", method_id, repetition_id))), ("admitted_event_count", admitted_event_count), ("drain_budget", drain_budget), ("drain_event_count", drain_event_count), ("path_cache_hits", service_executor.cache_hits), ("path_cache_misses", service_executor.cache_misses), ("path_cache_invalidations", service_executor.cache_invalidations)), sum(response_times) / len(response_times) if response_times else None, success_count / requests_processed if requests_processed else None, availability_value, sum(replica.valid for replica in state.scenario.replicas.values()), transfer_volume, sum(item.duration_ms or 0.0 for item in decision_records), replication_transfer_volume=replication_transfer_volume, records=records)
                        summaries.append(summary)
                        if on_complete is not None:
                            on_complete(summary)
                        completed_attempts += 1
                        if config.progress:
                            print(f"completed {completed_attempts} / {expected_attempts}", flush=True)
                    except Exception as error:
                        summary = RunSummary(
                            config.experiment_id, config.configuration_id, artifacts.scenario_id,
                            workload_id, failure_id, repetition_id, method_id, metadata.run_id,
                            f"attempt-{metadata.run_id}", "FAILED",
                            requests_processed if 'requests_processed' in locals() else 0, 0, 0,
                            decisions, len(recorder.observations),
                            (("error", type(error).__name__), ("message", str(error))),
                        )
                        summaries.append(summary)
                        if on_complete is not None:
                            on_complete(summary)
                        completed_attempts += 1
                        if config.progress:
                            print(f"completed {completed_attempts} / {expected_attempts}", flush=True)
    return tuple(summaries)


def run_integration_pilot(workload_id: str, failure_id: str, request_limit: int = 12, request_sequences: Optional[Tuple[int, ...]] = None, path_cache_enabled: bool = True) -> Tuple[RunSummary, ...]:
    """Execute one small all-method integration cell without final-matrix scale."""
    config = RunnerConfig(pilot=True, request_limit=request_limit)
    config = RunnerConfig(
        master_seed=config.master_seed,
        configuration_id=config.configuration_id,
        experiment_id=config.experiment_id,
        pilot=True,
        request_limit=request_limit,
        request_sequences=request_sequences,
        path_cache_enabled=path_cache_enabled,
    )
    original_workloads, original_failures = config.workloads, config.failures
    # Keep the runner's core path unchanged while selecting one explicit pilot cell.
    class PilotCellConfig(RunnerConfig):
        @property
        def workloads(self):
            return (workload_id,)

        @property
        def failures(self):
            return (failure_id,)

        @property
        def repetitions(self):
            return ("rep-01",)

    return run_pilot_matrix(PilotCellConfig(master_seed=config.master_seed, configuration_id=config.configuration_id, experiment_id=config.experiment_id, pilot=True, request_limit=request_limit))


def _registry(method_id: str) -> MethodRegistry:
    registry = MethodRegistry()
    registry.register(MethodRegistration(method_id, lambda: None))
    return registry

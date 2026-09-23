"""Small deterministic end-to-end pilot harness.

This is common execution scaffolding only. It is intentionally separate from
scientific method implementations and is not the final experiment runner.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Tuple

from .domain import File, NetworkLink, Node, Replica, Request, Scenario, Site, User
from .eimorm import EimormContext, EimormRequest
from .events import Event
from .hrs import HrsRequest, HrsSite, HrsWeights
from .ogsa import OgsaAssignment, OgsaConfig, OgsaObjectiveContext, OgsaRequest, OgsaWeights
from .proposed import OisInput, OisWeights, ProposedRequest
from .dprs import DprsConnection, DprsDataset, DprsNodeTiming, DprsRequest
from .provenance import RawObservation, RawRecorder, RunMetadata
from .runtime import AdapterDispatcher, DecisionExecutor, FrozenScenario, MethodRegistration, MethodRegistry, ReplayTrace
from .state import SimulationState
from .adapters import SimulationAdapter


@dataclass(frozen=True)
class PilotArtifacts:
    workload_id: str
    requests: Tuple[Request, ...]
    failure_events: Tuple[Event, ...]
    digest: str


@dataclass(frozen=True)
class PilotRun:
    method_id: str
    run_id: str
    status: str
    requests_completed: int
    requests_failed: int
    decisions: int
    transitions: int
    observations: Tuple[RawObservation, ...]


def build_pilot_scenario() -> SimulationState:
    sites = {
        "site-01": Site("site-01", ("site-01-edge", "site-01-data")),
        "site-02": Site("site-02", ("site-02-edge", "site-02-data")),
    }
    nodes = {
        "site-01-edge": Node("site-01-edge", "site-01", storage_capacity=100.0),
        "site-01-data": Node("site-01-data", "site-01", storage_capacity=100.0),
        "site-02-edge": Node("site-02-edge", "site-02", storage_capacity=100.0),
        "site-02-data": Node("site-02-data", "site-02", storage_capacity=100.0),
    }
    links = {
        "link-01": NetworkLink("link-01", "site-01-edge", "site-01-data", 10.0, 1.0),
        "link-02": NetworkLink("link-02", "site-01-data", "site-01-edge", 10.0, 1.0),
        "link-03": NetworkLink("link-03", "site-02-edge", "site-02-data", 10.0, 1.0),
        "link-04": NetworkLink("link-04", "site-02-data", "site-02-edge", 10.0, 1.0),
        "link-05": NetworkLink("link-05", "site-01-data", "site-02-data", 2.5, 20.0),
        "link-06": NetworkLink("link-06", "site-02-data", "site-01-data", 2.5, 20.0),
    }
    scenario = Scenario(
        scenario_id="pilot-scenario",
        sites=sites,
        nodes=nodes,
        files={"file-001": File("file-001", 1.0)},
        replicas={"primary-001": Replica("primary-001", "file-001", "site-01-data", True)},
        users={"client-01": User("client-01", "site-01")},
        network_links=links,
    )
    return SimulationState(scenario)


def build_pilot_artifacts() -> PilotArtifacts:
    request = Request(
        "request-000001", "client-01", "file-001", 6.0,
        sequence=1, operation="read", source_site_id="site-01", source_node_id="site-01-edge",
    )
    return PilotArtifacts("pilot-balanced", (request,), (), "pilot-artifacts-v1")


def _adapter(method_id: str, state: SimulationState) -> SimulationAdapter:
    file_id = "file-001"
    if method_id == "Proposed":
        request = ProposedRequest(
            file_id=file_id,
            ois=OisInput(((0.0, 1.0),), 6.0, 0.0001, 1.0, 1.0, 1.0, 1.0, 1.0, OisWeights()),
            weighted_access_rate=2.0,
            maximum_replication_rate=1.0,
            current_replica_count=1,
        )
        from .proposed import ProposedAdapter
        return ProposedAdapter(request)
    if method_id == "HRS":
        from .hrs import HRSAdapter
        return HRSAdapter(HrsRequest(file_id, (HrsSite("site-01", normalized_accesses=1.0, normalized_centrality=1.0), HrsSite("site-02", normalized_accesses=0.5, normalized_centrality=0.5)), weights=HrsWeights()))
    if method_id == "DPRS":
        from .dprs import DPRSAdapter
        timings = tuple(DprsNodeTiming(node_id, 0.5, 1.0, 10.0) for node_id in state.scenario.nodes)
        connections = tuple(DprsConnection(link.source_node_id, link.target_node_id, link.bandwidth or 1.0, 1.0) for link in state.scenario.network_links.values())
        return DPRSAdapter(DprsRequest(DprsDataset(file_id, 1.0), timings, connections, 1.0, 1.0))
    if method_id == "OGSA":
        from .ogsa import OGSAAdapter
        assignment = OgsaAssignment(((1, 0, 0, 0),), (1.0,), (100.0, 100.0, 100.0, 100.0))
        context = OgsaObjectiveContext((0.1,), ((1.0, 1.0, 1.0, 1.0),), ((1.0, 0.0, 0.0, 0.0),), (1.0, 1.0, 1.0, 1.0), ((1.0, 0.0, 0.0, 0.0),), (10.0,) * 4, (2.0,) * 4, 2.0, (1.0,))
        return OGSAAdapter(OgsaRequest(assignment, context, OgsaWeights.source_reported_equal(), OgsaConfig(population_size=4, generations=1), file_id=file_id))
    if method_id == "EIMORM":
        from .eimorm import EIMORMAdapter
        return EIMORMAdapter(EimormRequest(EimormContext(file_id, 6.0, 0.0, 1, 1.0, 1.0, 12.0, 10.0)))
    raise ValueError("unknown pilot method")


def run_pilot(method_ids: Tuple[str, ...] = ("Proposed", "HRS", "DPRS", "OGSA", "EIMORM")) -> Tuple[PilotRun, ...]:
    artifacts = build_pilot_artifacts()
    frozen = FrozenScenario.capture(build_pilot_scenario(), ReplayTrace(artifacts.failure_events, "pilot-scenario", "pilot-seed", "pilot-stream"))
    results = []
    for method_id in method_ids:
        state = frozen.clone_state()
        recorder = RawRecorder()
        executor = DecisionExecutor(recorder=recorder)
        adapter = _adapter(method_id, state)
        dispatcher = AdapterDispatcher(_registry(method_id), executor)
        dispatch = dispatcher.dispatch(method_id, state, adapter, f"pilot-{method_id}")
        request_result = _serve(state, artifacts.requests[0], recorder)
        results.append(PilotRun(method_id, f"pilot-{method_id}", "VALID", int(request_result.outcome == "SUCCESS"), int(request_result.outcome != "SUCCESS"), 1, int(dispatch.execution is not None), recorder.observations))
    return tuple(results)


def _registry(method_id: str) -> MethodRegistry:
    registry = MethodRegistry()
    registry.register(MethodRegistration(method_id, lambda: None))
    return registry


def _serve(state: SimulationState, request: Request, recorder: RawRecorder):
    from .runtime import RequestServiceExecutor
    return RequestServiceExecutor(recorder).serve(state, request)

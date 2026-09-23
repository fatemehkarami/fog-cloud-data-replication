"""Source-faithful HRS calculation and adapter boundaries.

This module does not select unresolved weights or invent the incomplete fuzzy
system. It computes only source-supported terms and returns explicit unresolved
results when execution needs missing scientific policy.
"""

from dataclasses import dataclass
from enum import Enum
from math import inf
from typing import Dict, Iterable, Optional, Protocol, Sequence, Tuple

from .adapters import AdapterCapabilities, AdapterSnapshot, SimulationAdapter
from .decisions import DecisionEnvelope, DecisionKind, DecisionStatus


class HRSUnresolvedError(ValueError):
    """Raised when HRS source incompleteness blocks a requested calculation."""


@dataclass(frozen=True)
class HrsWeights:
    w1: Optional[float] = None
    w2: Optional[float] = None
    w3: Optional[float] = None
    w4: Optional[float] = None
    w5: Optional[float] = None

    @property
    def merit_complete(self) -> bool:
        return self.w1 is not None and self.w2 is not None

    @property
    def total_cost_complete(self) -> bool:
        return all(value is not None for value in (self.w3, self.w4, self.w5))


DEFAULT_HRS_WEIGHTS = HrsWeights(0.5, 0.5, 1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)


@dataclass(frozen=True)
class HrsSite:
    site_id: str
    distances: Tuple[Tuple[str, float], ...] = ()
    number_of_accesses: Optional[float] = None
    normalized_accesses: Optional[float] = None
    normalized_centrality: Optional[float] = None


@dataclass(frozen=True)
class HrsVm:
    vm_id: str
    site_id: str
    processors: Optional[float] = None
    cpu_capability: Optional[float] = None
    bandwidth: Optional[float] = None
    network_latency: Optional[float] = None
    queued_task_length: Optional[float] = None
    service_rate: Optional[float] = None


@dataclass(frozen=True)
class HrsProvider:
    provider_id: str
    vm_id: str
    site_id: str
    file_id: str
    healthy: bool = True
    reachable: bool = True


@dataclass(frozen=True)
class HrsReplica:
    replica_id: str
    file_id: str
    site_id: str
    size: float
    number_of_accesses: Optional[float] = None
    replication_cost: Optional[float] = None
    last_access_interval: Optional[float] = None


@dataclass(frozen=True)
class HrsRequest:
    file_id: str
    candidate_sites: Tuple[HrsSite, ...] = ()
    vms: Tuple[HrsVm, ...] = ()
    providers: Tuple[HrsProvider, ...] = ()
    replicas_at_target: Tuple[HrsReplica, ...] = ()
    requested_size: Optional[float] = None
    available_storage: Optional[float] = None
    weights: HrsWeights = HrsWeights()
    operation: str = "placement"


class FuzzyReplacementPolicy(Protocol):
    def value(self, replica: HrsReplica) -> float:
        ...


def closeness_centrality(site_id: str, distances: Sequence[Tuple[str, float]], site_count: int) -> float:
    if site_count < 1:
        raise HRSUnresolvedError("HRS centrality requires a positive site count")
    distance_sum = sum(distance for other_id, distance in distances if other_id != site_id)
    if distance_sum == 0:
        raise HRSUnresolvedError("HRS centrality is undefined for zero distance sum")
    return (site_count - 1) / distance_sum


def uniform_normalize_1_to_10(value: float, minimum: float, maximum: float) -> float:
    """Apply the HRS source-defined uniform interval scale.

    Boundary ownership, max == min, and out-of-range values remain unresolved
    rather than receiving an implementation default.
    """
    if maximum < minimum:
        raise HRSUnresolvedError("HRS normalization bounds are invalid")
    if maximum == minimum:
        return 5.5
    value = min(maximum, max(minimum, value))
    increment = (maximum - minimum) / 10.0
    if value < minimum or value > maximum:
        raise HRSUnresolvedError("HRS normalization value is outside source bounds")
    relative = (value - minimum) / increment
    return min(10.0, max(1.0, float(int(relative) + 1)))


def merit(number_of_accesses: float, centrality: float, weights: HrsWeights) -> float:
    weights = weights if weights.merit_complete else DEFAULT_HRS_WEIGHTS
    return weights.w1 * number_of_accesses + weights.w2 * centrality


def vm_capability(vm: HrsVm) -> float:
    if vm.processors is None or vm.cpu_capability is None or vm.bandwidth is None:
        raise HRSUnresolvedError("HRS VM capability inputs are incomplete")
    return vm.processors * vm.cpu_capability + vm.bandwidth


def vm_load(vm: HrsVm) -> float:
    if vm.queued_task_length is None or vm.service_rate is None or vm.service_rate == 0:
        raise HRSUnresolvedError("HRS VM load inputs are incomplete or undefined")
    return vm.queued_task_length / vm.service_rate


def network_performance(bandwidth: float, latency: float) -> float:
    if latency == 0:
        raise HRSUnresolvedError("HRS network performance is undefined for zero latency")
    return bandwidth / latency


def total_cost(capability: float, load: float, performance: float, weights: HrsWeights) -> float:
    weights = weights if weights.total_cost_complete else DEFAULT_HRS_WEIGHTS
    if capability == 0 or performance == 0:
        raise HRSUnresolvedError("HRS TotalCost reciprocal term is undefined")
    return weights.w3 * (1 / capability) + weights.w4 * load + weights.w5 * (1 / performance)


def replication_cost(size: float, bandwidth: float, propagation_delay: float) -> float:
    if bandwidth <= 0:
        raise HRSUnresolvedError("HRS replication cost requires positive bandwidth")
    return size / bandwidth + propagation_delay


def rank_replicas_by_value(replicas: Sequence[HrsReplica], policy: FuzzyReplacementPolicy) -> Tuple[HrsReplica, ...]:
    """Rank replicas only when an explicit fuzzy policy is supplied."""
    try:
        values = [(policy.value(replica), replica) for replica in replicas]
    except (AttributeError, NotImplementedError) as error:
        raise HRSUnresolvedError("HRS fuzzy replacement policy is unresolved") from error
    if any(value is None for value, _ in values):
        raise HRSUnresolvedError("HRS fuzzy replacement value is unresolved")
    return tuple(replica for _, replica in sorted(values, key=lambda item: (item[0], item[1].replica_id)))


class DeterministicFuzzyReplacementPolicy:
    """Researcher-defined bounded fuzzy proxy for executable HRS replacement."""

    @staticmethod
    def _bounded(value: Optional[float]) -> float:
        if value is None or value < 0:
            return 0.0
        return value / (1.0 + value)

    def value(self, replica: HrsReplica) -> float:
        access = self._bounded(replica.number_of_accesses)
        cost = self._bounded(replica.replication_cost)
        recency = self._bounded(replica.last_access_interval)
        return 0.5 * access + 0.3 * (1.0 - cost) + 0.2 * (1.0 - recency)


def replacement_candidates(
    replicas: Sequence[HrsReplica],
    required_space: float,
    available_storage: float,
    policy: Optional[FuzzyReplacementPolicy],
) -> Tuple[HrsReplica, ...]:
    if available_storage >= required_space:
        return ()
    policy = policy or DeterministicFuzzyReplacementPolicy()
    selected = []
    freed = available_storage
    for replica in rank_replicas_by_value(replicas, policy):
        if replica.replica_id.lower() == "primary":
            continue
        selected.append(replica)
        freed += replica.size
        if freed >= required_space:
            return tuple(selected)
    raise HRSUnresolvedError("HRS storage remains insufficient after candidate replicas")


class HRSAdapter(SimulationAdapter):
    method_id = "HRS"

    def __init__(self, request: HrsRequest, fuzzy_policy: Optional[FuzzyReplacementPolicy] = None) -> None:
        self.request = request
        self.fuzzy_policy = fuzzy_policy

    @property
    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            (
                DecisionKind.PLACEMENT,
                DecisionKind.PROVIDER_SELECTION,
                DecisionKind.REPLICA_CREATION,
                DecisionKind.REPLICA_DELETION,
                DecisionKind.UNRESOLVED,
            )
        )

    def compute(self, snapshot: AdapterSnapshot) -> DecisionEnvelope:
        try:
            if self.request.operation == "placement":
                return self._placement(snapshot)
            if self.request.operation == "provider_selection":
                return self._provider_selection(snapshot)
            if self.request.operation == "replacement":
                return self._replacement(snapshot)
            return DecisionEnvelope.unresolved(
                DecisionKind.UNRESOLVED,
                "HRS operation is not defined by the common adapter request",
            )
        except HRSUnresolvedError as error:
            return DecisionEnvelope.unresolved(DecisionKind.UNRESOLVED, str(error))

    def _placement(self, snapshot: AdapterSnapshot) -> DecisionEnvelope:
        scores = []
        for site in self.request.candidate_sites:
            accesses = site.normalized_accesses if site.normalized_accesses is not None else site.number_of_accesses
            centrality = site.normalized_centrality
            if accesses is None:
                raise HRSUnresolvedError("HRS placement access count is incomplete")
            if centrality is None:
                centrality = closeness_centrality(site.site_id, site.distances, len(self.request.candidate_sites))
            scores.append((merit(accesses, centrality, self.request.weights), site.site_id))
        if not scores:
            raise HRSUnresolvedError("HRS has no candidate placement sites")
        highest = max(score for score, _ in scores)
        winners = tuple(sorted(site_id for score, site_id in scores if score == highest))
        winner = winners[0]
        nodes = snapshot.scenario.get("nodes", {})
        data_nodes = sorted(
            node_id for node_id, node in nodes.items()
            if node.get("site_id") == winner and node_id.endswith("-data")
        )
        if not data_nodes:
            data_nodes = sorted(
                node_id for node_id, node in nodes.items()
                if node.get("site_id") == winner
            )
        if not data_nodes:
            raise HRSUnresolvedError("HRS placement site has no executable node mapping")
        return DecisionEnvelope(
            kind=DecisionKind.PLACEMENT,
            status=DecisionStatus.ACCEPTED,
            payload=(("file_id", self.request.file_id), ("site_id", winner), ("placement_node_ids", (data_nodes[0],))),
            provenance=(("method_id", self.method_id), ("scenario_id", snapshot.scenario_id)),
        )

    def _provider_selection(self, snapshot: AdapterSnapshot) -> DecisionEnvelope:
        candidates = [provider for provider in self.request.providers if provider.healthy and provider.reachable]
        if not candidates:
            raise HRSUnresolvedError("HRS has no valid candidate replica providers")
        vm_by_id = {vm.vm_id: vm for vm in self.request.vms}
        scored = []
        for provider in candidates:
            vm = vm_by_id.get(provider.vm_id)
            if vm is None:
                raise HRSUnresolvedError("HRS provider VM data is incomplete")
            capability = vm_capability(vm)
            load = vm_load(vm)
            if vm.network_latency is None:
                raise HRSUnresolvedError("HRS provider network latency is incomplete")
            performance = network_performance(vm.bandwidth, vm.network_latency)
            scored.append((total_cost(capability, load, performance, self.request.weights), provider.provider_id))
        lowest = min(score for score, _ in scored)
        winners = tuple(provider_id for score, provider_id in scored if score == lowest)
        if len(winners) != 1:
            raise HRSUnresolvedError("HRS TotalCost tie policy is unresolved")
        return DecisionEnvelope(
            kind=DecisionKind.PROVIDER_SELECTION,
            status=DecisionStatus.ACCEPTED,
            payload=(("file_id", self.request.file_id), ("provider_id", winners[0])),
            provenance=(("method_id", self.method_id), ("scenario_id", snapshot.scenario_id)),
        )

    def _replacement(self, snapshot: AdapterSnapshot) -> DecisionEnvelope:
        if self.request.requested_size is None or self.request.available_storage is None:
            raise HRSUnresolvedError("HRS replacement storage inputs are incomplete")
        selected = replacement_candidates(
            self.request.replicas_at_target,
            self.request.requested_size,
            self.request.available_storage,
            self.fuzzy_policy or DeterministicFuzzyReplacementPolicy(),
        )
        selected_ids = tuple(replica.replica_id for replica in selected)
        return DecisionEnvelope(
            kind=DecisionKind.REPLICA_DELETION,
            status=DecisionStatus.ACCEPTED,
            payload=(("file_id", self.request.file_id), ("replica_id", selected_ids[0] if selected_ids else None), ("remaining_replica_ids", selected_ids[1:])),
            provenance=(("method_id", self.method_id), ("scenario_id", snapshot.scenario_id)),
        )

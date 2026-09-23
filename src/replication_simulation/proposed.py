"""Source-faithful Proposed Method structures and policy boundaries.

This module preserves the complete Proposed pipeline without selecting open
scientific parameters or implementing simulator mutation.
"""

from dataclasses import dataclass, field
from enum import Enum
from math import ceil, log, sqrt
from random import Random
from typing import Any, Callable, Mapping, Optional, Protocol, Sequence, Tuple

from .adapters import AdapterCapabilities, AdapterSnapshot, SimulationAdapter
from .decisions import DecisionEnvelope, DecisionKind, DecisionStatus


class ProposedUnresolvedError(ValueError):
    """Raised when an unresolved Proposed definition blocks a calculation."""


class ObjectiveDirection(str, Enum):
    MINIMIZE = "minimize"
    MAXIMIZE = "maximize"


@dataclass(frozen=True)
class OisWeights:
    w1: Optional[float] = None
    w2: Optional[float] = None
    w3: Optional[float] = None
    w4: Optional[float] = None
    w5: Optional[float] = None

    @property
    def complete(self) -> bool:
        return all(value is not None for value in (self.w1, self.w2, self.w3, self.w4, self.w5))


DEFAULT_OIS_WEIGHTS = OisWeights(0.2, 0.2, 0.2, 0.2, 0.2)


@dataclass(frozen=True)
class OisInput:
    access_events: Tuple[Tuple[float, float], ...] = ()
    current_time: Optional[float] = None
    decay_parameter: Optional[float] = None
    file_size: Optional[float] = None
    replication_count: Optional[float] = None
    replication_weight: Optional[float] = None
    file_type_priority: Optional[float] = None
    user_count: Optional[float] = None
    weights: OisWeights = OisWeights()


@dataclass(frozen=True)
class OisComponents:
    access_frequency: float
    file_size: float
    replication_frequency: float
    file_type: float
    user_count: float


@dataclass(frozen=True)
class ObjectiveVector:
    energy: float
    response_time: float
    data_node_load: float
    total_cost: float
    network_centrality: float

    @property
    def values(self) -> Tuple[float, ...]:
        return (
            self.energy,
            self.response_time,
            self.data_node_load,
            self.total_cost,
            self.network_centrality,
        )


PROPOSED_OBJECTIVE_DIRECTIONS = (
    ObjectiveDirection.MINIMIZE,
    ObjectiveDirection.MINIMIZE,
    ObjectiveDirection.MINIMIZE,
    ObjectiveDirection.MINIMIZE,
    ObjectiveDirection.MAXIMIZE,
)


@dataclass(frozen=True)
class ReplicaCountResult:
    additional_replicas: int
    action: str


@dataclass(frozen=True)
class Nsga3Config:
    population_size: int = 12
    generation_count: int = 5
    reference_directions: Tuple[Tuple[float, ...], ...] = ()
    crossover: Optional[Callable[..., Any]] = None
    mutation: Optional[Callable[..., Any]] = None
    rng: Optional[Random] = field(default=None, compare=False, repr=False)


@dataclass(frozen=True)
class ProposedRequest:
    file_id: str
    ois: Optional[OisInput] = None
    weighted_access_rate: Optional[float] = None
    maximum_replication_rate: Optional[float] = None
    current_replica_count: Optional[int] = None
    nsga3: Nsga3Config = Nsga3Config()
    operation: str = "pipeline"


class TimingPolicy(Protocol):
    def should_replicate(self, request: ProposedRequest) -> bool:
        ...


class ReplacementPolicy(Protocol):
    def rank(self, file_id: str, snapshot: AdapterSnapshot) -> Tuple[str, ...]:
        ...


def compute_ois_components(value: OisInput) -> OisComponents:
    if value.current_time is None or value.decay_parameter is None:
        raise ProposedUnresolvedError("OIS access-decay inputs are unresolved")
    if value.file_size is None or value.file_size <= 0:
        raise ProposedUnresolvedError("OIS file size is unresolved or invalid")
    if value.replication_count is None or value.replication_weight is None:
        raise ProposedUnresolvedError("OIS replication-frequency inputs are unresolved")
    if value.file_type_priority is None or value.user_count is None:
        raise ProposedUnresolvedError("OIS file-type or user-count input is unresolved")
    if not value.access_events:
        raise ProposedUnresolvedError("OIS access history is unresolved")
    denominator = 0.0
    numerator = 0.0
    for access_time, event_value in value.access_events:
        weight = exp_decay(value.decay_parameter, value.current_time - access_time)
        numerator += weight * event_value
        denominator += weight
    if denominator == 0:
        raise ProposedUnresolvedError("OIS access normalization is undefined")
    return OisComponents(
        access_frequency=numerator / denominator,
        file_size=log(value.file_size),
        replication_frequency=value.replication_count * value.replication_weight,
        file_type=value.file_type_priority,
        user_count=value.user_count,
    )


def exp_decay(decay_parameter: float, elapsed_time: float) -> float:
    """Preserve the source's exponential access-decay structure."""
    from math import exp
    return exp(-decay_parameter * elapsed_time)


def compute_ois(value: OisInput) -> float:
    weights = value.weights if value.weights.complete else DEFAULT_OIS_WEIGHTS
    components = compute_ois_components(value)
    return (
        weights.w1 * components.access_frequency
        + weights.w2 * components.file_size
        + weights.w3 * components.replication_frequency
        + weights.w4 * components.file_type
        + weights.w5 * components.user_count
    )


def determine_replica_count(
    weighted_access_rate: Optional[float],
    maximum_replication_rate: Optional[float],
    current_replica_count: Optional[int],
) -> ReplicaCountResult:
    if weighted_access_rate is None or maximum_replication_rate is None or current_replica_count is None:
        raise ProposedUnresolvedError("Proposed replica-count inputs are unresolved")
    if maximum_replication_rate <= 0:
        raise ProposedUnresolvedError("Proposed maximum replication rate is undefined")
    additional = ceil(weighted_access_rate / maximum_replication_rate) - current_replica_count
    if additional > 0:
        action = "create"
    elif additional < 0:
        action = "delete_candidates"
    else:
        action = "no_op"
    return ReplicaCountResult(additional, action)


def objective_key(vector: ObjectiveVector) -> Tuple[float, ...]:
    """Represent the scientific directions uniformly for comparisons."""
    return tuple(
        value if direction is ObjectiveDirection.MINIMIZE else -value
        for value, direction in zip(vector.values, PROPOSED_OBJECTIVE_DIRECTIONS)
    )


def dominates(left: ObjectiveVector, right: ObjectiveVector) -> bool:
    left_key = objective_key(left)
    right_key = objective_key(right)
    return all(a <= b for a, b in zip(left_key, right_key)) and any(
        a < b for a, b in zip(left_key, right_key)
    )


def nondominated_sort(population: Sequence[ObjectiveVector]) -> Tuple[Tuple[int, ...], ...]:
    domination_counts = [0] * len(population)
    dominates_map = [[] for _ in population]
    fronts = [[]]
    for index, candidate in enumerate(population):
        for other_index, other in enumerate(population):
            if index == other_index:
                continue
            if dominates(candidate, other):
                dominates_map[index].append(other_index)
            elif dominates(other, candidate):
                domination_counts[index] += 1
        if domination_counts[index] == 0:
            fronts[0].append(index)
    front_index = 0
    while front_index < len(fronts) and fronts[front_index]:
        next_front = []
        for index in fronts[front_index]:
            for dominated_index in dominates_map[index]:
                domination_counts[dominated_index] -= 1
                if domination_counts[dominated_index] == 0:
                    next_front.append(dominated_index)
        front_index += 1
        if next_front:
            fronts.append(next_front)
    return tuple(tuple(front) for front in fronts if front)


def association_candidates(
    objective_vectors: Sequence[ObjectiveVector],
    reference_directions: Sequence[Tuple[float, ...]],
) -> Tuple[Tuple[int, int], ...]:
    if not reference_directions:
        raise ProposedUnresolvedError("NSGA-III reference directions are unresolved")
    if any(len(direction) != 5 for direction in reference_directions):
        raise ProposedUnresolvedError("NSGA-III reference directions must match five objectives")
    normalized = []
    for vector in objective_vectors:
        normalized.append(
            tuple(
                value
                for value in ProposedAdapter._normalized_key(vector, objective_vectors)
            )
        )
    associations = []
    for index, point in enumerate(normalized):
        best_direction = min(
            range(len(reference_directions)),
            key=lambda direction_index: sum(
                (point[dimension] - reference_directions[direction_index][dimension]) ** 2
                for dimension in range(5)
            ),
        )
        associations.append((index, best_direction))
    return tuple(associations)


class ProposedAdapter(SimulationAdapter):
    method_id = "Proposed"

    def __init__(self, request: ProposedRequest, timing_policy: Optional[TimingPolicy] = None) -> None:
        self.request = request
        self.timing_policy = timing_policy

    @property
    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            (
                DecisionKind.PLACEMENT,
                DecisionKind.REPLICA_COUNT,
                DecisionKind.REPLICA_DELETION,
            )
        )

    @staticmethod
    def _default_reference_directions() -> Tuple[Tuple[float, ...], ...]:
        return tuple(
            tuple(1.0 if index == dimension else 0.0 for index in range(5))
            for dimension in range(5)
        )

    @staticmethod
    def _node_payload(snapshot: AdapterSnapshot, node_id: str) -> Mapping[str, Any]:
        nodes = snapshot.scenario.get("nodes", {})
        return nodes[node_id]

    @classmethod
    def _candidate_nodes(cls, snapshot: AdapterSnapshot, file_id: str) -> Tuple[str, ...]:
        nodes = snapshot.scenario.get("nodes", {})
        replicas = snapshot.scenario.get("replicas", {})
        occupied = {
            replica["node_id"]
            for replica in replicas.values()
            if replica.get("file_id") == file_id and replica.get("valid", True)
        }
        candidates = []
        for node_id in sorted(nodes):
            node = cls._node_payload(snapshot, node_id)
            if node_id in occupied or not node.get("healthy", True) or not node.get("reachable", True):
                continue
            capacity = node.get("storage_capacity")
            used = node.get("storage_used", 0.0)
            if capacity is not None and used >= capacity:
                continue
            candidates.append(node_id)
        return tuple(candidates)

    @classmethod
    def _objective_for_node(cls, snapshot: AdapterSnapshot, file_id: str, node_id: str) -> ObjectiveVector:
        node = cls._node_payload(snapshot, node_id)
        capacity = node.get("storage_capacity")
        used = node.get("storage_used", 0.0)
        load = used / capacity if capacity and capacity > 0 else 0.0
        links = snapshot.scenario.get("network_links", {})
        degree = sum(
            1
            for link in links.values()
            if link.get("source_node_id") == node_id or link.get("target_node_id") == node_id
        )
        centrality = 1.0 / (1.0 + degree) if degree else 1.0
        file_size = snapshot.scenario.get("files", {}).get(file_id, {}).get("size") or 0.0
        capacity_cost = file_size / capacity if capacity and capacity > 0 else 1.0
        return ObjectiveVector(load, load, load, capacity_cost, centrality)

    @staticmethod
    def _normalized_key(vector: ObjectiveVector, population: Sequence[ObjectiveVector]) -> Tuple[float, ...]:
        keys = [objective_key(item) for item in population]
        current = objective_key(vector)
        normalized = []
        for dimension, value in enumerate(current):
            values = [item[dimension] for item in keys]
            lower, upper = min(values), max(values)
            normalized.append(0.0 if upper == lower else (value - lower) / (upper - lower))
        return tuple(normalized)

    @classmethod
    def _select_nodes(cls, snapshot: AdapterSnapshot, file_id: str, count: int, config: Nsga3Config) -> Tuple[str, ...]:
        candidates = cls._candidate_nodes(snapshot, file_id)
        if not candidates:
            raise ProposedUnresolvedError("Proposed has no healthy, reachable, capacity-valid placement candidate")
        vectors = tuple(cls._objective_for_node(snapshot, file_id, node_id) for node_id in candidates)
        population = list(candidates)
        directions = config.reference_directions or cls._default_reference_directions()
        for _ in range(max(0, config.generation_count)):
            fronts = nondominated_sort(tuple(vectors))
            if not fronts:
                break
            # Deterministic NSGA-III-style environmental selection: retain the
            # nondominated candidates, then use normalized reference association.
            selected = list(fronts[0])
            if len(selected) < min(config.population_size, len(population)):
                remaining = [index for index in range(len(population)) if index not in selected]
                selected.extend(sorted(remaining, key=lambda index: objective_key(vectors[index])))
            selected = selected[: min(config.population_size, len(population))]
            population = [population[index] for index in selected]
            vectors = [vectors[index] for index in selected]
        ranked = sorted(
            zip(population, vectors),
            key=lambda item: (cls._normalized_key(item[1], vectors), item[0]),
        )
        return tuple(node_id for node_id, _ in ranked[: min(count, len(ranked))])

    @staticmethod
    def _deletion_candidate(snapshot: AdapterSnapshot, file_id: str) -> Optional[str]:
        replicas = [
            (replica_id, replica)
            for replica_id, replica in snapshot.scenario.get("replicas", {}).items()
            if replica.get("file_id") == file_id and replica.get("valid", True)
        ]
        if len(replicas) <= 1:
            return None
        return sorted(replicas, key=lambda item: item[0], reverse=True)[0][0]

    def compute(self, snapshot: AdapterSnapshot) -> DecisionEnvelope:
        stages = ("ois", "selection", "timing", "replica_count", "nsga3_placement", "replacement")
        try:
            if self.request.ois is None:
                raise ProposedUnresolvedError("OIS input is unresolved")
            compute_ois(self.request.ois)
            if self.timing_policy is not None and not self.timing_policy.should_replicate(self.request):
                return DecisionEnvelope.no_op("Proposed timing policy selected no replication")
            count = determine_replica_count(
                self.request.weighted_access_rate,
                self.request.maximum_replication_rate,
                self.request.current_replica_count,
            )
            if count.action == "no_op":
                return DecisionEnvelope.no_op("Proposed replica-count stage selected no action")
            if count.action == "delete_candidates":
                replica_id = self._deletion_candidate(snapshot, self.request.file_id)
                if replica_id is None:
                    return DecisionEnvelope.no_op("Proposed replacement preserved the last valid replica")
                return DecisionEnvelope(
                    DecisionKind.REPLICA_DELETION,
                    DecisionStatus.ACCEPTED,
                    (("file_id", self.request.file_id), ("replica_id", replica_id), ("stages", stages)),
                    provenance=(("method_id", self.method_id), ("scenario_id", snapshot.scenario_id)),
                )
            if not self.request.nsga3.reference_directions:
                directions = self._default_reference_directions()
                config = Nsga3Config(
                    population_size=self.request.nsga3.population_size,
                    generation_count=self.request.nsga3.generation_count,
                    reference_directions=directions,
                    crossover=self.request.nsga3.crossover,
                    mutation=self.request.nsga3.mutation,
                    rng=self.request.nsga3.rng,
                )
            else:
                config = self.request.nsga3
            node_ids = self._select_nodes(snapshot, self.request.file_id, count.additional_replicas, config)
            return DecisionEnvelope(
                DecisionKind.PLACEMENT,
                DecisionStatus.ACCEPTED,
                (
                    ("file_id", self.request.file_id),
                    ("placement_node_ids", node_ids),
                    ("replica_count", count.additional_replicas),
                    ("stages", stages),
                    ("normalization", "population_min_max_internal"),
                ),
                provenance=(("method_id", self.method_id), ("scenario_id", snapshot.scenario_id)),
            )
        except ProposedUnresolvedError as error:
            return DecisionEnvelope.unresolved(DecisionKind.UNRESOLVED, str(error))

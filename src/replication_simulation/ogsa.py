"""Source-faithful OGSA (OBL + GSA) components.

The source's GSO terminology is intentionally not implemented. Scientific
policies that remain unresolved return explicit unresolved results.
"""

from dataclasses import dataclass
from math import inf, sqrt
from random import Random
from typing import Callable, Optional, Protocol, Sequence, Tuple

from .adapters import AdapterCapabilities, AdapterSnapshot, SimulationAdapter
from .decisions import DecisionEnvelope, DecisionKind, DecisionStatus


class OGSAUnresolvedError(ValueError):
    """Raised when an unresolved OGSA policy blocks execution."""


AssignmentMatrix = Tuple[Tuple[int, ...], ...]


@dataclass(frozen=True)
class OgsaAssignment:
    matrix: AssignmentMatrix
    file_sizes: Tuple[float, ...]
    node_capacities: Tuple[float, ...]


@dataclass(frozen=True)
class OgsaObjectiveContext:
    unavailable_probabilities: Tuple[float, ...] = ()
    service_time_by_file_node: Tuple[Tuple[float, ...], ...] = ()
    access_by_file_node: Tuple[Tuple[float, ...], ...] = ()
    node_load_values: Tuple[float, ...] = ()
    energy_load_by_file_node: Tuple[Tuple[float, ...], ...] = ()
    pmax_by_node: Tuple[float, ...] = ()
    pidle_by_node: Tuple[float, ...] = ()
    q: Optional[float] = None
    latency_by_file: Tuple[float, ...] = ()


@dataclass(frozen=True)
class OgsaObjectiveVector:
    mfu: float
    mst: float
    lv: float
    ec: float
    ml: float

    @property
    def values(self) -> Tuple[float, ...]:
        return self.mfu, self.mst, self.lv, self.ec, self.ml


@dataclass(frozen=True)
class OgsaWeights:
    alpha1: float
    alpha2: float
    alpha3: float
    alpha4: float
    alpha5: float

    @classmethod
    def source_reported_equal(cls) -> "OgsaWeights":
        return cls(0.2, 0.2, 0.2, 0.2, 0.2)

    @property
    def values(self) -> Tuple[float, ...]:
        return self.alpha1, self.alpha2, self.alpha3, self.alpha4, self.alpha5


@dataclass(frozen=True)
class OgsaAgent:
    position: Tuple[float, ...]
    velocity: Tuple[float, ...]


@dataclass(frozen=True)
class OgsaConfig:
    population_size: int = 8
    generations: int = 5
    g0: float = 1.0
    epsilon: float = 1e-9
    lower_bound: float = 0.0
    upper_bound: float = 1.0
    non_uniformity: float = 2.0
    rng: Optional[Random] = None


class ContinuousToBinaryPolicy(Protocol):
    def convert(self, position: Tuple[float, ...], file_count: int, node_count: int) -> AssignmentMatrix:
        ...


class FeasibilityPolicy(Protocol):
    def handle(self, assignment: AssignmentMatrix) -> AssignmentMatrix:
        ...


class InitializationPolicy(Protocol):
    def create(self, population_size: int, dimensions: int) -> Tuple[OgsaAgent, ...]:
        ...


class RandomSource(Protocol):
    def random(self) -> float:
        ...


def validate_assignment(assignment: OgsaAssignment) -> None:
    if not assignment.matrix:
        raise OGSAUnresolvedError("OGSA assignment matrix is empty")
    if len(assignment.matrix) != len(assignment.file_sizes):
        raise OGSAUnresolvedError("OGSA file assignment dimensions are inconsistent")
    node_count = len(assignment.node_capacities)
    if any(len(row) != node_count for row in assignment.matrix):
        raise OGSAUnresolvedError("OGSA assignment matrix dimensions are inconsistent")
    if any(value not in (0, 1) for row in assignment.matrix for value in row):
        raise OGSAUnresolvedError("OGSA assignment matrix must be binary")
    if any(sum(row) == 0 for row in assignment.matrix):
        raise OGSAUnresolvedError("OGSA integrity constraint requires one assignment per file")
    usage = [0.0] * node_count
    for row, size in zip(assignment.matrix, assignment.file_sizes):
        for node_index, assigned in enumerate(row):
            if assigned:
                usage[node_index] += size
    if any(used > capacity for used, capacity in zip(usage, assignment.node_capacities)):
        raise OGSAUnresolvedError("OGSA capacity constraint is violated")


def mfu(assignment: OgsaAssignment, context: OgsaObjectiveContext) -> float:
    if len(context.unavailable_probabilities) != len(assignment.matrix):
        raise OGSAUnresolvedError("OGSA MFU inputs are incomplete")
    values = []
    for row, probability in zip(assignment.matrix, context.unavailable_probabilities):
        values.append(sum(value * probability for value in row))
    return sum(values) / len(values)


def mst(assignment: OgsaAssignment, context: OgsaObjectiveContext) -> float:
    service = context.service_time_by_file_node
    access = context.access_by_file_node
    if len(service) != len(assignment.matrix) or len(access) != len(assignment.matrix):
        raise OGSAUnresolvedError("OGSA MST inputs are incomplete")
    totals = []
    for service_row, access_row in zip(service, access):
        if len(service_row) != len(access_row):
            raise OGSAUnresolvedError("OGSA MST row dimensions are inconsistent")
        access_total = sum(access_row)
        if access_total == 0:
            totals.append(0.0)
        else:
            totals.append(sum(value * weight for value, weight in zip(service_row, access_row)) / access_total)
    return sum(totals) / len(totals)


def lv(context: OgsaObjectiveContext) -> float:
    loads = context.node_load_values
    if len(loads) < 2:
        raise OGSAUnresolvedError("OGSA LV requires at least two node load values")
    mean = sum(loads) / len(loads)
    return sum((value - mean) ** 2 for value in loads) / (len(loads) - 1)


def ec(assignment: OgsaAssignment, context: OgsaObjectiveContext) -> float:
    if context.q is None or context.q == 0:
        raise OGSAUnresolvedError("OGSA EC cooling parameter Q is unresolved")
    if len(context.pmax_by_node) != len(assignment.node_capacities) or len(context.pidle_by_node) != len(assignment.node_capacities):
        raise OGSAUnresolvedError("OGSA EC power inputs are incomplete")
    if len(context.energy_load_by_file_node) != len(assignment.matrix):
        raise OGSAUnresolvedError("OGSA EC load inputs are incomplete")
    total = 0.0
    for node_index, (pmax, pidle) in enumerate(zip(context.pmax_by_node, context.pidle_by_node)):
        node_load = sum(
            assignment.matrix[file_index][node_index] * context.energy_load_by_file_node[file_index][node_index]
            for file_index in range(len(assignment.matrix))
        )
        total += node_load * (pmax - pidle) + pidle
    return (1 + 1 / context.q) * total


def ml(context: OgsaObjectiveContext) -> float:
    if not context.latency_by_file:
        raise OGSAUnresolvedError("OGSA ML inputs are incomplete")
    return sum(context.latency_by_file) / len(context.latency_by_file)


def objective_vector(assignment: OgsaAssignment, context: OgsaObjectiveContext) -> OgsaObjectiveVector:
    return OgsaObjectiveVector(
        mfu(assignment, context),
        mst(assignment, context),
        lv(context),
        ec(assignment, context),
        ml(context),
    )


def mof(objectives: OgsaObjectiveVector, weights: OgsaWeights) -> float:
    return sum(value * weight for value, weight in zip(objectives.values, weights.values))


def opposite_position(position: Sequence[float], lower: Sequence[float], upper: Sequence[float]) -> Tuple[float, ...]:
    if not (len(position) == len(lower) == len(upper)):
        raise OGSAUnresolvedError("OGSA OBL bounds are dimensionally inconsistent")
    return tuple(low + high - value for value, low, high in zip(position, lower, upper))


def masses(fitness: Sequence[float]) -> Tuple[float, ...]:
    if not fitness:
        raise OGSAUnresolvedError("OGSA fitness population is empty")
    best = min(fitness)
    worst = max(fitness)
    denominator = best - worst
    if denominator == 0:
        return tuple(1.0 / len(fitness) for _ in fitness)
    raw = tuple((value - worst) / denominator for value in fitness)
    total = sum(raw)
    if total == 0:
        raise OGSAUnresolvedError("OGSA mass normalization has zero total mass")
    return tuple(value / total for value in raw)


def gravitational_constant(g0: float, iteration: int, maximum_iterations: int) -> float:
    if maximum_iterations <= 0:
        raise OGSAUnresolvedError("OGSA maximum iterations are unresolved")
    return g0 * (1 - iteration / maximum_iterations)


def acceleration(
    agent_index: int,
    agents: Sequence[OgsaAgent],
    mass_values: Sequence[float],
    g_value: float,
    epsilon: float,
    gbest_indices: Sequence[int],
    random_value: float,
) -> Tuple[float, ...]:
    if epsilon <= 0 or len(agents) != len(mass_values):
        raise OGSAUnresolvedError("OGSA acceleration inputs are incomplete")
    dimensions = len(agents[agent_index].position)
    result = [0.0] * dimensions
    for other_index in gbest_indices:
        if other_index == agent_index:
            continue
        distance = sqrt(sum(
            (agents[other_index].position[d] - agents[agent_index].position[d]) ** 2
            for d in range(dimensions)
        ))
        denominator = distance + epsilon
        for dimension in range(dimensions):
            result[dimension] += (
                random_value * g_value * mass_values[other_index]
                * (agents[other_index].position[dimension] - agents[agent_index].position[dimension])
                / denominator
            )
    return tuple(result)


def update_agent(agent: OgsaAgent, acceleration_values: Sequence[float], random_value: float) -> OgsaAgent:
    if len(agent.position) != len(agent.velocity) or len(agent.position) != len(acceleration_values):
        raise OGSAUnresolvedError("OGSA agent dimensions are inconsistent")
    velocity = tuple(random_value * value + acceleration_values[index] for index, value in enumerate(agent.velocity))
    position = tuple(value + velocity[index] for index, value in enumerate(agent.position))
    return OgsaAgent(position, velocity)


@dataclass(frozen=True)
class OgsaRequest:
    assignment: Optional[OgsaAssignment] = None
    objective_context: Optional[OgsaObjectiveContext] = None
    weights: Optional[OgsaWeights] = None
    config: OgsaConfig = OgsaConfig()
    file_id: Optional[str] = None
    rng: Optional[Random] = None
    operation: str = "placement"


def repair_assignment(
    matrix: AssignmentMatrix,
    file_sizes: Sequence[float],
    capacities: Sequence[float],
) -> AssignmentMatrix:
    """Deterministically repair binary rows and capacity overflow."""
    repaired = [list(row) for row in matrix]
    usage = [0.0] * len(capacities)
    for file_index, row in enumerate(repaired):
        assigned = [index for index, value in enumerate(row) if value]
        if not assigned:
            assigned = [min(range(len(capacities)), key=lambda index: (usage[index], index))]
            row[assigned[0]] = 1
        for node_index in assigned:
            usage[node_index] += file_sizes[file_index]
    for file_index, row in enumerate(repaired):
        for node_index, value in enumerate(row):
            if not value or usage[node_index] <= capacities[node_index]:
                continue
            row[node_index] = 0
            usage[node_index] -= file_sizes[file_index]
            if not any(row):
                replacement = min(range(len(capacities)), key=lambda index: (usage[index], index))
                row[replacement] = 1
                usage[replacement] += file_sizes[file_index]
    repaired_tuple = tuple(tuple(int(value) for value in row) for row in repaired)
    validate_assignment(OgsaAssignment(repaired_tuple, tuple(file_sizes), tuple(capacities)))
    return repaired_tuple


def position_to_assignment(
    position: Sequence[float],
    file_count: int,
    node_count: int,
    file_sizes: Sequence[float],
    capacities: Sequence[float],
) -> AssignmentMatrix:
    matrix = tuple(
        tuple(1 if position[file_index * node_count + node_index] >= 0.5 else 0 for node_index in range(node_count))
        for file_index in range(file_count)
    )
    return repair_assignment(matrix, file_sizes, capacities)


def _random_agent(rng: Random, dimensions: int, config: OgsaConfig) -> OgsaAgent:
    position = tuple(rng.uniform(config.lower_bound, config.upper_bound) for _ in range(dimensions))
    velocity = tuple(rng.uniform(-1.0, 1.0) for _ in range(dimensions))
    return OgsaAgent(position, velocity)


def optimize(
    assignment: OgsaAssignment,
    context: OgsaObjectiveContext,
    weights: OgsaWeights,
    config: OgsaConfig,
    rng: Random,
) -> AssignmentMatrix:
    dimensions = len(assignment.matrix) * len(assignment.node_capacities)
    agents = tuple(_random_agent(rng, dimensions, config) for _ in range(config.population_size))

    def evaluate(agent: OgsaAgent) -> Tuple[float, AssignmentMatrix]:
        candidate = position_to_assignment(
            agent.position,
            len(assignment.matrix),
            len(assignment.node_capacities),
            assignment.file_sizes,
            assignment.node_capacities,
        )
        return mof(objective_vector(OgsaAssignment(candidate, assignment.file_sizes, assignment.node_capacities), context), weights), candidate

    best_fitness, best_assignment = evaluate(agents[0])
    for agent in agents[1:]:
        fitness, candidate = evaluate(agent)
        if fitness < best_fitness:
            best_fitness, best_assignment = fitness, candidate
    for iteration in range(config.generations):
        fitnesses = tuple(evaluate(agent)[0] for agent in agents)
        mass_values = masses(fitnesses)
        g_value = gravitational_constant(config.g0, iteration, max(1, config.generations))
        ordered = sorted(range(len(agents)), key=lambda index: (fitnesses[index], index))
        gbest_indices = ordered[:max(1, int(len(agents) * 0.02))]
        updated = []
        for index, agent in enumerate(agents):
            accel = acceleration(index, agents, mass_values, g_value, config.epsilon, gbest_indices, rng.random())
            updated.append(update_agent(agent, accel, rng.random()))
        agents = tuple(updated)
        opposite = tuple(
            OgsaAgent(opposite_position(agent.position, (config.lower_bound,) * dimensions, (config.upper_bound,) * dimensions), agent.velocity)
            for agent in agents
        )
        candidates = agents + opposite
        for agent in candidates:
            fitness, candidate = evaluate(agent)
            if fitness < best_fitness:
                best_fitness, best_assignment = fitness, candidate
        agents = tuple(sorted(candidates, key=lambda agent: (evaluate(agent)[0], agent.position))[:config.population_size])
    return best_assignment


class OGSAAdapter(SimulationAdapter):
    method_id = "OGSA"

    def __init__(self, request: OgsaRequest) -> None:
        self.request = request

    @property
    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities((DecisionKind.PLACEMENT, DecisionKind.UNRESOLVED))

    def compute(self, snapshot: AdapterSnapshot) -> DecisionEnvelope:
        try:
            if self.request.operation != "placement":
                return DecisionEnvelope.no_op("OGSA supports placement only")
            if self.request.assignment is None or self.request.objective_context is None:
                raise OGSAUnresolvedError("OGSA assignment/objective context is unresolved")
            validate_assignment(self.request.assignment)
            weights = self.request.weights or OgsaWeights.source_reported_equal()
            rng = self.request.rng or self.request.config.rng or Random(0)
            final_assignment = optimize(self.request.assignment, self.request.objective_context, weights, self.request.config, rng)
            if self.request.file_id is None:
                raise OGSAUnresolvedError("OGSA placement requires a file_id for common runtime translation")
            file_index = 0
            node_ids = tuple(
                node_id for node_index, node_id in enumerate(sorted(snapshot.scenario.get("nodes", {})))
                if final_assignment[file_index][node_index]
            )
            if not node_ids:
                raise OGSAUnresolvedError("OGSA final assignment has no executable node")
            return DecisionEnvelope(
                DecisionKind.PLACEMENT,
                DecisionStatus.ACCEPTED,
                (("file_id", self.request.file_id), ("placement_node_ids", node_ids), ("assignment_matrix", final_assignment)),
                provenance=(("method_id", self.method_id), ("scenario_id", snapshot.scenario_id)),
            )
        except OGSAUnresolvedError as error:
            return DecisionEnvelope.unresolved(DecisionKind.UNRESOLVED, str(error))

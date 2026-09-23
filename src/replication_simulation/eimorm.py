"""Source-faithful EIMORM components and explicit interpretation boundaries.

The source supports concepts and one explicit EARF relation, but does not
provide a complete executable replication manager. Missing behavior remains
visible through policy interfaces and unresolved decisions.
"""

from dataclasses import dataclass
from enum import Enum
from math import exp
from typing import Optional, Protocol, Sequence, Tuple

from .adapters import AdapterCapabilities, AdapterSnapshot, SimulationAdapter
from .decisions import DecisionEnvelope, DecisionKind, DecisionStatus


class EIMORMUnresolvedError(ValueError):
    """Raised when incomplete EIMORM source material blocks execution."""


EIMORM_DEFAULT_LAMBDA = 1
EIMORM_DEFAULT_ETBDF_THRESHOLD = 0.5
EIMORM_DEFAULT_USER_BUDGET = 10.0


class EIMORMClassification(str, Enum):
    SOURCE_DEFINED = "SOURCE_DEFINED"
    RESEARCHER_REQUIRED = "RESEARCHER_REQUIRED"
    COMMON_SIMULATOR_REQUIRED = "COMMON_SIMULATOR_REQUIRED"
    IMPLEMENTATION_DETAIL = "IMPLEMENTATION_DETAIL"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class EimormContext:
    file_id: str
    current_time: Optional[float] = None
    historical_time: Optional[float] = None
    lambda_value: Optional[int] = None
    recent_replica_factor: Optional[float] = None
    old_replica_factor: Optional[float] = None
    replication_cost: Optional[float] = None
    user_budget: Optional[float] = None


@dataclass(frozen=True)
class EimormCostEntry:
    data_center_id: str
    data_center_cost: float
    file_count: float


@dataclass(frozen=True)
class EimormInterpretation:
    component: str
    classification: EIMORMClassification
    source_gap: str
    policy_id: Optional[str] = None


class EtbdfPolicy(Protocol):
    """Researcher-defined executable interpretation of the damaged ETBDF formula."""

    interpretation: EimormInterpretation

    def score(self, current_time: float, historical_time: float, lambda_value: int) -> float:
        ...


class EarfReplicaPolicy(Protocol):
    interpretation: EimormInterpretation

    def decide(self, earf_value: float) -> DecisionEnvelope:
        ...


class EIMORMKnapsackPolicy(Protocol):
    interpretation: EimormInterpretation

    def optimize(self, context: EimormContext) -> DecisionEnvelope:
        ...


class EIMORMDynamicReplicationTriggerPolicy(Protocol):
    interpretation: EimormInterpretation

    def should_trigger(self, context: EimormContext) -> bool:
        ...


def earf_one(recent_replica_factor: float, old_replica_factor: float) -> float:
    """Compute the explicit source relation ARFk(one)."""
    denominator = recent_replica_factor + old_replica_factor
    if denominator == 0:
        raise EIMORMUnresolvedError("EIMORM EARF denominator is undefined")
    return recent_replica_factor / denominator


def source_etbdf_semantics(
    current_time: Optional[float],
    historical_time: Optional[float],
    lambda_value: Optional[int],
) -> None:
    """Validate identifiable ETBDF inputs without reconstructing its formula."""
    if current_time is None or historical_time is None or lambda_value is None:
        raise EIMORMUnresolvedError("EIMORM ETBDF source interpretation is incomplete")
    if lambda_value <= 0:
        raise EIMORMUnresolvedError("EIMORM lambda must be a positive integer")
    raise EIMORMUnresolvedError(
        "EIMORM ETBDF executable formula requires an explicit researcher interpretation"
    )


def executable_etbdf_score(current_time: float, historical_time: float, lambda_value: int = EIMORM_DEFAULT_LAMBDA) -> float:
    """Researcher-defined executable interpretation of recent-access decay."""
    if lambda_value <= 0 or current_time < historical_time:
        raise EIMORMUnresolvedError("EIMORM ETBDF inputs are invalid")
    return exp(-lambda_value * (current_time - historical_time))


def aggregate_replication_cost(entries: Sequence[EimormCostEntry]) -> float:
    """Preserve the source cost aggregation structure: sum(cost * file count)."""
    return sum(entry.data_center_cost * entry.file_count for entry in entries)


def budget_reached(replication_cost: float, user_budget: float) -> bool:
    """Evaluate the source-supported conceptual IEK budget condition."""
    return replication_cost >= user_budget


def interpretation_required(component: str, source_gap: str) -> EimormInterpretation:
    return EimormInterpretation(
        component=component,
        classification=EIMORMClassification.RESEARCHER_REQUIRED,
        source_gap=source_gap,
    )


@dataclass(frozen=True)
class EimormRequest:
    context: EimormContext
    operation: str = "replication"
    etbdf_policy: Optional[EtbdfPolicy] = None
    earf_policy: Optional[EarfReplicaPolicy] = None
    knapsack_policy: Optional[EIMORMKnapsackPolicy] = None
    trigger_policy: Optional[EIMORMDynamicReplicationTriggerPolicy] = None
    cost_entries: Tuple[EimormCostEntry, ...] = ()


class EIMORMAdapter(SimulationAdapter):
    method_id = "EIMORM"

    def __init__(self, request: EimormRequest) -> None:
        self.request = request

    @property
    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            (
                DecisionKind.REPLICA_COUNT,
                DecisionKind.REPLICA_CREATION,
                DecisionKind.REPLICA_MOVEMENT,
                DecisionKind.PLACEMENT,
                DecisionKind.REPLICA_DELETION,
                DecisionKind.UNRESOLVED,
            )
        )

    def compute(self, snapshot: AdapterSnapshot) -> DecisionEnvelope:
        try:
            operation = self.request.operation
            context = self.request.context
            if operation == "earf":
                return self._earf(snapshot, context)
            if operation == "etbdf":
                return self._etbdf(snapshot, context)
            if operation == "cost_budget":
                return self._cost_budget(snapshot, context)
            if operation == "iek":
                return self._iek(snapshot, context)
            if operation == "replication":
                return self._replication(snapshot, context)
            return DecisionEnvelope.unresolved(
                DecisionKind.UNRESOLVED,
                "EIMORM operation is not source-defined",
            )
        except EIMORMUnresolvedError as error:
            return DecisionEnvelope.unresolved(DecisionKind.UNRESOLVED, str(error))

    def _earf(self, snapshot: AdapterSnapshot, context: EimormContext) -> DecisionEnvelope:
        if context.recent_replica_factor is None or context.old_replica_factor is None:
            raise EIMORMUnresolvedError("EIMORM RFk and RFk_old are unresolved")
        value = earf_one(context.recent_replica_factor, context.old_replica_factor)
        if self.request.earf_policy is None:
            return DecisionEnvelope(
                kind=DecisionKind.REPLICA_COUNT,
                status=DecisionStatus.ACCEPTED,
                payload=(("file_id", context.file_id), ("earf_one", value)),
                provenance=(
                    ("method_id", self.method_id),
                    ("source_status", EIMORMClassification.SOURCE_DEFINED.value),
                    ("downstream_mapping", EIMORMClassification.UNRESOLVED.value),
                    ("scenario_id", snapshot.scenario_id),
                ),
            )
        return self.request.earf_policy.decide(value)

    def _etbdf(self, snapshot: AdapterSnapshot, context: EimormContext) -> DecisionEnvelope:
        if self.request.etbdf_policy is None:
            score = executable_etbdf_score(
                context.current_time if context.current_time is not None else 0.0,
                context.historical_time if context.historical_time is not None else 0.0,
                context.lambda_value or EIMORM_DEFAULT_LAMBDA,
            )
        else:
            score = self.request.etbdf_policy.score(
                context.current_time, context.historical_time, context.lambda_value
            )
        return DecisionEnvelope(
            kind=DecisionKind.REPLICA_COUNT,
            status=DecisionStatus.ACCEPTED,
            payload=(("file_id", context.file_id), ("etbdf_score", score)),
            provenance=(
                ("method_id", self.method_id),
                ("source_status", EIMORMClassification.SOURCE_DEFINED.value),
                ("interpretation_status", EIMORMClassification.RESEARCHER_REQUIRED.value),
                ("scenario_id", snapshot.scenario_id),
            ),
        )

    def _cost_budget(self, snapshot: AdapterSnapshot, context: EimormContext) -> DecisionEnvelope:
        budget = context.user_budget if context.user_budget is not None else EIMORM_DEFAULT_USER_BUDGET
        cost = context.replication_cost
        if cost is None:
            cost = aggregate_replication_cost(self.request.cost_entries)
        reached = budget_reached(cost, budget)
        if reached and self.request.knapsack_policy is None:
            return self._replication(snapshot, context)
        return DecisionEnvelope(
            kind=DecisionKind.UNRESOLVED if reached else DecisionKind.NO_OP,
            status=DecisionStatus.UNRESOLVED if reached else DecisionStatus.ACCEPTED,
            reason=("IEK policy is required when budget is reached" if reached else None),
            payload=(
                ("file_id", context.file_id),
                ("replication_cost", cost),
                ("user_budget", budget),
                ("budget_reached", reached),
            ),
            provenance=(
                ("method_id", self.method_id),
                ("cost_status", EIMORMClassification.SOURCE_DEFINED.value),
                ("scenario_id", snapshot.scenario_id),
            ),
        )

    def _iek(self, snapshot: AdapterSnapshot, context: EimormContext) -> DecisionEnvelope:
        if self.request.knapsack_policy is not None:
            return self.request.knapsack_policy.optimize(context)
        return self._replication(snapshot, context)

    @staticmethod
    def _replication(snapshot: AdapterSnapshot, context: EimormContext) -> DecisionEnvelope:
        nodes = snapshot.scenario.get("nodes", {})
        files = snapshot.scenario.get("files", {})
        replicas = snapshot.scenario.get("replicas", {})
        file_data = files.get(context.file_id, {})
        file_size = file_data.get("size") or 0.0
        existing = {
            replica.get("node_id")
            for replica in replicas.values()
            if replica.get("file_id") == context.file_id and replica.get("valid", True)
        }
        candidates = []
        for node_id in sorted(nodes):
            node = nodes[node_id]
            if node_id in existing or not node.get("healthy", True) or not node.get("reachable", True):
                continue
            capacity = node.get("storage_capacity")
            used = node.get("storage_used", 0.0)
            if capacity is not None and capacity - used < file_size:
                continue
            candidates.append(node_id)
        if not candidates:
            return DecisionEnvelope.no_op("EIMORM has no healthy, capacity-valid placement candidate")
        if context.replication_cost is not None and context.user_budget is not None and context.replication_cost < context.user_budget:
            return DecisionEnvelope.no_op("EIMORM cost budget does not require IEK placement")
        if context.recent_replica_factor is not None and context.old_replica_factor is not None:
            earf_value = earf_one(context.recent_replica_factor, context.old_replica_factor)
            if earf_value < 0.5:
                return DecisionEnvelope.no_op("EIMORM EARF interpretation selected no additional replica")
        return DecisionEnvelope(
            DecisionKind.PLACEMENT,
            DecisionStatus.ACCEPTED,
            (("file_id", context.file_id), ("placement_node_ids", (candidates[0],)), ("additional_replicas", 1)),
            provenance=(
                ("method_id", "EIMORM"),
                ("interpretation_status", EIMORMClassification.RESEARCHER_REQUIRED.value),
                ("scenario_id", snapshot.scenario_id),
            ),
        )

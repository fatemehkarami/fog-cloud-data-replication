"""Source-faithful DPRS placement components.

This module contains placement computation only. It does not create, delete,
move, or select runtime replicas.
"""

from dataclasses import dataclass
from math import inf
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .adapters import AdapterCapabilities, AdapterSnapshot, SimulationAdapter
from .decisions import DecisionEnvelope, DecisionKind, DecisionStatus


class DPRSUnresolvedError(ValueError):
    """Raised when a source-incomplete DPRS detail is required."""


DPRS_RESPONSE_TIME_THRESHOLD = 10.0


@dataclass(frozen=True)
class DprsNodeTiming:
    node_id: str
    arrival_rate: float
    service_rate: float
    disk_speed: float


@dataclass(frozen=True)
class DprsConnection:
    source_node_id: str
    target_node_id: str
    bandwidth: float
    coefficient: float


@dataclass(frozen=True)
class DprsDataset:
    dataset_id: str
    size: float
    usage_frequency: Optional[float] = None
    time_span: Optional[float] = None


@dataclass(frozen=True)
class DprsRequest:
    dataset: DprsDataset
    node_timings: Tuple[DprsNodeTiming, ...]
    connections: Tuple[DprsConnection, ...]
    disk_coefficient: float
    transfer_coefficient: float
    existing_replica_node_ids: Tuple[str, ...] = ()
    response_time_threshold: float = DPRS_RESPONSE_TIME_THRESHOLD

    @property
    def timing_by_node(self) -> Dict[str, DprsNodeTiming]:
        return {timing.node_id: timing for timing in self.node_timings}

    @property
    def node_ids(self) -> Tuple[str, ...]:
        ids = {timing.node_id for timing in self.node_timings}
        for connection in self.connections:
            ids.add(connection.source_node_id)
            ids.add(connection.target_node_id)
        return tuple(sorted(ids))


@dataclass(frozen=True)
class DprsEdge:
    source: str
    target: str
    weight: float

    def key(self) -> Tuple[str, str]:
        return tuple(sorted((self.source, self.target)))


@dataclass(frozen=True)
class DprsVertex:
    vertex_id: str
    real_id: str
    virtual: bool = False


@dataclass(frozen=True)
class DprsGraph:
    vertices: Tuple[DprsVertex, ...]
    edges: Tuple[DprsEdge, ...]

    @property
    def vertex_ids(self) -> Set[str]:
        return {vertex.vertex_id for vertex in self.vertices}


@dataclass(frozen=True)
class KruskalResult:
    edges: Tuple[DprsEdge, ...]
    had_equal_weight_tie: bool


def wait_access_latency(arrival_rate: float, service_rate: float) -> float:
    """Preserve the printed DPRS equation: Tw = rho / (lambda - mu)."""
    if service_rate == 0 or arrival_rate == service_rate:
        raise DPRSUnresolvedError("DPRS wait-latency equation is undefined for these rates")
    traffic_intensity = arrival_rate / service_rate
    return traffic_intensity / (arrival_rate - service_rate)


def write_read_time(dataset_size: float, disk_speed: float, coefficient: float) -> float:
    if disk_speed == 0:
        raise DPRSUnresolvedError("DPRS write/read time requires non-zero disk speed")
    return (dataset_size / disk_speed) * coefficient


def transfer_time(dataset_size: float, bandwidth: float, coefficient: float) -> float:
    if bandwidth <= 0:
        raise DPRSUnresolvedError("DPRS transfer time requires positive bandwidth")
    return (dataset_size / bandwidth) * coefficient


def response_time_components(
    dataset_size: float,
    arrival_rate: float,
    service_rate: float,
    disk_speed: float,
    disk_coefficient: float,
    bandwidth: float,
    transfer_coefficient: float,
) -> Tuple[float, float, float, float]:
    wait = wait_access_latency(arrival_rate, service_rate)
    read_write = write_read_time(dataset_size, disk_speed, disk_coefficient)
    transfer = transfer_time(dataset_size, bandwidth, transfer_coefficient)
    return wait, read_write, transfer, wait + read_write + transfer


def aggregate_response_time(response_times: Sequence[float]) -> float:
    """Use the arithmetic mean for a deterministic placement decision summary."""
    if not response_times:
        raise DPRSUnresolvedError("DPRS response-time aggregation has no observations")
    return sum(response_times) / len(response_times)


def transform_edge_weight(
    edge_weight: float,
    source_timing: DprsNodeTiming,
    target_timing: DprsNodeTiming,
    source_degree: int,
    target_degree: int,
    dataset_size: float,
    disk_coefficient: float,
) -> float:
    """Move source vertex costs to an adjacent edge as printed by DPRS."""
    if source_degree == 0 or target_degree == 0:
        raise DPRSUnresolvedError("DPRS edge transformation requires non-zero endpoint degrees")
    source_cost = (
        wait_access_latency(source_timing.arrival_rate, source_timing.service_rate)
        + write_read_time(dataset_size, source_timing.disk_speed, disk_coefficient)
    ) / source_degree
    target_cost = (
        wait_access_latency(target_timing.arrival_rate, target_timing.service_rate)
        + write_read_time(dataset_size, target_timing.disk_speed, disk_coefficient)
    ) / target_degree
    return edge_weight + source_cost + target_cost


def build_transformed_graph(request: DprsRequest) -> DprsGraph:
    node_ids = request.node_ids
    degrees = {node_id: 0 for node_id in node_ids}
    for connection in request.connections:
        degrees[connection.source_node_id] += 1
        degrees[connection.target_node_id] += 1
    timings = request.timing_by_node
    edges = []
    for connection in request.connections:
        source = timings.get(connection.source_node_id)
        target = timings.get(connection.target_node_id)
        if source is None or target is None:
            raise DPRSUnresolvedError("DPRS timing is missing for a graph endpoint")
        base = transfer_time(request.dataset.size, connection.bandwidth, connection.coefficient)
        edges.append(
            DprsEdge(
                connection.source_node_id,
                connection.target_node_id,
                transform_edge_weight(
                    base,
                    source,
                    target,
                    degrees[connection.source_node_id],
                    degrees[connection.target_node_id],
                    request.dataset.size,
                    request.disk_coefficient,
                ),
            )
        )
    vertices = tuple(DprsVertex(node_id, node_id) for node_id in node_ids)
    return DprsGraph(vertices, tuple(edges))


def _adjacency(graph: DprsGraph, edges: Sequence[DprsEdge]) -> Dict[str, List[DprsEdge]]:
    adjacency = {vertex.vertex_id: [] for vertex in graph.vertices}
    for edge in edges:
        adjacency[edge.source].append(edge)
        adjacency[edge.target].append(edge)
    return adjacency


def shortest_path_weight(graph: DprsGraph, source: str, target: str) -> float:
    distances = {vertex.vertex_id: inf for vertex in graph.vertices}
    distances[source] = 0.0
    unvisited = set(distances)
    while unvisited:
        current = min(unvisited, key=lambda vertex_id: (distances[vertex_id], vertex_id))
        unvisited.remove(current)
        if current == target:
            return distances[current]
        if distances[current] == inf:
            break
        for edge in _adjacency(graph, graph.edges)[current]:
            neighbor = edge.target if edge.source == current else edge.source
            candidate = distances[current] + edge.weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
    return inf


def build_auxiliary_graph(graph: DprsGraph, request: DprsRequest) -> DprsGraph:
    """Create real and virtual vertices and source-described real-to-virtual edges."""
    real_vertices = tuple(DprsVertex(vertex.vertex_id, vertex.real_id) for vertex in graph.vertices)
    virtual_vertices = tuple(
        DprsVertex(vertex.vertex_id + "'", vertex.real_id, virtual=True)
        for vertex in graph.vertices
    )
    auxiliary_edges: List[DprsEdge] = []
    for real in real_vertices:
        for virtual in virtual_vertices:
            weight = shortest_path_weight(graph, real.vertex_id, virtual.real_id)
            if weight != inf:
                auxiliary_edges.append(DprsEdge(real.vertex_id, virtual.vertex_id, weight))
    return DprsGraph(real_vertices + virtual_vertices, tuple(auxiliary_edges))


def kruskal(graph: DprsGraph) -> KruskalResult:
    parent = {vertex.vertex_id: vertex.vertex_id for vertex in graph.vertices}
    rank = {vertex.vertex_id: 0 for vertex in graph.vertices}
    ordered = sorted(graph.edges, key=lambda edge: (edge.weight, edge.key()))
    had_tie = False

    def find(vertex_id: str) -> str:
        while parent[vertex_id] != vertex_id:
            parent[vertex_id] = parent[parent[vertex_id]]
            vertex_id = parent[vertex_id]
        return vertex_id

    selected: List[DprsEdge] = []
    for edge in ordered:
        left = find(edge.source)
        right = find(edge.target)
        if left == right:
            continue
        if any(
            selected_edge.weight == edge.weight
            and set((selected_edge.source, selected_edge.target))
            & set((edge.source, edge.target))
            for selected_edge in selected
        ):
            had_tie = True
        if rank[left] < rank[right]:
            left, right = right, left
        parent[right] = left
        if rank[left] == rank[right]:
            rank[left] += 1
        selected.append(edge)
    return KruskalResult(tuple(selected), had_tie)


def prune_auxiliary_tree(graph: DprsGraph, tree: KruskalResult) -> Tuple[Set[str], bool]:
    """Apply the source-described virtual and redundant edge pruning order."""
    edges = list(tree.edges)
    unresolved_tie = False
    virtual_ids = {vertex.vertex_id for vertex in graph.vertices if vertex.virtual}

    def degree(vertex_id: str) -> int:
        return sum(vertex_id in (edge.source, edge.target) for edge in edges)

    for virtual_id in sorted(virtual_ids):
        if degree(virtual_id) == 1:
            edges = [edge for edge in edges if virtual_id not in (edge.source, edge.target)]

    surviving_virtual = {
        vertex_id for vertex_id in virtual_ids if any(vertex_id in (edge.source, edge.target) for edge in edges)
    }
    for virtual_id in sorted(surviving_virtual):
        real_id = virtual_id[:-1]
        edges = [edge for edge in edges if real_id not in (edge.source, edge.target)]

    for real_id in sorted({vertex.real_id for vertex in graph.vertices if not vertex.virtual}):
        candidates = [edge for edge in edges if edge.source == real_id or edge.target == real_id]
        by_virtual: Dict[str, DprsEdge] = {}
        for edge in candidates:
            other = edge.target if edge.source == real_id else edge.source
            if other not in virtual_ids:
                continue
            previous = by_virtual.get(other)
            if previous is None or edge.weight < previous.weight:
                by_virtual[other] = edge
        keep = set(id(edge) for edge in by_virtual.values())
        edges = [edge for edge in edges if edge not in candidates or id(edge) in keep]

    return {virtual_id[:-1] for virtual_id in surviving_virtual}, unresolved_tie


class DPRSAdapter(SimulationAdapter):
    method_id = "DPRS"

    def __init__(self, request: DprsRequest) -> None:
        self.request = request

    @property
    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities((DecisionKind.PLACEMENT,))

    def compute(self, snapshot: AdapterSnapshot) -> DecisionEnvelope:
        try:
            transformed = build_transformed_graph(self.request)
            auxiliary = build_auxiliary_graph(transformed, self.request)
            tree = kruskal(auxiliary)
            selected, _ = prune_auxiliary_tree(auxiliary, tree)
            nodes = snapshot.scenario.get("nodes", {})
            files = snapshot.scenario.get("files", {})
            replicas = snapshot.scenario.get("replicas", {})
            existing = set(self.request.existing_replica_node_ids)
            existing.update(
                replica.get("node_id")
                for replica in replicas.values()
                if replica.get("file_id") == self.request.dataset.dataset_id and replica.get("valid", True)
            )
            file_size = files.get(self.request.dataset.dataset_id, {}).get("size", self.request.dataset.size)
            placement_nodes = []
            for node_id in sorted(selected):
                node = nodes.get(node_id)
                if node is None or node_id in existing or not node.get("healthy", True) or not node.get("reachable", True):
                    continue
                capacity = node.get("storage_capacity")
                used = node.get("storage_used", 0.0)
                if capacity is not None and capacity - used < file_size:
                    continue
                placement_nodes.append(node_id)
            if not placement_nodes:
                raise DPRSUnresolvedError("DPRS produced no executable placement node")
            payload = (
                ("dataset_id", self.request.dataset.dataset_id),
                ("file_id", self.request.dataset.dataset_id),
                ("placement_node_ids", tuple(placement_nodes)),
                ("response_time_threshold", self.request.response_time_threshold),
            )
            return DecisionEnvelope(
                kind=DecisionKind.PLACEMENT,
                status=DecisionStatus.ACCEPTED,
                payload=payload,
                provenance=(("method_id", self.method_id), ("scenario_id", snapshot.scenario_id)),
            )
        except DPRSUnresolvedError as error:
            return DecisionEnvelope.unresolved(DecisionKind.PLACEMENT, str(error))

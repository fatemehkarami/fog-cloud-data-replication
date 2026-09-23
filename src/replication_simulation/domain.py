"""Algorithm-neutral simulation domain entities."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple


@dataclass
class Site:
    site_id: str
    node_ids: Tuple[str, ...] = ()


@dataclass
class VM:
    vm_id: str
    node_id: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Node:
    node_id: str
    site_id: str
    healthy: bool = True
    reachable: bool = True
    storage_capacity: Optional[float] = None
    storage_used: float = 0.0
    vm_ids: Tuple[str, ...] = ()

    @property
    def available_storage(self) -> Optional[float]:
        if self.storage_capacity is None:
            return None
        return self.storage_capacity - self.storage_used


@dataclass
class File:
    file_id: str
    size: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Replica:
    replica_id: str
    file_id: str
    node_id: str
    valid: bool = True
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class User:
    user_id: str
    site_id: Optional[str] = None


@dataclass
class Task:
    task_id: str
    request_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Request:
    request_id: str
    user_id: str
    file_id: str
    arrival_time: float
    task_ids: Tuple[str, ...] = ()
    attributes: Dict[str, Any] = field(default_factory=dict)
    sequence: Optional[int] = None
    operation: str = "read"
    source_site_id: Optional[str] = None
    source_node_id: Optional[str] = None


@dataclass
class NetworkLink:
    link_id: str
    source_node_id: str
    target_node_id: str
    bandwidth: Optional[float] = None
    latency: Optional[float] = None
    available: bool = True


@dataclass(frozen=True)
class MetricRecord:
    metric_id: str
    name: str
    value: Any
    timestamp: Optional[float] = None
    metadata: Tuple[Tuple[str, Any], ...] = ()


@dataclass
class Scenario:
    scenario_id: str
    sites: Dict[str, Site] = field(default_factory=dict)
    nodes: Dict[str, Node] = field(default_factory=dict)
    vms: Dict[str, VM] = field(default_factory=dict)
    files: Dict[str, File] = field(default_factory=dict)
    replicas: Dict[str, Replica] = field(default_factory=dict)
    users: Dict[str, User] = field(default_factory=dict)
    requests: Dict[str, Request] = field(default_factory=dict)
    tasks: Dict[str, Task] = field(default_factory=dict)
    network_links: Dict[str, NetworkLink] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Experiment:
    experiment_id: str
    scenarios: Dict[str, Scenario] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

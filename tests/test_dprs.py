import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from replication_simulation import (
    AdapterSnapshot,
    DPRSAdapter,
    DprsConnection,
    DprsDataset,
    DprsGraph,
    DprsNodeTiming,
    DprsRequest,
    DprsVertex,
    DecisionKind,
    DecisionStatus,
    Event,
    File,
    Node,
    Scenario,
    SimulationState,
    Site,
    kruskal,
    prune_auxiliary_tree,
    response_time_components,
    aggregate_response_time,
    transform_edge_weight,
)
from replication_simulation.dprs import DprsEdge, DPRSUnresolvedError


class DPRSFoundationTests(unittest.TestCase):
    def request(self):
        return DprsRequest(
            dataset=DprsDataset("dataset-1", 100.0),
            node_timings=(
                DprsNodeTiming("node-1", 1.0, 2.0, 10.0),
                DprsNodeTiming("node-2", 1.0, 2.0, 20.0),
            ),
            connections=(DprsConnection("node-1", "node-2", 50.0, 1.0),),
            disk_coefficient=2.0,
            transfer_coefficient=3.0,
        )

    def test_response_time_preserves_printed_formula_structure(self):
        wait, read_write, transfer, total = response_time_components(
            dataset_size=100.0,
            arrival_rate=1.0,
            service_rate=2.0,
            disk_speed=10.0,
            disk_coefficient=2.0,
            bandwidth=50.0,
            transfer_coefficient=3.0,
        )
        self.assertEqual(wait, -0.5)
        self.assertEqual(read_write, 20.0)
        self.assertEqual(transfer, 6.0)
        self.assertEqual(total, wait + read_write + transfer)

    def test_undefined_wait_input_is_explicit(self):
        with self.assertRaises(DPRSUnresolvedError):
            response_time_components(100.0, 1.0, 1.0, 10.0, 2.0, 50.0, 3.0)

    def test_response_time_aggregation_is_deterministic(self):
        self.assertEqual(aggregate_response_time((2.0, 4.0, 6.0)), 4.0)

    def test_edge_transformation_uses_endpoint_degrees(self):
        source = DprsNodeTiming("node-1", 1.0, 2.0, 10.0)
        target = DprsNodeTiming("node-2", 1.0, 2.0, 20.0)
        result = transform_edge_weight(6.0, source, target, 1, 1, 100.0, 2.0)
        self.assertEqual(result, 35.0)

    def test_kruskal_prevents_cycles(self):
        graph = DprsGraph(
            vertices=tuple(DprsVertex(vertex_id, vertex_id) for vertex_id in ("a", "b", "c")),
            edges=(
                DprsEdge("a", "b", 1.0),
                DprsEdge("b", "c", 2.0),
                DprsEdge("a", "c", 3.0),
            ),
        )
        result = kruskal(graph)
        self.assertEqual(len(result.edges), 2)
        self.assertFalse(result.had_equal_weight_tie)

    def test_pruning_removes_degree_one_virtual_and_returns_survivors(self):
        graph = DprsGraph(
            vertices=(
                DprsVertex("a", "a"),
                DprsVertex("b", "b"),
                DprsVertex("a'", "a", True),
                DprsVertex("b'", "b", True),
            ),
            edges=(),
        )
        tree = type("Tree", (), {
            "edges": (DprsEdge("a", "a'", 1.0), DprsEdge("a", "b'", 2.0), DprsEdge("b", "b'", 1.0)),
            "had_equal_weight_tie": False,
        })()
        selected, unresolved = prune_auxiliary_tree(graph, tree)
        self.assertEqual(selected, {"b"})
        self.assertFalse(unresolved)

    def test_adapter_returns_placement_without_mutating_snapshot_state(self):
        scenario = Scenario(
            scenario_id="scenario-1",
            sites={"site-1": Site("site-1", ("node-1", "node-2"))},
            nodes={
                "node-1": Node("node-1", "site-1"),
                "node-2": Node("node-2", "site-1"),
            },
            files={"dataset-1": File("dataset-1", 100.0)},
        )
        state = SimulationState(scenario)
        snapshot = AdapterSnapshot.from_state(state, run_id="run-1")
        before = state.scenario.nodes["node-1"].storage_used
        result = DPRSAdapter(self.request()).compute(snapshot)
        self.assertEqual(result.kind, DecisionKind.PLACEMENT)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)
        self.assertTrue(dict(result.payload)["placement_node_ids"])
        self.assertEqual(state.scenario.nodes["node-1"].storage_used, before)
        self.assertEqual(result.provenance[0], ("method_id", "DPRS"))

    def test_adapter_capability_is_placement_only(self):
        adapter = DPRSAdapter(self.request())
        self.assertEqual(adapter.capabilities.decisions, (DecisionKind.PLACEMENT,))


if __name__ == "__main__":
    unittest.main()

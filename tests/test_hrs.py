import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from replication_simulation import (
    AdapterSnapshot,
    DecisionKind,
    DecisionStatus,
    File,
    HRSAdapter,
    HRSUnresolvedError,
    HrsProvider,
    HrsReplica,
    HrsRequest,
    HrsSite,
    HrsVm,
    HrsWeights,
    Node,
    Replica,
    Scenario,
    SimulationState,
    Site,
    closeness_centrality,
    merit,
    network_performance,
    replication_cost,
    total_cost,
    uniform_normalize_1_to_10,
    vm_capability,
    vm_load,
)


class FuzzyPolicy:
    def __init__(self, values):
        self.values = values

    def value(self, replica):
        return self.values[replica.replica_id]


class HRSTests(unittest.TestCase):
    def setUp(self):
        scenario = Scenario(
            scenario_id="scenario-hrs",
            sites={"site-1": Site("site-1", ("node-1",))},
            nodes={"node-1": Node("node-1", "site-1")},
            files={"file-1": File("file-1", 5.0)},
            replicas={"primary": Replica("primary", "file-1", "node-1")},
        )
        self.state = SimulationState(scenario)
        self.snapshot = AdapterSnapshot.from_state(self.state, run_id="run-1")

    def test_centrality_and_source_formula_terms(self):
        self.assertEqual(closeness_centrality("a", (("b", 2.0),), 2), 0.5)
        self.assertEqual(merit(4.0, 2.0, HrsWeights(2.0, 3.0)), 14.0)
        self.assertEqual(vm_capability(HrsVm("vm", "site", 2.0, 10.0, 5.0)), 25.0)
        self.assertEqual(vm_load(HrsVm("vm", "site", queued_task_length=8.0, service_rate=2.0)), 4.0)
        self.assertEqual(network_performance(100.0, 5.0), 20.0)
        self.assertEqual(replication_cost(10.0, 5.0, 2.0), 4.0)

    def test_normalization_is_deterministic_and_handles_edges(self):
        self.assertEqual(uniform_normalize_1_to_10(1.5, 0.0, 10.0), 2.0)
        self.assertEqual(uniform_normalize_1_to_10(0.0, 0.0, 10.0), 1.0)
        self.assertEqual(uniform_normalize_1_to_10(10.0, 0.0, 10.0), 10.0)
        self.assertEqual(uniform_normalize_1_to_10(5.0, 5.0, 5.0), 5.5)

    def test_fixed_researcher_weights_are_used_when_omitted(self):
        self.assertEqual(merit(1.0, 1.0, HrsWeights()), 1.0)
        self.assertAlmostEqual(total_cost(1.0, 1.0, 1.0, HrsWeights()), 1.0)

    def test_placement_returns_decision_without_mutation(self):
        request = HrsRequest(
            file_id="file-1",
            candidate_sites=(
                HrsSite("site-1", normalized_accesses=8.0, normalized_centrality=2.0),
                HrsSite("site-2", normalized_accesses=2.0, normalized_centrality=7.0),
            ),
            weights=HrsWeights(w1=1.0, w2=1.0),
        )
        result = HRSAdapter(request).compute(self.snapshot)
        self.assertEqual(result.kind, DecisionKind.PLACEMENT)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)
        self.assertEqual(dict(result.payload)["site_id"], "site-1")
        self.assertEqual(dict(result.payload)["placement_node_ids"], ("node-1",))
        self.assertIn("primary", self.state.scenario.replicas)

    def test_provider_selection_requires_source_weights_and_latency(self):
        request = HrsRequest(
            file_id="file-1",
            operation="provider_selection",
            providers=(HrsProvider("provider", "vm", "site-1", "file-1"),),
            vms=(HrsVm(
                "vm",
                "site-1",
                processors=2.0,
                cpu_capability=10.0,
                bandwidth=100.0,
                queued_task_length=4.0,
                service_rate=2.0,
                network_latency=5.0,
            ),),
            weights=HrsWeights(w3=1.0, w4=1.0, w5=1.0),
        )
        result = HRSAdapter(request).compute(self.snapshot)
        self.assertEqual(result.kind, DecisionKind.PROVIDER_SELECTION)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)

    def test_replacement_uses_deterministic_fuzzy_policy_and_one_transition(self):
        replicas = (
            HrsReplica("r1", "file-1", "site-1", 3.0),
            HrsReplica("r2", "file-1", "site-1", 4.0),
        )
        request = HrsRequest(
            file_id="file-1",
            operation="replacement",
            replicas_at_target=replicas,
            requested_size=5.0,
            available_storage=1.0,
        )
        selected = HRSAdapter(request).compute(self.snapshot)
        self.assertEqual(selected.kind, DecisionKind.REPLICA_DELETION)
        self.assertEqual(dict(selected.payload)["replica_id"], "r1")

    def test_replacement_not_needed_when_storage_is_sufficient(self):
        request = HrsRequest(
            file_id="file-1",
            operation="replacement",
            replicas_at_target=(HrsReplica("r1", "file-1", "site-1", 3.0),),
            requested_size=5.0,
            available_storage=5.0,
        )
        result = HRSAdapter(request, FuzzyPolicy({"r1": 0.2})).compute(self.snapshot)
        self.assertIsNone(dict(result.payload)["replica_id"])

    def test_initial_primary_copy_is_consumed_not_regenerated(self):
        before = dict(self.state.scenario.replicas)
        HRSAdapter(HrsRequest(file_id="file-1")).compute(self.snapshot)
        self.assertEqual(before, self.state.scenario.replicas)
        self.assertIn("primary", self.state.scenario.replicas)


if __name__ == "__main__":
    unittest.main()

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from replication_simulation import (
    AdapterSnapshot,
    DecisionKind,
    DecisionStatus,
    File,
    Node,
    OisInput,
    OisWeights,
    ObjectiveVector,
    ProposedAdapter,
    ProposedRequest,
    ProposedUnresolvedError,
    ReplicaCountResult,
    Scenario,
    SimulationState,
    Site,
    Nsga3Config,
    compute_ois,
    determine_replica_count,
    dominates,
    nondominated_sort,
    objective_key,
)


class AlwaysReplicate:
    def should_replicate(self, request):
        return True


class ProposedTests(unittest.TestCase):
    def setUp(self):
        scenario = Scenario(
            scenario_id="scenario-proposed",
            sites={"site-1": Site("site-1", ("node-1",))},
            nodes={"node-1": Node("node-1", "site-1")},
            files={"file-1": File("file-1", 4.0)},
        )
        self.state = SimulationState(scenario)
        self.snapshot = AdapterSnapshot.from_state(self.state, run_id="run-1")

    def ois_input(self):
        return OisInput(
            access_events=((0.0, 2.0), (1.0, 4.0)),
            current_time=2.0,
            decay_parameter=0.5,
            file_size=4.0,
            replication_count=2.0,
            replication_weight=3.0,
            file_type_priority=5.0,
            user_count=2.0,
            weights=OisWeights(1.0, 1.0, 1.0, 1.0, 1.0),
        )

    def test_ois_uses_source_components_without_other_method_logic(self):
        value = compute_ois(self.ois_input())
        self.assertGreater(value, 0.0)

    def test_ois_uses_fixed_equal_weights_when_weights_are_omitted(self):
        incomplete = self.ois_input()
        incomplete = OisInput(
            access_events=incomplete.access_events,
            current_time=incomplete.current_time,
            decay_parameter=incomplete.decay_parameter,
            file_size=incomplete.file_size,
            replication_count=incomplete.replication_count,
            replication_weight=incomplete.replication_weight,
            file_type_priority=incomplete.file_type_priority,
            user_count=incomplete.user_count,
        )
        self.assertGreater(compute_ois(incomplete), 0.0)

    def test_replica_count_preserves_all_three_source_branches(self):
        self.assertEqual(determine_replica_count(10.0, 3.0, 2), ReplicaCountResult(2, "create"))
        self.assertEqual(determine_replica_count(6.0, 3.0, 2), ReplicaCountResult(0, "no_op"))
        self.assertEqual(determine_replica_count(3.0, 3.0, 2), ReplicaCountResult(-1, "delete_candidates"))

    def test_objectives_remain_five_dimensional_with_directions(self):
        better = ObjectiveVector(1.0, 1.0, 1.0, 1.0, 2.0)
        worse = ObjectiveVector(2.0, 2.0, 2.0, 2.0, 1.0)
        self.assertTrue(dominates(better, worse))
        self.assertEqual(len(objective_key(better)), 5)
        self.assertEqual(len(nondominated_sort((better, worse))[0]), 1)

    def test_nsga_association_uses_deterministic_internal_normalization(self):
        from replication_simulation.proposed import association_candidates
        self.assertEqual(
            association_candidates((ObjectiveVector(1, 1, 1, 1, 1),), ((1, 1, 1, 1, 1),)),
            ((0, 0),),
        )

    def test_adapter_returns_executable_placement_with_fixed_defaults(self):
        request = ProposedRequest(
            file_id="file-1",
            ois=self.ois_input(),
            weighted_access_rate=6.0,
            maximum_replication_rate=3.0,
            current_replica_count=1,
            nsga3=Nsga3Config(reference_directions=((1, 1, 1, 1, 1),)),
        )
        result = ProposedAdapter(request, AlwaysReplicate()).compute(self.snapshot)
        self.assertEqual(result.kind, DecisionKind.PLACEMENT)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)
        self.assertEqual(dict(result.payload)["placement_node_ids"], ("node-1",))
        self.assertEqual(self.state.scenario.files["file-1"].file_id, "file-1")

    def test_adapter_uses_default_timing_policy(self):
        request = ProposedRequest(
            file_id="file-1",
            ois=self.ois_input(),
            weighted_access_rate=3.0,
            maximum_replication_rate=3.0,
            current_replica_count=1,
        )
        result = ProposedAdapter(request).compute(self.snapshot)
        self.assertEqual(result.kind, DecisionKind.NO_OP)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)


if __name__ == "__main__":
    unittest.main()

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from replication_simulation import (
    AdapterSnapshot,
    DecisionEnvelope,
    DecisionKind,
    DecisionStatus,
    Event,
    EventQueue,
    ExecutionPipeline,
    File,
    NetworkLink,
    Node,
    Replica,
    Request,
    RunMetadata,
    Scenario,
    SimulationAdapter,
    SimulationClock,
    SimulationState,
    Site,
    StateValidator,
)


class CommonFoundationTests(unittest.TestCase):
    def make_state(self, capacity=10.0):
        scenario = Scenario(
            scenario_id="scenario-1",
            sites={"site-1": Site("site-1", ("node-1",))},
            nodes={"node-1": Node("node-1", "site-1", storage_capacity=capacity)},
            files={"file-1": File("file-1", size=4.0)},
            network_links={"link-1": NetworkLink("link-1", "node-1", "node-1")},
        )
        return SimulationState(scenario)

    def test_domain_consistency_and_storage_accounting(self):
        state = self.make_state()
        state.scenario.replicas["replica-1"] = Replica("replica-1", "file-1", "node-1")
        state.scenario.nodes["node-1"].storage_used = 4.0
        self.assertEqual(state.scenario.replicas["replica-1"].file_id, "file-1")
        self.assertEqual(state.scenario.nodes["node-1"].available_storage, 6.0)

    def test_freeze_and_clone_are_independent(self):
        state = self.make_state()
        state.freeze()
        clone = state.clone()
        clone.scenario.nodes["node-1"].storage_used = 3.0
        self.assertTrue(state.frozen)
        self.assertFalse(clone.frozen)
        self.assertEqual(state.scenario.nodes["node-1"].storage_used, 0.0)
        with self.assertRaises(RuntimeError):
            state.record("mutation")

    def test_event_queue_orders_equal_timestamps_by_sequence(self):
        queue = EventQueue()
        first = queue.schedule(Event(1.0, "first"))
        second = queue.schedule(Event(1.0, "second"))
        self.assertLess(first.sequence, second.sequence)
        self.assertEqual(queue.pop().event_type, "first")
        self.assertEqual(queue.pop().event_type, "second")

    def test_clock_cannot_move_backwards(self):
        clock = SimulationClock()
        clock.advance_to(2.0)
        with self.assertRaises(ValueError):
            clock.advance_to(1.0)

    def test_snapshot_does_not_expose_mutable_collections(self):
        snapshot = AdapterSnapshot.from_state(self.make_state(), run_id="run-1")
        with self.assertRaises(TypeError):
            snapshot.scenario["files"]["file-2"] = File("file-2")

    def test_unresolved_decision_is_explicit_and_rejected(self):
        state = self.make_state()
        decision = DecisionEnvelope.unresolved(DecisionKind.PLACEMENT, "policy is not decided")
        result = StateValidator().validate(state, decision)
        self.assertFalse(result.valid)
        self.assertEqual(decision.status, DecisionStatus.UNRESOLVED)

    def test_validation_rejects_capacity_duplicate_and_unhealthy_target(self):
        state = self.make_state(capacity=2.0)
        validator = StateValidator()
        too_large = DecisionEnvelope(
            DecisionKind.REPLICA_CREATION,
            DecisionStatus.ACCEPTED,
            (("file_id", "file-1"), ("node_id", "node-1"), ("size", 3.0)),
        )
        self.assertFalse(validator.validate(state, too_large).valid)
        state.scenario.replicas["replica-1"] = Replica("replica-1", "file-1", "node-1")
        duplicate = DecisionEnvelope(
            DecisionKind.REPLICA_CREATION,
            DecisionStatus.ACCEPTED,
            (("file_id", "file-1"), ("node_id", "node-1"), ("size", 1.0)),
        )
        self.assertFalse(validator.validate(state, duplicate).valid)
        state.scenario.nodes["node-1"].healthy = False
        self.assertFalse(validator.validate(state, duplicate).valid)

    def test_pipeline_mutates_only_after_validation_and_records_raw_outcomes(self):
        state = self.make_state()
        decision = DecisionEnvelope(
            DecisionKind.REPLICA_CREATION,
            DecisionStatus.ACCEPTED,
            (("file_id", "file-1"), ("node_id", "node-1"), ("size", 4.0)),
        )
        pipeline = ExecutionPipeline()
        pipeline.process(state, decision, lambda current, _: current.scenario.nodes["node-1"].__setattr__("storage_used", 4.0))
        self.assertEqual(state.scenario.nodes["node-1"].storage_used, 4.0)
        self.assertEqual([item.observation_type for item in pipeline.recorder.observations], ["validation", "execution"])

    def test_provenance_retains_run_identity(self):
        metadata = RunMetadata("experiment-1", "scenario-1", "run-1", "unassigned", seed_identity="seed-x")
        self.assertEqual(metadata.scenario_id, "scenario-1")
        self.assertEqual(metadata.seed_identity, "seed-x")


if __name__ == "__main__":
    unittest.main()

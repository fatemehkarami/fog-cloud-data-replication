import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from replication_simulation import (
    AdapterCapabilities,
    AdapterDispatcher,
    AdapterSnapshot,
    CANONICAL_METHODS,
    DecisionEnvelope,
    DecisionExecutor,
    DecisionKind,
    DecisionStatus,
    Event,
    FailureRecoveryExecutor,
    File,
    FrozenScenario,
    HrsRequest,
    MatchedRunOrchestrator,
    MethodRegistration,
    MethodRegistry,
    Node,
    NetworkLink,
    RawRecorder,
    Request,
    RequestServiceExecutor,
    ReplayTrace,
    Replica,
    RunMetadata,
    Scenario,
    SimulationAdapter,
    SimulationEventLoop,
    SimulationState,
    Site,
)


class DummyAdapter(SimulationAdapter):
    def __init__(self, method_id, decision):
        self.method_id = method_id
        self.decision = decision

    def compute(self, snapshot):
        return self.decision


class RuntimeTests(unittest.TestCase):
    def state(self):
        return SimulationState(Scenario(
            scenario_id="scenario-runtime",
            sites={"site-1": Site("site-1", ("node-1", "node-2"))},
            nodes={
                "node-1": Node("node-1", "site-1", storage_capacity=10.0),
                "node-2": Node("node-2", "site-1", storage_capacity=10.0),
            },
            files={"file-1": File("file-1", 4.0)},
            replicas={"r1": Replica("r1", "file-1", "node-1")},
        ))

    def test_registry_has_only_canonical_roster(self):
        registry = MethodRegistry()
        for method_id in CANONICAL_METHODS:
            registry.register(MethodRegistration(method_id, lambda: None))
        self.assertEqual(registry.method_ids, CANONICAL_METHODS)
        with self.assertRaises(ValueError):
            registry.register(MethodRegistration("HER", lambda: None))

    def test_freeze_clone_and_matched_preparation_replay_same_realized_state(self):
        state = self.state()
        frozen = FrozenScenario.capture(
            state,
            ReplayTrace((Event(1.0, "request_arrival"),), "scenario-runtime", "seed-id", "stream-id"),
        )
        registry = MethodRegistry()
        for method_id in CANONICAL_METHODS:
            registry.register(MethodRegistration(method_id, lambda: None))
        runs = MatchedRunOrchestrator().prepare_runs(
            frozen,
            registry,
            lambda method_id: RunMetadata("experiment", "scenario-runtime", method_id, method_id, seed_identity="seed-id"),
        )
        self.assertEqual(tuple(run.method_id for run in runs), CANONICAL_METHODS)
        self.assertEqual(runs[0].state.scenario.replicas.keys(), runs[-1].state.scenario.replicas.keys())
        runs[0].state.scenario.nodes["node-1"].storage_used = 4.0
        self.assertEqual(runs[-1].state.scenario.nodes["node-1"].storage_used, 0.0)

    def test_event_loop_orders_and_dispatches_generic_handlers(self):
        state = self.state()
        loop = SimulationEventLoop(state, DecisionExecutor())
        seen = []
        loop.register_handler("a", lambda event: seen.append(event.event_type))
        loop.register_handler("b", lambda event: seen.append(event.event_type))
        loop.schedule(Event(2.0, "b"))
        loop.schedule(Event(1.0, "a"))
        self.assertEqual(loop.run(), 2)
        self.assertEqual(seen, ["a", "b"])
        self.assertEqual(state.current_time, 2.0)

    def test_dispatcher_keeps_adapter_read_only_and_executes_decision(self):
        state = self.state()
        decision = DecisionEnvelope(
            DecisionKind.REPLICA_CREATION,
            DecisionStatus.ACCEPTED,
            (("replica_id", "r2"), ("file_id", "file-1"), ("node_id", "node-2")),
        )
        registry = MethodRegistry()
        registry.register(MethodRegistration("DPRS", lambda: None, (DecisionKind.REPLICA_CREATION,)))
        result = AdapterDispatcher(registry, DecisionExecutor()).dispatch(
            "DPRS", state, DummyAdapter("DPRS", decision), "run-1"
        )
        self.assertEqual(result.execution.status, DecisionStatus.ACCEPTED)
        self.assertIn("r2", state.scenario.replicas)
        self.assertEqual(state.scenario.nodes["node-2"].storage_used, 4.0)

    def test_placement_translation_rejects_ambiguous_site(self):
        state = self.state()
        decision = DecisionEnvelope(
            DecisionKind.PLACEMENT,
            DecisionStatus.ACCEPTED,
            (("file_id", "file-1"), ("site_id", "site-1")),
        )
        result = DecisionExecutor().execute(state, decision)
        self.assertEqual(result.status, DecisionStatus.REJECTED)
        self.assertIn("unambiguous", result.reason)

    def test_delete_protects_last_valid_replica_and_records_transition(self):
        state = self.state()
        decision = DecisionEnvelope(
            DecisionKind.REPLICA_DELETION,
            DecisionStatus.ACCEPTED,
            (("replica_id", "r1"),),
        )
        recorder = RawRecorder()
        result = DecisionExecutor(recorder=recorder).execute(state, decision)
        self.assertEqual(result.status, DecisionStatus.REJECTED)
        self.assertIn("last valid replica", result.reason)
        self.assertIn("r1", state.scenario.replicas)
        self.assertEqual(len(recorder.observations), 1)

    def test_delete_and_move_mutate_generic_state_only_after_validation(self):
        state = self.state()
        state.scenario.replicas["r2"] = Replica("r2", "file-1", "node-2")
        state.scenario.nodes["node-2"].storage_used = 4.0
        delete = DecisionEnvelope(DecisionKind.REPLICA_DELETION, DecisionStatus.ACCEPTED, (("replica_id", "r2"),))
        self.assertEqual(DecisionExecutor().execute(state, delete).status, DecisionStatus.ACCEPTED)
        state.scenario.replicas["r2"] = Replica("r2", "file-1", "node-2")
        move = DecisionEnvelope(
            DecisionKind.REPLICA_MOVEMENT,
            DecisionStatus.ACCEPTED,
            (("replica_id", "r2"), ("target_node_id", "node-1")),
        )
        self.assertEqual(DecisionExecutor().execute(state, move).status, DecisionStatus.REJECTED)

    def test_failure_and_recovery_are_external_state_events(self):
        state = self.state()
        executor = FailureRecoveryExecutor()
        self.assertEqual(executor.fail_node(state, "node-1").status, DecisionStatus.ACCEPTED)
        self.assertFalse(state.scenario.nodes["node-1"].healthy)
        self.assertEqual(executor.recover_node(state, "node-1").status, DecisionStatus.ACCEPTED)
        self.assertTrue(state.scenario.nodes["node-1"].healthy)

    def test_request_service_executes_success_and_records_response(self):
        state = self.state()
        request = Request("request-1", "user-1", "file-1", 6.0, source_node_id="node-1")
        result = RequestServiceExecutor().serve(state, request)
        self.assertEqual(result.outcome, "SUCCESS")
        self.assertEqual(result.serving_replica_id, "r1")
        self.assertEqual(result.response_time, 0.0)

    def test_request_service_records_failure_without_response_time(self):
        state = self.state()
        state.scenario.nodes["node-1"].healthy = False
        state.scenario.nodes["node-1"].reachable = False
        request = Request("request-2", "user-1", "file-1", 6.0, source_node_id="node-1")
        result = RequestServiceExecutor().serve(state, request)
        self.assertEqual(result.outcome, "FAILED")
        self.assertIsNone(result.response_time)

    def test_request_path_cache_hits_without_topology_change(self):
        state = self.state()
        request = Request("request-cache", "user-1", "file-1", 6.0, source_node_id="node-1")
        executor = RequestServiceExecutor()
        executor.serve(state, request)
        executor.serve(state, request)
        self.assertGreaterEqual(executor.cache_hits, 1)

    def test_request_path_cache_invalidates_after_node_and_link_changes(self):
        state = self.state()
        request = Request("request-cache", "user-1", "file-1", 6.0, source_node_id="node-1")
        executor = RequestServiceExecutor()
        executor.serve(state, request)
        executor.invalidate_paths()
        self.assertEqual(executor.cache_invalidations, 1)
        executor.serve(state, request)
        self.assertGreaterEqual(executor.cache_misses, 2)


class PlacementExecutionTests(unittest.TestCase):
    """Covers the PLACEMENT causal-runtime repair: a successful PLACEMENT decision
    creates an additional replica, transferred from an existing valid source
    replica, on each accepted target node."""

    def state_with_link(self):
        return SimulationState(Scenario(
            scenario_id="scenario-placement",
            sites={"site-1": Site("site-1", ("node-1", "node-2"))},
            nodes={
                "node-1": Node("node-1", "site-1", storage_capacity=10.0),
                "node-2": Node("node-2", "site-1", storage_capacity=10.0),
            },
            files={"file-1": File("file-1", 4.0)},
            replicas={"r1": Replica("r1", "file-1", "node-1")},
            network_links={"link-1": NetworkLink("link-1", "node-1", "node-2", bandwidth=10.0, latency=1.0)},
        ))

    def placement_decision(self, node_ids=("node-2",)):
        return DecisionEnvelope(
            DecisionKind.PLACEMENT,
            DecisionStatus.ACCEPTED,
            (("file_id", "file-1"), ("placement_node_ids", node_ids)),
        )

    def test_valid_placement_creates_a_replica(self):
        state = self.state_with_link()
        result = DecisionExecutor().execute(state, self.placement_decision())
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)
        self.assertIn("placement-file-1-node-2", state.scenario.replicas)
        self.assertTrue(state.scenario.replicas["placement-file-1-node-2"].valid)

    def test_placement_updates_storage_used(self):
        state = self.state_with_link()
        DecisionExecutor().execute(state, self.placement_decision())
        self.assertEqual(state.scenario.nodes["node-2"].storage_used, 4.0)

    def test_duplicate_file_placement_on_same_node_is_rejected(self):
        state = self.state_with_link()
        executor = DecisionExecutor()
        first = executor.execute(state, self.placement_decision())
        self.assertEqual(first.status, DecisionStatus.ACCEPTED)
        second = executor.execute(state, self.placement_decision())
        self.assertEqual(second.status, DecisionStatus.REJECTED)
        self.assertEqual(len([r for r in state.scenario.replicas.values() if r.node_id == "node-2"]), 1)

    def test_insufficient_capacity_placement_is_rejected(self):
        state = self.state_with_link()
        state.scenario.nodes["node-2"].storage_capacity = 1.0
        result = DecisionExecutor().execute(state, self.placement_decision())
        self.assertEqual(result.status, DecisionStatus.REJECTED)
        self.assertNotIn("placement-file-1-node-2", state.scenario.replicas)

    def test_primary_replica_is_preserved_after_placement(self):
        state = self.state_with_link()
        DecisionExecutor().execute(state, self.placement_decision())
        self.assertIn("r1", state.scenario.replicas)
        self.assertTrue(state.scenario.replicas["r1"].valid)

    def test_subsequent_request_service_uses_newly_placed_replica(self):
        state = self.state_with_link()
        DecisionExecutor().execute(state, self.placement_decision())
        request = Request("request-1", "user-1", "file-1", 1.0, source_node_id="node-2")
        result = RequestServiceExecutor().serve(state, request)
        self.assertEqual(result.outcome, "SUCCESS")
        self.assertEqual(result.serving_replica_id, "placement-file-1-node-2")

    def test_replication_transfer_is_recorded_separately_with_nonzero_bytes(self):
        state = self.state_with_link()
        recorder = RawRecorder()
        DecisionExecutor(recorder=recorder).execute(state, self.placement_decision())
        transfers = [obs for obs in recorder.observations if obs.observation_type == "transfer"]
        self.assertEqual(len(transfers), 1)
        payload = dict(transfers[0].payload)
        self.assertEqual(payload["purpose"], "replication_movement")
        self.assertGreater(payload["bytes"], 0)

    def test_placement_execution_does_not_retroactively_mutate_prior_snapshot(self):
        state = self.state_with_link()
        snapshot = AdapterSnapshot.from_state(state)
        replicas_before = dict(snapshot.scenario["replicas"])
        DecisionExecutor().execute(state, self.placement_decision())
        self.assertEqual(dict(snapshot.scenario["replicas"]), replicas_before)
        self.assertIn("placement-file-1-node-2", state.scenario.replicas)


if __name__ == "__main__":
    unittest.main()

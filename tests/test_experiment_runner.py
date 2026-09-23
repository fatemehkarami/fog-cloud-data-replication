import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from replication_simulation.adapters import AdapterSnapshot
from replication_simulation.decisions import DecisionKind
from replication_simulation.domain import Request
from replication_simulation.experiment_runner import RunnerConfig, _adapter, build_frozen_state, run_pilot_matrix
from replication_simulation.result_records import TransitionRecord


class ExperimentRunnerTests(unittest.TestCase):
    def test_default_pilot_runs_ten_method_runs(self):
        summaries = run_pilot_matrix(RunnerConfig(pilot=True))
        self.assertEqual(len(summaries), 10)
        self.assertEqual({summary.method_id for summary in summaries}, {"Proposed", "HRS", "DPRS", "OGSA", "EIMORM"})
        self.assertTrue(all(summary.status == "VALID" for summary in summaries))
        self.assertTrue(all(summary.observations > 0 for summary in summaries))

    def test_full_configuration_is_represented_without_execution(self):
        config = RunnerConfig(pilot=False)
        self.assertEqual(config.workloads, ("W01", "W02", "W03"))
        self.assertEqual(config.failures, ("F0", "F1", "F2", "F3", "F4"))
        self.assertEqual(len(config.repetitions), 30)
        self.assertEqual(config.effective_request_limit, 1200)

    def test_active_replica_count_can_exceed_initial_catalog_after_placement(self):
        summaries = run_pilot_matrix(RunnerConfig(pilot=True, request_limit=40))
        self.assertTrue(any(summary.active_replica_count is not None and summary.active_replica_count > 100 for summary in summaries))

    def test_pilot_matrix_is_deterministic_across_repeated_runs(self):
        first = run_pilot_matrix(RunnerConfig(pilot=True, request_limit=20))
        second = run_pilot_matrix(RunnerConfig(pilot=True, request_limit=20))
        for a, b in zip(first, second):
            self.assertEqual(a.method_id, b.method_id)
            self.assertEqual(a.active_replica_count, b.active_replica_count)
            self.assertEqual(a.response_time_mean, b.response_time_mean)
            self.assertEqual(a.network_transfer_volume, b.network_transfer_volume)
            self.assertEqual(a.replication_transfer_volume, b.replication_transfer_volume)

    def test_each_method_reaches_its_currently_wired_decision_stage(self):
        # Documents the lifecycle audit: only the default-operation stage per
        # request type is reachable through the runner today. HRS's storage-
        # pressure replacement stage and EIMORM's standalone ETBDF/EARF/IEK
        # stages are not invoked here (see diagnosis); this is a known,
        # deliberately deferred gap, not a silent omission.
        state = build_frozen_state("scenario-stage-audit", 12345)
        file_id = sorted(state.scenario.files)[0]
        request = Request("request-1", "client-01", file_id, 6.0, source_node_id="site-01-edge", source_site_id="site-01")
        snapshot = AdapterSnapshot.from_state(state)
        expected_kinds = {
            "Proposed": {DecisionKind.PLACEMENT, DecisionKind.NO_OP, DecisionKind.REPLICA_DELETION},
            "HRS": {DecisionKind.PLACEMENT},
            "DPRS": {DecisionKind.PLACEMENT},
            "OGSA": {DecisionKind.PLACEMENT},
            "EIMORM": {DecisionKind.PLACEMENT, DecisionKind.NO_OP},
        }
        for method_id, kinds in expected_kinds.items():
            with self.subTest(method_id=method_id):
                decision = _adapter(method_id, state, request).compute(snapshot)
                self.assertIn(decision.kind, kinds)

    def test_accepted_placements_change_runtime_state_through_the_actual_runner_path(self):
        # Cross-method causal smoke test: runs each of Proposed, HRS, DPRS, OGSA,
        # and EIMORM through the real dispatcher/DecisionExecutor/RequestServiceExecutor
        # path on one small deterministic scenario. It does not require the five
        # methods to differ from one another; it only requires that whenever a
        # method's run contains an accepted placement, the runtime state actually
        # reflects it (catalog growth and a recorded replication transfer).
        summaries = run_pilot_matrix(RunnerConfig(pilot=True, request_limit=30))
        any_method_had_accepted_placement = False
        for summary in summaries:
            with self.subTest(method_id=summary.method_id):
                accepted_node_placements = 0
                for record in summary.records:
                    if not isinstance(record, TransitionRecord):
                        continue
                    payload = dict(record.payload)
                    if payload.get("action") != "placement_executed":
                        continue
                    for node_result in payload.get("placements", ()):
                        if dict(node_result).get("status") == "accepted":
                            accepted_node_placements += 1
                if accepted_node_placements > 0:
                    any_method_had_accepted_placement = True
                    self.assertGreater(summary.active_replica_count, 100)
                    self.assertGreater(summary.replication_transfer_volume, 0)
        self.assertTrue(any_method_had_accepted_placement)


if __name__ == "__main__":
    unittest.main()

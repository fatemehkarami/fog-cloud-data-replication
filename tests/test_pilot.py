import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from replication_simulation import FailureRecoveryExecutor, RequestServiceExecutor
from replication_simulation.pilot import build_pilot_scenario, run_pilot


class PilotTests(unittest.TestCase):
    def test_all_methods_complete_common_pilot_request(self):
        results = run_pilot()
        self.assertEqual(tuple(result.method_id for result in results), ("Proposed", "HRS", "DPRS", "OGSA", "EIMORM"))
        self.assertTrue(all(result.status == "VALID" for result in results))
        self.assertTrue(all(result.requests_completed == 1 for result in results))
        self.assertTrue(all(result.observations for result in results))

    def test_pilot_failure_and_recovery_change_serviceability(self):
        state = build_pilot_scenario()
        request = next(iter(state.scenario.requests.values()), None)
        if request is None:
            from replication_simulation import Request
            request = Request("request-1", "client-01", "file-001", 6.0, source_node_id="site-01-edge")
        executor = FailureRecoveryExecutor()
        self.assertEqual(executor.fail_node(state, "site-01-data").status.value, "accepted")
        self.assertEqual(RequestServiceExecutor().serve(state, request).outcome, "FAILED")
        self.assertEqual(executor.recover_node(state, "site-01-data").status.value, "accepted")
        self.assertEqual(RequestServiceExecutor().serve(state, request).outcome, "SUCCESS")


if __name__ == "__main__":
    unittest.main()

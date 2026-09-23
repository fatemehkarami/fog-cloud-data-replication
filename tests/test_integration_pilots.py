import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from replication_simulation.experiment_runner import run_integration_pilot
from replication_simulation.result_records import FailureObservation, RecoveryObservation


class IntegrationPilotTests(unittest.TestCase):
    def test_pilot_cells_cover_workload_and_failure_paths(self):
        for workload, failure in (("W01", "F0"), ("W01", "F1"), ("W02", "F0"), ("W03", "F2")):
            with self.subTest(workload=workload, failure=failure):
                summaries = run_integration_pilot(workload, failure, request_limit=12)
                self.assertEqual(len(summaries), 5)
                self.assertTrue(all(summary.status == "VALID" for summary in summaries))
                self.assertTrue(all(summary.requests_total == 12 for summary in summaries))
                self.assertTrue(all(summary.reliability is not None for summary in summaries))
                self.assertTrue(all(summary.observations > 0 for summary in summaries))

    def test_twenty_request_failure_window_replays_failure_and_recovery(self):
        sequences = tuple(range(295, 305)) + tuple(range(395, 405))
        summaries = run_integration_pilot("W01", "F1", request_limit=20, request_sequences=sequences)
        self.assertEqual(len(summaries), 5)
        for summary in summaries:
            self.assertEqual(summary.status, "VALID")
            self.assertEqual(summary.requests_total, 20)
            self.assertTrue(any(isinstance(record, FailureObservation) for record in summary.records))
            self.assertTrue(any(isinstance(record, RecoveryObservation) for record in summary.records))
            self.assertIsNotNone(summary.service_availability)


if __name__ == "__main__":
    unittest.main()

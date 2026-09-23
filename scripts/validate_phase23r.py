"""Targeted Phase 23R full-workload validation; never runs the final matrix."""
from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path

from replication_simulation.experiment_runner import run_integration_pilot
from replication_simulation.result_records import FailureObservation, RecoveryObservation, RequestObservation

CASES = (("W01", "F0"), ("W01", "F1"), ("W02", "F0"), ("W03", "F2"))
OUT_JSON = Path("results/phase23R_runtime_validation.json")
OUT_TXT = Path("results/phase23R_runtime_validation.txt")


def record_type(value):
    return value.__class__.__name__


def main():
    output = {"cases": [], "total_runs": 0, "valid_runs": 0, "failures": []}
    for workload, failure in CASES:
        summaries = run_integration_pilot(workload, failure, request_limit=1200)
        for summary in summaries:
            records = tuple(summary.records)
            requests = tuple(record for record in records if isinstance(record, RequestObservation))
            failure_records = tuple(record for record in records if isinstance(record, FailureObservation))
            recovery_records = tuple(record for record in records if isinstance(record, RecoveryObservation))
            expected_ids = tuple(f"request-{index:06d}" for index in range(1, 1201))
            actual_ids = tuple(record.request_id for record in requests)
            expected_times = tuple(index * 6.0 for index in range(1, 1201))
            actual_times = tuple(record.arrival_time for record in requests)
            failure_times = tuple(record.timestamp for record in failure_records)
            recovery_times = tuple(record.timestamp for record in recovery_records)
            during_failure = tuple(record for record in requests if 1800.0 <= record.arrival_time < 2400.0)
            after_recovery = tuple(record for record in requests if record.arrival_time >= 2400.0)
            checks = {
                "status_valid": summary.status == "VALID",
                "requests_total_1200": summary.requests_total == 1200,
                "request_observation_count_1200": len(requests) == 1200,
                "request_ids_exact": actual_ids == expected_ids,
                "timestamps_exact": actual_times == expected_times,
                "failure_records_present": bool(failure_records) if failure != "F0" else not failure_records,
                "recovery_records_present": bool(recovery_records) if failure in ("F1", "F2", "F3") else not recovery_records,
                "failure_timestamp_valid": all(timestamp in (1800.0, 3600.0, 4800.0, 5400.0) for timestamp in failure_times),
                "recovery_timestamp_valid": all(timestamp in (2400.0, 4500.0, 5400.0) for timestamp in recovery_times),
                "provenance_present": bool(summary.provenance),
                "raw_records_present": bool(records),
            }
            if failure == "F1":
                checks["failure_window_requests_present"] = bool(during_failure)
                checks["post_recovery_requests_present"] = bool(after_recovery)
                checks["failure_window_outcomes_recorded"] = all(record.outcome in ("SUCCESS", "FAILED") for record in during_failure)
            case_result = {
                "workload": workload,
                "failure": failure,
                "method": summary.method_id,
                "run_id": summary.run_id,
                "status": summary.status,
                "requests_total": summary.requests_total,
                "request_observations": len(requests),
                "failure_events": len(failure_records),
                "recovery_events": len(recovery_records),
                "failure_timestamps": failure_times,
                "recovery_timestamps": recovery_times,
                "failure_window_successful": sum(record.outcome == "SUCCESS" for record in during_failure),
                "failure_window_failed": sum(record.outcome == "FAILED" for record in during_failure),
                "metrics": {
                    "response_time_mean": summary.response_time_mean,
                    "reliability": summary.reliability,
                    "service_availability": summary.service_availability,
                    "active_replica_count": summary.active_replica_count,
                    "network_transfer_volume": summary.network_transfer_volume,
                    "algorithm_decision_time": summary.algorithm_decision_time,
                },
                "checks": checks,
                "provenance": dict(summary.provenance),
            }
            output["cases"].append(case_result)
            output["total_runs"] += 1
            output["valid_runs"] += int(all(checks.values()))
            if not all(checks.values()):
                output["failures"].append(case_result)
    output["validation"] = "PASS" if not output["failures"] and output["total_runs"] == 20 else "FAIL"
    OUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True, default=lambda value: asdict(value) if is_dataclass(value) else str(value)))
    lines = ["Phase 23R Runtime Validation", "", f"Validation: {output['validation']}", f"Runs: {output['total_runs']}", f"Valid runs: {output['valid_runs']}"]
    for case in output["cases"]:
        lines.append(f"{case['workload']}/{case['failure']}/{case['method']}: requests={case['requests_total']} observations={case['request_observations']} failures={case['failure_events']} recoveries={case['recovery_events']} status={case['status']}")
    if output["failures"]:
        lines.append(f"Failed checks: {len(output['failures'])}")
    OUT_TXT.write_text("\n".join(lines) + "\n")
    print(json.dumps({"validation": output["validation"], "runs": output["total_runs"], "valid_runs": output["valid_runs"], "json": str(OUT_JSON), "txt": str(OUT_TXT)}, sort_keys=True))


if __name__ == "__main__":
    main()

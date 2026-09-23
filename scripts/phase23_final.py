"""Execute and structurally validate the corrected frozen Phase 23 campaign."""
from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from replication_simulation.experiment_runner import (
    FAILURES,
    METHODS,
    WORKLOADS,
    RunnerConfig,
    build_artifacts,
    run_pilot_matrix,
)
from replication_simulation.result_records import RequestObservation

ROOT = Path(__file__).resolve().parents[1]
# Default (unchanged) path: the preserved pre-repair historical artifact. Any
# explicit --output override must never fall back to reading or writing this path.
DEFAULT_RAW = ROOT / "results" / "phase23_final_raw.json"
RAW = DEFAULT_RAW
REPORT_JSON = ROOT / "results" / "phase23_final_execution_report.json"
REPORT_TXT = ROOT / "results" / "phase23_final_execution_report.txt"
EXPECTED_RUNS = 2250
EXPECTED_REQUESTS = EXPECTED_RUNS * 1200
EXPECTED_STATUSES = {"VALID", "INVALID", "UNRESOLVED", "FAILED", "TIMED_OUT"}


def derive_paths(output: Optional[str]) -> Dict[str, Path]:
    """Resolve the raw checkpoint/output path and its paired report paths.

    Passing None preserves the original default path/behaviour exactly. An
    explicit override is used verbatim and is never mixed with the default.
    """
    raw = Path(output).resolve() if output else DEFAULT_RAW
    report_stem = raw.stem[: -len("_raw")] if raw.stem.endswith("_raw") else raw.stem
    return {
        "raw": raw,
        "report_json": raw.with_name(f"{report_stem}_execution_report.json"),
        "report_txt": raw.with_name(f"{report_stem}_execution_report.txt"),
    }


def run_identity(record: Dict[str, Any]) -> str:
    return f"{record['method_id']}-{record['workload_id']}-{record['failure_scenario_id']}-{record['repetition_id']}"


def serialize_summary(summary: Any) -> Dict[str, Any]:
    result = asdict(summary)
    result["provenance"] = dict(summary.provenance)
    result["records"] = []
    for record in summary.records:
        payload = asdict(record) if is_dataclass(record) else dict(record)
        result["records"].append({"record_type": type(record).__name__, **payload})
    return result


def write_checkpoint(records: Iterable[Dict[str, Any]], raw_path: Path) -> None:
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(records, key=run_identity)
    fd, temporary = tempfile.mkstemp(prefix=f"{raw_path.stem}_", suffix=".json", dir=raw_path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(ordered, stream, indent=2, sort_keys=True, allow_nan=False)
            stream.write("\n")
        os.replace(temporary, raw_path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_existing(raw_path: Path) -> Dict[str, Dict[str, Any]]:
    """Load completed run identities strictly from raw_path; never from any other artifact."""
    if not raw_path.exists():
        return {}
    with raw_path.open() as stream:
        loaded = json.load(stream)
    if not isinstance(loaded, list):
        raise ValueError(f"{raw_path} must contain a JSON array")
    records: Dict[str, Dict[str, Any]] = {}
    attempts = set()
    for record in loaded:
        identity = run_identity(record)
        if identity in records:
            raise ValueError(f"duplicate persisted run identity: {identity}")
        if record.get("attempt_id") in attempts:
            raise ValueError(f"duplicate persisted attempt identity: {record.get('attempt_id')}")
        attempts.add(record.get("attempt_id"))
        records[identity] = record
    return records


def finite_values(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(finite_values(item) for item in value.values())
    if isinstance(value, list):
        return all(finite_values(item) for item in value)
    return True


def validate(records: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    expected_ids = {
        f"{method}-{workload}-{failure}-rep-{repetition:02d}"
        for workload in WORKLOADS
        for failure in FAILURES
        for repetition in range(1, 31)
        for method in METHODS
    }
    actual_ids = set(records)
    status_counts = {status: 0 for status in EXPECTED_STATUSES}
    errors = []
    request_count = 0
    cells = {}
    attempts = set()
    config = RunnerConfig(pilot=False, request_limit=1200, progress=False)
    for identity, record in records.items():
        status = record.get("status")
        if status in status_counts:
            status_counts[status] += 1
        else:
            errors.append(f"{identity}: unknown status {status}")
        attempt_id = record.get("attempt_id")
        if attempt_id in attempts:
            errors.append(f"{identity}: duplicate attempt identity")
        attempts.add(attempt_id)
        if record.get("run_id") != identity or attempt_id != f"attempt-{identity}":
            errors.append(f"{identity}: identity or attempt mismatch")
        if record.get("requests_total") != 1200:
            errors.append(f"{identity}: requests_total is {record.get('requests_total')}")
        typed = record.get("records", [])
        requests = [item for item in typed if item.get("record_type") == "RequestObservation"]
        request_ids = [item.get("request_id") for item in requests]
        expected_request_ids = [f"request-{index:06d}" for index in range(1, 1201)]
        if len(requests) != 1200 or request_ids != expected_request_ids:
            errors.append(f"{identity}: request observations or IDs invalid")
        if [item.get("arrival_time") for item in requests] != [index * 6.0 for index in range(1, 1201)]:
            errors.append(f"{identity}: timestamps invalid")
        if any(item.get("record_type") is None for item in typed):
            errors.append(f"{identity}: untyped raw record")
        provenance = record.get("provenance") or {}
        for key in ("scenario_digest", "workload_digest", "failure_digest", "master_seed_identity", "scenario_seed_identity", "workload_seed_identity", "failure_seed_identity", "method_seed_identity"):
            if not provenance.get(key):
                errors.append(f"{identity}: missing provenance {key}")
        if not finite_values(record):
            errors.append(f"{identity}: nonfinite value")
        artifacts = build_artifacts(config, record["workload_id"], record["failure_scenario_id"], record["repetition_id"])
        expected_digests = {
            "scenario_digest": artifacts.scenario_digest,
            "workload_digest": artifacts.workload_digest,
            "failure_digest": artifacts.failure_digest,
        }
        if any(provenance.get(key) != value for key, value in expected_digests.items()):
            errors.append(f"{identity}: artifact digest mismatch")
        request_count += len(requests)
        cell = (record.get("workload_id"), record.get("failure_scenario_id"), record.get("repetition_id"))
        cells.setdefault(cell, set()).add(record.get("method_id"))
    missing = expected_ids - actual_ids
    unexpected = actual_ids - expected_ids
    if missing:
        errors.append(f"missing run identities: {len(missing)}")
    if unexpected:
        errors.append(f"unexpected run identities: {len(unexpected)}")
    complete_cells = sum(len(methods) == 5 for methods in cells.values())
    representative = {
        failure: sum(1 for identity in actual_ids if f"-{failure}-" in identity and records[identity].get("requests_total") == 1200)
        for failure in ("F1", "F2", "F3", "F4")
    }
    checks = {
        "expected": EXPECTED_RUNS,
        "unique_runs": len(actual_ids),
        "missing_runs": len(missing),
        "duplicate_run_identities": len(records) - len(actual_ids),
        "duplicate_attempt_identities": len(records) - len(attempts),
        "status_total": sum(status_counts.values()),
        "status_counts": status_counts,
        "complete_workload_failure_repetition_cells": complete_cells,
        "expected_cells": 450,
        "requests_per_run": 1200,
        "request_observations_total": request_count,
        "expected_request_observations": EXPECTED_REQUESTS,
        "no_missing_request_ids": not any("request observations or IDs invalid" in error for error in errors),
        "no_nonfinite_prohibited_values": all(finite_values(record) for record in records.values()),
        "provenance_complete": not any("missing provenance" in error for error in errors),
        "artifact_digests_consistent": not any("artifact digest mismatch" in error for error in errors),
        "representative_failure_runs": representative,
    }
    valid = (
        not errors and len(actual_ids) == EXPECTED_RUNS and request_count == EXPECTED_REQUESTS
        and complete_cells == 450 and all(value == 450 for value in representative.values())
        and sum(status_counts.values()) == EXPECTED_RUNS
    )
    return {"validation": "PASS" if valid else "FAIL", "checks": checks, "errors": errors}


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Execute and structurally validate the corrected frozen Phase 23 campaign.")
    parser.add_argument(
        "--output",
        default=None,
        help="Override the raw checkpoint/output path. Defaults to results/phase23_final_raw.json (unchanged behaviour). "
             "Resumability and validation operate only on the selected path; the historical default is never inspected "
             "when an override is given.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the resolved configuration/paths and completed-run audit only; execute no campaign runs.",
    )
    args = parser.parse_args(argv)
    paths = derive_paths(args.output)
    raw_path, report_json_path, report_txt_path = paths["raw"], paths["report_json"], paths["report_txt"]

    records = load_existing(raw_path)
    initial_count = len(records)
    config = RunnerConfig(pilot=False, request_limit=1200, progress=True)

    if args.dry_run:
        expected_matrix_size = len(config.workloads) * len(config.failures) * len(config.repetitions) * len(METHODS)
        print(json.dumps({
            "dry_run": True,
            "selected_output_path": str(raw_path),
            "historical_default_path": str(DEFAULT_RAW),
            "uses_historical_default_path": raw_path == DEFAULT_RAW,
            "completed_run_ids_source": str(raw_path),
            "initial_persisted_runs_in_selected_output": initial_count,
            "pilot": config.pilot,
            "effective_request_limit": config.effective_request_limit,
            "methods": list(METHODS),
            "workloads": list(config.workloads),
            "failures": list(config.failures),
            "repetitions": list(config.repetitions),
            "expected_matrix_size": expected_matrix_size,
            "campaign_executed": False,
        }, indent=2, sort_keys=True))
        return

    def persist(summary: Any) -> None:
        identity = summary.run_id
        if identity in records:
            raise RuntimeError(f"attempted overwrite of completed run: {identity}")
        serialized = serialize_summary(summary)
        if serialized["requests_total"] != 1200:
            raise RuntimeError(f"run did not execute 1200 requests: {identity}")
        records[identity] = serialized
        write_checkpoint(records.values(), raw_path)

    run_pilot_matrix(config, completed_run_ids=set(records), on_complete=persist)
    result = validate(records)
    result["execution"] = {"initial_persisted_runs": initial_count, "final_persisted_runs": len(records), "raw_dataset": str(raw_path)}
    report_json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    lines = [
        "Phase 23 Corrected Primary Execution Report",
        "",
        f"Validation: {result['validation']}",
        f"Persisted runs: {len(records)} / {EXPECTED_RUNS}",
        f"Request observations: {result['checks']['request_observations_total']} / {EXPECTED_REQUESTS}",
        f"Complete cells: {result['checks']['complete_workload_failure_repetition_cells']} / 450",
        f"Status counts: {result['checks']['status_counts']}",
    ]
    if result["errors"]:
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in result["errors"])
    report_txt_path.write_text("\n".join(lines) + "\n")
    print(json.dumps(result, sort_keys=True))
    if result["validation"] != "PASS":
        raise SystemExit(1)
    print("CORRECTED PRIMARY 2,250-RUN EXPERIMENT COMPLETE")




if __name__ == "__main__":
    main()

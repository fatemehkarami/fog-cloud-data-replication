"""Focused cache performance/semantic validation; never runs the final matrix."""
from __future__ import annotations

import json
import os
import resource
import time
from pathlib import Path

from replication_simulation.experiment_runner import run_integration_pilot

CASES = (("W01", "F0"), ("W01", "F1"), ("W02", "F0"), ("W03", "F2"))
OUT_JSON = Path("results/phase23P_performance_validation.json")
OUT_TXT = Path("results/phase23P_performance_validation.txt")


def run_case(workload, failure, cache):
    start_wall = time.perf_counter()
    start_cpu = time.process_time()
    summaries = run_integration_pilot(workload, failure, request_limit=1200, path_cache_enabled=cache)
    wall = time.perf_counter() - start_wall
    cpu = time.process_time() - start_cpu
    return summaries, wall, cpu


def signature(summary):
    return (summary.requests_total, summary.requests_successful, summary.requests_failed, summary.response_time_mean, summary.reliability, summary.service_availability, summary.active_replica_count, summary.network_transfer_volume)


def main():
    results = []
    selected_cases = CASES
    requested_case = os.environ.get("PHASE23P_CASE")
    if requested_case:
        selected_cases = tuple(case for case in CASES if "/".join(case) == requested_case)
    for workload, failure in selected_cases:
        summaries, wall, cpu = run_case(workload, failure, True)
        for summary in summaries:
            provenance = dict(summary.provenance)
            results.append({"workload": workload, "failure": failure, "method": summary.method_id, "cache": "on", "status": summary.status, "requests_total": summary.requests_total, "request_successful": summary.requests_successful, "request_failed": summary.requests_failed, "wall_seconds": wall / 5.0, "cpu_seconds": cpu / 5.0, "requests_per_second": summary.requests_total / (wall / 5.0), "metrics": signature(summary), "cache_hits": provenance.get("path_cache_hits"), "cache_misses": provenance.get("path_cache_misses"), "cache_invalidations": provenance.get("path_cache_invalidations")})
    baseline, wall, cpu = ((), 0.0, 0.0)
    baseline_by_method = {summary.method_id: summary for summary in baseline}
    optimized_by_method = {(row["workload"], row["failure"], row["method"]): row for row in results}
    semantic = []
    for method, summary in baseline_by_method.items():
        optimized = optimized_by_method[("W01", "F0", method)]
        semantic.append({"method": method, "equivalent": signature(summary) == tuple(optimized["metrics"]), "cache_off_wall_seconds": wall / 5.0, "cache_on_wall_seconds": optimized["wall_seconds"], "cache_off_cpu_seconds": cpu / 5.0, "cache_on_hits": optimized["cache_hits"], "cache_on_misses": optimized["cache_misses"]})
    output = {"cases": results, "cache_off_baseline": semantic, "cache_off_baseline_available": bool(semantic), "all_1200_request_runs": all(row["requests_total"] == 1200 and row["status"] == "VALID" for row in results), "semantic_equivalence": all(row["equivalent"] for row in semantic) if semantic else "NOT_MEASURED", "optimized_wall_seconds": sum(row["wall_seconds"] for row in results) / len(results) if results else None, "cache_off_baseline_wall_seconds": wall / 5.0 if semantic else None, "estimated_full_campaign_seconds": (sum(row["wall_seconds"] for row in results) / len(results) if results else 0.0) * (2250 / 20.0)}
    output_path = Path(f"results/phase23P_performance_validation_{requested_case.replace('/', '_')}.json") if requested_case else OUT_JSON
    text_path = Path(f"results/phase23P_performance_validation_{requested_case.replace('/', '_')}.txt") if requested_case else OUT_TXT
    output["output_json"] = str(output_path)
    output["output_txt"] = str(text_path)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True))
    lines = ["Phase 23P Performance Validation", "", f"Semantic equivalence: {output['semantic_equivalence']}", f"All 1200-request runs valid: {output['all_1200_request_runs']}", f"Optimized mean wall seconds/run: {output['optimized_wall_seconds']}", f"Cache-off W01/F0 mean wall seconds/run: {output['cache_off_baseline_wall_seconds']}", f"Estimated full campaign seconds: {output['estimated_full_campaign_seconds']}", ""]
    for row in semantic:
        lines.append(f"{row['method']}: equivalent={row['equivalent']} cache-on hits={row['cache_on_hits']} misses={row['cache_on_misses']} cache-off={row['cache_off_wall_seconds']:.3f}s cache-on={row['cache_on_wall_seconds']:.3f}s")
    text_path.write_text("\n".join(lines) + "\n")
    print(json.dumps({"json": str(output_path), "txt": str(text_path), "semantic_equivalence": output["semantic_equivalence"], "all_1200_request_runs": output["all_1200_request_runs"]}, sort_keys=True))


if __name__ == "__main__":
    main()

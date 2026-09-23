"""Generate all seven thesis figures using the shared design system.

Run: python3 scripts/generate_thesis_figures.py

Regenerates 01_response_time through 07_algorithm_decision_time (PNG @300 DPI
+ vector PDF) in results/charts/, and prints a verification report comparing
each figure's plotted overall means against a direct recomputation from
results/phase23_final_run_metrics.csv.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict

from thesis_figures_common import METHODS, MetricConfig, load_all_runs, render_figure

BYTES_PER_GB = 1e9  # decimal GB; display-only conversion, underlying bytes unchanged

METRICS = [
    MetricConfig(
        key="response_time",
        filename="01_response_time",
        axis_label="Response Time (s)",
        annotate_unit_suffix=" s",
        annotate_base_decimals=3,
        annotate_max_decimals=6,
        locator=("multiple", 0.5),
        caption="Points show mean response time; error bars show 95% paired-bootstrap confidence intervals.",
        seed_offset=0,
    ),
    MetricConfig(
        key="reliability",
        filename="02_reliability",
        axis_label="Reliability (proportion)",
        annotate_base_decimals=3,
        annotate_max_decimals=6,
        locator=("multiple", 0.05),
        caption="Points show mean reliability; error bars show 95% paired-bootstrap confidence intervals.",
        seed_offset=1000,
    ),
    MetricConfig(
        key="service_availability",
        filename="03_service_availability",
        axis_label="Service Availability (proportion)",
        annotate_base_decimals=3,
        annotate_max_decimals=6,
        locator=("multiple", 0.05),
        caption="Points show mean service availability; error bars show 95% paired-bootstrap confidence intervals.",
        seed_offset=2000,
    ),
    MetricConfig(
        key="active_replica_count",
        filename="04_active_replica_count",
        axis_label="Registered/Valid Replica Count",
        annotate_base_decimals=1,
        annotate_max_decimals=3,
        locator=("multiple", 50),
        caption=(
            "Points show mean registered/valid replica count; error bars show 95% paired-bootstrap "
            "confidence intervals. Reflects final registered/valid replicas, not confirmed healthy/reachable replicas."
        ),
        seed_offset=3000,
    ),
    MetricConfig(
        key="network_transfer_volume",
        filename="05_network_transfer_volume",
        axis_label="Network Transfer Volume (GB)",
        annotate_unit_suffix=" GB",
        annotate_base_decimals=1,
        annotate_max_decimals=4,
        transform=lambda v: v / BYTES_PER_GB,
        locator=("multiple", 500),
        caption="Points show mean network transfer volume; error bars show 95% paired-bootstrap confidence intervals.",
        seed_offset=4000,
    ),
    MetricConfig(
        key="replication_transfer_volume",
        filename="06_replication_transfer_volume",
        axis_label="Replication Transfer Volume (GB)",
        annotate_unit_suffix=" GB",
        annotate_base_decimals=1,
        annotate_max_decimals=4,
        transform=lambda v: v / BYTES_PER_GB,
        locator=("auto", 6),
        caption="Points show mean replication transfer volume; error bars show 95% paired-bootstrap confidence intervals.",
        seed_offset=5000,
    ),
    MetricConfig(
        key="algorithm_decision_time",
        filename="07_algorithm_decision_time",
        axis_label="Algorithm Decision Time (ms)",
        annotate_unit_suffix=" ms",
        annotate_base_decimals=1,
        annotate_max_decimals=4,
        locator=("auto", 6),
        caption="Points show mean algorithm decision time; error bars show 95% paired-bootstrap confidence intervals.",
        seed_offset=6000,
    ),
]


def recompute_overall_means_from_csv():
    """Independent recomputation of overall per-method means straight from the CSV, for verification."""
    sums = defaultdict(lambda: defaultdict(float))
    counts = defaultdict(lambda: defaultdict(int))
    fields = [m.key for m in METRICS]
    from thesis_figures_common import RUN_METRICS
    with RUN_METRICS.open(newline="") as handle:
        for row in csv.DictReader(handle):
            method = row["method"]
            for f in fields:
                sums[f][method] += float(row[f])
                counts[f][method] += 1
    return {f: {m: sums[f][m] / counts[f][m] for m in METHODS} for f in fields}


def main():
    all_runs = load_all_runs()
    verification_source = recompute_overall_means_from_csv()

    report_rows = []
    for config in METRICS:
        result = render_figure(config, all_runs)
        row = {"metric": config.key, "filename": config.filename, "methods": {}}
        max_abs_diff = 0.0
        for method in METHODS:
            plotted = float(result["overall_means_native"][method])
            independent = float(verification_source[config.key][method])
            diff = abs(plotted - independent)
            max_abs_diff = max(max_abs_diff, diff)
            row["methods"][method] = {"plotted_mean": plotted, "independent_mean": independent, "abs_diff": diff}
        row["max_abs_diff"] = max_abs_diff
        row["match"] = bool(max_abs_diff < 1e-9)
        report_rows.append(row)
        print(f"Saved results/charts/{config.filename}.png and .pdf "
              f"(max |plotted-independent| = {max_abs_diff:.3e})")

    all_match = all(row["match"] for row in report_rows)
    print()
    print(f"Verification: {'PASS' if all_match else 'FAIL'} - all plotted overall means "
          f"{'match' if all_match else 'DO NOT all match'} an independent recomputation from the clean run-level CSV.")
    print(json.dumps(report_rows, indent=2))


if __name__ == "__main__":
    main()

"""Shared plotting/statistics library for the thesis figure design system.

Data source: results/phase23_final_run_metrics.csv (clean run-level results,
no counterfactual/test-only markers). Means and 95% paired-bootstrap
confidence intervals are computed directly from these run-level values using
matched resampling (matched by repetition within each grouping), matching the
documented CMP-RD-009 bootstrap protocol (10,000 resamples). No values are
fabricated, tuned, or altered; these scripts only visualize existing data.

Note: results/phase23_final_method_summary.csv, phase23_final_cell_summary.csv,
phase23_bootstrap_results.csv, and phase23_statistical_results.csv are
explicitly labeled "TEST ONLY - COUNTERFACTUAL RESULTS; NOT SCIENTIFIC RESULTS"
and are therefore never used as a source in this design system.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, MultipleLocator

RUN_METRICS = Path("results/phase23_final_run_metrics.csv")
OUT_DIR = Path("results/charts")

METHODS = ["Proposed", "HRS", "DPRS", "OGSA", "EIMORM"]
WORKLOADS = ["W01", "W02", "W03"]
FAILURES = ["F0", "F1", "F2", "F3", "F4"]
BOOTSTRAP_RESAMPLES = 10_000
RNG_SEED_BASE = 20260918

# Colorblind-friendly palette (Okabe-Ito), one fixed color+marker per method,
# shared across every thesis figure in this design system.
STYLE = {
    "Proposed": dict(color="#0072B2", marker="o"),
    "HRS": dict(color="#E69F00", marker="s"),
    "DPRS": dict(color="#009E73", marker="^"),
    "OGSA": dict(color="#D55E00", marker="D"),
    "EIMORM": dict(color="#CC79A7", marker="X"),
}


@dataclass
class MetricConfig:
    key: str  # raw CSV field name
    filename: str  # output filename stem, e.g. "02_reliability"
    axis_label: str  # y-axis label
    annotate_unit_suffix: str = ""  # appended to overall-panel mean labels, e.g. " s", " GB", " ms"
    annotate_base_decimals: int = 3  # starting decimal places for overall-panel mean labels
    annotate_max_decimals: int = 6  # cap for adaptive precision so labels stay readable
    transform: Callable[[float], float] = lambda v: v  # display-unit conversion only
    locator: tuple = ("auto", 6)  # ("multiple", step) or ("auto", nbins)
    # Caption text is stored only for PNG/PDF metadata (thesis captions live in the document);
    # it is never rendered inside the plot area.
    caption: str = "Points show mean values; error bars show 95% paired-bootstrap confidence intervals."
    seed_offset: int = 0
    top_pad_frac: float = 0.05
    bottom_pad_frac: float = 0.06
    overall_errorbar: dict = field(default_factory=lambda: dict(elinewidth=1.3, capsize=3.4, capthick=1.3))
    dodged_errorbar: dict = field(default_factory=lambda: dict(elinewidth=1.4, capsize=3.4, capthick=1.4))


def adaptive_decimals(values, base_decimals, max_decimals):
    """Smallest decimal count >= base_decimals that keeps all values visually distinct.

    Formatting only; never changes the underlying values being displayed.
    """
    decimals = base_decimals
    while decimals < max_decimals:
        rounded = [round(v, decimals) for v in values]
        if len(set(rounded)) == len(values):
            break
        decimals += 1
    return decimals


def load_all_runs():
    """Return {field: {method: {(workload, failure, repetition): value}}}."""
    fields = [
        "response_time", "reliability", "service_availability",
        "active_replica_count", "network_transfer_volume",
        "replication_transfer_volume", "algorithm_decision_time",
    ]
    data = {f: {m: {} for m in METHODS} for f in fields}
    with RUN_METRICS.open(newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row["workload"], row["failure"], row["repetition"])
            method = row["method"]
            for f in fields:
                data[f][method][key] = float(row[f])
    return data


def bootstrap_ci(values_by_method, keys, rng):
    """Matched paired bootstrap 95% CI of the mean for each method."""
    n = len(keys)
    arrays = {m: np.array([values_by_method[m][key] for key in keys]) for m in METHODS}
    resample_means = {m: np.empty(BOOTSTRAP_RESAMPLES) for m in METHODS}
    for i in range(BOOTSTRAP_RESAMPLES):
        indices = rng.integers(0, n, size=n)
        for m in METHODS:
            resample_means[m][i] = arrays[m][indices].mean()
    result = {}
    for m in METHODS:
        lower, upper = np.percentile(resample_means[m], [2.5, 97.5])
        result[m] = (arrays[m].mean(), lower, upper)
    return result


def overall_stats(values_by_method, rng):
    keys = sorted({key for m in METHODS for key in values_by_method[m]})
    return bootstrap_ci(values_by_method, keys, rng)


def workload_stats(values_by_method, rng):
    out = {}
    for workload in WORKLOADS:
        keys = sorted({key for m in METHODS for key in values_by_method[m] if key[0] == workload})
        out[workload] = bootstrap_ci(values_by_method, keys, rng)
    return out


def failure_stats(values_by_method, rng):
    out = {}
    for failure in FAILURES:
        keys = sorted({key for m in METHODS for key in values_by_method[m] if key[1] == failure})
        out[failure] = bootstrap_ci(values_by_method, keys, rng)
    return out


def configure_style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.titleweight": "bold",
        "axes.labelsize": 9,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.fontsize": 8.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "axes.edgecolor": "#333333",
        "figure.dpi": 100,
    })


def style_axis(ax):
    ax.grid(axis="y", color="#d9d9d9", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="both", length=3, color="#333333")


def apply_locator(ax, locator):
    kind, value = locator
    if kind == "multiple":
        ax.yaxis.set_major_locator(MultipleLocator(value))
    else:
        ax.yaxis.set_major_locator(MaxNLocator(nbins=value))


def draw_overall(ax, overall, config: MetricConfig):
    ax.set_title("(a) Overall comparison", loc="left")
    x = np.arange(len(METHODS))
    means_d = {m: config.transform(overall[m][0]) for m in METHODS}
    decimals = adaptive_decimals(list(means_d.values()), config.annotate_base_decimals, config.annotate_max_decimals)
    for i, method in enumerate(METHODS):
        mean, lower, upper = overall[method]
        mean_d, lower_d, upper_d = (config.transform(v) for v in (mean, lower, upper))
        style = STYLE[method]
        err = np.array([[mean_d - lower_d], [upper_d - mean_d]])
        ax.errorbar(
            x[i], mean_d, yerr=err, fmt=style["marker"], color=style["color"],
            markersize=6, markeredgecolor="white", markeredgewidth=0.6,
            zorder=3, **config.overall_errorbar,
        )
        label = f"{mean_d:.{decimals}f}{config.annotate_unit_suffix}"
        ax.annotate(
            label, (x[i], upper_d), textcoords="offset points",
            xytext=(0, 6), ha="center", fontsize=8, color="#222222",
        )
    ax.set_xticks(x)
    ax.set_xticklabels(METHODS)
    ax.set_xlim(-0.6, len(METHODS) - 0.4)
    style_axis(ax)


def draw_dodged(ax, categories, stats_by_category, title, config: MetricConfig):
    ax.set_title(title, loc="left")
    offsets = np.linspace(-0.28, 0.28, len(METHODS))
    for i, method in enumerate(METHODS):
        style = STYLE[method]
        xs, ys, lowers, uppers = [], [], [], []
        for c, category in enumerate(categories):
            mean, lower, upper = stats_by_category[category][method]
            mean_d, lower_d, upper_d = (config.transform(v) for v in (mean, lower, upper))
            xs.append(c + offsets[i])
            ys.append(mean_d)
            lowers.append(mean_d - lower_d)
            uppers.append(upper_d - mean_d)
        ax.errorbar(
            xs, ys, yerr=[lowers, uppers], fmt=style["marker"], color=style["color"],
            markersize=5, markeredgecolor="white", markeredgewidth=0.5,
            zorder=3, **config.dodged_errorbar,
        )
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories)
    ax.set_xlim(-0.6, len(categories) - 0.4)
    style_axis(ax)


def render_figure(config: MetricConfig, all_runs):
    values_by_method = all_runs[config.key]
    seed = RNG_SEED_BASE + config.seed_offset
    rng = np.random.default_rng(seed)
    overall = overall_stats(values_by_method, rng)
    by_workload = workload_stats(values_by_method, rng)
    by_failure = failure_stats(values_by_method, rng)

    configure_style()
    fig, axes = plt.subplots(
        3, 1, figsize=(6.8, 8.2), sharey=True,
        gridspec_kw={"hspace": 0.42},
    )

    draw_overall(axes[0], overall, config)
    draw_dodged(axes[1], WORKLOADS, by_workload, "(b) Workload effect", config)
    draw_dodged(axes[2], FAILURES, by_failure, "(c) Failure scenario effect", config)

    all_lower, all_upper = [], []
    for group in (overall, *by_workload.values(), *by_failure.values()):
        for mean, lower, upper in group.values():
            all_lower.append(config.transform(lower))
            all_upper.append(config.transform(upper))
    ymin, ymax = min(all_lower), max(all_upper)
    span = ymax - ymin
    top_pad = span * config.top_pad_frac
    bottom_pad = span * config.bottom_pad_frac
    for ax in axes:
        ax.set_ylim(ymin - bottom_pad, ymax + top_pad)
        ax.set_ylabel(config.axis_label)
        apply_locator(ax, config.locator)
        ax.ticklabel_format(axis="y", style="plain")

    legend_handles = [
        Line2D([0], [0], marker=STYLE[m]["marker"], color=STYLE[m]["color"],
               linestyle="none", markersize=6, markeredgecolor="white",
               markeredgewidth=0.6, label=m)
        for m in METHODS
    ]
    fig.legend(
        handles=legend_handles, labels=METHODS, loc="lower center",
        ncol=len(METHODS), bbox_to_anchor=(0.5, 0.045), frameon=False,
        handletextpad=0.5, columnspacing=1.4,
    )
    # Methodological explanations (e.g. CI meaning, replica-count caveats) belong in the thesis
    # caption, not inside the plot; config.caption is only carried into PNG/PDF metadata below.
    fig.subplots_adjust(left=0.13, right=0.97, top=0.965, bottom=0.10)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata_png = {"Title": config.axis_label, "Description": config.caption}
    metadata_pdf = {"Title": config.axis_label, "Subject": config.caption}
    fig.savefig(OUT_DIR / f"{config.filename}.png", dpi=300, metadata=metadata_png)
    fig.savefig(OUT_DIR / f"{config.filename}.pdf", metadata=metadata_pdf)
    plt.close(fig)

    return {
        "metric": config.key,
        "overall_means_native": {m: overall[m][0] for m in METHODS},
    }

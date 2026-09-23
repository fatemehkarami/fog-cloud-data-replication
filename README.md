# Dynamic and Reliable Multi-Objective Data Replication in Fog-Cloud Computing

## Overview

This repository contains the simulation implementation and reproducible experimental results for a PhD research project on dynamic multi-objective data replication in edge-cloud computing.

The proposed method uses:

- Overall Importance Score (OIS)
- Dynamic replication selection
- Replication timing
- Replica-count determination
- Replica placement
- NSGA-III multi-objective optimization
- Replica replacement

The proposed placement stage considers Energy Consumption, Response Time, Data Node Load, Total Cost, and Network Centrality.

## Methods Compared

1. Proposed
2. HRS - Hybrid Replication Strategy
3. DPRS
4. OGSA
5. EIMORM

## Experimental Design

The final experiment used the following design:

- 4 sites
- 12 heterogeneous nodes
- 100 data files
- 3 workloads
- 5 failure scenarios
- 30 independent repetitions
- 2,250 method runs
- 1,200 requests per run
- 2,700,000 total admitted requests
- Simulation horizon: 7,200 seconds

### Workloads

- W01 Balanced
- W02 Stationary Skew
- W03 Phase Shift

### Failure Scenarios

- F0 No failure
- F1 Node transient failure
- F2 Site transient failure
- F3 Link transient failure
- F4 Persistent node failure

## Evaluation Metrics

The final experiment reports seven metrics:

1. Response Time
2. Reliability
3. Service Availability
4. Registered/Valid Replica Count
5. Network Transfer Volume
6. Replication Transfer Volume
7. Algorithm Decision Time

Registered/Valid Replica Count is a descriptive catalogued-valid count. It must not be interpreted as the number of currently healthy or reachable replicas.

## Final Results

The following are descriptive means from the final simulation dataset, [results/phase23_final_run_metrics.csv](results/phase23_final_run_metrics.csv). Transfer volumes use decimal gigabytes for display.

| Method | Response Time (s) | Reliability | Service Availability | Registered/Valid Replica Count | Network Transfer (GB) | Replication Transfer (GB) | Algorithm Decision (ms) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Proposed | 3.119 | 0.985183 | 0.963099 | 153.333 | 4,287.39 | 214.03 | 4570.582 |
| HRS | 3.635 | 0.982307 | 0.959549 | 140.722 | 4,284.85 | 158.39 | 3768.744 |
| DPRS | 1.480 | 0.984559 | 0.962107 | 357.578 | 4,292.76 | 730.89 | 11549.315 |
| OGSA | 3.634 | 0.979144 | 0.957347 | 122.020 | 4,269.98 | 57.95 | 4055.153 |
| EIMORM | 1.765 | 0.982437 | 0.959667 | 447.411 | 4,299.20 | 1292.99 | 7612.080 |

These are descriptive means and should be interpreted within the defined experimental design. No method should be considered universally best. In the observed final dataset:

- Proposed has the highest observed mean Reliability.
- Proposed has the highest observed mean Service Availability.
- DPRS has the lowest mean Response Time.
- OGSA has the lowest Replication Transfer Volume.
- HRS has the lowest Algorithm Decision Time.

## Reproducibility

The repository contains:

- Source code and method implementations
- Simulation and runtime components
- Workload and failure generation
- Analysis scripts
- Figure-generation scripts
- Tests
- Canonical run-level results
- Final thesis figures

The canonical run-level dataset is [results/phase23_final_run_metrics.csv](results/phase23_final_run_metrics.csv). Large raw simulation JSON/checkpoint files are intentionally excluded from Git to keep the repository lightweight.

## Figures

Final figures are provided under [results/charts/](results/charts/) in both PNG and PDF formats:

- `01_response_time`
- `02_reliability`
- `03_service_availability`
- `04_active_replica_count`
- `05_network_transfer_volume`
- `06_replication_transfer_volume`
- `07_algorithm_decision_time`

## Repository Structure

```text
docs/
results/
	phase23_final_run_metrics.csv
	charts/
scripts/
src/
tests/
README.md
.gitignore
```

## Limitations
- The evaluation is simulation-based.
- No real production cloud or edge deployment was performed.
- Results depend on the defined workloads, topology, failure scenarios, and simulation assumptions.

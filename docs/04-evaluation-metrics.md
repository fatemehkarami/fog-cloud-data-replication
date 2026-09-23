# Evaluation Metrics

All five algorithms must be evaluated using the same metrics.

Primary dissertation metrics:

1. Energy Consumption
2. Response Time
3. Data Node Load
4. Total Cost
5. Closeness Centrality
6. Reliability
7. Availability

Additional operational metrics:

8. Number of replicas
9. Number of replica creations
10. Number of replica deletions
11. Number of failed requests
12. Number of successful requests
13. Algorithm execution time

---

# 1. Energy Consumption

Unit:

Joules

Objective:

Minimize

Use the energy model defined in the dissertation.

---

# 2. Response Time

Unit:

milliseconds

Objective:

Minimize

Response time must include the components defined in the dissertation,
including queueing, read/write, and data-transfer effects.

---

# 3. Data Node Load

Objective:

Minimize

The load must consider:

- storage
- CPU
- memory
- disk I/O

Use the dissertation's load formulation.

---

# 4. Total Cost

Objective:

Minimize

Total cost consists of:

- data transfer cost
- data storage cost

Use the dissertation's cost formulation.

---

# 5. Closeness Centrality

Objective:

Maximize placement quality according to the centrality formulation
defined by the dissertation.

IMPORTANT:

Before implementation, verify the mathematical direction and
normalization of this metric.

---

# 6. Reliability

Reliability measures the probability that required data remains
accessible/usable over the evaluation period despite node failures.

The simulator must explicitly model failures.

Reliability must be calculated consistently for all five algorithms.

The exact mathematical definition must be finalized before coding.

Candidate definition:

Reliability =
successful required data-access events /
total required data-access events

However, this definition must be reviewed against the dissertation
and should not be adopted automatically.

A second possible system-level formulation is based on the probability
that at least one valid replica remains available.

This formulation must be discussed and selected before implementation.

---

# 7. Availability

Availability measures the proportion of time or requests during which
the required data service is available.

Candidate request-based definition:

Availability =
successful data-access requests /
total data-access requests

Candidate time-based definition:

Availability =
available simulation time /
total simulation time

The final definition must be selected before implementation.

All five algorithms must use exactly the same definition.

---

# 8. Failed Requests

Record:

- total requests
- successful requests
- failed requests
- failures caused by node failure
- failures caused by network failure
- failures caused by insufficient replica availability

---

# 9. Replica Count

Record:

- initial replicas
- created replicas
- deleted replicas
- final replicas
- average number of replicas

This metric helps evaluate storage overhead.

---

# 10. Statistical Evaluation

Each experiment must be repeated multiple times using independent
random seeds.

For each algorithm and metric report:

- Mean
- Standard deviation
- Minimum
- Maximum

Where appropriate, statistical significance tests should be applied.

The number of repetitions must be configurable.

---

# 11. Visualization

Generate at minimum:

1. Energy comparison
2. Response-time comparison
3. Node-load comparison
4. Cost comparison
5. Centrality comparison
6. Reliability comparison
7. Availability comparison
8. Replica-count comparison

Use identical scales and experimental conditions where meaningful.

Results should be exportable to CSV for later plotting and analysis.
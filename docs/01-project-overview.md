# Project Overview

## 1. Research Goal

The goal of this project is to develop a controlled and reproducible
simulation environment for comparing five data replication strategies
in an Edge-Cloud computing environment.

The five algorithms are:

1. HRS
2. DPRS
3. EIMORM
4. OGSA
5. Proposed NSGA-III-based dynamic replication strategy

The simulation must compare all five methods under exactly the same
system environment, dataset, workload, network topology, node
characteristics, failure model, and request patterns.

Only the replication strategy should differ between algorithms.

---

## 2. Important Research Principle

This project is intended to support a doctoral dissertation.

Therefore:

- The implementation must be reproducible.
- All assumptions must be explicitly documented.
- The simulator must not silently invent missing values.
- If an algorithm from a paper cannot be implemented unambiguously,
  the implementation must stop and report the missing information.
- The system must distinguish between:
  - information explicitly stated in the papers,
  - assumptions introduced for simulation,
  - parameters selected by the researcher.

Do NOT invent algorithmic details.

If information about HRS, DPRS, EIMORM, or OGSA is insufficient,
ask the researcher for clarification.

---

## 3. Simulation Environment

The simulator represents a heterogeneous Edge-Cloud environment.

The environment contains:

- Data Centers
- Hosts
- Data Nodes
- Data Files
- Users / Clients
- Requests
- Network connections
- Replica placements
- Node failures and recovery events

The simulator must support dynamic changes over simulation time.

---

## 4. Data Model

The simulation must represent:

### Data Files

Each file should have at least:

- FileId
- Size
- Type
- Access frequency
- Access history
- Number of users accessing the file
- Current number of replicas
- Replica locations
- Popularity / importance information

### Data Nodes

Each data node should have at least:

- NodeId
- DataCenterId
- HostId
- Storage capacity
- Used storage
- Available storage
- CPU capacity
- Memory capacity
- CPU utilization
- Memory utilization
- Read/write capacity
- Network bandwidth
- Network position
- Failure characteristics
- Current state

### Requests

Each request should contain:

- RequestId
- UserId
- FileId
- Request timestamp
- Request type
- Source node / user location
- Required file
- Completion time
- Whether the request succeeded
- Whether the request failed because of node/network failure

---

## 5. Simulation Time

The simulation must be time-aware.

Requests, replica decisions, failures, recoveries,
and replica replacement must occur according to simulation time.

The simulator should support multiple independent simulation runs.

Each run must use a configurable random seed.

---

## 6. Experimental Fairness

All five algorithms must use:

- identical data files
- identical users
- identical requests
- identical network topology
- identical node capacities
- identical failure events
- identical simulation duration
- identical random seeds where applicable

The only intended difference is the replication algorithm.

This is essential for a fair comparison.

---

## 7. Algorithms

The system must use a common interface.

Conceptually:

IReplicationAlgorithm

Each algorithm must receive the same simulation state and return
replication decisions.

The five implementations are:

- HRS
- DPRS
- EIMORM
- OGSA
- ProposedMethod

Do not allow one algorithm to access information that is unavailable
to the other algorithms unless that information is explicitly part
of that algorithm's original model.

---

## 8. Outputs

For every algorithm and every simulation run, record:

- Energy consumption
- Response time
- Data node load
- Total cost
- Closeness centrality
- Reliability
- Availability
- Number of replicas
- Number of successful requests
- Number of failed requests
- Number of replica creations
- Number of replica deletions
- Number of replica replacements
- Simulation execution time

Raw results must be saved in machine-readable format such as CSV or JSON.

---

## 9. Reproducibility

Every experiment must record:

- Algorithm name
- Experiment ID
- Random seed
- Number of nodes
- Number of files
- Number of requests
- Simulation duration
- Failure model parameters
- Algorithm parameters
- Evaluation metric values

The simulator must be capable of reproducing the same experiment
when the same configuration and random seed are provided.
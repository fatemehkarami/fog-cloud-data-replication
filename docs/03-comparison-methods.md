# Comparison Algorithms

The simulation compares the proposed method against four published
replication strategies:

1. HRS
2. DPRS
3. EIMORM
4. OGSA

The original papers are available in the project repository.

---

# 1. General Implementation Rule

For each comparison algorithm:

1. Read the corresponding paper provided in the project.
2. Identify the original algorithm.
3. Extract:
   - system model
   - input parameters
   - decision variables
   - replica-selection mechanism
   - replica-number mechanism
   - replica-placement mechanism
   - replacement mechanism
   - optimization objectives
   - constraints
   - required parameters
   - pseudocode/algorithm steps
4. Implement the algorithm as faithfully as possible.

Do NOT invent missing algorithmic details.

---

# 2. Evidence-Based Implementation

For every algorithm, create a technical specification before writing
the implementation.

The specification must contain:

## Algorithm name

## Original paper

## Problem addressed

## Inputs

## Outputs

## Decision variables

## Replica selection

## Replica number determination

## Replica placement

## Replica replacement

## Objective function(s)

## Constraints

## Parameters

## Time complexity if reported

## Assumptions

## Information missing from paper

---

# 3. Missing Information Rule

If the paper does not specify a parameter or implementation detail:

DO NOT silently invent a value.

Instead classify the issue as one of:

A. Explicitly defined in paper

B. Can be derived from paper

C. Requires a common simulation assumption

D. Cannot be determined from paper

For category D, stop implementation of that part and ask the researcher.

For category C, propose the assumption and clearly document it.

---

# 4. Fair Comparison

All algorithms must operate within the same simulation environment.

The following must remain identical:

- topology
- nodes
- node capacities
- files
- users
- requests
- request timestamps
- network bandwidth
- simulation duration
- failure events
- recovery events
- random seed
- evaluation procedure

Only the replication decision mechanism should differ.

---

# 5. Algorithm Adapter

Each algorithm must implement the common interface:

IReplicationAlgorithm

The simulator must not contain algorithm-specific logic.

Algorithm-specific behavior belongs inside the corresponding
algorithm implementation.

---

# 6. Algorithm Output

Every algorithm must return a common replication-decision structure
containing at minimum:

- replica creation decisions
- replica deletion decisions
- replica placement decisions
- replica movement/replacement decisions where applicable

If an original algorithm does not support a particular operation,
that operation must remain disabled rather than being artificially
added.

---

# 7. Required Documentation

Before implementing any comparison algorithm, Copilot must produce:

docs/algorithms/HRS-spec.md
docs/algorithms/DPRS-spec.md
docs/algorithms/EIMORM-spec.md
docs/algorithms/OGSA-spec.md

The researcher must review these specifications before implementation.
# OGSA researcher decision register

## 1. Purpose

This document exists to record the decisions that a researcher must make in order to turn the source-faithful OGSA specification and implementation boundary into an executable experimental implementation.

It is not an implementation.

This file is intentionally limited to the following source-of-truth documents:

- [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md)
- [docs/algorithms/OGSA-implementation-contract.md](docs/algorithms/OGSA-implementation-contract.md)

The purpose is not to claim that OGSA specifies more than it actually does. The purpose is to make explicit the decisions required for implementation while preserving a strict separation between:

- SOURCE_DEFINED behavior
- RESEARCHER_DEFINED choices
- SIMULATOR_DEFINED behavior
- UNRESOLVED / BLOCKED items

This document must never be presented later as though the original paper specified these decisions.

---

## 2. Decision principles

1. Source behavior must remain unchanged.
2. Missing source behavior must be explicitly labeled.
3. No decision may silently become part of the scientific definition of OGSA.
4. Researcher decisions must be reproducible.
5. Every selected value or rule must have a rationale.
6. Decisions affecting comparison fairness must be documented.
7. Experimental parameters from the paper must be distinguished from researcher-selected parameters.
8. If the source is genuinely ambiguous, the ambiguity must be preserved unless a decision is necessary for execution.

Status values used throughout:

- OPEN
- DECIDED
- BLOCKED
- NOT_APPLICABLE

At the initial creation of this file, all genuine researcher decisions are OPEN unless the value is explicitly fixed by the source experiment and does not require researcher choice.

---

## 3. Critical OGSA hybridization decision

### OGSA-RD-001 — OGSA hybrid identity ambiguity

- Topic: hybridization ambiguity
- Source-defined information:
  - OGSA-spec.md states that OGSA is a hybridization of OBL and GSA.
  - Another passage in the same source also mentions OBL + GSO.
  - OGSA-spec.md preserves the inconsistency and classifies the issue as PARTIALLY_DEFINED / UNRESOLVED.
  - OGSA-implementation-contract.md preserves the same ambiguity and prohibits silently selecting GSA or GSO as the definitive scientific identity.
- What is missing:
  - The paper does not provide a definitive, unique hybrid identity for executable implementation.
  - A definitive choice between GSA and GSO is not available without a researcher-defined project interpretation.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The optimizer identity affects how the algorithm is assembled and interpreted in an experimental implementation.
  - The source does not resolve this ambiguity on its own, so the project must make the interpretation explicit if execution proceeds.
- Researcher decision:
  - CMP-RD-013 records the project interpretation as OBL + GSA for the executable experiment, while preserving the fact that the source also mentions GSO and does not define this identity uniquely.
- Status: DECIDED — PROJECT INTERPRETATION RECORDED BY CMP-RD-013
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The source is inconsistent; therefore the scientific definition remains ambiguous unless the researcher makes an explicit project-level choice.
- Impact on reproducibility:
  - High, because different hybrid choices may materially alter the optimizer behavior and comparison fairness.

### OGSA-RD-002 — Explicit GSA equations as the executable project basis

- Topic: project basis for the optimizer
- Source-defined information:
  - OGSA-spec.md explicitly provides GSA equations for mass, acceleration, gravitational constant, velocity, and position update.
  - These formulas are source-defined and retained in the implementation contract.
- What is missing:
  - The source does not provide a definitive final answer for whether the project-level executable optimizer is to be treated as GSA-based, GSO-based, or another explicit interpretation.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - An implementation may choose to follow the explicit GSA equations while still leaving the broader hybrid identity as a project-level choice.
  - If a project adopts the GSA equations as its executable basis, the decision should be documented as a researcher-defined project interpretation rather than as source-defined OGSA behavior.
- Researcher decision:
  - CMP-RD-013 resolves the executable basis as GSA-based while preserving the source-level ambiguity in the scientific documentation.
- Status: DECIDED — PROJECT BASIS RECORDED BY CMP-RD-013
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper provides GSA equations, but the hybrid naming inconsistency remains unresolved in the source itself.
- Impact on reproducibility:
  - Medium, because it affects interpretation and may affect reproduction if the implementation is later described as if it were source-defined behavior.

---

## 4. Search / solution representation decisions

### OGSA-RD-003 — Binary assignment matrix representation

- Topic: internal representation of Ψ
- Source-defined information:
  - OGSA-spec.md defines Ψij as a binary file-to-data-node assignment matrix.
  - Ψij = 1 if file Fi is assigned to data node DNj.
  - Ψij = 0 otherwise.
  - Integrity constraint: Σ_j Ψij > 0
  - Capacity constraint: Σ_i Ψij × S_i ≤ C_j
- What is missing:
  - The source does not define how a binary assignment matrix is encoded internally for a continuous optimization algorithm.
  - The source does not define how a GSA particle position is converted into valid binary Ψ values.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A numerical optimizer needs a concrete internal representation and conversion mechanism.
- Researcher decision required:
  - The researcher must choose an internal representation and conversion rule for extracting a valid binary assignment from optimizer positions.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The scientific claim is only that Ψ exists as a binary assignment matrix; the implementation must still choose a representation strategy.
- Impact on reproducibility:
  - High, because the representation and conversion method directly affects the search behavior and objective evaluation.

### OGSA-RD-004 — Continuous-to-binary conversion method

- Topic: conversion from GSA position updates to valid Ψ
- Source-defined information:
  - OGSA simulation updates positions through GSA equations.
  - The source does not define how these continuous position values map to binary assignments.
- What is missing:
  - There is no source-defined conversion function from a continuous position vector into decisive binary file-to-node assignments.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - GSA position updates produce continuous values, but the optimization problem is defined on binary assignment values.
- Researcher decision required:
  - The researcher must define the conversion rule used to map continuous positions to binary assignments.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The source defines the decision problem but not the encoding strategy.
- Impact on reproducibility:
  - High.

### OGSA-RD-005 — Constraint enforcement after position update

- Topic: feasibility of candidate solutions
- Source-defined information:
  - OGSA-spec.md states the integrity and capacity constraints.
- What is missing:
  - The source does not specify whether candidate solutions are repaired, clipped, resampled, or rejected after GSA updates.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Any executable optimizer must handle infeasible solutions after updates.
- Researcher decision required:
  - The researcher must define how infeasible solutions are handled.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper defines constraints but not an implementation mechanism for enforcing them.
- Impact on reproducibility:
  - High.

### OGSA-RD-006 — Invalid candidate-solution handling

- Topic: invalid solutions
- Source-defined information:
  - Candidate solutions must satisfy integrity and capacity constraints.
- What is missing:
  - There is no source-defined invalid-solution policy.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A numerical implementation must decide how to treat candidate solutions that violate constraints.
- Researcher decision required:
  - The researcher must decide whether invalid solutions are rejected, repaired, or penalized in the objective evaluation.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper specifies what is valid, but not how invalid states are processed.
- Impact on reproducibility:
  - High.

---

## 5. Initial population decisions

### OGSA-RD-007 — Initial solution generation

- Topic: initialization procedure
- Source-defined information:
  - OGSA-spec.md says the initial solution is randomly generated based on the number of files and data nodes.
  - A table of example file-to-node assignments is provided.
- What is missing:
  - The source does not specify the exact random-generation method.
  - The source does not specify whether every initial solution must satisfy constraints before evaluation.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The algorithm needs a concrete initialization procedure for an executable implementation.
- Researcher decision required:
  - The researcher must define the exact initialization process and whether feasibility is enforced during initialization.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper gives the concept of random generation but not the implementation mechanics.
- Impact on reproducibility:
  - High.

### OGSA-RD-008 — Feasibility of initial population

- Topic: initial population validity
- Source-defined information:
  - The source imposes integrity and capacity constraints.
- What is missing:
  - The source does not specify whether every initial solution is checked against these constraints before first evaluation.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The optimizer requires a valid starting state if the source constraints are to be enforced.
- Researcher decision required:
  - The researcher must define how the initial population is generated so that it is feasible, or how infeasible initial solutions are handled.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Initialization feasibility is not a source-defined algorithmic step.
- Impact on reproducibility:
  - High.

### OGSA-RD-009 — Distribution of initial assignments

- Topic: random assignment distribution
- Source-defined information:
  - The initial solution is random.
- What is missing:
  - The source does not specify how random assignments are distributed across nodes or files.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Different distributions influence search behavior and fairness.
- Researcher decision required:
  - The researcher must define the distribution rule or generator used for random assignment.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Randomness is source-defined, but its exact implementation is not.
- Impact on reproducibility:
  - High.

---

## 6. OBL decisions

### OGSA-RD-010 — OBL equation itself

- Topic: opposite solution generation
- Source-defined information:
  - OGSA-spec.md explicitly gives: oS_id = L_d + U_d − S_id
- What is missing:
  - The source does not define how this equation applies to binary assignment matrices or to the continuous optimizer representation.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - An executable implementation must define how this opposite-solution concept is applied to the actual representation of candidate solutions.
- Researcher decision required:
  - The researcher must define how OBL operates in the project-specific representation of Ψ and of each candidate solution.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The formula is source-defined, but its use in a concrete optimizer representation is not.
- Impact on reproducibility:
  - High.

### OGSA-RD-011 — Opposite-solution feasibility

- Topic: valid opposite solutions
- Source-defined information:
  - OBL is part of the algorithm.
- What is missing:
  - The source does not define whether the opposite solution must satisfy integrity and capacity constraints before evaluation.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Opposite generation can yield invalid assignment states unless feasibility handling is defined.
- Researcher decision required:
  - The researcher must define how opposite solutions are checked and, if necessary, repaired or rejected.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The source defines OBL but not feasibility treatment of the resulting solution.
- Impact on reproducibility:
  - High.

### OGSA-RD-012 — OBL timing relative to feasibility

- Topic: ordering of steps
- Source-defined information:
  - The paper lists solution initialization, opposite generation, fitness evaluation, and iterative updates.
- What is missing:
  - The source does not specify whether OBL is applied before or after constraints are enforced.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Ordering changes feasibility and objective evaluation.
- Researcher decision required:
  - The researcher must choose the execution order.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The ordering is part of executable behavior but not source-defined behavior.
- Impact on reproducibility:
  - High.

---

## 7. Fitness / objective decisions

### OGSA-RD-013 — Objective scaling / normalization policy

- Topic: objective formulation and scalarization treatment
- Source-defined information:
  - OGSA-spec.md defines MOF(Ψ) = α1U1 + α2U2 + α3U3 + α4U4 + α5U5.
  - The paper reports α1 = α2 = α3 = α4 = α5 = 0.2.
  - The objectives are MFU, MST, LV, EC, and ML.
- What is missing:
  - The source does not define whether objective values are normalized, rescaled, or evaluated in raw units when combined into the weighted sum.
  - Scaling and normalization are not source-defined OGSA behavior.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Different objectives may have different numerical magnitudes, so a project must state whether it uses raw values or applies a custom scaling or normalization scheme.
  - If a scaling or normalization policy is introduced, it must be documented as a researcher-defined implementation adaptation and not as source-defined OGSA behavior.
- Researcher decision required:
  - The researcher must decide whether objective values are used directly in the weighted sum or whether an implementation-specific scaling or normalization scheme is introduced.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper defines the weighted sum but not any scale-handling policy, and scaling/normalization is not itself part of the source-defined OGSA scientific behavior.
- Impact on reproducibility:
  - High.

### OGSA-RD-014 — Handling undefined mathematical cases

- Topic: objective evaluation edge cases
- Source-defined information:
  - Objective formulas include denominators and sums.
- What is missing:
  - The source does not define what to do if denominators are zero or an objective produces an undefined value.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Real implementations require a numerical handling policy for invalid values, even though this is not a source-defined mathematical rule.
- Researcher decision required:
  - The researcher must decide how undefined objective cases are handled.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The equations are source-defined, but their numerical edge-case handling is not.
- Impact on reproducibility:
  - Medium.

---

## 8. MFU / availability decisions

### OGSA-RD-15 — Operational interpretation of MFU

- Topic: availability objective interpretation
- Source-defined information:
  - The paper defines file unavailability with the product of assignment values and failure probabilities.
- What is missing:
  - The source does not specify how this is operationalized for multiple replicas or for partial assignments in a real implementation.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A concrete implementation must decide how availability is computed from a candidate assignment matrix.
- Researcher decision required:
  - The researcher must specify how MFU is evaluated for the implementation.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The source defines the formula conceptually but not a runtime evaluation rule for all edge cases.
- Impact on reproducibility:
  - Medium to high.

### OGSA-RD-16 — Zero or invalid assignment handling in availability

- Topic: numerical edge cases
- Source-defined information:
  - Ψij is binary and may be 0 or 1.
- What is missing:
  - The source does not define the behavior for zero or invalid assignment sets in the availability model.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - An implementation must decide how to handle zero-product or null assignment cases.
- Researcher decision required:
  - The researcher must define handling for zero or invalid assignment cases.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The formula is given, but edge-case handling is not.
- Impact on reproducibility:
  - Medium.

---

## 9. MST decisions

### OGSA-RD-17 — Interpretation of A(i,j) and A(i)

- Topic: mean service time evaluation
- Source-defined information:
  - MST depends on A(i,j), A(i), S_i, and TR_j.
- What is missing:
  - The source does not define the exact operational meaning of A(i,j) or A(i) beyond their role in the formula.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Without an exact interpretation, the service-time calculation cannot be implemented deterministically.
- Researcher decision required:
  - The researcher must define the operational source of A(i,j) and how A(i) is computed.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper names the variables but does not define their runtime meaning fully.
- Impact on reproducibility:
  - High.

### OGSA-RD-18 — Zero-access-rate handling in MST

- Topic: service-time numerical edge cases
- Source-defined information:
  - ST(i) uses A(i,j) / A(i).
- What is missing:
  - The source does not specify the handling of zero or undefined access-rate values.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Division by zero or zero access-rate leads to undefined behavior.
- Researcher decision required:
  - The researcher must define how such cases are processed.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Exact numerical edge handling is not source-defined.
- Impact on reproducibility:
  - Medium.

---

## 10. Load variance decisions

### OGSA-RD-19 — Load interpretation

- Topic: operational meaning of L(i,j)
- Source-defined information:
  - L(i,j) = A(i,j) × ST(i,j)
  - L_j = Σ_i L(i,j)
  - L = (1/m) × Σ_j L_j
  - LV = U3(Ψ) = Σ_j (L_j − L)^2 / (m − 1)
- What is missing:
  - The source does not define how load is accumulated or how node load is measured during execution.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The optimizer needs a concrete means of computing node load from the assignment and the runtime state.
- Researcher decision required:
  - The researcher must define the operational interpretation of node load in the implementation.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The mathematical formula exists, but the operational runtime semantics are not given.
- Impact on reproducibility:
  - High.

### OGSA-RD-20 — m <= 1 case in variance

- Topic: edge-case handling
- Source-defined information:
  - LV uses denominator m − 1.
- What is missing:
  - The source does not define the handling for m <= 1.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Division by zero or negative denominator is invalid.
- Researcher decision required:
  - The researcher must specify the behavior for m <= 1.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - This is a general numerical edge case not handled in the paper.
- Impact on reproducibility:
  - Low to medium.

---

## 11. Energy decisions

### OGSA-RD-21 — Energy objective interpretation

- Topic: EC model
- Source-defined information:
  - OGSA-spec.md preserves the source expression for EC and explicitly notes that the extracted formula is partially unclear.
- What is missing:
  - The exact operational meaning of the expression and the various terms is not fully clear.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A direct implementation cannot be guaranteed without a researcher-defined interpretation of the partially damaged formula.
- Researcher decision required:
  - The researcher must decide how to interpret and compute EC for implementation, while preserving the source formula as the scientific basis.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The source gives the objective but not a fully unambiguous implementation-ready expression.
- Impact on reproducibility:
  - High.

### OGSA-RD-22 — Energy edge-case handling

- Topic: edge cases in the energy objective
- Source-defined information:
  - The formula includes terms such as Q, Pmax(j), and Pidle(j).
- What is missing:
  - The source does not define handling when Q is undefined or zero, or when power values are missing.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The formula must be evaluated in a concrete runtime environment.
- Researcher decision required:
  - The researcher must define how missing or zero quantities are handled.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper defines the objective but not every numerical edge case.
- Impact on reproducibility:
  - Medium.

---

## 12. Latency decisions

### OGSA-RD-23 — Interactive meaning of r and B_j in ML

- Topic: latency model interpretation
- Source-defined information:
  - OGSA-spec.md preserves the latency expression involving r, B_j, A(i,j), and S_i.
- What is missing:
  - The exact operational meaning of r and B_j is not fully defined beyond the notation used in the paper.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A concrete latency calculation needs a runtime definition for each variable.
- Researcher decision required:
  - The researcher must define the operational semantics of r and B_j in the implementation.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The formulas exist, but some variables are not fully operationalized in the source.
- Impact on reproducibility:
  - High.

### OGSA-RD-24 — Zero bandwidth handling in latency

- Topic: numerical edge cases
- Source-defined information:
  - Latency depends on B_j and assigns larger bandwidth to lower latency.
- What is missing:
  - The source does not define handling when B_j = 0.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Division by zero would otherwise be undefined.
- Researcher decision required:
  - The researcher must define the behavior in such cases.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The source names the variable but not the edge-case handling.
- Impact on reproducibility:
  - Medium.

---

## 13. Replica count decision

### OGSA-RD-25 — Source-defined replica-count problem without a source formula

- Topic: replica count interpretation
- Source-defined information:
  - OGSA-spec.md states that the paper identifies the challenge of deciding how many replicas should be created.
  - The source also states that the assignment matrix Ψ implicitly represents placement but does not provide a direct target replica-count formula.
- What is missing:
  - There is no direct source-defined formula for the number of replicas per file.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - An executable implementation must decide how to interpret the assignment matrix in terms of replica count and replica creation actions.
- Researcher decision required:
  - The researcher must decide how replica count is interpreted from Ψ for the experiment.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The problem is acknowledged, but the exact count policy is not source-defined.
- Impact on reproducibility:
  - High.

### OGSA-RD-26 — No source replication factor

- Topic: replication factor
- Source-defined information:
  - The source does not provide an explicit replication-factor formula.
- What is missing:
  - There is no direct replication-factor equation in OGSA-spec.md or the implementation contract.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A researcher must decide whether a replication factor will exist at all and how it is computed.
- Researcher decision required:
  - The researcher must decide whether a project-specific replication factor is introduced.
- Status: OPEN
- Source status: UNRESOLVED / BLOCKED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The source explicitly lacks a direct replication-factor policy.
- Impact on reproducibility:
  - High.

---

## 14. Replica creation decision

### OGSA-RD-27 — Translate assignment to runtime replica creation

- Topic: creation action
- Source-defined information:
  - The paper describes assignment as the solution representation and says that replicas are generated through the optimization outcome.
- What is missing:
  - The source does not define a runtime create/no-create rule or trigger.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The simulator must know when and how to create a replica in practice.
- Researcher decision required:
  - The researcher must decide how an optimized Ψ assignment is translated into concrete simulator-level creation actions.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The optimization defines assignment, but runtime creation is not source-defined.
- Impact on reproducibility:
  - High.

---

## 15. Placement / node selection decision

### OGSA-RD-28 — Translate Ψ into simulator-level placement

- Topic: placement execution
- Source-defined information:
  - Placement is represented by the assignment matrix Ψ.
  - The source-faithful baseline contains no additional placement heuristic.
- What is missing:
  - The source does not define any standalone placement heuristic beyond the assignment model itself.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The simulator must still know how to interpret the optimized assignment matrix in a runtime environment, even though the default source-faithful baseline does not add a placement heuristic.
- Researcher decision required:
  - The researcher must decide how the optimized Ψ assignment will be used to place replicas in the simulator.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The placement problem is source-defined as an assignment problem, but the runtime realization is not. A default source-faithful baseline contains no additional placement heuristic.
- Impact on reproducibility:
  - High.

### OGSA-RD-29 — Placement heuristics are not source-defined OGSA behavior

- Topic: placement-policy guardrail
- Source-defined information:
  - The source does not define nearest-node, cheapest-node, least-loaded-node, highest-availability, random, ranking, or weighted placement heuristics.
- What is missing:
  - Any such heuristic would be a researcher-defined addition.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A project may choose to add a placement heuristic, but such a choice is not source-defined OGSA behavior and must be documented as a researcher-defined extension.
- Researcher decision required:
  - If a placement heuristic is later introduced, it must be explicitly recorded as RESEARCHER_DEFINED and must never be described as OGSA source behavior.
- Status: OPEN
- Source status: UNRESOLVED / BLOCKED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The project must preserve a scientific boundary between source behavior and project-defined behavior.
- Impact on reproducibility:
  - High if introduced without explicit documentation.

---

## 16. Failure / recovery decisions

### OGSA-RD-30 — Failure simulation model

- Topic: runtime failure behavior
- Source-defined information:
  - The source uses failure probability as a parameter in the availability model.
- What is missing:
  - The source does not provide a failure detector, failure distribution, or recovery policy.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - If failures are to be simulated, the model must be defined.
- Researcher decision required:
  - The researcher must decide whether failure is only an optimization input, or whether runtime failures are simulated in the experiment.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The source includes failure probability, but not the runtime failure logic.
- Impact on reproducibility:
  - High.

### OGSA-RD-31 — Recovery policy

- Topic: recovery behavior
- Source-defined information:
  - The source does not define a recovery algorithm.
- What is missing:
  - Recovery method, failed-node handling, and repair process are not specified.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A runtime implementation requires a recovery policy if failures are simulated.
- Researcher decision required:
  - The researcher must define whether recovery is part of the experiment and how it is implemented.
- Status: OPEN
- Source status: UNRESOLVED / BLOCKED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Recovery is not a source-defined behavior.
- Impact on reproducibility:
  - High.

---

## 17. Deletion / replacement decisions

### OGSA-RD-32 — Deletion policy

- Topic: replica deletion
- Source-defined information:
  - OGSA-spec.md states that the source does not provide a deletion or replacement policy.
- What is missing:
  - No trigger, target, or rule is defined.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A runtime simulator may require replica deletion logic if it models dynamic state changes.
- Researcher decision required:
  - The researcher must decide whether deletion is part of the experimental implementation and, if so, how it is defined.
- Status: OPEN
- Source status: UNRESOLVED / BLOCKED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Deletion is not source-defined and must not be silently introduced.
- Impact on reproducibility:
  - High.

### OGSA-RD-33 — Replacement policy

- Topic: replica replacement
- Source-defined information:
  - No source-defined replacement rule exists.
- What is missing:
  - There is no target-selection rule for replacement.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - If the simulator supports deletion, replacement must also be specified.
- Researcher decision required:
  - The researcher must define replacement semantics if a dynamic setting is used.
- Status: OPEN
- Source status: UNRESOLVED / BLOCKED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Replacement is outside the source-defined scientific content.
- Impact on reproducibility:
  - High.

---

## 18. Dynamic replication decisions

### OGSA-RD-34 — Iterative optimizer vs runtime dynamic replication

- Topic: dynamic behavior distinction
- Source-defined information:
  - The paper defines an iterative optimization loop over generations.
  - OGSA-spec.md distinguishes this from a runtime dynamic re-replication schedule.
- What is missing:
  - The source does not provide a trigger for runtime re-optimization outside the optimizer loop.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A project may choose to run OGSA periodically or on events, but this is not source-defined.
- Researcher decision required:
  - The researcher must decide whether the experimental implementation runs OGSA once per workload, repeatedly, or on some schedule.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Iterative optimization is source-defined; runtime dynamic trigger policy is not.
- Impact on reproducibility:
  - High.

### OGSA-RD-35 — Re-optimization trigger

- Topic: event-based execution
- Source-defined information:
  - No runtime trigger is source-defined.
- What is missing:
  - No periodic, request-driven, or event-driven trigger is provided.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - An implementation that executes the optimizer repeatedly must define a trigger.
- Researcher decision required:
  - The researcher must define any runtime trigger used in the experimental execution.
- Status: OPEN
- Source status: UNRESOLVED / BLOCKED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - A trigger is not a paper-defined algorithmic component.
- Impact on reproducibility:
  - High.

---

## 19. GSA parameter decisions

### OGSA-RD-36 — gmax, yL, and yU

- Topic: gravitational constant initialization
- Source-defined information:
  - G0 = g_max(y_U − y_L)
- What is missing:
  - The source does not define the exact operational meaning of gmax, yL, or yU beyond the notation.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The implementation needs concrete values or semantics.
- Researcher decision required:
  - The researcher must decide how gmax, yL, and yU are defined for the project-level optimizer.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper gives the symbolic equation but not a definitive numerical or semantic definition.
- Impact on reproducibility:
  - High.

### OGSA-RD-37 — epsilon and distance interpretation

- Topic: numerical stability and distance semantics
- Source-defined information:
  - The acceleration equation includes ε and R_ij(k).
- What is missing:
  - The source does not define all parameter semantics for ε and R_ij.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Numeric stability and distance definition are required in a concrete implementation.
- Researcher decision required:
  - The researcher must define epsilon handling and the distance computation used in the project.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The formula exists but the concrete numerical semantics are not fully specified by the paper.
- Impact on reproducibility:
  - High.

### OGSA-RD-38 — best_fit == worst_fit handling

- Topic: mass calculation edge case
- Source-defined information:
  - Mass is computed using best_fit and worst_fit.
- What is missing:
  - The source does not define what happens when best_fit = worst_fit.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Division by zero or degenerate mass values must be handled explicitly.
- Researcher decision required:
  - The researcher must define the behavior when best_fit == worst_fit.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Numerical edge cases are not addressed by the source paper.
- Impact on reproducibility:
  - Medium.

### OGSA-RD-39 — gbest selection rule

- Topic: elite agent selection
- Source-defined information:
  - The paper states that g is the set of the first 2% agents with the best fitness and biggest mass.
- What is missing:
  - The source does not define detailed tie-breaking or selection behavior inside this group.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The implementation must determine how the elite set is chosen in practice.
- Researcher decision required:
  - The researcher must define the precise gbest selection method.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The source names the elite group but not the exact selection procedure at runtime.
- Impact on reproducibility:
  - High.

### OGSA-RD-40 — random-number generation and tie-breaking semantics

- Topic: stochastic behavior
- Source-defined information:
  - rand is described as a uniform random number in [0,1].
- What is missing:
  - The source does not define the random generator, seeds, or tie-breaking semantics.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A deterministic implementation requires a reproducible random policy.
- Researcher decision required:
  - The researcher must define the random generator and seed policy for the experiment.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Randomness is present in the algorithm, but the exact generator and reproducibility policy are not source-defined.
- Impact on reproducibility:
  - High.

---

## 20. Experimental parameter decisions

### OGSA-RD-42 — Source-reported experiment values vs general algorithm requirements

- Topic: parameter separation
- Source-defined information:
  - OGSA-spec.md lists multiple reported values including 8 data nodes, 200 generations, population size 20, non-uniformity = 2, α = 0.2, and the specific node and network parameters.
- What is missing:
  - The paper does not define a general universal parameter set for all possible deployments.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The implementation needs a concrete experiment design.
- Researcher decision required:
  - The researcher must decide which values are used for the specific implementation and which remain experiment-specific.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper gives example values, not a universal algorithm specification.
- Impact on reproducibility:
  - High.

### OGSA-RD-43 — Number of files and workload generation

- Topic: dataset construction
- Source-defined information:
  - The source defines a file set and a node set, but not a workload generator.
- What is missing:
  - No file-count distribution, storage-generation process, or access-pattern generator is specified.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A concrete experiment needs a workload and dataset definition.
- Researcher decision required:
  - The researcher must define file counts, file-size distribution, and access-rate generation for the experiment.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper names the variables but not the workload-generation rules.
- Impact on reproducibility:
  - High.

### OGSA-RD-44 — Random seed and repetition policy

- Topic: stochastic reproducibility
- Source-defined information:
  - rand is a uniform random value in [0,1].
- What is missing:
  - The source does not define random seed identity, run count, or statistical reporting policy.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A reproducible experimental setup requires a defined random-policy and replication strategy.
- Researcher decision required:
  - The researcher must choose the seed policy and repetition scheme.
- Status: OPEN
- Source status: SOURCE_DEFINED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The algorithm is stochastic but the paper does not specify the experimental reproduction policy.
- Impact on reproducibility:
  - High.

---

## 22. Simulator integration decisions

### OGSA-RD-45 — Simulator input adapter

- Topic: integration with the common simulator
- Source-defined information:
  - OGSA-spec.md and the implementation contract describe what algorithm inputs are needed.
- What is missing:
  - The source does not define how the simulator provides these inputs to OGSA at runtime.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - An experimental implementation requires a mapping layer between simulator state and OGSA optimization data.
- Researcher decision required:
  - The researcher must define the simulator-to-OGSA adapter contract for the implementation.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Input semantics are source-defined, but the adapter design is not.
- Impact on reproducibility:
  - High.

### OGSA-RD-46 — Simulator output adapter

- Topic: return values to the simulator
- Source-defined information:
  - The implementation contract defines conceptual outputs: final assignment and objective values.
- What is missing:
  - The source does not define exactly how these outputs are serialized or handed back to the simulator.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - The simulator must know how to consume optimization results.
- Researcher decision required:
  - The researcher must define the simulator output mapping.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The algorithm outcome is source-defined, but the runtime interface is not.
- Impact on reproducibility:
  - Medium.

### OGSA-RD-47 — Runtime placement execution model

- Topic: simulator-level placement action
- Source-defined information:
  - Placement is represented by Ψ.
- What is missing:
  - The paper does not define the mechanism by which the chosen assignment is realized in the simulator.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - A working implementation must map the optimized assignment onto the simulator's state.
- Researcher decision required:
  - The researcher must define how the optimized assignment is realized in the project runtime.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Source behavior stops at the assignment model; runtime realization is outside the source paper.
- Impact on reproducibility:
  - High.

---

## 23. Comparison fairness decisions

### OGSA-RD-48 — Fair comparison setup

- Topic: external evaluation fairness
- Source-defined information:
  - OGSA is compared against GSA-based data replication and an MOE method in the paper.
- What is missing:
  - The source does not define a common dataset, common topology, or common runtime environment for cross-algorithm comparison.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Fairness in any comparison requires common assumptions and setup.
- Researcher decision required:
  - The researcher must decide the comparison protocol and fairness conditions for experimental evaluation.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - Comparison fairness is an experimental design requirement, not a source-defined OGSA property.
- Impact on reproducibility:
  - High.

### OGSA-RD-49 — Evaluation metrics and reporting policy

- Topic: statistical evaluation
- Source-defined information:
  - The paper reports objective values and comparison figures for media such as unavailability, latency, service time, load variance, and energy consumption.
- What is missing:
  - The source does not define number of runs, confidence intervals, or statistical reporting policy.
- Why an executable implementation or reproducible experiment requires an explicit policy:
  - Executable experimentation needs a reporting plan.
- Researcher decision required:
  - The researcher must define the evaluation protocol and statistical reporting method.
- Status: OPEN
- Source status: SOURCE_DEFINED_BUT_PARTIALLY_SPECIFIED
- Researcher status: RESEARCHER_DEFINED
- Rationale:
  - The paper contains experimental results but not a formal reproducibility and reporting policy.
- Impact on reproducibility:
  - High.

---

## 24. Decision register

| ID | Decision | Source-defined information | Missing information | Decision required | Status | Rationale | Impact on reproducibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OGSA-RD-001 | OGSA hybrid identity | OBL + GSA and OBL + GSO are both mentioned | definitive identity not resolved | choose implementation identity if needed | OPEN | source inconsistency | High |
| OGSA-RD-002 | GSA equations as implementation basis | explicit GSA equations exist | hybrid identity remains ambiguous | decide whether GSA is the project basis | OPEN | paper provides GSA equations | Medium |
| OGSA-RD-003 | Ψ representation | Ψ is binary assignment matrix | internal representation not defined | define representation strategy | OPEN | binary model is source-defined | High |
| OGSA-RD-004 | Continuous-to-binary conversion | Ψ is binary, but not how to encode | conversion rule missing | define conversion rule | OPEN | GSA positions are continuous | High |
| OGSA-RD-005 | constraint enforcement | constraints exist | enforcement mechanism missing | define enforcement method | OPEN | paper states constraints only | High |
| OGSA-RD-006 | invalid candidate handling | invalid states are not allowed | policy missing | define handling behavior | OPEN | source does not specify | High |
| OGSA-RD-007 | initialization procedure | random generation is source-defined | exact procedure missing | define random generation policy | OPEN | source is conceptual | High |
| OGSA-RD-008 | initialization feasibility | constraints are defined | feasibility enforcement unspecified | define initialization policy | OPEN | source does not specify | High |
| OGSA-RD-009 | initial assignment distribution | random assignment is source-defined | distribution not defined | define random distribution | OPEN | source does not specify | High |
| OGSA-RD-010 | OBL application | opposite-solution equation is source-defined | use within representation not defined | define OBL mapping | OPEN | OBL formula is source-defined | High |
| OGSA-RD-011 | opposite-solution feasibility | OBL exists | feasibility policy missing | define feasibility policy | OPEN | not given by source | High |
| OGSA-RD-012 | OBL ordering | source flow implies order | ordering not specified | decide OBL timing | OPEN | step ordering is not explicit | High |
| OGSA-RD-013 | weighted objective use | MOF formula is source-defined | scaling policy missing | define scalarization handling | OPEN | objective scales may differ | High |
| OGSA-RD-014 | undefined objective cases | formulas exist | edge-case handling missing | define numerical policy | OPEN | paper does not specify | Medium |
| OGSA-RD-15 | MFU operationalization | conceptual formula exists | runtime semantics not fully defined | define evaluation method | OPEN | mixed notation / OCR | Medium-high |
| OGSA-RD-16 | MFU edge cases | Ψ is binary | zero/invalid assignment handling missing | define edge handling | OPEN | not specified | Medium |
| OGSA-RD-17 | A(i,j) and A(i) | variables and formulas exist | precise semantic interpretation missing | define source of A(i,j) and A(i) | OPEN | not fully specified | High |
| OGSA-RD-18 | zero-access-rate handling | formulas exist | undefined behavior not specified | define zero-rate handling | OPEN | not specified | Medium |
| OGSA-RD-19 | load interpretation | formula exists | runtime load semantics missing | define node-load semantics | OPEN | not specified | High |
| OGSA-RD-20 | variance denominator edge case | LV formula exists | m<=1 case unspecified | define edge behavior | OPEN | not specified | Low-medium |
| OGSA-RD-21 | EC interpretation | expression exists | source is partially unclear | define implementation interpretation | OPEN | OCR ambiguity remains | High |
| OGSA-RD-22 | EC numerical edge cases | objective exists | zero/missing power values not handled | define edge handling | OPEN | not specified | Medium |
| OGSA-RD-23 | ML variable semantics | formulas exist | r and B_j meaning not fully clear | define runtime semantics | OPEN | source notation incomplete | High |
| OGSA-RD-24 | ML bandwidth edge case | B_j is used | zero bandwidth not addressed | define edge-case handling | OPEN | not specified | Medium |
| OGSA-RD-25 | replica count interpretation | problem is recognized | no explicit source formula | decide how Ψ implies count | OPEN | source is incomplete | High |
| OGSA-RD-26 | source replication factor | absent | no formula given | decide whether to add one | OPEN | not source-defined | High |
| OGSA-RD-27 | creation action | optimization assignment exists | runtime create/no-create is missing | define mapping to runtime action | OPEN | no source rule | High |
| OGSA-RD-28 | placement execution | Ψ is placement model | not how to realize placement | define placement mapping | OPEN | runtime realization not source-defined | High |
| OGSA-RD-29 | placement heuristics guardrail | heuristics are prohibited by source | researcher may choose them | decide if any heuristic is allowed | OPEN | project choice only | High |
| OGSA-RD-30 | failure simulation model | failure probability is source-known | fail model missing | decide whether failures are simulated | OPEN | not source-defined | High |
| OGSA-RD-31 | recovery policy | no recovery policy source-defined | recovery absent | decide if recovery exists | OPEN | absent from source | High |
| OGSA-RD-32 | deletion policy | deletion not specified | trigger/target not specified | decide if deletion is part of experiment | OPEN | source absent | High |
| OGSA-RD-33 | replacement policy | replacement not specified | no policy provided | define if needed | OPEN | source absent | High |
| OGSA-RD-34 | optimizer repetition policy | iterative loop is source-defined | runtime trigger not defined | decide single vs repeated runs | OPEN | not source-defined | High |
| OGSA-RD-35 | re-optimization trigger | no trigger is source-defined | trigger absent | define runtime trigger if needed | OPEN | not source-defined | High |
| OGSA-RD-36 | gmax/yL/yU semantics | symbolic equation exists | exact runtime meaning missing | define values or semantics | OPEN | not fully specified | High |
| OGSA-RD-37 | epsilon and distance semantics | formula exists | missing parameter semantics | define epsilon and Rij handling | OPEN | not specified | High |
| OGSA-RD-38 | best_fit == worst_fit | formula exists | degenerate case not specified | define degenerate handling | OPEN | not specified | Medium |
| OGSA-RD-39 | gbest selection | elite set exists | exact selection procedure missing | define elite set rule | OPEN | not specified | High |
| OGSA-RD-40 | random generator and reproducibility | rand in [0,1] | seed / generator policy missing | define random-policy | OPEN | not source-defined | High |
| OGSA-RD-42 | source experimental values vs general config | values are reported | universal constants not defined | separate experiment values from general settings | OPEN | source-specific examples | High |
| OGSA-RD-43 | file count and workload generation | file sets exist | workload model absent | define dataset generation | OPEN | not in source | High |
| OGSA-RD-44 | random seed and repetition | stochastic algorithm exists | run policy undefined | define seed/repetition policy | OPEN | not in source | High |
| OGSA-RD-45 | simulator input adapter | input structure is known | adapter design absent | define adapter mapping | OPEN | project-specific integration | High |
| OGSA-RD-46 | simulator output adapter | output concept is known | serialization mapping missing | define output mapping | OPEN | project-specific integration | Medium |
| OGSA-RD-47 | runtime placement execution | Ψ placement exists | realization in simulator missing | define simulator realization | OPEN | project-specific integration | High |
| OGSA-RD-48 | fair comparison setup | source compares to other methods | common experiment design absent | define comparison fairness | OPEN | not source-defined | High |
| OGSA-RD-49 | evaluation/reproducibility policy | figures exist | exact reporting policy absent | define number of runs and reporting | OPEN | not source-defined | High |

---

## 25. Decision dependencies

| Dependency | Depends on | Notes |
| --- | --- | --- |
| Hybridization | source ambiguity | researcher choice if implementation proceeds |
| Optimizer representation | hybridization | affects encoding strategy |
| Binary conversion | optimizer representation | required for Ψ and GSA interaction |
| Constraint enforcement | binary conversion | needed for valid candidate generation |
| Fitness evaluation | constraints and representation | depends on objective semantics |
| Replica count interpretation | fitness and decision representation | not source-defined |
| Placement execution | replica interpretation | project-level mapping |
| Runtime simulator integration | placement execution | simulator-specific |
| Experimental comparison | runtime setup and fairness | not source-defined |

This dependency map is a researcher implementation dependency map and must not be mistaken for a source-defined scientific dependency.

---

## 26. Recommended decision order

Stage 1 — Mathematical executability
- Confirm the exact mathematical objects that must be implemented.
- Identify the source-defined equations and unresolved edge cases.

Stage 2 — Solution representation
- Decide the internal representation of Ψ and the continuous-to-binary mapping.
- Establish how candidate feasibility is checked.

Stage 3 — Optimizer mechanics
- Decide the hybrid identity to be used in the project, if required.
- Define GSA parameter semantics and elite-set behavior.

Stage 4 — Replica interpretation
- Decide how Ψ corresponds to replica count and creation actions.
- Define how placement is realized in the simulator.

Stage 5 — Runtime integration
- Define how the optimizer communicates with the simulator.
- Decide how results are consumed and stored.

Stage 6 — Failure / dynamic behavior
- Decide whether failures and dynamic re-optimization are included in the experiment.

Stage 7 — Experimental configuration
- Define the dataset, workload, repetition policy, and criteria for comparison.

Stage 8 — Fair comparison
- Document common assumptions across compared methods and report any deviations.

This is a recommended order for researcher decisions only. It is not source-defined OGSA behavior.

---

## 27. Prohibited researcher shortcuts

The following may not be silently chosen as if they were part of the source paper:

- NSGA-II
- NSGA-III
- Pareto dominance
- a different scalarization
- normalized objectives
- standard GSA implementation
- standard GSO implementation
- arbitrary replica factor
- nearest-node placement
- cheapest-node placement
- least-loaded-node placement
- highest-availability placement
- random placement
- EIMORM IEK
- EIMORM popularity score
- EIMORM ETBDF
- EIMORM EARF
- arbitrary failure recovery
- arbitrary deletion
- arbitrary runtime trigger

If any of these are eventually selected, they must be recorded explicitly as researcher-defined modifications/extensions and cannot be presented as OGSA-source behavior.

---

## 28. Source vs researcher vs simulator matrix

| Capability | Source-defined? | Researcher decision needed? | Simulator decision needed? | Current status |
| --- | --- | --- | --- | --- |
| Ψ representation | Yes | Yes | No | OPEN |
| constraints | Yes | No | No | SOURCE_DEFINED |
| initialization | Yes, conceptually | Yes | No | OPEN |
| OBL | Yes | Yes | No | OPEN |
| MFU | Yes, conceptually | Yes | No | OPEN |
| MST | Yes | Yes | No | OPEN |
| LV | Yes | Yes | No | OPEN |
| EC | Yes, but partially unclear | Yes | No | OPEN |
| ML | Yes, but partially unclear | Yes | No | OPEN |
| MOF | Yes | Yes | No | OPEN |
| GSA equations | Yes | Yes | No | OPEN |
| hybridization | Yes, but inconsistent | Yes | No | OPEN |
| binary conversion | No | Yes | No | OPEN |
| constraint repair | No | Yes | No | OPEN |
| replica count | Partially | Yes | No | OPEN |
| replica creation | Partially | Yes | Yes | OPEN |
| placement | Partially | Yes | Yes | OPEN |
| node selection | Partially | Yes | Yes | OPEN |
| failure | Partially | Yes | Yes | OPEN |
| recovery | No | Yes | Yes | OPEN |
| deletion | No | Yes | Yes | OPEN |
| replacement | No | Yes | Yes | OPEN |
| dynamic replication | Partially | Yes | Yes | OPEN |
| trigger | No | Yes | Yes | OPEN |
| workload | Partially | Yes | Yes | OPEN |
| experiment parameters | Yes, partially | Yes | No | OPEN |
| simulator integration | No | Yes | Yes | OPEN |
| evaluation | Partially | Yes | No | OPEN |

---

## 29. Implementation blockers

### A. Mathematical implementation blockers
- definitive hybrid identity
- exact binary encoding and conversion method
- constraint enforcement policy
- numerical handling of undefined objective values
- ambiguous objective formulas (EC and ML)

### B. Optimizer implementation blockers
- precise GSA parameter semantics
- elite-set selection procedure
- random generator and seed policy
- feasibility handling for OBL and GSA updates
- behavior of best_fit == worst_fit cases

### C. Replica placement blockers
- replica count interpretation
- runtime creation policy
- runtime placement execution model
- explicit treatment of Ψ as a simulator action

### D. Runtime simulation blockers
- failure simulation policy
- recovery policy
- deletion/replacement behavior
- runtime trigger policy
- simulator integration contract

### E. Experimental evaluation blockers
- workload generation
- comparison protocol
- run count and statistical reporting
- fairness conditions across algorithms

---

## 30. Final self-audit

- no source behavior was invented: PASS
- no formulas were silently repaired: PASS
- no EIMORM behavior was imported: PASS
- no NSGA behavior was imported: PASS
- no GSA/GSO ambiguity was silently resolved: PASS
- no replica-count rule was invented: PASS
- no placement heuristic was invented: PASS
- no failure/recovery policy was invented: PASS
- no deletion policy was invented: PASS
- no runtime trigger was invented: PASS
- source experiment values remain distinguishable from researcher decisions: PASS
- all researcher decisions are explicitly labeled: PASS
- all genuine researcher decisions are OPEN: PASS
- OGSA-spec.md was not modified: PASS
- OGSA-implementation-contract.md was not modified: PASS
- this document contains decisions, not implementation code: PASS

This document remains a rigorous researcher decision register for implementing OGSA while preserving the scientific separation between SOURCE, RESEARCHER, and SIMULATOR.

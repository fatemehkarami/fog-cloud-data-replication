# EIMORM researcher decision register

## 1. Purpose and Scope

This document records only the decisions that must be made by the research team in order to convert the source-faithful EIMORM specification into an executable experimental implementation.

This document is derived only from:

- [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md)
- [docs/algorithms/EIMORM-implementation-contract.md](docs/algorithms/EIMORM-implementation-contract.md)

This document does not modify either source file.

This document is not an extension of the original EIMORM paper.

It is a researcher-defined decision registry only.

Its purpose is to preserve and make explicit the transition:

- PARTIALLY DEFINED / UNRESOLVED in the source
- ↓
- RESEARCHER_DEFINED decision required for execution

No researcher-defined policy is selected in this document.

---

## 2. Decision Classification Rules

Every decision in this document must preserve the following distinction:

- SOURCE_DEFINED: explicitly supported by the EIMORM paper
- PARTIALLY_DEFINED: a concept or formula exists but is incomplete, OCR-damaged, or ambiguous
- UNRESOLVED: the paper does not provide enough information for source-faithful implementation
- RESEARCHER_DEFINED: a decision that WE must choose to execute the experiment
- SIMULATOR_DEFINED: behavior owned by the common simulator rather than the source algorithm

Key rule:

A researcher-defined decision is not evidence that the source paper defined the behavior.

The purpose of this document is to identify the missing choices, not to hide the fact that the paper is incomplete.

---

## 3. Source-Faithful Boundary

The following boundary remains in force:

- EARF / `ARFk(one)` is source-defined as a replica-factor expression.
- The paper does not provide the executable mapping from EARF to replica creation or exact replica count.
- ETBDF is source-defined in concept, but its executable equation is partially defined and OCR-damaged.
- IEK is source-defined in concept, but the exact knapsack algorithm and objective are not provided.
- Placement and provider selection are conceptual and unresolved in the source.
- Deletion / replacement / failure recovery are discussed conceptually, but not executable in source form.
- Multi-objective optimization is source-discussed, but the complete objective function is unresolved.
- Any runtime schedule or invocation pattern used by the experiment must be tracked as RESEARCHER_DEFINED EXPERIMENTAL CONFIGURATION.

This document does not choose those decisions. It only records them as OPEN.

---

## 4. Researcher Decision Register

The following is the decision register.

### Decision ID: RD-ETBDF-001

Decision:
Executable ETBDF formula

Source status:
PARTIALLY_DEFINED

Paper provides:
The paper states that ETBDF is associated with time-based decay and recent accesses receive higher weight. The source also names `tc`, `ts`, and `λ` and indicates ETBDF is used in file identification.

Paper does not provide:
A clean, unambiguous executable equation. The OCR-damaged formula is not sufficient to reconstruct a source-faithful implementation without additional researcher choice.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

### Decision ID: RD-ETBDF-002

Decision:
Interpretation of OCR-damaged ETBDF expression

Source status:
PARTIALLY_DEFINED

Paper provides:
The source gives a damaged formula and textual semantics: time decay, recency weighting, `tc`, `ts`, positive integer `λ`.

Paper does not provide:
A single authoritative repaired equation or a unique interpretation of the OCR-damaged notation.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

### Decision ID: RD-ETBDF-003

Decision:
Decay parameter selection for ETBDF

Source status:
PARTIALLY_DEFINED

Paper provides:
`λ` is described as a positive integer parameter.

Paper does not provide:
The actual value, the set of allowed values, or the operational rule for choosing a value.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

### Decision ID: RD-ETBDF-004

Decision:
Normalization of ETBDF score

Source status:
PARTIALLY_DEFINED

Paper provides:
The concept of time-weighted file importance exists.

Paper does not provide:
Any normalization method, score range, or ranking rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

### Decision ID: RD-ETBDF-005

Decision:
Threshold or cutoff for ETBDF score

Source status:
PARTIALLY_DEFINED

Paper provides:
ETBDF is used in file identification and high-access / recent-access classification.

Paper does not provide:
A threshold, percentile, or selection rule for choosing files.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

### Decision ID: RD-ETBDF-006

Decision:
Conversion from ETBDF score to file priority

Source status:
PARTIALLY_DEFINED

Paper provides:
A file-identification role exists for ETBDF.

Paper does not provide:
Any rule that converts the score into a file priority, selection rank, or candidate list.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 5. ETBDF Operationalization

This section records the operational decisions required if ETBDF is used experimentally.

### Decision ID: RD-ETBDF-OP-001

Decision:
Whether ETBDF is computed per file, per block, or per data-center/file pair

Source status:
PARTIALLY_DEFINED

Paper provides:
ETBDF is associated with file weighting and file importance.

Paper does not provide:
The exact object on which the decay function is applied.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-ETBDF-OP-002

Decision:
Time window used for historical access weighting

Source status:
PARTIALLY_DEFINED

Paper provides:
The concept of a historical / start time `ts` and current access time `tc` is present.

Paper does not provide:
The historical window length or aggregation period.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-ETBDF-OP-003

Decision:
Whether ETBDF produces a scalar value or rank ordering

Source status:
PARTIALLY_DEFINED

Paper provides:
ETBDF is used for identifying file importance.

Paper does not provide:
The output representation of the value.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 6. File Selection Policy

### Decision ID: RD-FILE-001

Decision:
How ETBDF is converted into file selection

Source status:
PARTIALLY_DEFINED

Paper provides:
File identification and recency-weighting are discussed.

Paper does not provide:
What constitutes a selected file, how many files are selected, or how priorities are converted into action.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-FILE-002

Decision:
Use of threshold versus top-K selection

Source status:
PARTIALLY_DEFINED

Paper provides:
The paper references high-access and popular files but provides no threshold or rank method.

Paper does not provide:
Whether to select all files above a score, a top-K set, or another formulation.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-FILE-003

Decision:
Tie-handling for file selection

Source status:
PARTIALLY_DEFINED

Paper provides:
No tie-breaking rule is offered.

Paper does not provide:
Any rule for equal ETBDF values or equal file priorities.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 7. Replica Creation Policy

### Decision ID: RD-CREATE-001

Decision:
Create / no-create rule

Source status:
PARTIALLY_DEFINED

Paper provides:
The source says replicas are determined in Phase 2 and that EARF is associated with the Phase-2 replica-factor decision.

Paper does not provide:
A complete rule that decides whether a new replica is created.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-CREATE-002

Decision:
Availability threshold for replica creation

Source status:
PARTIALLY_DEFINED

Paper provides:
Availability is discussed as an optimization target and a file/block availability concept exists.

Paper does not provide:
A source-defined availability threshold for triggering a new replica.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-CREATE-003

Decision:
Mapping from EARF / `ARFk(one)` to replica creation decision

Source status:
UNRESOLVED

Paper provides:
`ARFk(one) = RFk / (RFk + RFk_old)` is source-defined.

Paper does not provide:
A direct create/no-create mapping, a threshold value, or a decision rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-CREATE-004

Decision:
Whether multiple replicas may be created in a single decision cycle

Source status:
UNRESOLVED

Paper provides:
Phase-2 reasoning exists, but no exact count or batch rule is given.

Paper does not provide:
Any rule for one versus many replicas created in a decision cycle.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-CREATE-005

Decision:
Whether EARF is evaluated per file, per data center, or per replica set

Source status:
UNRESOLVED

Paper provides:
EARF is associated with a replica-factor decision for files.

Paper does not provide:
The precise evaluation scope or aggregation domain.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 8. Replica Count Policy

### Decision ID: RD-COUNT-001

Decision:
Target replica count

Source status:
PARTIALLY_DEFINED

Paper provides:
The source discusses dynamic replica count and Phase-2 replica-factor determination.

Paper does not provide:
An executable target formula or exact target count rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-COUNT-002

Decision:
Maximum replica count

Source status:
UNRESOLVED

Paper provides:
The concept of a cost-aware strategy exists and mentions not replicating too much.

Paper does not provide:
A maximum count, limit, or cap.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-COUNT-003

Decision:
Minimum replica count

Source status:
UNRESOLVED

Paper provides:
The concept of file availability and cost tradeoff exists.

Paper does not provide:
A minimum count requirement or protected-copy rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-COUNT-004

Decision:
Relationship between EARF and replica count

Source status:
UNRESOLVED

Paper provides:
EARF is associated with the Phase-2 replica-factor decision.

Paper does not provide:
Any mapping from EARF to exact replica count.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-COUNT-005

Decision:
When replica count is reduced or allowed to remain stable

Source status:
UNRESOLVED

Paper provides:
Dynamic re-replication and re-balancing are discussed conceptually.

Paper does not provide:
A concrete rule for increasing or decreasing replica count over time.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-COUNT-006

Decision:
Storage constraints affecting count

Source status:
SIMULATOR_DEFINED

Paper provides:
Cost, capacity, and storage are discussed at a high level.

Paper does not provide:
A formal storage-feasibility rule that determines the allowed number of replicas.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 9. Availability Decision Policy

### Decision ID: RD-AVAIL-001

Decision:
Operational availability formula

Source status:
PARTIALLY_DEFINED

Paper provides:
Availability is a central objective and formulas appear for block availability and file availability.

Paper does not provide:
A complete, unambiguous executable formula in a source-faithful form.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-AVAIL-002

Decision:
Handling of OCR-damaged availability formulas

Source status:
PARTIALLY_DEFINED

Paper provides:
The formulas are present but damaged in extraction.

Paper does not provide:
A justified repaired equation.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-AVAIL-003

Decision:
Availability threshold used to trigger or justify a replica

Source status:
UNRESOLVED

Paper provides:
Availability is a goal and a concept.

Paper does not provide:
Any threshold or target value.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-AVAIL-004

Decision:
Relationship between availability and replica creation

Source status:
UNRESOLVED

Paper provides:
Availability influences the replica decision conceptually.

Paper does not provide:
The explicit rule linking availability to the creation process.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-AVAIL-005

Decision:
Relationship between availability and IEK

Source status:
UNRESOLVED

Paper provides:
IEK is associated with reducing cost while preserving availability.

Paper does not provide:
A formal availability constraint within the IEK optimization.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 10. Placement Policy

### Decision ID: RD-PLACE-001

Decision:
Replica placement rule

Source status:
UNRESOLVED

Paper provides:
The strategy conceptually mentions that replicas should be placed to balance cost, availability, and load.

Paper does not provide:
An executable placement algorithm.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-PLACE-002

Decision:
Candidate data-center filtering rule

Source status:
UNRESOLVED

Paper provides:
The data-center set and cost / availability context exist.

Paper does not provide:
Any rule for deciding which sites are eligible candidates for placement.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-PLACE-003

Decision:
Cost consideration in placement

Source status:
UNRESOLVED

Paper provides:
Cost is an optimization objective and a placement consideration.

Paper does not provide:
A concrete cost-based ranking or selection rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-PLACE-004

Decision:
Availability consideration in placement

Source status:
UNRESOLVED

Paper provides:
Availability matters in the placement discussion.

Paper does not provide:
A source-defined placement rule based on availability.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-PLACE-005

Decision:
Load consideration in placement

Source status:
UNRESOLVED

Paper provides:
Load balancing is a goal.

Paper does not provide:
A source-defined placement rule based on load.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-PLACE-006

Decision:
Tie-breaking for placement

Source status:
UNRESOLVED

Paper provides:
No tie-breaking rule is specified.

Paper does not provide:
Any deterministic or probabilistic policy for equal placement candidates.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-PLACE-007

Decision:
Whether provider and placement are treated as one action or separate actions

Source status:
UNRESOLVED

Paper provides:
The source references replica placement and provider selection only conceptually.

Paper does not provide:
Any formal separation or combination rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-PLACE-008

Decision:
Any heuristic not described explicitly by the paper

Source status:
UNRESOLVED

Paper provides:
No placement heuristic is source-defined.

Paper does not provide:
A permitted heuristic for nearest, cheapest, least-loaded, highest-availability, weighted scoring, Pareto selection, or random selection.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 11. Provider Selection Policy

### Decision ID: RD-PROVIDER-001

Decision:
Provider-selection rule

Source status:
UNRESOLVED

Paper provides:
The source discusses placement, available replicas, and data-center heterogeneity.

Paper does not provide:
An explicit provider-selection algorithm.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-PROVIDER-002

Decision:
Candidate-provider filtering

Source status:
UNRESOLVED

Paper provides:
The concept of file replicas across data centers exists.

Paper does not provide:
How candidate providers are chosen, which environments qualify, or whether the provider set is restricted to a subset.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-PROVIDER-003

Decision:
Cost-aware provider ranking

Source status:
UNRESOLVED

Paper provides:
Cost is a consideration but no ranking rule is specified.

Paper does not provide:
Any cost-based ranking or score.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-PROVIDER-004

Decision:
Tie-breaking among providers

Source status:
UNRESOLVED

Paper provides:
No tie-break rule.

Paper does not provide:
Any deterministic or probabilistic rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 12. Cost and User-Budget Policy

### Decision ID: RD-COST-001

Decision:
Operational cost function

Source status:
PARTIALLY_DEFINED

Paper provides:
Cost is discussed as a major objective and uses data-center cost differences.

Paper does not provide:
A complete operational cost function or per-replica cost model.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-COST-002

Decision:
User-budget representation

Source status:
PARTIALLY_DEFINED

Paper provides:
The budget is discussed conceptually as a user budget.

Paper does not provide:
A numerical representation, unit, or time scale.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-COST-003

Decision:
Budget comparison condition

Source status:
PARTIALLY_DEFINED

Paper provides:
IEK is associated with the user-budget condition when replication cost reaches or exceeds the budget.

Paper does not provide:
The exact comparison operator or a threshold definition.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-COST-004

Decision:
Cost calculation granularity

Source status:
PARTIALLY_DEFINED

Paper provides:
Cost is discussed at a data-center and replication level.

Paper does not provide:
Whether cost is computed per file, per block, per replica, per request, or per decision cycle.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 13. IEK Operationalization

### Decision ID: RD-IEK-001

Decision:
Knapsack items

Source status:
UNRESOLVED

Paper provides:
IEK is described as a cost-optimization mechanism under the user-budget condition.

Paper does not provide:
The exact item definition for the knapsack formulation.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-IEK-002

Decision:
Item value / profit

Source status:
UNRESOLVED

Paper provides:
The paper mentions optimization of replication cost and moving replicas from high-cost to low-cost data centers.

Paper does not provide:
The exact profit, value, or utility of each candidate item.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-IEK-003

Decision:
Item weight

Source status:
UNRESOLVED

Paper provides:
No knapsack item weight is specified.

Paper does not provide:
Any item-weight definition or capacity semantics.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-IEK-004

Decision:
Capacity definition

Source status:
UNRESOLVED

Paper provides:
The idea of a user budget exists.

Paper does not provide:
A capacity value, a unit, or a formal budget constraint.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-IEK-005

Decision:
Objective function of IEK

Source status:
UNRESOLVED

Paper provides:
The paper mentions cost optimization and moving replication from high-cost to low-cost data centers.

Paper does not provide:
The mathematical objective or the optimization target.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-IEK-006

Decision:
Constraints and feasibility conditions

Source status:
UNRESOLVED

Paper provides:
Availability should not be compromised.

Paper does not provide:
A formal feasibility constraint, penalty, or availability bound.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-IEK-007

Decision:
Selection strategy used in IEK

Source status:
UNRESOLVED

Paper provides:
The concept exists, but no algorithm is specified.

Paper does not provide:
A pseudocode, algorithmic step, or selection rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-IEK-008

Decision:
IEK output and representation

Source status:
UNRESOLVED

Paper provides:
IEK is described as a cost-optimization step.

Paper does not provide:
The exact output structure or result object.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-IEK-009

Decision:
Interaction between IEK and availability constraints

Source status:
UNRESOLVED

Paper provides:
Availability should not be compromised.

Paper does not provide:
A measurable availability constraint or formal tradeoff definition.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-IEK-010

Decision:
Movement from high-cost to low-cost data centers

Source status:
UNRESOLVED

Paper provides:
The conceptual direction is clear: move replication from higher-cost data centers to lower-cost data centers.

Paper does not provide:
Which replicas move, when, and under what exact condition.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 14. Replica Deletion / Replacement Policy

### Decision ID: RD-DEL-001

Decision:
Deletion trigger

Source status:
UNRESOLVED

Paper provides:
Dynamic re-replication and re-balancing are discussed conceptually.

Paper does not provide:
Any deletion trigger.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-DEL-002

Decision:
Replica chosen for deletion

Source status:
UNRESOLVED

Paper provides:
No selection policy is described.

Paper does not provide:
A replica-ranking or value metric for deletion.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-DEL-003

Decision:
Replacement trigger

Source status:
UNRESOLVED

Paper provides:
Re-replication and re-balancing are discussed at a conceptual level.

Paper does not provide:
Any replacement trigger.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-DEL-004

Decision:
Source and destination of replacement

Source status:
UNRESOLVED

Paper provides:
Cost-aware re-replication from higher-cost to lower-cost data centers is referenced.

Paper does not provide:
A formal source/destination choice rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-DEL-005

Decision:
Consistency handling during deletion / replacement

Source status:
UNRESOLVED

Paper provides:
The concept of replication and re-balancing exists.

Paper does not provide:
Any consistency procedure or ordering rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-DEL-006

Decision:
Minimum replica protection

Source status:
UNRESOLVED

Paper provides:
Fault tolerance and availability are discussed.

Paper does not provide:
Any rule for preserving a minimum number of replicas or protected copies.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 15. Failure / Recovery Policy

### Decision ID: RD-FAIL-001

Decision:
Failure model

Source status:
UNRESOLVED

Paper provides:
Replication is discussed as a fault-tolerance mechanism.

Paper does not provide:
Any failure model, failure distribution, or failure probability definition.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-FAIL-002

Decision:
Failure generation in the simulator

Source status:
SIMULATOR_DEFINED

Paper provides:
Conceptual fault tolerance, but no source-defined failure-generation algorithm.

Paper does not provide:
An exact failure generation mechanism.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-FAIL-003

Decision:
Failure detection

Source status:
UNRESOLVED

Paper provides:
No failure-detection rule.

Paper does not provide:
Any detection or monitoring specification.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-FAIL-004

Decision:
Recovery policy

Source status:
UNRESOLVED

Paper provides:
The concept of replication enabling recovery is discussed.

Paper does not provide:
Any recovery algorithm, repair rule, or re-replication rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-FAIL-005

Decision:
Re-replication after failure

Source status:
UNRESOLVED

Paper provides:
General mentions of fault tolerance and dynamic re-replication exist.

Paper does not provide:
A trigger or algorithm for re-replication after failure.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-FAIL-006

Decision:
Failed-node exclusion policy

Source status:
UNRESOLVED

Paper provides:
No explicit node-exclusion rule.

Paper does not provide:
A failure-handling policy that removes failed data centers or nodes from consideration.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 16. Multi-Objective Optimization Policy

The source-discussed optimization dimensions are:

1. Availability
2. Cost
3. Load balancing
4. Energy consumption
5. Latency / service time

### Decision ID: RD-MOO-001

Decision:
Objective representation

Source status:
UNRESOLVED

Paper provides:
Five dimensions are discussed conceptually.

Paper does not provide:
A complete objective vector or a formal representation.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-MOO-002

Decision:
Normalization of objectives

Source status:
UNRESOLVED

Paper provides:
The existence of multiple objectives is clear.

Paper does not provide:
A normalization rule, a scaling strategy, or a common unit for comparison.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-MOO-003

Decision:
Objective weighting

Source status:
UNRESOLVED

Paper provides:
The need to balance objectives is explicit.

Paper does not provide:
Any weight values or a rule for choosing them.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-MOO-004

Decision:
Aggregation method

Source status:
UNRESOLVED

Paper provides:
The optimization is multi-objective in concept.

Paper does not provide:
A scalarization, weighted-sum method, Pareto formulation, or other aggregation rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-MOO-005

Decision:
Optimization method

Source status:
UNRESOLVED

Paper provides:
No algorithmic optimization method is specified.

Paper does not provide:
A source-defined optimization algorithm.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-MOO-006

Decision:
Fitness function or decision score

Source status:
UNRESOLVED

Paper provides:
The five objectives are named, but no fitness function is given.

Paper does not provide:
Any formula for a single-value score or objective comparison.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-MOO-007

Decision:
Method selection among candidate optimization strategies

Source status:
UNRESOLVED

Paper provides:
No specific strategy is selected.

Paper does not provide:
A selection among weighted-sum, Pareto, NSGA-II, NSGA-III, or any other approach.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 17. Trigger / Invocation Policy

### Decision ID: RD-TRIGGER-001

Decision:
When EIMORM is invoked

Source status:
PARTIALLY_DEFINED

Paper provides:
The source describes two conceptual phases and a budget-related IEK condition.

Paper does not provide:
A complete event-driven, time-driven, or request-driven runtime trigger.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-TRIGGER-002

Decision:
Periodic versus event-driven execution

Source status:
UNRESOLVED

Paper provides:
No explicit periodic schedule or event model.

Paper does not provide:
A scheduling rule for runtime invocation.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-TRIGGER-003

Decision:
Request-based or time-based trigger policy

Source status:
UNRESOLVED

Paper provides:
Only conceptual file-access and popularity discussions.

Paper does not provide:
A request-based or time-based trigger rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-TRIGGER-004

Decision:
Experiment schedule used in execution

Source status:
RESEARCHER_DEFINED EXPERIMENTAL CONFIGURATION

Paper provides:
No complete schedule.

Paper does not provide:
A runtime scheduling policy for the algorithm.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 18. Simulator Integration Decisions

### Decision ID: RD-SIM-001

Decision:
Ownership of catalog mutation

Source status:
SIMULATOR_DEFINED

Paper provides:
The replica catalog and replica manager are mentioned.

Paper does not provide:
A complete mutation protocol or ownership boundary.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-SIM-002

Decision:
Storage validation and capacity enforcement

Source status:
SIMULATOR_DEFINED

Paper provides:
Storage and cost are discussed conceptually.

Paper does not provide:
A source-defined capacity or validation rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-SIM-003

Decision:
State mutation for replica creation and deletion

Source status:
SIMULATOR_DEFINED

Paper provides:
Conceptual replication behaviors exist.

Paper does not provide:
The exact state-change sequence or mutation order.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-SIM-004

Decision:
Failure generation and execution schedule

Source status:
SIMULATOR_DEFINED

Paper provides:
Conceptual fault tolerance is stated.

Paper does not provide:
The simulation-level failure generation rule.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

### Decision ID: RD-SIM-005

Decision:
Interface contract for unresolved outputs

Source status:
SOURCE_DEFINED_IN_CONTRACT

Paper provides:
The EIMORM contract requires unresolved decision placeholders.

Paper does not provide:
Concrete operation for unresolved outcomes.

Researcher decision:
TO BE DECIDED

Chosen alternative:
EMPTY

Rationale:
TO BE DECIDED

Impact:
TO BE DECIDED

Status:
OPEN

---

## 19. Experimental Parameters

This table is intentionally empty for researcher-defined values.

| Parameter | Source value | Researcher value | Unit | Rationale | Status |
|---|---|---|---|---|---|
| number of data centers | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| number of hosts | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| number of VMs | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| number of files | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| number of blocks | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| file size | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| block size | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| number of requests | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| request rate | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| access distribution | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| lambda | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| user budget | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| storage capacity | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| bandwidth | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| failure parameters | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| experiment duration | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |
| invocation frequency | EMPTY | EMPTY | EMPTY | TO BE DECIDED | OPEN |

Important rule:

The source does not provide numeric values for these parameters. If a value is not present in the source, it remains EMPTY and OPEN.

---

## 20. Alternatives Considered

The following alternatives remain open and are intentionally not selected.

### Decision ID: RD-ALT-ETBDF

Alternative A:
TO BE DECIDED

Alternative B:
TO BE DECIDED

Alternative C:
TO BE DECIDED

Selected:
EMPTY

Reason:
EMPTY

### Decision ID: RD-ALT-FILE-SELECTION

Alternative A:
TO BE DECIDED

Alternative B:
TO BE DECIDED

Alternative C:
TO BE DECIDED

Selected:
EMPTY

Reason:
EMPTY

### Decision ID: RD-ALT-REPLICA-CREATION

Alternative A:
TO BE DECIDED

Alternative B:
TO BE DECIDED

Alternative C:
TO BE DECIDED

Selected:
EMPTY

Reason:
EMPTY

### Decision ID: RD-ALT-REPLICA-COUNT

Alternative A:
TO BE DECIDED

Alternative B:
TO BE DECIDED

Alternative C:
TO BE DECIDED

Selected:
EMPTY

Reason:
EMPTY

### Decision ID: RD-ALT-PLACEMENT

Alternative A:
TO BE DECIDED

Alternative B:
TO BE DECIDED

Alternative C:
TO BE DECIDED

Selected:
EMPTY

Reason:
EMPTY

### Decision ID: RD-ALT-PROVIDER

Alternative A:
TO BE DECIDED

Alternative B:
TO BE DECIDED

Alternative C:
TO BE DECIDED

Selected:
EMPTY

Reason:
EMPTY

### Decision ID: RD-ALT-IEK

Alternative A:
TO BE DECIDED

Alternative B:
TO BE DECIDED

Alternative C:
TO BE DECIDED

Selected:
EMPTY

Reason:
EMPTY

### Decision ID: RD-ALT-MOO

Alternative A:
TO BE DECIDED

Alternative B:
TO BE DECIDED

Alternative C:
TO BE DECIDED

Selected:
EMPTY

Reason:
EMPTY

---

## 21. Decision Rationale

The rationale for each future researcher decision must answer the following questions:

1. Why is this decision necessary?
2. What does the paper actually specify?
3. What does the paper leave unresolved?
4. Why was this particular implementation choice selected?
5. What effect could this choice have on experimental results?
6. Is the choice likely to favor or disadvantage EIMORM?
7. Can the choice be changed later without changing the source-faithful layer?

The rationale section is intentionally left blank for later completion.

### Decision ID: RD-RATIONALE-001

Reasoning:
TO BE DECIDED

Impact on results:
TO BE DECIDED

Evidence from source:
TO BE DECIDED

Evidence from contracts:
TO BE DECIDED

Status:
OPEN

---

## 22. Traceability to EIMORM-spec.md and EIMORM-implementation-contract.md

| Decision ID | Decision | EIMORM-spec Section | Implementation Contract Section | Source Status | Researcher Decision | Status |
|---|---|---|---|---|---|---|
| RD-ETBDF-001 | Executable ETBDF formula | section 8 | section 9 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-ETBDF-002 | OCR interpretation | section 8 | section 9 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-ETBDF-003 | Decay parameter selection | section 8 | section 9 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-ETBDF-004 | Normalization | section 8 | section 9 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-ETBDF-005 | Threshold / cutoff | section 8 | section 9 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-ETBDF-006 | Score-to-priority conversion | section 8 | section 9 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-FILE-001 | File-selection policy | section 8, section 20 | section 8, section 9 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-CREATE-001 | Create / no-create policy | section 9 | section 14 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-CREATE-003 | EARF → create mapping | section 9 | section 10, section 14 | UNRESOLVED | TO BE DECIDED | OPEN |
| RD-COUNT-001 | Target replica count | section 9 | section 15 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-COUNT-004 | EARF → replica count mapping | section 9 | section 10, section 15 | UNRESOLVED | TO BE DECIDED | OPEN |
| RD-AVAIL-001 | Availability formula | section 10 | section 11 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-PLACE-001 | Placement rule | section 17 | section 16 | UNRESOLVED | TO BE DECIDED | OPEN |
| RD-PROVIDER-001 | Provider-selection rule | section 17 | section 16 | UNRESOLVED | TO BE DECIDED | OPEN |
| RD-COST-001 | Cost function | section 11 | section 12 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-COST-003 | Budget comparison condition | section 11, section 16 | section 12, section 13 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-IEK-001 | IEK item definition | section 16 | section 13 | UNRESOLVED | TO BE DECIDED | OPEN |
| RD-IEK-005 | IEK objective function | section 16 | section 13 | UNRESOLVED | TO BE DECIDED | OPEN |
| RD-DEL-001 | Deletion trigger | section 18 | section 17 | UNRESOLVED | TO BE DECIDED | OPEN |
| RD-FAIL-001 | Failure model | section 19 | section 18 | UNRESOLVED | TO BE DECIDED | OPEN |
| RD-MOO-003 | Objective weighting | section 15 | section 19 | UNRESOLVED | TO BE DECIDED | OPEN |
| RD-MOO-005 | Optimization method | section 15 | section 19 | UNRESOLVED | TO BE DECIDED | OPEN |
| RD-TRIGGER-001 | Trigger / invocation | section 7, section 20 | section 20 | PARTIALLY_DEFINED | TO BE DECIDED | OPEN |
| RD-SIM-001 | Catalog mutation | section 25 | section 21, section 22 | SIMULATOR_DEFINED | TO BE DECIDED | OPEN |

---

## 23. Open Decisions

The following decisions must be resolved before executable implementation can proceed:

- ETBDF executable formula
- ETBDF threshold / selection rule
- file-selection mechanism
- create / no-create rule
- replica-count rule
- availability operationalization
- placement policy
- provider-selection policy
- cost function
- budget handling
- IEK algorithm
- deletion / replacement policy
- failure / recovery policy
- multi-objective formulation
- objective weighting
- optimization method
- invocation schedule
- simulator integration policy
- experimental parameter values

This list is intentionally open and may grow as the experiment design matures.

---

## 24. Final Decision Status

### Researcher Decision Status

| Area | Status |
|---|---|
| ETBDF | OPEN |
| File selection | OPEN |
| Replica creation | OPEN |
| Replica count | OPEN |
| Availability | OPEN |
| Placement | OPEN |
| Provider selection | OPEN |
| Cost/Budget | OPEN |
| IEK | OPEN |
| Deletion/Replacement | OPEN |
| Failure/Recovery | OPEN |
| Multi-objective formulation | OPEN |
| Trigger/Invocation | OPEN |
| Simulator integration | OPEN |
| Experimental parameters | OPEN |

No researcher-defined implementation policy has been selected in this document yet.

---

## Final self-audit

This file was audited against the required restrictions.

1. No missing EIMORM behavior has been invented. PASS
2. No OCR-damaged formula has been repaired. PASS
3. No EARF → replica-count mapping has been selected. PASS
4. No EARF → create/no-create mapping has been selected. PASS
5. No placement heuristic has been selected. PASS
6. No provider-selection policy has been selected. PASS
7. No IEK algorithm has been selected. PASS
8. No deletion policy has been selected. PASS
9. No failure model has been selected. PASS
10. No objective weights have been selected. PASS
11. No NSGA-II / NSGA-III / Pareto / weighted-sum method has been selected. PASS
12. No numerical experimental parameters have been invented. PASS
13. Every researcher-defined decision is explicitly marked as OPEN. PASS
14. Source-defined behavior remains distinguishable from researcher-defined behavior. PASS
15. EIMORM-spec.md and EIMORM-implementation-contract.md remain unchanged. PASS

Audit result: all 15 checks passed.

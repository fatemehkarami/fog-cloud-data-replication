# EIMORM implementation contract

## 1. Purpose and Scope

This document defines the implementation boundary for EIMORM only from the current source-of-truth specification in [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md).

The purpose is not to complete missing source behavior. The purpose is to define a precise boundary between:

- EIMORM source behavior
- EIMORM implementation / adapter behavior
- Common simulator behavior
- Researcher-defined extension points

This contract intentionally prevents researcher-defined or simulator-defined behavior from being silently presented as source-defined EIMORM behavior.

## 1A. Phase 15 execution decisions

| Area | Source-supported behavior | Researcher decision | Why needed |
|---|---|---|---|
| ETBDF | Recent-access/time-decay concept; formula is OCR-damaged | Score `exp(-lambda * (current_time - historical_time))`, `lambda = 1`, threshold `0.5`; non-negative elapsed time required | Provides a deterministic recency score without claiming to repair the paper formula. |
| File selection | ETBDF identifies recent/important files | Evaluate the requested file only on each admitted read request | Minimal request-driven execution consistent with the source concept. |
| EARF | Preserve `RFk / (RFk + RFk_old)` exactly | `ARF >= 0.5` requests one additional replica; lower values produce no action | Gives the explicit formula an executable mapping without importing another replica-count policy. |
| Create/no-create | Replication is discussed conceptually | Create/placement is selected only when the fixed ETBDF/EARF/budget gates require it | Avoids automatic replication on every request. |
| Availability | Source discusses file/block availability | Use common catalogued valid replicas and common node health/reachability as context; no fabricated probability | Keeps availability source context separate from runtime metrics. |
| Cost | Preserve `sum(data_center_cost * file_count)` | Use supplied cost entries; default user budget `10.0` only when omitted | Makes the budget gate executable and auditable. |
| IEK | IEK is source-conceptual; exact knapsack is incomplete | Deterministic single-candidate capacity-valid placement, selected by stable node ID; no unrelated optimizer | Minimal IEK-compatible interpretation without importing another method. |
| Placement | Heterogeneous data centers/providers are source context | Choose the first stable healthy, reachable, non-duplicate, capacity-valid node | Produces a common-runtime-compatible placement decision. |
| Deletion/replacement/recovery | Not completely source-defined | No automatic deletion, replacement, retry, or recovery; CMP-RD-005 remains external | Avoids inventing lifecycle behavior. |
| Randomness | No EIMORM randomness is required | Deterministic execution; no new RNG | Reproducible and source-faithful. |

These are RESEARCHER-DECIDED interpretations where the source is incomplete. They are not presented as original EIMORM paper behavior.

This document is a contract, not executable code and not a pseudocode implementation of EIMORM itself.

Classification values used throughout:

- SOURCE-REQUIRED
- RESEARCHER-REQUIRED
- COMMON-SIMULATOR-REQUIRED
- IMPLEMENTATION-DETAIL
- UNRESOLVED

The system must not treat unresolved or researcher-defined behavior as paper-defined EIMORM behavior.

---

## 2. Source-of-Truth Rules

This document is derived only from the current EIMORM specification file and must not add any behavior that is not traceable there.

Source-of-truth requirements:

- Treat [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md) as the only authoritative source for EIMORM behavior.
- Preserve all terminology and distinctions already established there, including:
  - SOURCE-DEFINED
  - PARTIALLY DEFINED
  - UNRESOLVED
  - RESEARCHER-DEFINED EXPERIMENTAL CONFIGURATION
  - SIMULATOR-DEFINED behavior
- Do not silently repair OCR-damaged formulas.
- Do not infer implementation rules from common replication practice.
- Do not import algorithms or policies from HDFS, DPRS, OGSA, HSR, EIMORM-related papers, or any other source.
- Do not convert an unresolved or partially defined concept into a source-defined algorithm simply because the concept is named in the paper.

The contract must explicitly separate:

- what the paper states;
- what the paper implies but does not define sufficiently;
- what must be chosen by the researcher or simulator to run an experiment.

When the source is incomplete, ambiguous, or OCR-damaged, the implementation must preserve that uncertainty rather than silently repairing it. Any repair, interpretation, parameter choice, or algorithmic completion requires an explicit researcher decision and must not be presented as source-defined behavior.

---

## 3. Terminology and Status Classification

### 3.1 Status classification rules

- SOURCE-REQUIRED
- The paper explicitly provides the concept, variable, or formula in a source-faithful way.

- RESEARCHER-REQUIRED
- A decision is required to make the algorithm executable in the project, but the paper does not specify it.

- COMMON-SIMULATOR-REQUIRED
- A behavior belongs to the shared execution environment, not to the EIMORM source algorithm.

- IMPLEMENTATION-DETAIL
- A software-handling detail is needed without changing EIMORM scientific behavior.

- UNRESOLVED
- The paper is incomplete, OCR-damaged, ambiguous, or otherwise insufficient for faithful execution.

### 3.2 Required interpretation rule

Any capability that is not directly and specifically defined in the source must be treated as one of:

- RESEARCHER-REQUIRED
- COMMON-SIMULATOR-REQUIRED
- UNRESOLVED

It must not be silently labeled SOURCE-REQUIRED.

---

## 4. EIMORM Responsibilities

EIMORM responsibilities are limited to source-supported behaviors in the paper.

At the EIMORM layer, the implementation may only do the following, and only when explicitly supported by the source specification:

- represent the conceptual multi-tier heterogeneous data-center environment;
- read file and block state from the replica catalog and related metadata;
- reason about file importance / access recency in terms of the source-defined ETBDF concept;
- evaluate the Phase-2 replica-factor discussion based on EARF / `ARFk(one)`;
- identify the cost-budget condition under which IEK is mentioned as relevant;
- assess source-level availability, cost, and load objectives as conceptual optimization dimensions;
- expose unresolved decisions as explicit outputs rather than inventing them.

EIMORM must not implement any of the following unless it is explicitly marked RESEARCHER-REQUIRED and separately documented:

- exact ETBDF equation;
- exact replica-count formula;
- exact provider-selection heuristic;
- exact placement algorithm;
- exact deletion or replacement policy;
- exact failure-recovery algorithm;
- exact multi-objective weighting or scalarization;
- exact invocation schedule.

---

## 5. Adapter Responsibilities

The EIMORM adapter is the boundary layer between source-level EIMORM concepts and the common simulator.

Adapter responsibilities:

- translate source-available metadata into EIMORM-readable inputs;
- preserve the distinction between source-defined and project-defined behaviors;
- expose unresolved values as explicit unresolved outputs, not as fabricated decisions;
- reject any attempt to turn researcher-defined or simulator-defined policy into paper-defined EIMORM behavior;
- maintain a clear separation between EIMORM logic and simulator execution.

Adapter responsibilities must not include:

- inventing an unmentioned placement heuristic;
- inventing an exact IEK objective function;
- silently calculating a replica target count not defined by the source;
- repairing OCR-damaged formulas into a new executable equation;
- treating simulator scheduling as source behavior.

---

## 6. Common Simulator Responsibilities

The simulator owns execution and physical state management.

The simulator is responsible for:

- storage capacity and validity checks;
- simulation state management;
- access-history generation and timestamps;
- failure generation and recovery execution if modeled;
- method invocation scheduler if the experiment requires a runtime trigger;
- serialization / state mutation of replica catalog entries as part of execution;
- any operational rule that is not source-defined by EIMORM.

The simulator may define a runtime trigger, but it must be classified as:

- RESEARCHER-REQUIRED

and must not be described as the source-defined behavior of EIMORM.

---

## 7. Data Model / Required Inputs

This section defines the inputs that may be required by the EIMORM adapter. The contract does not define unsupported meanings.

| Input | Meaning | Classification | Exact value known | Blocks faithful execution | Notes |
| --- | --- | --- | --- | --- | --- |
| data centers | cloud sites / DCs | SOURCE-REQUIRED | No project value | No | Source architecture describes heterogeneous data centers and tiers |
| files | data objects / file identifiers | SOURCE-REQUIRED | No project value | No | Files are discussed as F = {f1,...,fs} |
| blocks | partitioned data blocks | SOURCE-REQUIRED | No project value | No | File partitioning into blocks is source-defined |
| replica catalog info | file-to-replica metadata and data-center locations | COMMON-SIMULATOR-REQUIRED | No project value | No | Common state supplies this source-observable context |
| block availability | per-block availability probability | UNRESOLVED | No | Yes | Probability concept is source-defined, exact formula is damaged |
| file availability | aggregate availability of a file | UNRESOLVED | No | Yes | Discussed in the paper, formulas are OCR-damaged |
| file unavailability | complement of file availability | UNRESOLVED | No | Yes | Concept exists, exact formula is unclear |
| RFk | recent replica factor of the file | UNRESOLVED | No | Yes | Source concept exists; executable semantics are incomplete |
| RFk_old | old replica factor of the file | UNRESOLVED | No | Yes | Source concept exists; executable semantics are incomplete |
| ARFk(one) | enhanced adjustable replica factor | SOURCE-REQUIRED | Formula only | Yes | `ARFk(one) = RFk / (RFk + RFk_old)`; downstream mapping is missing |
| access timestamps | time of access events | COMMON-SIMULATOR-REQUIRED | No project value | No | Runtime history is supplied by the common simulator |
| tc | current / access time | SOURCE-REQUIRED | No | No | Source names the semantic role, not a project clock value |
| ts | historical / starting time | SOURCE-REQUIRED | No | No | Source names the semantic role, not a project clock value |
| lambda | decay parameter | SOURCE-REQUIRED | No | Yes | Source says `λ` is a positive integer; no value or repaired formula is provided |
| cost | cost per data center / replication cost | UNRESOLVED | No | Yes | Source defines a major dimension, but the executable model is incomplete |
| user budget | condition for IEK relevance | RESEARCHER-REQUIRED | No | Yes | Source gives the concept, not a threshold or budget value |
| load / service-time info | load balancing quantities | UNRESOLVED | No | Yes | Concept exists, formulas are damaged |
| energy-related parameters | peak and idle power values | UNRESOLVED | No | Yes | `Pmax(j)` and `Pidle(j)` are named, but the formula is damaged |
| latency-related parameters | request latency and bandwidth terms | UNRESOLVED | No | Yes | Source discusses latency, but the executable model is damaged |
| storage / capacity state | free space, capacity, storage feasibility | COMMON-SIMULATOR-REQUIRED | No project value | No | Common simulator owns physical feasibility state |
| failure state | node or site failure information | COMMON-SIMULATOR-REQUIRED | No project value | No | Common simulator may provide events; EIMORM recovery is unresolved |

Important boundary:

- EIMORM can accept these inputs only to the extent the source supports them.
- Missing semantics must not be filled by guessing.

---

## 8. EIMORM Processing Pipeline

The EIMORM paper gives a conceptual processing flow, not an executable algorithmic specification.

The source-faithful conceptual pipeline is:

1. Observe files, access history, and data-center state.
2. Identify files needing replication using source-defined ETBDF / recency-weighting concept.
3. Assess file availability and replica-related state.
4. Evaluate Phase 2 replica-factor decision using EARF / `ARFk(one)`.
5. Check whether replication cost exceeds the user budget and whether IEK is relevant.
6. Consider availability, cost, load, energy, and latency objectives as source-discussed goals.
7. Return source-level analysis or unresolved decisions; the common simulator owns the replica catalog and authoritative dynamic runtime state.

This pipeline is intentionally conceptual and must not be treated as complete executable pseudocode.

---

## 9. Phase 1 Contract — File Identification / ETBDF

### 9.1 Source status

ETBDF concept is SOURCE-REQUIRED; its executable treatment is UNRESOLVED.

### 9.2 Source-verifiable semantics

The paper supports only the following semantics:

- ETBDF is associated with time-based decay;
- more recent accesses receive higher weight;
- `tc` represents current or access time;
- `ts` represents historical or start time;
- `λ` is a positive integer parameter.

### 9.3 Contract rule

The implementation may treat ETBDF as a recency-weighting concept, but it may not claim the paper provides a clean executable formula.

### 9.4 Required external decision

If an implementation needs an executable ETBDF function, that function is:

- RESEARCHER-REQUIRED

and the contract must state that the paper does not provide an unambiguous executable equation.

### 9.5 Prohibited behavior

The implementation must not:

- silently repair the OCR-damaged ETBDF expression into a different formula;
- treat ETBDF as a precise threshold rule without source support;
- assign an exact ETBDF threshold without a researcher-defined choice.

---

## 10. Phase 2 Contract — Replica-Factor Decision / EARF

### 10.1 Source formula

The source-defined formula is:

`ARFk(one) = RFk / (RFk + RFk_old)`

The displayed relation is SOURCE-REQUIRED.

### 10.2 Critical contractual rule

EARF / `ARFk(one)` is associated with the Phase-2 replica-factor decision, but the executable mapping from this factor to final replica creation or exact replica count is UNRESOLVED.

The implementation may not claim that EARF:

- directly decides whether a replica is created;
- directly determines the exact number of replicas;
- directly provides a target replica count;
- directly provides a placement decision.

### 10.3 Required external decision

Any operational mapping from `ARFk(one)` to a real replica-creation rule or target count must be:

- RESEARCHER-REQUIRED

This is not a source-defined behavior of EIMORM.

### 10.4 Contract output

The adapter may expose the following conceptual output forms only:

- `ReplicaFactorDecision = {EARF_context, phase_2_context}`
- `ReplicaCreationDecision = UNRESOLVED`
- `TargetReplicaCount = UNRESOLVED`

---

## 11. Availability Contract

Availability is a source-defined objective and is discussed at both block and file levels.

### 11.1 Source status

- block availability: B
- file availability: B
- file unavailability / reliability expressions: B to E depending on formula quality and extraction consistency

### 11.2 Contract rule

The implementation may accept availability metrics as paper-defined quantities, but it may not assume that the source provides a complete executable availability algorithm.

### 11.3 Required boundary

If the project needs a concrete availability threshold or a final availability target to drive replica creation, that threshold is:

- RESEARCHER-REQUIRED

### 11.4 Important restriction

The paper’s availability / unavailability / reliability expressions are not automatically identical to any project-wide Reliability metric. This distinction must be preserved.

---

## 12. Cost and User-Budget Contract

### 12.1 Source status

Cost is source-defined in concept, but not fully formalized as a complete executable cost function. The user-budget trigger is part of the conceptual narrative.

### 12.2 Source-faithful semantics

The paper states that:

- replication cost increases with data-center choice and replication overhead;
- high-cost data centers are relevant to the cost optimization discussion;
- cost optimization moves replication from higher-cost data centers to lower-cost data centers;
- IEK is invoked when replication cost reaches or exceeds the user budget.

### 12.3 Implementation constraint

The implementation may instrument cost and user-budget values, but it must not invent a cost function or budget threshold without project-level decision.

Any concrete budget threshold or cost formula used in simulation is:

- RESEARCHER-REQUIRED

not EIMORM-defined behavior.

---

## 13. IEK Contract

### 13.1 Source status

IEK's conceptual role is SOURCE-REQUIRED; its executable optimizer is UNRESOLVED.

### 13.2 Source-verifiable semantics

The paper supports the following statements:

- IEK is used for replication-cost optimization;
- it is associated with the user-budget condition;
- it is associated with moving replication from higher-cost data centers to lower-cost data centers;
- availability must not be compromised.

### 13.3 Contract rule

The implementation may treat IEK as a conceptual cost-optimization mechanism under the user-budget condition, but it may not invent the following without explicit researcher-defined specification:

- knapsack item definition;
- value/profit;
- weight;
- capacity;
- objective function;
- selection algorithm;
- sorting rule;
- exact output;
- exact pseudocode.

Those missing details are UNRESOLVED.

### 13.4 Required extension point

If the project needs a concrete IEK optimizer, it must be:

- RESEARCHER-REQUIRED

---

## 14. Replica Creation Contract

### 14.1 Source status

Replica creation is UNRESOLVED.

### 14.2 Source-fidelity rule

The source says that new replicas are determined in Phase 2; it associates EARF with the replica-factor decision; it does not provide an executable final creation rule.

### 14.3 Contract rule

The adapter may expose a decision request such as:

- `ReplicaCreationRequest = {file_id, availability_context, cost_context, phase_2_factor}`

but it may not produce or assume a final concrete create/no-create decision unless the project defines it as a researcher extension.

### 14.4 Required extension point

Any actual create-or-do-not-create decision rule is:

- RESEARCHER-REQUIRED

The exact replica-creation threshold or condition is not source-defined.

---

## 15. Replica Count Contract

### 15.1 Source status

Dynamic replica count is UNRESOLVED.

### 15.2 Contract rule

The paper does not provide an exact target replica-count formula.

Source-defined statements only:

- there are multiple phases;
- EARF is associated with the Phase-2 replica-factor decision;
- new replicas are considered in Phase 2;
- exact replica count is not specified in the paper.

### 15.3 Required output

The implementation contract must permit only:

- `TargetReplicaCount = UNRESOLVED`

or a researcher-defined value chosen by outside policy, not by EIMORM source logic.

### 15.4 Forbidden assumption

The implementation must not assume:

- exact replica count = f(availability threshold)
- exact replica count = function of EARF alone
- exact replica count = target from a hand-coded heuristic

---

## 16. Replica Placement / Provider Selection Contract

### 16.1 Source status

Placement and provider selection are UNRESOLVED.

### 16.2 Source-faithful rule

The source describes placement conceptually as a cost-availability-load-aware decision but does not provide an executable policy.

The implementation must not assume any of the following unless explicitly marked as researcher-defined:

- nearest provider;
- cheapest provider;
- highest availability provider;
- least-loaded provider;
- weighted score;
- ranking;
- Pareto selection;
- random selection.

### 16.3 Interface boundary

The EIMORM layer may produce a request containing source-supported information, such as:

- file identifier;
- candidate data-center context;
- current replica state;
- availability and cost context;
- load-related state.

The actual provider-selection or placement policy is not source-defined and is classified as:

- RESEARCHER-REQUIRED

---

## 17. Replica Deletion / Replacement / Re-replication Contract

### 17.1 Source status

Replica deletion, replacement, and re-replication are UNRESOLVED.

### 17.2 Source-fidelity rule

The paper discusses dynamic re-replication and re-balancing conceptually, but it does not define:

- deletion rule;
- replacement trigger;
- replica selection for deletion;
- ordering;
- consistency procedure.

### 17.3 Contract rule

The adapter must not invent any deletion or replacement policy.

The simulator may execute deletion or replacement only after a separately documented researcher decision supplies the missing policy. The EIMORM policy itself is:

- RESEARCHER-REQUIRED

not source-defined EIMORM behavior.

---

## 18. Failure Handling Contract

### 18.1 Source status

Failure handling is UNRESOLVED.

### 18.2 Source-fidelity rule

The paper notes conceptual fault tolerance through replication, but it does not provide an executable:

- failure detector;
- failure model;
- recovery algorithm;
- repair policy;
- re-replication trigger;
- failed-node exclusion policy.

### 18.3 Implementation boundary

Failure-event generation belongs to COMMON-SIMULATOR-REQUIRED. Any EIMORM recovery policy remains UNRESOLVED and requires a separate RESEARCHER-REQUIRED extension; neither is source-defined EIMORM behavior.

---

## 19. Multi-Objective Contract

### 19.1 Source status

The five objectives are source-discussed concepts, but their full optimization formulation is UNRESOLVED.

The five source-discussed optimization dimensions are:

1. Availability
2. Cost
3. Load balancing
4. Energy consumption
5. Latency / service time

### 19.2 Contract rule

The implementation may treat these as five source-discussed optimization dimensions, but it may not invent:

- weights;
- normalization;
- scalarization;
- Pareto dominance;
- NSGA-II;
- NSGA-III;
- weighted sum;
- fitness function;
- objective aggregation;

unless explicitly marked researcher-defined.

### 19.3 Required distinction

The project must preserve the distinction between:

- “five source-discussed optimization dimensions”
- “a complete executable five-objective optimization formulation”

The latter is not source-defined.

---

## 20. Trigger / Invocation Contract

### 20.1 Source status

The trigger policy is UNRESOLVED.

### 20.2 Source-supported behavior

The source supports:

- two conceptual phases;
- high-access / popularity-related replication discussion;
- a user-budget condition for IEK.

### 20.3 Not source-defined

The exact trigger policy is not defined in the paper, including:

- exact event trigger;
- periodic interval;
- request-count threshold;
- time interval;
- scheduler policy.

### 20.4 Contract rule

If the common simulator requires an invocation schedule, that schedule is:

- RESEARCHER-REQUIRED

not EIMORM behavior.

---

## 21. State Mutation and Replica Catalog Contract

### 21.1 Ownership

The source-level EIMORM logic does not own the full runtime replica-catalog state in an executable sense.

The ownership boundary is:

- EIMORM / adapter: source-level calculations and decision inputs that are actually specified
- simulator: physical state, capacity validation, execution of state changes, and catalog persistence
- researcher-defined layer: missing policies required to make an experiment executable

### 21.2 Contract rule

The adapter must not silently mutate simulator state beyond the contractually defined interface.

The simulator is responsible for:

- writing replica catalog entries;
- validating feasibility;
- serializing state;
- handling updates consistent with the chosen simulator policy.

---

## 22. Simulator Interface Contract

This section defines conceptual interfaces without generating implementation code.

### 22.1 Interface A — Simulator → EIMORM adapter

Purpose:

- provide source-level data needed for EIMORM evaluation

Inputs:

- current file metadata
- data-center metadata
- access history and timestamps
- cost context
- budget context
- availability context
- storage/capacity state
- catalog state

Classification:

- source-defined or simulator-defined depending on the specific field
- not all fields are paper-defined with precise semantics

Outputs:

- EIMORM-compatible data bundle for source-supported analysis

Validation responsibility:

- simulator validates state quality and availability of runtime values

### 22.2 Interface B — Adapter → EIMORM source-level logic

Purpose:

- pass the source-supported EIMORM inputs into the conceptual logic

Inputs:

- file and block metadata
- access time and recency-related values
- replica-factor context
- budget context
- cost context
- availability and load context

Outputs:

- EIMORM source-level analysis object
- unresolved decision placeholders where needed

Classification:

- source-defined only for supported fields
- unresolved outputs permitted

### 22.3 Interface C — EIMORM adapter → Simulator

Purpose:

- return the results of a source-supported analysis or unresolved decision object

Outputs allowed:

- `ReplicaFactorDecision = {...}`
- `ReplicaCreationDecision = UNRESOLVED`
- `TargetReplicaCount = UNRESOLVED`
- `PlacementDecision = UNRESOLVED`
- `ProviderSelection = UNRESOLVED`
- `DeletionDecision = UNRESOLVED`

This interface must not return a fabricated final action where the paper does not provide the rule.

---

## 23. Unresolved Decisions / Researcher-Defined Extension Points

The following decisions are unresolved in the paper and require researcher-defined behavior if the project runs an experiment:

1. executable ETBDF function
2. ETBDF threshold or weighting cutoff
3. exact replica-count rule
4. exact target replica-count formula
5. exact create / no-create rule
6. exact placement rule
7. exact provider selection rule
8. exact IEK optimization objective and capacity semantics
9. exact cost threshold and budget handling
10. exact deletion / replacement policy
11. exact failure recovery policy
12. exact objective weights for the five objectives
13. exact invocation schedule for the full EIMORM process
14. any concrete simulator scheduling or event trigger model presented as source-defined behavior

These extension points must be marked as:

- RESEARCHER-REQUIRED

and must never be automatically treated as source-defined EIMORM behavior.

---

## 24. Prohibited Assumptions

The implementation MUST NOT assume any of the following:

- repaired ETBDF equation;
- exact ETBDF threshold;
- exact replica-count formula;
- EARF threshold;
- direct EARF → create-replica mapping;
- cheapest-provider selection;
- nearest-provider selection;
- least-loaded-provider selection;
- arbitrary placement heuristic;
- invented IEK knapsack formulation;
- invented deletion policy;
- invented failure-recovery algorithm;
- invented objective weights;
- invented normalization;
- invented Pareto optimization;
- invented invocation schedule presented as source behavior;
- importing behavior from other replication algorithms.

Any of the above must remain UNRESOLVED in this contract. A separately documented researcher or common-simulator policy may define an extension, but that policy is not EIMORM source behavior.

---

## 25. Traceability Matrix to EIMORM-spec.md

| Contract Requirement | EIMORM-spec.md Section | Classification | Implementation Treatment | Notes |
| --- | --- | --- | --- | --- |
| EIMORM is a multi-objective cloud replication strategy | sections 1–3 | SOURCE-REQUIRED | Preserve identity and conceptual scope | No executable objective vector is implied |
| multi-tier heterogeneous architecture | section 4 | SOURCE-REQUIRED | Preserve architecture roles | Common simulator supplies runtime state |
| ETBDF concept | section 8 | UNRESOLVED | Preserve recency semantics; do not repair equation | Exact executable formula is blocking |
| `tc`, `ts`, `λ` | section 8 | SOURCE-REQUIRED | Preserve named meanings | Lambda value and formula use remain unresolved |
| EARF formula | section 9 | SOURCE-REQUIRED | Preserve `ARFk(one) = RFk / (RFk + RFk_old)` | Formula alone does not produce an action |
| EARF-to-replica creation mapping | section 9 | UNRESOLVED | Return unresolved output | No executable mapping is supplied |
| replica creation | section 9, section 26 | UNRESOLVED | Do not infer create/no-create | Conceptual Phase 2 discussion is incomplete |
| replica count | section 9, section 26 | UNRESOLVED | Do not infer a count formula | No exact formula is supplied |
| availability metrics | section 10 | UNRESOLVED | Preserve concepts, not damaged equations | Exact formulas and thresholds block execution |
| cost objective | section 11 | UNRESOLVED | Preserve cost dimension only | Exact executable model is incomplete |
| user budget trigger | section 11 | RESEARCHER-REQUIRED | Treat as an external configuration if used | Source gives no threshold or value |
| IEK role | section 16 | UNRESOLVED | Preserve conceptual budget-aware role | No knapsack formulation is supplied |
| placement logic | section 17 | UNRESOLVED | Return unresolved placement | No executable rule is given |
| deletion / replacement | section 18 | UNRESOLVED | Do not invent a policy | Dynamic re-replication is conceptual only |
| failure handling | section 19 | UNRESOLVED | Do not infer recovery | Fault tolerance is conceptual only |
| five objectives | section 15 | UNRESOLVED | Preserve named dimensions only | No formal vector, weights, or aggregation |
| trigger policy | section 7, section 20 | UNRESOLVED | Common invocation is external | No deterministic event trigger is specified |
| replica catalog ownership | section 4, section 25 | COMMON-SIMULATOR-REQUIRED | Simulator owns mutation and persistence | EIMORM reads context only |
| experimental setup | section 22 | COMMON-SIMULATOR-REQUIRED | Treat CloudSim/environment as common setup | Workload values remain external decisions |
| source-fidelity boundary | sections 23–27 | SOURCE-REQUIRED | Preserve uncertainty and prohibit repairs | This is a contract rule |

---

## 26. Final Implementation Readiness Assessment

| Capability | Classification | Implementation readiness | Reason |
| --- | --- | --- | --- |
| File identification | UNRESOLVED | LIMITED | ETBDF concept is source-defined, but exact executable formula is unresolved |
| ETBDF | UNRESOLVED | LIMITED | OCR-damaged formula and no unambiguous threshold |
| Availability | UNRESOLVED | LIMITED | probability-based concepts exist, but formulas are incomplete |
| EARF | UNRESOLVED | LIMITED | formula is explicit, but mapping to create/no-create or count is unresolved |
| Replica creation | UNRESOLVED | LIMITED | conceptual phase-2 decision exists, but no executable final rule |
| Replica count | UNRESOLVED | LIMITED | dynamic count is discussed, but exact formula is missing |
| Cost | UNRESOLVED | LIMITED | cost is central and named, but objective and threshold details are absent |
| IEK | UNRESOLVED | LIMITED | conceptual budget-driven cost optimization exists, but the algorithm is not provided |
| Placement | UNRESOLVED | NOT READY | no concrete placement rule in the paper |
| Provider selection | UNRESOLVED | NOT READY | no source-defined provider policy |
| Deletion / replacement | UNRESOLVED | NOT READY | conceptual re-replication and re-balancing do not specify a concrete rule |
| Failure handling | UNRESOLVED | NOT READY | no recovery or failure-detection policy |
| Load balancing | UNRESOLVED | LIMITED | objective exists, but metric formulas are incomplete |
| Energy | UNRESOLVED | LIMITED | energy objective exists, but exact model is not implementation-ready |
| Latency | UNRESOLVED | LIMITED | latency objective exists, but exact formula is not implementation-ready |
| Multi-objective optimization | UNRESOLVED | NOT READY | five goals are named, but no executable objective function is provided |
| Trigger policy | UNRESOLVED | LIMITED | conceptual phases and budget trigger exist, but no deterministic runtime schedule |

### A. READY TO IMPLEMENT

Only a narrow set of things can be implemented source-faithfully without assuming missing behavior:

- the conceptual multi-tier architecture;
- the source-level distinction of file identification, Phase 2, and budget-triggered IEK discussion;
- explicit handling of the ETBDF concept as a recency-based access-weight idea;
- explicit handling of the EARF formula as a source-defined replica-factor expression;
- explicit preservation of unresolved decisions as outputs rather than invented decisions;
- separation of source behavior from simulator-defined or researcher-defined behavior.

### B. BLOCKED BY SOURCE / RESEARCH DECISION

The following cannot be implemented source-faithfully without separate researcher-defined choices:

- executable ETBDF function;
- exact replica-count rule;
- exact create/no-create rule;
- exact provider placement logic;
- exact provider selection rule;
- exact IEK algorithm;
- exact deletion / replacement strategy;
- exact failure-recovery policy;
- exact multi-objective optimization formulation;
- exact trigger schedule, runtime invocation policy, or event frequency;
- any concrete heuristic or threshold not named in the source.

---

## Final implementation-readiness statement

This implementation contract is intentionally conservative. It makes EIMORM look less complete than a generalized replication strategy would look, but it is faithful to the source paper.

The key rule is simple:

- keep source-defined behavior separate from researcher-defined behavior;
- keep simulator-defined behavior separate from EIMORM behavior;
- never convert unresolved or partially defined EIMORM behavior into a source-defined algorithm.

When the source is incomplete:

- document the gap;
- define the interface boundary;
- mark the decision as RESEARCHER-REQUIRED or UNRESOLVED;
- keep the source behavior separate.

This contract therefore defines a reproducible and honest implementation boundary for EIMORM without claiming scientific completeness that the paper does not support.

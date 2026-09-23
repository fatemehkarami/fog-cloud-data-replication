# OGSA implementation contract

## 1. Purpose and scope

This document defines the implementation boundary for OGSA only from the current source-of-truth specification in [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md).

The purpose is not to complete missing source behavior. The purpose is to define a precise boundary between:

- source-defined OGSA behavior
- partially specified OGSA behavior
- researcher-defined extensions
- simulator-defined behavior
- unresolved behavior

This contract is not executable code and not an implementation of OGSA itself.

## 1A. Phase 14 execution decisions

| Decision | Source support | Researcher decision | Reason |
|---|---|---|---|
| Binary assignment representation | Ψ is source-defined binary file/node assignment | Row-major tuple matrix `(file_index, node_index)` | Directly represents Ψ and supports source constraints. |
| Continuous-to-binary conversion | Not specified by source | Position `>= 0.5` maps to 1; otherwise 0 | Simple deterministic threshold compatible with binary Ψ. |
| Population initialization | Random initialization is source-supported | Fixed population `8`; positions uniform in `[0,1]`, velocity in `[-1,1]`, using the isolated OGSA RNG | Small fixed executable population with reproducible stream use. |
| Feasibility | At-least-one assignment and capacity constraints are source-defined | Deterministic repair assigns empty rows to least-used nodes and removes overflowing assignments in stable file/node order | Enforces source constraints without changing the objective. |
| Bounds/parameters | Bounds and optimizer parameters are incomplete | `lower=0`, `upper=1`, `g0=1`, `epsilon=1e-9`, `generations=5`; equal MOF weights `0.2` | Fixed pre-execution configuration; no tuning. |
| Objective edge cases | Source objective names/equations are retained | Zero access contributes zero MST; equal-fitness masses are uniform; invalid dimensions/NaN/infinite values are rejected | Avoids NaN/infinity without inventing a new objective. |
| OBL + GSA order | CMP-RD-013 resolves OBL + GSA identity | Initialize, evaluate original/opposite candidates, retain best, then perform GSA mass/gravity/acceleration/velocity/position updates for five generations | Explicit deterministic project execution order. |
| gbest/ties | Source mentions best agents but tie details are incomplete | Stable fitness then population-index ordering; top 2% rounded down with minimum one agent | Reproducible tie handling. |
| Placement | Assignment matrix is source-defined; runtime mapping is not | Require `file_id`; return assigned healthy/reachable node IDs as a common `PLACEMENT` decision; common runtime mutates state | Preserves adapter read-only boundary. |
| Lifecycle/failure | No source-defined deletion, replacement, recovery, or automatic re-replication | Placement only; unsupported lifecycle operations remain outside OGSA; CMP-RD-005 events remain external | Avoids importing behavior from other methods. |

These are researcher interpretations where the source is incomplete, not claims that OGSA specifies the selected conversion, repair, bounds, or population values.

Classification values used throughout:

- SOURCE-REQUIRED
- RESEARCHER-REQUIRED
- COMMON-SIMULATOR-REQUIRED
- IMPLEMENTATION-DETAIL
- UNRESOLVED

The system must not treat unresolved or researcher-defined behavior as source-defined OGSA behavior.

---

## 2. Source-of-truth rules

This document is derived only from [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) and must not add behavior not traceable there.

Source-of-truth requirements:

- Treat [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) as the only authoritative source for OGSA behavior.
- Preserve the exact terminology already established there:
  - SOURCE-REQUIRED
  - UNRESOLVED
  - UNRESOLVED
  - experiment-specific parameter values
- Do not silently repair OCR-damaged formulas.
- Do not infer implementation rules from generic cloud replication practice.
- Do not import behavior from EIMORM, DPRS, HSR, HDFS, NSGA-II, NSGA-III, or other replication algorithms.
- Do not convert an unresolved or partially defined concept into source-defined OGSA behavior.

The contract must explicitly separate:

- what the paper states;
- what the paper implies but does not define sufficiently;
- what must be chosen by the researcher or simulator to run an experiment.

---

## 3. Terminology and status classification

### 3.1 Status classification rules

- SOURCE-REQUIRED
- The paper explicitly provides the concept, variable, or formula in a source-faithful way.

- RESEARCHER-REQUIRED
- A decision is required to make the algorithm executable in the project, but the paper does not specify it.

- COMMON-SIMULATOR-REQUIRED
- A behavior belongs to the execution environment rather than to the source algorithm.

- IMPLEMENTATION-DETAIL
- A software-handling detail is needed without changing OGSA scientific behavior.

- UNRESOLVED
- The paper does not provide enough information to implement source-faithfully.

### 3.2 Required interpretation rule

Any capability that is not directly and specifically defined in OGSA-spec.md must be treated as one of:

- RESEARCHER-REQUIRED
- COMMON-SIMULATOR-REQUIRED
- UNRESOLVED

It must not be silently labeled SOURCE-REQUIRED.

---

## 4. OGSA responsibilities

OGSA responsibilities are limited to source-supported behaviors in the paper.

At the OGSA layer, the implementation may do the following only when explicitly supported by [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md):

- represent files and data nodes;
- represent the binary assignment matrix Ψ;
- enforce the integrity constraint and capacity constraint;
- initialize candidate solutions;
- generate opposite solutions using OBL;
- evaluate fitness using the source-defined objective function;
- evaluate the five objectives MFU, MST, LV, EC, and ML;
- compute the weighted MOF;
- minimize MOF;
- compute mass, acceleration, gravitational constant, velocity, and position updates using the source-defined GSA equations;
- iterate until a maximum number of iterations is reached;
- select the best solution found;
- return the replicated-file solution represented by the final assignment.

OGSA must not implement anything beyond this unless it is explicitly marked as researcher-defined or simulator-defined and documented as such.

Specifically, OGSA must not assume or implement:

- a separate replica-count formula not in the source;
- nearest-node, cheapest-node, least-loaded-node, highest-availability, random, ranking, or weighted placement heuristics;
- a deletion or replacement rule;
- failure recovery logic;
- a live-cloud invocation schedule;
- a Pareto optimizer or NSGA method;
- a generic cloud replication policy not in the paper.

---

## 5. Data model / required inputs

This section lists the inputs explicitly supported by OGSA-spec.md.

| Input | Meaning | Classification | Owner | Required | Experiment-specific |
| --- | --- | --- | --- | --- | --- |
| files | set of files F = {F1, ..., Fn} | COMMON-SIMULATOR-REQUIRED | simulator / adapter | Yes | No |
| file size | S_i for file F_i | COMMON-SIMULATOR-REQUIRED | simulator / adapter | Yes | No |
| file access rate | R_i for file F_i | COMMON-SIMULATOR-REQUIRED | simulator / adapter | Yes | No |
| data nodes | set of nodes DN = {DN1, ..., DNm} | COMMON-SIMULATOR-REQUIRED | simulator / adapter | Yes | No |
| node failure probability | P_j for data node DNj | SOURCE-REQUIRED | simulator / adapter | Yes | Partially |
| node transfer rate | TR_j for data node DNj | COMMON-SIMULATOR-REQUIRED | simulator / adapter | Yes | Partially |
| node capacity | C_j for data node DNj | COMMON-SIMULATOR-REQUIRED | simulator / adapter | Yes | Partially |
| node network speed / bandwidth | B_j or network speed | COMMON-SIMULATOR-REQUIRED | simulator / adapter | Yes | Partially |
| access rate at node | A(i,j) | COMMON-SIMULATOR-REQUIRED | simulator / adapter | Yes | Partially |
| load | L_j / L(i,j) | COMMON-SIMULATOR-REQUIRED | simulator / adapter | Yes | Partially |
| power values | Pmax(j), Pidle(j) | COMMON-SIMULATOR-REQUIRED | simulator / adapter | Yes | Partially |
| α1..α5 | objective weights in MOF | RESEARCHER-REQUIRED | researcher / experiment config | Yes | Yes |
| population size | number of candidate solutions | RESEARCHER-REQUIRED | researcher / experiment config | Yes | Yes |
| number of generations | maximum iterations | RESEARCHER-REQUIRED | researcher / experiment config | Yes | Yes |
| non-uniformity parameter | optimizer parameter mentioned in experiments | RESEARCHER-REQUIRED | researcher / experiment config | Yes | Yes |
| lower/upper bound for OBL | L_d, U_d | SOURCE-REQUIRED | optimizer | Yes | No |
| iteration counter | k | IMPLEMENTATION-DETAIL | optimizer | Yes | No |
| best fit | minimum MOF value | IMPLEMENTATION-DETAIL | optimizer | Yes | No |
| worst fit | maximum MOF value | IMPLEMENTATION-DETAIL | optimizer | Yes | No |
| gbest set | first 2% agents with best fitness | SOURCE-REQUIRED | optimizer | Partially | Partially |
| epsilon | small positive constant | SOURCE-REQUIRED | optimizer | Partially | Partially |
| rand | uniform random number in [0,1] | SOURCE-REQUIRED | optimizer | Yes | No |

Important boundary:

- The source defines the parameter names and several experiment-specific values.
- It does not define a complete general-purpose execution contract beyond the displayed equations and optimization loop.
- Missing parameter semantics are not source-defined; each must receive one controlled classification before use.

---

## 6. Decision representation

The implementation contract for the assignment matrix is:

### Ψij

where:

- Ψij = 1 if file Fi is assigned to data node DNj
- Ψij = 0 otherwise

This is SOURCE-REQUIRED.

The source-defined constraints are:

### Σ_j Ψij > 0

and:

### Σ_i Ψij × S_i ≤ C_j

These are SOURCE-REQUIRED.

Contract rule:

- The assignment matrix is the source-defined representation of file-to-data-node placement.
- The assignment matrix implicitly encodes replica placement.
- No additional constraint may be introduced without being explicitly supported in OGSA-spec.md.

---

## 7. Objective function contract

The OGSA paper explicitly defines five objectives:

- U1 = MFU (mean file unavailability)
- U2 = MST (mean service time)
- U3 = LV (load variance)
- U4 = EC (energy consumption)
- U5 = ML (mean latency)

The source-defined weighted objective is:

### MOF(Ψ) = α1U1(Ψ) + α2U2(Ψ) + α3U3(Ψ) + α4U4(Ψ) + α5U5(Ψ)

The source statement is that MOF is minimized.

The paper reports the configuration:

### α1 = α2 = α3 = α4 = α5 = 0.2

This is SOURCE-REQUIRED as an experiment-specific source configuration.

Contract rule:

- The weighted sum objective remains the source-defined objective formulation.
- Do not introduce normalization, Pareto dominance, alternative scalarization, NSGA, or additional objective functions.
- Do not describe OGSA as NSGA-II, NSGA-III, or any other optimizer not explicitly supported by the paper.

---

## 8. Objective formula contract

This section preserves the objective formulas exactly as supported by OGSA-spec.md.

### 8.1 MFU

Source-defined conceptual formula:

### P(F_i unavailable) = Π_j Ψij × P_j

### MFU = U1(Ψ) = (1/n) × Σ_i P(F_i unavailable)

Status:

- UNRESOLVED

Implementation treatment:

- available as a conceptual objective term;
- exact OCR quality and notation are imperfect in the extracted source;
- do not silently repair the formula.

### 8.2 MST

Source-defined formulas:

### ST(i,j) = Ψ(i,j) × S_i / TR_j

### ST(i) = Σ_j ST(i,j) × A(i,j) / A(i)

### MST = U2(Ψ) = (1/n) × Σ_i ST(i)

Status:

- SOURCE-REQUIRED

Implementation treatment:

- implement only as the paper presents the formula;
- preserve notation and ambiguity where the source text is extracted or OCR-heavy.

### 8.3 LV

Source-defined formulas:

### L(i,j) = A(i,j) × ST(i,j)

### L_j = Σ_i L(i,j)

### L = (1/m) × Σ_j L_j

### LV = U3(Ψ) = Σ_j (L_j − L)^2 / (m − 1)

Status:

- SOURCE-REQUIRED

Implementation treatment:

- keep the objective as the source-defined variance formulation;
- do not add additional balancing heuristics.

### 8.4 EC

Source-defined conceptual formula:

### EC = (1 + 1/Q) × Σ_j Σ_i Ψ(i,j) × L(i,j) × (Pmax(j) − Pidle(j)) + Pidle(j)

Status:

- UNRESOLVED

Implementation treatment:

- preserve the source-defined structure and noted OCR ambiguity;
- do not invent a new energy expression.

### 8.5 ML

Source-defined conceptual formulas:

### L_i = (1/r) × Σ_j Ψ(i,j) × (S_i / B_j) × A(i,j)

### ML = U5(Ψ) = Σ_i L_i / n

Status:

- UNRESOLVED

Implementation treatment:

- preserve the objective as source-defined;
- do not transform it into an alternative latency model.

---

## 9. OBL contract

The source-defined opposite-solution equation is:

### oS_id = L_d + U_d − S_id

Status:

- SOURCE-REQUIRED

Contract rule:

- Preserve this equation exactly as the paper presents it.
- Do not add OBL mechanisms not explicitly present in the source text.

Required inputs:

- S_id: current agent position in dimension d
- L_d: lower bound in dimension d
- U_d: upper bound in dimension d

Required output:

- oS_id: opposite agent position in dimension d

---

## 10. GSA contract

This contract documents only the GSA equations explicitly supported by OGSA-spec.md.

### 10.1 Mass calculation

### m_i(k) = (Fit_i(k) − worst_fit(k)) / (best_fit(k) − worst_fit(k))

### M_i(k) = m_i(k) / Σ_j m_j(k)

Status:

- SOURCE-REQUIRED

### 10.2 Acceleration

### A_i^d(k) = Σ_{j ∈ gbest, j != i} rand × G(k) × M_j(k) × (s_j^d(k) − s_i^d(k)) / (R_ij(k) + ε)

Status:

- SOURCE-REQUIRED

### 10.3 Gravitational constant

### G(k) = G0 × (1 − k / K)

### G0 = g_max(y_U − y_L)

Status:

- SOURCE-REQUIRED

### 10.4 Velocity and position updates

### V_i^d(k + 1) = rand × V_i^d(k) + a_i^d(k)

### S_i^d(k + 1) = S_i^d(k) + V_i^d(k + 1)

Status:

- SOURCE-REQUIRED

Contract rule:

- Keep only the equations explicitly present in the source.
- Do not import a standard GSA implementation from elsewhere.
- Do not infer missing parameter semantics beyond the names already presented in the paper.

---

## 11. Hybridization ambiguity

This is a critical boundary requirement.

The source-spec preserves a contradiction:

- the paper describes OGSA as OBL + GSA;
- another passage mentions OBL + GSO.

This ambiguity must be preserved.

Status:

- UNRESOLVED for the hybridization identity and its precise executable form

Contract rule:

- Do not silently choose GSA or GSO as the definitive scientific identity.
- Do not claim the paper definitively resolves the hybridization.
- At the same time, the contract may state that the paper explicitly provides GSA-based equations and a GSA-style iterative update process.

---

## 12. File selection

The source does not provide a separate, standalone file-selection heuristic.

The source-supported interpretation is:

- file assignment and replication decisions are represented by the optimization over Ψ;
- a candidate solution contains assignment decisions for files across nodes;
- selection is implicit in the optimization, not specified by a separate file-ranking rule.

Status:

- UNRESOLVED

Prohibited additions:

- popularity threshold
- top-K selection
- ranking rule
- access-rate cutoff
- manual filtering

---

## 13. Replica creation

The source states that replication is part of the optimizer, and the optimization produces a placement assignment matrix.

The source does not provide a separate create/no-create rule.

Status:

- UNRESOLVED for the existence of the optimization-based replica decision and any exact runtime create/no-create logic

Contract rule:

- assignment existence is source-defined;
- concrete runtime creation action is not separately specified by the source.

---

## 14. Replica count

The paper identifies the problem of deciding how many replicas to create, but it does not provide a precise formula.

Status:

- UNRESOLVED for the problem statement and any exact target-count formula

Prohibited additions:

- target replica-count formula
- replication-factor equation
- minimum or maximum replica count rule
- count derived from MFU or objective thresholds

---

## 15. Placement / node selection

The placement logic is represented through the assignment matrix Ψ and optimized by the objective function.

The source does not provide any separate node-selection heuristic such as:

- nearest node
- cheapest node
- highest availability
- least-loaded node
- random placement
- ranking rule
- weighted placement heuristic

Status:

- UNRESOLVED for the exact selection mechanism outside the optimizer

---

## 16. Cost

The source discusses cost considerations at a high level, but does not define a standalone executable cost function or budget model.

Status:

- UNRESOLVED for a source-defined cost formula

Contract rule:

- Do not import EIMORM-style budget logic or any other algorithm-specific cost mechanism.
- Keep cost as an objective-tradeoff concept, not as an executable source-defined model.

---

## 17. Failure / recovery

The paper uses failure probability as an input and uses it in the availability objective.

The source does not provide:

- a failure detector
- a failure model
- a recovery algorithm
- a repair process
- a failed-node exclusion rule
- a re-replication trigger after failure

Status:

- SOURCE-REQUIRED for the use of node failure probability in the model
- UNRESOLVED for failure handling and recovery policy

---

## 18. Deletion / replacement

The source does not define a deletion or replacement policy.

Status:

- UNRESOLVED

Contract rule:

- No deletion trigger
- No replacement rule
- No ordering or consistency policy may be invented

---

## 19. Dynamic replication

The source defines an iterative optimization loop that updates solutions over generations.

This is not the same as a live-cloud dynamic re-replication schedule.

Status:

- UNRESOLVED for iterative solution updates and runtime dynamic replication behavior

---

## 20. Trigger / invocation

The paper defines the optimizer's own internal iteration and termination condition:

- maximum generation count
- best fitness selection
- solution update loop

This is different from a live-cloud replication trigger.

Status:

- SOURCE-REQUIRED for optimizer iteration and max-iteration termination
- UNRESOLVED for live-cloud invocation scheduling

Contract rule:

- Do not invent reoptimization triggers based on time, request count, or event detection.

---

## 21. Simulator responsibilities

The simulator owns runtime and operational behavior that the paper does not specify as source-defined OGSA behavior.

Examples include, only when supported by OGSA-spec.md:

- execution environment and state persistence
- capacity enforcement at runtime
- workload generation
- experiment scheduling
- runtime state mutation
- physical node state or system-host state

Status:

- COMMON-SIMULATOR-REQUIRED

Contract rule:

- Anything not defined in the paper remains out of scope for OGSA itself.
- Do not attribute simulator responsibilities to the source algorithm.

---

## 22. Interface contract

This is a conceptual interface contract only; it does not define executable code.

### 22.1 Simulator → OGSA adapter

Allowed inputs only:

- file set
- node set
- file size and access rate
- node failure probability, transfer rate, capacity, bandwidth
- objective-related state needed by the source-defined model
- optimizer parameters explicitly supported by the paper

Status:

- Each field is classified individually as SOURCE-REQUIRED, COMMON-SIMULATOR-REQUIRED, or UNRESOLVED.

### 22.2 Adapter → OGSA logic

Pass conceptual state required for:

- assignment matrix Ψ
- objective evaluation
- OBL and GSA steps
- best/worst fitness comparison
- iteration updates

Status:

- Each field is classified individually as SOURCE-REQUIRED, COMMON-SIMULATOR-REQUIRED, or UNRESOLVED.

### 22.3 OGSA → Simulator

Return conceptual outputs only:

- final assignment / replicated-file solution
- best objective value or best fitness if available
- unresolved fields where the source does not define them

Status:

- Each interface field must be classified individually as SOURCE-REQUIRED, COMMON-SIMULATOR-REQUIRED, or UNRESOLVED; no combined classification is assigned.

Contract rule:

- The output must not include invented replica-count or placement heuristics.

---

## 23. Researcher-defined extension points

The following decisions are not source-defined and therefore require researcher choices only if the project decides to run the algorithm experimentally:

- exact parameter semantics beyond the paper's explicit names
- exact hybridization choice between GSA and GSO if a definitive identity is required
- exact interpretation of replica count from the assignment matrix
- exact runtime create/no-create policy
- exact runtime placement execution model
- deletion / replacement policy
- failure recovery policy
- live-cloud invocation schedule
- workload generation details not reported in the source
- any experiment-specific tuning not explicitly fixed by the paper

Status:

- RESEARCHER-REQUIRED

Contract rule:

- These cannot be silently treated as source-defined OGSA behavior.

---

## 24. Experimental parameters

The OGSA paper reports the following experiment-specific values:

- 8 data nodes
- 200 generations
- population size 20
- non-uniformity parameter 2
- α1..α5 = 0.2
- node failure probabilities: 0.002, 0.003, 0.005, 0.004, 0.001, 0.006, 0.001, 0.001
- transfer rates: 350, 200, 150, 225, 250, 175, 325, 300 MB/s
- capacities: 200, 150, 100, 120, 200, 250, 100, 150 GB
- network speed: 1000 Mbit
- Java (JDK 1.6)
- CloudSim tools
- Windows 7 environment

Status:

- A for the source-reported experiment values
- C for any broader generalization beyond those values

Contract rule:

- Keep experiment values separate from general algorithm requirements.
- Do not convert example values into universal algorithm constants.

---

## 25. Prohibited assumptions

This contract explicitly prohibits:

- repairing OCR formulas
- adding standard GSA equations not present in the source
- choosing GSO versus GSA without source support
- inventing replica-count formulas
- inventing placement heuristics
- importing EIMORM IEK or other EIMORM logic
- importing NSGA-II or NSGA-III behavior
- inventing failure recovery
- inventing deletion policies
- inventing runtime schedules
- inventing objective weights
- inventing constraints
- inventing workload assumptions

---

## 26. Traceability matrix

| Requirement | OGSA-spec section | Classification | Implementation treatment | Notes |
| --- | --- | --- | --- | --- |
| Ψ assignment matrix | Section 4, 5, 23 | SOURCE-REQUIRED | Binary file-to-data-node decision matrix |
| integrity constraint | Section 5, 23 | SOURCE-REQUIRED | Σ_j Ψij > 0 |
| capacity constraint | Section 5, 23 | SOURCE-REQUIRED | Σ_i Ψij × S_i ≤ C_j |
| MFU | Section 13, 22, 23 | UNRESOLVED | Availability objective preserved; OCR ambiguity remains |
| MST | Section 15, 22, 23 | SOURCE-REQUIRED | Source formula provided |
| LV | Section 14, 22, 23 | SOURCE-REQUIRED | Source formula provided |
| EC | Section 17, 22, 23 | UNRESOLVED | OCR-damaged formula preserved as unresolved |
| ML | Section 15, 22, 23 | UNRESOLVED | Source objective exists; notation remains imperfect |
| MOF | Section 7, 22, 23 | SOURCE-REQUIRED | Weighted objective function |
| OBL | Section 7, 23 | SOURCE-REQUIRED | oS_id = L_d + U_d − S_id |
| GSA equations | Section 7, 23 | SOURCE-REQUIRED | mass, acceleration, G, velocity, position |
| hybridization | Section 2, 11 | UNRESOLVED | OBL + GSA versus OBL + GSO remains unresolved |
| replica count | Section 9, 10 | UNRESOLVED | No source formula |
| placement | Section 11 | UNRESOLVED | via Ψ; no separate heuristic |
| node selection | Section 12 | UNRESOLVED | Optimizer assignment is source-supported; no separate policy |
| failure probability | Section 13, 19 | SOURCE-REQUIRED | Availability uses failure probability |
| failure recovery | Section 19 | UNRESOLVED | No source-defined recovery algorithm |
| deletion | Section 18 | UNRESOLVED | No source-defined policy |
| dynamic behavior | Section 20 | UNRESOLVED | Optimizer updates are not runtime trigger policy |
| trigger / invocation | Section 21 | UNRESOLVED | Internal iteration versus live invocation remains distinct |
| experiment parameters | Section 25, 26 | SOURCE-REQUIRED | Source-reported values only |

---

## 27. Implementation readiness assessment

| Capability | Classification | Readiness | Explanation |
| --- | --- | --- | --- |
| assignment matrix Ψ | SOURCE-REQUIRED | READY | Fully specified as source-defined decision representation |
| integrity and capacity constraints | SOURCE-REQUIRED | READY | Explicitly provided in the source |
| objective formulation | SOURCE-REQUIRED | READY | Weighted-sum multi-objective formulation is explicit |
| objective functions MFU, MST, LV | SOURCE-REQUIRED | LIMITED | Source formulas are present, but some ambiguity remains in extracted notation |
| EC, ML | UNRESOLVED | LIMITED | Present, but partially damaged or notation-imperfect in extraction |
| OBL | SOURCE-REQUIRED | READY | Explicit opposite-solution formula is present |
| GSA update equations | SOURCE-REQUIRED | READY | Explicit equations are present in the paper |
| hybrid identity | UNRESOLVED | NOT READY | Source inconsistency is preserved, no definitive resolution |
| replica count | UNRESOLVED | NOT READY | Problem is recognized but no formula is given |
| placement selection | UNRESOLVED | NOT READY | Placement is represented by assignment optimization, but no heuristic is source-defined |
| failure recovery | UNRESOLVED | NOT READY | Not source-defined |
| deletion / replacement | UNRESOLVED | NOT READY | Not source-defined |
| live runtime trigger | UNRESOLVED | NOT READY | Internal optimizer iteration is not live-cloud invocation |

---

## 28. Reproducibility boundary

### What can be reconstructed source-faithfully from OGSA-spec.md?

- the objective set and weighted objective function
- the assignment matrix and constraints
- the OBL update equation
- the GSA formulas explicitly present in the paper
- the optimizer loop and termination condition
- the source-reported experiment parameter values
- the explicit ambiguity and unresolved areas in the source text

### What cannot be reconstructed without researcher-defined decisions?

- exact hybridization choice if a definitive identity is required
- exact replica-count policy
- exact placement selection rule beyond the optimizer
- delete or replacement logic
- failure recovery logic
- runtime invocation policy
- general live-cloud execution schedule
- any behavior hidden by OCR-damaged or incomplete equations

---

## 29. Final self-audit

This implementation contract has been checked against the source-fidelity requirements in [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md).

Confirmed:

- no implementation code was created: PASS
- no researcher decisions were selected as source behavior: PASS
- no EIMORM behavior was imported: PASS
- no formulas were silently repaired: PASS
- no unsupported GSA or OBL behavior was added: PASS
- OBL + GSA / GSO ambiguity was preserved: PASS
- no replica-count heuristic was invented: PASS
- no placement heuristic was invented: PASS
- no failure / recovery algorithm was invented: PASS
- no runtime trigger was invented: PASS
- source-reported experiment values were kept separate from general requirements: PASS
- every unresolved behavior remains explicitly marked: PASS

This contract remains a faithful implementation boundary document derived only from OGSA-spec.md and does not extend the source beyond its stated scientific meaning.

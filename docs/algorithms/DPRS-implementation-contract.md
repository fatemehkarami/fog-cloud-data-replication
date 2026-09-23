# DPRS implementation contract

## 1. Purpose and source identity

This document defines the implementation contract for DPRS as a source-faithful specification only.

DPRS refers to:

- Dataset Replica Placement Strategy under a Response Time Constraint
- Source paper: "Dataset replica placement strategy under a response time constraint in the cloud"
- Authors: Xiuguo Wu and Wei Su
- Publication context: Int. J. Information Technology and Management, Vol. 18, No. 1, 2019

This contract is derived only from:

- [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md)
- [DPRS.pdf](DPRS.pdf)
- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md)
- [docs/06-common-domain-model.md](docs/06-common-domain-model.md)
- [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md)

## 1A. Phase 13 execution decisions

| Decision | Source support | Researcher decision | Reason |
|---|---|---|---|
| Queue/wait equation | Printed source structure is preserved; OCR/queue notation is incomplete and the printed formula can produce nonphysical values | Preserve the printed `Tw = rho / (lambda - mu)` function for source-faithful calculations; reject undefined rates rather than repair the equation | Avoids silently replacing the source equation. |
| Aggregate response time | Source defines total response-time concepts but not one runtime aggregation rule | Arithmetic mean of available component totals for a DPRS decision epoch | Simple deterministic aggregation without pooling requests as experiments. |
| Response-time threshold | Source discusses `T_upper` but does not fix a common executable value | Fixed `10.0 s` request parameter, recorded with the DPRS configuration and never tuned | Supplies the source-context threshold without importing another method's rule. |
| Equal-weight/tie behavior | Source does not define executable tie handling | Stable lexical ordering of node/edge IDs; equal graph weights no longer return unresolved solely because of a tie | Deterministic placement output. |
| Invocation | DPRS is a placement method under a response-time constraint | Invoke on each admitted read request requiring a placement evaluation; do not add a replica-count trigger | Keeps invocation request-driven and method-specific. |
| Placement translation | Source selects placement sites/nodes; common runtime validates node targets | Return `file_id` and capacity/health-valid `placement_node_ids`; common executor performs validation/state mutation | Integrates DPRS output without direct adapter mutation. |
| Lifecycle | Source does not define selection, creation lifecycle, deletion, replacement, or recovery | DPRS emits placement only; deletion/replacement/failure recovery remain no-op/unsupported outside this adapter | Prevents invented lifecycle behavior. |
| Randomness | No DPRS algorithm-local RNG is source-required | No RNG added | Preserves deterministic graph placement for fixed inputs. |

These are researcher decisions required for executable integration, not claims that the DPRS paper specifies the selected threshold, tie rule, or aggregation value.

This document is not a code specification and does not create C# or executable implementation logic.

It documents the scientific behavior that the source paper explicitly supports and distinguishes this from simulator-owned behavior that must be implemented separately.

Classification labels:

- SOURCE-REQUIRED for DPRS scientific behavior
- COMMON-SIMULATOR-REQUIRED where the simulator owns runtime execution, validation, and state mutation
- RESEARCHER-REQUIRED where the project must choose a behavior not fixed by the source paper
- UNRESOLVED where the source paper is incomplete or ambiguous

---

## 2. Scope of DPRS

DPRS is a placement optimization method under a response-time constraint.

It is not, in the current source, a full end-to-end replication-management algorithm in the sense of:

- request-time replica selection
- provider selection
- replica creation lifecycle management
- replica replacement or deletion policy
- dynamic replica-count determination
- failure-handling policy

The source provides a graph-theoretic replica placement strategy for selecting storage sites based on response-time and network/resource considerations.

This document therefore defines DPRS as a source-faithful placement decision method only, unless a source statement explicitly states otherwise.

Classification:

- SOURCE-REQUIRED for placement optimization
- UNRESOLVED for request-time lifecycle operations

---

## 3. Source-defined problem

The source problem is stated as follows:

- In cloud data-intensive environments, large datasets are stored across distributed data centers.
- To reduce user response time, replica placement must be chosen carefully.
- Too many replicas are infeasible in practice.
- The key issue is to choose suitable data-center locations for dataset replicas while satisfying response-time constraints.

The paper proposes a model for:

- estimating response time
- converting the placement problem to a graph problem
- solving the placement problem with an approximate algorithm based on minimum spanning tree / Kruskal-style pruning

The paper does not define a complete request-time replication process, replica lifecycle management, or algorithmic failure handling.

Classification:

- SOURCE-REQUIRED for response-time-based replica placement
- UNRESOLVED for broader replication-management behavior

---

## 4. Source-defined inputs

The DPRS source explicitly defines the following input concepts.

### 4.1 Data-center inputs

- data-center identifier dci
- average storage price sp_i
- total storage capacity ts_i
- vacant space vs_i

### 4.2 Dataset inputs

- dataset identifier d_i
- dataset size s_i
- store place s_p
- usage frequency UF

### 4.3 Network and performance inputs

- distance or edge cost between data centers
- data transfer bandwidth between data centers
- storage read/write speed or disk speed RS
- queue parameters for requests arriving at a data center
- request arrival rate λ_m
- service rate μ_m
- wait access latency T_w
- write/read time T_w/r
- transfer time T_trsf
- response-time threshold T_upper as a scenario/evaluation parameter used in the paper's reported analysis

### 4.4 Graph inputs

- vertex set V representing data centers
- edge set E representing connections between data centers
- edge weight function f(e)
- vertex latency / write-read functions f1(v), f2(v)

Classification:

- SOURCE-REQUIRED

---

## 5. Source-defined data-center and dataset model

The paper defines a data center as a four-tuple:

- (dci, sp_i, ts_i, vs_i)

Where:

- dci = data-center identifier
- sp_i = average storage price
- ts_i = total storage capacity (unit TB in the paper)
- vs_i = vacant space / extra storage capacity

The paper defines a dataset as a four-tuple:

- (d_m, s_i, s_p, UF)

Where:

- d_m = dataset identifier
- s_i = dataset size
- s_p = store place
- UF = usage frequency in a certain time period

Important restriction:

The source defines data-center and dataset structure for the placement model. It does not define a complete runtime replica catalog lifecycle, including request-time replica creation, replacement, and deletion policy.

Classification:

- SOURCE-REQUIRED for data-center and dataset structure
- UNRESOLVED for runtime replica lifecycle semantics

---

## 6. Response-time model

The paper defines the response time of a dataset request as:

T_di = T_w + T_w/r + T_trsf

### Meaning of variables

- T_di = response time of a dataset request for dataset d_i
- T_w = wait access latency
- T_w/r = write/read time
- T_trsf = data transfer time

### Classification of formula

- Fully specified in concept, but the exact OCR-transcribed notation is partially fragmented in the source extraction.
- The decomposition is source-defined and clear.
- Status: UNRESOLVED, with minor extraction ambiguity in notation formatting.

The paper also defines a total response time for a dataset d_i on data center dc_m as a sum over dataset responses and time factors:

T_dcm = Σ (x_dcm × T_di × η_ti × T)

The source text indicates this as a total response-time expression over a set of data items and time periods.

### Meaning of variables

- T_dcm = total response time of dataset d_i on data center dc_m
- x_dcm ∈ {0,1} = indicator whether dc_m stores a replica of d_i
- T_di = one dataset response time
- η_ti = usage frequency of the dataset during period T
- T = time span (example: one day)

### Classification

- UNRESOLVED due to OCR-heavy notation
- Source-defined intent is clear, but implementation should treat the formula as a paper-defined model and not silently replace it with a different response metric.

---

## 7. Queue/wait-latency model

The paper models the wait latency as an M/M/1/∞/∞ queue system.

The source states the system as:

- first M = request arrivals frequency, determined by a Poisson process
- second M = service time, determined by an exponential distribution
- one server
- infinite queue length and infinite number of requests

The source states the average wait-access latency formula exactly as printed in Theorem 1:

Tw = ρm / (λm − μm)

with:

ρm = λm / μm

### Meaning of variables

- λm = request arrival rate
- μm = service rate per data center
- ρm = traffic intensity
- Tw = average wait access latency

Source-fidelity note:

The printed equation appears inconsistent with the conventional stable M/M/1 formulation, but this implementation contract preserves the equation exactly as published in the source paper rather than silently correcting it.

Important caution:

The source provides the queue abstraction and response-time decomposition, but not a request-time or provider-level decision algorithm based on queue latency alone.

---

## 8. Read/write time model

The paper defines write/read time as proportional to dataset size and inversely proportional to disk speed:

T_w/r = (d_i.s_i / RS) × γ

### Meaning of variables

- T_w/r = write/read time for dataset d_i
- d_i.s_i = dataset size
- RS = hard-disk rotational speed in rpm
- γ = proportionality coefficient used to adjust units

### Classification

- SOURCE-REQUIRED
- Fully specified in the paper at the conceptual level

The paper gives an example using 1 GB and 5,400 rpm, with γ = 55, producing roughly ten seconds.

This is an implementation-level example, not a universal constant unless the project explicitly adopts it.

---

## 9. Transfer-time model

The paper defines transfer time as:

T_trsf = (d_i.s_i / bandwidth(dc_j, dc_k)) × ξ

### Meaning of variables

- T_trsf = single dataset transfer time
- d_i.s_i = dataset size
- bandwidth(dc_j, dc_k) = network transport capacity between data centers j and k
- ξ = adjustment coefficient used to align units

### Classification

- SOURCE-REQUIRED
- Fully specified at the conceptual level

The source also states that if more than one path exists between two data centers, the transfer time is the minimum transfer time among possible paths for the current simple model.

This is a source-defined simplification for the placement algorithm.

---

## 10. Response-time constraint

The source defines the placement problem under a response-time constraint.

The article repeatedly states that the placement algorithm is designed to minimize response time, and the paper's reported analysis/evaluation scenario uses a response-time threshold of T_upper = 10 seconds.

This 10-second value is specifically used in the paper's reported analysis/evaluation scenario. It is not specified as a universal DPRS algorithm input and it is not described as a universally hard-coded runtime rule.

The threshold is described qualitatively as:

- choose replica placements that minimize the response time needed to serve requests
- compare alternative replica degrees and evaluate whether the resulting response time is below the reported scenario threshold

Important interpretation:

- Response-time constraint is a source-defined optimization target for placement
- T_upper = 10 seconds is a scenario-specific threshold used in the paper's reported analysis
- T_upper is not specified as a universal algorithm input
- It does not define a request-time, algorithmic decision rule for replica creation or provider selection

Classification:

- SOURCE-REQUIRED for the optimization target
- RESEARCHER-REQUIRED if a project chooses a different numerical threshold or policy

---

## 11. Graph construction

The source converts the placement problem into a graph model.

Definitions:

- each data center dci is a vertex vi
- the set V is the vertex set
- each connection between two data centers becomes an edge e
- the set E is the edge set
- transfer time or adjusted response cost becomes the edge weight function f(e)
- vertices with replica storage are from subset P ⊆ V

The optimization problem is described as selecting a tree T from graph G(V, E, f) such that:

- P ⊆ V_T ⊆ V
- E_T ⊆ E
- minimize Σ f(e) + Σ f(v)

This objective is clearly stated in source language as a tree-selection problem similar to a Steiner-tree formulation, though the paper reduces it to an approximate minimum-spanning-tree solution.

### Classification

- SOURCE-REQUIRED
- Fully specified at the conceptual level

Important caution:

This graph construction is about placement optimization, not about algorithmic request handling or replica-selection decisions during runtime.

---

## 12. Virtual-vertex construction

The source describes an algorithm that creates virtual vertices as candidate replica store locations.

The algorithm steps are described in source language:

1. Initialize a virtual vertex set V′
2. For each real vertex v_i ∈ V, create a corresponding virtual vertex v′_i
3. Add edges between real and virtual vertices, representing shortest path or routing cost to the destination data center

The source text states that the algorithm first creates a set of virtual vertices as candidate replica store places and then constructs a spanning graph G″.

This is source-defined algorithmic structure.

### Meaning of variables

- V = real data-center set
- V′ = virtual data centers representing candidate replica-store sites
- G″ = auxiliary graph for the algorithm

### Classification

- SOURCE-REQUIRED
- UNRESOLVED in prose and algorithm steps
- Not a lifecycle management algorithm; it is a placement-site construction step

---

## 13. Edge/vertex weight transformation

The paper describes the transformation of weights from vertices to edges before computing a minimum spanning tree.

The source equation is:

w'(dcp,dcq)
= w(dcp,dcq)
+ [Tw/r(dcp) + Tw(dcp)] / deg(dcp)
+ [Tw/r(dcq) + Tw(dcq)] / deg(dcq)

### Meaning of variables

- w(dcp,dcq) = original edge weight between data centers p and q
- w'(dcp,dcq) = new edge weight after assigning vertex cost to adjacent edges
- Tw/r(dcp) = write/read time at data center p
- Tw(dcp) = wait access latency at data center p
- deg(dcp) = degree of vertex dcp

### Classification

- Source-defined transformation
- Preserved exactly as published in the source paper
- Status: SOURCE-REQUIRED

The purpose is to convert vertex-based latency and I/O costs into edge costs so that the placement problem can be solved with a spanning-tree approximation.

---

## 14. Minimum-spanning-tree / Kruskal procedure

The source describes a replica placement algorithm based on Kruskal's minimum spanning tree.

Algorithm steps, as transcribed from the source:

1. Initialize an edge-weighted graph G′′ = (V′′, E′′, f′′(e))
2. Add edges between real and virtual vertices
3. Set edge weights using the shortest path in the original graph
4. Generate a minimum spanning tree T of G″ using Kruskal's algorithm
5. Delete low-degree virtual vertices and neighboring edges
6. Remove redundant vertices and edges
7. Output the remaining vertex set as the replica-placement set

The source explicitly states that the algorithm is an approximate algorithm using Kruskal's minimal spanning tree.

### Classification

- SOURCE-REQUIRED
- This is the clearest point of DPRS implementation readiness

### Important limitation

This is a placement algorithm, not a full request-time replica lifecycle algorithm.

---

## 15. Low-degree virtual-vertex pruning

The source says that after building the minimum spanning tree, the algorithm deletes virtual vertices and their adjacent edges whose degree is 1.

This is a source-defined pruning rule used to eliminate redundant candidate replica locations.

The source also gives the conceptual rationale:

- certain virtual vertices are redundant
- a candidate replica location cannot coexist with its duplicate virtual form if it becomes the same logical placement site

### Classification

- SOURCE-REQUIRED
- Algorithmic structure is clear

---

## 16. Redundant edge/vertex removal

The source describes additional cleanup in the tree:

- delete redundant DCs and connections
- delete redundant edges where multiple virtual-vertex options exist and the larger-weight edge is removed

This is source-defined and is part of the approximate placement algorithm.

### Classification

- SOURCE-REQUIRED

---

## 17. Final placement output

The source concludes that the remaining candidate DCs are selected as replication placement sites.

The example in the paper selects a final set such as:

- {dc1, dc4, dc6}

This is the final output of the placement algorithm.

### Meaning

- the algorithm outputs the set of data centers where replicas should be stored
- it does not define a request-time mechanism for selecting among current replicas in a file request
- it does not define a provider-selection policy

### Classification

- SOURCE-REQUIRED for placement-site output
- UNRESOLVED for request-time usage of those locations

---

## 18. Placement decision contract

The DPRS placement decision contract is:

- Input: cloud graph, data-center state, dataset metadata, network weights, response-time model
- Compute: candidate replica placement sites using graph construction, edge weighting, and Kruskal-based pruning
- Return: a set of selected data centers for placement of a dataset replica

This is the authoritative DPRS scientific behavior.

The contract must preserve the difference between:

- DPRS placement decision
and
- simulator-owned execution of the placement decision

The simulator owns validation and mutation.

The adapter may return a placement decision only if the source contract supports it as a placement optimization.

Classification:

- SOURCE-REQUIRED for placement decision semantics
- COMMON-SIMULATOR-REQUIRED for execution boundary

---

## 19. DPRS Adapter Execution Contract

The DPRS adapter operates under a strict READ → COMPUTE → RETURN boundary.

### 19.1 Allowed adapter responsibilities

The DPRS adapter may:

- read the current simulator state;
- read data-center information;
- read dataset metadata;
- read network/graph information;
- obtain the parameters required by the DPRS response-time model;
- execute the source-defined DPRS placement algorithm;
- return the resulting placement set (SCRD).

### 19.2 Adapter non-mutation boundary

The DPRS adapter must NOT directly mutate:

- replica catalog;
- file catalog;
- storage usage;
- node health;
- network state;
- request state;
- event queue;
- simulation clock;
- common metrics.

This boundary is COMMON-SIMULATOR-REQUIRED.

### 19.3 Placement decision output

DPRS scientific output:

- a set of selected data-center locations (SCRD) where replicas should be placed.

This output is SOURCE-REQUIRED.

SCRD must not be reinterpreted as:

- a replica provider;
- a request-time replica selector;
- a replacement decision;
- a dynamic replica-count optimizer.

The simulator-side execution of SCRD is COMMON-SIMULATOR-REQUIRED.

### 19.4 Simulator-side execution of SCRD

DPRS computes:

- placement decision

The simulator performs:

- validation
- feasibility checking
- state mutation
- replica creation / event scheduling
- metric recording

If a selected placement is invalid under common simulator constraints, the simulator may reject or handle that decision according to the project's common validation policy.

This validation/execution behavior is COMMON-SIMULATOR-REQUIRED and is not DPRS scientific behavior. Any project-specific rejection choice remains RESEARCHER-REQUIRED.

### 19.5 Trigger and applicability policy

The DPRS paper does not define a runtime trigger condition for invoking the placement algorithm.

For the comparative simulator, the researcher must select a common invocation policy for placement algorithms so that DPRS can be evaluated in the same experimental framework.

This is RESEARCHER-REQUIRED. The simulator supplies the common invocation facility, classified as COMMON-SIMULATOR-REQUIRED.

The DPRS paper also does not specify whether the placement algorithm is invoked:

- for every dataset,
- only for popular datasets,
- only on request,
- periodically.

This is UNRESOLVED.

The project must choose a common experimental invocation policy, and that policy is RESEARCHER-REQUIRED; the invocation facility is COMMON-SIMULATOR-REQUIRED.

### 19.6 Replica catalog relationship

DPRS does not directly own or mutate the common replica catalog.

The DPRS adapter returns SCRD.

The common simulator maps the accepted placement decision into the simulator's replica-placement representation and performs the actual state mutation.

Classification:

- SCRD = SOURCE-REQUIRED
- mapping / execution = COMMON-SIMULATOR-REQUIRED

### 19.7 End-to-end integration pseudocode

Conceptual pseudocode only:

OnPlacementInvocation:
    state = Simulator.GetReadOnlyState()

    decision = DPRSAdapter.ComputePlacement(state)

    validatedDecision = Simulator.ValidatePlacement(decision)

    if validatedDecision is valid:
        Simulator.ExecutePlacement(validatedDecision)

    Simulator.RecordMetrics()

Classification:

- DPRS logic = SOURCE-REQUIRED
- state access, validation, execution, metric recording = COMMON-SIMULATOR-REQUIRED

---

## 20. Storage and validity constraints

The source defines response-time and graph-based placement but does not define a complete storage lifecycle rule.

The following points are explicit:

- response time depends on storage access latency and transfer time
- storage capacity and vacant-space data are defined in the data-center model
- the placement optimization is influenced by data-center resources and network connectivity

The data-center model includes storage-related attributes such as total storage and vacant space, but the source does not define an explicit storage-capacity feasibility rule within RPRC.

Storage-capacity validation performed by the simulator is a common execution constraint and is not part of the source-defined DPRS placement algorithm.

The following are not explicitly defined by the source:

- a precise enforced storage-capacity algorithm for deciding whether a replica may be created
- deletion when storage is insufficient
- dynamic replica-count cap enforcement
- exact timeout or invalidity rules for placements

If the project chooses a specific response to infeasible placement, such as:

- reject placement,
- skip placement,
- record infeasibility,

that choice must be marked RESEARCHER-REQUIRED; runtime enforcement is COMMON-SIMULATOR-REQUIRED.

Do not add deletion or replacement logic to DPRS.

Classification:

- SOURCE-REQUIRED for the data-center and dataset model
- COMMON-SIMULATOR-REQUIRED for runtime capacity enforcement
- UNRESOLVED for explicit DPRS storage policy rules

---

## 21. Failure handling and node availability

Failure handling is UNRESOLVED / NOT DEFINED IN SOURCE.

Node failure and recovery are generated and managed by the common simulator. DPRS does not receive an invented source-defined failure-handling mechanism.

If a DPRS placement decision is affected by a failed or unavailable node, the simulator applies the common validity / feasibility policy.

This classification is COMMON-SIMULATOR-REQUIRED.

DPRS is not defined by the source as an algorithm that decides how to recover from failure or to re-plan after node loss.

---

## 22. Unsupported or unresolved capabilities

The DPRS source does not explicitly define the following capabilities as algorithmic behaviors:

- Replica selection: UNRESOLVED
- Provider selection: UNRESOLVED
- Replica creation: UNRESOLVED
- Replica deletion/replacement: UNRESOLVED
- Dynamic replica count: UNRESOLVED
- Failure handling: UNRESOLVED

The only clear capability supported by the source is:

- Placement optimization: YES

Classification matrix:

| Capability | Status |
| --- | --- |
| Replica selection | UNRESOLVED |
| Provider selection | UNRESOLVED |
| Replica creation | UNRESOLVED |
| Replica deletion/replacement | UNRESOLVED |
| Dynamic replica count | UNRESOLVED |
| Placement optimization | YES |
| Failure handling | UNRESOLVED |

This is intentionally strict and source-faithful.

---

## 23. Parameters and source-defined constants

The source defines the following as paper-specific model elements:

- dci, sp_i, ts_i, vs_i
- d_i, s_i, s_p, UF
- T_di, T_w, T_w/r, T_trsf
- λ, μ, ρ
- RS
- γ
- ξ
- graph weights and adjacency structure
- T_upper in the example analysis

### Important status of parameter values

The paper does define the model structure, but it does not define a universal implementation-ready parameterization for all simulation environments.

Thus:

- source-defined constants/structures: SOURCE-REQUIRED
- numerical values assigned in example contexts: RESEARCHER-REQUIRED unless explicitly mandated by the project

### Formula-specific status

- T_di = T_w + T_w/r + T_trsf: SOURCE-REQUIRED
- T_w/r = (d_i.s_i / RS) × γ: SOURCE-REQUIRED
- T_trsf = (d_i.s_i / bandwidth(dc_j, dc_k)) × ξ: SOURCE-REQUIRED
- Tw queue formula: SOURCE-REQUIRED as printed in the paper: Tw = ρm / (λm − μm), ρm = λm / μm
- w' transformation formula: SOURCE-REQUIRED as printed in the paper: w'(dcp,dcq) = w(dcp,dcq) + [Tw/r(dcp) + Tw(dcp)] / deg(dcp) + [Tw/r(dcq) + Tw(dcq)] / deg(dcq)
- graph and spanning-tree algorithm: SOURCE-REQUIRED

---

## 24. Tie-breaking and unspecified behavior

The source does not define explicit tie-breaking rules for:

- equal edge weights
- equal placement cost among candidate sites
- equal virtual-vertex degrees
- equal response-time outcomes

Therefore:

- tie-breaking is not source-defined scientific behavior
- any deterministic tie-breaker used by the project must be documented as RESEARCHER-REQUIRED
- it must not be presented as a source-defined property of DPRS

Classification:

- UNRESOLVED in the source
- RESEARCHER-REQUIRED if a project chooses a deterministic rule for implementation

---

## 25. Randomness

The source does not define an algorithmic stochastic component for DPRS placement.

The placement algorithm is graph-based and deterministic once the graph, weights, and candidate sites are fixed.

Therefore:

- DPRS is not described as requiring algorithm-local random seed behavior
- any randomness in a project implementation would belong to the simulator or researcher setup, not the DPRS paper itself

Classification:

- SOURCE-REQUIRED: no random algorithmic component identified
- RESEARCHER-REQUIRED if project-specific random generation is added outside the paper

---

## 26. Complexity

The source describes the algorithmic complexity in broad terms:

- Algorithm 1 contains one loop over the edges, but the paper also states that, with an adjacency-matrix representation, calculating vertex degrees requires O(n²).
- Kruskal's minimum spanning tree is polynomial-time.
- Additional graph pruning and removal steps are O(n).

The paper states that Algorithm 1 is O(n²) under the adjacency-matrix representation. For Algorithm 2 / RPRC, the paper reports total time complexity O(n²).

This source-reported complexity is distinct from actual implementation complexity, which depends on the concrete data structures, graph representation, and execution environment and should be measured separately.

Classification:

- SOURCE-REQUIRED
- Actual implementation performance should be measured separately from the source-reported complexity

---

## 27. Source-fidelity rules

The following source-fidelity rules are mandatory for any DPRS implementation contract.

1. DPRS is a placement decision method, not a full replication-management method.
2. Do not infer request-time replica selection from the paper.
3. Do not infer provider selection from the paper.
4. Do not infer dynamic replica-count determination from the paper.
5. Do not infer replacement or deletion logic from the paper.
6. Do not infer failure-handling behavior from the paper.
7. Keep the graph-based placement optimization separate from simulator-owned execution.
8. Mark any behavior not supported by the paper as UNRESOLVED or RESEARCHER-REQUIRED.
9. If a scientific gap exists, do not repair it by assumption.
10. If the exact formula is OCR-ambiguous, preserve the ambiguity and mark it as unresolved rather than silently correcting it.

Classification:

- SOURCE-REQUIRED for the placement logic
- UNRESOLVED for unsupported lifecycle capabilities

---

## 28. Implementation-readiness checklist

The DPRS source is implementation-ready only for the following:

- [ ] Data-center and dataset model is defined.
- [ ] Response-time decomposition is defined.
- [ ] Wait-latency model is defined conceptually.
- [ ] Read/write and transfer-time models are defined conceptually.
- [ ] Graph representation is defined.
- [ ] Virtual-vertex construction is defined.
- [ ] Weight transformation is defined conceptually.
- [ ] Kruskal-based minimum spanning tree step is defined.
- [ ] Low-degree pruning is defined.
- [ ] Redundant-edge and redundant-vertex removal is defined.
- [ ] Final placement output is defined conceptually.

The DPRS source is not implementation-ready for the following unless separately specified by a researcher or additional source material:

- [ ] request-time replica selection
- [ ] provider selection
- [ ] replica creation lifecycle
- [ ] replacement or deletion
- [ ] dynamic replica count
- [ ] failure handling

---

## Remaining Scientific Gaps

The following items remain genuinely source-undefined as DPRS scientific behavior:

- request-time replica selection
- provider selection
- replacement or deletion
- dynamic replica count
- failure handling as a DPRS algorithmic behavior

The following items are not DPRS scientific behavior. Project policy is RESEARCHER-REQUIRED and runtime integration is COMMON-SIMULATOR-REQUIRED:

- invocation policy for placement algorithm
- mapping from SCRD to simulator replica representation
- validation and feasibility checking
- execution of accepted placement decisions
- replica-catalog mutation boundary
- storage-capacity enforcement policy
- handling of failed or unavailable nodes in the common simulator

### Integration Decisions

The project must choose a common experimental invocation policy for placement algorithms so that DPRS can be evaluated in the same framework.

The project must also choose:

- when placement decisions are evaluated during the experiment;
- how accepted SCRD values are mapped into the simulator's state model;
- which feasibility checks are enforced before mutation;
- how infeasible placements are rejected or recorded;
- how replica catalog updates are performed by the simulator;
- how timing and event scheduling are coordinated with the common environment.

These decisions are RESEARCHER-REQUIRED; their runtime facilities are COMMON-SIMULATOR-REQUIRED and must not be described as DPRS scientific behavior.

---

## Freeze Criteria

This contract is ready to freeze when:

- DPRS scientific behavior is fully separated from simulator behavior;
- SCRD is clearly defined as the placement output;
- the adapter uses READ → COMPUTE → RETURN;
- the simulator uses VALIDATE → EXECUTE → MUTATE → RECORD;
- no unsupported DPRS lifecycle behavior has been invented;
- all researcher-defined integration policies are explicitly labeled;
- all remaining source ambiguities are preserved.

---

## Final classification summary

DPRS source-faithful capability summary:

| Capability | Classification |
| --- | --- |
| Replica selection | UNRESOLVED |
| Provider selection | UNRESOLVED |
| Replica creation | UNRESOLVED |
| Replica deletion/replacement | UNRESOLVED |
| Dynamic replica count | UNRESOLVED |
| Placement optimization | YES |
| Failure handling | UNRESOLVED |

This document intentionally keeps DPRS as a placement-optimization method under a response-time constraint and does not convert it into a full end-to-end replication-management algorithm without explicit source support.

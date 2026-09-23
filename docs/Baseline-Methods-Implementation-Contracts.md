# Baseline Methods Implementation Contracts

## Scope and scientific boundary

This document converts the four published baseline methods into implementation-focused contracts while preserving scientific fidelity to the source specifications.

The source files are the authoritative definitions:

- [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md)
- [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md)
- [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md)
- [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md)
- [docs/Proposed-Method-Implementation-Contract.md](docs/Proposed-Method-Implementation-Contract.md)

Important rules:

- Do not invent, infer, modernize, improve, or add mechanisms that are not explicitly supported by the corresponding source specification.
- Do not copy the Proposed Method into any baseline.
- Do not add the Proposed Method OIS formula, NSGA-III objective set, or dynamic replica-number rule to any baseline.
- If something is not specified in the source, it is listed as:
  - NOT SPECIFIED IN SOURCE
  - or
  - UNRESOLVED — RESEARCHER DECISION
- For every method, algorithm logic is separated from common simulator infrastructure.

---

## 1. HRS

### 1.1 Method identity

- Full method name: Hybrid Replication Strategy (HRS) with fuzzy-based deletion for heterogeneous cloud data centers
- Original source: [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md)
- Main purpose: dynamic data replication for heterogeneous cloud data centers, improving availability, performance, and load balance
- Type of replication strategy: dynamic replication strategy
- Performs:
  - replica selection: YES — SOURCE SPECIFIED
  - replica placement: YES — SOURCE SPECIFIED
  - replica-number determination: NOT SPECIFIED IN SOURCE
  - replica replacement/deletion: YES — SOURCE SPECIFIED (fuzzy-based deletion)
  - request routing: NOT EXPLICITLY STATED AS A SEPARATE ALGORITHM; request handling is implied by file lookup and data-center selection
  - optimization: NO — SOURCE SPECIFIED AS A DECISION POLICY, not a formal optimization algorithm
  - failure handling: NOT SPECIFIED IN SOURCE as a special algorithm mechanism

### 1.2 Algorithm pipeline

Input
→ identify target file / missing file condition
→ choose best site using centrality and access count
→ select replica provider based on VM capability, VM load, and network performance
→ if storage pressure exists, evaluate replica deletion using fuzzy value
→ return replica placement / selection / deletion decisions
→ output final replication state

This pipeline reflects the source description and is not forced into the Proposed Method pipeline.

### 1.3 Inputs

| Name | Meaning | Unit | Source | Static / Dynamic | Status |
|---|---|---|---|---|---|
| File request | Requested data file | file ID | source description | dynamic | YES — SOURCE SPECIFIED |
| File access count | Number of file accesses | count | source description | dynamic | YES — SOURCE SPECIFIED |
| Centrality | Node centrality in the network | normalized score | source description | static/dynamic depending on topology | YES — SOURCE SPECIFIED |
| VM capability | CPU and communication capability | composite metric | source description | dynamic | YES — SOURCE SPECIFIED |
| VM load | Current load on VM / node | queue/service metric | source description | dynamic | YES — SOURCE SPECIFIED |
| Network performance | bandwidth, latency, link quality | Mbps/ms | source description | dynamic/static depending on environment | YES — SOURCE SPECIFIED |
| Replica size | Size of candidate replica | bytes/GB | source description indirectly | dynamic | YES — SOURCE SPECIFIED |
| Last access time | Time since last access | time units | fuzzy deletion input | dynamic | YES — SOURCE SPECIFIED |
| Replication cost | Cost factor in deletion assessment | cost units | source description | dynamic | YES — SOURCE SPECIFIED |
| Storage state | Available storage capacity | capacity units | implied by deletion under restricted storage | dynamic | YES — SOURCE SPECIFIED |
| Data-center topology | Network and graph structure | graph | source description | static | YES — SOURCE SPECIFIED |

### 1.4 Outputs

- selected candidate node for placement
- selected replica provider for request execution
- candidate replicas for deletion
- final updated replica set
- updated file placement state

### 1.5 State changes

- new replica created at best site
- selected replica provider used for access
- low-value replica removed when storage is restricted
- file access counters updated
- node load and centrality fields updated if the simulator tracks them

### 1.6 Mathematical formulation

#### 1.6.1 Placement score

The source describes a merit value:

$$
Merit = W_1 \times NumberOfAccess + W_2 \times Centrality
$$

This was explicitly summarized in the source text.

Required definitions:
- NumberOfAccess = number of accesses to the file or replica candidate
- Centrality = centrality measure used in the network graph
- $W_1$, $W_2$ = weight values determined empirically

Source requirement: values are normalized to a 1–10 scale before applying the formula.

UNRESOLVED — RESEARCHER DECISION: the exact normalization method and exact centrality formulation in the source excerpt are not fully explicit in the extracted specification.

#### 1.6.2 Replica selection

The source states that the method uses a combined cost function using:
- VM capability
- VM load
- network performance

The exact formula is not fully captured in the available HRS specification.

UNRESOLVED — RESEARCHER DECISION: exact formula for the combined cost function must be extracted from the original paper or provided by the researcher.

#### 1.6.3 Fuzzy deletion value

The source states that the fuzzy inference system has three inputs:
- number of accesses
- cost
- time interval between current time and last access

and one output:
- value

The rule set is described as fuzzy and uses 21 rules, but the exact formula and membership functions are not fully included in the current specification.

UNRESOLVED — RESEARCHER DECISION: precise fuzzy membership functions and rule base must be extracted from the original paper or provided by the researcher.

#### 1.6.4 Deletion condition

The source states that the replica with the lowest value is the appropriate candidate for deletion.

This yields:

- lowest fuzzy output value = candidate for deletion

This is explicit.

### 1.7 Optimization mechanism

NOT APPLICABLE

HRS is described as a hybrid strategy with fuzzy deletion, not as a formal optimization solver. It is a policy-based method.

### 1.8 Objectives

Source-stated goals:
- improve availability
- improve performance
- improve load balance
- reduce access time
- support better response time

These are goals, not a formal single objective function in the source excerpt.

### 1.9 Constraints

- storage restriction requires deletion of low-value replicas
- candidate placement must consider centrality and access count
- replica selection must favor suitable provider based on VM capability, load, and network performance

This is explicit from the source description.

Mandatory simulator invariants:
- every file must retain at least one valid replica
- last valid replica must not be deleted
- candidate deletion must not violate file availability

These are not HRS-specific objectives but are required common invariants.

### 1.10 Triggering events

- missing file or unavailable replica for a request
- storage pressure or insufficient space on target node
- periodic or event-driven replication decision

The source explicitly states that replication takes place when a task needs the file and it is not present in local storage.

### 1.11 Replica number

- DYNAMIC REPLICATION is the declared strategy
- the source does not define a formal dynamic replica-number calculation formula

Status:
- NOT SPECIFIED IN SOURCE
- DO NOT INVENT A DYNAMIC REPLICA-NUMBER FORMULA

### 1.12 Replacement / deletion

- YES — SOURCE SPECIFIED
- mechanism: fuzzy inference system with three inputs and one output
- deletion candidate: lowest fuzzy value among existing replicas

Important: do not add OIS-based replacement logic or Proposed Method deletion rules.

### 1.13 Request processing

- when a task needs a file and the file is not in local storage, replication occurs
- file is selected from candidate providers using the combined cost function
- a provider with lower cost and better network/VM conditions is preferred

This is source-supported and may be implemented as an algorithm-specific request path.

### 1.14 Failure behavior

The source emphasizes fault tolerance and availability, but it does not provide a special failure-handling algorithm.

Status:
- NOT SPECIFIED IN SOURCE
- common simulation failure handling may model node health separately from algorithm logic

### 1.15 Initial placement

- source describes a best-site placement strategy for new replica
- initial placement rule is not fully specified as a cold-start policy

Status:
- partially described
- not fully formalized in the extracted source specification

### 1.16 Parameters

| Parameter | Meaning | Value from source | Unit | Default value | Source | Configurable? | Status |
|---|---|---|---|---|---|---|---|
| $W_1$ | access weight | empirical | scalar | NOT SPECIFIED | source description | YES | RESEARCHER DECISION |
| $W_2$ | centrality weight | empirical | scalar | NOT SPECIFIED | source description | YES | RESEARCHER DECISION |
| NumberOfAccess | access frequency | integer count | requests | source-defined | source description | YES | SOURCE SPECIFIED |
| Centrality | node centrality | graph score | normalized value | source-defined | source description | YES | SOURCE SPECIFIED |
| Fuzzy inputs | accesses, cost, last access interval | fuzzy variables | domain-specific | NOT SPECIFIED | source description | YES | RESEARCHER DECISION |
| Fuzzy output | replica value | scalar | [0,1] described | NOT SPECIFIED | source description | YES | RESEARCHER DECISION |
| Rule count | fuzzy rules | 21 | integer | 21 | source description | NO | SOURCE SPECIFIED |

### 1.17 Pseudocode

```text
Input: request for file F, current node state, candidate replica set, storage state

if file not found locally then
    identify candidate nodes
    compute site merit using centrality and access count
    select best site for new replica placement
    select best replica provider using VM capability, VM load, and network performance
    if storage is constrained then
        evaluate all existing replicas using fuzzy value
        delete the lowest-value eligible replica
    end if
    create new replica at chosen site
end if

Output: updated replica state
```

This pseudocode uses only behavior explicitly described in the source.

### 1.18 Unit tests

- best site selected by highest merit value
- candidate provider chosen using VM capability / load / network cost
- fuzzy deletion selects the lowest value
- storage pressure triggers deletion
- last valid replica is never deleted
- request for missing file triggers replica decision

### 1.19 Integration tests

- HRS in common simulator with same workload as other methods
- request for missing file executes HRS selection and placement
- HRS deletion is triggered by low storage and not by an external invented rule
- metrics update with HRS-specific decisions

### 1.20 Scientific limitations

- exact fuzzy rules and membership functions are incomplete in the extracted source
- exact replica-selection cost function is incomplete
- exact normalization details are incomplete
- exact initial placement policy under cold start is not fully specified

### 1.21 Researcher decisions required

| Method | Decision required | Why required | Possible options | Recommended option | Impact on validity |
|---|---|---|---|---|---|
| HRS | exact fuzzy membership functions | source summary is incomplete | extract from original paper or researcher-provided specification | extract from original paper first | critical |
| HRS | exact replica selection cost formula | source summary does not fully specify | use exact paper formula or stop | exact paper formula | critical |
| HRS | exact normalization and centrality formula | source summary is incomplete | explicit source formula or researcher-defined normalization | use exact source formulation if available | critical |

---

## 2. DPRS

### 2.1 Method identity

- Full method name: Dataset Replica Placement Strategy under a Response Time Constraint in the Cloud
- Original source: [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md)
- Main purpose: minimize response time by strategically placing dataset replicas among data centers under a response-time constraint
- Type of replication strategy: placement-oriented dataset replica strategy
- Performs:
  - replica selection: NO — NOT SPECIFIED IN SOURCE
  - replica placement: YES — SOURCE SPECIFIED
  - replica-number determination: NO — NOT SPECIFIED IN SOURCE
  - replica replacement/deletion: NO — NOT SPECIFIED IN SOURCE
  - request routing: implicitly through response-time model, but not a special routing method
  - optimization: YES — source uses graph-based approximation via minimum spanning tree / Steiner-like abstraction
  - failure handling: NO — NOT SPECIFIED IN SOURCE

### 2.2 Algorithm pipeline

Input
→ construct graph of data centers and transfer relationships
→ transform vertex delays into edge weights
→ construct candidate replica graph
→ apply minimum spanning tree based placement under response-time constraint
→ output selected replica placement set

This baseline is placement-oriented and does not impose the Proposed Method pipeline.

### 2.3 Inputs

| Name | Meaning | Unit | Source | Static / Dynamic | Status |
|---|---|---|---|---|---|
| Data centers | DC nodes in cloud | IDs | source model | static | YES — SOURCE SPECIFIED |
| Dataset size | size of dataset | bytes/GB | source definition | static | YES — SOURCE SPECIFIED |
| Data-center storage price | storage pricing | cost units | source definition | static | YES — SOURCE SPECIFIED |
| Total storage | available storage in DC | TB | source definition | static | YES — SOURCE SPECIFIED |
| Vacant storage | free capacity | TB | source definition | static | YES — SOURCE SPECIFIED |
| Usage frequency | dataset access frequency | requests/time | source definition | dynamic | YES — SOURCE SPECIFIED |
| Transfer bandwidth | communication capacity between DCs | data rate | source definition | static/dynamic | YES — SOURCE SPECIFIED |
| Wait access latency $T_w$ | queue delay | time units | source model | dynamic | YES — SOURCE SPECIFIED |
| Write/read time $T_{w/r}$ | disk or storage latency | time units | source model | dynamic | YES — SOURCE SPECIFIED |
| Data transfer time $T_{trsf}$ | network transfer time | time units | source model | dynamic | YES — SOURCE SPECIFIED |
| Graph topology | node/edge relationships | graph | source model | static | YES — SOURCE SPECIFIED |
| Response-time threshold | placement constraint | time units | source mentions response-time constraint | researcher decision or source parameter | RESEARCHER DECISION |

### 2.4 Outputs

- subset of graph vertices selected for replica storage
- final replica-placement set or candidate placement set
- response-time-minimizing replica distribution under constraint

### 2.5 State changes

- candidate replica locations selected on the graph
- dataset placement state updated
- no explicit replica deletion or replacement behavior is defined

### 2.6 Mathematical formulation

#### 2.6.1 Total response time

The source defines response time as:

$$
T_{di} = T_w + T_{w/r} + T_{trsf}
$$

This is explicit.

#### 2.6.2 Wait access latency model

The source describes a queue model with M/M/1/∞/∞ and derives average wait access latency:

$$
T_w = \frac{\rho_m}{\lambda_m - \mu_m}
$$

Source text describes this in the theorem section. The exact notation is source-derived and must be preserved as in the original paper.

#### 2.6.3 Disk write/read time

$$
T_{w/r} = \frac{d_i \cdot s_i}{RS} \cdot \gamma
$$

with definitions:
- $d_i.s_i$ = dataset size
- $RS$ = disk rotational speed
- $\gamma$ = adjustment coefficient

This appears in the source excerpt.

#### 2.6.4 Data transfer time

$$
T_{trsf} = \frac{d_i \cdot s_i}{bandwidth(dc_j, dc_k)} \cdot \xi
$$

with definitions:
- $bandwidth(dc_j, dc_k)$ = transfer capacity between DCs
- $\xi$ = adjustment coefficient

#### 2.6.5 Edge-weight transformation

The source explicitly defines the transformation from vertex delay values to edge weights:

$$
w'(dcp, dcq) = w(dcp, dcq) + \frac{(T_{w/r}(dcp)+T_w(dcp))(T_{w/r}(dcq)+T_w(dcq))}{deg(dcp) + deg(dcq)}
$$

This is source-driven and must be preserved if implementing the original algorithm.

#### 2.6.6 Objective

The source defines a graph-based minimum objective concept based on spanning-tree minimization and response-time constraint.

The high-level objective is:

- minimize total response time / graph weight under a response-time constraint

The exact global mathematical optimization is not fully captured in the current source summary, but the source clearly establishes a Steiner-tree-style objective and Kruskal approximation approach.

UNRESOLVED — RESEARCHER DECISION: exact final objective function and thresholding logic must be extracted from the original paper or explicitly defined by the researcher.

### 2.7 Optimization mechanism

- Graph transformation
- Candidate replica selection by graph approximation
- Kruskal minimum spanning tree approach
- Steiner-tree-like abstraction as a placement model

This is explicit in the source and must be preserved as-is.

### 2.8 Objectives

- minimize response time
- respect response-time constraint
- reduce wait latency and transfer delay

This is the source-defined objective set.

### 2.9 Constraints

- response-time constraint
- logical replica placement on graph nodes
- candidate node subset under graph transformation
- minimum spanning-tree-based placement subject to chosen source/replica vertices

This is explicit in the source description.

### 2.10 Triggering events

- initial placement or candidate set construction
- replica placement decision triggered by dataset demand and response-time considerations
- no source-specific failure trigger is defined

### 2.11 Replica number

- NOT SPECIFIED IN SOURCE
- no dynamic replica-count formula is defined

This is a critical boundary: do not apply the Proposed Method formula to DPRS.

### 2.12 Replacement / deletion

- NOT SPECIFIED IN SOURCE

### 2.13 Request processing

The source defines response-time evaluation and queue models, but not a full request scheduler.

The algorithm is placement-driven, not request-driven beyond response-time estimation.

### 2.14 Failure behavior

- NOT SPECIFIED IN SOURCE

### 2.15 Initial placement

- the source defines a graph-based candidate placement strategy, but not a universal initial placement startup rule for simulation

Status:
- source-specific placement logic is specified
- initial placement bootstrap is not fully specified

### 2.16 Parameters

| Parameter | Meaning | Value from source | Unit | Default value | Source | Configurable? | Status |
|---|---|---|---|---|---|---|---|
| $T_w$ | wait latency | derived from queue model | time | source-derived | source model | YES | SOURCE SPECIFIED |
| $T_{w/r}$ | write/read time | formula-based | time | source-derived | source model | YES | SOURCE SPECIFIED |
| $T_{trsf}$ | transfer time | formula-based | time | source-derived | source model | YES | SOURCE SPECIFIED |
| $\lambda_m$ | arrival rate | queue model parameter | requests/time | NOT SPECIFIED | source model | YES | RESEARCHER DECISION |
| $\mu_m$ | service rate | queue model parameter | service/time | NOT SPECIFIED | source model | YES | RESEARCHER DECISION |
| $\gamma$ | read/write coefficient | adjustment coefficient | scalar | NOT SPECIFIED | source model | YES | RESEARCHER DECISION |
| $\xi$ | transfer coefficient | adjustment coefficient | scalar | NOT SPECIFIED | source model | YES | RESEARCHER DECISION |
| response-time constraint | placement threshold | constraint defined by source | time units | NOT SPECIFIED | source model | YES | RESEARCHER DECISION |

### 2.17 Pseudocode

```text
Input: graph G(V, E, f(e)), DCs, dataset, request frequency, storage parameters

construct weighted graph from DC topology
for each edge do
    transform vertex delays to edge weights
end for
build candidate replica graph with virtual vertices
apply Kruskal minimum spanning tree
remove redundant low-degree vertices
select remaining vertices as replica storage set
Output: replica placement subset S
```

This matches the source description without adding unsupported logic.

### 2.18 Unit tests

- edge-weight transformation yields expected transformed graph values
- candidate subset is produced by minimum spanning tree
- redundant low-degree vertices are removed
- output replica set respects graph constraints
- total response time is computed using queue, read/write, and transfer components

### 2.19 Integration tests

- DPRS runs in common simulator with identical topology and workload
- replacement/deletion operations are absent and not added
- placement decisions respect response-time constraint and graph structure
- metrics update from placement decisions without adding unsupported logic

### 2.20 Scientific limitations

- no explicit replica-number mechanism
- no replacement/deletion policy
- no explicit selection mechanism
- exact response-time threshold is not fixed
- exact graph objective and thresholding are incomplete in the source excerpt

### 2.21 Researcher decisions required

| Method | Decision required | Why required | Possible options | Recommended option | Impact on validity |
|---|---|---|---|---|---|
| DPRS | response-time threshold | source uses a constraint but does not fix the numeric value | use researcher-defined threshold or exact paper value | use paper value if available; otherwise explicit researcher-defined threshold | critical |
| DPRS | final exact placement objective | source summary is not fully formalized | use exact paper objective or researcher-specified formalization | exact paper objective when available | critical |
| DPRS | queue model parameters | not fully specified | use common simulator defaults or explicit researcher values | explicit researcher values | important |

---

## 3. EIMORM

### 3.1 Method identity

- Full method name: An Efficient and Improved Multi-Objective Optimized Replication Management with Dynamic and Cost-Aware Strategies in Cloud Computing Data Centers
- Original source: [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md)
- Main purpose: dynamic, cost-aware replication management emphasizing availability, load balancing, cost, and energy efficiency
- Type of replication strategy: dynamic, multi-objective replication strategy
- Performs:
  - replica selection: YES — SOURCE SPECIFIED in the sense of selecting based on replica factor and cost-aware conditions
  - replica placement: YES — SOURCE SPECIFIED
  - replica-number determination: YES — SOURCE SPECIFIED, via replica-factor logic
  - replica replacement/deletion: NOT FULLY SPECIFIED IN SOURCE
  - request routing: implied by access rate and data-center selection
  - optimization: YES — multi-objective and cost-aware optimization described
  - failure handling: implied via availability / failure probability, but not an explicit failure-response algorithm

### 3.2 Algorithm pipeline

Input
→ identify file replica need based on availability and access rate
→ compute replica factor and cost-aware suitability
→ select candidate placement according to availability / cost / load trade-offs
→ create or maintain replicas according to the dynamic replication factor
→ update availability, load, energy, and cost state
→ output updated replica set

### 3.3 Inputs

| Name | Meaning | Unit | Source | Static / Dynamic | Status |
|---|---|---|---|---|---|
| File availability probability | probability that file info remains available | probability | source description | dynamic | YES — SOURCE SPECIFIED |
| Block availability | availability of block copies | probability | source description | dynamic | YES — SOURCE SPECIFIED |
| File access rate $A(i,j)$ | rate of access to file $i$ at node $j$ | requests/time | source formula | dynamic | YES — SOURCE SPECIFIED |
| Data-center bandwidth $B(j)$ | node bandwidth | data rate | source formula | static/dynamic | YES — SOURCE SPECIFIED |
| File size $S_i$ | file size | bytes/GB | source formula | static | YES — SOURCE SPECIFIED |
| Current replica factor $RF_k$ | recent file replication factor | scalar | source description | dynamic | YES — SOURCE SPECIFIED |
| Old replica factor $RF_{kold}$ | prior replica factor | scalar | source description | dynamic | YES — SOURCE SPECIFIED |
| Cost of replication | cost to replicate at a data center | cost units | source description | dynamic | YES — SOURCE SPECIFIED |
| Load variance | imbalance metric | scalar | source objective | dynamic | YES — SOURCE SPECIFIED |
| Failure probability | node or file failure likelihood | probability | source model | static/dynamic | YES — SOURCE SPECIFIED |
| Service time | time to serve access | time units | source objective | dynamic | YES — SOURCE SPECIFIED |

### 3.4 Outputs

- updated replica set for candidate files
- updated availability state
- updated cost state
- updated load-balancing state
- final file placement vector

### 3.5 State changes

- create or maintain replicas according to replication factor
- cost-aware readjustment of placement
- update file availability and load state
- update storage and node capacity state

### 3.6 Mathematical formulation

#### 3.6.1 File availability

The source defines probability of file availability and file unavailability based on replication and node failure probability.

High-level formula described in the source excerpt:

$$
P(F_i) = 1 - P(F_i^{unavailable})
$$

and the system availability is built from the product across node assignments.

This is explicit at a conceptual level.

UNRESOLVED — RESEARCHER DECISION: the exact final probability formula as it appears in the full paper must be extracted from the original paper if implementation needs the exact equation.

#### 3.6.2 Replica-factor rule

The source gives the following conceptual formula:

$$
ARF_K(one) = \frac{RF_K}{RF_K + RF_{Kold}}
$$

or equivalent ratio-based formulation depending on source wording.

This is source-supported but the exact final notation and usage must be matched carefully to the paper.

UNRESOLVED — RESEARCHER DECISION: exact final formula and the precise replication-factor interpretation must be extracted from the original paper.

#### 3.6.3 Mean service time objective

The source provides a service-time formulation involving access rate and data transfer rate.

The structure is explicit but not fully captured in the current extracted spec.

UNRESOLVED — RESEARCHER DECISION: exact final formula must be extracted from the original paper.

#### 3.6.4 Load variance objective

The source provides a load variance model based on access rate and service time.

This is explicit in the source summary and should be preserved as a source-specific objective if implementing the original paper.

#### 3.6.5 Energy objective

The source states that total energy minimization is part of the objective set.

This is explicit in the paper summary, but the exact formula is only partly shown in the extracted excerpt.

UNRESOLVED — RESEARCHER DECISION: exact energy formulation must be extracted from the original paper.

### 3.7 Optimization mechanism

- multi-objective optimization is explicitly stated
- cost-aware and availability-aware decisions are included
- the source mentions improved knapsack logic for cost optimization

However, the precise optimization algorithm and exact equation set are not fully captured in the provided summary.

UNRESOLVED — RESEARCHER DECISION: exact knapsack formulation and objective weighting must be extracted from the original paper.

### 3.8 Objectives

The source describes several objectives:
- mean file unavailability
- mean service time
- load variance
- energy consumption
- latency / access delay

These objectives are source-specific and must not be replaced with the Proposed Method’s five objectives.

### 3.9 Constraints

- maintain availability while balancing cost
- avoid overloading the system
- manage data-center replication cost
- keep file availability above acceptable levels
- respect storage or placement feasibility where implied

The source is not fully explicit on formal constraints, but the objectives and cost-aware conditions are clear enough to keep as implementation constraints.

### 3.10 Triggering events

- file access rate or replication factor changes
- data center cost changes
- file availability below the desired level
- dynamic load or service-time condition

This is source-supported, but not a formal event scheduler description.

### 3.11 Replica number

- YES — SOURCE SPECIFIED, via replication-factor logic
- This is dynamic and cost-aware
- However, the exact final formula is incomplete in the summary

UNRESOLVED — RESEARCHER DECISION: exact dynamic replica-number logic must be extracted from the original paper.

### 3.12 Replacement / deletion

- NOT FULLY SPECIFIED IN SOURCE
- the source discusses replication cost and balancing, but no explicit replacement or deletion rule is fully detailed in the excerpts provided

Status:
- NOT SPECIFIED IN SOURCE
- DO NOT INVENT DELETE LOGIC

### 3.13 Request processing

- the method uses access rate and file availability as part of the decision process
- a request triggers the evaluation of whether a file should be replicated or maintained on more nodes

This is source-supported, but the exact request-handling scheduler is not detailed.

### 3.14 Failure behavior

- failure probability is considered in the availability formulation
- failure response is not a separate algorithmic mechanism in the source excerpt

Status:
- implied in the availability model
- not an explicit algorithmic mechanism

### 3.15 Initial placement

- not fully specified in the source summary

Status:
- NOT SPECIFIED IN SOURCE

### 3.16 Parameters

| Parameter | Meaning | Value from source | Unit | Default value | Source | Configurable? | Status |
|---|---|---|---|---|---|---|---|
| $A(i,j)$ | access rate of file i at node j | source-defined | requests/time | NOT SPECIFIED | source formula | YES | SOURCE SPECIFIED |
| $B(j)$ | bandwidth of node j | source-defined | data rate | NOT SPECIFIED | source formula | YES | SOURCE SPECIFIED |
| $RF_k$ | recent replica factor | source-defined | scalar | NOT SPECIFIED | source description | YES | SOURCE SPECIFIED |
| $RF_{kold}$ | old replica factor | source-defined | scalar | NOT SPECIFIED | source description | YES | SOURCE SPECIFIED |
| $P(F_i)$ | file availability probability | probability | scalar | NOT SPECIFIED | source formula | YES | SOURCE SPECIFIED |
| failure probability | node/file failure risk | probability | scalar | NOT SPECIFIED | source model | YES | RESEARCHER DECISION |
| cost parameters | storage / replication costs | cost units | source-defined | NOT SPECIFIED | source model | YES | RESEARCHER DECISION |

### 3.17 Pseudocode

```text
Input: file request, file metadata, node states, current replica counts, cost and availability metadata

if file availability is insufficient or access rate indicates need then
    compute replica factor and recent/old replica ratio
    estimate availability and cost trade-off
    select candidate data-center locations under cost and load constraints
    create or maintain replicas accordingly
end if

Output: updated replica set
```

This pseudocode stays within the source description and avoids adding unsupported methods.

### 3.18 Unit tests

- replication-factor formula updates correctly
- file availability is computed correctly when the replica set changes
- cost-aware placement is accepted only if the source-defined logic supports it
- load variance computation matches the source model
- file availability remains at least one valid replica after dynamic changes

### 3.19 Integration tests

- EIMORM executes in the common simulator with same input workload and seed schedule
- cost calculations and availability updates are consistent with the source model
- no unsupported replacement logic is introduced

### 3.20 Scientific limitations

- exact replica-factor formula and final objective weighting are incomplete in the extracted source
- the precise knapsack optimization is not fully captured
- exact cost and energy calculations are not fully specified in the extracted summary

### 3.21 Researcher decisions required

| Method | Decision required | Why required | Possible options | Recommended option | Impact on validity |
|---|---|---|---|---|---|
| EIMORM | exact replica-factor formula | source summary is partially ambiguous | use exact paper formula or researcher-defined formulation | exact paper formula | critical |
| EIMORM | objective weighting and normalization | not fully captured | exact paper details or explicit researcher specification | exact paper details if available | critical |
| EIMORM | cost and energy model details | source summary incomplete | extract from original paper or define explicitly | extract from paper | critical |

---

## 4. OGSA

### 4.1 Method identity

- Full method name: Multi-Objective Data Replication in Cloud Computing Environment using Oppositional Gravitational Search Algorithm (OGSA)
- Original source: [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md)
- Main purpose: optimize replica placement using OGSA with multi-objective fitness based on file availability, service time, load variance, energy, and latency
- Type of replication strategy: optimization-based multi-objective replica placement strategy
- Performs:
  - replica selection: NO — NOT SPECIFIED IN SOURCE as a separate mechanism
  - replica placement: YES — SOURCE SPECIFIED
  - replica-number determination: NOT SPECIFIED IN SOURCE as a separate mechanism
  - replica replacement/deletion: NO — NOT SPECIFIED IN SOURCE
  - request routing: not specified as a separate mechanism
  - optimization: YES — SOURCE SPECIFIED
  - failure handling: not specified as an explicit algorithm mechanism

### 4.2 Algorithm pipeline

Input
→ generate initial population of candidate replica assignments
→ evaluate fitness using multi-objective function
→ apply oppositional-based learning and GSA search updates
→ update population and select best candidate solution
→ output optimized replica-placement solution

This is the published pipeline for OGSA as described in the source.

### 4.3 Inputs

| Name | Meaning | Unit | Source | Static / Dynamic | Status |
|---|---|---|---|---|---|
| Number of files | file set size | count | source description | static | YES — SOURCE SPECIFIED |
| Number of data nodes | node count | count | source description | static | YES — SOURCE SPECIFIED |
| File assignment matrix | binary file-to-node assignment | 0/1 matrix | source definition | dynamic | YES — SOURCE SPECIFIED |
| Failure probability of each node | node reliability parameter | probability | source definition | static/dynamic | YES — SOURCE SPECIFIED |
| Transfer rate | data transfer rate of each node | MB/s | source definition | static/dynamic | YES — SOURCE SPECIFIED |
| Capacity of each node | storage capacity | GB | source definition | static | YES — SOURCE SPECIFIED |
| Network speed | bandwidth / transmission capacity | Mbit/s | source definition | static/dynamic | YES — SOURCE SPECIFIED |
| Access rate $A(i,j)$ | file access rate | requests/time | source objective formulas | dynamic | YES — SOURCE SPECIFIED |
| File size $S_i$ | size | bytes/GB | source objective formulas | static | YES — SOURCE SPECIFIED |
| Service time | file service time | time units | source objective | dynamic | YES — SOURCE SPECIFIED |
| Load variance | variance of node load | scalar | source objective | dynamic | YES — SOURCE SPECIFIED |
| Energy consumption | system energy | energy units | source objective | dynamic | YES — SOURCE SPECIFIED |
| Latency | mean latency | time units | source objective | dynamic | YES — SOURCE SPECIFIED |

### 4.4 Outputs

- optimized replica-placement configuration
- final assignment matrix $\Psi_{ij}$
- best feasible replica set according to the objective function

### 4.5 State changes

- candidate placement matrix evolves over iterations
- selected nodes change as the solution improves
- final replica placement set is selected from the best optimization result
- no separate replica deletion policy is described

### 4.6 Mathematical formulation

#### 4.6.1 Binary assignment variable

The source defines the decision matrix:

$$
\Psi = (\Psi_{ij})
$$

with:

$$
\Psi_{ij} =
\begin{cases}
1 & \text{if file } F_i \text{ is assigned to data node } DN_j \\
0 & \text{otherwise}
\end{cases}
$$

This is explicit in the source and must be preserved.

#### 4.6.2 Mean file unavailability objective

The source defines the objective function as mean file unavailability and uses the product of failure probabilities across assigned data nodes.

This is explicit but the exact final formula is partially truncated in the excerpt.

UNRESOLVED — RESEARCHER DECISION: exact final formula from the original article must be extracted if implementation requires the full mathematical expression.

#### 4.6.3 Mean service time objective

The source gives:\n
$$
ST(i,j) = \Psi_{ij} \times \frac{S_i}{TR_j}
$$

and then aggregates across the access rate ratio. This is consistent with the material shown.

#### 4.6.4 Load variance objective

The source defines:

$$
L_{ij} = A_{ij} \times ST_{ij}
$$

and then computes node load and load variance.

This is explicit in the source excerpt.

#### 4.6.5 Energy objective

The source includes the total energy objective based on renewable and cooling energy terms.

This is explicit but the final exact equation is partially truncated in the excerpt.

UNRESOLVED — RESEARCHER DECISION: exact final energy equation must be extracted from the full paper.

#### 4.6.6 Mean latency objective

The source defines mean latency as a function of access rate and transfer capacity.

This is explicit in the source description, but the full equation is not completely visible in the summary.

UNRESOLVED — RESEARCHER DECISION: exact latency objective formula must be extracted from the original paper.

### 4.7 Optimization mechanism

The source explicitly defines OGSA as a hybrid of:
- oppositional-based learning (OBL)
- gravitational search algorithm (GSA)

The algorithm performs:
- initial population generation
- opposite solutions generation
- fitness evaluation
- mass and acceleration updates
- velocity and position updates
- termination on maximum iteration count
- best solution selected

This is explicit enough to implement as a source-defined optimization method if the full equations and objective function are available.

### 4.8 Objectives

The source states the objective function is composed of five single objectives:
- mean file unavailability
- mean service time
- load variance
- energy consumption
- mean latency

This is explicit and must not be replaced by the Proposed Method’s five objectives.

### 4.9 Constraints

- each file assignment must be binary
- node capacity must not be exceeded
- the solution should be feasible for the given storage and node resources
- final candidate solution selected after maximum iterations

This is partly explicit and partly implied by the optimization setup.

### 4.10 Triggering events

- cold start or initial optimization run
- periodic or event-based replica placement optimization
- population update based on fitness

The exact scheduling trigger is not detailed in the source excerpt.

### 4.11 Replica number

- not explicitly separated as a dynamic formula
- the optimization decides the placement arrangement, not a separate dynamic replica count

Status:
- NOT SPECIFIED IN SOURCE as a separate mechanism

### 4.12 Replacement / deletion

- NOT SPECIFIED IN SOURCE

### 4.13 Request processing

- source includes access rates, service time, and latency but no explicit per-request decision process when a file is requested

Status:
- NOT SPECIFIED IN SOURCE as an event-based request policy

### 4.14 Failure behavior

- failure probability is used in availability calculations, but there is no explicit failure-response algorithm in the source summary

Status:
- implied parameter usage only

### 4.15 Initial placement

- initial population is generated by random file assignment to data nodes

This is explicit source behavior.

### 4.16 Parameters

| Parameter | Meaning | Value from source | Unit | Default value | Source | Configurable? | Status |
|---|---|---|---|---|---|---|---|
| $\Psi_{ij}$ | binary assignment | 0/1 | binary | source-defined | source formula | NO | SOURCE SPECIFIED |
| $P_j$ | failure probability of node j | source-defined | probability | NOT SPECIFIED | source model | YES | RESEARCHER DECISION |
| $TR_j$ | transfer rate | source-defined | MB/s | NOT SPECIFIED | source formula | YES | RESEARCHER DECISION |
| $S_i$ | file size | source-defined | bytes/GB | NOT SPECIFIED | source formula | YES | RESEARCHER DECISION |
| population size | OGSA population size | source-defined conceptually | count | NOT SPECIFIED | source algorithm | YES | RESEARCHER DECISION |
| iterations | maximum iterations | source-defined | count | NOT SPECIFIED | source algorithm | YES | RESEARCHER DECISION |

### 4.17 Pseudocode

```text
Input: set of files F, data nodes DN, initial random assignment population

initialize population of candidate assignment matrices
calculate opposite solutions
repeat until termination condition is reached
    evaluate each solution using the multi-objective fitness function
    update mass, acceleration, velocity, and position according to GSA rules
    apply oppositional learning update
    select best solution candidate
end repeat
Output: best assignment matrix and replica placement set
```

This matches the explicit published behavior and does not add unsupported mechanisms.

### 4.18 Unit tests

- binary assignment matrix is valid
- node capacity constraint is respected
- best solution selected at termination
- objective function re-evaluates correctly on candidate solution
- population update preserves feasibility where possible

### 4.19 Integration tests

- OGSA executed in common simulator with identical topology, workload, and failures
- output placement set is recorded and evaluated consistently
- no unsupported request routing or replacement logic is added

### 4.20 Scientific limitations

- exact objective weighting and normalization are incomplete in the extracted source
- exact GSA update equations may need extraction from the full original paper
- no explicit replacement/deletion mechanism is defined
- no explicit request-handling logic is defined

### 4.21 Researcher decisions required

| Method | Decision required | Why required | Possible options | Recommended option | Impact on validity |
|---|---|---|---|---|---|
| OGSA | exact objective weighting and normalization | incomplete in source excerpt | exact paper values or explicit researcher specification | exact paper first | critical |
| OGSA | exact GSA update formulas | may be truncated in extracted summary | original paper extraction | exact paper extraction | critical |
| OGSA | exact population and termination parameters | source summary is conceptual | explicit researcher-defined values | researcher-defined with full documentation | important |

---

## 5. Final comparison matrix

| Capability | Proposed | HRS | DPRS | EIMORM | OGSA |
|---|---|---|---|---|---|
| Replica selection | YES — SOURCE SPECIFIED | YES — SOURCE SPECIFIED | NO — SOURCE SPECIFIED | YES — SOURCE SPECIFIED | NO — SOURCE SPECIFIED |
| Replica placement | YES — SOURCE SPECIFIED | YES — SOURCE SPECIFIED | YES — SOURCE SPECIFIED | YES — SOURCE SPECIFIED | YES — SOURCE SPECIFIED |
| Dynamic replica count | YES — SOURCE SPECIFIED | NOT SPECIFIED IN SOURCE | NOT SPECIFIED IN SOURCE | YES — SOURCE SPECIFIED | NOT SPECIFIED IN SOURCE |
| Replica deletion | YES — SOURCE SPECIFIED (OIS-based, per proposal) | YES — SOURCE SPECIFIED (fuzzy deletion) | NOT SPECIFIED IN SOURCE | NOT SPECIFIED IN SOURCE | NOT SPECIFIED IN SOURCE |
| Replica replacement | YES — SOURCE SPECIFIED | NOT APPLICABLE as a separate formal mechanism beyond deletion | NOT SPECIFIED IN SOURCE | NOT SPECIFIED IN SOURCE | NOT SPECIFIED IN SOURCE |
| Optimization | YES — NSGA-III | NO — policy-based | YES — graph approximation/minimum spanning tree | YES — multi-objective optimization described | YES — OGSA optimization |
| Multi-objective optimization | YES — SOURCE SPECIFIED | NO | NO | YES — SOURCE SPECIFIED | YES — SOURCE SPECIFIED |
| Failure-specific mechanism | NOT SPECIFIED IN SOURCE as algorithmic behavior | NOT SPECIFIED IN SOURCE | NOT SPECIFIED IN SOURCE | IMPLIED by availability model, not a dedicated mechanism | IMPLIED by failure probability model, not a dedicated mechanism |
| Request-triggered execution | YES — SOURCE SPECIFIED | YES — SOURCE SPECIFIED | PARTIALLY IMPLIED in response-time model | PARTIALLY IMPLIED | NOT SPECIFIED IN SOURCE |
| Periodic execution | YES — SOURCE SPECIFIED | NOT EXPLICITLY SPECIFIED | PARTIALLY IMPLIED by graph construction | PARTIALLY IMPLIED | YES — SOURCE SPECIFIED (population iteration) |

---

## 6. Contract consistency check

### 6.1 Consistency with the Proposed Method contract

The baseline methods are intentionally not forced into the Proposed Method pipeline. Each one retains its own documented scientific boundary.

Consistent points:
- Proposed Method uses OIS and NSGA-III, which are not copied into baselines.
- HRS keeps its merit-based placement and fuzzy deletion logic.
- DPRS keeps its placement-oriented graph / response-time model.
- EIMORM keeps replica-factor / cost / availability logic.
- OGSA keeps assignment-matrix / OGSA optimization logic.

Potential inconsistencies to watch:
- if the common simulator demands identical event triggers for all algorithms, the researcher must remember that source-defined triggers differ across methods; a common event engine is infrastructure, not algorithm behavior.
- the common simulator may need a default request scheduler, but this must be treated as simulator infrastructure and not as an invented baseline mechanism.

### 6.2 Missing information across the source files

The following items remain unresolved in the source material and must not be silently filled:

- HRS fuzzy membership functions and exact rule set
- HRS exact replica selection cost formula
- DPRS exact response-time threshold and objective formalization
- EIMORM exact replica-factor formula and objective weights
- OGSA exact objective weighting / normalization and GSA equations
- all algorithms lack a single fixed common failure-response mechanism at the algorithm level

This is acceptable only if the project explicitly labels them as:

UNRESOLVED — RESEARCHER DECISION

### 6.3 Scientific boundary preserved

This document intentionally preserves the distinction between:
- algorithm-specific scientific behavior
- common simulation infrastructure
- researcher-defined design choices

This is the correct implementation boundary for a fair PhD simulation study.

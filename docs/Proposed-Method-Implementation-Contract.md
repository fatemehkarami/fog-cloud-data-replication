# Proposed Method Implementation Contract

## 1. Purpose and scope

This document defines the implementation contract for the Proposed Method only. It formalizes the scientific pipeline below:

Request
→ OIS-based replica selection
→ Dynamic replica-number determination
→ NSGA-III replica placement
→ OIS-based replica replacement/deletion
→ Metrics update

This contract is intentionally strict: it does not invent missing scientific mechanisms. Any definition that is not explicitly stated or directly derivable from the project specification is marked as:

RESEARCHER-REQUIRED

This contract does not add reliability or availability as optimization objectives for the NSGA-III placement stage. Reliability and availability remain evaluation metrics only.

## 1A. Phase 11 execution decisions

The following fixed decisions make the normal Proposed adapter path executable. They are researcher-decided interpretations where the source is silent; they do not change the common environment, common metrics, or other methods.

| ID | Decision | Source-supported? | Researcher choice | Why needed |
|---|---|---|---|---|
| P-EXEC-001 | Access-event value `v_j` | No; the source leaves it open | `v_j = 1.0` for every raw read event | Makes access decay deterministic without weighting requests by method output. |
| P-EXEC-002 | Access decay | Exponential form is source-defined | `lambda = 0.0001 s^-1`; elapsed time is non-negative seconds | Supplies one fixed time-aware decay parameter. |
| P-EXEC-003 | OIS weights | Formula is source-defined; values are not | Equal weights `(0.2, 0.2, 0.2, 0.2, 0.2)` | Avoids privileging one OIS component without evidence. |
| P-EXEC-004 | Replication-frequency weight | Concept is source-defined; time rule is not | `replication_weight = 1.0` | Keeps the source RF component executable without importing another policy. |
| P-EXEC-005 | File-type priority | Component is source-defined; CMP-RD-002 has no semantic file types | `T_i = 1.0` for the frozen common catalog | Avoids inventing categories in the common dataset. |
| P-EXEC-006 | OIS component normalization | Required conceptually, exact bounds are not fixed | Use deterministic per-decision-set min/max for internal OIS components; a zero range maps to `0.0` | Prevents unit dominance inside OIS without using final experiment results. |
| P-EXEC-007 | Invocation/timing | Dynamic request-driven behavior is source-compatible; exact trigger is not fixed | Invoke on every admitted read request; replicate only when OIS is computed and the count stage requests additional replicas | Supplies a deterministic trigger without making every request a replication action. |
| P-EXEC-008 | Replica count | `ceil(WA/Rj-max) - Nc` is source-defined | Use supplied weighted access rate, fixed `Rj_max` request input, and current valid replica count; negative delta deletes at most one eligible non-primary replica per decision | Preserves the source branch structure with a bounded executable mutation. |
| P-EXEC-009 | NSGA-III population/generations | Algorithm family is source-defined; values are not | Population `12`, generations `5`, deterministic five unit reference directions | Fixed, small, reproducible configuration for the 12-node environment. |
| P-EXEC-010 | Initialization/variation/selection | Exact operators are not specified | Stable node-ID initialization; nondominated sorting; normalized reference-direction association; lexical tie-break; no stochastic crossover/mutation unless an injected Proposed stream is supplied | Keeps the implementation recognizably NSGA-III without inventing uncontrolled randomness. |
| P-EXEC-011 | Internal objectives | Objective names/directions are source-defined; complete formulas are not | Use common-state-compatible load, capacity cost, and degree-centrality proxies isolated inside Proposed; unsupported energy/response inputs use the same deterministic proxy vector | Makes candidate comparison executable without altering CMP-RD-007 metrics. |
| P-EXEC-012 | Placement/feasibility | Valid placement and capacity constraints are common requirements | Candidate nodes must be healthy, reachable, non-duplicate, and capacity-valid; return a common `PLACEMENT` decision | Produces a validated decision without mutating common state in the adapter. |
| P-EXEC-013 | Replacement | OIS-based replacement is source-conceptual; ranking is incomplete | Delete the lexically greatest eligible non-primary valid replica when count reduction is requested; preserve the last valid replica | Provides deterministic storage-pressure behavior without importing HRS fuzzy replacement. |
| P-EXEC-014 | Request failure | Common metrics define unsuccessful access but no deadline/retry | No deadline or retry is added; unavailable service returns an unresolved/unsuccessful common outcome when request execution is implemented | Avoids inventing request semantics. |

P-EXEC-011's proxy values are internal Proposed decision inputs, not common evaluation measurements and not claims that the source formulas are complete. All values are fixed before execution and must not be tuned from results.

---

## 2. Method definition boundary

The Proposed Method is a dynamic data replication strategy with the following components:

1. Replica selection based on Overall Importance Score (OIS)
2. Dynamic replica-number determination and dynamic replication timing
3. Replica placement by NSGA-III multi-objective optimization
4. Replica replacement/deletion based on OIS

The implementation must preserve this sequence for every file and request-driven decision event.

---

## 3. General execution pipeline

### 3.1 Pipeline definition

The algorithm operates in the following order for each decision cycle:

1. Request arrives
2. Check if the requested file is available on a valid healthy node
3. If not available or if replica policy requires adaptation, compute OIS for the file
4. Determine dynamic replica number requirement
5. If replica creation is required, perform NSGA-III placement optimization
6. If replica count is excessive, identify low-value eligible replicas for deletion
7. Update file, node, and replica state
8. Update simulation metrics

### 3.2 Mandatory invariants

The implementation must enforce the following invariants at all times:

- Every file must always have at least one valid replica.
- A file cannot be stored as valid on a failed node.
- A valid replica must be reachable through the simulation network model.
- The last valid replica of a file must never be deleted.
- A replica decision must respect storage capacity and node health.
- Only the replication decision mechanism differs across algorithms; all other environment state remains common.

---

## 4. Stage 1 — Request handling

### 4.1 Inputs

- Request event
- File identifier requested by the user
- Source node / requester location
- Simulation time
- Current replica state of the file
- Current node health state
- Current storage availability
- Current network state

### 4.2 Outputs

- Request outcome: success or failure
- Trigger status for replica policy re-evaluation
- File availability status
- Replica selection candidate set, if needed

### 4.3 State changes

- Update request history
- Update file access history
- Update file access counters and time stamps
- Update request success/failure counters
- If a missing-file condition is detected, expose the condition for the unresolved replication-policy evaluation; do not treat it as an automatic replication trigger

### 4.4 Mathematical formulas

No new formula is required beyond the simulation request-processing rule and file availability checks.

Request success condition:

A request-service outcome requires a valid and reachable replica on a healthy node. Whether completion within a deadline or response-time condition changes the success classification is RESEARCHER-REQUIRED and remains unresolved.

This is a simulation-level service evaluation boundary, not an optimization objective. The contract does not define a deadline value, timeout threshold, or request-failure trigger.

### 4.5 Parameters

- Request arrival rate
- File request type
- Request deadline or response-time threshold — RESEARCHER-REQUIRED
- Source node and file ID
- Current node health status

### 4.6 Constraints

- A request cannot be completed from an invalid or failed replica.
- A request cannot complete if no valid replica remains available.
- Request results must be recorded even if the file is unavailable.

### 4.7 Triggering events

- Request arrival
- Request completion
- File unavailability detected
- Replica set changes

### 4.8 Expected algorithm behavior

- A request is served only from a valid replica.
- If the required file is unavailable, the request outcome is recorded, but the success/failure classification and any replication-policy trigger are RESEARCHER-REQUIRED and unresolved.
- The algorithm does not silently create a replica without evaluating the policy state.

### 4.9 Failure behavior

- If the file is unavailable, the system records the failed request and continues the simulation.
- If a node is unhealthy, availability and service outcome are recorded; whether the request is classified as failed, redirected, or used to trigger replication is RESEARCHER-REQUIRED and unresolved.

### 4.10 Required unit tests

- Request from a healthy valid replica succeeds.
- Request from a failed node fails.
- Request for a file with no valid replica fails and triggers policy evaluation.
- Request history is updated correctly.
- A success/failure record is created for every request.

---

## 5. Stage 2 — OIS-based replica selection

### 5.1 Definition

Replica selection uses the Overall Importance Score (OIS) for each file.

The method must use the following formula:

$$
OIS_i = w_1 \cdot AF_i + w_2 \cdot FS_i + w_3 \cdot RF_i + w_4 \cdot T_i + w_5 \cdot UC_i
$$

with configurable weights and normalized components.

### 5.2 Inputs

- File metadata
- Access history for the file
- File size
- Replication frequency metrics
- File type
- Number of users accessing the file
- Current time
- Weight configuration
- Normalization policy

### 5.3 Outputs

- OIS for the file
- File importance ranking relative to other files in the decision set
- Candidate file selection for replication evaluation

### 5.4 State changes

- Update the file importance value
- Update file access history and popularity summaries
- Mark the file as candidate for replication if policy thresholding requires it

### 5.5 Mathematical formulas

#### 5.5.1 Access frequency

The project specification states:

For access event j:

$$
weight_j = e^{-\lambda t_j}
$$

where:
- $t_j$ = time difference between current time and access-event timestamp
- $\lambda$ = exponential decay parameter

Weighted access frequency:

$$
AF_i = \frac{\sum_j(weight_j \cdot v_j)}{\sum_j(weight_j)}
$$

where $v_j$ is the value/frequency associated with access event $j$.

RESEARCHER-REQUIRED: exact access-event modeling and the definition of $v_j$ must be fixed by the researcher if not already defined elsewhere in the project specification.

#### 5.5.2 File-size score

$$
FS_i = \log(S_i)
$$

where $S_i$ is file size.

#### 5.5.3 Replication-frequency score

$$
RF_i = N_{rf_i} \cdot w_i
$$

where:
- $N_{rf_i}$ = number of times file $f_i$ has required replication
- $w_i$ = time-based weighting factor

RESEARCHER-REQUIRED: exact definition of $w_i$ and its time dependency must be specified by the researcher if not already provided elsewhere.

#### 5.5.4 File type importance

$$
T_i
$$

This is the file-type importance value. The project requires that file types be configurable and that the simulator must not arbitrarily assign type priorities.

RESEARCHER-REQUIRED: the exact priority mapping for each file type must be specified by the researcher.

#### 5.5.5 User count

$$
UC_i
$$

This is the number of users accessing the file.

### 5.6 Parameters

- $w_1, w_2, w_3, w_4, w_5$
- $\lambda$
- file-type importance table
- file-size normalization rule
- replica-frequency weighting rule
- access-event weighting rule

### 5.7 Constraints

- OIS must be computed for files under evaluation only.
- Normalization must be applied consistently across all files in a decision epoch.
- OIS must not be computed using unavailable or invalid file metadata.
- A file with no valid replica cannot be treated as eligible for deletion based solely on OIS if it is the only valid replica.

### 5.8 Triggering events

- Request failure due to file unavailability
- Periodic replication policy evaluation
- Node recovery event affecting file reachability
- Significant change in access frequency or request volume

### 5.9 Expected algorithm behavior

- Files with higher OIS are more likely to be selected for replication support.
- OIS is used as the importance signal for replication decisions.
- The ranking must be consistent and reproducible for the same simulation state and seed.

### 5.10 Failure behavior

- If file metadata is incomplete, OIS cannot be computed and the file is excluded from automatic candidate selection.
- If a file has no valid replica, the request fails and the system records the missing-data condition.
- OIS cannot be used to justify deleting the last valid replica.

### 5.11 Required unit tests

- OIS is computed correctly for a known file with a known access history.
- Weight normalization is applied consistently.
- File type priority is loaded from configuration exactly once and not silently assigned.
- OIS for a hot file is greater than OIS for a cold file under the same environment.
- Files with no valid metadata cannot compute OIS.
- A file with only one valid replica is never considered eligible for OIS-based deletion.

---

## 6. Stage 3 — Dynamic replica-number determination

### 6.1 Definition

The dynamic replica-number estimation is:

$$
N_n = \lceil WA / R_{j\_max} \rceil - N_c
$$

where:
- $WA$ = weighted access rate
- $R_{j\_max}$ = maximum request-processing rate considered for the node
- $N_c$ = current number of replicas

Decision rule:

- $N_n > 0$ → create replicas
- $N_n = 0$ → no replication action
- $N_n < 0$ → identify unnecessary replicas for deletion

### 6.2 Inputs

- File OIS value
- File access rate and weighted access rate
- Current number of replicas $N_c$
- Maximum request-processing rate $R_{j\_max}$
- Current node state and file state
- Storage availability

### 6.3 Outputs

- Replica-create decision count
- Replica-delete decision list
- No-action decision

### 6.4 State changes

- Increase or decrease replica count on the candidate file
- Update replicas list
- Update file metadata
- Update storage usage and node capacity records

### 6.5 Mathematical formulas

The documented formula is explicit and must be used as-is.

$$
N_n = \left\lceil \frac{WA}{R_{j\_max}} \right\rceil - N_c
$$

### 6.6 Parameters

- $WA$
- $R_{j\_max}$
- $N_c$
- current node request-processing capacity

RESEARCHER-REQUIRED: exact definition of $WA$ and the calculation of $R_{j\_max}$ for heterogeneous nodes must be finalized by the researcher.

### 6.7 Constraints

- The computed replica count must not result in fewer than one valid replica for any file.
- The decision must respect storage capacity.
- The node health state must be valid before a replica is created.
- Replica creation and deletion decisions must be applied sequentially and atomically.

### 6.8 Triggering events

- Request rate increases significantly
- File importance changes from access history
- Storage state changes due to file growth or deletion
- Periodic policy evaluation timer

### 6.9 Expected algorithm behavior

- A hot or highly important file may require more replicas.
- A file with a stable or low access pattern may keep or reduce its replica count.
- The algorithm reacts dynamically over time rather than using a static fixed replica count.

### 6.10 Failure behavior

- If no valid target node is available for creation, the decision is recorded as deferred and no invalid replica is created.
- If there is insufficient storage on all candidate nodes, the replica creation request is rejected and logged.
- If $N_n < 0$ but all replicas are already necessary or there is only one valid replica, the algorithm must not delete the last valid replica.

### 6.11 Required unit tests

- $N_n > 0$ produces a create decision.
- $N_n = 0$ produces no action.
- $N_n < 0$ produces a deletion candidate list.
- A file with one valid replica is never reduced below one valid replica.
- Storage-capacity rejection is logged correctly.
- The formula is reproducible across repeated evaluations.

---

## 7. Stage 4 — NSGA-III replica placement

### 7.1 Definition

Replica placement uses NSGA-III to optimize a five-objective placement problem. The objective vector is:

1. Minimize energy consumption
2. Minimize response time
3. Minimize data-node load
4. Minimize total cost
5. Maximize closeness centrality

Reliability and availability are excluded from the NSGA-III objective vector and are retained as evaluation metrics only.

### 7.2 Decision variable

The decision variable is binary:

$$
\psi(i,j) \in \{0,1\}
$$

where:
- $\psi(i,j)=1$ if file $f_i$ is placed on node $D_j$
- $\psi(i,j)=0$ otherwise

### 7.3 Inputs

- Candidate file to replicate
- Current set of candidate nodes
- Node capacities
- File size
- Network topology and link attributes
- Node health state
- Current load and energy state
- Current response-time estimates
- Current storage state and replica set
- NSGA-III parameters

### 7.4 Outputs

- Placement configuration for the file
- Selected nodes for new replicas
- Final replica creation list
- Feasible placement set satisfying capacity and health constraints

### 7.5 State changes

- Add new valid replicas to selected nodes
- Update storage usage
- Update file replica records
- Update node network and resource counters
- Update energy, cost, response-time, and load estimates after placement

### 7.6 Mathematical formulas

#### 7.6.1 Energy consumption objective

The project specification provides the following:

For node $D_j$:

$$
ERE(j) = \sum_i [\psi(i,j) \cdot l(i,j) \cdot (P_{max}(j)-P_{idle}(j))] + P_{idle}(j)
$$

Total energy:

$$
ERE = \sum_j ERE(j)
$$

Cooling energy:

$$
Q = \frac{1}{T_{out}/T_{in} - 1}
$$

$$
ECE(j)=\frac{ERE(j)}{Q}
$$

$$
ECE = \sum_j ECE(j)
$$

Total system energy:

$$
E(system)=ERE + ECE
$$

Objective:

Minimize $E(system)$

RESEARCHER-REQUIRED: exact definition of $l(i,j)$, $P_{max}(j)$, $P_{idle}(j)$, $T_{out}$, and $T_{in}$ is required before implementation.

#### 7.6.2 Response-time objective

The project requires response time to be minimized, but the exact method-specific formula is not fully specified in the current method contract.

RESEARCHER-REQUIRED: exact response-time formulation for the NSGA-III objective must be finalized by the researcher.

#### 7.6.3 Data-node load objective

The project requires the load objective to be minimized, but the exact load formulation is not fully specified in the current method contract.

RESEARCHER-REQUIRED: exact load formulation used in the placement objective must be finalized by the researcher.

#### 7.6.4 Total cost objective

The project requires cost minimization, but no exact cost function is specified in the proposal excerpt beyond general references to data transfer and storage cost.

RESEARCHER-REQUIRED: exact cost model must be finalized by the researcher.

#### 7.6.5 Closeness-centrality objective

The method specifies that centrality should be maximized, but the precise formula and normalization are not fully specified in the current documentation.

RESEARCHER-REQUIRED: exact closeness-centrality definition, normalization, and direction must be finalized by the researcher.

### 7.7 Parameters

- NSGA-III population size
- number of reference points
- generations / stopping criterion
- crossover and mutation parameters
- objective weights, if any are used in the final formulation
- file candidate set
- candidate node pool

### 7.8 Constraints

- $\psi(i,j) \in \{0,1\}$
- node must be healthy
- node must have enough free storage
- no invalid or failed node may host a replica
- every file must retain at least one valid replica after placement
- the placement decision must respect capacity and node-health constraints

### 7.9 Triggering events

- file requires additional replica
- file is selected by OIS and dynamic replica-number rule
- node capacity changes after recovery or replica deletion
- periodic optimization event

### 7.10 Expected algorithm behavior

- The optimizer searches for a feasible location set for the target file.
- Placement is decided by the five objectives only.
- Reliability and availability are not used as additional objectives in NSGA-III.
- The chosen solution must be feasible and reproducible for a fixed seed.

### 7.11 Failure behavior

- Failed nodes are excluded from the candidate set.
- Any placement that violates node health is discarded.
- If no feasible placement exists, the decision is recorded as deferred and the system retains the last valid replica set until a future eligible condition appears.

### 7.12 Required unit tests

- Candidate placement excludes failed nodes.
- A placement solution respects storage capacity.
- All $psi(i,j)$ values are binary.
- Final file has at least one valid replica after NSGA-III placement.
- Optimization result is reproducible under a fixed seed.
- Objective values update after each placement iteration.
- Reliability and availability are not included as additional NSGA-III objectives.

---

## 8. Stage 5 — OIS-based replica replacement and deletion

### 8.1 Definition

Replica replacement is OIS-based. The lowest-value eligible replicas are deletion candidates. The last valid replica of a file must never be deleted.

This is the required scientific boundary for this implementation contract.

### 8.2 Inputs

- Current replica list for a file
- Validity and health of each replica
- File OIS values
- Current access counts and access timestamps
- Storage pressure and capacity constraints
- File-level replica count
- Node health state

### 8.3 Outputs

- Replica deletion candidate list
- Replica retention list
- Final deletion authorization list
- Final post-deletion file replica state

### 8.4 State changes

- Remove low-value replicas from eligible set
- Keep the highest-value replicas according to OIS-driven replacement behavior
- Update file replica count
- Update node storage usage
- Update file access metadata and replica history

### 8.5 Mathematical formulas

There is no explicit numeric deletion-score formula in the project specification beyond the OIS-based replacement requirement.

Therefore:

- the replacement decision must rank eligible replicas by their replica value as determined by OIS relevance and/or access history, but
- the numerical formula for the replacement score is not specified in the project contract.

RESEARCHER-REQUIRED: exact value function used to rank duplicate or low-priority replicas under the OIS-based replacement policy must be defined by the researcher.

### 8.6 Eligibility rule

A replica is eligible for deletion only if:

- the replica is valid,
- the node is healthy,
- the replica is not the only valid replica for the file,
- the file retains at least one valid replica after deletion,
- deleting the replica does not violate the file-level minimum-replica invariant.

### 8.7 Constraints

- The last valid replica must never be deleted.
- Deletion decisions must respect node health and file availability.
- Deletion decisions must not create file unavailability beyond the intended policy behavior.
- A replacement decision cannot delete a replica on a failed node unless the node is already marked invalid by failure handling.

### 8.8 Triggering events

- $N_n < 0$
- storage pressure on target node
- file-level replica count exceeds required count
- periodic cleanup event

### 8.9 Expected algorithm behavior

- Lowest-value eligible replicas are the most likely to be deleted.
- OIS-based deletion must prioritize low-value replicas only when the file still retains at least one valid replica.
- The algorithm does not allow the final valid replica to disappear.

### 8.10 Failure behavior

- If all replicas are invalid or all candidate nodes are unhealthy, the deletion decision is skipped and reported as blocked.
- Failed nodes are not considered for retention unless they remain valid before failure handling updates.

### 8.11 Required unit tests

- The last valid replica is never deleted.
- A failed replica is not retained as valid.
- Deletion is blocked when only one valid replica remains.
- Lowest-value eligible replica is selected before higher-value replicas.
- Deletion decision is recorded correctly in the file and node state.
- Storage usage is updated after a delete operation.

---

## 9. Stage 6 — Metrics update

### 9.1 Definition

After every accepted replication decision and every request outcome, the simulator updates the metric state.

### 9.2 Inputs

- File and replica state
- Request outcomes
- Node health state
- Node and network load state
- Energy and cost state
- Availability and reliability counter state

### 9.3 Outputs

- Updated energy metrics
- Updated response-time metrics
- Updated data-node load metrics
- Updated total cost metrics
- Updated centrality calculations
- Updated availability and reliability counters
- Updated replica counts and event logs

### 9.4 State changes

- Increment or decrement replica counters
- Update node load and memory usage
- Update energy usage counters
- Update file-level availability time windows
- Update successful and failed request counts
- Update network and storage cost accumulators

### 9.5 Mathematical formulas

#### 9.5.1 Availability (time-based)

The project specification requires time-based availability:

$$
Availability_f = \frac{\text{Time during which at least one valid replica is available}}{\text{Total simulation time}}
$$

System-level availability:

$$
Availability_{system} = \frac{1}{N_f} \sum_{f=1}^{N_f} Availability_f
$$

#### 9.5.2 Reliability (request-based)

The project specification requires:

$$
Reliability = \frac{\text{Number of successfully completed data access requests}}{\text{Total data access requests}}
$$

This is an evaluation metric only and not a NSGA-III objective.

#### 9.5.3 Response time

$$
\overline{T}_{resp} = \frac{1}{N_{req}} \sum_{r=1}^{N_{req}} T_r
$$

#### 9.5.4 Energy

The project requires energy consumption to be tracked, but the exact method-level calculation is not fully specified in the current contract unless the energy model is finalized.

RESEARCHER-REQUIRED: exact energy model to be used during metric updates must be finalized by the researcher.

### 9.6 Parameters

- simulation time
- metric aggregation window
- file availability history
- request counters
- node energy counters
- network transfer counters
- storage cost terms

### 9.7 Constraints

- Reliability and availability are never optimization targets for NSGA-III.
- Metrics must be updated after every request and replication decision.
- All five methods must use the same metric formulas for fairness.
- Metric calculations must not depend on algorithm-specific hidden state.

### 9.8 Triggering events

- request completion
- replica creation/deletion
- node failure/recovery
- periodic metric flush
- simulation end

### 9.9 Expected algorithm behavior

- Metrics reflect the actual simulation state.
- The evaluation logic is common across all algorithms.
- The algorithm does not modify evaluation metrics beyond the allowed event model.

### 9.10 Failure behavior

- Failed requests are counted and included in reliability calculations.
- File unavailability periods are included in availability calculations.
- A failed node can temporarily reduce availability but must not cause silent metric corruption.

### 9.11 Required unit tests

- Successful request increments reliability numerator.
- Failed request increments reliability denominator only.
- Availability is updated correctly when a file becomes unavailable.
- Replica count metrics reflect creation and deletion events.
- Energy, cost, and load values update after a replica action.
- Final metric summary matches aggregated event data.

---

## 10. Formal algorithm contract summary

### 10.1 Stage sequence

Request
→ OIS-based replica selection
→ Dynamic replica-number determination
→ NSGA-III replica placement
→ OIS-based replica replacement/deletion
→ Metrics update

### 10.2 Data flow contract

For each file under decision:

1. compute OIS
2. determine replica count delta via $N_n$
3. if $N_n > 0$, perform candidate placement with NSGA-III
4. if $N_n < 0$, identify unnecessary eligible replicas for deletion using OIS-based ranking
5. if $N_n = 0$, no action
6. update metrics and simulation state

### 10.3 Invariants

- no file has zero valid replicas
- last valid replica is protected
- NSGA-III objective set stays fixed to five placement objectives only
- reliability and availability are evaluation metrics only
- no extra objective functions are added

---

## 11. Required configuration parameters

This section lists the parameters that must be configurable and documented before implementation begins.

### 11.1 OIS parameters

- $w_1$
- $w_2$
- $w_3$
- $w_4$
- $w_5$
- $\lambda$
- file-type priority table
- access-event weighting rule
- file-size normalization rule
- replica-frequency weighting rule

### 11.2 Dynamic replica-number parameters

- $WA$
- $R_{j\_max}$
- $N_c$
- file-specific weighted access profile
- candidate node processing capacity

RESEARCHER-REQUIRED: exact formulas for $WA$ and $R_{j\_max}$ and their time dependence must be finalized.

### 11.3 NSGA-III placement parameters

- population size
- number of reference points
- stopping criterion
- objective normalization policy
- terminal evaluation and sorting policy
- candidate-node pool definition
- maximum placement iterations

RESEARCHER-REQUIRED: objective normalization scheme must be finalized before implementation.

### 11.4 OIS-based replacement parameters

- replacement trigger threshold
- eligible-replica ranking rule
- minimum replica count per file
- deletion priority ordering

RESEARCHER-REQUIRED: exact deletion priority function and ranking rule must be finalized.

### 11.5 Simulation parameters

- simulation duration
- random seed list
- failure schedule generation parameters
- request workload generation parameters
- node capacity parameters
- network topology parameters
- storage threshold policy

---

## 12. A. Implementation-ready items

The following items are implementation-ready based on the current contract and project specification:

- The pipeline sequence is fixed.
- The OIS formula is fixed.
- The dynamic replica-number formula is fixed.
- The NSGA-III decision variable is fixed.
- The five placement objectives are fixed.
- Reliability and availability are evaluation metrics only.
- Every file must retain at least one valid replica.
- The last valid replica cannot be deleted.
- Failed nodes are excluded from replica placement.
- Replica decisions must respect storage capacity and node health.
- All metric updates occur after request and replication events.

---

## 13. B. Remaining ambiguities

These items remain intentionally unresolved and must be treated as explicit researcher decisions:

1. Exact computation of weighted access rate $WA$
2. Exact computation of maximum request-processing rate $R_{j\_max}$
3. Exact access-event value definition $v_j$
4. Exact time-based weighting $w_i$ in the replication-frequency component
5. Exact file-type priority mapping $T_i$
6. Exact objective normalizations for energy, response time, load, cost, and centrality
7. Exact response-time objective formula
8. Exact load model and data-node load formula
9. Exact total-cost formula
10. Exact closeness-centrality definition and normalization
11. Exact OIS replacement-value function
12. Exact deletion ranking rule among eligible replicas
13. Exact simulation-level network cost model
14. Exact node energy model constants and facility cooling parameters
15. Exact deadline policy for request success/failure

All of the above are explicitly flagged as:

RESEARCHER-REQUIRED

---

## 14. C. Required unit and integration tests

### 14.1 Unit tests

- Request handling: file unavailable triggers fail + policy evaluation.
- OIS computation: exact expected result for a simple known access history.
- Dynamic replica-number rule: create branch, no-op branch, delete branch.
- OIS-based selection: file with higher OIS is selected over lower importance when both are candidates.
- Replica count invariant: no file with one valid replica may be deleted.
- Placement eligibility: failed nodes are excluded.
- Placement binary constraint: $psi(i,j)$ is binary.
- Storage constraint: created replica never exceeds node capacity.
- Replacement: lowest-value eligible replica is chosen for deletion.
- Metrics update: request success/failure affects reliability, availability, and replica counters correctly.

### 14.2 Integration tests

- End-to-end request processing with a hot file produces expected replica adaptation.
- End-to-end request outcome with a missing valid replica records the unresolved service/failure policy without assuming that failure itself triggers OIS or dynamic replica-count logic.
- End-to-end request when the file is available but the node fails triggers fallback or failure handling without violating invariants.
- End-to-end placement when storage is insufficient blocks the placement decision.
- End-to-end deletion when storage is full removes only eligible replicas.
- End-to-end metrics update across a multi-file scenario matches expected totals.

### 14.3 Regression tests

- Same seed, same configuration, same request stream → same replica decisions and metric outputs.
- Different seeds produce different random runs but consistent statistical outputs.
- Changing a single weight in the configuration changes the OIS ranking only where intended.

---

## 15. D. Scientific assumptions that must be documented in the thesis

The thesis must explicitly document the following assumptions, even if they are researcher-defined simulation choices:

1. OIS component normalization policy
2. File-type importance mapping
3. Access-event value definition and decay policy
4. Definition of weighted access rate $WA$
5. Definition of maximum request-processing rate $R_{j\_max}$
6. Storage-capacity enforcement rule and capacity accounting method
7. Node health rule for placement and request execution
8. Availability aggregation rule across files
9. Reliability definition and request-success criteria
10. Response-time thresholding or deadline policy
11. Energy model constants used in the simulator
12. Cost model components and units
13. Closeness-centrality normalization method
14. Load definition used in the placement objective
15. The decision to exclude reliability and availability from NSGA-III objectives
16. The decision to keep all algorithms in the same environment and to disable unsupported algorithm-specific mechanisms

These must be documented as assumptions, not silently embedded as numerical defaults.

---

## 16. E. Final scientific boundary

This implementation contract intentionally does not add any additional optimization objective, weight, or replication rule beyond the explicit method definition. Reliability and availability remain evaluation metrics only.

The contract is therefore implementation-safe for the initial research version but still includes scientifically unresolved items that must be resolved by the researcher before numerical implementation can be finalized.

---

## 17. Final summary

The Proposed Method is implementation-ready at the pipeline level, but it is not implementation-final until the researcher resolves the unresolved definitions listed in this contract. The project must not silently fill these gaps with arbitrary values.

The implementation contract is therefore a formal specification boundary: it defines what is required, what is explicitly allowed, and what still requires a researcher decision before coding can begin.

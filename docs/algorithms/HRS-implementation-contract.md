# HRS implementation contract

## 1. Scope and source basis

This document is a software requirement contract derived only from the verified HRS specification in [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) and the original HRS paper. It is intentionally limited to the behavior explicitly supported by HRS and does not add new scientific logic.

This contract is structured into four clearly separated sections:

- A. Paper-defined behavior
- B. Required simulator integration behavior
- C. Unresolved scientific parameters
- D. Readiness and compliance

No HRS implementation code is specified here. This document defines the required software contract only.

## 1A. Phase 12 execution decisions

The following researcher-decided choices make the normal HRS path executable without changing the source-defined Merit, TotalCost, placement, provider-selection, or fuzzy-replacement concepts.

| Decision | Source support | Researcher decision | Reason |
|---|---|---|---|
| Merit weights W1/W2 | Formula is source-defined; final vector is ambiguous | Default `(0.5, 0.5)` when omitted; explicit complete weights remain accepted | Equal emphasis is deterministic and avoids privileging access or centrality. |
| TotalCost weights W3/W4/W5 | Formula is source-defined; final vector is ambiguous | Default `(1/3, 1/3, 1/3)` when omitted; explicit complete weights remain accepted | Equal emphasis across capability, load, and network-performance terms. |
| 1–10 normalization edges | Source defines the scale but not boundary ownership | Clamp to `[1,10]`; `max == min` maps to `5.5`; invalid reversed bounds remain unresolved | Deterministic handling without dropping boundary candidates. |
| Merit ties | Source does not define a tie rule | Lexically smallest stable site ID wins | Reproducible and method-local. |
| TotalCost ties | Source does not define a tie rule | Lexically smallest stable provider ID wins | Reproducible and method-local. |
| Fuzzy replacement | Membership/rules/inference are incomplete | Deterministic bounded proxy: 0.5 access value + 0.3 inverse cost value + 0.2 inverse recency value, with each non-negative input mapped by `x/(1+x)`; missing inputs map to zero contribution | Minimal executable HRS-specific policy; no fuzzy system is imported from another method. |
| Replacement transition | HRS may select multiple replicas; executor handles one deletion | Return the lowest-valued eligible replica as singular `replica_id`; expose remaining IDs for subsequent deterministic transitions; never select the sole/primary replica | Matches one-transition executor semantics and protects the last valid copy. |
| Site-to-node placement | HRS source selects a site; common runtime executes nodes | Select the stable site `data` node (`site-XX-data`), falling back to the lexically first node in that site | Consistent with CMP-RD-002's site roles and runtime placement contract. |
| Invocation | Source trigger is request-driven local absence | Evaluate HRS on each admitted read request; no additional failure-triggered invocation is added | Preserves the source request-triggered lifecycle. |
| Failure/recovery | No complete HRS recovery algorithm is source-defined | Use CMP-RD-005 external events; do not add automatic HRS repair or re-replication | Preserves the common failure boundary. |

These decisions are researcher interpretations, not claims that the HRS paper specifies the values or fuzzy proxy. They are fixed before execution and must not be tuned from results.

---

## A. Paper-defined behavior

### A.1 Algorithm identity

- Algorithm name: Hybrid Replication Strategy
- Source paper title: "A hybrid data replication strategy with fuzzy-based deletion for heterogeneous cloud data centers"
- Authors: N. Mansouri and M. M. Javidi
- Publication year: 2018
- Source acronym: HRS

### A.2 Trigger and lifecycle

Primary/source-defined replication trigger:

- "When a task needs the file, and it is not present in the local storage, replication takes place."

Required control flow:

1. Request for file
2. Check local availability
3. If file is absent:
   - select placement site
   - select replica provider
   - check whether the requested file replica already exists at the selected placement site
   - if the replica already exists at the selected placement site: do nothing
   - otherwise: check available storage at placement site
   - if sufficient storage: create replica
   - otherwise: perform fuzzy-based replacement, then create replica

Paper-defined phase intent:

- Placement: select the best site for storing a new replica to reduce access time.
- Selection: choose the best replica provider for the requesting entity based on VM capability, load, and network performance.
- Replacement: conditional execution only when storage is insufficient at the placement site; delete the lowest-value replicas so the new replica can be stored.

### A.3 Replica placement contract

#### A.3.1 Site centrality

Source-defined centrality concept:

- The relative importance of a site is determined by the centrality of a node in a graph.
- The paper selects closeness centrality for placement.
- The paper defines:

  Centrality(v) = (N - 1) / Σ_{a ≠ v} d(v,a)

  where:
  - N = total number of sites in the system
  - d(v,a) = distance between site v and site a

#### A.3.2 Number of accesses

- The placement decision includes the number of accesses to the file at the candidate site.
- The paper states that number of access is used together with centrality in placement because recently accessed files are likely to be accessed again.

#### A.3.3 Merit function

Paper-defined formula:

- Merit = W1 × NumberOfAccess + W2 × Centrality

Source status:

- The source defines the structure of the Merit formula.
- The source does not provide one unambiguous final weight vector that is authoritative for all execution contexts.
- The paper includes empirical/example weight values and a contradictory textual statement, which means the final W1/W2 assignment is not source-complete enough to be hardened as a project-wide mandatory implementation choice.

Contract requirement:

- The implementation contract must not silently select a final W1/W2 vector.
- Any final W1/W2 assignment must be classified as a researcher-required or source-clarified parameter before implementation is frozen.
- The contract must preserve the source ambiguity rather than repair it by choosing values.

#### A.3.4 HRS internal normalization vs common comparison normalization

The paper states that the scales of the factors differ and that a normalization step into a 1–10 scale is used before Merit is computed.

Required source-faithful distinction:

- HRS INTERNAL NORMALIZATION: the internal HRS placement stage references a factor scaling step before Merit.
- COMMON COMPARISON NORMALIZATION: any normalization used for cross-method comparison or common metrics belongs to the comparison/research layer and must not be embedded inside HRS.

Source status:

- The paper explicitly supports the concept of HRS internal normalization before Merit.
- The paper explicitly defines the uniform interval calculation: Inc. = (max - min) / 10.
- The paper explicitly defines the intended interval mapping from min through min + 10 x Inc. to normalized values 1 through 10.
- Exact boundary ownership when a value is exactly on an interval boundary, behavior when max equals min, and handling of values outside the observed min/max range remain unresolved.

Contract requirement:

- Implement HRS internal normalization according to the source-defined uniform 1-10 interval rule above.
- Do not invent min/max values, bounds, boundary conventions, or edge-case behavior.
- Keep HRS internal normalization separate from common comparison normalization.
- Common comparison normalization must not be implemented inside HRS.

#### A.3.5 Placement decision rule

- Compute the Merit score for each candidate site.
- Select the site with the highest Merit value.
- This site is the chosen placement site for the new replica.

The exact numerical coefficients used in Merit remain unresolved unless explicitly provided by the source or a later researcher decision; the implementation contract does not select or freeze them.

#### A.3.6 Initial primary-copy placement

- The source states that the primary copy of each data file is randomly placed in different sites at the beginning of the simulation.
- This is source-defined HRS simulation setup for initial primary-copy placement.
- HRS does not define a random seed policy, repetition count, or common random-scenario policy.
- Those experiment-level controls belong to the common simulator or researcher-decision layer and must not be invented here.

#### A.3.7 Placement tie handling

- The paper does not define an explicit tie-break rule.
- Therefore, for equal Merit values, the implementation must use a project-level deterministic policy only if such a policy is separately defined by the simulator or researcher.
- This deterministic policy is not part of the HRS scientific algorithm and must not be treated as source-defined HRS behavior.

### A.4 Replica selection contract

#### A.4.1 Required decision objective

The paper defines the provider-selection objective as minimizing TotalCost.

When the requested file is not available locally, HRS creates a list of candidate replica providers derived from sites/nodes that currently contain a replica of the requested file, and selects the provider with minimum TotalCost.

This candidate-provider list does not mean all VMs or all data nodes in the system; it is restricted to nodes/sites that already hold a replica of the requested file.

#### A.4.2 VM capability

Paper-defined VM capability formula:

- C = (n × alpha) + beta

where:
- n = number of processors
- alpha = CPU process capability (Mips)
- beta = communication bandwidth ability (Gbps)

#### A.4.3 VM load

Paper-defined load formula:

- L = Nt / Sr

where:
- Nt = total length of tasks in the service queue
- Sr = service rate

#### A.4.4 Network performance

Paper-defined network performance formula:

- N(a,b) = Bandwidth(a,b) / NetworkLatency(a,b)

where:
- Bandwidth(a,b) is measured in Mbits/s
- NetworkLatency(a,b) is measured in ms

#### A.4.5 TotalCost

Paper-defined formula:

- TotalCost = W3 × (1 / C) + W4 × L + W5 × (1 / N)

where:
- W3, W4, W5 = weight values for capability, load, and network performance

Source status:

- The paper states that the weights are adjustable and that equal weights are used in simulation examples.
- The source does not provide a single authoritative final vector for all execution contexts.
- The paper does not give a source-complete final executable value set for W3, W4, and W5 that can be treated as mandatory project policy.

Contract requirement:

- The implementation contract must not silently hard-code W3 = W4 = W5 = 1/3.
- The implementation contract must not convert the source's example or empirical wording into a mandatory final executable vector.
- Any final vector for W3, W4, W5 must be treated as a researcher-required selection or a source clarification before implementation is frozen.

#### A.4.6 Selection rule

- If the required file is not available in the local site, build the candidate replica-provider list from sites/nodes that currently contain a replica of the requested file.
- Compute TotalCost for each candidate provider.
- Select the candidate provider with minimum TotalCost.
- If the requested file replica already exists at the selected placement site, do not create another replica.

The exact final values of W3, W4, and W5 remain unresolved unless an authoritative source or explicit researcher decision is provided.

#### A.4.7 Selection tie handling

- The paper does not define a tie-break rule.
- Therefore, any equal TotalCost values require a project-level deterministic policy only if such a policy is separately defined by the simulator or researcher.
- This is not scientific HRS behavior; it is simulator policy.

### A.5 Replica replacement contract

#### A.5.1 Trigger condition

- Replica replacement is conditional and is triggered only when enough storage space is not available in the placement site for storing the new replica.
- Replacement is not a mandatory phase after every selection step.
- The correct source-faithful sequence is: file request -> local check -> placement -> provider selection -> check whether the requested replica already exists at the selected placement site -> if it exists: do nothing -> otherwise: storage check -> if storage is insufficient: conditional fuzzy replacement -> create replica.

#### A.5.2 Inputs used by replacement

The paper explicitly states that HRS uses three fuzzy inputs:

- Number of accesses
- Replication cost
- Last access time interval

The paper also states that the output is:

- Value of replica

#### A.5.3 Replication-cost formula

Paper-defined formula:

- Cost = Size / Bandwidth(x,y) + PropagationDelayTime(x,y)

where:
- Size = replica size
- Bandwidth(x,y) = bandwidth between provider site x and requester site y
- PropagationDelayTime(x,y) = time required to transfer the replica from provider x to requester y

Interpretation required by the paper:

- Larger replica size increases replication cost.
- Lower bandwidth increases replication cost.
- Greater propagation delay increases replication cost.

#### A.5.4 Fuzzy output and deletion rule

The paper states:

- The fuzzy system assigns a Value to each replica.
- The output range is [0,1].
- The source-defined input ranges are NumberOfAccesses 0 to 55, ReplicationCost 0 to 25, and LastAccessTimeInterval 0 to 12 x 10^5.
- These ranges do not define the missing membership-function breakpoints or rule semantics.
- A replica with the lowest value is an appropriate candidate for deletion.
- HRS computes the Value for all files in the target site.
- It sorts the list in ascending order of Value.
- It selects candidate files from the list until enough space is available.

Required deletion rule:

- Sort candidate replicas by ascending Value.
- Delete lowest-value replicas first.
- Stop deleting when sufficient free space exists for the new replica.

Fuzzy execution details not explicitly recoverable from the source remain unresolved. The implementation must not substitute common fuzzy-logic defaults or construct a synthetic complete rule base.

#### A.5.5 Storage constraint

- Replacement is required only when storage is insufficient.
- The paper does not define a separate storage policy beyond deleting enough low-value replicas to accommodate the new copy.

#### A.5.6 Replacement tie handling

- The paper does not define a tie-break rule for equal replica values.
- Therefore, equal Value values require a project-level deterministic policy.

---

## B. Required simulator integration behavior

This section defines the software-level behavior that must be present in the simulation environment, without modifying the scientific algorithm.

### B.1 Required input data

The simulator must provide the following values to HRS.

#### B.1.1 Site/network data

- Site identifiers
- Topology or distance matrix used to compute closeness centrality
- Distance between sites, d(v,a)
- Bandwidth between sites
- Network latency between sites
- Provider/requester site mapping

#### B.1.2 File and replica data

- File identifier
- File size
- Replica location set
- Number of accesses per file/site
- Last access time per replica
- Current storage usage at each site
- Available storage capacity at each site

#### B.1.3 VM data

- VM identifier
- Site hosting VM
- Number of processors n
- Alpha: CPU process capability (Mips)
- Beta: communication bandwidth ability (Gbps)
- Nt: total tasks in service queue
- Sr: service rate

#### B.1.4 Request/task data

- Task identifier
- Requesting site
- Requested file identifier
- Local file availability flag
- Submission time
- Completion/return time

### B.2 Required outputs

The simulation must produce the following derived outputs from the HRS algorithm:

- Selected placement site
- Selected provider site
- Replica placement decision
- Replica selection decision
- Deleted replicas during replacement
- Final storage state after replacement
- File/value ranking used during fuzzy replacement
- TotalCost per candidate provider
- Merit per candidate site
- Replica Value per candidate replica

### B.3 Preconditions

HRS must only execute when all of the following are true:

- a file request exists that requires replication because the file is not in local storage
- site-level distance or network topology data is available for centrality computation
- bandwidth and latency data are available for network-performance and replication-cost computations
- storage capacity data is available at the placement site
- VM capability, load, and network-data inputs are available for provider scoring
- the target replica list exists for the replacement phase if storage is insufficient
- the candidate replica-provider list is generated only from sites/nodes that currently contain a replica of the requested file
- the placement site is checked for whether the requested file replica already exists before any storage or replacement step

### B.4 Postconditions

After HRS execution:

- if a valid placement site exists, it is selected according to Merit
- if a valid candidate provider exists, it is selected according to minimum TotalCost
- if the requested file replica already exists at the selected placement site, no replica is created and no storage or replacement step is executed
- if the requested file replica does not exist at the selected placement site, then storage is checked
- if storage is insufficient at the placement site, low-value replicas are removed until enough space exists
- after each deletion, available storage is re-evaluated
- deletion stops as soon as sufficient storage is available for the new replica
- otherwise, no replacement is performed and the new replica is created directly when storage is sufficient
- the target replica is stored only after the placement and storage check have been satisfied

### B.5 Decision rules

#### B.5.1 Placement rule

- Compute the HRS placement factors as defined by the source.
- Apply the source-defined HRS internal uniform 1-10 normalization rule before computing Merit. Boundary ownership, max-equals-min behavior, and out-of-range handling remain unresolved.
- Compute Merit using the source-defined formula shape: W1 × NumberOfAccess + W2 × Centrality.
- Select the site with maximum Merit.

The concrete numerical values of W1 and W2 are not fixed by the source and must remain unresolved in this contract unless a later authoritative decision is added.

#### B.5.2 Selection rule

- Compute C = (n × alpha) + beta
- Compute L = Nt / Sr
- Compute N(a,b) = Bandwidth(a,b) / NetworkLatency(a,b)
- Compute TotalCost = W3 × (1/C) + W4 × L + W5 × (1/N)
- Build the candidate replica-provider list only from sites/nodes that currently contain a replica of the requested file
- Select the candidate provider with minimum TotalCost
- If the requested file replica already exists at the selected placement site, do nothing and do not continue to storage-check or replacement logic

The exact weight vector W3, W4, W5 remains unresolved in this contract and must not be silently assigned.

#### B.5.3 Replacement rule

- Check available storage at the placement site before creating the replica.
- If storage is sufficient, create the replica without invoking replacement.
- If storage is insufficient, evaluate replicas at the target site.
- Compute replica Value via the fuzzy system.
- Sort replicas in ascending order of Value.
- Delete the lowest-value replicas until enough space is available.
- Then create the replica.

### B.6 Storage constraints

The simulator must track the following:

- total capacity per site
- used storage per site
- required space for the candidate replica
- space freed by each deleted replica

Required behavior:

- if the requested file replica already exists at the selected placement site, no storage check or replacement is performed
- otherwise, replacement must not proceed without checking whether the target site has enough available storage
- after each deletion, available storage is re-evaluated
- deletion stops as soon as sufficient storage is available for the new replica

### B.7 Error and edge cases

These do not change the scientific algorithm but must be handled by the simulator as deterministic software conditions.

- No candidate site available for placement
- No candidate provider available for selection
- Zero or missing bandwidth value
- Zero or missing latency value
- Zero or missing VM capability value
- Zero or missing service rate Sr
- Empty replica list during replacement
- Insufficient storage even after deleting all candidate replicas
- Duplicate file entries or duplicate site IDs
- Equal Merit values
- Equal TotalCost values
- Equal replica Value values

Required handling policy:

- For all tie cases, use a project-level deterministic policy, because no source-defined tie-break rule exists.
- For all invalid numeric values, mark the decision as invalid or reject the replication step according to simulator policy; do not invent scientific behavior to compensate.

---

## C. Unresolved scientific parameters

This section marks all scientific details that remain unresolved in the HRS paper and therefore must remain unresolved in any implementation.

### C.1 Fuzzy membership parameters

The paper states that the fuzzy system uses three inputs and one output, and it provides ranges, but the exact continuous membership-function parameters are not recoverable from the paper in a source-faithful way.

The following are therefore UNRESOLVED:

- exact membership-function shapes
- breakpoints for all fuzzy sets
- exact membership-function parameters for NumberOfAccesses
- exact membership-function parameters for ReplicationCost
- exact membership-function parameters for LastAccessTimeInterval
- exact membership-function parameters for ReplicaValue

### C.2 Fuzzy rules

The paper states there are 21 fuzzy rules and shows some examples, but it does not provide the complete rule set in a recoverable form.

The following are therefore UNRESOLVED:

- the full set of 21 rules
- the exact antecedent combinations for all rules
- the exact consequent labels for all rules

### C.3 Fuzzy inference method

The paper does not state the specific fuzzy inference mechanism used.

The following is therefore UNRESOLVED:

- Mamdani vs Sugeno inference

### C.4 Defuzzification method

The paper does not state the defuzzification method used by the fuzzy system.

The following is therefore UNRESOLVED:

- centroid, bisector, mean of maxima, smallest of maxima, largest of maxima, or any other defuzzification method

### C.5 Unresolved HRS weights in source paper

Source-defined information:

- The Merit formula uses W1 and W2.
- The paper reports empirical/example W1/W2 pairs in its table and states that W3, W4, and W5 are adjustable.
- The paper states that W3, W4, and W5 have equal value in its simulation and gives a sum-to-one condition, but this is not an unambiguous project-wide final vector.

Source ambiguity:

- The W1/W2 prose conflicts with the W1/W2 table.
- The source does not provide one unambiguous authoritative final weight vector for execution in this project.

The following are UNRESOLVED:

- final W1 and W2 values for Merit
- final W3, W4, and W5 values for TotalCost
- whether any reported example or simulation setting is intended as the final project configuration

The following are RESEARCHER-REQUIRED before a final executable configuration can be frozen:

- an explicit decision selecting or otherwise defining the final W1/W2 configuration
- an explicit decision selecting or otherwise defining the final W3/W4/W5 configuration

The implementation contract does not assign a final vector and must not invent one.

### C.6 Other paper-undefined behaviors

The following remain outside the HRS scientific contract because the paper does not provide enough source detail:

- exact topology structure of the cloud network
- complete network graph specification
- exact bandwidth matrix
- exact simulation schedule beyond the supplied parameter summary
- exact hit-ratio formula
- exact bandwidth-consumption formula
- exact number-of-communications formula
- exact load-variance formula
- exact overall HRS complexity expression
- any additional optimization beyond placement, selection, and replacement
- any periodic optimization, dynamic replica count optimization, failure-recovery logic, or energy objective not explicitly in the HRS paper

---

## D. Contract summary

### D.1 Required HRS behavior

- Primary/source-defined replication trigger: replication is triggered when a requested file is not present in the local storage.
- Select placement site via centrality + number of accesses.
- Compute C = (n × alpha) + beta
- Compute L = Nt / Sr
- Compute N(a,b) = Bandwidth(a,b) / NetworkLatency(a,b)
- Compute TotalCost = W3 × (1 / C) + W4 × L + W5 × (1 / N)
- Select provider via minimum TotalCost from candidate replica providers derived from sites/nodes that currently contain a replica of the requested file.
- Check whether the requested file replica already exists at the selected placement site.
- If the replica already exists at the selected placement site, do nothing and do not continue into storage-check or replacement logic.
- If the replica does not exist at the selected placement site, check storage.
- If storage is sufficient, create the replica without replacement.
- If storage is insufficient, replace low-value replicas using the fuzzy system output.
- After each deletion, available storage is re-evaluated.
- Create the replica once sufficient storage is available.

### D.2 Required non-scientific specification boundaries

- The fuzzy membership functions and complete fuzzy rule base remain UNRESOLVED.
- Tie handling must use a project-level deterministic policy only if such a policy is separately defined by the simulator or researcher.
- No additional optimization objective, periodic optimization, or failure-recovery logic may be introduced unless separately specified outside the HRS paper.

### D.3 Parameter classification

Each parameter or requirement must be classified as exactly one of the allowed labels below.

- W1, W2 — UNRESOLVED
- W3, W4, W5 — UNRESOLVED
- HRS internal normalization rule — SOURCE-REQUIRED
- HRS internal normalization boundary and degenerate-range handling — UNRESOLVED
- fuzzy input and output ranges — SOURCE-REQUIRED
- fuzzy membership boundaries — UNRESOLVED
- fuzzy membership functions — UNRESOLVED
- fuzzy rule base — UNRESOLVED
- fuzzy inference method — UNRESOLVED
- defuzzification method — UNRESOLVED
- target storage check before replacement — SOURCE-REQUIRED
- candidate-provider selection from sites containing the file — SOURCE-REQUIRED
- centrality metric definition — SOURCE-REQUIRED
- Merit formula shape — SOURCE-REQUIRED
- TotalCost formula shape — SOURCE-REQUIRED
- replacement-trigger condition — SOURCE-REQUIRED
- replacement ranking by lowest replica value — SOURCE-REQUIRED
- deterministic tie-break policy — IMPLEMENTATION-DETAIL
- initial random primary-copy placement — SOURCE-REQUIRED
- random seed and repetition policy — COMMON-SIMULATOR-REQUIRED
- common comparison normalization — COMMON-SIMULATOR-REQUIRED

### D.4 Implementation readiness

#### D.4.1 Ready to implement

The following source-defined behavior is ready to implement without adding scientific assumptions:

- replication trigger and placement/selection/replacement lifecycle
- closeness-centrality formula and Merit formula structure
- source-defined HRS internal 1-10 normalization rule, subject to separately recorded edge-case handling
- VM capability, VM load, network performance, and TotalCost formula structures
- minimum-TotalCost provider selection from current replica providers
- storage check, conditional replacement, ascending Value deletion, and stop condition
- initial random primary-copy placement as a simulator setup behavior, without inventing seed or repetition policy

#### D.4.2 Blocked by source/research decision

HRS is blocked from a faithful final executable configuration by the following:

- final W1/W2 configuration
- final W3/W4/W5 configuration
- normalization boundary and max-equals-min behavior
- the complete fuzzy rule base and exact membership parameters
- the fuzzy inference and defuzzification method

Before implementation is frozen, the researcher must explicitly decide or clarify each blocked item. The developer must not choose a weight vector, infer fuzzy parameters, complete the rule base, select fuzzy defaults, or repair the source contradiction.

What must not be invented by the developer:

- a new weight vector
- a fallback equal-weight policy
- a guessed fuzzy membership set
- a guessed rule base
- a guessed defuzzification rule
- a common comparison normalization method embedded inside HRS
- any non-source failure-recovery or dynamic optimization behavior

---

## E. Compliance checklist for HRS implementation

An implementation is considered HRS-source-faithful only if all items below are satisfied:

- [ ] Primary/source-defined replication trigger: replication is triggered when a requested file is not present in the local storage.
- [ ] Placement uses centrality and number of accesses.
- [ ] Merit uses the source-defined formula structure and preserves the unresolved weight boundary.
- [ ] Selection uses VM capability, VM load, and network performance.
- [ ] C, L, N, and TotalCost formulas match the paper.
- [ ] The final W1/W2 and W3/W4/W5 values are not silently hard-coded by the contract.
- [ ] HRS internal normalization is separated from common comparison normalization.
- [ ] The fuzzy rule base and membership parameters remain explicitly unresolved.
- [ ] The contract does not import Proposed, DPRS, EIMORM, or OGSA logic.
- [ ] The contract is blocked by source or researcher decisions for final executable parameterization until the missing values are specified explicitly.
- [ ] Candidate replica providers are derived only from sites/nodes that currently contain a replica of the requested file.
- [ ] If the requested file replica already exists at the selected placement site, no storage checking, fuzzy replacement, or extra replica is created.
- [ ] If a valid candidate provider exists, it is selected according to minimum TotalCost.
- [ ] Replacement is triggered only by insufficient storage after the replica-already-exists check.
- [ ] Replacement uses the three fuzzy inputs from the paper.
- [ ] Replica Value is sorted ascending and low-value replicas are removed first.
- [ ] Missing fuzzy parameters and rules remain explicitly marked as UNRESOLVED.
- [ ] No invented optimization methods or objective functions are introduced.
- [ ] Only project-level deterministic tie policies are used where the source does not specify a rule.

This contract is intentionally kept at the software-requirement level and does not implement the method.

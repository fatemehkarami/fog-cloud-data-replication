# EIMORM specification extracted from the original paper

## 1. Source identity

- Full paper title: "An efficient and improved multi-objective optimized replication management with dynamic and cost aware strategies in cloud computing data center"
- Authors: E. Bijolin Edwin, P. Umamaheswari, M. Roshni Thanka
- Publication: Cluster Computing
- Year: 2017
- DOI: https://doi.org/10.1007/s10586-017-1313-6
- Acronym used by the paper: EIMORM
- Paper type: source paper for a cloud data-replication strategy with dynamic, cost-aware, multi-objective optimization

Status summary:

- SOURCE-DEFINED: paper identity, title, authors, publication context
- PARTIALLY DEFINED: exact relationship among EIMORM, DCR2S, EDCR2S, and IEK is not fully specified in a formal architecture diagram or pseudocode
- UNRESOLVED: any hierarchical decomposition not explicitly shown in the paper

---

## 2. Algorithm identity and terminology

### 2.1 Algorithm identity

The paper presents EIMORM as an efficient and improved multi-objective optimized replication management strategy for cloud computing data centers.

The abstract explicitly states that:

- replication is used to increase availability and performance;
- the multi-objective optimization strategy considers replication cost from higher-cost data centers to lower-cost data centers;
- the method uses the concept of Improved knapsack (IEK) to optimize replication cost;
- availability and load balancing are considered as part of the replication process;
- EIMORM balances among optimization objectives.

The conclusion also states:

- "Dynamic cost-aware re-replication and re-balancing Strategy (DCR2S) algorithm on heterogeneous cloud infra data centers has multiple phases in rebalancing the datas."
- "When the replication cost increases to the user budget, then the Improved and efficient Knapsack algorithm is implemented for the optimization of replication cost."
- "EIMORM algorithm was introduced to invoke and solve the objectives of the problem and to be tested."

### 2.2 Terminology preserved from the paper

The source paper uses the following terms:

- EIMORM
- DCR2S
- EDCR2S
- IEK / Improved and Efficient Knapsack
- ETBDF / Enhanced Time Based Decaying Function
- EARF / Enhanced Adjustable Replica Factor
- replica catalog
- replica manager
- broker
- data center, host, VM
- file availability, block availability, file unavailability
- multi-objective optimization

### 2.3 Relationship between EIMORM, DCR2S, EDCR2S, IEK, ETBDF, EARF

The paper does not provide a single, formal subsystem hierarchy that defines all relationships unequivocally. The source statements are instead fragmentary:

- EIMORM is the overall replication-management strategy.
- DCR2S is mentioned as a dynamic cost-aware re-replication and re-balancing strategy in the conclusion.
- EDCR2S is described in the phase-1 discussion as the proposed algorithm that uses ETBDF.
- IEK is explicitly described as the mechanism used to optimize replication cost when the replication cost exceeds the user budget.
- ETBDF is described as a file-weighting / time-decay function used in file identification.
- EARF is described as a factor associated with the Phase-2 replica-factor decision; the paper does not specify the executable mapping from this factor to replica creation or exact replica count.

Important source-fidelity statement:

- The paper does not specify a complete formal call graph or algorithm inheritance chain among these names.
- Therefore, the relationships among EIMORM, DCR2S, EDCR2S, and IEK should be treated as PARTIALLY DEFINED and not reconstructed beyond what the source explicitly states.

---

## 3. Problem addressed

The paper is concerned with a cloud storage system in which:

- users request data files from geographically distributed data centers;
- files may be replicated to improve data availability and application performance;
- too many replicas increase overhead and energy/cost;
- the strategy should keep performance, load balancing, availability, and cost in balance;
- the system is heterogeneous, with different data centers having different availability, cost, load, and performance characteristics.

The text states that replication must be done selectively because:

- creating replicas indiscriminately is not efficient;
- only popular files with high access frequency should be replicated;
- once a file has reached sufficient availability, further replicas add cost without proportional availability gain;
- replica placement must be chosen carefully to improve performance without causing excessive replication overhead.

The paper also explicitly emphasizes multi-objective optimization and cost-aware behavior, especially for re-replication and re-balancing of copies from higher-cost to lower-cost data centers.

Status:

- DEFINED: high-level problem statement
- PARTIALLY DEFINED: exact optimization formulation, objective weighting, and decision thresholds are not fully specified
- UNRESOLVED: no formal optimization problem is stated in a complete and executable form

---

## 4. System architecture

The paper describes a multi-tier hierarchical, heterogeneous cloud system with the following components:

- super data center(s) at the most internal tier
- ordinary data centers at outer tiers
- users connected to ordinary data centers through brokers
- hosts inside each data center
- virtual machines running on hosts
- replica catalog keeping file-replica location metadata
- replica manager making replication decisions and interacting with the catalog

The architecture is described in prose and Figure 1, with the following source statements:

- "multi-tier hierarchical architecture provides better data sharing; all the data files are placed at the innermost tier i.e. at the Super Data Center."
- "Figure 1 shows Super data centers which the most reliable data centers are having high availability, high reliability, high performance, huge storage space and high processing capabilities compared to the data centers in other tiers."
- "Users are present in outer-most tier and are directly connected to the ordinary data centers."
- "The data centers are heterogeneous in nature."
- "Each data center consists of multiple hosts. A host is a physical machine that can run multiple virtual machines on it."
- "A user sends a request to the broker to access a data file. The broker helps to schedule the user’s request to a desired data center."
- "The replica catalog maintains the information regarding the location of all the replicas of each data file. So broker first requests the replica catalog to get the requested data file in that data center."

### 4.1 Data-center model described by the paper

The text states that each data center can be represented as a set:

- DC = {dc1, dc2, ..., dcx}

with files:

- F = {f1, f2, ..., fs}

and blocks:

- B = {B1, B2, ..., Bs}

The paper also says each data file is partitioned into fixed-size blocks.

### 4.2 Explicitly described system roles

- Data center: infrastructure site; heterogeneous in cost, reliability, availability, performance
- Host: physical machine
- VM: run on host, resource for processing requests
- Broker: scheduler / requestRouter for user access
- Replica catalog: metadata store of replica locations and block availability parameters
- Replica manager: computes or coordinates file replication decisions from catalog state

Status:

- DEFINED: architectural roles and components are described in prose
- PARTIALLY DEFINED: exact interaction protocol between replica manager, catalog, and broker is not formally specified
- UNRESOLVED: a complete execution workflow for request handling and placement decisions is not provided

---

## 5. Data / file model

### 5.1 File and block model

The paper states that a data file is partitioned into fixed-size blocks. The text uses the notation:

- file f_k
- block b_kj
- replica of a file may be stored across different data centers

### 5.2 Block availability and file availability

The paper defines block availability as a per-block, per-replica probability. The text states:

- "Let pr(bekj) represents the block availability ... of a block b_kj of each replica of a data file, say flk."
- "In heterogeneous system, the availability of data at different data centers is different."
- "The different improved values of pr(bekj) at each data centers are being maintained by the replica catalog along with the location of each replica."

The exact statement includes:

- `Pr(beKj)Main DC > Pr(bekj)imp DC > Pr(bekj)Normal DC`

This is a source-defined ordering of availability across Different data-center tiers, but no exact formula for the availability values is given beyond the probability formulation below.

### 5.3 Replica factors and availability information

The paper introduces a replica-factor mechanism:

- `RFk` = recent replica factor of the file
- `RFk_old` = old replica factor of the file
- `ARFk(one)` = enhanced adjustable replica factor for one file

The source text provides the equation:

```
ARFK(one) = RFK / (RFK + RFKold)
```

and states that this is associated with the Phase-2 replica-factor decision. The paper does not specify the executable mapping from this factor to replica creation or exact replica count.

Status:

- DEFINED: concept of blocks, file availability, and replica factor
- PARTIALLY DEFINED: formulas are partially OCR-damaged and not fully formalized
- UNRESOLVED: exact semantics of `RFk`, `RFk_old`, and the mapping from replica factors to replica count are not fully specified

---

## 6. Inputs and parameters

This section records only source-observable parameters and marks missing or ambiguous ones.

| Parameter / symbol | Meaning in the paper | Status |
| --- | --- | --- |
| DC / dcx | data-center set | DEFINED |
| F / fk | file set and individual file | DEFINED |
| B / bkj | blocks of a file | DEFINED |
| pr(bekj) | block availability probability | PARTIALLY DEFINED |
| Pr(Flk) | file availability probability | PARTIALLY DEFINED |
| P(Falk) / file unavailability | file unavailability probability | PARTIALLY DEFINED |
| `RFk` | recent replica factor | PARTIALLY DEFINED |
| `RFk_old` | old replica factor | PARTIALLY DEFINED |
| `ARFk(one)` | adjustable replica factor for one file | DEFINED in equation form |
| `ETBDF` | enhanced time-based decaying function | PARTIALLY DEFINED |
| `tc` | current access time | DEFINED in text |
| `ts` | start time of historical access interval | DEFINED in text |
| `λ` | decay rate parameter in ETBDF | DEFINED as `λ ∈ {1, 2, 3, ...}` |
| `Cost(DC)` | replication cost per data center | PARTIALLY DEFINED |
| `bk(dck)` | count of files in a data center | PARTIALLY DEFINED |
| `Pmax(j)` | max power draw of node j | DEFINED in text |
| `Pidle(j)` | idle power of node j | DEFINED in text |
| `U(i, j)` | file existence / availability indicator | PARTIALLY DEFINED |
| `sn(i, j)` | service duration or mean service time | PARTIALLY DEFINED |
| `A(i, j)` | percent of read requests or access proportion | PARTIALLY DEFINED |
| `B(j)` | bandwidth at node j | PARTIALLY DEFINED |
| `Li` | data mean latency for file i | PARTIALLY DEFINED |
| user budget | threshold for invoking IEK | PARTIALLY DEFINED |
| objective weights / normalization | system preference weights | UNRESOLVED |
| simulation workload sizes | number of users, files, VMs, blocks, requests | UNRESOLVED |
| exact battery / energy coefficients | not fully specified | UNRESOLVED |

Important distinction:

- If the paper provides a formula or word definition, it is SOURCE-DEFINED.
- If the formula is visibly OCR-corrupted or incomplete, it is PARTIALLY DEFINED.
- If the paper says a concept exists but gives no concrete rule or value, it is UNRESOLVED.

---

## 7. Replication trigger / phase structure

The source describes a multi-phase decision process, but it does not provide a fully formal trigger policy or pseudocode for the global algorithm.

The paper states that:

- "Phase 1: analyze the type of file and time to replicate"
- "Phase 2: determining new replicas"

It also states that ETBDF is used in file identification and that EARF / `ARFk(one)` is associated with the Phase-2 replica-factor decision, but the paper does not specify the executable mapping from this factor to replica creation or exact replica count.

The paper also says:

- replication is triggered for files with high access rates and high popularity;
- once a file is sufficiently replicated, further additions add limited benefit and increase cost;
- the Improved Efficient Knapsack method is invoked when replication cost exceeds the user budget.

The exact trigger condition for invoking the full EIMORM process is not formally stated as a deterministic algorithmic rule.

Status:

- DEFINED: there are at least two phases and a conceptual workflow
- PARTIALLY DEFINED: exact activation conditions, ordering, and loop structure are not formally provided
- UNRESOLVED: global scheduling policy for replication decisions and event triggers

---

## 8. Phase 1 — File identification

### 8.1 ETBDF

The paper states:

- "Enhanced time based decaying function (ETBDF) used to assign different 'Data weights' and 'Data importance' of accesses in data file node with enormous data time intervals."
- "ETBDF gives weights higher in accessing recent data file."
- "The proposed algorithm EDCR2S algorithm has different phases as in data nodes."

The source text then gives the following formula, with OCR corruption:

```
ETBDF = ( tc , ts = er −(tc − ts)λ )
```

and a textual explanation:

- `λ ∈ {1, 2, 3, ...}`
- `ts` = data start time
- `tc` = access current time

This expression is explicitly treated as:

- PARTIALLY DEFINED
- OCR-DAMAGED
- SOURCE-VERIFIABLE only in the limited sense that it is a time-decay / recency-based weighting concept, and that recent accesses are assigned higher weight

The paper does not provide a clean, unambiguous executable equation in a publishable form. The source must not be silently repaired into a different mathematical function. The only source-faithful semantics are:

- ETBDF is associated with time-based decay and access weighting;
- more recent accesses receive higher weight;
- `tc` is the current/access time;
- `ts` is the start time of the historical interval;
- `λ` is described as a positive integer parameter.

### 8.2 How the paper uses ETBDF

The paper uses ETBDF to rank or weight files by recency and importance of access. More recent accesses are assigned higher weight. This is used for file identification and prioritization before deciding whether the file needs more replicas.

### 8.3 Thresholds or exact decision rule

The paper does not state a threshold such as:

- file selected if ETBDF > X,
- replication if access weight exceeds a fixed threshold,
- or a formal rule to convert ETBDF into replica priority.

This is therefore:

- PARTIALLY DEFINED: usage concept is clear
- UNRESOLVED: exact decision rule and threshold are absent

---

## 9. Phase 2 — Determining new replicas

The paper states:

- "Next process after data file identification is to determine the suitable number of new replicas."
- "The replica manager calculates the old probability of File Availability in data center."
- "This data center replica factor is determined by the Enhanced Adjustable Replica Factor (EARFk)."

### 9.1 EARF and the replica-factor rule

The source text provides the specific formula:

```
ARFK(one) = RFK / (RFK + RFKold)
```

with the explanatory text:

- `RFk_old` = old replica factor of the data file
- `RFk` = recent replica factor of the data file
- `ARFk(one)` = ratio of recent replica factor to total current plus old replica factor

This formula is the clearest explicit expression associated with the Phase-2 replica-factor decision. It is not sufficient to conclude that EARF directly decides whether a replica should be created or determines the exact number of new replicas. The paper does not specify the executable mapping from the replica factor to a final replica-creation decision or target replica count.

### 9.2 How replica count is actually determined

The paper does not provide a complete, implementable rule such as:

- number of replicas = ceil( ... )
- new replica count = derived from availability threshold
- create one more replica whenever `ARFk(one)` > threshold
- any exact formula for target replica count

The text only says:

- the replica manager calculates old file availability;
- EARF / `ARFk(one)` is associated with the Phase-2 replica-factor decision;
- availability is used in the selection of a file for replication;
- new replicas are considered when that evaluation indicates a need.

This means the actual replica-count logic is:

- PARTIALLY DEFINED at the conceptual level,
- UNRESOLVED as an executable algorithmic rule.

The mapping from EARF / `ARFk(one)` to an exact replica-creation decision or exact replica count is UNRESOLVED.

### 9.3 Missing behavior in Phase 2

The paper does not define:

- explicit target availability threshold,
- exact formula for desired replica count,
- exact decision to create one or several replicas,
- precise handling when file availability is already high,
- exception handling if the cost or budget is exceeded,
- exact provider / placement selection procedure.

---

## 10. Availability model

The paper contains a block-level and file-level availability discussion, but the mathematical presentation is heavily OCR-damaged. The following is the best faithful extraction from the source.

### 10.1 Block availability

The source states:

- `pr(bekj)` is the block availability probability for a block of a particular replica of a file.
- In heterogeneous clouds, block availability differs across data centers.
- The catalog maintains these probabilities for each replica.

It also writes:

```
Pr(beKj)Main DC > Pr(bekj)imp DC > Pr(bekj)Normal DC
```

This is a source-defined ordering of availability by data-center type, but it is not a formal model with a complete calculation rule.

### 10.2 File availability

The text states that the probability of file availability and the probability of file unavailability are calculated as follows:

```
Pr(Flk) =
{
  (1 − ∏_{j=1}^{brk} (1 − p(bavk)i)   for phase 1
  ∏_{kj=1}^{n} ( 1 − ∏_{j=1}^{brk}(1 − p(bavk)i) )  for phase 2
}
```

and a companion equation appears for file unavailability:

```
P(Falk) =
{
  1 − ( ... )  for phase 1
  ...  for phase 2
}
```

This is clearly source-defined in concept but heavily corrupted in OCR. It should be treated as:

- PARTIALLY DEFINED: conceptually clear
- UNRESOLVED: exact formula cannot be reconstructed without ambiguity

### 10.3 File unavailability and reliability-related expressions

The paper includes the following additional text on page 5:

- `R(fi) = ∏_{k=1}^{n} (i, j) × p_j`
- `R(fi) = 1 − ∏ ...`
- "here Q_ is cumulative multiplier of non-zero elements of file f1 unavailable is 0.000005."

These expressions are not presented consistently enough to serve as an implementation-ready reliability or unavailability model. They are best treated as:

- PARTIALLY DEFINED: the discussion of file unavailability exists
- UNRESOLVED: exact mathematical form and semantic meaning cannot be fixed from the source without introducing assumptions

Important source-fidelity rule:

The paper's availability / unavailability / reliability expressions are not automatically equivalent to the project's common Reliability metric. The source-level expressions are EIMORM paper artifacts; any project-wide Reliability definition must be established separately as a simulator or researcher-defined metric, and it must not be silently identified with the paper's `R(fi)` expressions.

### 10.4 Availability status summary

- DEFINED: availability is a primary objective and block/file availability are discussed as probability-based concepts
- PARTIALLY DEFINED: there are available formulas, but they are ambiguous or OCR-damaged
- UNRESOLVED: no definitive operational rule for a target availability threshold or for exact file-unavailability calculation

---

## 11. Cost model

The paper says that cost is a major objective and that the cost differs by data center. It also says the method optimizes cost by moving replication from higher-cost to lower-cost data centers.

### 11.1 Cost definition

The paper defines a cost set:

```
Cost(DC) = { cost(dc1), cost(dc2), ..., cost(dck) }
```

and states that higher-performance, higher-availability, and more reliable data centers have higher replication cost.

It then gives a cost expression of the form:

```
Costi(DCS)j = Σ_{x=1}^{y} (cost(dck) × bk(dck))
```

where:

- `bk(dck)` appears to be the count of files in a data center;
- the total cost is aggregated across data centers.

This is the paper’s explicit cost model as presented, but the notation is weakly extracted and not fully formalized.

### 11.2 User budget and IEK

The paper states:

- "When the replication cost increases to the user budget, then the Improved and efficient Knapsack algorithm is implemented for the optimization of replication cost."

This phrase gives a conceptual trigger, but:

- there is no explicit formula for the budget;
- no threshold value is given;
- no formal knapsack objective function is stated.

### 11.3 Cost-model status

- DEFINED: cost is a primary optimization objective and is discussed as a function of data-center replication cost
- PARTIALLY DEFINED: cost formulas are visible but not fully consistent or formalized in the text
- UNRESOLVED: exact user-budget threshold, knapsack objective, and optimization constraints are not provided

---

## 12. Load balancing model

The paper identifies load balancing as one of the optimization objectives and provides several related expressions.

### 12.1 Mean service time (MST)

The text writes:

```
sn(i, j) = (i, j) × Si / tqj
```

and further:

```
st(j) = Σ_{k=1}^{m} st(i, j) × (an cos nπ A(i, j) / A(i) + n)
```

The equation is clearly OCR-damaged and semantically unclear. The paper says the mean service time of a file on a data node is derived from observed service duration and access patterns.

### 12.2 DLoad variance (DLV)

The paper states:

```
a(i, j) = B(i, j) × sn(i, j)
```

and then discusses node load variance and the degree of load balancing of the system.

This is not a complete, unambiguous definition of a variance metric; it is best treated as a source-defined concept with an incompletely extracted formula.

### 12.3 Interpretation

The public intent is clear:

- the algorithm measures load distribution across nodes;
- imbalance should be reduced to improve performance;
- load balancing is one objective alongside availability and cost.

However, the precise formula for DLoad variance and the exact optimization target are not fully specified.

Status:

- DEFINED: load balancing is an objective and a concept in the paper
- PARTIALLY DEFINED: some formulas are present but OCR-damaged
- UNRESOLVED: exact DLoad variance definition and optimization rule are not cleanly present

---

## 13. Energy model

The paper explicitly names energy consumption as an optimization concern and provides a formula that appears in the source as follows:

```
ERE(j) = Σ_{i=1}^{n} /Phi1(i, j) × l(i, j) × (Pmax(j) − Pidle(j)) + Pidle(j)
```

where:

- `Pmax(j)` = maximum power consumed by node `Dj` at peak load
- `Pidle(j)` = power consumed when the node is idle

The paper states that the total level of energy-minimized consumption has data renewable energy consumption (DREC); DRE and DCE should be minimized.

It also says that the system aims to reduce energy consumption while keeping load balanced and availability adequate.

Status:

- DEFINED: energy is a consideration and the variables `Pmax` and `Pidle` are named
- PARTIALLY DEFINED: the equation is OCR-corrupted and not fully readable
- UNRESOLVED: no complete, implementation-ready energy objective function or exact threshold is provided

---

## 14. Latency model

The paper includes a section called "Data mean latency (DML)" and states that minimizing latency is important in storage systems.

The paper gives a formula of the following shape:

```
Li = 1 / ri × Σ_{j=1}^{m} /Phi1(i, j) × si / B(j) × A(i, j)
```

with the textual explanation:

- `A(i, j)` = percentage of read requests of data through data nodes `Dj` requesting file `fi`
- `B(j)` = minimum bandwidth in node `Dj`

The formula is visibly malformed in extraction and should not be repaired silently. It demonstrates that the paper uses a latency model for file access and read patterns, but the exact symbolic details are not reliable enough for a direct executable implementation.

Status:

- DEFINED: latency is a relevant objective
- PARTIALLY DEFINED: the model exists in prose and a malformed equation
- UNRESOLVED: exact formula and parameter definitions cannot be reconstructed without assumption

---

## 15. Multi-objective optimization

The paper clearly claims that the strategy is a multi-objective optimization approach. The five performance dimensions explicitly discussed are:

- availability
- cost
- load balancing
- energy consumption
- latency / service time

The abstract and architecture discussion repeatedly state that EIMORM balances among these objectives.

However, the paper does not provide:

- a complete formal five-objective vector definition,
- a scalar aggregation function,
- a Pareto formulation,
- explicit weighting coefficients,
- any normalization strategy across the five objectives,
- a fully specified objective function or optimization criterion.

The paper does mention that proportion parameters are used in the experimental comparison and that performance can be tuned according to user preference, but it does not provide a complete formal five-objective objective formulation in a way that is directly executable. The exact objective aggregation and weighting are therefore UNRESOLVED.

Status:

- DEFINED: multi-objective nature is explicit
- PARTIALLY DEFINED: the five dimensions are identified
- UNRESOLVED: total objective function, aggregation, and weighting mechanism are not specified by the source

---

## 16. Improved Knapsack / IEK

### 16.1 What the paper explicitly says

The paper states that:

- "The concept of improved and efficient Knapsack(IEK) algorithm is being used that will optimize replication cost."
- "When the replication cost increases to the user budget, then the Improved and efficient Knapsack algorithm is implemented for the optimization of replication cost."

It also states that the method is used to move replication from higher-cost data centers to lower-cost data centers without compromising data availability.

This is source-faithful wording: IEK is described as a cost-optimization mechanism for re-replication under the stated user-budget condition, and it is associated with moving replication from higher-cost to lower-cost data centers. The paper does not state that IEK selects which replicas to keep, unless that selection logic is explicitly given elsewhere in the source; no such explicit item-selection semantics are provided here.

### 16.2 Trigger condition

The only clear trigger described is:

- when replication cost exceeds the user budget

This is a conceptual trigger and not a fully specified decision equation.

### 16.3 Role in replication-cost optimization

The role is clear conceptually:

- IEK is used as a cost-optimization mechanism for re-replication under a user-budget constraint;
- it is tied to moving replication from higher-cost to lower-cost data centers;
- exact item-selection semantics remain UNRESOLVED.

### 16.4 Input and output

The paper does not provide:

- the exact knapsack inputs,
- the value of each item or weight,
- the capacity variable,
- the profit function,
- the output data structure

### 16.5 Pseudocode

No implementable IEK pseudocode is provided in the paper.

Status:

- DEFINED: IEK exists as a conceptual cost-optimization mechanism
- PARTIALLY DEFINED: trigger and role are clear conceptually
- UNRESOLVED: exact algorithm, inputs, outputs, and pseudocode are not provided

---

## 17. Replica placement

The source discusses replica placement conceptually but does not specify a complete placement rule.

The paper says:

- the broker first checks the replica catalog;
- the replica manager decides whether a file should be replicated;
- replicas should be placed at data centers that balance availability, cost, and load;
- the strategy aims to place replicas in the right data centers and avoid excessive replication.

However, the paper does not explicitly define a placement algorithm such as:

- selecting the nearest data center,
- selecting the cheapest available data center,
- selecting the data center with maximum availability,
- selecting the least-loaded node,
- selecting a provider according to a closed-form objective.

The paper does not provide a final, executable placement formula.

Therefore:

- PARTIALLY DEFINED: placement is a conceptual requirement of the strategy
- UNRESOLVED: actual placement decision rule is not fully specified

---

## 18. Replica deletion / replacement / re-replication

### 18.1 Conceptual statements

The paper discusses dynamic and cost-aware re-replication and re-balancing. It states that:

- dynamic replication can create and delete replicas;
- replication cost is optimized by re-replicating from higher-cost data centers to lower-cost data centers without compromising data availability;
- EIMORM is designed to address dynamic and cost-aware replication management;
- load balancing and cost balancing are important in replica management.

### 18.2 What is not executable

The paper does not define an actual executable policy for:

- which file is deleted,
- which replica is chosen for deletion,
- when replacement is triggered,
- how re-replication decisions are ordered,
- how to maintain consistency when moving replicas,
- a formal replacement heuristic or cost formula for choosing old replicas to remove.

### 18.3 Source fidelity

The paper contains conceptual language about dynamic behavior but not a concrete, implementable replica-deletion or replacement rule. This makes it unsafe to infer an implementation from general replication practice.

Status:

- PARTIALLY DEFINED: conceptual dynamic re-replication and re-balancing are mentioned
- UNRESOLVED: exact deletion, replacement, and re-replication policy are not specified

---

## 19. Failure handling

The paper discusses fault tolerance conceptually and says that replication provides resilience when one site fails, but it does not give a formal failure model or recovery algorithm.

The text states:

- "When some sites holding the requested file fail, the request can still be served from other sites by holding the replica of the desired file in the main file."
- the system aims to maintain high reliability and fault tolerance.

However, there is no formal specification for:

- failure detection,
- repair procedures,
- failed-node exclusion logic,
- re-replication after node failure,
- failure probability model,
- recovery trigger threshold.

Status:

- PARTIALLY DEFINED: fault tolerance is a conceptual objective
- UNRESOLVED: failure detection, recovery, and fault-handling algorithm are not defined by the source

---

## 20. Original paper's algorithm / pseudocode

The paper does not present a complete algorithmic pseudocode for EIMORM itself.

What the paper does contain:

1. A conceptual system workflow in prose.
2. A high-level description of two phases:
   - Phase 1: file identification and weight assignment via ETBDF
   - Phase 2: determine new replicas using EARF and replica-manager logic
3. A conceptual explanation that IEK is invoked when replication cost exceeds the user budget.
4. A MySQL replication script in the experimental section that is clearly part of the infrastructure setup and validation environment, not the EIMORM replication algorithm itself.

The paper does not provide a clean EIMORM pseudocode block such as:

- initialize state
- evaluate files
- compute ETBDF
- compute availability / cost / load / energy
- decide replica count
- place replicas
- update catalog
- invoke IEK if budget exceeded

Therefore the best faithful reconstruction is:

```
EIMORM conceptual workflow (source-faithful):
1. Observe files and data-center context.
2. Identify files needing replication using ETBDF / recency-weighted access analysis.
3. Compute current file availability and other relevant replica state.
4. Evaluate the Phase-2 replica-factor decision using EARF / `ARFk(one)` and related replica-factor logic; the mapping to final replica creation or exact replica count remains unresolved.
5. Use IEK when replication cost exceeds the user budget.
6. Balance availability, cost, and load.
7. Maintain replica catalog and perform dynamic re-replication / re-balancing as conceptually described.
```

This is a reconstruction from the paper's prose only. It must not be treated as a complete executable algorithm.

Status:

- PARTIALLY DEFINED: conceptual workflow exists
- UNRESOLVED: formal pseudocode for EIMORM is not given

Note on Phase-2 wording:

The paper describes EARF / `ARFk(one)` as part of the Phase-2 replica-factor decision, but it does not specify the executable mapping from this factor to replica creation or exact replica count.

---

## 21. Complexity

The paper does not provide an explicit complexity analysis for EIMORM, ETBDF, EARF, IEK, or the full multi-objective optimization procedure.

No clear algorithmic complexity is explicitly stated for the decision process.

Status:

- UNRESOLVED: no source-defined complexity analysis is available

---

## 22. Original experimental setup

The paper's experimental section states that CloudSim was used and that the system was simulated in Java.

Explicit items in the paper:

- "CloudSim has been used for simulating and evaluating the proposed system."
- "CloudSim is a Java based simulator which provides many classes for modeling and simulating cloud systems."
- "We developed our own classes for simulation of the proposed system."
- "For replication process we use Vmware workstation, Vmware Tools, Xampp with MySQL running on it."

The paper reports a comparison with HDFS in a figure labeled as performance of EIMORM and HDFS.

It also says:

- EIMORM improves performance in the presence of user preference tuning;
- experimental results show it is more energy efficient and better performing than HDFS under the evaluated setup;
- the system uses multi-objective optimization and balancing among availability, cost, and load balancing.

The following items are not explicitly specified by the paper:

- number of data centers
- number of hosts / VMs
- workload generation profile
- file sizes or block sizes
- request rates or arrival distributions
- exact parameter values for objective weights
- exact thresholds for availability or budget
- detailed experimental scenario list
- precise comparison table of other algorithms beyond the high-level HDFS comparison

Status:

- DEFINED: CloudSim, Java-based simulator, VMware/XAMPP/MySQL environment, HDFS comparison mentioned
- PARTIALLY DEFINED: comparison methodology is described at a high level
- UNRESOLVED: detailed experiment configuration, workloads, and parameter values are not fully specified in the source

---

## 23. What the paper does not define

The paper does not define the following as a source-faithful executable behavior:

- exact file-selection threshold for replication
- exact target replica count or availability threshold
- exact algorithm for deciding where to place a replica
- exact provider-selection rule
- exact replica deletion rule
- exact replacement policy
- exact re-replication scheduling/policy
- exact definition of the knapsack objective and capacity
- exact optimization weights for the five objectives
- exact objective function used in the multi-objective optimization
- exact failure-detection and recovery policy
- exact complexity analysis
- exact workload parameters and scenario configuration
- exact values for most coefficients and thresholds

This list is intentionally strict and source-faithful.

---

## 24. Source-fidelity risk register

| Item | Status | Evidence | Implementation consequence |
| --- | --- | --- | --- |
| ETBDF equation | PARTIALLY DEFINED | Extracted formula is OCR-corrupted and not fully readable | Must not silently rewrite it without a researcher-defined approximation |
| EARF / replica-factor formula | DEFINED in equation form | `ARFK(one) = RFK / (RFK + RFKold)` is explicitly stated | The formula is source-defined, but its mapping to replica creation or exact replica count remains UNRESOLVED |
| IEK | PARTIALLY DEFINED | It is named and conceptually described, but no pseudocode or objective is supplied | Must not invent a knapsack algorithm from general knowledge |
| placement logic | UNRESOLVED | No exact placement heuristic is given | Must not invent a placement policy from other replication methods |
| replica deletion / replacement | UNRESOLVED | Only conceptual language about dynamic re-replication exists | Must not assume a deletion rule |
| failure handling | PARTIALLY DEFINED | Fault tolerance is mentioned conceptually | Must not model a specific failure-recovery algorithm without source support |
| multi-objective objective function | UNRESOLVED | Objectives are named, but no full aggregation or weight scheme is given | Any weighting must be researcher-defined experimental configuration |
| trigger policy | PARTIALLY DEFINED | ETBDF / EARF / IEK are discussed, but not in a precise event-driven rule | Must clearly separate source behavior from simulator invocation policy |
| load-balancing model | PARTIALLY DEFINED | Some equations are present but OCR-damaged | Must preserve ambiguity rather than correcting assumptions |
| latency / energy / availability formulas | PARTIALLY DEFINED | Present but malformed in extraction | Must treat exact implementation as not fully reliable from source alone |
| experimental configuration | PARTIALLY DEFINED | CloudSim and environment are described, but exact workloads are not | Must label missing values as researcher-defined configuration |

---

## 25. Mapping to our common simulator

This mapping is done only after establishing the source behavior. The rule is strict: do not invent missing EIMORM semantics to satisfy the common simulator.

| Required simulator interaction | Source-defined behavior | Adapter responsibility | Simulator responsibility | Unresolved issue |
| --- | --- | --- | --- | --- |
| When to invoke replication logic | The paper implies a two-phase workflow and mentions a budget-triggered IEK step, but does not provide a precise trigger policy | Adapter may read the state and expose the source-defined decision inputs only | Common simulator may define an experiment invocation schedule, but that is RESEARCHER-DEFINED EXPERIMENTAL CONFIGURATION and not source behavior | Exact runtime trigger condition is not source-defined |
| Read current file and replica state | The replica catalog is explicitly mentioned as the source of replica-location and availability information | Adapter reads data-center, file, and replica metadata | Simulator owns state storage and serialization | Exact catalog schema not source-defined |
| Determine file importance | ETBDF is the source-level concept for recent-access weighting | Adapter can compute ETBDF only if the project adopts the source-defined semantics and accepts the OCR-damaged formula as PARTIALLY DEFINED | Simulator supplies access history and timestamps | Exact ETBDF formula is OCR-damaged and partially defined |
| Phase-2 replica-factor decision | Phase 2 says EARF / `ARFk(one)` is associated with the Phase-2 replica-factor decision; the paper does not specify the executable mapping from this factor to replica creation or exact replica count | Adapter may surface this factor only if the source clearly supports it | Simulator validates whether creating the replica is feasible | Mapping from factor to final replica creation or exact replica count is unresolved |
| Choose replica location | The paper references placement in cost-aware, availability-aware, load-aware contexts, but gives no final executable rule | Adapter must not invent a provider-selection or placement policy | Simulator may apply common validation and placement constraints | Exact placement decision algorithm is unresolved |
| Use IEK budget optimization | IEK is correlated with user budget and cost optimization, but no exact objective is given | Adapter may only compute based on the explicit source terms | Simulator provides budget and cost values | Exact IEK algorithm and constraints are unresolved |
| Update replica catalog | The source refers to replica manager and catalog, but not a complete mutation protocol | Adapter should not directly mutate catalog unless the project defines a separate simulator contract | Simulator owns mutation and consistency logic | Exact mutation semantics are not source-defined |
| Handle storage feasibility | The paper states cost and availability matter, but does not define storage-capacity enforcement policy | Adapter may not add storage logic unless the project explicitly defines it | Simulator enforces storage, capacity, and validity checks | Capacity policy is not source-defined |
| Handle failures | Fault tolerance is only conceptual | Adapter must not create a failure model | Simulator owns failure generation and recovery handling | Failure model is unresolved |

Important note: the simulator must not invent an EIMORM runtime trigger and present it as source behavior. If an experiment requires an invocation schedule, it is RESEARCHER-DEFINED EXPERIMENTAL CONFIGURATION and must be kept separate from the EIMORM algorithm.

---

## 26. Final capability status

Use of status values is deliberately strict and source-faithful.

| Capability | Status |
| --- | --- |
| Replica selection | UNRESOLVED |
| Provider selection | UNRESOLVED |
| Replica creation | PARTIALLY DEFINED |
| Replica deletion / replacement | UNRESOLVED |
| Dynamic replica count | PARTIALLY DEFINED |
| Placement optimization | UNRESOLVED |
| Failure handling | UNRESOLVED |

Interpretation:

- The source paper mentions these capabilities conceptually and sometimes connects them to the overall objective.
- However, the actual executable logic is not sufficiently specified to treat them as concrete algorithmic behavior without additional assumptions.
- Replica creation and dynamic replica count are only partially defined in the paper because the relevant Phase-2 replica-factor logic is described, but the exact decision mapping is not specified.
- Any exact implementation of these capabilities must be labeled RESEARCHER-DEFINED EXPERIMENTAL CONFIGURATION, not source-defined EIMORM behavior.

---

## 27. Reproducibility Boundary

The published paper provides enough information to reproduce several high-level concepts and formulas, but it does not provide enough information for a complete executable source-faithful reconstruction of all replication-management decisions without researcher-defined assumptions.

The reproducible boundary is therefore:

- Some concepts are clearly present and can be described as source-level behavior, such as the multi-tier cloud architecture, the role of ETBDF in recency-based file weighting, and the association of EARF / `ARFk(one)` with the Phase-2 replica-factor decision.
- Some formulas are present but are OCR-damaged or incomplete, and therefore cannot be treated as executable source formulas without a separate researcher-defined interpretation.
- Some behaviors are only discussed conceptually, such as cost-aware re-replication, placement balance, and fault tolerance, but not specified with a complete implementation rule.
- The exact trigger policy, placement decisions, replica-count rule, provider choice, deletion logic, and objective aggregation are not source-faithful enough to reconstruct without assumptions.

This boundary is intentionally strict: the paper can support a source-faithful specification of the problem and selected concepts, but not a complete executable replication-management implementation without additional researcher-defined decisions.

---

## 28. Audit summary

### Definitely reproducible

- EIMORM is a multi-objective cloud replication strategy emphasizing availability, cost, and load balancing.
- The paper uses a heterogeneous multi-tier cloud architecture with data centers, hosts, VMs, brokers, replica catalogs, and replica managers.
- ETBDF is a recency-weighted file-identification / access-weight concept.
- EARF and the formula `ARFK(one) = RFK / (RFK + RFKold)` are explicitly stated.
- IEK is explicitly named as a cost-optimization mechanism triggered by budget pressure.
- CloudSim is stated as the simulation environment, with a VMware / XAMPP / MySQL configuration described for replication experiments.

### Partially specified

- ETBDF equation exists but is OCR-corrupted and not fully reliable.
- Block/file availability formulas exist but are damaged and ambiguous.
- Cost equations and load/energy/latency formulas are mentioned but not fully readable and not implementation-ready.
- The global replication workflow is described conceptually in two phases.
- EIMORM, DCR2S, EDCR2S, ETBDF, EARF, and IEK are referenced as related concepts but the exact subsystem hierarchy is not formalized.

### Remains unresolved

- exact trigger policy for replication
- exact replica count rule
- exact placement rule
- exact provider selection policy
- exact IEK algorithm and objective function
- exact deletion and replacement strategy
- exact objective-weight aggregation
- exact failure model and recovery procedure
- exact complexity analysis
- exact experimental workloads and numerical parameters

### Highest-risk ambiguities for later implementation

1. The ETBDF formula is the strongest mathematical ambiguity in the paper.
2. The availability formulas are partly present but not cleanly transcribed.
3. IEK does not provide a usable algorithmic specification.
4. The exact replica-count / placement decision logic is absent.
5. The multi-objective objective function and weighting method are not explicitly provided.
6. The source does not define a complete replacement or failure-recovery policy.

This specification intentionally preserves the paper’s ambiguity and does not convert EIMORM into a fully invented or generalized replication algorithm.

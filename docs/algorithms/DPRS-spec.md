# DPRS Source Specification

## 1. Source Identity

- Full paper title: "Dataset replica placement strategy under a response time constraint in the cloud"
- Authors: Xiuguo Wu and Wei Su
- Journal: International Journal of Information Technology and Management
- Volume / issue / year: Vol. 18, No. 1, 2019
- Page range: pp. 74-92
- Algorithm / strategy name used in the paper: Dataset replica placement strategy under a response time constraint; in the algorithm section, the paper also refers to the procedure as RPRC (Approximate algorithm for replica placements based on response-time constraint).
- Terminology note: the paper presents a replica placement strategy and also names the procedure RPRC in the algorithm discussion. This document treats the scientific source as DPRS as a source-level label, while preserving the paper's own algorithm name when it is explicitly used.

---

## 2. Research Problem

The paper is concerned with data-intensive cloud storage where large collections of datasets are distributed across multiple data centres and are frequently requested by users in different regions. The core problem is that a dataset request experiences a response time consisting of multiple contributors: storage access latency, transfer time, and wait time.

The paper states that dataset replicas should be placed at suitable data-centre locations to reduce user response time, while also recognizing that too many replicas are infeasible in practice. Therefore, the problem is not a general replication-management problem but a data-placement problem under a response-time constraint.

The paper's source framing is:

- cloud environment with large datasets stored in distributed data centres
- user requests may arrive from different regions
- reducing response time motivates replication
- excessive replica counts are impractical
- the key issue is to select suitable data-centre locations for replicas while respecting response-time constraints

This document distinguishes the paper's problem from a broader generic replication-management problem. The paper does not define a complete request lifecycle, failure/recovery policy, or generalized replication governance system.

---

## 3. Scope of the Proposed Strategy

The source proposes a replica placement strategy under a response-time constraint. The proposed method is based on the following sequence:

1. estimate response time,
2. model the placement problem as a graph problem,
3. construct a graph over data centres and candidate replica sites,
4. apply a transformed edge-weight model,
5. generate a minimum spanning tree using Kruskal-style logic,
6. prune redundant virtual vertices and edges,
7. output the remaining candidate sites as the replica-placement set.

The paper does not define the following as source-defined scientific behaviors:

- request-time replica selection: SOURCE-UNRESOLVED / NOT DEFINED IN SOURCE
- replica provider selection: SOURCE-UNRESOLVED / NOT DEFINED IN SOURCE
- replica creation lifecycle: SOURCE-UNRESOLVED / NOT DEFINED IN SOURCE
- replica deletion or replacement: SOURCE-UNRESOLVED / NOT DEFINED IN SOURCE
- dynamic replica-count optimization: SOURCE-UNRESOLVED / NOT DEFINED IN SOURCE
- failure handling: SOURCE-UNRESOLVED / NOT DEFINED IN SOURCE
- recovery handling: SOURCE-UNRESOLVED / NOT DEFINED IN SOURCE

The paper explicitly defines a placement optimization problem and approximate solution, not a full replication-management mechanism.

---

## 4. Source-Defined Data-Centre Model

The paper defines a data centre as a four-tuple:

(dci, spi, tsi, vsi)

Where:

- dci = data-centre identifier
- spi = average storage price of data, determined by the cloud storage service provider
- tsi = total storage space of data centre dci, with unit TB
- vsi = size of vacant space on data centre dci, meaning the extra storage capacity

The paper states that each data centre can be described in that form. This model is source-defined and is used as part of the placement formulation.

---

## 5. Source-Defined Dataset Model

The paper defines a dataset as a four-tuple:

(dm, si, sp, UF)

Where:

- dm = dataset identifier, unique in the cloud environment
- si = size of dataset
- sp = store place, sp ∈ DC
- UF = usage frequency in a certain period

The paper also describes the placement model in terms of which data centres store replicas and which do not, but it does not define a full runtime catalog lifecycle beyond the placement formulation itself.

---

## 6. Response-Time Model

The paper defines the response time of a dataset request as:

Tdi = Tw + Tw/r + Ttrsf

Where:

- Tdi = response time of a dataset request for dataset di
- Tw = wait access latency on a data centre from request arrival until the request starts to be served
- Tw/r = write/read time for dataset di
- Ttrsf = data transfer time from source data centre to destination

The paper states that the response time includes:

- data transfer time between the two data centres,
- storage access latency for serving the current request,
- wait latency before the request is served.

This decomposition is source-defined.

### 6.1 Wait Access Latency

The paper models the wait latency as an M/M/1/∞/∞ queue model.

The source states the queue interpretation as:

- first M = request arrivals frequency, determined by a Poisson process
- second M = service time, determined by an exponential distribution
- one means the number of CPU or a single server
- first ∞ means the number of permitted waiting requests is abundant
- second ∞ means the number of requests is infinite

The paper then states the average wait access latency theorem exactly as printed:

Tw = ρm / (λm − μm)

with:

ρm = λm / μm

Where:

- λm = request arrival rate
- μm = service rate per data centre
- ρm = traffic intensity or utilisation
- Tw = average wait access latency

SOURCE-INCONSISTENCY NOTE:

The printed equation appears inconsistent with the conventional stable M/M/1 formulation. This document preserves the printed equation exactly as it appears in the source paper and explicitly labels it as SOURCE-INCONSISTENT rather than silently substituting a textbook formula. Any later correction to this formula would be a researcher-defined choice, not a source-extraction fact.

### 6.2 Write/Read Time

The paper defines write/read time as proportional to the dataset size and inversely related to the hard-disk rotational speed:

Tw/r = (di.si / RS) × γ

Where:

- Tw/r = time of disk write/read for dataset di
- di.si = size of dataset di
- RS = hard disk rotational speed with unit rpm
- γ = proportional control coefficient used to adjust the proportion and unit of Tw/r

The paper gives an example:

- dataset size = 1 G
- hard disk = 5,400 rpm
- γ = 55
- write/read time is nearly ten seconds

This numerical example is source-provided and must not be treated as a universal constant unless later adopted as a project-defined configuration.

### 6.3 Transfer Time

The paper defines dataset transfer time as:

Ttrsf = (di.si / bandwidth(dcj, dck)) × ξ

Where:

- Ttrsf = single dataset transfer time
- di.si = size of dataset di
- bandwidth(dcj, dck) = network transport capacity between data centres dcj and dck
- ξ = adjustment coefficient used to adjust the proportion and unit of Ttrsf

The paper also states that when more than one path exists between two data centres, the transfer time is simplified to the minimum transfer time among all possible paths in the current study.

This is a source-defined simplification for the placement model. The paper does not define a more detailed routing algorithm.

---

## 7. Total Response Time on a Data Centre

The paper defines the total response time of one dataset di on data centre dcm as:

T_dcm = Σ (x_dcm × Tdi × η_ti × T)

The source text indicates that this is the sum of all dataset response times over a period and that the response time is estimated over a time span T.

Variables:

- T_dcm = total response time of dataset di on data centre dcm
- x_dcm ∈ {0,1} = indicator variable: x_dcm = 1 if data centre dcm stores a replica of dataset di, otherwise 0
- Tdi = one dataset response time, as defined in Definition 3
- η_ti = usage frequency during a period T
- T = time span; the paper gives one day as the example period

This formulation is source-defined, but the paper's OCR-extracted notation is somewhat noisy. The wording is internally inconsistent: the definition title refers to the total response time of one dataset on a data centre, while k is defined as the number of datasets in that data centre and the equation aggregates over those datasets. The source intent is clear: it is a total response-time expression over dataset responses and usage frequency over a time window. The document preserves this and marks the notation as SOURCE-UNRESOLVED only where the notation is not cleanly recoverable. It does not resolve or rewrite the source equation.

---

## 8. Replica Placement Model

The paper transforms the placement problem into a graph-theoretic problem in Section 4.1.

The source states the following transformation rules:

1. each data centre dci is regarded as a vertex vi
2. all vertices constitute a vertex set V
3. each connection between two data centres becomes an edge e
4. all edges constitute an edge set E
5. the transfer time between two data centres is treated as the weight of an edge, represented by f: e → Z+
6. the vertices corresponding to data centres with replicas constitute subset P, where P ⊆ V

The graph is then represented as G(V, E, f), and the problem is to find a tree T such that:

- P ⊆ VT ⊆ V
- ET ⊆ E
- minimize Σ f(e) + Σ f(v)

The source explains that this is the same as a Steiner-tree problem if the wait latency and write/read time on each data centre (vertex) are omitted. The paper then notes that Steiner tree is NP-hard and therefore the problem is also NP-hard in the response-time setting.

This is a source-defined graph model for placement optimization under response-time constraints.

---

## 9. Edge-Weight Transformation

Before applying the Kruskal-style minimum spanning tree, the paper moves vertex-based costs to adjacent edges.

The source equation is:

w′(dcp,dcq)
=
w(dcp,dcq)
+
[(Tw/r(dcp) + Tw(dcp)) / deg(dcp)]
+
[(Tw/r(dcq) + Tw(dcq)) / deg(dcq)]

Where:

- w(dcp,dcq) = original edge weight between data centres p and q
- w′(dcp,dcq) = new edge weight after assigning vertex cost to adjacent edges
- Tw/r(dcp), Tw/r(dcq) = write/read time on the two data centres
- Tw(dcp), Tw(dcq) = wait access latency on the two data centres
- deg(dcp), deg(dcq) = degree of the vertices

The source states that the main idea is to assign wait access latency and write/read time from each data centre to adjacent edges so that the placement problem can be solved by a spanning-tree approximation.

The paper also states that the degree can be obtained using an adjacency matrix and that this calculation requires O(n²) in the described adjacency-matrix implementation.

---

## 10. Replica Placement Algorithm

The paper presents two relevant algorithmic components: Algorithm 1 and Algorithm 2.

### 10.1 Algorithm 1: Move vertex weight to edges

The source states that the algorithm initializes an edge-weighted graph G′(V′, E′, f′(e)) by setting V′ = V and E′ = E, then for each edge e(vi, vj), it assigns a new edge weight using the transformed formula above.

The source parts relevant to this phase are:

- initialize edge-weighted graph
- assign the weight of each edge using the transformation formula
- set the transformed vertex/edge relation
- the degree of each vertex is computed from the adjacency matrix

The source notes the complexity of this step in terms of adjacency-matrix access.

### 10.2 Algorithm 2: Approximate algorithm for replica placements based on response-time constraint

The source presents the approximate algorithm as RPRC and states the following sequence:

1. Initialize a virtual vertex set V′ by setting vi′ = vi if and only if vi ∈ V.
2. Initialize an edge-weighted graph G″(V″, E″, f″(e)) by setting V″ = V ∪ V′.
3. The paper explicitly describes edges only between primitive/real vertices V and virtual candidate vertices V′; the edge weight represents the response time to the destination data centre.
4. The edge weight between a primitive/real vertex vi and a virtual candidate vertex vj is determined using the shortest-path response-time value in the original graph G to the corresponding destination data centre.
5. Generate a minimum spanning tree T of G″ using Kruskal's algorithm.
6. For each vertex vi′ ∈ V′, delete the vertex and adjacent edges whose degree is 1.
7. For each vertex vi ∈ V, remove vi and adjacent edges if vi′ is present.
8. For each vertex vi ∈ V, if there are multiple edges from vi to different virtual vertices vj′, delete the edge with larger weight.
9. Output the remaining candidate set as SCRD.

The paper explains that this procedure creates virtual vertices as candidate replica store locations and then constructs a spanning graph. It also explains that the source/primitive vertices are treated specially and that low-degree and redundant virtual vertices are pruned.

The paper is explicit that:

- virtual vertices are candidate replica store locations,
- the final remaining candidate set is the selected replica-placement set,
- the primitive data-centre vertices remain relevant as the real data centres,
- redundant candidates and larger-weight redundant edges are removed.

This is source-defined algorithmic structure and should not be simplified into a different optimization formulation.

---

## 11. Response-Time Constraint

The paper frames the problem as a placement strategy under a response-time constraint. The algorithm is described as solving the problem under a response-time constraint using minimum spanning tree / approximate methods.

The source example analysis states that the upper limit of the response time in a single request is:

T_upper = 10 s

Important source-fidelity requirement:

- T_upper is part of the response-time constraint used by the paper's analysis;
- T_upper = 10 s is the value used in the paper's analytical/evaluation example;
- 10 s must not be treated as a universal constant for all experiments.

The paper uses this value in the example evaluation and comparison of replica-placement strategies. The wording is scenario-based and evaluation-oriented, not presented as a universally hard-coded runtime rule for all situations.

---

## 12. Complexity

The paper reports the following complexity statements:

- Algorithm 1: one loop over the edges, but degree calculation using adjacency matrix requires O(n²)
- Kruskal-based minimum spanning tree: polynomial time, and the paper reports the algorithmic complexity as O(n²)
- additional pruning and removal steps: O(n)
- total complexity of RPRC / Algorithm 2: reported by the paper as O(n²)

These are SOURCE-REPORTED COMPLEXITY statements. They are not implementation-independent complexity guarantees for all possible software designs.

---

## 13. Simulation / Evaluation Configuration

The paper provides some explicit simulation/evaluation details. This section records only what is explicitly stated in the source and does not merge them with project-wide simulator assumptions.

A. Section 5.2 analytical example:

- 8 data centres
- T = 24 hours
- T_upper = 10 s

This analytical example is separate from the broader simulation environment and does not imply that every simulation lasted 24 hours.

B. Section 5.3 simulation environment:

- SwinDew-C
- 10 servers
- 10 high-end PCs
- VMware
- Hadoop
- Table 3 hardware/software environment
- datasets ranging from 1 G to 2 G

The paper also states that tasks are scheduled and associated with datasets in the cloud. These are source-expressed simulation parameters and should be treated as experimental conditions, not general algorithm requirements.

---

## 14. Evaluation Metrics Reported by the Paper

The paper reports the following broad evaluation logic:

- compare response time under different replica-placement strategies
- compare the number of replicas required to satisfy the response-time threshold
- compare the total response time and transfer time under workload variation
- report the final replica-placement set and corresponding data centres
- report average response time as a source-reported response-time measure
- report maximum response time as a source-reported response-time measure

The paper does not present a general-purpose metric framework for all future algorithms beyond these measured quantities. The source evaluation is focused on response time and replica degree / placement set quality as observed in the paper.

This document distinguishes the paper's own source-reported response-time measures (average response time, maximum response time) from metrics computed later in a common simulator for the broader project.

---

## 15. Source-Defined Behaviour vs Undefined Behaviour

| Item | Status | Evidence / Note |
|------|--------|-----------------|
| Response-time estimation | SOURCE-DEFINED | Explicitly defined as Tdi = Tw + Tw/r + Ttrsf |
| Replica placement | SOURCE-DEFINED | Explicit graph model and Kruskal-based placement procedure |
| Steiner-tree formulation | SOURCE-DEFINED | The paper states the placement problem is similar to a Steiner-tree problem |
| Kruskal-based approximation | SOURCE-DEFINED | The paper explicitly describes the approximate algorithm based on Kruskal minimum spanning tree |
| Request-time replica selection | NOT DEFINED | No source-defined rule is given |
| Provider selection | NOT DEFINED | No source-defined rule is given |
| Replica deletion / replacement | NOT DEFINED | No source-defined policy is given |
| Dynamic replica count | NOT DEFINED | No source-defined optimization of replica count is stated |
| Failure handling | NOT DEFINED | No source-defined failure policy is stated |
| Recovery handling | NOT DEFINED | No source-defined recovery policy is stated |
| Storage-feasibility policy | NOT DEFINED unless explicitly stated | The paper describes storage attributes but not a DPRS-specific enforcement rule |
| Tie-breaking | NOT DEFINED unless explicitly stated | No tie rule given in the source |

---

## 16. Source Inconsistencies and Ambiguities

This section records issues the paper presents that must remain explicit rather than silently repaired.

### 16.1 Wait-latency equation

The paper prints the average wait-access latency equation as:

Tw = ρm / (λm − μm)

with ρm = λm / μm.

This is SOURCE-INCONSISTENT with the conventional stable M/M/1 formulation. The paper's printed equation is preserved exactly as source text; it is not silently replaced by a textbook formula.

### 16.2 Total response-time equation

The paper's notation around total response time is OCR-sensitive and partially fragmented. The decomposition Tdi = Tw + Tw/r + Ttrsf is clearer and source-defined, but the broader aggregate expression over data centres and time periods is less cleanly recoverable. This is SOURCE-UNRESOLVED in notation detail if a clean symbolic expression is needed for later implementation.

### 16.3 Notation around Tw and Tw/r

The paper uses Tw and Tw/r in adjacent contexts. OCR and formatting make the distinction between wait latency and write/read time easy to confuse. The source definitions are clear enough to separate the two concepts, but the notation requires careful source-aware handling.

### 16.4 T_upper usage

The paper uses T_upper = 10 s in the example evaluation scenario, but it does not present this as a universal algorithm parameter. This is a source-defined scenario value, not necessarily a universal DPRS requirement.

### 16.5 Virtual vertices and candidate sites

The paper uses virtual vertices as candidate replica locations and later removes some of them using degree-based pruning. The exact intended semantics of the final candidate set are clear in the algorithm discussion but must remain source-faithful and not be replaced by a different conceptual model.

### 16.6 Complexity notation

The paper reports O(n²) in the algorithm discussion for the key procedures and also mentions O(n) for some substeps. This is source-reported complexity and must not be replaced by a later implementation-specific complexity claim without explicit labeling.

---

## 17. Strict Source-Fidelity Rules

1. DPRS-spec.md is the scientific source-of-truth extraction.
2. Missing source details must remain explicitly unresolved.
3. No simulator behavior may be presented as DPRS scientific behavior.
4. No additional optimization objectives may be invented.
5. No request-time replication lifecycle may be invented.
6. No failure or recovery policy may be invented.
7. No storage policy may be invented unless explicitly supported by the paper.
8. Printed equations must be preserved even if they appear inconsistent; inconsistencies must be flagged.
9. Experimental parameters must not automatically become universal algorithm parameters.
10. Implementation decisions belong in DPRS-implementation-contract.md, not here.

---

## Final Status

The following matters are now confirmed from the source paper:

- The paper is a response-time-constrained replica placement strategy.
- The graph model, virtual vertices, Kruskal minimum spanning tree, pruning, and output set are source-defined.
- The key response-time decomposition is source-defined.
- The wait-latency equation is preserved exactly as printed, with a recorded SOURCE-INCONSISTENCY note.
- The edge-weight transformation is source-defined and preserved as printed.
- The source does not define request-time provider selection, replica lifecycle actions, failure/recovery, or dynamic replica-count logic.

The following items remain SOURCE-UNRESOLVED or SOURCE-INCONSISTENT:

- the printed wait-latency equation is SOURCE-INCONSISTENT but preserved as printed
- the aggregate total response-time notation is partly ambiguous and should remain source-aware
- the role of T_upper beyond the reported example evaluation remains source-ambiguous
- request-time replica selection, provider selection, storage enforcement, and lifecycle behaviors remain source-undefined
- tie-breaking remains undefined unless later specified outside the source

This DPRS-spec.md is ready to be treated as a frozen scientific extraction of the paper, as long as all unresolved and inconsistent material is kept explicit and no implementation behavior is inferred from it.

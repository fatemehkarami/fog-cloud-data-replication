# Comparison Researcher Decisions

## 1. Purpose

This document records the researcher-defined decisions required to transform the common comparison architecture into an executable and reproducible five-method experiment.

This file is not an algorithm specification.
This file is not an implementation.
This file does not define missing algorithm behavior for any source paper.

Its role is to preserve the boundary between:

- SOURCE_DEFINED: behavior specified by the corresponding paper
- RESEARCHER_DEFINED: experimental choices required because the paper or common architecture does not fully specify them
- SIMULATOR_DEFINED: execution mechanics of the common simulation environment
- UNRESOLVED: not sufficiently specified yet

The comparison-level decisions in this file are required before implementation can proceed. Their status is recorded explicitly; decisions not yet selected remain OPEN.

---

## 2. Scope

The comparison scope is fixed as exactly five methods:

1. Proposed
2. HRS — Hybrid Replication Strategy
3. DPRS
4. OGSA
5. EIMORM

Canonical naming constraints:
- HRS is the canonical acronym for Hybrid Replication Strategy.
- HSR is not a separate method and is not a final roster entry.
- HER and APRS are obsolete names and are not final roster entries.
- Internal compatibility aliases, if ever required, must resolve to one of these five method identities and must not create an additional experimental method.

This file does not add other methods.
This file does not remove any of these methods.
This file does not alter the scientific scope of the method-specific papers.

If repository naming is inconsistent, that is a consistency issue to be documented, not a reason to change the research scope.

---

## 3. Decision Status Model

The status model used throughout this document is:

- OPEN
- DECIDED
- FROZEN
- BLOCKED

At creation time, all genuine researcher decisions are OPEN.
No numerical choice, statistical method, seed value, topology value, or workload value is selected in this document.

---

## 4. Source / Researcher / Simulator Boundary

### SOURCE_DEFINED
Behavior explicitly specified by the corresponding paper for a method.

Examples:
- a source-defined objective function
- a source-defined decision variable
- a source-defined replica-selection concept
- a source-defined optimizer equation

### RESEARCHER_DEFINED
Experimental choices required because the paper or the common architecture does not fully specify the behavior.

Examples:
- common workload generation policy
- common topology choice
- random seed policy
- repeated-run protocol
- comparison metric operational definition
- common result schema
- statistical summary protocol

### SIMULATOR_DEFINED
Execution mechanics of the common simulation environment.

Examples:
- event scheduling
- storage accounting
- request processing
- topology state mutation
- metrics recording
- result export

### UNRESOLVED
A fact, rule, or boundary that has not yet been specified sufficiently for implementation.

Examples:
- exact common workload generator
- exact termination policy
- exact result schema
- exact evaluation metric formula if the source is incomplete

This file documents only researcher-level decisions required for implementation readiness. It does not convert unresolved or simulator-defined behavior into source behavior.

---

## 5. Decision Dependency Map

The following dependency structure represents the order in which comparison-level decisions must eventually be resolved.

This map is a researcher decision map only; it is not a source-defined scientific dependency map.

- Common experimental environment
  - topology
  - site/node/resource model
  - storage and network assumptions
  - initial state
  - failure model baseline
  - simulation horizon
  - termination conditions

- Dataset and workload definition
  - file count and distribution
  - request rate and access patterns
  - workload scenarios
  - scenario generation

- Randomness and reproducibility policy
  - seed policy
  - independent runs
  - run count
  - replication of stochastic conditions

- Common evaluation metric definitions
  - metric operational meaning
  - raw measurement rules
  - metric aggregation rules

- Result schema and statistical protocol
  - raw results
  - run summaries
  - aggregated statistics
  - confidence/significance handling

- Visualization protocol
  - plot composition
  - display scaling
  - normalization boundary

- Experiment matrix
  - method × workload × topology × scenario × run

- Final fairness review
  - common conditions kept common
  - algorithm-specific differences preserved

Important rule:
These dependencies are not a license to introduce algorithmic assumptions. They are only the order in which comparison decisions must be made.

---

## 6. Researcher Decisions

### CMP-RD-001 — Five-Method Roster and Naming Consistency

Status: DECIDED

Purpose:
Ensure the five-method comparison scope is represented consistently across the comparison layer.

Why this decision is required:
The architecture and project materials name multiple methods, but consistency across the final experiment must be enforced before implementation.

Current evidence:
The repository's authoritative comparison and architecture documents support a five-method roster. The runtime registry and concrete adapters use the identities Proposed, HRS, DPRS, OGSA, and EIMORM.

Researcher decision:
The final comparison roster is exactly:

1. Proposed
2. HRS — Hybrid Replication Strategy
3. DPRS
4. OGSA
5. EIMORM

HRS is the canonical acronym. HSR must not be treated as a separate method. HER and APRS are obsolete and must not appear in the final comparison roster. Any internal compatibility alias must map to one of the five canonical identities and must not create another algorithm or experimental method.

Dependencies:
None beyond the comparison design baseline.

Affected methods:
- Proposed Method / Proposed NSGA-III
- HRS (canonical source name; HRS is a repository alias)
- DPRS
- EIMORM
- OGSA

Source boundary:
Source-defined names and paper identities remain unchanged.

Simulator boundary:
The common simulator uses the final method roster as a comparison configuration only.

Constraints / guardrails:
- Do not add methods.
- Do not remove methods.
- Do not rename scientific method identities for convenience.

Decision:
DECIDED — FINAL FIVE-METHOD ROSTER

---

### CMP-RD-002 — Common Experimental Environment

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Define the shared experimental environment used by all five methods while preserving the distinction between common infrastructure and method-specific decision logic.

Why this decision is required:
The common architecture requires identical external conditions across methods, but it does not define the final concrete environment in sufficient detail for implementation. A fair comparison requires common execution conditions without collapsing algorithmic differences into a common method behavior.

Current evidence:
The repository architecture and domain-model documents explicitly state that the following are common simulation concerns:
- topology
- node/resource state
- storage and network assumptions
- initial state
- file and replica catalog
- request/workload generation
- failure-event infrastructure
- simulation horizon and termination policy
- seed/repetition regime
- metric collection and reporting

These are documented as common-simulator or experiment-design concerns in [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md), [docs/06-common-domain-model.md](docs/06-common-domain-model.md), and [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md).

Researcher decision:
The shared experimental environment specification is resolved below, while the line between common infrastructure and method-specific algorithm behavior remains mandatory.

#### CMP-RD-002 decision worksheet

This worksheet makes the pending choice explicit without selecting numerical values or importing one paper's experimental parameters into the common environment. For every item, source support means that a paper or project specification describes the concept; it does not mean that the source supplies a common value for all five methods.

##### A. Topology

| Item | Explicit source/specification support | Not specified / unresolved | Researcher choice required | Common across five methods | Fairness impact | Reproducibility impact |
|---|---|---|---|---|---|---|
| Number of data, edge, and cloud nodes | Papers/specifications describe data centres, data nodes, sites, providers, or hierarchical tiers; the common architecture requires a shared node population. | No common node counts or final role inventory are established. | Select node counts and role assignments, or document an externally supplied topology. | Yes. | High: changes capacity, placement options, and failure exposure. | High: record node IDs, roles, and configuration identity. |
| Node connectivity | Source models refer to network relationships, candidate sites, or data-centre connectivity. | No single complete cross-method connectivity graph is specified. | Select which node/site pairs are connected and whether links are directed or undirected. | Yes. | High: changes reachability and transfer paths. | High: serialize the graph and link identities. |
| Network topology | Individual source scenarios may depict cloud/data-centre or hierarchical arrangements. | No common topology structure is specified; paper figures are not a common experimental mandate. | Select the common topology structure. | Yes. | High. | High: record topology/configuration ID and graph definition. |
| Heterogeneous vs homogeneous resources | HRS and comparison materials explicitly discuss heterogeneous environments; other papers describe differing node/data-centre capabilities. | No common heterogeneity profile or equivalence rule is fixed. | Select a common heterogeneous or homogeneous resource model. | Yes. | High: affects all algorithms' feasible decisions. | High: record per-node resource profiles. |
| Connectivity representation | Domain model provides sites, nodes, and network links as shared entities. | No final representation policy is selected for adjacency, link objects, or site-to-node mapping. | Select the serialized representation used by the simulator. | Yes. | Medium to high. | High: representation must round-trip exactly. |

##### B. Compute resources

| Item | Explicit source/specification support | Not specified / unresolved | Researcher choice required | Common across five methods | Fairness impact | Reproducibility impact |
|---|---|---|---|---|---|---|
| CPU capacity and model | Papers refer to processing capability, CPU speed, VM/task computation, or node performance. | No common CPU capacities, units, or model are fixed. | Select CPU representation and capacities. | Yes. | High: affects service time, load, and placement feasibility. | High: record units and per-node values. |
| Memory capacity | Cloud/VM and node-resource concepts are present in the specifications. | No common memory capacities or accounting rule are fixed. | Select memory representation and capacities. | Yes. | Medium to high. | High: record units and per-node values. |
| Processing capacity | DPRS and HRS source descriptions use performance/load-related concepts; common domain model permits processing attributes. | No common processing-rate metric or conversion is fixed. | Select the processing-capacity metric and conversion rule. | Yes. | High. | High: record metric definition and values. |
| VM/host representation | HRS explicitly models providers/VMs; common domain model includes VMs. | No common VM-to-host inventory or mapping is specified. | Select whether and how VM/host entities are represented for the shared environment. | Yes for the environment; use remains method-specific where required. | Medium to high. | High: record mappings and configuration identity. |

##### C. Storage

| Item | Explicit source/specification support | Not specified / unresolved | Researcher choice required | Common across five methods | Fairness impact | Reproducibility impact |
|---|---|---|---|---|---|---|
| Per-node storage capacity | Source papers discuss restricted or available storage and data-centre storage capacity. | No common capacity values or units are fixed. | Select capacity representation and per-node capacities. | Yes. | High: directly controls replication and replacement pressure. | High: record values and units. |
| Initial storage utilization | Sources discuss load/storage state, but do not provide a common initial utilization profile. | Initial used capacity is not fixed. | Select initial utilization or derive it from the initial file/replica catalog. | Yes. | High. | High: record the realized initial state. |
| Available capacity | Domain model defines storage used/capacity and available storage behavior. | No common initial availability rule or reservation policy is selected. | Select how available capacity is calculated and serialized. | Yes. | High. | High: record capacity, used space, and derivation rule. |

##### D. Network

| Item | Explicit source/specification support | Not specified / unresolved | Researcher choice required | Common across five methods | Fairness impact | Reproducibility impact |
|---|---|---|---|---|---|---|
| Bandwidth | HRS, DPRS, and the common domain model identify bandwidth or transfer-performance concepts. | No common bandwidth values, units, or link assignment are fixed. | Select per-link or per-node bandwidth representation and values. | Yes. | High: affects transfer time and response metrics. | High: record values, units, and link mapping. |
| Latency | Sources and domain model identify latency/response-time concepts. | No common latency values, units, or propagation model are fixed. | Select latency representation and values. | Yes. | High. | High: record values, units, and calculation rule. |
| Transfer characteristics | Sources mention transfer time, packet/network behavior, or response-time components. | No common queueing, contention, loss, serialization, or transfer model is fixed. | Select the externally applied transfer model. | Yes; method-specific objectives must not alter it. | High. | High: record model version and parameters. |

##### E. Initial scenario state

| Item | Explicit source/specification support | Not specified / unresolved | Researcher choice required | Common across five methods | Fairness impact | Reproducibility impact |
|---|---|---|---|---|---|---|
| Files and file metadata | All methods operate on files/data objects; the domain model defines a shared file catalog. | File count, IDs, sizes, attributes, and distribution are not fixed here. | Select the file catalog and serialization. | Yes. | High. | High: record catalog/configuration identity. |
| Initial replicas and primary copies | Sources discuss replicas; HRS explicitly requires random initial primary-copy placement. | Common initial replica count, full placement, and primary-copy policy are not otherwise fixed. | Select the common initial replica catalog while preserving CMP-RD-002-HRS-001. | Yes for the realized matched state. | High. | High: record the complete replica mapping. |
| Node health and reachability | Common architecture/domain model represents health, reachability, and external failure/recovery events. | Initial health/reachability values are not fixed. | Select the initial health state and encode external event inputs. | Yes. | High. | High: record initial state and event trace identity. |
| Initial load | Sources use load/performance concepts; common runtime tracks simulation state. | No common initial load profile or load-generation rule is fixed. | Select initial load representation and values. | Yes. | High. | High: record per-node load state and derivation. |
| Initial resource utilization | Storage utilization is discussed; broader CPU, memory, and network utilization are not jointly fixed. | No common utilization profile is specified. | Select which utilization fields exist and their initial values or derivation. | Yes. | High. | High: record realized utilization state. |

##### F. Scenario identity

| Item | Explicit source/specification support | Not specified / unresolved | Researcher choice required | Common across five methods | Fairness impact | Reproducibility impact |
|---|---|---|---|---|---|---|
| Scenario ID | Runtime `Scenario` and replay abstractions require a scenario identity. | Naming format and lifecycle are not fixed. | Select the scenario identifier policy. | Yes. | Medium: supports matched-run association. | High. |
| Configuration ID | Run provenance includes configuration identity; architecture requires reproducible configuration tracking. | Final configuration schema and naming policy are not fixed. | Select the configuration identity policy covering topology/resources/storage/network/state. | Yes. | Medium to high. | High. |
| Reproducibility metadata | Runtime provenance supports experiment/scenario/run/method IDs, seed identity, random-stream identity, configuration identity, and trace metadata. | No final required metadata schema or seed/repetition policy is selected. | Select the metadata fields and serialization format; do not invent seed values here. | Common scenario metadata must be common; algorithm-local metadata may remain method-specific. | High. | High: required to reproduce and audit matched runs. |

Worksheet boundary:
- Common experimental environment: topology, resource environment, storage environment, network environment, initial scenario state, externally supplied workload, and externally supplied failure/recovery events.
- Algorithm-specific parameters: optimizer population, generations, weights, thresholds, fuzzy parameters, OIS parameters, IEK parameters, GSA parameters, DPRS-specific parameters, and replication policies.
- Paper-specific experimental parameters remain paper-specific unless a later explicit researcher decision promotes a parameter into the common environment. No such promotion is made here.

Worksheet status:
RESOLVED / RESEARCHER-DECIDED — selected values and their classifications are recorded below.

#### CMP-RD-002 Researcher Decisions

The following environment is the common external control for matched execution of all five methods. These values are researcher decisions, not algorithm definitions and not claims that any one paper defines the complete common environment.

##### Selected common environment

| Decision ID | Parameter | Chosen value | Unit / representation | Classification | Source evidence | Research rationale | Fairness rationale | Implementation impact | Dependency |
|---|---|---|---|---|---|---|---|---|---|
| CMP-RD-002-T01 | Sites/data centres | 4 stable sites: `site-01` through `site-04` | Site IDs | RESEARCHER-DECIDED | Sources describe multiple data centres/sites and HRS random placement across sites; no common count is specified. | Four sites expose locality and cross-site placement effects while remaining practical for repeated matched runs. | Every method sees the same site set and locality structure. | Populate `Scenario.sites`; preserve stable IDs. | CMP-RD-003 workload; CMP-RD-004 replay. |
| CMP-RD-002-T02 | Data nodes and roles | 12 nodes, 3 per site: `edge`, `data`, and `cloud` | 4 x 3 node inventory; IDs `site-XX-edge`, `site-XX-data`, `site-XX-cloud` | RESEARCHER-DECIDED | Sources discuss data nodes, providers, VMs, and tiers, but use incompatible scales. | Twelve nodes are large enough to expose placement, load, storage, and network trade-offs without using the eight-node example as a universal requirement. | Roles and identities are common; no method receives an extra node class. | Populate `Scenario.nodes` and site membership. | CMP-RD-003; CMP-RD-004. |
| CMP-RD-002-T03 | Connectivity/topology | Sparse hierarchical graph: within each site, `edge` and `cloud` connect bidirectionally to the site `data` gateway; the four `data` gateways connect as a directed complete site-level mesh | 16 intra-site directed links plus 12 inter-site directed links = 28 directed links | RESEARCHER-DECIDED (CORRECTED IN REVIEW) | Sources and domain model require network/data-centre relationships; no common graph is specified. | A sparse gateway topology preserves locality and meaningful graph/path structure while remaining small and fully reachable. | DPRS, HRS, and all other methods receive the same graph and reachability information; no method receives a private edge. | Create 28 directed links and route cross-site traffic through data gateways. | CMP-RD-003 workload; CMP-RD-005 failure link policy. |
| CMP-RD-002-T04 | Heterogeneity | Heterogeneous by node role; the role profile is repeated at each site | Role metadata plus explicit capacities | RESEARCHER-DECIDED | HRS and comparison materials describe heterogeneous environments; other sources do not define a common profile. | Repeating three role classes isolates heterogeneity from site identity and makes comparisons interpretable. | Heterogeneity is an external condition applied identically to all methods. | Add resource metadata to node configuration; do not add algorithm objectives. | Method contracts consume only source-relevant fields. |
| CMP-RD-002-C01 | CPU capacity | `edge`: 4 vCPU / 4,000 MIPS; `data`: 8 vCPU / 8,000 MIPS; `cloud`: 16 vCPU / 16,000 MIPS | vCPU and MIPS; MIPS is 1,000 per vCPU | RESEARCHER-DECIDED | HRS uses CPU process capability and DPRS/other sources discuss processing performance; no common value is supplied. | Three proportional capacity classes provide measurable processing heterogeneity without importing a paper-specific machine profile. | All methods see identical capacity and initial utilization; CPU is not a new algorithm objective. | Requires future generic node resource fields or configuration attributes. | CMP-RD-002 initial utilization; CMP-RD-006 horizon. |
| CMP-RD-002-C02 | Memory capacity | `edge`: 8 GiB; `data`: 16 GiB; `cloud`: 32 GiB | GiB per node | RESEARCHER-DECIDED | Cloud/VM resources are source-supported, but no common memory values are specified. | Memory scales with the CPU classes and provides a common execution constraint without changing algorithms. | Same memory limits and utilization apply to every method. | Requires future generic memory fields; no adapter logic change. | CMP-RD-006 horizon; method execution. |
| CMP-RD-002-C03 | Initial CPU/memory utilization | 40% CPU and 40% memory on every node | Fraction of declared capacity; `0.40` | RESEARCHER-DECIDED | Sources discuss load/resource state but do not specify a common initial profile. | A controlled moderate starting load prevents an unrealistically empty system while leaving headroom for workload effects. | The identical relative state prevents one method from receiving more initial capacity. | Initialize common state; do not infer algorithm behavior from it. | CMP-RD-003 workload; CMP-RD-005 failures. |
| CMP-RD-002-S01 | Storage capacity | `edge`: 80 GiB; `data`: 160 GiB; `cloud`: 320 GiB per node | GiB per node | RESEARCHER-DECIDED | Sources discuss restricted/available storage but provide incompatible scenario values. | Role-scaled capacities create meaningful storage pressure while allowing a valid initial catalog and later replication activity. | All methods face the same capacity constraint and storage accounting. | Populate `Node.storage_capacity`; validate usage against capacity. | CMP-RD-003 dataset; method-specific replication. |
| CMP-RD-002-S02 | Initial storage utilization | Derived from the initial replica catalog; no independent percentage override | Sum of `File.size` for valid replicas on each node | COMMON-SIMULATOR REQUIREMENT | The domain model and runtime already account for storage used by replicas; sources do not define a common initial percentage. | Derivation prevents contradictory hand-entered utilization and catalog state. | Every method starts from the same realized storage state. | Initialize `storage_used` from the frozen catalog and release it immediately on deletion. | CMP-RD-002-E01; CMP-RD-003. |
| CMP-RD-002-N01 | Bandwidth | Same-site: 10 Gbps; cross-site: 2.5 Gbps, symmetric but represented as two directed links | Gbps per directed link | RESEARCHER-DECIDED | HRS and DPRS explicitly use bandwidth; other sources discuss transfer/network performance. | Locality-sensitive bandwidth exposes transfer trade-offs without copying a paper-specific network. | All methods use the same link capacities. | Populate `NetworkLink.bandwidth`; preserve units. | CMP-RD-003 workload; CMP-RD-005 failures. |
| CMP-RD-002-N02 | Latency | Same-site: 1 ms; cross-site: 20 ms | Milliseconds per directed link | RESEARCHER-DECIDED | Sources discuss latency/response-time components but do not agree on a common value. | The contrast makes site locality observable and remains computationally simple. | Identical link delays prevent method-specific network advantages. | Populate `NetworkLink.latency`; preserve units. | CMP-RD-003 workload; CMP-RD-006 horizon. |
| CMP-RD-002-N03 | Link availability and sharing | All links initially available; active transfers share a link's bandwidth equally; latency is additive per traversed link; no loss model is selected | `NetworkLink.available=True`; equal-share fluid model | COMMON-SIMULATOR REQUIREMENT | Domain model represents link availability; papers do not define one common contention/loss model. | Equal sharing is deterministic and avoids adding an unapproved optimizer or queueing policy. | The same external transfer semantics apply to all methods. | Requires generic transfer accounting; dynamic link failures remain CMP-RD-005. | CMP-RD-005 failures; CMP-RD-006 horizon. |
| CMP-RD-002-E01 | File catalog | 100 files: 34 small, 33 medium, 33 large. Exact IDs are `file-001`–`file-017` at 1 GiB, `file-018`–`file-034` at 2 GiB, `file-035`–`file-045` at 3 GiB, `file-046`–`file-056` at 4 GiB, `file-057`–`file-067` at 5 GiB, `file-068`–`file-078` at 6 GiB, `file-079`–`file-089` at 7 GiB, and `file-090`–`file-100` at 8 GiB | GiB; stable IDs `file-001` through `file-100`; canonical bucket ordering defines the manifest | RESEARCHER-DECIDED (CORRECTED IN REVIEW) | All methods operate on files; sources mention file size/type/access concepts but no common catalog. | One hundred files and three size classes expose storage and popularity interactions without making repeated runs impractical; exact ID-to-size mapping makes storage demand reproducible. | The exact catalog is frozen before any method executes. | Populate `Scenario.files`; file sizes are required for storage accounting. | CMP-RD-003 workload. |
| CMP-RD-002-E02 | Initial primary copies | Exactly one primary per file; the primary target is the site's `data` node; site assignment is realized once at scenario creation using the preserved HRS rule and conditioned on valid common capacity | Explicit file-to-primary-node mapping; four primary candidate nodes | CMP-RD-002-HRS-001 plus RESEARCHER-DECIDED common validity rule | HRS explicitly requires random primary placement across sites; other papers do not define a common initial placement. | One primary gives an auditable baseline; mapping sites to data nodes makes the site-level source rule executable without adding method-specific placement logic. | The realized mapping is frozen and replayed identically across all five methods. | Requires explicit primary mapping and initial-state validation. | CMP-RD-002-HRS-001; CMP-RD-004 replay. |
| CMP-RD-002-E03 | Initial additional replicas | Exactly 50 files receive one additional replica: 9 files of 1 GiB, 8 of 2 GiB, 6 of 3 GiB, 6 of 4 GiB, 5 of 5 GiB, 6 of 6 GiB, 5 of 7 GiB, and 5 of 8 GiB. Within each exact-size bucket, select files by ascending SHA-256 of `cmp-rd-002-common-env-v1|file-id|additional-replica` until that exact target is met; all other files have only their primary | Initial replica count distribution: 1 or 2 valid replicas per file | RESEARCHER-DECIDED (CORRECTED IN REVIEW) | Sources discuss replicas but do not define a common initial count or placement. | Stratified hash selection avoids arbitrary ID parity, balances size classes, is independent of workload ordering, and is reproducible. | The same catalog and mapping are supplied to all methods. | Populate `Scenario.replicas`; no method-specific lifecycle is implied. | CMP-RD-003 workload; method execution. |
| CMP-RD-002-E04 | Initial replica placement | Additional replicas use a canonical deterministic round-robin over stable node IDs, skipping the primary node and candidates that would violate capacity; the realized result is frozen | Frozen mapping in the scenario manifest | RESEARCHER-DECIDED | No source defines a common cross-method initial secondary-placement policy. | A deterministic scenario-construction policy avoids giving one algorithm control of the starting comparison state while preserving capacity validity. | All methods receive the same realized placement. | Requires deterministic manifest generation and validation. | CMP-RD-004 replay. |
| CMP-RD-002-U01 | Initial health | All 12 nodes and all links start healthy/available and reachable; no failed node exists initially | Boolean node/link state | RESEARCHER-DECIDED | Common runtime supports health/reachability; papers do not define a common initial failure state. | A healthy baseline isolates replication behavior; dynamic failures remain CMP-RD-005. | Every method starts from the same external health state. | Validate initial health and preserve `NetworkLink.available`. | CMP-RD-005. |
| CMP-RD-002-I01 | Scenario/configuration identity | Scenario ID identifies the realized manifest; configuration ID is `cmp-rd-002-common-env-v1`; replay ID is the SHA-256 digest of the canonical manifest excluding method-local configuration and results | Stable strings plus canonical-manifest digest | RESEARCHER-DECIDED | Runtime/provenance supports scenario and configuration identities; no final naming/digest rule exists. | Content identity detects accidental changes to the matched scenario. | A matched run must reference the same scenario/configuration/replay IDs for all methods. | Store IDs in scenario/replay metadata and run provenance. | CMP-RD-004 seed/stream policy; CMP-RD-008 result schema. |
| CMP-RD-002-I02 | Seed/random-stream identity | Seed values and repetition schedule remain owned by CMP-RD-004; the manifest records `scenario_seed_identity` and `scenario_random_stream_identity` supplied by that decision | Required metadata fields; no seed value selected here | COMMON-SIMULATOR REQUIREMENT | Sources identify randomness for HRS/OGSA but do not provide a common seed protocol. | Preserves CMP-RD-002-HRS-001 without prematurely resolving CMP-RD-004. | Common scenario identities are replayed; algorithm-local streams remain separate. | Extend manifest/provenance linkage when CMP-RD-004 is resolved. | CMP-RD-004. |

##### Storage and initial-state rules

- Primary and additional replicas both consume `File.size` storage.
- Deleting a valid replica immediately releases its file size from the owning node.
- Initial storage usage is derived from the frozen replica catalog; it is never independently invented.
- Initial catalog construction rejects duplicate file/node replicas, invalid references, and capacity overflow.
- Initial primary placement is sampled once at scenario creation under the existing CMP-RD-002-HRS-001 interpretation and never regenerated per method.
- The initial catalog is capacity-valid but is not tuned after observing method results.

##### Source-Derived vs Researcher-Decided

Source-derived facts are limited to the existence of sites/data nodes, heterogeneous or resource-related concepts, bandwidth/latency/transfer concepts, files/replicas, and HRS random primary-copy placement. OGSA's source-reported equal objective weights, HRS formula terms, DPRS response-time threshold examples, and other paper-specific parameters remain method-specific and are not imported into this environment.

All concrete counts, capacities, sizes, utilization values, topology structure, link model, initial replica distribution, initial secondary placement policy, and identity/digest policy above are RESEARCHER-DECIDED or COMMON-SIMULATOR REQUIREMENTS. They are not source-defined algorithm parameters.

##### Fairness and reproducibility rationale

- The same 4-site/12-node graph, resource profile, storage capacity, network model, file catalog, replica catalog, health state, and manifest identity are supplied to every method in a matched run.
- Heterogeneity is repeated by node role rather than assigned to a particular method or site, so no method receives privileged resources.
- Storage pressure is present in the common environment and is controlled by the frozen catalog and capacities, not by method-specific settings.
- The initial replica catalog and HRS primary mapping are realized before method execution and deep-cloned for each method.
- The complete manifest digest, scenario/configuration IDs, and seed/stream identity fields provide an auditable replay boundary.
- The chosen environment is computationally manageable: 12 nodes, 100 files, and a 28-link sparse gateway graph are small enough for repeated five-method matched runs while exposing locality, heterogeneity, storage, and placement trade-offs.

#### CMP-RD-002 Scientific Feasibility Review

This review was performed after resolution and records the corrections required before the decision can be safely frozen.

##### Storage feasibility calculations

Exact primary volume:

- Small: 17 x 1 GiB + 17 x 2 GiB = 51 GiB
- Medium: 11 x 3 GiB + 11 x 4 GiB + 11 x 5 GiB = 132 GiB
- Large: 11 x 6 GiB + 11 x 7 GiB + 11 x 8 GiB = 231 GiB
- Total primary volume = **414 GiB**

The corrected stratified additional-replica selection contains 17 small files, 17 medium files, and 16 large files. The exact selected size buckets are 9 x 1 GiB + 8 x 2 GiB, 6 x 3 GiB + 6 x 4 GiB + 5 x 5 GiB, and 6 x 6 GiB + 5 x 7 GiB + 5 x 8 GiB:

- Additional-replica volume = 25 + 67 + 111 = **203 GiB**
- Total initial storage demand = 414 + 203 = **617 GiB**

Available storage:

- Edge: 4 x 80 GiB = 320 GiB
- Data: 4 x 160 GiB = 640 GiB
- Cloud: 4 x 320 GiB = 1,280 GiB
- Total available storage = **2,240 GiB**
- Per-site capacity = 80 + 160 + 320 = **560 GiB**

If values vary anywhere within the selected class ranges while class counts remain fixed, the bounds are:

- Primary minimum/maximum = 34 x 1 + 33 x 3 + 33 x 6 = **331 GiB**; 34 x 2 + 33 x 5 + 33 x 8 = **497 GiB**.
- Additional-replica minimum/maximum under the 17/17/16 class allocation = 17 x 1 + 17 x 3 + 16 x 6 = **164 GiB**; 17 x 2 + 17 x 5 + 16 x 8 = **247 GiB**.
- Total initial demand minimum/maximum = **495–744 GiB**.

Unconstrained placement is not always feasible: all exact initial demand on one node would be 617 GiB, exceeding the largest 320 GiB node; all demand on one site would also exceed its 560 GiB capacity. This is a generic placement-validity issue, not a reason to let a method regenerate state. The corrected scenario generator must sample the HRS primary mapping and place additional replicas only from capacity-valid assignments. A valid assignment always exists because primary demand is at most 497 GiB against 640 GiB of aggregate data-node capacity, and additional demand is at most 247 GiB against 1,600 GiB of aggregate edge/cloud capacity. Any invalid random realization is rejected and resampled before the frozen artifact is created.

##### Required primary-placement semantics

The resolved meaning is:

1. A common scenario-generation process realizes the source-defined HRS random primary placement once, at scenario creation.
2. Each file's primary is mapped to the `data` node of its realized site.
3. The complete file-to-primary-node mapping is frozen in the common scenario artifact.
4. The exact mapping is supplied to Proposed, HRS, DPRS, OGSA, and EIMORM.
5. HRS does not regenerate primary placement independently for each method.
6. The scenario generator rejects/resamples any realization that violates generic capacity, reference, or uniqueness constraints before freezing the artifact.

This preserves CMP-RD-002-HRS-001 in substance. Capacity conditioning is a common initial-state validity rule, not an HRS optimization or replacement behavior.

Placement pools and capacity checks are explicit:

- Primary placement candidates are exactly the four `data` nodes, one gateway node per site. Primary demand is checked against each data node's 160 GiB capacity and the site's 560 GiB capacity; the maximum possible primary demand is 497 GiB against 640 GiB aggregate data-node capacity.
- Additional-replica candidates are all 12 nodes except the file's primary node, subject to no duplicate file/node replica. The generator may use residual `edge`, `data`, or `cloud` capacity, with the aggregate edge/cloud capacity providing a guaranteed fallback pool for the maximum 247 GiB additional demand.
- Every accepted assignment is checked per node and per site, not merely against aggregate capacity.

The common scenario-generation predicate is:

`generate candidate initial state -> validate all generic capacity/identity/reference constraints -> reject invalid realization -> resample or reconstruct -> freeze only the first valid realization`

This predicate is common scenario-generation infrastructure. It is not an HRS algorithm modification and does not allow HRS to regenerate its placement during method execution.

##### Network-topology assessment

The original 132-link decision was a fully connected directed graph. It was not retained: direct connectivity between every node weakens path-selection and topology effects, and can reduce DPRS's graph structure to weighted edge selection rather than meaningful hierarchical routing. The corrected 28-link graph is:

- 16 directed intra-site links: `edge -> data`, `data -> edge`, `cloud -> data`, and `data -> cloud` at each site;
- 12 directed inter-site links: six bidirectional gateway connections, represented as both directed links for every unordered pair of distinct site `data` gateways;
- cross-site traffic therefore traverses an edge/cloud-to-data link, one inter-site gateway link, and a data-to-edge/cloud link;
- same-site traffic uses the local gateway links.

This remains fully reachable, preserves site bandwidth/latency differences, and gives DPRS a meaningful sparse four-site graph while applying exactly the same topology to all five methods.

##### Resource consistency assessment

The CPU profile is internally consistent: each role has 1,000 MIPS per vCPU. The 40% CPU and memory values are researcher-selected initial conditions, not source-defined values and not algorithm objectives. They are scientifically meaningful only as common background state before workload events begin. The current `Node` model does not explicitly represent CPU, memory, or those utilization fractions, so this is not yet necessarily represented by the runtime and remains a future common-simulator implementation gap. No method-specific algorithm logic may depend on the 40% condition unless its own source contract independently requires such state. Storage is different: its initial value must be calculated from the replica catalog, not assigned independently. With the corrected generator, every affected node is checked before freezing.

##### Initial-state and fairness audit table

| Parameter | Current decision | Audit result | Issue severity | Corrected decision | Scientific rationale |
|---|---|---|---|---|---|
| Site/node scale | 4 sites, 12 role-based nodes | Feasible and computationally manageable | NONE | Unchanged | Exposes locality and heterogeneity without adopting OGSA's source-specific eight-node example. |
| Topology density | 132 directed all-to-all links | Direct links weaken path/topology behavior, especially for DPRS | HIGH | 28-link sparse gateway topology | Preserves reachable but nontrivial graph structure and site locality. |
| File-size distribution | Class ranges with an underspecified deterministic assignment | Exact demand was not reproducible | HIGH | Explicit per-size bucket counts and exact selected additional-replica size buckets | Makes storage demand independently recomputable. |
| Initial additional replicas | Odd file IDs received an extra replica | Arbitrary ID/order bias; could correlate with future workload ordering | HIGH | Hash-selected, size-stratified 50-file sample with fixed class targets | Reproducible, balanced, method-independent, and not based on method outcomes. |
| Primary placement | Random HRS placement mapped to data nodes | Valid only if capacity-invalid realizations are rejected before freezing | HIGH | Generate once, condition on generic validity, freeze, replay identically | Preserves HRS randomness while guaranteeing a valid common state. |
| Storage capacity | 2,240 GiB aggregate; 617 GiB exact initial demand | Globally feasible, but arbitrary placement can overflow nodes/sites | MEDIUM | Capacity-valid manifest construction and validation are mandatory | Storage pressure remains meaningful without pre-execution infeasibility. |
| CPU/MIPS/RAM | Role-scaled capacities, 40% initial CPU/memory utilization | MIPS/vCPU is consistent; current model cannot represent utilization explicitly | MEDIUM | Keep values; classify explicit fields as implementation gaps | Common resource state is clear without inventing algorithm logic. |
| Initial health | All nodes healthy/reachable; links available | Feasible and isolated from CMP-RD-005 | NONE | Unchanged | Establishes a clean common baseline for dynamic failure studies later. |
| Network sharing | Equal bandwidth sharing, additive latency, no loss model | Generic and common, but requires future transfer implementation | LOW | Unchanged | Avoids method-specific network behavior and unselected queueing assumptions. |

##### Generic initial-state validation

The resolved environment requires validation that every file has exactly one primary, every primary and replica references an existing node, no file/node replica pair is duplicated, catalog-derived storage equals recorded storage, every node remains within capacity, all nodes are initially healthy/reachable, all links are initially available, all IDs are unique, and the frozen manifest cannot be mutated. The current repository does not yet implement the complete validator or explicit primary/utilization fields; these remain generic implementation gaps, not scientific defaults.

##### CMP-RD-002 Freeze Criteria

CMP-RD-002 is frozen only when the common scenario generator can construct a state satisfying:

- unique IDs;
- valid site/node membership;
- valid primary mappings;
- valid replica mappings;
- no duplicate file-node replica;
- per-node storage capacity;
- per-site storage capacity where applicable;
- valid network endpoints;
- positive capacities;
- valid initial health;
- deterministic catalog;
- deterministic replica-selection rule;
- deterministic configuration/replay identity.

The scientific environment is already decided. These criteria define implementation validity only and introduce no new scientific choices.

##### Computational feasibility

Twelve nodes, 100 files, four sites, and 28 links produce a small finite state for repeated matched runs. The largest obvious state dimensions are the file-to-node replica catalog and method-specific search populations, not the common environment itself. Five methods times multiple scenarios and repetitions is therefore operationally plausible without reducing the environment to a trivial topology. No benchmark or execution estimate was generated in this review.

##### Review conclusion

CMP-RD-002 is **RESOLVED / RESEARCHER-DECIDED and safe to freeze after this review**. The corrected topology, exact catalog, hash-stratified replica selection, and capacity-valid scenario-generation requirements are now authoritative decision text. No blocking scientific feasibility issue remains at the common-environment level. CMP-RD-003 and later decisions remain outside this review.

##### Implementation consequences

No algorithm implementation changes are authorized or required by this decision. The common implementation must eventually add or configure:

- explicit CPU, memory, and utilization representation;
- explicit primary-copy mapping;
- manifest-derived storage initialization;
- generic scenario validation;
- first-class configuration/replay identity linkage and canonical-manifest digest.

Existing `FrozenScenario` cloning remains the mechanism for creating independent method states. Algorithm-specific parameters remain outside the common manifest.

##### Validation requirements

The common scenario validator must enforce:

- unique site, node, VM, file, replica, and link identities;
- valid site-node and VM-node membership;
- valid network endpoints and exactly one reverse directed link where the manifest specifies symmetric connectivity;
- positive capacities and non-negative file sizes, bandwidths, and latencies;
- utilization fractions in `[0, 1]` and utilization not exceeding declared capacity;
- every file's required primary mapping references an existing file and node;
- every replica references an existing file and node, has a unique identity, and is not duplicated on the same file/node pair;
- initial storage usage equals the sum of valid replica file sizes and does not exceed node capacity;
- all initial nodes are healthy/reachable and all initial links are available;
- frozen scenario capture preserves the canonical manifest and rejects mutation of the frozen source;
- every matched method run references identical scenario, configuration, replay, and manifest-digest identities.

These are method-independent environment rules. They do not validate optimizer populations, thresholds, objective formulas, fuzzy parameters, or replication policies.

##### Open dependencies

CMP-RD-002 is resolved, but it does not resolve later decisions:

- CMP-RD-003 owns the request/workload trace, arrival process, user distribution, and workload replay details.
- CMP-RD-004 owns seed values, repetition schedule, and algorithm-local random streams; it must populate the scenario seed/stream identity fields.
- CMP-RD-005 owns dynamic failure/recovery events; CMP-RD-002 defines only the initially healthy state.
- CMP-RD-006 owns simulation horizon and termination.
- CMP-RD-007 through CMP-RD-012 own metrics, result schema, statistics, visualization, experiment matrix, and normalization; CMP-RD-007 through CMP-RD-012 are now resolved as separate boundaries, subject only to remaining method implementation gaps.

Decision status:
RESOLVED / RESEARCHER-DECIDED. CMP-RD-002-HRS-001 remains preserved in substance and remains linked to CMP-RD-002 and CMP-RD-004.

#### CMP-RD-002 implementation-surface audit

This audit inspects the current generic model and identifies whether each environment attribute can be represented without selecting a scientific value. The five adapters receive read-only scenario snapshots; they do not define or own the common environment.

| Parameter | Common/method-specific | Source support | Researcher decision required? | Fairness impact | Reproducibility impact | Current implementation support |
|---|---|---|---|---|---|---|
| Topology and node/site graph | Common | Papers describe data centres, data nodes, sites, providers, or tiers, but no common graph is fixed. | No; CMP-RD-002 selected the common graph. | High | High | **IMPLEMENTED** structurally through `Scenario.sites`, `Scenario.nodes`, and `NetworkLink`; selected values require manifest configuration. |
| Compute resources / CPU | Common environment; source formulas remain method-specific | Papers discuss processing capability, CPU speed, VM computation, or node performance. | No for the selected profile; future field representation remains an implementation gap. | High | High | **PARTIALLY IMPLEMENTED**; generic `Node` has no explicit CPU field, though `attributes` can carry the selected profile. |
| Memory | Common environment | Cloud/VM resource concepts appear, but no common memory model or value is specified. | No for the selected profile; future field representation remains an implementation gap. | Medium to high | High | **PARTIALLY IMPLEMENTED** through generic attributes only; no explicit memory capacity/accounting field. |
| Storage capacity | Common | Sources discuss storage capacity, restrictions, and available space. | No for the selected profile. | High | High | **IMPLEMENTED** through `Node.storage_capacity`, `storage_used`, and `available_storage`; selected values require manifest configuration. |
| Network bandwidth | Common environment; algorithm formulas remain method-specific | HRS and DPRS explicitly use bandwidth-related concepts; other sources discuss transfer/network performance. | No for the selected link profile. | High | High | **IMPLEMENTED** through `NetworkLink.bandwidth`; selected values require manifest configuration. |
| Network latency | Common environment; source response-time formulas remain method-specific | Sources discuss latency, response time, propagation, or transfer delay. | No for the selected link profile. | High | High | **IMPLEMENTED** through `NetworkLink.latency`; selected units/model require manifest configuration. |
| Node/site identity | Common | All methods require identifiable placement locations or data nodes. | Identity policy only | High | High | **IMPLEMENTED** through dictionary keys and `site_id`/`node_id`; uniqueness and referential validation are incomplete. |
| Node health/reachability | Common external state | Common architecture and domain model define health/reachability and external failure/recovery events. | Initial state and event policy | High | High | **IMPLEMENTED** through `Node.healthy`, `Node.reachable`, and external runtime events. |
| Initial replica catalog | Common initial state | Papers discuss replicas; exact common initial catalog is not specified. | No for the selected catalog; validation remains an implementation gap. | High | High | **IMPLEMENTED** through `Scenario.replicas`; generic catalog validation is incomplete. |
| Primary-copy mapping | Common realized scenario state for matched replay; HRS source semantics remain source-specific | HRS explicitly states random initial primary placement; other papers do not establish a common primary-copy rule. | No; CMP-RD-002-HRS-001 and the common validity rule are resolved. | High | High | **PARTIALLY IMPLEMENTED**; a `Replica` points to a file/node, but primary status has no explicit field or mapping. |
| Initial resource utilization | Common initial state | Sources discuss load/storage/resource use but provide no common utilization profile. | No for the selected profile; future field representation remains an implementation gap. | High | High | **PARTIALLY IMPLEMENTED** for storage only via `storage_used`; CPU, memory, and network utilization are not explicit. |
| Scenario identity | Common | Runtime and replay structures require a scenario identity. | Identifier policy only | Medium | High | **IMPLEMENTED** through `Scenario.scenario_id`, `ReplayTrace.scenario_id`, and `RunMetadata.scenario_id`. |
| Configuration identity | Common provenance | Project architecture and provenance require configuration tracking; no final schema is selected. | No for CMP-RD-002; linkage remains an implementation gap. | Medium to high | High | **PARTIALLY IMPLEMENTED** as `RunMetadata.configuration_identity` and generic frozen metadata; not a first-class `Scenario`/`FrozenScenario` field. |
| Replay identity | Common matched-run control | Project architecture requires replayable common scenarios; papers do not define a cross-method replay identity. | No for the selected identity structure; linkage remains an implementation gap. | High | High | **PARTIALLY IMPLEMENTED** through `ReplayTrace` event/scenario/seed/stream identities and frozen scenario cloning; configuration linkage and complete state digest are not explicit. |

##### Source-defined versus researcher-required environment parameters

Source materials provide concepts or method-local inputs, not a common numerical environment. The following source-defined or source-supported items must remain method-specific unless explicitly adopted later by the researcher:

- HRS: heterogeneous/provider/VM concepts, CPU capability, bandwidth, network latency, and random initial primary placement.
- DPRS: data-centre storage/performance concepts, bandwidth, transfer time, queue/wait latency, and response-time components.
- OGSA: data-node assignment, node/network speed or bandwidth, capacity, failure-probability and latency-related objective inputs.
- EIMORM: hierarchical/site/resource, availability, cost, load, energy, and latency concepts; exact executable formulas remain unresolved where documented.
- Proposed: common scenario objects and method-local objective/replication inputs; no paper-defined common topology or resource values.

The common values for node/site counts and roles, topology structure, capacities, storage and utilization profiles, bandwidth and latency values/models, initial replica count and placement policy, initial health state, and scenario/configuration/replay identity policy are resolved below. Their future data-model representation and validation remain implementation gaps. No paper-specific parameter is promoted to a common value here.

##### Initial immutable scenario requirements

The current simulator can construct one scenario and clone it with `FrozenScenario.capture(...).clone_state()`. A valid matched initial scenario must contain, without scientific defaults:

- a unique scenario identity and configuration/replay metadata;
- stable site and node identities with valid site membership;
- the selected common resource, storage, network, health, and utilization state;
- the complete file catalog, including file sizes where required for storage accounting;
- the complete initial replica catalog with valid file/node references;
- an explicit primary-copy mapping for each file where the experiment requires one;
- the externally supplied workload and failure/recovery trace when those are part of the selected scenario.

Each method receives a deep-cloned state from that frozen scenario. Method execution may mutate its clone, but must not regenerate or alter the shared initial realization before the method acts.

##### HRS replay dependencies

Preserving CMP-RD-002-HRS-001 requires these scenario fields:

1. `scenario_id`.
2. Configuration identity for the topology and initial state.
3. Stable site and node identities and the candidate site/node set.
4. Ordered file IDs/catalog identity.
5. The realized file-to-primary-site/node mapping.
6. The complete initial replica catalog, including explicit primary designation.
7. Scenario seed identity and random-stream identity used to generate the realization.

The full matched scenario additionally requires the common topology, resource, storage, network, health, utilization, workload, and external-event fields. Those fields support replay of the whole scenario but do not supply an HRS algorithm-specific replacement or placement policy.

##### Generic validation requirements

These rules can be implemented without choosing scientific values:

- scenario, site, node, VM, file, replica, link, request, and event identities are unique within their respective scopes;
- every node references an existing site, and every site membership list references existing nodes;
- every VM references an existing node;
- every network endpoint references an existing node, and link IDs are unique;
- capacity, size, bandwidth, and latency values are either explicitly unresolved or valid non-negative values in declared units; no default is supplied;
- storage usage is non-negative and does not exceed declared capacity when both are present;
- every replica references an existing file and node;
- every primary mapping references an existing file and node, and the mapped node is valid for the scenario;
- initial replica records and primary mappings are internally consistent;
- node health/reachability fields are valid booleans;
- a scenario identity is present and unique within its experiment/configuration scope;
- replay metadata refers to the same scenario/configuration identity as the frozen state;
- frozen scenario capture must preserve the recorded initial state without sharing mutable collections with method clones.

Rules outside this decision remain unresolved, including workload generation, seed/repetition policy, dynamic failures, simulation horizon, metrics, result schema, statistics, visualization, experiment matrix, and normalization. The initial replica distribution, primary requirement, topology class, and utilization meanings are resolved by CMP-RD-002 above.

##### Researcher decision table

The following worksheet rows are retained as the question trace; their statuses are updated to reflect the selected decisions above.

| ID | Parameter | Question to decide | Possible options | Source evidence | What is missing | Fairness implication | Reproducibility implication | Implementation dependency | Status |
|---|---|---|---|---|---|---|---|---|---|
| CMP-RD-002-A01 | Topology inventory | Which node/site roles and identities comprise the common environment? | Researcher-defined inventory or externally supplied topology | Papers describe sites/data centres/nodes/tiers | Counts, roles, and IDs | Same inventory for all methods | Serialize stable IDs and configuration identity | Scenario construction and adapter snapshots | RESOLVED |
| CMP-RD-002-A02 | Connectivity | Which node/site pairs are connected and how are links represented? | Directed/undirected graph, explicit links, or another documented representation | Network relationships and links are source-supported | Complete graph and link semantics | Same graph and reachability | Serialize graph and link values | Network validation and transfer layer | RESOLVED |
| CMP-RD-002-B01 | Compute and memory | What CPU/processing and memory fields are present and how are they measured? | Explicit capacities/rates, abstract attributes, or a documented host/VM model | Processing/VM concepts appear in sources | Common fields, units, and values | Same capacity model | Record units and per-node values | Node model and runtime accounting | RESOLVED |
| CMP-RD-002-C01 | Storage | What capacity, initial use, and available-space rules apply? | Explicit capacity/use model or another documented accounting model | Storage constraints are source-supported | Values and initial utilization | Same storage pressure | Record capacities, use, and derivation | State validation and replica mutation | RESOLVED |
| CMP-RD-002-D01 | Network performance | What bandwidth, latency, and transfer model is common? | Per-link/per-node values and documented transfer semantics | Bandwidth/latency concepts appear in sources | Values, units, contention, and propagation rules | Same communication conditions | Record model version and parameters | Network execution and metrics | RESOLVED |
| CMP-RD-002-E01 | Initial files/replicas | What file catalog, sizes, replica catalog, and primary mapping start each run? | Researcher-defined catalog and realized replayed state | Files/replicas are common concepts; HRS primary placement is source-defined | Counts, sizes, initial replicas, primary semantics | Identical initial state | Serialize complete catalog/mapping | Scenario freeze and clone | RESOLVED |
| CMP-RD-002-E02 | Initial health/load/utilization | What health, reachability, load, and utilization state starts the scenario? | Explicit state fields or documented derivation from initial state | Health/load/resource concepts are supported | Initial state and utilization semantics | Same starting conditions | Record realized state and derivation | State initialization and external events | RESOLVED |
| CMP-RD-002-F01 | Scenario/configuration identity | How are scenario and configuration identities assigned and linked? | Stable names, content-derived identities, or another documented policy | Runtime/provenance identity fields exist | Final naming and scope policy | Enables matched-run association | Prevents accidental mismatches | Provenance and replay metadata | RESOLVED |
| CMP-RD-002-F02 | Replay identity | What metadata proves that all five methods received the same realization? | Seed/stream IDs, trace IDs, state digest, or a documented combination | Replay structures support scenario/seed/stream identity | Complete replay record and digest policy | Strong matched comparison guarantee | Enables exact audit/reconstruction | Frozen scenario orchestration | RESOLVED |

##### Dependency audit

The current dependency order is appropriate:

`CMP-RD-002` -> `CMP-RD-003` dataset/workload -> `CMP-RD-004` randomness/replay -> `CMP-RD-005` failures -> `CMP-RD-006` horizon -> method execution.

No reordering is required. CMP-RD-004 must consume the scenario identity and replay boundary established by CMP-RD-002, while CMP-RD-003 must define the workload fields that become part of the frozen scenario. CMP-RD-005 and CMP-RD-006 depend on the resulting scenario/event representation. Method execution remains downstream and must not resolve any common-environment field implicitly.

##### CMP-RD-002 audit status

RESOLVED / RESEARCHER-DECIDED. This audit records the selected configuration surface and remaining implementation gaps without changing scientific behavior.

Dependencies:
- CMP-RD-001
- CMP-RD-003
- CMP-RD-005
- CMP-RD-006

Affected methods:
- Proposed Method / Proposed NSGA-III
- HRS
- DPRS
- EIMORM
- OGSA

Source boundary:
The common environment is not source-defined algorithm behavior. It belongs to the project experiment design and common simulation layer.

Simulator boundary:
This belongs to the simulator and experiment configuration layer.

Common-vs-method-specific boundary:
The following are common experimental conditions and must be standardized across all five methods unless a source paper explicitly defines otherwise:

1. Network topology
   - Classification: RESEARCHER-DEFINED for the final experiment; SIMULATOR-DEFINED for the runtime implementation.
   - Fairness requirement: all methods see the same topology and network graph.
    - Status: RESOLVED by CMP-RD-002; selected topology is recorded above.

2. Number and type of nodes
   - Classification: RESEARCHER-DEFINED for the experiment; SIMULATOR-DEFINED for creation and state tracking.
   - Fairness requirement: all methods run on the same node population and node roles.
    - Status: RESOLVED by CMP-RD-002; selected node inventory is recorded above.

3. Node resource capacities
   - Classification: RESEARCHER-DEFINED for the experiment; SIMULATOR-DEFINED for runtime accounting.
   - Fairness requirement: CPU, memory, storage, and network capacities must be common across methods.
    - Status: RESOLVED by CMP-RD-002; selected resource profile is recorded above.

4. Storage capacities
   - Classification: RESEARCHER-DEFINED for the experiment; SIMULATOR-DEFINED for accounting and validation.
   - Fairness requirement: storage limits must be identical across methods.
    - Status: RESOLVED by CMP-RD-002; selected storage profile is recorded above.

5. Network bandwidth and latency
   - Classification: RESEARCHER-DEFINED for the experiment; SIMULATOR-DEFINED for runtime propagation and delay computation.
   - Fairness requirement: all methods interact with the same communication model.
    - Status: RESOLVED by CMP-RD-002; selected network profile is recorded above.

6. Initial replica state
   - Classification: RESEARCHER-DEFINED for the experiment; SIMULATOR-DEFINED for initialization and state assignment.
   - Fairness requirement: the initial replica placement and storage state must be shared across methods before each method acts.
    - Status: RESOLVED by CMP-RD-002; selected initial state is recorded above.

7. File population
   - Classification: RESEARCHER-DEFINED for the dataset definition; SIMULATOR-DEFINED for the file catalog.
   - Fairness requirement: all methods operate on the same file set, file sizes, and catalog.
    - Status: RESOLVED for the CMP-RD-002 file catalog; request workload remains CMP-RD-003.

8. Request workload
   - Classification: RESEARCHER-DEFINED for the experiment; SIMULATOR-DEFINED for invocation scheduling.
   - Fairness requirement: each method sees the same request stream or the same replayed workload trace.
   - Status: OPEN unless the common workload is specified.

9. Failure-event infrastructure
   - Classification: SIMULATOR-DEFINED for the event mechanism; RESEARCHER-DEFINED for whether failures are included in the experiment.
   - Fairness requirement: failure scheduling may be common, but method-specific response must remain source-specific.
   - Status: OPEN unless the experiment chooses the failure protocol.

10. Simulation start state
    - Classification: RESEARCHER-DEFINED for the experiment; SIMULATOR-DEFINED for runtime setup.
    - Fairness requirement: all methods begin from the same runtime state.
    - Status: RESOLVED by CMP-RD-002 for the common initial configuration.

11. Randomness regime
    - Classification: RESEARCHER-DEFINED for the comparison design; SIMULATOR-DEFINED for seed management and runtime generation.
    - Fairness requirement: reproducibility must be common across methods, while algorithm-internal stochasticity remains method-specific.
    - Status: OPEN unless a seed/repetition regime is chosen.

12. Common evaluation layer
    - Classification: RESEARCHER-DEFINED for metric definitions and reporting protocol; SIMULATOR-DEFINED for data collection.
    - Fairness requirement: the evaluation layer must not standardize internal method objectives or source-specific optimizer formulas.
    - Raw-result requirement: the future comparison must be based on raw simulation results and downstream statistical aggregation, not on manually created or fabricated values. The common evaluation layer therefore must preserve the raw per-run measurement records needed to generate reproducible comparison charts later.
    - Status: OPEN unless the common metric set and reporting policy are selected.

The following remain method-specific and must not be silently standardized across all methods:
- optimizer identity
- objective function or fitness definition
- OIS
- popularity mechanism
- replication factor logic
- number-of-replicas logic
- placement strategy
- provider selection logic
- deletion policy
- replacement policy
- internal optimizer parameters
- algorithm-specific dynamic trigger
- any method-specific trigger or repair policy not explicitly defined by the source

This list is a guardrail, not a change to source behavior.

Constraints / guardrails:
- Do not convert simulator environment settings into algorithm-specific scientific behavior.
- Do not invent method-specific topology assumptions.
- Do not assume one algorithm has access to conditions denied to another.
- Do not impose the Proposed Method's OIS, replica-count logic, or NSGA-III placement onto HRS, DPRS, EIMORM, or OGSA.
- Do not force the baselines to use the same optimization engine merely because the common simulator supports it.
- Do not resolve any concrete numerical values for topology, capacities, workload, seeds, or timing in this decision without explicit evidence.
- Do not create comparison charts or fabricated numerical values at this stage. The required output of the future experimental pipeline is raw, reproducible result data that can support later statistical aggregation and chart generation.

Decision:
RESOLVED — RESEARCHER-DECIDED

---

### CMP-RD-003 — Dataset and Workload

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Define the common dataset and workload used by all five methods while preserving the distinction between the external workload and each algorithm's internal decision logic.

Why this decision is required:
The architecture explicitly requires a common workload, but no concrete generator or workload specification is defined. The repository supports the fairness principle that all five methods should observe the same external data and request stream while each method continues to interpret that external workload using its own source-defined logic.

Current evidence:
The repository evidence establishes that the system must represent a common shared environment, users, files, requests, and runtime events, but it does not specify a final dataset generator or request generation policy. The evidence is strongest for the fair-comparison requirement, not for any specific numerical workload value.

The clearest repository evidence is:
- [docs/01-project-overview.md](docs/01-project-overview.md) says the simulation must compare all five methods under identical system environment, dataset, workload, network topology, node characteristics, failure model, and request patterns.
- [docs/03-comparison-methods.md](docs/03-comparison-methods.md) states the same external environment must be maintained across algorithms, while only the replication decision mechanism differs.
- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) distinguishes common workload and event generation from algorithm-specific decisions.
- [docs/06-common-domain-model.md](docs/06-common-domain-model.md) defines files, requests, users, network, and simulation-time state as shared domain concepts.
- [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) requires common metrics and repeated runs, but it does not specify the final dataset parameters.

Researcher decision:
The common dataset remains the 100-file CMP-RD-002 catalog. The workload is resolved below as a materialized, exogenous, read-only trace with three explicit workload scenarios. The trace is independent of all method outputs and is replayed identically across all five methods.

#### CMP-RD-003 Researcher Decision

##### Dataset boundary

- The 100 file IDs, exact sizes, primary mappings, initial replicas, and size-derived small/medium/large classes remain exactly as resolved by CMP-RD-002.
- No additional semantic file types are introduced. The size class is common dataset metadata only; it is not a replacement for any method's source-defined file-type or importance interpretation.
- File sizes in request records are copied from the immutable file catalog. The workload generator does not alter file size, replica count, primary placement, or storage state.

##### Workload scenarios

| Decision ID | Scenario | Exact definition | Classification | Rationale | Dependency |
|---|---|---|---|---|---|
| CMP-RD-003-W01 | Balanced access | 1,200 read requests over 7,200 seconds, one request every 6 seconds; each of the 100 files is selected exactly 12 times in a deterministic file-order cycle. No hot, warm, or cold popularity classes are used. | RESEARCHER-DECIDED | Provides a non-skewed baseline so popularity-aware behavior is not evaluated only under a long-tail workload. | CMP-RD-004 replay identity; CMP-RD-006 termination. |
| CMP-RD-003-W02 | Stationary skew | 1,200 read requests at the same 6-second interval. A 10-request deterministic cycle contains 6 hot, 3 warm, and 1 cold request: hot cohort is 20 files and receives 720 requests, warm cohort is 30 files and receives 360 requests, and cold cohort is 30 files and receives 120 requests. Hot cohort B is not selected in this stationary scenario; selection is round-robin within each active cohort. | RESEARCHER-DECIDED | Exercises replication pressure and access concentration without using any algorithm's popularity formula. | CMP-RD-004 replay identity; CMP-RD-006 termination. |
| CMP-RD-003-W03 | Predefined phase shift | 1,200 read requests at the same 6-second interval. Phase A contains requests 1–600 and uses hot cohort A with 60%, stable warm cohort with 30%, and cold cohort with 10%. Phase B contains requests 601–1,200 and replaces hot cohort A with disjoint hot cohort B; warm and cold cohorts remain unchanged. | RESEARCHER-DECIDED | Tests response to an externally imposed popularity change while remaining independent of method results. | CMP-RD-004 replay identity; CMP-RD-006 termination. |

The file cohorts are generated once by sorting the 100 file IDs by SHA-256 of `cmp-rd-003-cohort-v1|file-id`: the first 20 files are hot cohort A, the next 20 are hot cohort B, the next 30 are warm, and the final 30 are cold. This hash-based partition is independent of file ordering, file size, method outputs, and future request observations.

For W02, the 60/30/10 values are request proportions, not file proportions: 720 hot requests, 360 warm requests, and 120 cold requests. The active hot cohort contains 20 files, the warm cohort contains 30 files, and the cold cohort contains 30 files; the inactive hot-B cohort receives zero requests in W02. For W03, Phase 1 is requests 1–600 with Hot-A active, and Phase 2 is requests 601–1,200 with disjoint Hot-B active. Each phase contains exactly 360 active-hot requests, 180 warm requests, and 60 cold requests. Warm and cold cohorts do not change between phases.

Within every cohort, files are selected in the canonical hash-sorted order and wrap around. W01 uses one complete 100-file cycle repeated 12 times. W02 uses six hot, three warm, and one cold selection per cycle. W03 uses six selected-hot, three warm, and one cold selection per cycle in each phase. The exact request-to-file mapping is therefore deterministic.

Timestamp index is exact for every scenario: sequence $n \in \{1, \ldots, 1200\}$ has `timestamp(n) = 6 x n` seconds. Therefore `request-000001` occurs at 6 seconds and `request-001200` occurs at 7,200 seconds. These are workload-trace timestamps only and do not resolve CMP-RD-006 simulation termination or horizon.

##### Request model

| Parameter | Final decision | Classification | Fairness and reproducibility rationale | Current implementation status |
|---|---|---|---|---|
| Operation | Read-only access; no writes or updates in CMP-RD-003 | RESEARCHER-DECIDED | All source methods are primarily evaluated around reads/accesses, while no common write consistency model exists. | `Request` has no operation field; implementation gap. |
| Request count/rate | 1,200 requests per scenario, one every 6 seconds, equivalent to 10 requests/minute | RESEARCHER-DECIDED | Sufficient to expose access, network, load, and replication effects for 100 files while remaining tractable for five methods and repeated runs. | `Request.arrival_time` exists; generator is missing. |
| Arrival time/order | Sequence `n ∈ {1,...,1200}`, `timestamp(n) = 6 x n` seconds; `request-000001` is at 6 seconds and `request-001200` is at 7,200 seconds; sequence order is authoritative | COMMON-SIMULATOR REQUIREMENT | Materialized timestamps and stable order prevent per-method arrival differences. These trace timestamps do not resolve CMP-RD-006 termination. | Events support timestamps and insertion ordering; dedicated trace sequence is missing. |
| Request overlap | Requests are scheduled independently of completion; service may overlap when runtime capacity permits | COMMON-SIMULATOR REQUIREMENT | The workload does not serialize methods or hide queue/load behavior. | Event scheduling exists; completion/concurrency accounting is missing. |
| Target file | Deterministic cohort/cycle rules above; repeated access to the same file is allowed | RESEARCHER-DECIDED | Models realistic repeated access without algorithm-specific popularity calculations. | `Request.file_id` exists. |
| Requester identity | 16 clients: `client-01` through `client-16`; `client-01`–`client-04` belong to site-01, `client-05`–`client-08` to site-02, `client-09`–`client-12` to site-03, and `client-13`–`client-16` to site-04. `client_index = ((sequence - 1) mod 16) + 1`. | RESEARCHER-DECIDED | Makes requester identity explicit and balanced across sites, independently of algorithm behavior. | `User.user_id` and `User.site_id` exist; client generation is missing. |
| Source location | `site_index = ((sequence - 1) mod 4) + 1`; sequences 1,5,9,... originate at site-01, 2,6,10,... at site-02, 3,7,11,... at site-03, and 4,8,12,... at site-04. The source node is always that site's `edge` node. | RESEARCHER-DECIDED | Exercises common local/remote network conditions without letting methods choose source locations. | `User.site_id` exists; request source node is missing. |
| Request size | Copied from the immutable target `File.size` | COMMON-SIMULATOR REQUIREMENT | Prevents inconsistent request/file size definitions. | No typed request-size field; derivable from `file_id`. |
| Duration/completion | No duration is generated in the trace; service start, completion, response time, outcome, and bytes transferred are runtime observations | COMMON-SIMULATOR REQUIREMENT | Avoids inventing method-specific service behavior in the workload. | Completion/outcome fields and request handling are missing. |
| Concurrent file access | Multiple requests may target the same or different files; no method controls the external trace | COMMON-SIMULATOR REQUIREMENT | Preserves natural contention and repeated-access behavior equally. | Runtime event queue exists; request handler is missing. |

##### Popularity and access semantics

The workload provides only raw ordered access events: file ID, timestamp, requester, source location, and read operation. The simulator may derive generic access count, last-access time, distinct-user count, and access history from those events. It must not calculate OIS, HRS Merit, DPRS-specific popularity, EIMORM ETBDF, or OGSA fitness. Each adapter remains responsible for consuming only the source-defined interpretation available to that method.

Client assignment, source-site assignment, timestamps, file selection, cohort membership, and phase boundaries are generated without observing replication decisions, replica placement, algorithm fitness, OIS, HRS Merit, DPRS decisions, OGSA fitness, EIMORM decisions, or performance metrics. The trace is fixed before any method execution.

The W01/W02/W03 distributions are external workload controls, not claims about any source formula. W02 supplies a stationary long-tail stress case; W01 supplies a balanced control; W03 supplies a predefined phase change to test dynamic behavior across methods without using any algorithm output to determine the change.

##### Workload artifact and replay boundary

Each materialized workload artifact contains:

- CMP-RD-002 `scenario_id`;
- `workload_id` (`cmp-rd-003-balanced-v1`, `cmp-rd-003-skew-v1`, or `cmp-rd-003-phase-shift-v1`);
- canonical trace identity/digest;
- stable sequence number and `request_id` formatted as `request-000001` through `request-001200`;
- `user_id`, source site, and source node;
- target `file_id` and catalog-derived request size;
- `operation="read"`;
- arrival timestamp and phase/cohort metadata.

The artifact is generated once, stored, frozen, and replayed with identical request order and timestamps across Proposed, HRS, DPRS, OGSA, and EIMORM. CMP-RD-004 owns seed and repetition allocation; the workload artifact identity must be recorded without selecting that later seed schedule here.

##### Causal replication feedback

The common event boundary is:

`request event -> current scenario state -> method decision -> validated state transition -> subsequent request observes resulting state`

The workload itself never changes after materialization. A later request may observe a replica created by an earlier accepted method decision, but replica selection, creation, deletion, movement, and recovery remain method/runtime behaviors outside CMP-RD-003. Equal timestamps use the existing event insertion order; a future request handler must preserve this causal rule.

##### Source evidence table

| Method/source | Dataset and workload evidence | What is not specified or remains method-specific |
|---|---|---|
| Proposed Method | Requests, file access history, timestamps, file size, replication frequency, users, and success/failure concepts are described. | No common file count, request count, arrival law, source-site distribution, final popularity distribution, OIS weights, decay, or trigger policy. |
| HRS | Source experiment reports 20 data centres, 100–1,000 tasks, Poisson task assignment, 1–5 files per task, and 100–500 million instructions per task; source also uses access count and recency. | These are paper-specific values and conflict with CMP-RD-002's common scale; fuzzy/popularity parameters and a common request generator are not defined. |
| DPRS | Dataset size, usage frequency, request arrival rate, Poisson/M/M/1 response-time concepts, transfer time, and wait latency are described. | The source does not define a complete common request trace or require its Poisson model to govern every method; the printed formula remains source-specific. |
| EIMORM | Read requests, access proportions, timestamps, time decay, popularity, users, and geographically distributed data centres are discussed. | File/request counts, exact access distribution, executable decay, invocation schedule, and complete workload generator are unresolved; ETBDF is not repaired here. |
| OGSA | File size, access rate, access rate by file/node, service time, latency, load, bandwidth, and an eight-node source experiment are described. | The eight-node experiment and optimizer settings are source-specific; no common request generator or access-pattern generator is supplied. |

The different source scales and models justify a researcher-defined common trace. No source parameter is silently promoted to the common workload.

##### Fairness rationale

- Every method receives the same ordered 1,200-request artifact for a given scenario, including timestamps, target files, requesters, and source locations.
- Balanced, skewed, and phase-shift scenarios prevent conclusions from depending on one popularity shape.
- Any advantage from locality, recency, popularity, or adaptation is attributable to the method's source-defined behavior, not a different input stream.
- The workload is generated independently of method outputs and is never tuned after execution.
- Read-only semantics avoid granting one method an unsupported write/recovery interpretation.
- The trace is sufficiently large to create repeated file access and locality effects while remaining manageable for repeated five-method experiments.

##### Validation requirements

The common workload validator must enforce:

- unique workload, trace, request, user, and sequence identities;
- monotonically increasing timestamps and deterministic sequence ordering;
- valid target file IDs and catalog-derived request sizes;
- valid requester, source-site, and source-node identities;
- `operation` is one of the resolved common operations (`read` for CMP-RD-003);
- non-negative timestamps and valid request metadata;
- scenario/workload/configuration identity linkage;
- deterministic artifact digest and canonical serialization;
- identical artifact identity, request order, timestamps, and fields across matched methods;
- no algorithm output, method metric, or method decision can influence trace generation;
- causal processing preserves the request-to-state-transition ordering above.

##### Implementation consequences and gaps

No algorithm implementation changes are required or authorized. The current runtime already provides `Request.file_id`, `user_id`, and `arrival_time`, event timestamps/insertion ordering, read-only adapter snapshots, and frozen scenario cloning. It does not yet provide a workload generator, typed operation/source-node/sequence fields, access-history updates, request handlers, completion/outcome records, trace identity binding, or materialized workload replay. These are common-simulator implementation gaps.

Decision status:
RESOLVED / RESEARCHER-DECIDED. CMP-RD-004 through CMP-RD-012 are resolved by their own sections and retain separate ownership of their respective boundaries.

Dependencies:
- CMP-RD-002
- CMP-RD-004
- CMP-RD-011

Affected methods:
- Proposed Method / Proposed NSGA-III
- HRS
- DPRS
- EIMORM
- OGSA

Classification of workload properties (pre-resolution evidence; final decisions are recorded above):

1. Number of files
   - Classification: RESEARCHER-DEFINED for the experimental dataset; UNRESOLVED in the current repository evidence.
   - Evidence: [docs/01-project-overview.md](docs/01-project-overview.md) and [docs/06-common-domain-model.md](docs/06-common-domain-model.md) mention files as part of the common model, but no final file count is stated.
   - Fairness impact: high; all methods must operate on the same file set.
    - Decision status: RESOLVED by CMP-RD-003.

2. File-size distribution and file-size range
   - Classification: RESEARCHER-DEFINED for the dataset; UNRESOLVED in current evidence.
   - Evidence: file size is part of the shared data model, but the repository does not define a generation law or numerical range.
   - Fairness impact: high; file sizes materially affect storage pressure and replica decisions.
    - Decision status: RESOLVED by CMP-RD-003.

3. Number of requests
   - Classification: RESEARCHER-DEFINED for the workload design; UNRESOLVED in current evidence.
   - Evidence: the common model includes requests, but no final request count or request generation policy is stated.
   - Fairness impact: high; workload intensity determines comparative stress on all methods.
    - Decision status: RESOLVED by CMP-RD-003.

4. Request arrival process
   - Classification: RESEARCHER-DEFINED for the workload generator; UNRESOLVED in current evidence.
   - Evidence: the repository defines the presence of requests and time-aware simulation, but not the stochastic or deterministic arrival model.
   - Fairness impact: high; the request stream must be common across methods.
    - Decision status: RESOLVED by CMP-RD-003.

5. Request frequency and access rate
   - Classification: RESEARCHER-DEFINED for the common workload; UNRESOLVED in current evidence.
   - Evidence: access frequency appears as a common file property in [docs/01-project-overview.md](docs/01-project-overview.md), but the generation law is not specified.
   - Fairness impact: high; frequency affects popularity, access pressure, and response behaviors.
    - Decision status: RESOLVED by CMP-RD-003.

6. File popularity / access distribution
   - Classification: RESEARCHER-DEFINED for the external workload distribution; SOURCE-DEFINED for each method's internal popularity or importance mechanism.
   - Evidence: the shared domain model explicitly expects file access history and popularity/importance information, but the exact popularity distribution is not specified by the repository.
   - Fairness impact: high; the same external popularity pattern should be used unless a source method explicitly requires a different internal interpretation.
    - Decision status: RESOLVED at the common-workload level; method-specific interpretation remains source-defined or unresolved.

7. User and request distribution
   - Classification: RESEARCHER-DEFINED for the external workload; UNRESOLVED in current evidence.
   - Evidence: users and requests are part of the common domain model, but their distribution across sites or clients is not defined.
   - Fairness impact: high; user locality, access skew, and spatial hot spots affect fairness.
    - Decision status: RESOLVED by CMP-RD-003.

8. Request-to-file mapping
   - Classification: RESEARCHER-DEFINED for the external workload generation; UNRESOLVED in current evidence.
   - Evidence: the system records request objects and file IDs, but no generation rule linking requests to files is specified.
   - Fairness impact: high; this defines the underlying access trace used by all methods.
    - Decision status: RESOLVED by CMP-RD-003.

9. Workload intensity and stress level
   - Classification: RESEARCHER-DEFINED for the experiment; UNRESOLVED in current evidence.
   - Evidence: the repository requires dynamic simulation and fairness but does not specify a stress-level design.
   - Fairness impact: high; if scenarios are used, they must be common across all algorithms.
    - Decision status: RESOLVED by CMP-RD-003.

10. Dataset scenarios and storage-pressure scenarios
    - Classification: RESEARCHER-DEFINED for the experimental design; UNRESOLVED in current evidence.
    - Evidence: the architecture and overview documents allow dynamic simulation and scenario-based comparison, but do not define final scenario dimensions or values.
    - Fairness impact: high; scenario definition must be common across algorithms.
    - Decision status: RESOLVED by CMP-RD-003.

11. Dynamic workload changes over time
    - Classification: RESEARCHER-DEFINED for scenario generation; SIMULATOR-DEFINED for event execution; SOURCE-DEFINED for each algorithm's internal dynamic response behavior.
    - Evidence: the project overview says the environment is dynamic and time-aware, and the architecture distinguishes common failure and dynamic scenario infrastructure from method-specific dynamic logic.
    - Fairness impact: high; the external workload changes must remain common, while each method's reaction remains source-specific.
    - Decision status: RESOLVED by CMP-RD-003.

12. Request replay across methods
    - Classification: RESEARCHER-DEFINED fairness policy; not yet resolved.
    - Evidence: the project overview and comparison-method documents repeatedly state that all five algorithms must see the same dataset, users, requests, and network conditions, but they do not yet specify whether the exact same request stream must be replayed identically across all runs.
    - Fairness impact: high; identical replay is the strongest fairness guarantee and should be used unless a different policy is explicitly justified.
    - Decision status: RESOLVED by CMP-RD-003.

13. External workload vs algorithm-specific internal logic
    - Classification: COMMON EXTERNAL WORKLOAD is RESEARCHER-DEFINED / SIMULATOR-DEFINED; INTERNAL ALGORITHM LOGIC is SOURCE-DEFINED.
    - Evidence: the common architecture and domain model explicitly separate common state from algorithm-specific internal decisions.
    - Fairness impact: essential; it prevents one method from being given a different dataset or different popularity mechanism merely because the algorithm internally uses one.
    - Decision status: RESOLVED structurally by CMP-RD-003.

Source-defined properties that must remain method-specific:
- Proposed Method OIS
- Proposed Method replication/file selection logic
- Proposed Method replica timing logic
- Proposed Method number-of-replicas logic
- NSGA-III-based placement/optimization
- Proposed Method replacement strategy
- HRS placement and selection logic
- HRS replacement logic
- DPRS placement logic
- EIMORM ETBDF / EARF / IEK behavior when source-defined
- OGSA optimization behavior and objectives

These must not be overwritten by a common workload policy.

Simulator-defined properties:
- workload generation engine
- request creation and time stamping
- event scheduling
- log/export of raw workload records
- scenario replay management
- dataset serialization for re-runs

These belong to the common simulation and trace infrastructure, not to any algorithm's scientific logic.

Researcher-defined properties resolved by CMP-RD-003:
- the CMP-RD-002 file catalog is retained;
- exact request counts, arrival times, file-selection rules, popularity cohorts, source locations, read-only semantics, scenario set, and replay policy are defined above.

Constraints / guardrails:
- Do not define workload as a hidden algorithm objective.
- Do not invent file distributions or popularity laws without designation as researcher-defined choices.
- Do not introduce method-specific dataset differences.
- Do not use the Proposed Method's OIS, timing logic, or replica-count mechanism as a common external workload rule.
- Do not generate workload parameters after observing method performance.
- Do not fabricate numerical results or future values in this decision.

Decision:
RESOLVED — RESEARCHER-DECIDED

---

### CMP-RD-004 — Randomness and Reproducibility

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Audit and classify the randomness and reproducibility requirements before real simulation begins, while preserving the strict separation between common external conditions and algorithm-internal stochastic behavior.

Why this decision is required:
The repository explicitly requires reproducible simulation, repeated runs, and common fair conditions, but the source papers do not jointly define a single randomness policy or seed regime for all five methods. The comparison design therefore must identify which randomness is common, which is algorithm-specific, and which remains unresolved.

Current evidence:
The following evidence is the relevant foundation for this decision:

- [docs/01-project-overview.md](docs/01-project-overview.md) requires a controlled and reproducible simulation environment and states that each run must use a configurable random seed.
- [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) requires repeated execution with independent random seeds and reports mean, standard deviation, minimum, and maximum.
- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) separates scenario randomness from algorithm randomness and states that common external scenarios must be reproducible across matched algorithm runs.
- [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md) explicitly states that common scenario randomness must be the same across matched algorithm runs, while algorithm-local randomness may differ and need not be consumed in the same order or quantity.
- [docs/02-proposed-method.md](docs/02-proposed-method.md) defines the Proposed Method as a multi-stage dynamic strategy, but it does not state a random seed, a random initialization policy, or a repetition protocol for the full method.
- [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) states that the primary copy of each file is randomly placed at the beginning of the simulation. This is source-defined random initialization for HRS for that specific initial placement step.
- [docs/algorithms/DPRS-implementation-contract.md](docs/algorithms/DPRS-implementation-contract.md) explicitly states that DPRS is not described as requiring algorithm-local random seed behavior.
- [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) states that the initial solution is randomly generated and that a random variable in [0,1] is used in the search process.
- [docs/algorithms/EIMORM-implementation-contract.md](docs/algorithms/EIMORM-implementation-contract.md) lists random selection as one of several possible heuristics, but the source material does not specify a single executable random policy.

Researcher decision:
The reproducibility policy is resolved below while preserving the required boundary between:
- common external randomness (workload, request stream, scenario generation, failure schedule, common initial conditions), and
- algorithm-internal randomness (source-defined stochastic operators or optimization state updates).

The following properties must be classified, not silently fixed:

1. Whether each source method uses randomness.
2. Where randomness occurs inside each method, if explicitly stated.
3. Whether the source specifies random initialization.
4. Whether the source specifies random population generation.
5. Whether the source specifies random selection.
6. Whether the source specifies random mutation/crossover or equivalent operators.
7. Whether the source specifies random node/file/request selection.
8. Whether the source specifies random failure generation.
9. Whether the source specifies random workload generation.
10. Whether the source specifies random network/topology generation.
11. Whether the source specifies a random seed.
12. Whether the source specifies a fixed seed.
13. Whether the source specifies multiple independent runs.
14. Whether the source specifies repeated experiments.
15. Whether the source reports mean/average results across runs.
16. Whether the source reports standard deviation, variance, confidence intervals, or similar statistics.
17. Whether the source specifies warm-up periods or discarded initial observations.
18. Whether the source specifies deterministic initialization.
19. Whether the common simulator introduces randomness independently of the algorithms.
20. Which randomness must be common across methods for fair comparison.
21. Which randomness must remain method-specific.
22. Whether the same external random workload/conditions should be replayed across all five methods.
23. Whether different algorithm-internal random processes require independent streams.
24. How random state must be recorded for reproducibility.
25. What minimum information must be stored with every experiment/run.

Classification of key randomness and reproducibility properties:

- Proposed Method / Proposed NSGA-III
  - Random initialization of the method as a whole: UNRESOLVED.
  - Random population generation or stochastic evolutionary initialization: UNRESOLVED.
  - Random selection inside the optimization loop: UNRESOLVED.
  - Random mutation/crossover or equivalent operators: UNRESOLVED unless a more specific source contract later states otherwise.
  - Random seed value: UNRESOLVED.
  - Deterministic initialization: UNRESOLVED.
  - Multiple independent runs: RESEARCHER-DEFINED, not source-defined.
  - Mean and variance across runs: RESEARCHER-DEFINED, not source-defined.
  - Warm-up/discarded observations: UNRESOLVED.

- HRS
  - Random placement of the primary copy of each file at simulation start: SOURCE-DEFINED.
  - Random node/file selection beyond that explicit initial placement: UNRESOLVED.
  - Random seed policy: UNRESOLVED.
  - Fixed seed policy: UNRESOLVED.
  - Repetition protocol: RESEARCHER-DEFINED.

- DPRS
  - Algorithm-local randomness: SOURCE-DEFINED as absent / not identified by the source and implementation contract.
  - Random selection: SOURCE-DEFINED as not required by the paper.
  - Random seed behavior: SOURCE-DEFINED as not part of the DPRS algorithm definition.
  - Any randomness introduced in project implementation outside the source: RESEARCHER-DEFINED or SIMULATOR-DEFINED only.

- EIMORM
  - Random selection as a candidate decision heuristic: RESEARCHER-DEFINED or UNRESOLVED depending on whether the implementation chooses that policy.
  - Exact random selection rule: UNRESOLVED.
  - Random seed for any chosen random tie-break or selection policy: RESEARCHER-DEFINED.
  - Fixed deterministic alternative: RESEARCHER-DEFINED if selected as a project policy.

- OGSA
  - Random initial solution generation: SOURCE-DEFINED.
  - Random assignment of files to nodes in the initial solution: SOURCE-DEFINED.
  - Random number generation in [0,1]: SOURCE-DEFINED.
  - Exact random generator family and seed policy: RESEARCHER-DEFINED or UNRESOLVED; the source defines the presence of randomness but not the concrete generator or seed protocol.
  - Population generation or stochastic search operators: SOURCE-DEFINED at the conceptual level, but exact implementation mechanics remain UNRESOLVED.
  - Multiple independent runs and reporting statistics: RESEARCHER-DEFINED.

Common external experimental randomness (fairness layer):
- workload generation
- request arrival process
- request-to-file mapping
- user/request assignment
- failure-event schedule
- externally generated topology or initial system state
- scenario replay conditions

Classification:
- RESEARCHER-DEFINED for the exact policy to be used in the experiment
- SIMULATOR-DEFINED for the runtime implementation of that policy
- COMMON-SIMULATOR DESIGN for the requirement that matched algorithm runs see the same common scenario stream

Algorithm-internal randomness:
- NSGA-III evolutionary operators if used in the Proposed Method
- OGSA initial-population generation and randomized search updates
- any explicit source-defined random selection rule in EIMORM if the implementation chooses it
- any algorithm-specific stochasticity introduced by a source paper for that specific method

Classification:
- SOURCE-DEFINED when the paper states the existence of a random mechanism
- RESEARCHER-DEFINED when the exact implementation details are not in the source
- UNRESOLVED when the repository still lacks sufficient source evidence to determine the exact operational behavior

Fairness boundary:
The common simulator may generate common scenario randomness and the same external workload conditions, but it must not force all algorithms to consume the same algorithm-internal random stream merely to appear comparable. The architecture explicitly requires common environment and common scenario inputs, while allowing algorithm-local randomness to vary independently. This is the correct fairness boundary and should remain in force.

Replay requirement:
The same realized workload and external scenario artifacts are replayed exactly across all five methods for each matched repetition. The actual failure artifact remains owned by CMP-RD-005, but any later failure realization must follow this same replay boundary.

Reproducibility record required in the future:
At minimum, the experiment metadata must preserve enough information to reproduce a run. The complete result schema remains owned by CMP-RD-008, but the randomness/provenance fields include:
- experiment/scenario identifier
- method name and source specification version
- run identifier
- random seed or seed set
- random-stream identity if multiple streams are used
- common dataset/workload configuration identifier
- topology/configuration identifier
- failure schedule identifier
- simulator version / commit
- algorithm configuration version
- raw per-run outputs
- termination condition and simulation horizon metadata
- runtime timestamps if they are relevant to trace reconstruction

This is a reproducibility requirement, not a decision to fix final field names or numerical values.

Special boundary notes:
- The Proposed Method remains a multi-stage dynamic replication strategy with OIS, replica selection, timing, replica-number logic, placement, and replacement stages. It must not be reduced to "NSGA-III only" in this decision.
- HRS is the canonical acronym for Hybrid Replication Strategy; HSR is not a separate method.
- Baselines must not import OIS, NSGA-III, ETBDF, EARF, IEK, Ψ, OBL, GSA/GSO, or other cross-method concepts into one another unless the source method explicitly requires them.
- The presence of stochasticity does not by itself authorize a common seeded random stream across methods.
- A random policy that is not specified by a source paper remains UNRESOLVED or RESEARCHER-DEFINED rather than being silently chosen.
- This decision does not resolve the later statistical-analysis or visualization decisions.

#### CMP-RD-004 Researcher Decision

##### Stochasticity inventory

| Method | Stochastic component | Source evidence | Source-defined? | Current implementation support | Researcher decision required? | CMP-RD-004 responsibility | Method-specific responsibility |
|---|---|---|---|---|---|---|---|
| Proposed Method / Proposed NSGA-III | Possible population initialization, variation, selection, or tie sampling inside NSGA-III | Proposed contracts define NSGA-III stages but do not define a seed, initialization distribution, crossover/mutation policy, or stochastic selection rule. | UNRESOLVED, not silently added | No active RNG; adapter returns unresolved for incomplete NSGA-III execution. | Yes, in the Proposed-method decision boundary before execution. | Repetition identity and reserved method stream derivation. | Exact stochastic operators and parameters. |
| HRS | Random initial primary-copy placement | HRS specification explicitly states random primary placement at simulation start. | SOURCE-REQUIRED | Scenario/runtime can freeze and clone state, but no RNG injection exists. | Seed/stream policy only; no new HRS randomness. | Common scenario stream, validation, freeze, and replay. | HRS must not regenerate the primary mapping. |
| HRS | Additional random candidate selection or fuzzy randomness | No complete source requirement identified; fuzzy policy is incomplete. | UNRESOLVED | No HRS RNG is active for this purpose. | No selection until source/researcher decision explicitly authorizes it. | Record any later authorized stream identity. | HRS contract must preserve unresolved fuzzy/tie behavior. |
| DPRS | Poisson/exponential queue-model assumptions | DPRS source describes Poisson arrivals and exponential service in its response-time model, but the common workload is CMP-RD-003's materialized trace. | SOURCE-REQUIRED model assumption, not a common trace generator | Current DPRS code does not generate arrivals or service samples. | No algorithm-local RNG is selected. | Common trace/replay boundary only. | Preserve source queue formulas without importing their generator into other methods. |
| OGSA | Random initial solution/file assignment and random factors in GSA updates | OGSA source defines random initialization and random values in `[0,1]` for GSA updates; CMP-RD-013 fixes OBL + GSA. | SOURCE-REQUIRED | `RandomSource` is only a protocol argument; no RNG is wired into the adapter. | Generator family, seed derivation, and unresolved binary/feasibility policies remain separate OGSA decisions. | Isolated OGSA method stream and provenance. | Consume only OGSA's local stream. |
| EIMORM | Random selection as a possible heuristic | EIMORM contract lists random selection as a possibility but does not require one executable random operator. | UNRESOLVED / RESEARCHER-DECIDED only if later authorized | No RNG is active. | Do not add randomness here. | Reserve an isolated stream identity if later required. | EIMORM researcher decisions must define any stochastic heuristic. |

##### Master seed and derivation protocol

The experiment uses one master seed token selected and registered before the first experiment execution. It is recorded in the experiment seed registry/provenance, immutable for the registered experiment, and must never be selected, replaced, or changed after observing results. CMP-RD-004 selects the derivation protocol but does not hard-code the master seed value. Define `H(label, fields)` as SHA-256 over the canonical UTF-8 serialization of the label and ordered fields, with unambiguous length-prefix encoding. The resulting 256-bit digest is the recorded seed identity; the first 128 bits may be supplied as the numeric seed to a deterministic RNG implementation.

For experiment `experiment_id`, configuration `configuration_id`, scenario `scenario_id`, workload `workload_id`, and repetition `repetition_id`, derive:

```text
scenario_seed_identity = H("scenario", master_seed, experiment_id,
                           configuration_id, scenario_id, repetition_id)
workload_seed_identity = H("workload", master_seed, experiment_id,
                           configuration_id, workload_id, repetition_id)
failure_seed_identity = H("failure", master_seed, experiment_id,
                          configuration_id, scenario_id, repetition_id)
method_seed_identity = H("method", master_seed, experiment_id,
                         configuration_id, scenario_id, workload_id,
                         repetition_id, method_id)
```

The scenario seed represents the common environment and initial-state realization, so it deliberately does not depend on `workload_id`; the same scenario can be reused with multiple CMP-RD-003 workload artifacts. The workload seed represents the request trace and does depend on `workload_id`. The workload trace in CMP-RD-003 is deterministic and consumes no random values; its workload seed identity is recorded as a derivation identity, not used to alter the trace. The failure seed remains separate, is recorded for reproducibility when applicable, and does not select failure times or probabilities here; CMP-RD-005 owns the actual failure schedule. Separate labels and complete context prevent one logical purpose from shifting another stream.

##### Logical stream architecture

Common streams generate or identify only common artifacts:

- `scenario.initial_state`, including the HRS source-defined primary realization;
- `scenario.workload`, reserved but not consumed by the deterministic CMP-RD-003 trace;
- `scenario.failures`, reserved for the later CMP-RD-005 failure design.

Method-local streams are separate:

- `algorithm.Proposed`;
- `algorithm.HRS`, unused unless a later source-faithful HRS stochastic component is authorized;
- `algorithm.DPRS`, unused because no algorithm-local randomness is source-required;
- `algorithm.OGSA`, required for source-defined random initialization and GSA factors;
- `algorithm.EIMORM`, unused unless a later researcher decision authorizes a source-supported stochastic heuristic.

A method-local stream is never the source of a common scenario artifact. Consuming 500 values in OGSA cannot advance Proposed, HRS, DPRS, EIMORM, workload, or failure streams.

##### Repetition and replay policy

The researcher-selected repetition count is **30 independent repetitions per method, workload scenario, and configuration cell**. Repetition IDs are fixed as `rep-01` through `rep-30` before execution. The count is common to all five methods and is selected before observing results; CMP-RD-009 retains ownership of statistical tests, confidence intervals, and aggregation details.

For each repetition, the common process is:

1. derive the common identities and logical stream identities;
2. construct one common scenario and materialized workload artifact;
3. construct the registered CMP-RD-005 failure artifact;
4. validate and freeze the canonical common manifest;
5. compute and record its replay identity/digest;
6. deep-clone the exact state for all five methods;
7. replay identical external artifacts and timestamps for every method;
8. allow only method-local streams to produce source-required algorithm randomness.

HRS primary placement is generated once by the common scenario stream, validated, frozen, and replayed identically. HRS never regenerates that mapping using its local stream.

SOURCE-REQUIRED: HRS randomly places primary copies at simulation start. RESEARCHER/COMMON-SIMULATOR DECISION: the realized HRS-compatible primary placement is generated once, validated, frozen, and replayed identically across all five methods. The HRS source does not itself require replay across competing methods; replay is the project's matched-comparison decision.

EXACT REPLAY: the same scenario/workload/failure artifacts, same method configuration, same method seed identity, same implementation version, and same deterministic ordering rules produce the same execution trace, assuming deterministic implementation.

INDEPENDENT REPETITION: the same experimental cell uses a different registered repetition identity and derived seed set, producing an independent stochastic realization.

MATCHED COMPARISON: all five methods under one repetition use the same experimental cell and common artifacts, while method-specific stochastic streams remain isolated.

##### Provenance and seed registry

Every run must record the randomness/provenance fields needed to reconstruct its realization without defining CMP-RD-008's complete result schema:

- experiment ID;
- scenario ID;
- workload ID and workload artifact digest;
- configuration ID;
- replay/canonical-manifest digest;
- repetition ID and repetition index;
- master seed identity and, when execution occurs, the actual numeric master seed value;
- scenario seed identity and, when execution occurs, the actual numeric scenario seed value;
- workload seed identity or deterministic-trace identity and any actual numeric workload seed value used;
- failure seed identity, actual numeric failure seed when applicable, and failure-artifact digest when CMP-RD-005 applies;
- method ID and method-configuration identity;
- method-local seed identity, actual numeric method-local seed when execution occurs, and named stream identities;
- source specification version and implementation version/commit;
- deterministic ordering/serialization version;
- interpretation status and decision provenance.

Existing `RunMetadata` fields are a partial foundation. The future common simulator must enforce the required fields and bind them to the frozen scenario/workload artifacts.

Seed identity is the stable derivation/reference identifier; seed value is the actual numeric input supplied to an RNG at execution. CMP-RD-004 does not select the master numeric value now, but the raw/provenance layer must be able to record every actual numeric seed used later.

##### Determinism boundary and no-cherry-picking rule

The common simulator must use stable IDs, sorted canonical serialization, explicit event sequence numbers for equal timestamps, deterministic graph traversal order, deterministic tie handling where already required by the common model, and deterministic artifact hashing. Unordered set/dictionary iteration, parallel completion order, floating-point tie ambiguity, and optimizer tie handling must not silently alter common artifact identity. Source-level unresolved ties remain unresolved rather than being invented by this decision; method-specific ties remain in their method decision boundary.

All 30 planned repetitions for every method/scenario/configuration cell must be executed and retained. No repetition may be removed because its result is unfavorable. Technical invalidity criteria must be defined before execution; failed, unresolved, rejected, timed-out, and invalid attempts remain recorded. A permitted rerun uses the same repetition identity and preserves the original attempt record. No seed, workload, failure realization, or method-local stream may be selected after observing results.

##### Fairness boundary

- Common scenario, workload, and later failure artifacts are identical across all five methods for a matched repetition.
- Method-local streams are deterministically derived from the same master experiment seed and matched experimental identity; identical integer seeds are not required because methods consume randomness differently.
- Each method receives the same 30 repetition identities and no method can consume another method's random values.
- HRS's source-required primary randomness is common scenario state, not a per-method advantage.
- OGSA retains source-required stochasticity without forcing its random trajectory onto any other method.
- No RNG is added to DPRS or EIMORM without source-faithful authorization, and Proposed stochastic behavior remains unresolved until its own policy is decided.

##### Implementation consequences and gaps

No algorithm implementation changes are authorized. The current repository lacks an active RNG abstraction, seed derivation service, named stream registry, RNG injection into adapter snapshots, workload/failure artifact generation, replay validation, canonical manifest serialization/digest, required provenance enforcement, and tests for stream independence or exact replay. These are common-simulator implementation gaps. `RandomSource` in OGSA is an existing protocol boundary, not a completed RNG implementation.

##### Validation requirements

The future common infrastructure must validate that:

- every repetition has one pre-derived identity and no duplicate repetition ID;
- all common artifacts for a matched repetition have identical digests across methods;
- scenario/workload/failure streams are distinct by derivation label and context;
- method-local stream identities are distinct from common streams and from other methods;
- the HRS primary mapping is generated once and never regenerated by an adapter;
- all required seed, stream, artifact, method, configuration, and implementation identities are present;
- canonical serialization and event ordering are deterministic;
- no method output can affect future common artifact generation;
- all planned repetitions and technical failures remain auditable.

##### Downstream dependencies

CMP-RD-004 resolves only randomness and reproducibility. CMP-RD-005 remains responsible for the actual failure/dynamic scenario protocol and consumes the reserved failure stream. CMP-RD-006 remains responsible for simulation horizon and termination. CMP-RD-007 and CMP-RD-008 are resolved; CMP-RD-009 through CMP-RD-012 remain responsible for statistics, visualization, experiment matrix, and normalization.

Decision status:
RESOLVED / RESEARCHER-DECIDED.

Constraints / guardrails:
- Do not choose a numerical seed value.
- Do not choose a statistical confidence-interval method or test here; the repetition count is fixed at 30 per method/scenario/configuration cell.
- Do not select a confidence-interval method here.
- Do not resolve later comparison decisions such as statistical testing, final chart generation, or experiment matrix design.
- Do not treat algorithm-internal randomness as a common objective.
- Do not fabricate performance values or run summaries.
- Do not convert a missing source definition into an invented implementation detail.

Decision:
RESOLVED — RESEARCHER-DECIDED

---

### CMP-RD-002-HRS-001 — HRS Initial Random Primary-Copy Placement Fairness

Status: DECIDED — SCOPED EXPERIMENTAL INTERPRETATION

Parent decisions:
- CMP-RD-002 — Common Experimental Environment
- CMP-RD-004 — Randomness and Reproducibility

Purpose:
Record the comparative-experiment interpretation for HRS's source-described random initial primary-copy placement without changing HRS source behavior or closing either parent decision.

Source boundary:
- HRS explicitly states that the primary copy of each data file is randomly placed in different sites at the beginning of the simulation.
- The source does not specify whether ownership of that randomization is HRS-internal or scenario-level.
- The source does not specify a seed, distribution, repetition policy, or replay policy.

Researcher decision:
For comparative experiments, HRS's source-described random initial primary-copy placement is treated as part of the generated scenario state.

For each experimental run:
1. Generate the initial primary-copy placement using the source-described random placement behavior.
2. Record the realized initial primary-copy placement.
3. Freeze that realized placement as part of the scenario state.
4. Replay the same realized initial state across all five methods in the matched comparison run.
5. Preserve HRS's source-described random initialization semantics; do not replace them with a deterministic placement heuristic.
6. Do not allow HRS to independently regenerate a different initial placement during matched execution.
7. Record the scenario identifier and random-stream/seed identity used to generate the scenario.
8. Leave the exact seed policy and repetition count under the existing CMP-RD-004 decision; this scoped decision does not select either.

Scenario fields required specifically to support this replay:
- `scenario_id`
- `configuration_id` for the topology and initial-state configuration
- the ordered file catalog and file identifiers
- the candidate site/node identity set used for primary placement
- the realized file-to-primary-site/node mapping
- the complete initial replica catalog, including primary-copy designation
- the scenario random seed identity and random-stream identity used for generation
- stable site and node identifiers needed to interpret the mapping

The broader matched-run state also requires the common topology, resource, storage, network, health, utilization, workload, and external-event fields listed in the CMP-RD-002 worksheet. Those fields are required to replay the full scenario, but they are not additional inputs to the HRS primary-placement realization itself.

Trade-off and interpretation boundary:
- This preserves the realized source-described random initialization.
- This enables matched comparison and a common initial state.
- This moves ownership of the random realization into scenario construction for the comparative experiment.
- This is a researcher-defined fairness/reproducibility interpretation, not a claim that the HRS source requires replay across methods.
- The source does not explicitly say that the randomization is scenario-level.

Scope guardrails:
- This decision does not resolve the later CMP-RD-003 through CMP-RD-006 workload, randomness, failure, or horizon choices.
- This decision does not resolve CMP-RD-004's seed, repetition, or statistical protocol.
- No HRS algorithmic placement, selection, replacement, or failure-recovery behavior is changed.

Decision:
DECIDED — SCOPED EXPERIMENTAL INTERPRETATION

---

### CMP-RD-005 — Failure and Dynamic Scenario Protocol

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Classify the failure and dynamic-scenario boundary in the common experiment without adding source behavior or numerical failure assumptions.

Why this decision is required:
The common architecture separates common simulation events from method-specific responses, but the source papers do not define a single cross-method failure protocol or recovery scheme. This section therefore distinguishes:
- the common simulator's responsibility for externally imposed events,
- the researcher's responsibility to decide whether such events are included,
- the method-specific logic that is explicitly source-defined,
- the unresolved gaps that must remain open.

Current evidence:
The clearest evidence is as follows:

- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) defines failure and recovery as part of the common simulation environment and states that failures and recovery scheduling belong to the simulator, while method responses remain source-specific if the source defines them.
- [docs/06-common-domain-model.md](docs/06-common-domain-model.md) includes an exogenous failure/recovery schedule as a shared runtime concept.
- [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md) states that node failure and node recovery are common simulation events and that the simulator owns state transitions.
- [docs/01-project-overview.md](docs/01-project-overview.md) requires failures and recoveries to be represented in the simulation environment.
- [docs/02-proposed-method.md](docs/02-proposed-method.md) states that the Proposed Method detects changes in node state and failures at evaluation intervals, but it does not define a complete failure probability model, failure schedule, or recovery algorithm.
- [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) describes an initial random placement and discusses failure probability in the system context, but it does not define a source-level failure-recovery mechanism.
- [docs/algorithms/DPRS-implementation-contract.md](docs/algorithms/DPRS-implementation-contract.md) explicitly states that failure handling is not defined in the source and that node failure/recovery are managed by the common simulator.
- [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md) discusses fault tolerance conceptually and states that replication provides resilience when a site fails, but does not provide a formal failure model or recovery policy.
- [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) explicitly uses node failure probability in the availability objective, but explicitly states that actual failure handling and recovery logic are not specified.

Researcher decision required:
The researcher must decide when the common experiment includes failures and which external event schedule is used, while preserving the strict boundary between:
- common failure event generation,
- the decision to include failures in the experiment,
- source-defined algorithm responses,
- unresolved recovery gaps.

Exact classification vocabulary for this section:
- SOURCE-DEFINED
- RESEARCHER-DEFINED
- SIMULATOR-DEFINED
- UNRESOLVED

Only one label is used for each property. No composite labels are used.

Major properties and classifications:

1. Common failure event generation
   - Classification: SIMULATOR-DEFINED.
   - Evidence: the common architecture explicitly assigns node failure and node recovery to the simulator.

2. Decision whether failures are included in the experiment
   - Classification: RESEARCHER-DEFINED.
   - Evidence: the project architecture requires the experiment to define whether failures are part of the study, but no final protocol is fixed in the source docs.

3. Exact failure probability for a method
   - Classification: UNRESOLVED.
   - Evidence: no source paper gives a complete cross-method failure-probability protocol or a final numerical schedule.

4. Exact failure timing or schedule
   - Classification: UNRESOLVED.
   - Evidence: no source paper defines a runtime failure schedule.

5. Exact recovery time
   - Classification: UNRESOLVED.
   - Evidence: no source paper defines a recovery time model.

6. Exact failure-triggered dynamic response
   - Classification: UNRESOLVED unless a source explicitly defines it for a particular method.
   - Evidence: a dynamic trigger may be source-supported in a specific method, but it is not common across all methods.

7. Replica reconstruction or re-replication after failure
   - Classification: UNRESOLVED for all five methods unless a source explicitly states it.
   - Evidence: the source papers do not provide a complete failure-repair algorithm in the reviewed specification set.

8. Node recovery to service
   - Classification: UNRESOLVED unless a source paper explicitly defines the operation.
   - Evidence: separate from failure event generation and separate from source-defined response logic.

Method-specific classifications:

- Proposed Method / Proposed NSGA-III
  - Dynamic evaluation of access history and node state: SOURCE-DEFINED.
  - Detection of failures at evaluation intervals: SOURCE-DEFINED at the conceptual level.
  - Replica selection, timing, count adjustment, placement, and replacement under storage pressure: SOURCE-DEFINED.
  - Failure probability model: UNRESOLVED.
  - Failure timing, runtime failure schedule, and recovery algorithm: UNRESOLVED.
  - Failure-triggered re-optimization: UNRESOLVED.
  - Automatic recovery or automatic replica reconstruction: UNRESOLVED.
  - The Proposed Method remains a multi-stage dynamic replication strategy and must not be reduced to NSGA-III-only behavior in this section.

- HRS
  - Initial primary-copy placement is randomly determined: SOURCE-DEFINED.
  - Replacement and adaptive selection logic under storage-pressure or priority conditions: SOURCE-DEFINED only as far as the HRS source description supports it.
  - Failure recovery behavior: UNRESOLVED.
  - Failure probability as a contextual factor in system design: SOURCE-DEFINED only as a conceptual input discussed in the broader method context, not as a complete runtime failure/recovery mechanism.
  - Explicit runtime failure schedule: UNRESOLVED.
  - Recovery mechanism: UNRESOLVED.

- DPRS
  - DPRS placement logic and response-time objective: SOURCE-DEFINED.
  - DPRS algorithm-local failure handling: UNRESOLVED.
  - DPRS recovery algorithm: UNRESOLVED.
  - Runtime failure event generation and recovery scheduling: SIMULATOR-DEFINED if the common experiment includes them.
  - DPRS must not be assigned an invented failure-recovery mechanism.

- EIMORM
  - Conceptual fault tolerance through replication and resilience: SOURCE-DEFINED.
  - Dynamic cost-aware re-replication or rebalancing when explicitly specified by the source: SOURCE-DEFINED only if the evidence supports that exact behavior.
  - Exact failure detector, failure distribution, and recovery policy: UNRESOLVED.
  - Runtime failure recovery: UNRESOLVED.

- OGSA
  - Node failure probability used as an input in the availability objective: SOURCE-DEFINED.
  - Runtime failure event generation: UNRESOLVED.
  - Runtime failure recovery: UNRESOLVED.
  - Re-replication after failure: UNRESOLVED.
  - Any assumption that the simulator must dynamically fail nodes during runtime is not supported by the source evidence and must remain UNRESOLVED.

Failure vs recovery must remain distinct:

- failure occurrence: UNRESOLVED unless the source explicitly defines it for the specific method
- failure detection: SOURCE-DEFINED only for the Proposed Method at the conceptual level; otherwise UNRESOLVED
- node unavailability or replica loss: SIMULATOR-DEFINED if externally imposed in the common experiment; otherwise UNRESOLVED
- algorithm response after failure: UNRESOLVED unless explicitly source-defined
- replica reconstruction or re-replication: UNRESOLVED unless explicitly source-defined
- node recovery: UNRESOLVED unless explicitly source-defined

Common versus algorithm-specific boundary:

- Common failure event generation: SIMULATOR-DEFINED.
- Decision to include failures in the experiment: RESEARCHER-DEFINED.
- Common failure schedule when included: RESEARCHER-DEFINED and SIMULATOR-DEFINED only at the experiment-infrastructure level; not source-defined algorithm behavior.
- Method-specific response after a failure: SOURCE-DEFINED only if the source explicitly states it; otherwise UNRESOLVED.
- Recovery logic: UNRESOLVED unless the source explicitly defines it for that method.

Special checks:

- Proposed Method: no failure-triggered NSGA-III rerun is added here unless the source explicitly provides it.
- HRS: storage-pressure replacement and ordinary replacement are not automatically the same as failure recovery; failure recovery remains UNRESOLVED.
- DPRS: no failure-recovery mechanism is invented.
- EIMORM: ETBDF, EARF, IEK, and dynamic rebalancing remain source-defined concepts only where the source explicitly supports them; they do not automatically imply failure recovery.
- OGSA: node failure probability in the availability model is distinct from runtime failure schedule generation and failure recovery. They are classified separately.

#### CMP-RD-005 Researcher Decision

##### Source evidence table

| Method | Source-supported failure-related claims | Classification | Not source-defined / unresolved |
|---|---|---|---|
| Proposed Method | Dynamic evaluation includes node state/failure detection conceptually; replication, placement, and replacement are part of the multi-stage method. | SOURCE-REQUIRED at the conceptual evaluation boundary | Failure probability, exact timing, recovery, failure-triggered optimization, request redirection, and reconstruction. |
| HRS | Initial random placement and contextual failure/availability discussion; ordinary placement/provider/replacement logic. | SOURCE-REQUIRED only for stated concepts | Failure detector, failure schedule, recovery, and failure-triggered re-replication. |
| DPRS | Response-time and graph placement model; failure/recovery is assigned to the common simulator by its implementation contract. | SOURCE-REQUIRED placement model; COMMON-SIMULATOR-REQUIRED events | DPRS repair, lifecycle, recovery, and failure response. |
| EIMORM | Conceptual availability, resilience, and cost-aware re-replication discussion. | SOURCE-REQUIRED conceptual resilience only | Executable failure detector, trigger, threshold, repair, recovery, and replica mapping. |
| OGSA | Node failure probability appears in the availability/MFU objective. | SOURCE-REQUIRED objective input | Runtime failure generation, recovery, failed-node exclusion, and re-replication. |

No source provides a complete common failure schedule or recovery protocol. No source-specific probability is promoted into the common experiment.

##### Failure scenario classes

The common failure artifact contains one of the following five pre-registered classes. CMP-RD-011 remains responsible for the eventual experiment-matrix selection and reporting combinations.

| Class | Purpose | Exact externally supplied events |
|---|---|---|
| `F0-control` | No-failure baseline | No node or link events. |
| `F1-node-transient` | Isolated node outage | One eligible node fails at `t=1,800 s` and recovers at `t=2,400 s`; duration 600 s. All 12 edge/data/cloud nodes are eligible. |
| `F2-site-transient` | Correlated site outage | All three nodes of one selected site fail at `t=3,600 s` and recover at `t=4,500 s`; duration 900 s. |
| `F3-link-transient` | Gateway connectivity disruption | Both directed links of one selected inter-site gateway pair become unavailable at `t=4,800 s` and are restored at `t=5,400 s`; duration 600 s. |
| `F4-node-persistent` | Persistent replica-outage stress | One selected data node hosting at least one initial primary-only file fails at `t=5,400 s` and remains unavailable through the CMP-RD-003 trace boundary at `t=7,200 s`; active duration 1,800 s. |

F1, F2, and F3 contain one failure episode and no overlapping independent episodes. F2 is a simultaneous three-node site event by definition. F4 has no recovery event within the workload artifact. All failures occur after the initially healthy CMP-RD-002 state.

##### Target selection and failure randomness

The target schedule is generated once per repetition using the CMP-RD-004 failure stream identity and stable manifest IDs. For candidate target `x`, compute `H("cmp-rd-005-target", failure_seed_identity, class_id, stable_id(x))` and select the lowest digest, using stable ID as the tie-break.

- F1 candidates are all 12 nodes, so edge, data, and cloud roles are eligible.
- F2 candidates are the four sites; the selected site contributes all three of its nodes.
- F3 candidates are the six unordered pairs of distinct site data gateways; each selected pair is represented by both directed links.
- F4 candidates are data nodes hosting at least one initial primary-only file; this ensures the persistent outage tests operational access to primary data without changing CMP-RD-002.

This is common scenario generation, independent of method output, workload response, or performance. It uses CMP-RD-004's failure stream but does not define failure probabilities or alter the seed derivation protocol.

##### Event and recovery semantics

For a node failure, the common simulator sets the node unavailable and unreachable and disables its incident links for operational connectivity. For recovery, it restores the node and its incident links to the pre-event availability state. For F3, only the selected directed gateway links are disabled and restored.

At equal timestamps, event priority is:

1. failure or recovery state transition;
2. request arrival;
3. method observation and decision;
4. validated state transition;
5. request completion or observation.

The existing event queue's insertion sequence remains the final deterministic tie-break. This priority is a common simulator rule, not method-specific behavior. A failure at the same timestamp as a request therefore applies before that request is evaluated.

Recovery restores external health/connectivity only. It does not recreate, move, delete, or count replicas; it does not invoke an optimizer, retry a request, or trigger re-replication. Failure-triggered replication is not implied by a failure event.

##### Replica, request, and availability boundary

Physical node failure means operational unavailability. Replica metadata remains present and valid in the catalog; the replica is inaccessible while its node or required path is unavailable. Recovery restores access to the existing metadata if the node/path is available. Replica deletion, reconstruction, replacement, and re-replication remain method-specific and are not performed by the common failure model.

CMP-RD-005 does not define request success, timeout, deadline, response-time, or failure classification semantics. The current runtime lacks a complete request executor and outcome model. The common layer may record health transitions and blocked/unavailable observations once implemented; CMP-RD-007 owns metric definitions. System/node availability, data availability, replica availability, and request success remain distinct concepts.

##### Failure artifact replay

For each `scenario_id`, `configuration_id`, `workload_id`, `repetition_id`, and failure class, the common generator produces a canonical schedule containing:

- failure artifact ID and digest;
- failure class;
- failure seed identity;
- selected node/site/link IDs;
- event type, timestamp, duration, and recovery timestamp where applicable;
- pre-event and post-event health/availability states;
- canonical ordering sequence.

The schedule is validated, frozen, and replayed identically across Proposed, HRS, DPRS, OGSA, and EIMORM. No method regenerates or modifies it. The failure artifact is part of the matched replay identity but does not redefine CMP-RD-008's complete result schema.

##### Common versus method-specific behavior

Common and researcher-decided:

- failure class, target eligibility, target identity, timestamp, duration, recovery event, health transition, link availability transition, event priority, artifact identity, validation, and replay;
- initial health remains all nodes healthy/reachable and all links available;
- failure generation is independent of every method's RNG and output.

Method-specific or unresolved:

- detection timing beyond the common event visibility;
- replication trigger, placement, selection, replacement, repair, reconstruction, retry, and recovery strategy;
- method-specific request handling and use of alternate replicas;
- any source-specific failure response not explicitly defined by its contract.

The common simulator does not import Proposed repair, HRS replacement, DPRS placement, EIMORM re-replication, or OGSA optimizer behavior into another method.

##### Fairness and scenario scale

All five methods receive the same failure class, selected target, timestamps, duration, recovery state, event order, failure artifact digest, and failure seed identity for each matched repetition. No method can influence later failure events, and schedules are fixed before result observation.

Five classes are the smallest set that covers the required scientific contrasts without making failure behavior a single undifferentiated stress test: a baseline, isolated transient outage, correlated site outage, connectivity-only outage, and persistent primary-data outage. Combined with the three CMP-RD-003 workloads and 30 CMP-RD-004 repetitions, this defines 450 common workload/failure/repetition cells before the five method executions in each cell. CMP-RD-011 remains responsible for the final matrix presentation and any explicitly justified exclusions.

##### Implementation consequences and gaps

No algorithm implementation changes are authorized. The current infrastructure partially supports node health transitions and deterministic event queue ordering, but it lacks failure artifact generation/replay, link failure transitions, recovery scheduling, event-priority semantics, failure provenance binding, request behavior during failure, availability/outcome recording, and validation of failure schedules. Replica metadata preservation is structurally possible but not semantically complete for outage intervals.

##### Validation requirements

The common failure validator must enforce:

- valid class and artifact identity;
- failure seed identity and matched scenario/workload/repetition linkage;
- eligible and existing target IDs;
- no duplicate or overlapping events within a class unless explicitly defined by F2;
- failure and recovery timestamps consistent with the declared duration;
- all event timestamps within the workload artifact boundary;
- all initial nodes/links healthy and available before the first event;
- incident-link consistency for node failures;
- both directed links represented for F3 gateway-pair outages;
- deterministic canonical event ordering and digest;
- identical failure artifact identity across all five matched runs;
- no method output or method-local RNG can alter the schedule;
- logical replica records remain present unless a later method-specific decision changes them.

##### Downstream dependencies

CMP-RD-004 remains authoritative for failure seed derivation, stream isolation, and repetition identity. CMP-RD-006 remains responsible for final simulation horizon and termination; the 7,200-second CMP-RD-003 boundary is only the workload/failure artifact boundary. CMP-RD-007 and CMP-RD-008 are resolved; CMP-RD-009 through CMP-RD-012 remain responsible for statistics, visualization, experiment matrix, and normalization.

Decision status:
RESOLVED / RESEARCHER-DECIDED.

Constraints / guardrails:
- Do not invent failure probabilities or dynamic trigger intervals beyond the registered CMP-RD-005 schedule.
- Do not invent failure-triggered optimization loops.
- Do not invent automatic recovery or replica reconstruction for any method.
- Do not convert a static availability-model parameter into a runtime failure event schedule.
- Do not conflate workload dynamics, resource dynamics, and failure dynamics.
- Do not change the five-method scope.
- Do not generate results or implementation artifacts.

Decision:
RESOLVED — RESEARCHER-DECIDED

---

### CMP-RD-006 — Simulation Horizon and Termination

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Investigate and document how the common simulation horizon, start conditions, and termination conditions should eventually be defined without inventing numerical values or incorrectly substituting algorithm-internal iteration limits for the common experiment horizon.

Why this decision is required:
The project documents require a shared, time-aware simulation environment and a fair common experiment, but the source papers do not provide a single cross-method definition of simulation duration, start condition, or stopping criterion. The architecture therefore requires a clear separation between:
- common simulation horizon of the shared experiment,
- algorithm-internal iteration limits,
- workload completion boundary,
- event-driven stopping rules,
- failure-triggered dynamic behavior,
- measurement window and warm-up definition.

Current evidence:
The strongest evidence is the project-level comparison architecture and the source-specific method contracts:

- [docs/01-project-overview.md](docs/01-project-overview.md) requires the same simulation duration, system environment, network, dataset, request patterns, and failure model across all five methods.
- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) states that time-aware simulation and scenario execution are common simulator concerns, but it does not define a final horizon length or concrete stopping rule.
- [docs/06-common-domain-model.md](docs/06-common-domain-model.md) defines time-aware simulation, event scheduling, and shared runtime state, but remains generic about the final experiment duration.
- [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md) separates common simulator scheduling from method-specific decision logic and explicitly forbids one method from receiving a different simulation horizon merely because its algorithm executes differently.
- [docs/Proposed-Method-Implementation-Contract.md](docs/Proposed-Method-Implementation-Contract.md) defines the Proposed Method as a multi-stage algorithm with OIS, dynamic replica count, NSGA-III placement, and replacement; it gives internal parameter names such as "maximum placement iterations" and "simulation time" as evaluation inputs, but does not define the common experiment horizon itself.
- [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) explicitly defines an optimizer termination rule based on max iterations, but that is algorithm-internal optimizer stopping, not the common simulation horizon.
- [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) documents placement and replacement logic, but no source-defined global simulation duration or termination rule.
- [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md) and [docs/algorithms/DPRS-implementation-contract.md](docs/algorithms/DPRS-implementation-contract.md) discuss request processing and queue behavior, but no global simulation horizon or fixed request limit is explicitly specified by the source.
- [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md) describes ETBDF, EARF, IEK, and dynamic cost-aware behavior, but not a complete simulation horizon or termination rule.
- [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) defines optimizer termination at maximum iterations, but does not define the common simulation horizon across all five methods.

Researcher decision:
The common experiment defines the temporal boundary and termination policy below:
- simulation horizon,
- simulation start state,
- simulation end state,
- workload completion boundary,
- event-queue completion policy,
- warm-up and observation window,
- fixed-time versus workload-based stopping,
- maximum-time safeguards,
- termination reason logging.

These choices are researcher-decided because the source papers do not fix a common horizon.

#### CMP-RD-006 Researcher Decision

##### Source horizon audit

| Method/source | Source-supported temporal information | Classification | Common-horizon conclusion |
|---|---|---|---|
| Proposed Method | Dynamic evaluation and multi-stage replication; no common duration, end time, warm-up, or termination rule. | SOURCE-REQUIRED concepts; exact horizon UNRESOLVED | Method stages do not define the common clock. |
| HRS | Event-driven CloudSim-style source experiment and task settings; no common end time or drain rule. | SOURCE-REQUIRED source context; exact horizon UNRESOLVED | Paper duration is not imported into the comparison. |
| DPRS | Analytical response-time/queue examples and source-specific thresholds; no common simulation duration. | SOURCE-REQUIRED model context; exact horizon UNRESOLVED | Queue/optimizer concepts do not define experiment termination. |
| OGSA | Optimizer generation limit, including source-specific iterations. | SOURCE-REQUIRED method-internal termination | Generations never define the common simulation horizon. |
| EIMORM | Dynamic cost/access concepts; no complete duration or stopping rule. | SOURCE-REQUIRED concepts; exact horizon UNRESOLVED | No source duration is promoted to the comparison. |
| Common project documents | CMP-RD-003 fixes the final workload timestamp at 7,200 seconds; CMP-RD-005 fixes failure/recovery event timestamps through that boundary. | COMMON-SIMULATOR-REQUIRED plus RESEARCHER-DECIDED boundary | The 7,200-second value becomes the common admission boundary, not a source-defined duration. |

##### Start and admission horizon

- Initial scenario construction occurs at `t = 0` with the CMP-RD-002 healthy/available state.
- `t = 0` is included as the initial state but has no CMP-RD-003 workload request.
- The first workload request is at `t = 6 s`.
- The common admission interval is **`[0, 7,200]` seconds**, inclusive.
- Every external workload, failure, and recovery event with timestamp `<= 7,200` is admitted and processed.
- `request-001200` at `t = 7,200 s` must be processed.
- No new external workload, failure, or recovery event is admitted after `t = 7,200`.

The 7,200-second boundary is a researcher-decided common admission horizon derived from the frozen CMP-RD-003/CMP-RD-005 artifacts. It does not claim that a source paper specifies a 7,200-second experiment.

##### Endpoint and drain semantics

The temporal policy is:

```text
Admission interval: [0, 7200]
Drain interval:     (7200, drain_end]
```

Already-admitted request completions and method-generated events causally triggered by admitted events may execute after `t = 7,200`. The simulator drains them until the causally descended event queue is empty. The drain is not a new workload window and does not admit new external events.

There is no arbitrary fixed cool-down duration. A deterministic implementation guard permits at most `100 x (number of admitted external events + number of registered failure/recovery events + 1)` post-horizon drain events. Reaching the guard marks the method run `TIMED_OUT`; it does not silently truncate the run or create a numerical result. This is a nontermination safeguard, not a scientific observation window.

##### Drain-guard classification and event-count semantics

The factor `100` is **not** a scientific experimental parameter, workload parameter, simulation-horizon parameter, performance-tuning parameter, method-specific parameter, evaluation parameter, or metric-normalization parameter. It is only a defensive execution-safety multiplier intended to prevent pathological or infinite causal event generation during post-admission draining. It is not theoretically optimal, empirically validated, or selected from observed results, and it must never be tuned to influence scientific outcomes.

The guard is event-based rather than a fixed number of seconds because the admission horizon is already fixed, post-horizon processing is causal draining rather than an additional scientific observation window, and a fixed extra time interval would introduce an arbitrary cooldown. The event-count guard limits pathological event generation without defining another scientific time horizon.

For this decision, an **admitted external event** is one workload/request event or one externally registered failure/recovery event whose timestamp is `<= 7,200`. Each failure event counts once and each recovery event counts once; a failure/recovery pair therefore counts as two events. Only events admitted at or before `7,200` enter the baseline. No post-horizon recovery event exists unless it was already registered and admitted under CMP-RD-005.

The common pre-drain baseline is fixed before method execution:

```text
baseline_event_count = admitted_workload_event_count
                     + admitted_failure_recovery_event_count
drain_budget = 100 x (baseline_event_count + 1)
```

The baseline never includes observed method performance or method-generated event counts. It is identical for all five methods in a matched run and cannot expand because one method creates more work.

The current executable event primitive is the repository's queued `Event`: an event is scheduled, assigned a deterministic sequence, popped, and dispatched. Therefore, once causal draining is implemented, **each executable queued event processed after the admission boundary consumes one drain-budget unit**, regardless of event type. A request root event, replication action event, transfer event, movement/replacement event, and completion event would each count individually if they are separate queued events. A single synchronous state mutation that is not represented as a queued event consumes no additional drain unit; the implementation must not invent event types merely to increase the budget.

The intended boundary is therefore:

- A: admitted external events establish the fixed baseline only.
- B: method-generated or causally descended events are not added to the baseline.
- C: every executable queued descendant processed during post-horizon draining consumes one unit.

The root event and every separate queued descendant are counted individually. This prevents a method from obtaining a larger guard by generating more descendants and applies the same formula and counting rule to Proposed NSGA-III, HRS, DPRS, OGSA, and EIMORM.

The current runtime does not yet implement complete method-generated event types, causal parent identities, drain counting, or a `TIMED_OUT` status. These are implementation requirements, not claims that the current runtime already performs this accounting.

If CMP-RD-006 later uses a shorter execution safeguard or if the drain guard is reached, the run retains partial observations and its technical status; CMP-RD-008 remains responsible for the complete raw-result schema.

##### Workload, failure, and method-generated events

- CMP-RD-003 request arrivals are admitted through `t = 7,200` only.
- CMP-RD-005 F0–F3 events at or before `t = 7,200` are processed; F4 remains unavailable through that boundary with no invented post-horizon recovery.
- Recovery events before or at `t = 7,200` are processed normally.
- A request arriving at `t = 7,200` may produce a completion after `t = 7,200`; that completion is drained if it was causally admitted.
- Method-generated replication, movement, replacement, optimization, and state-transition events triggered by admitted events may drain after `t = 7,200`.
- No method may extend the admission horizon because it has more work, and no method may terminate the common schedule early because it returns `UNRESOLVED`, `UNSUPPORTED`, or `NO_OP`.
- Method-internal generation/iteration limits remain method-specific and do not alter the common clock.

At equal timestamps, CMP-RD-005's common priority applies: failure/recovery transition, request arrival, method observation/decision, validated state transition, then request completion/observation. Within the same priority, the deterministic event sequence is the tie-break.

##### Termination predicate

The run terminates normally only when:

1. all external events with timestamp `<= 7,200` have been admitted and processed;
2. no new external event can be admitted;
3. all causally descended method-generated and already-started completion events have drained; and
4. the drain guard has not been exceeded.

An empty queue before the admission boundary is not normal completion; it is an incomplete schedule and marks the run `INVALID` unless the missing events were explicitly absent in the registered artifact. An event queue becoming empty after admission and causal drain is normal completion. A method decision status alone never terminates the common simulation.

##### Error and invalid-run handling

The temporal layer uses these technical statuses without resolving CMP-RD-008's complete result schema:

- `VALID`: normal admission and causal drain completed.
- `INVALID`: malformed event, invalid timestamp/order, invalid state transition, replay mismatch, or mandatory artifact validation failure.
- `UNRESOLVED`: a required method-specific policy is unresolved; preserve the method attempt and continue the common schedule where possible.
- `FAILED`: uncaught runtime exception or execution failure prevents that method run from completing.
- `TIMED_OUT`: drain guard or another pre-registered nontermination safeguard is reached.

Partial raw observations and termination reason must be retained. If the drain guard is exceeded, the run receives `TIMED_OUT`, is not treated as valid normal completion, and its events are not silently discarded. The run must not contribute a normal scientific result; its termination reason and partial execution remain auditable. Invalid, unresolved, failed, and timed-out attempts are not silently converted into metric values or ordinary aggregates. A method-specific failure does not regenerate common artifacts for the other methods.

##### Warm-up, cool-down, and metric boundary

- Warm-up: **0 seconds**; no initial observations are discarded.
- Primary admission window: `[0, 7,200]`.
- Drain observations after `7,200` are retained and separately identifiable.
- No steady-state requirement is imposed.
- No fixed cool-down window is imposed; only causal drain is allowed.
- CMP-RD-007 owns the definitions and aggregation of response time, availability, reliability, energy, cost, load, and network metrics. CMP-RD-006 defines only when observations can occur.

##### Algorithm iteration versus simulation time

OGSA GSA generations, Proposed NSGA-III population/generation limits, and any HRS, DPRS, or EIMORM internal loops are method-specific. They may stop an internal algorithm operation, but they do not stop, extend, or redefine the common simulation horizon.

##### Fairness and reproducibility

- All five methods start from `t = 0` and use the same inclusive admission horizon.
- All receive identical workload, failure, recovery, event-priority, endpoint, and drain rules.
- No method receives extra post-workload time; all admitted causal events use the same drain policy and guard.
- Method performance cannot alter termination or future external events.
- The horizon, admission interval, endpoint policy, drain policy/version, event-ordering version, termination reason, and run status must be part of the configuration/replay identity and provenance.
- CMP-RD-004's 30 repetitions and seed/stream identities remain unchanged.

##### Implementation consequences and gaps

The current runtime has a simulation clock, timestamped event queue, insertion ordering, and a horizon parameter, but it does not yet support the resolved protocol end to end. Gaps include explicit event priority, preserving events beyond a horizon, request completion events, method-generated event scheduling, causal drain mode, termination reasons/statuses, replay validation, failure/recovery integration, request scheduling from `Scenario.requests`, and provenance binding for horizon/drain configuration.

##### Validation requirements

The common simulator must validate:

- start time is `0` and all initial state is constructed before event processing;
- external timestamps are within the registered admission boundary;
- `t = 7,200` events are admitted;
- no new external event is admitted after the boundary;
- event priority and equal-time sequence ordering are deterministic;
- method-generated events are causally linked to admitted events;
- all five method runs use identical horizon, drain, ordering, and termination configuration identities;
- drain guard accounting is deterministic;
- invalid, unresolved, failed, and timed-out statuses retain partial observations and reasons;
- CMP-RD-005 F4 remains unavailable through `t = 7,200` without invented recovery.

##### Downstream dependencies

CMP-RD-007 owns metric definitions and observation aggregation. CMP-RD-008 owns the complete raw result schema. CMP-RD-009 owns statistical analysis. CMP-RD-010 owns visualization. CMP-RD-011 owns the final experiment matrix. CMP-RD-012 owns normalization/scaling. None of these decisions are resolved here.

Decision status:
RESOLVED / RESEARCHER-DECIDED.

Dependencies:
- CMP-RD-002 — Common Experimental Environment
- CMP-RD-003 — Dataset and Workload
- CMP-RD-004 — Randomness and Reproducibility
- CMP-RD-005 — Failure and Dynamic Scenario Protocol
- CMP-RD-007 — Common Evaluation Metrics
- CMP-RD-008 — Common Result Schema
- CMP-RD-009 — Statistical Analysis Protocol
- CMP-RD-011 — Experiment Matrix

Affected methods:
- Proposed Method / Proposed NSGA-III
- HRS
- DPRS
- EIMORM
- OGSA

Classification of key properties:

1. Common simulation horizon
   - Classification: UNRESOLVED.
   - Evidence: no source paper defines a common time horizon for the entire comparative experiment.
   - Interpretation: this is not a method-specific source property and must remain an experiment-design choice unless a paper explicitly fixes it.

2. Common simulation start time
   - Classification: UNRESOLVED.
   - Evidence: the common architecture assumes a time-aware simulation but does not define the initial simulation timestamp or start condition.
   - Interpretation: start time belongs to the common simulation setup and is not automatically derived from any algorithm-internal iteration counter.

3. Common simulation end time
   - Classification: UNRESOLVED.
   - Evidence: no source gives a fixed end timestamp or deadline for the common study.
   - Interpretation: final termination policy remains a researcher decision unless a source paper explicitly states a fixed horizon.

4. Common workload completion boundary
   - Classification: UNRESOLVED.
   - Evidence: workload content is defined in CMP-RD-003 as a common experiment concern, but no final completion rule is fixed.
   - Interpretation: this may later be time-based, workload-based, event-based, or hybrid, but the exact rule is not yet justified by the source evidence.

5. Fixed number of requests
   - Classification: UNRESOLVED.
   - Evidence: the project overview describes requests, but the final request count is not source-defined.

6. Fixed number of events
   - Classification: UNRESOLVED.
   - Evidence: the event infrastructure exists in the common architecture, but the exact event count is not fixed by the source papers.

7. Common simulation clock
   - Classification: SIMULATOR-DEFINED.
   - Evidence: the simulator owns simulation time, event ordering, and state change timing.

8. Decision whether the experiment uses a fixed time horizon
   - Classification: RESEARCHER-DEFINED.
   - Evidence: the architecture and comparison design require a common horizon decision, but the sources do not decide it.

9. Decision whether the experiment terminates on workload completion
   - Classification: RESEARCHER-DEFINED.
   - Evidence: no source paper defines a global workload completion condition for all methods.

10. Decision whether the experiment terminates on event-queue exhaustion
    - Classification: RESEARCHER-DEFINED.
    - Evidence: the architecture supports dynamic events and request processing, but no final policy is given.

11. Decision whether the experiment uses a maximum time safety guard
    - Classification: RESEARCHER-DEFINED.
    - Evidence: time-aware simulation implies a need for stopping safeguards, but the exact maximum time is not source-defined.

12. Warm-up period or discarded initial observations
    - Classification: UNRESOLVED.
    - Evidence: no source paper or project architecture document explicitly defines a warm-up period.

13. Measurement window
    - Classification: UNRESOLVED.
    - Evidence: the architecture and metric layer require measurement windows, but their exact boundaries are not specified by source evidence.

14. Post-failure recovery or observation window
    - Classification: UNRESOLVED.
    - Evidence: CMP-RD-005 defines the external failure artifact, and CMP-RD-006 now defines the common admission horizon and termination policy.

15. Common simulation duration metadata in result logs
    - Classification: SIMULATOR-DEFINED.
    - Evidence: the simulator must record how long a run executed and why it ended, but the exact horizon value is not fixed by source evidence.

Method-specific source checks:

- Proposed Method / Proposed NSGA-III
  - Overall proposed strategy is multi-stage and time-aware: SOURCE-DEFINED.
  - OIS evaluation and dynamic replica timing are source-defined within the Proposed Method contract: SOURCE-DEFINED.
  - Dynamic replica-number determination is source-defined as an algorithm behavior: SOURCE-DEFINED.
  - NSGA-III placement optimization has a maximum placement-iteration concept in the implementation contract: SOURCE-DEFINED.
  - The NSGA-III internal maximum iteration count is not automatically the common simulation horizon: UNRESOLVED as a cross-method interpretation; it is algorithm-internal and must remain distinct from the common experiment horizon.
  - Common simulation duration for the whole experiment: UNRESOLVED.
  - Common start condition and end condition: UNRESOLVED.
  - Replacement under storage constraints: SOURCE-DEFINED only within the method logic, not as a global stop condition: SOURCE-DEFINED for the decision stage, UNRESOLVED for common experiment timing.

- HRS
  - Source-defined placement and replacement logic: SOURCE-DEFINED.
  - Source-defined simulation duration: UNRESOLVED.
  - Source-defined request count or event count: UNRESOLVED.
  - Source-defined termination condition: UNRESOLVED.
  - Initial random placement is source-defined, but it is not a statement about the global simulation horizon: SOURCE-DEFINED for initial placement; UNRESOLVED for global timing.
  - Fuzzy replacement is method-specific behavior and must not be treated as a common simulation stop rule: SOURCE-DEFINED as a decision mechanism; UNRESOLVED as a global termination condition.

- DPRS
  - Request-intensive processing and queue-based service behavior are described in the source and contract: SOURCE-DEFINED at the request/service-model level.
  - Global simulation duration or termination rule: UNRESOLVED.
  - Infinite request queue or request processing assumptions are source-level modeling descriptions, not the final experiment horizon: UNRESOLVED for common experiment timing.
  - Dynamic adaptation and request handling are not equivalent to a common simulation stop criterion: UNRESOLVED.

- EIMORM
  - ETBDF, EARF, IEK, and dynamic cost-aware operations are source-defined conceptual components: SOURCE-DEFINED.
  - Exact simulation duration and end-of-run rule: UNRESOLVED.
  - Time-based metrics and dynamic evaluation intervals are not automatically a common simulation horizon: UNRESOLVED.
  - CloudSim-related experiment duration, if used in the source context, remains source-specific experimental detail rather than a common comparison horizon unless the project explicitly adopts it: UNRESOLVED.

- OGSA
  - Population size and maximum number of iterations are source-defined optimizer parameters: SOURCE-DEFINED.
  - The optimizer termination condition based on max iterations is source-defined: SOURCE-DEFINED.
  - The optimizer iteration count must not be equated with the entire common simulation duration: UNRESOLVED if the project treats it as a global horizon; it must remain distinct as algorithm-internal execution.
  - Common simulation horizon across all algorithms: UNRESOLVED.
  - Failure probability as an availability-model input is source-defined, but it is not automatically a runtime failure schedule or a stop condition: SOURCE-DEFINED for the model input; UNRESOLVED for dynamic failure generation and runtime termination.

Critical distinction: common simulation horizon vs algorithm-internal iteration limits

A fair comparison may have one common simulation clock and one external workload, while each algorithm internally has its own:
- optimization loop,
- generation count,
- convergence behavior,
- solver iteration count,
- internal termination logic.

This distinction is required by the architecture and must not be collapsed.

Examples:
- OGSA maximum generations: SOURCE-DEFINED as algorithm-internal optimizer termination.
- Proposed NSGA-III maximum placement iterations: SOURCE-DEFINED as algorithm-internal optimization control.
- Common experiment duration for all five methods: UNRESOLVED until the researcher chooses it.

The common simulation horizon is a project-level comparison boundary, not an algorithm parameter that can be inherited from one method without explicit source support.

Start-condition classifications

1. Initial simulation time
   - Classification: UNRESOLVED.
   - Evidence: the common architecture defines a time-aware system but no start timestamp or initial time is fixed.

2. Initial node state
   - Classification: RESEARCHER-DEFINED for the experiment configuration; SIMULATOR-DEFINED for runtime construction.
   - Evidence: common topology and resource state are required, but the precise initial state is not fixed yet.

3. Initial file population
   - Classification: RESEARCHER-DEFINED for the experiment; SIMULATOR-DEFINED for runtime setup.
   - Evidence: the dataset and workload are part of the comparison environment, but their exact initialization is not fixed.

4. Initial replica state
   - Classification: RESEARCHER-DEFINED for the experiment; SIMULATOR-DEFINED for runtime state creation.
   - Evidence: the architecture requires a common initial state, but the precise initial replica catalog is not fixed in source evidence.

5. Initial request queue and workload state
   - Classification: RESEARCHER-DEFINED for the workload design; SIMULATOR-DEFINED for runtime scheduling.
   - Evidence: the common workload is required, but its initial state is unresolved.

6. Initial popularity or access history
   - Classification: RESEARCHER-DEFINED for the experiment; SOURCE-DEFINED in the method-specific model where the algorithm defines its own popularity/importance interpretation.
   - Evidence: the common domain model includes file access history and popularity metadata, but no final distribution is fixed.

7. Initial storage utilization
   - Classification: RESEARCHER-DEFINED for the experiment; SIMULATOR-DEFINED for this state calculation.
   - Evidence: storage utilization depends on the chosen common workload and initial replica state.

8. Initial failures
   - Classification: UNRESOLVED unless CMP-RD-005 explicitly chooses a failure model.
   - Evidence: the project requires common failure infrastructure, but no source paper defines the initial failure state.

9. Initial optimization population or algorithm-specific search state
   - Classification: SOURCE-DEFINED for the method-specific algorithm only when the source defines it.
   - Evidence: this is algorithm-internal state and not part of the common simulation horizon.

Termination-condition classifications

1. Fixed simulation time
   - Classification: RESEARCHER-DEFINED if chosen; UNRESOLVED as a current project decision.
   - Evidence: the project architecture expects time-aware simulation, but no fixed common duration is given.

2. Fixed number of requests
   - Classification: RESEARCHER-DEFINED if chosen; UNRESOLVED in the current evidence.

3. Fixed number of events
   - Classification: RESEARCHER-DEFINED if chosen; UNRESOLVED in the current evidence.

4. Completion of workload
   - Classification: RESEARCHER-DEFINED if chosen; UNRESOLVED in the current evidence.

5. Completion of all requests
   - Classification: RESEARCHER-DEFINED if chosen; UNRESOLVED in the current evidence.

6. Optimizer generation limit
   - Classification: SOURCE-DEFINED for the method-specific optimizer behavior when the source defines one; not the common simulation horizon.
   - Example: OGSA maximum iterations is SOURCE-DEFINED at the algorithm level.

7. Convergence or stability criterion
   - Classification: SOURCE-DEFINED only if the source explicitly defines it; otherwise UNRESOLVED.
   - Evidence: the algorithm papers may refer to best fitness or convergence, but the common experiment does not inherit this as a global stop rule.

8. Resource exhaustion
   - Classification: RESEARCHER-DEFINED or SIMULATOR-DEFINED depending on the concrete experiment policy; currently UNRESOLVED.

9. Failure or recovery completion
   - Classification: UNRESOLVED unless CMP-RD-005 specifically defines a failure/recovery protocol.
   - Evidence: current evidence is explicitly open in CMP-RD-005.

10. No pending events
    - Classification: SIMULATOR-DEFINED as a generic event-queue termination aid.
    - Evidence: the common simulator can stop when no queued events remain, but this is not equivalent to a source-defined algorithm termination rule.

11. Explicit stopping condition in a source method
    - Classification: SOURCE-DEFINED for the method-specific algorithm when provided; e.g., OGSA maximum iterations.
    - Evidence: this does not automatically define the common comparison horizon.

12. Timeout or global deadline
    - Classification: RESEARCHER-DEFINED if used in the final experiment; UNRESOLVED in the source evidence.

Workload-based versus time-based versus event-based evidence

A. Time-based simulation
   - Evidence: the project overview and common architecture both require time-aware simulation.
   - Classification: RESEARCHER-DEFINED for the exact duration or time policy; UNRESOLVED until selected.

B. Workload-based simulation
   - Evidence: the project architecture and workload model require request streams and common dataset handling.
   - Classification: RESEARCHER-DEFINED for the exact stopping policy; UNRESOLVED in the current evidence.

C. Event-based simulation
   - Evidence: event scheduling and failure/recovery infrastructures are part of the common simulation architecture.
   - Classification: SIMULATOR-DEFINED for the event mechanism itself; RESEARCHER-DEFINED for the chosen stopping policy; UNRESOLVED for exact event-count termination.

D. Hybrid policies
   - Evidence: the architecture is compatible with hybrid policies, but the source papers do not specify a final hybrid rule.
   - Classification: UNRESOLVED unless a future researcher decision explicitly adopts a hybrid boundary.

Dynamic and failure interaction with the simulation horizon

The common simulation horizon must remain separate from:
- failure occurrence rate,
- failure timing,
- node recovery timing,
- request variability,
- popularity change,
- storage pressure,
- algorithm-triggered re-optimization,
- replacement events,
- re-replication events,
- optimization loop termination.

This distinction is required because CMP-RD-005 defines external failure events but does not resolve the final horizon. If a method-specific failure trigger is unresolved, CMP-RD-006 must not silently resolve it.

Examples:
- A failure schedule is not automatically a simulation horizon.
- A periodic trigger is not automatically implied by any time horizon.
- Dynamic events may be event-triggered, workload-triggered, failure-triggered, or algorithm-triggered, but those semantics are unresolved unless the source explicitly defines them.

Warm-up and measurement-window evidence

- Warm-up period: UNRESOLVED.
- Discarded initial observations: UNRESOLVED.
- Steady-state measurement window: UNRESOLVED.
- Observation period after failure or recovery: UNRESOLVED.
- Measurement window as a subset of the simulation horizon: UNRESOLVED unless the project later defines one.

No source paper defines a warm-up protocol or a measurement window boundary. Therefore the exact rules remain OPEN and must not be inferred from generic simulation practice.

Fair comparison and researcher boundary

The project requirements emphasize a common external experiment with source-faithful internal algorithm execution.

This implies:
- the same external scenario, workload, topology, request stream, and failure schedule should be shared across all five methods,
- the same common simulation clock and duration should be applied across methods,
- algorithm-internal iteration counts must not replace the common simulation horizon,
- a method must not be stopped early or extended selectively based on observed results.

These are fairness conditions and researcher decisions, not source-defined algorithm properties.

Experimental integrity guardrails

This decision must not invent any of the following:
- simulation duration,
- start timestamp,
- end timestamp,
- request count,
- event count,
- number of generations for the common simulator,
- warm-up duration,
- convergence threshold,
- stopping threshold,
- timeout,
- global measurement window,
- result-dependent termination.

The source audit remains unresolved, but the researcher policy above resolves the common horizon without claiming source-defined duration.

Decision:
RESOLVED — RESEARCHER-DECIDED

---

### CMP-RD-007 — Common Evaluation Metrics

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Document which metric concepts are algorithm-native for each source method, which metric concepts are measurable by the common simulator across the five methods, and which definitions remain unresolved for later researcher decision.

Why this decision is required:
The comparison architecture requires a common evaluation layer, but the source papers do not define one final, shared metric set or a single cross-method formula for each metric. The comparison layer therefore must preserve the distinction between source-native optimization objectives and simulator-measured comparison metrics.

Current evidence:
The evidence is distributed across the project architecture and the method-specific specifications:

- [docs/01-project-overview.md](docs/01-project-overview.md) requires a controlled, reproducible, common simulation environment and requires metrics to be recorded at the simulation level.
- [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) names common metrics and requires raw metric capture for later aggregation, but it does not set a final metric vector.
- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) requires the simulator to own metrics collection and result export without collapsing the algorithm objective into the simulator metric layer.
- [docs/06-common-domain-model.md](docs/06-common-domain-model.md) defines shared runtime state such as requests, files, nodes, requests, timing, and node health, which is required to compute a common metric set.
- [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md) states that algorithm adapters return source-defined decisions, while the simulator owns state mutation and metric recording.
- [docs/Proposed-Method-Implementation-Contract.md](docs/Proposed-Method-Implementation-Contract.md) defines the Proposed Method's five objective dimensions and explicitly separates them from evaluation metrics such as reliability and availability.
- [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) defines OGSA objective names and a weighted multi-objective optimization model, but it does not make these identical to a final common comparison metric list.
- [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) defines placement, selection, and fuzzy replacement metrics but not a full common comparison metric set.
- [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md) defines response-time components and placement-related quantities, but not a consistent cross-method comparison metric set.
- [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md) defines availability, cost, load balancing, and dynamic cost-aware rebalancing concepts, but it does not provide a complete, executable formal objective vector equivalent to the Proposed Method's NSGA-III formulation.

Researcher decision:
The final common metric protocol is defined below. It separates source-native objectives from externally measured metrics and does not resolve normalization, statistical analysis, result schema, visualization, experiment matrix, or scaling.
- the final common metric set,
- the measurement semantics for each metric,
- the raw per-run measurement fields required by the simulator,
- the metric boundaries for each method,
- the final common comparison criterion used in the thesis.

The source papers do not provide a complete common formula suite; concrete common definitions below are RESEARCHER-DECIDED harmonizations supported by COMMON-SIMULATOR-REQUIRED raw observations.

#### CMP-RD-007 Researcher Decision

##### Final primary metric set

| Metric | Definition | Unit | Direction | Temporal/observation scope | Failure handling | Classification |
|---|---|---|---|---|---|---|
| Request response time | For every request reaching a terminal outcome, `completion_timestamp - arrival_timestamp`. Failed requests have no response-time value. | Seconds | Minimize | Per-request; admission-window requests and their causal drain completions are retained separately. | Unavailable/failed requests are recorded with cause, not assigned zero response time. | RESEARCHER-DECIDED common operational definition; COMMON-SIMULATOR-REQUIRED timestamps. |
| Request reliability | `successful admitted read accesses / all admitted read accesses`. One admitted CMP-RD-003 read request is one required data-access event; the denominator includes every request arrival in `[0,7200]`, regardless of outcome. The numerator includes only requests with a terminal successful service outcome from the common request executor. | Dimensionless proportion | Maximize | Request-level over admitted requests; causal drain completions remain attributable to their admitted request and are tagged post-horizon. | An admitted request that cannot be served because data is unavailable/unreachable is unsuccessful. No deadline, timeout, retry, placement-success, optimizer-success, or exception-absence rule is added here. Failed requests remain in the denominator. | RESEARCHER-DECIDED common operational definition; COMMON-SIMULATOR-REQUIRED terminal outcomes. |
| Service availability | For a required file at time `t`, serviceability is true only when at least one catalogued replica is valid, complete under the common file model, hosted on a healthy and reachable node, and connected to the requesting source node by a valid path whose directed links are available. Availability is the time-weighted serviceable interval over `[0,7200]`. | Proportion `[0,1]` | Maximize | Per-file and system-wide over the inclusive CMP-RD-006 admission interval; denominator is exactly 7,200 seconds and post-horizon drain is excluded. Intervals are partitioned at failure, recovery, link, and replica-state transitions. | Failed-node/link intervals remove serviceability while preserving replica metadata; recovery restores it when a valid path returns. File aggregation weighting remains an explicit implementation/aggregation detail, not a hidden rule. | RESEARCHER-DECIDED common state-based definition; COMMON-SIMULATOR-REQUIRED interval/path instrumentation. |
| Active replica count | Number of valid catalog replicas at an observation point; report total valid replicas and currently reachable valid replicas separately. | Replica count | Descriptive; no universal optimize direction | Initial, event-level, final, time-weighted mean, and peak diagnostic observations. | Replicas on failed nodes remain catalogued/valid but are not active/reachable. Deleted replicas cease counting after the recorded deletion event. | RESEARCHER-DECIDED common diagnostic metric. |
| Network transfer volume | Sum of payload bytes actually transferred for request service and accepted replication/movement events; request-serving and replication traffic are separate components. | Bytes or GiB | Descriptive; lower is generally preferable but no optimization direction is imposed | Event-level and per-run over admission plus causal drain, with post-horizon traffic tagged. | Failed transfers count only if actual attempted bytes are recorded; no inferred bytes are fabricated. | RESEARCHER-DECIDED common operational metric. |
| Algorithm decision time | Elapsed wall-clock or CPU time used by an adapter to compute a decision, with clock type recorded; it is not request response time or simulation time. | Milliseconds | Minimize as an operational diagnostic | Per-decision and per-run; method computation only. | Unresolved/failed decisions retain measured time where available and status otherwise. | RESEARCHER-DECIDED common diagnostic metric. |

This is the smallest primary set selected to cover response performance, reliability/availability, replication state, network activity, and algorithm overhead without inventing energy, cost, load, or centrality models unavailable in the current common runtime.

##### Reliability and availability precision boundary

For reliability, `total required accesses` means all 1,200 admitted read requests in the selected CMP-RD-003 workload artifact, including requests that fail during F0–F4 conditions. Internal retries, replica-selection attempts, replication actions, and method-generated accesses are not additional denominator events. A slow request that eventually receives a terminal successful service outcome is reliable even though its response time may be large. A failed request receives no fabricated response-time value.

The successful-access predicate is intentionally execution-based: the common request executor must observe that the requested file was actually served and reached a terminal successful outcome. An algorithm placement decision, accepted mutation, optimizer result, absence of an exception, or presence of a catalog replica alone is insufficient. The current runtime does not implement this request completion/outcome lifecycle, so the metric definition is resolved but its execution predicate remains an **IMPLEMENTATION GAP**.

For availability, a `required file` is a file named by the common workload request being evaluated at time `t`; the metric does not silently treat every catalog file as continuously required. The common metric layer must preserve file-level intervals and defer the exact system-wide file aggregation weighting to an explicitly documented implementation/aggregation choice without selecting it from observed results. A `valid replica` is a catalogue entry that is not deleted/invalid and represents the complete file under the common file model; it is not necessarily serviceable. A replica on a failed node or across an unavailable link remains catalogued but is inactive until health, reachability, and path conditions return.

The valid path uses the frozen common directed topology and current link availability; it is not DPRS's method-specific graph construction. The current runtime has node/link fields but no path validation or interval ledger, so these are **IMPLEMENTATION GAPS**. Primary and additional replicas both count as candidate valid replicas; failure does not delete metadata, and recovery does not invent repair or re-replication.

Request reliability and service availability are distinct: reliability is a request-level terminal outcome, while availability is time-dependent serviceability of the workload-required file. A file may be serviceable while a request fails for a separately observed execution reason; an unavailable file can cause an unsuccessful request; and a request for one file does not become unsuccessful because another file is unavailable. No new failure causes are invented by this distinction.

##### Conditional metrics and exclusions

Energy consumption, total cost, data-node load, and network/closeness centrality are retained as conditional secondary candidates, not final primary metrics. They may be added only after their common operational models are independently specified before execution:

- Energy requires a declared per-node power model integrated over simulated time, including active/idle/communication boundaries and Joules.
- Total cost requires declared storage occupancy, transfer, computation, and currency/unit rules; no paper-specific pricing is imported.
- Data-node load requires a declared scalar/vector of CPU, memory, storage, disk-I/O, and time aggregation; these are not conflated without a later decision.
- Centrality requires a declared graph, directed/undirected treatment, edge weights, unreachable handling, selected node set, and aggregation.

The following remain diagnostics or method-internal quantities rather than additional primary metrics: native fitness/objective values, Pareto quality, convergence, number of non-dominated solutions, raw latency components, queue time, service time, storage utilization, replication overhead, replication time, request counts, failed/successful request counts, and peak/mean replica counts. They remain available as raw observations where implemented.

##### Objective versus evaluation boundary

The Proposed five-objective vector remains source-native: Energy Consumption, Response Time, Data Node Load, Total Cost, and Network Centrality, with its source-defined objective directions. OGSA's MFU, MST, LV, EC, and ML remain OGSA-native objectives under its OBL + GSA project interpretation. HRS Merit/TotalCost/fuzzy values, DPRS response-time components, and EIMORM availability/cost/ETBDF/IEK concepts remain method-internal or source-specific.

None of those native objectives or fitness values is automatically substituted for a common metric. A common metric is computed from the same simulator-level operational observations for all five methods.

##### Temporal and failure semantics

- Response time, reliability, active replicas, transfer volume, and decision time use request/event observations from the CMP-RD-006 admission interval and causal drain, with drain records explicitly tagged.
- Service availability uses only the fixed `[0,7200]` admission interval as its denominator; no arbitrary cooldown is added.
- Fixed initial population and failed-node/link state use the common CMP-RD-002/CMP-RD-005 semantics.
- Failed, unresolved, invalid, and timed-out runs retain raw observations and statuses but are not silently converted into ordinary metric values. CMP-RD-009 owns later statistical treatment.
- The fixed common node population remains the reference population for state observations; a failed node contributes operational availability as unavailable during its outage rather than being silently removed.
- The availability predicate is evaluated using the same common topology, health, reachability, directed-link, and replica-state semantics for all five methods; no method chooses which requests or files enter the denominator.

##### Raw-observation provenance

Each metric record must be traceable to raw observations carrying experiment ID, scenario ID, workload ID, failure class/artifact ID, repetition ID, method ID, configuration/replay identity, timestamp or interval, termination status, and implementation/source versions.

Required provenance paths include:

- response time -> request arrival and completion records;
- reliability -> request terminal outcome records and failure causes;
- service availability -> file/replica/node/link state intervals;
- active replicas -> replica catalog state transitions;
- transfer volume -> transfer event payload/byte records;
- decision time -> adapter start/end timing records.

This does not define CMP-RD-008's complete result schema.

##### Normalization and statistical boundary

All primary metrics are recorded in raw physical or dimensionless units. No cross-method normalization, inversion, weighting, pooled scaling, confidence interval, significance test, or final aggregation rule is selected here. CMP-RD-009 owns statistical analysis; CMP-RD-012 owns normalization/scaling; CMP-RD-008 owns the complete result schema; CMP-RD-010 owns visualization.

##### Fairness and double-counting audit

- All five methods use identical metric definitions, temporal boundaries, failure semantics, and raw-observation requirements.
- Method-internal fitness, normalization, objective weights, or optimizer scores cannot enter a common metric.
- Response time is end-to-end request latency; algorithm decision time is separate.
- Service availability is time-based; request reliability is request-based.
- Active replica count is descriptive state, not a second availability metric.
- Network transfer volume is traffic, not response time or cost.
- Conditional energy, cost, load, and centrality are excluded until common instrumentation exists, avoiding arbitrary formulas and method advantage.

##### Implementation consequences and gaps

The runtime currently supports only part of the required provenance foundation. It has request arrival fields, node/replica/link state, topology, event timestamps, and raw observation records, but lacks request start/completion/outcome lifecycle, transfer/path/byte accounting, energy ledger, common cost ledger, explicit CPU/memory/I/O utilization, integrated availability intervals, complete primary/replica semantics, typed metric records, and metric aggregation instrumentation. No metric implementation is added by this decision.

##### Validation requirements

The future metric layer must validate that:

- every response-time observation has one valid arrival and terminal completion record;
- failed requests are never assigned fabricated response times;
- every reliability denominator record corresponds to one admitted CMP-RD-003 read request, including requests that later fail;
- a reliability numerator record requires observed terminal successful service by the common request executor;
- no placement decision, optimizer status, exception absence, or replica count is accepted as a proxy for request success;
- reliability denominators and terminal outcomes are explicit;
- availability intervals do not overlap or silently omit state transitions;
- every availability interval identifies the requested file, replica validity, hosting-node health/reachability, directed path, and link availability;
- the availability denominator is exactly the 7,200-second `[0,7200]` admission interval and excludes causal drain time;
- replica counts distinguish valid catalogued from reachable/active replicas;
- transfer bytes are observed, not inferred from a method objective;
- decision-time clock type is recorded;
- metric records carry matched scenario/workload/failure/repetition/method identities;
- invalid/unresolved/failed/timed-out statuses remain auditable;
- no method-specific fitness or normalization enters common metrics.

##### Downstream dependencies

CMP-RD-008 remains responsible for the complete raw/result schema. CMP-RD-009 remains responsible for statistical analysis and aggregation. CMP-RD-010 remains responsible for visualization. CMP-RD-011 remains responsible for the final experiment matrix. CMP-RD-012 remains responsible for normalization/scaling. None is resolved here.

Decision status:
RESOLVED / RESEARCHER-DECIDED.

Dependencies:
- CMP-RD-003 — Dataset and Workload
- CMP-RD-004 — Randomness and Reproducibility
- CMP-RD-005 — Failure and Dynamic Scenario Protocol
- CMP-RD-006 — Simulation Horizon and Termination
- CMP-RD-008 — Common Result Schema
- CMP-RD-009 — Statistical Analysis Protocol
- CMP-RD-010 — Visualization Protocol
- CMP-RD-011 — Experiment Matrix
- CMP-RD-012 — Normalization and Scaling Boundary

Affected methods:
- Proposed Method / Proposed NSGA-III
- HRS
- DPRS
- EIMORM
- OGSA

Classification vocabulary for this section:
- SOURCE-DEFINED
- RESEARCHER-DEFINED
- SIMULATOR-DEFINED
- UNRESOLVED

Only one label is used for each agreed property.

A. Algorithm-native objectives / metrics

1. Proposed Method — source-native objective vector
   - Classification: SOURCE-DEFINED.
   - Evidence: [docs/Proposed-Method-Implementation-Contract.md](docs/Proposed-Method-Implementation-Contract.md) explicitly states the five optimization objectives as:
     1. Energy Consumption
     2. Response Time
     3. Data Node Load
     4. Total Cost
     5. Network Centrality
   - Important boundary: these are source-native objective dimensions for the Proposed Method's NSGA-III placement stage. They are not automatically the final common comparison metric set for all five methods.
   - Status of formulas, weights, units, normalization, aggregation rule: UNRESOLVED at the comparison level unless the project contract explicitly defines them.

2. Proposed Method — objective direction and objective meaning
   - Classification: SOURCE-DEFINED for the naming and conceptual objective roles.
   - Evidence: the source contract describes the objective vector as a multi-objective placement problem and states that reliability and availability are kept as evaluation metrics rather than NSGA-III objectives.
   - Important boundary: this is algorithm-native and must remain distinct from any common metric chosen later.
   - Exact direction, weight scheme, and normalization: UNRESOLVED at the comparison layer unless separately fixed in the project contract.

3. Proposed Method — reliability and availability as evaluation metrics only
   - Classification: SOURCE-DEFINED.
   - Evidence: [docs/Proposed-Method-Implementation-Contract.md](docs/Proposed-Method-Implementation-Contract.md) explicitly states that reliability and availability are not NSGA-III objectives and are retained as evaluation metrics only.
   - Important boundary: evaluation metrics can be measured externally even when not used as an optimization objective by the Proposed Method.

4. HRS — native selection and ranking quantities
   - Classification: SOURCE-DEFINED.
   - Evidence: [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) defines Merit, TotalCost, VM capability C, VM load L, network performance N, fuzzy input parameters (number of accesses, cost, last access time), and fuzzy output value of replica.
   - Important boundary: these are HRS-native decision quantities, not automatically the final common comparison metrics.
   - Whether each of these is a final cross-method comparison metric: UNRESOLVED.

5. HRS — explicit response time and cost components
   - Classification: SOURCE-DEFINED.
   - Evidence: [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) gives response time as an observed outcome and defines costs and replica value using fuzzy logic.
   - Important boundary: response time and cost are part of HRS's native decision logic, not necessarily the final common comparison metric definitions.
   - Exact final comparison semantics of these quantities: UNRESOLVED.

6. DPRS — source-native response-time and placement quantities
   - Classification: SOURCE-DEFINED.
   - Evidence: [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md) defines dataset response time components: wait access latency, write/read time, transfer time, total response time, and usage frequency over a time window.
   - Important boundary: these are source-defined placement and response-time constructs, not necessarily a universal metric vector across all methods.
   - Final cross-method metric interpretation: UNRESOLVED.

7. DPRS — replica count, replacement, deletion, and failure-handling mechanism
   - Classification: UNRESOLVED.
   - Evidence: [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md) and [docs/algorithms/DPRS-implementation-contract.md](docs/algorithms/DPRS-implementation-contract.md) explicitly state that full lifecycle behaviors such as deletion, replacement, failure handling, and recovery are not defined in the source or are not a primary part of the method specification.
   - Important boundary: the absence of a source-defined mechanism must not be silently created during comparison metric design.

8. EIMORM — source-defined concepts that are not a formal executable objective vector
   - Classification: SOURCE-DEFINED.
   - Evidence: [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md) defines availability, cost-aware re-replication, dynamic balancing, ETBDF, EARF, IEK, and cost/availability considerations.
   - Important boundary: EIMORM is not to be converted into a fabricated formal five-objective vector equivalent to the Proposed Method.
   - Exact formal objective vector for comparison: UNRESOLVED.

9. EIMORM — cost and availability semantics
   - Classification: SOURCE-DEFINED at the conceptual level.
   - Evidence: the source discusses cost, file/block availability, and adaptation under load and budget constraints.
   - Important boundary: these are source-defined concepts, but the exact cross-method metric equation is not fixed.
   - Final metric operational meaning: UNRESOLVED.

10. OGSA — source-native objective names
    - Classification: SOURCE-DEFINED.
    - Evidence: [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) explicitly names the objective components as:
      - MFU
      - MST
      - LV
      - EC
      - ML
    - These correspond to the source paper's multi-objective formulation of mean file unavailability, mean service time, load variance, energy consumption, and mean latency.
    - Important boundary: these remain OGSA's native objective model and should not be replaced by the Proposed Method's objective vector.

11. OGSA — source-native weighted objective model
    - Classification: SOURCE-DEFINED.
    - Evidence: [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) describes a weighted multi-objective optimization formulation with proportion variables α1..α5 and a population-based optimizer.
    - Important boundary: the source provides objective names and a weighted formulation, but the project comparison layer must not assume the same weighting or objective semantics apply to the other four methods.
    - Exact final common weighting or normalization policy: UNRESOLVED.

B. Common evaluation metrics and raw measurement requirements

The common simulator is allowed to measure common quantities after execution, but that does not mean those quantities are source-native objectives for every algorithm.

12. Response Time
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: the project and source methods all discuss response time, but the exact common operational definition is not fixed uniformly across all five methods.
    - Measurement requirement: SIMULATOR-DEFINED for recording request timestamps, replica availability timestamps, and completion timestamps.
    - Important boundary: response time must not mean algorithm optimizer runtime in one method and end-user request latency in another unless the metric is explicitly separated.

13. Availability
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: availability is discussed in the Proposed Method, EIMORM, and OGSA, but the exact time-window definition and the exact system boundary are not jointly fixed for the five-method comparison.
    - Measurement requirement: SIMULATOR-DEFINED for system-state tracking of valid/healthy/reachable replicas and time spent in a valid state.
    - Important boundary: availability is a common comparison metric candidate, not necessarily a universal algorithm objective.

14. Reliability
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: the Proposed Method explicitly treats reliability as an evaluation metric rather than an NSGA-III objective; other methods discuss availability and failure in different ways.
    - Measurement requirement: SIMULATOR-DEFINED for request-success and request-failure recording.

15. Energy Consumption
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: energy is explicitly named in the Proposed Method and OGSA objectives and appears in the architecture requirements, but the exact energy model and system boundary are not fixed across all methods.
    - Measurement requirement: SIMULATOR-DEFINED for per-node, per-event, or per-request energy-accounting fields.

16. Data Node Load
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: data-node load is a Proposed Method objective and appears in the broader architecture, but the exact load metric and normalization rule are not fixed for the common comparison layer.
    - Measurement requirement: SIMULATOR-DEFINED for per-node utilization and workload accounting.

17. Total Cost
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: total cost appears in Proposed Method and HRS; it is a source-defined decision quantity in HRS and an objective in Proposed Method, but the exact cross-method common cost structure is not fixed.
    - Measurement requirement: SIMULATOR-DEFINED for cost-accounting events, transfer accounting, and storage cost ledger entries.

18. Network Centrality / Closeness Centrality
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: HRS explicitly uses centrality in placement decisions and the Proposed Method includes Network Centrality as an objective. The common evaluator could compute a topology-derived centrality measure if the final experiment defines it.
    - Measurement requirement: SIMULATOR-DEFINED for topology graph and site-distance data.
    - Important boundary: centrality may be measured after execution even when it is not a baseline objective.

19. Failed Requests
    - Classification: SIMULATOR-DEFINED.
    - Evidence: request success/failure tracking is part of the shared runtime model in [docs/06-common-domain-model.md](docs/06-common-domain-model.md) and [docs/01-project-overview.md](docs/01-project-overview.md).
    - Important boundary: this is a raw measurement category, not a source-defined optimization objective for all methods.

20. Successful Requests
    - Classification: SIMULATOR-DEFINED.
    - Evidence: the common request model requires success/failure logging.

21. Replica Count
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: the architecture and common domain model include files and replicas, but no single final replica-count metric definition is fixed for all five methods across different source models.
    - Measurement requirement: SIMULATOR-DEFINED for replica catalog state and per-file replica count snapshots.

22. Storage Utilization
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: storage state is part of the common domain model, but the final comparison metric boundary, whether time-averaged or instantaneous, is not fixed.
    - Measurement requirement: SIMULATOR-DEFINED for node-level storage accounting.

23. Network Traffic / Data Transfer
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: transfer time, bandwidth, latency, and network performance are discussed by DPRS and HRS, but the final common network-traffic metric is not fixed.
    - Measurement requirement: SIMULATOR-DEFINED for transfer logs and network link state.

24. Algorithm Execution Time
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: algorithm execution time may be measured, but it must not be conflated with request response time or simulation duration.
    - Measurement requirement: SIMULATOR-DEFINED for method runtime timing.
    - Important boundary: algorithm runtime is not the same as end-user response time.

25. Replication Time
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: replication timing is discussed by the Proposed Method and HRS, but no single common replication-time metric is fixed for all methods.
    - Measurement requirement: SIMULATOR-DEFINED for replica creation and deletion timestamps.

26. Replication Overhead
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: overhead concepts appear in the architecture and in source papers, but the exact boundary and accounting rule are not fixed.
    - Measurement requirement: SIMULATOR-DEFINED for counts and transfer events associated with replication actions.

27. Request Completion Rate
    - Classification: UNRESOLVED as a final common metric definition.
    - Evidence: completion rate is a natural aggregate over request success/failure, but the exact metric definition and aggregation rule are not fixed.
    - Measurement requirement: SIMULATOR-DEFINED for raw request records.

28. Raw per-request measurement records
    - Classification: SIMULATOR-DEFINED.
    - Evidence: [docs/06-common-domain-model.md](docs/06-common-domain-model.md) and [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) require shared request state, timestamps, and event records.
    - Important boundary: these are raw recording requirements, not final aggregated statistics.

29. Raw per-node measurement records
    - Classification: SIMULATOR-DEFINED.
    - Evidence: the common environment records state for nodes, storage, capacity, health, and load.

30. Raw per-event measurement records
    - Classification: SIMULATOR-DEFINED.
    - Evidence: the common simulator owns event scheduling and state transitions, including request processing and replica actions.

31. Raw per-run measurement records
    - Classification: SIMULATOR-DEFINED.
    - Evidence: the common architecture, result schema, and evaluation metrics documents all require raw data retention before aggregation.

32. Final aggregated statistics such as mean, median, standard deviation, and confidence intervals
    - Classification: RESEARCHER-DEFINED.
    - Evidence: the project mentions repeated runs and summary statistics, but the exact aggregation protocol belongs to later statistics decisions and is not fixed here.
    - Important boundary: these decisions are not metric definitions and are not resolved in CMP-RD-007.

C. Metric semantics and fairness requirements

33. Distinction between algorithm-native objective and common comparison metric
    - Classification: SOURCE-DEFINED for the source-native objective semantics and SIMULATOR-DEFINED for the raw measurement infrastructure.
    - Important boundary: this is a structural requirement, not a final metric selection.
    - The same variable may be objective-native for one method and only externally measured for another. This must be preserved.

34. Final metric-selection decision for the five-method comparison
    - Classification: RESEARCHER-DEFINED.
    - Evidence: no final common metric set is fixed in the source papers or project architecture.

35. Exact common formulas, units, weights, normalization, and scaling
    - Classification: UNRESOLVED.
    - Evidence: project documents require that metric definitions be finalized before implementation, but the source papers do not jointly supply a final common formula suite.
    - Important boundary: normalization, transformation, and scaling belong to CMP-RD-012 and must not be resolved here.

36. Exact aggregation of raw per-run metrics into final thesis statistics
    - Classification: RESEARCHER-DEFINED and not part of CMP-RD-007.
    - Evidence: [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) and [docs/01-project-overview.md](docs/01-project-overview.md) require repeated runs and summaries, but the exact statistical protocol is delegated to CMP-RD-009.

37. Metric units explicitly in source papers
    - Classification: SOURCE-DEFINED only when the source paper explicitly states units.
    - Evidence: time units, storage units, bandwidth units, and cost units appear in the source literature, but the comparison layer does not yet fix a single uniform unit system across all five methods.
    - Exact cross-method unit alignment: UNRESOLVED.

38. Common-measurement requirement for fair comparison
    - Classification: RESEARCHER-DEFINED.
    - Evidence: the project requires the same external system conditions while keeping source-defined algorithm behavior distinct.
    - Important boundary: this is a fairness policy and must be fixed before implementation, but it does not imply that all methods must optimize the same objective vector.

D. Guardrails and open status

#### CMP-RD-010 Researcher Decision

No inspected source paper prescribes a common chart type, axis convention, method order, error-bar rule, or figure layout. The following are researcher-decided visualization rules, not source-defined algorithm behavior.

##### Primary figures

Create one fixed point-and-error-interval figure per CMP-RD-007 primary metric:

- Response time: mean run-level value with a two-sided 95% percentile paired-bootstrap CI; seconds, lower is better.
- Request reliability: mean proportion with the same CI semantics; `[0,1]`, higher is better.
- Service availability: mean proportion with the same CI semantics; `[0,1]`, higher is better.
- Active replica count: mean run-level diagnostic with CI; replica count, descriptive only.
- Network transfer volume: mean run-level volume with CI; bytes/GiB, descriptive only; request-service and replication/movement components remain distinct.
- Algorithm decision time: mean run-level time with CI; milliseconds and recorded clock type, lower is better.

The point is the CMP-RD-009 arithmetic mean. The interval is exactly its two-sided 95% percentile paired-bootstrap CI using matched repetition IDs and 10,000 resamples. It is never labeled as standard deviation or standard error. Supplementary tables may report the CMP-RD-009 median, sample SD, IQR, minimum, maximum, usable count, status/missingness counts, paired differences, adjusted p-values, and paired rank-biserial effects.

##### Method order and scenarios

Every figure and table uses this fixed order: Proposed, HRS — Hybrid Replication Strategy, DPRS, OGSA, EIMORM. Methods are never sorted by performance. Labels, colors, markers, and line styles are fixed before execution and remain constant, with non-color identifiers and grayscale compatibility.

Workload order is W01 Balanced, W02 Stationary Skew, W03 Phase Shift. Failure order is F0-control, F1-node-transient, F2-site-transient, F3-link-transient, F4-node-persistent. Use deterministic facets or separate figures with the same method order and axes. CMP-RD-011 owns which cells are executed; CMP-RD-010 does not combine or weight cells.

##### Axes and display rules

- Use native CMP-RD-007 units. Response time is displayed in seconds, following resolved CMP-RD-007; any older source mention of milliseconds is source context, not the common metric definition. A fixed global conversion to milliseconds is permitted only with an explicit label.
- Reliability and availability use fixed `[0,1]` axes; percentage labels are display-only and consistent.
- Nonnegative time, volume, and count metrics use linear axes with zero baselines.
- No logarithmic, broken, truncated, or result-dependent axis is permitted in primary figures.
- Axis limits are fixed by metric semantics/configuration or a pre-registered global rule before results; they are never tuned per method or observed value. Replica bounds derive from frozen configuration, not observed maxima.
- Raw/statistical values are never rounded for calculation; display rounding uses fixed metric-specific precision selected before execution.

##### Missingness, significance, and effects

Only statistically eligible observed values are plotted. Invalid, failed, unresolved, and timed-out attempts remain in accompanying status/count tables and are never replaced with zero. Insufficient usable observations or pairs are displayed as `NA` with the reason and usable count.

Primary figures do not use significance stars, compact letters, or winner markers. Supplementary tables may report the CMP-RD-009 Friedman result, all ten paired comparisons when applicable, Holm-adjusted p-values, paired rank-biserial effects, and unstandardized paired differences. No effect size becomes winner points and no practical-significance threshold is invented.

##### Native-objective diagnostics

Native objectives are supplementary method-specific diagnostics only: Proposed native objectives/NSGA-III diagnostics; OGSA MFU/MST/LV/EC/ML and OBL+GSA diagnostics; HRS Merit/TotalCost/fuzzy diagnostics; DPRS source response-time/graph diagnostics; and EIMORM source diagnostics only where executable. They are never universal metrics, pooled objective scores, or replacements for the six common metric figures.

##### Raw/display boundary and provenance

The immutable pipeline is `raw results -> CMP-RD-009 statistical results -> CMP-RD-010 display data -> figure/table`. Display-only unit conversion, percentage labeling, fixed rounding, and layout cannot alter raw/statistical values, normalize them, invert directions, or create rankings. Each figure/table artifact records schema, metric-definition, analysis-protocol, axis/unit/rounding/style versions; source statistical/raw observation IDs; experiment, scenario, workload, failure, repetition, and method identities; status/missingness counts; and implementation identity.

##### Implementation and downstream boundary

The repository has no statistical-result ingestion, chart-ready export, plotting module, or figure-provenance implementation; these are implementation gaps. CMP-RD-011 remains responsible for the executed experiment matrix. CMP-RD-012 remains responsible for normalization/scaling. No chart data or plotting code is created here.

Decision:
RESOLVED — RESEARCHER-DECIDED

Key guardrails:
- Do not create a fabricated metric vector.
- Do not force all five methods to share the same objective function.
- Do not treat an algorithm-native objective as a universal cross-method metric unless the project explicitly defines it as such.
- Do not equate optimization-runtime time with request response time.
- Do not equate replica count, storage utilization, or cost with a universal objective unless source evidence supports it.
- Do not define normalization or final statistical aggregation in this section.
- Do not add formulas that are not already present in the source or project architecture.

Decision:
RESOLVED — RESEARCHER-DECIDED

---

### CMP-RD-008 — Common Result Schema

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Document what information must be preserved from real execution so that raw simulation observations, raw per-run results, aggregated statistics, and later thesis charts remain traceable to an actual simulated run.

Why this decision is required:
The project architecture requires a comparison layer that records traceable execution outcomes, but the source papers do not specify a final implementation schema, file format, or exact field list. The result schema must therefore preserve the distinction between:
- raw simulation observations,
- raw per-run results,
- aggregated results,
- final visualization data,
- provenance metadata.

Current evidence:
The clearest evidence is the common architecture and comparison-model documents:

- [docs/01-project-overview.md](docs/01-project-overview.md) requires raw results to be saved in machine-readable form and records experiment metadata such as algorithm, seed, workload, simulation duration, and failure parameters.
- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) states that metrics collection and result export are common simulator concerns and that the common environment must preserve fairness and reproducibility.
- [docs/06-common-domain-model.md](docs/06-common-domain-model.md) identifies shared runtime state such as topology, nodes, files, replicas, users, requests, time, events, and health, which are required to compute raw observations.
- [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md) requires the simulator to own validation, execution, mutation, and recording, while algorithms return source-defined decisions only.
- [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) requires raw measurements and repeated-run results, but does not define the final final-result schema or output format.
- [docs/algorithms/comparison-researcher-decisions.md](docs/algorithms/comparison-researcher-decisions.md) earlier sections already distinguish raw execution data from aggregated statistical outputs and keep metric definitions open.

Researcher decision:
The project adopts the logical layered schema below. This resolves required identities, raw observation families, provenance, status, immutability, missing-value semantics, and traceability without selecting a physical file/database format or resolving downstream statistics, visualization, experiment matrix, or normalization.

#### CMP-RD-008 Logical Result Schema

##### Run identity and attempt records

`RunIdentity` identifies the planned matched execution cell and must contain:

- `experiment_id`, `configuration_id`, `scenario_id`, `workload_id`, `failure_artifact_id`, `repetition_id`, and `method_id`;
- `run_id` for the planned method/cell execution;
- CMP-RD-004 master, scenario, workload, failure, and method seed identities plus named stream identities;
- common scenario/replay/manifest digest, workload digest, and failure-schedule digest;
- source-interpretation/configuration identity, source version, implementation version/commit, schema version, metric-definition version, and deterministic-serialization version.

`AttemptRecord` identifies one concrete execution attempt and must contain:

- `attempt_id`, `run_id`, attempt ordinal, and rerun linkage;
- wall-clock start/end metadata when available;
- simulation start/end time, admission horizon, drain policy/version, and termination reason;
- run status, validation/error summary, and pointers to immutable raw artifacts.

`run_id` is not reused for a rerun. A rerun receives a distinct `attempt_id` and preserves the original attempt record and its status.

##### Run statuses and decision statuses

Run status uses CMP-RD-006/CMP-RD-004 technical values: `VALID`, `INVALID`, `UNRESOLVED`, `FAILED`, and `TIMED_OUT`. Method decision statuses such as `UNSUPPORTED` and `NO_OP` remain decision-layer values and do not automatically change run status. A run may continue its common schedule after a method decision is unresolved where the temporal/runtime contract permits; the attempt and decision are retained.

##### Event and transition records

`EventRecord` is an append-only causal ledger with:

- `event_id`, deterministic sequence number, timestamp, priority, event type, and `external_or_method_generated` classification;
- parent/causation event ID;
- optional request, failure, recovery, replica, transfer, decision, node, site, link, and file references;
- immutable structured payload, validation status, execution status, error code/reason, and state-transition reference.

`TransitionRecord` records a simulator-owned state mutation with transition ID, parent event ID, pre-state reference, post-state reference, mutation type, affected entity references, and validation/execution status. Existing queued `Event`, `RawObservation`, `DecisionEnvelope`, `ExecutionResult`, and `ValidationResult` concepts map to these logical records; no duplicate scientific concept is introduced.

##### Request observations

`RequestObservation` contains:

- request ID, sequence, arrival timestamp, requester/client ID, source site/node, target file ID, operation, and catalog-derived file size;
- admission status and event ID;
- optional service-start and completion timestamps, terminal outcome, outcome reason, response-time value, serving replica/node, path/transfer IDs, and bytes transferred;
- missing-value status for every unavailable optional field.

The schema does not add deadline, retry, or success semantics beyond CMP-RD-007. A missing completion is not zero and does not imply success.

##### Failure and recovery observations

`FailureObservation` and `RecoveryObservation` contain failure/recovery ID, artifact/class, target type and stable target identity, timestamp, duration/recovery timestamp where applicable, scenario/repetition IDs, failure seed identity, event ID/sequence, pre/post health and availability state, and raw error/status fields. The schema preserves CMP-RD-005's rule that failed-node replicas remain catalogued.

##### Replica and state observations

`ReplicaObservation` contains replica ID, file ID, node/site ID, primary flag when available, catalog validity, host health/reachability, serviceability, observation timestamp or interval, transition type, causation/decision/event references, and missing-value status. It distinguishes catalogued, valid, active/serviceable, failed-node inactive, recovered, and actually deleted states without inventing deletion semantics.

##### Transfer observations

`TransferObservation` contains transfer ID, request/parent event/decision association, traffic type (`request_service` or `replication_movement`), source/destination node IDs, file/replica IDs where known, path/link IDs where known, start/completion timestamps, actual bytes transferred, status, and missing-value reason. It records observed bytes only and does not infer bandwidth consumption from a method formula.

##### Decision observations

`DecisionObservation` contains decision ID, method ID, decision type, request/event association, start/end timestamps, duration, clock type (`wall_clock` or `cpu_clock`), decision status, validation/execution/transition references, provenance classification, and error/missing-value fields. It remains separate from request response time and simulation time.

##### Metric observations

`MetricObservation` contains metric ID/name and namespace, raw or derived classification, value, unit, direction, observation scope, timestamp or interval, run/attempt identity, definition/model version, missing-value status/reason, and source observation/event/transition IDs. Raw metric observations remain in native units; no normalization, inversion, weighting, or statistical aggregation is stored here.

##### Optional summaries and conditional metrics

`RunSummary` is a derived, non-authoritative view containing counts, metric availability, termination status, and pointers to raw artifacts. It never replaces raw records. Method-native objectives, optimizer populations, fitness, Pareto fronts, and convergence values are method-specific diagnostics with method/run provenance, not common metrics. Energy, cost, data-node load, and centrality may be represented as optional metric namespaces only after CMP-RD-007's conditional models are implemented; no placeholder values are emitted now.

##### Missing-value semantics

Every optional or unavailable value uses an explicit status such as `NOT_OBSERVED`, `NOT_APPLICABLE`, `UNRESOLVED`, `FAILED_MEASUREMENT`, or `UNAVAILABLE`, with an explanatory reason where needed. Zero is reserved for an actually observed zero. Missing completion is not completion time zero; missing transfer is not zero bytes; unsupported metrics are not fabricated.

##### Raw retention and immutability

Raw observations are retained for `VALID`, `INVALID`, `UNRESOLVED`, `FAILED`, and `TIMED_OUT` attempts, subject to recorded technical storage limitations. Frozen scenario, workload, failure schedule, initial state, run identity, and finalized raw observations are immutable. Invalid or failed attempts are never silently overwritten or deleted; reruns use a new attempt ID and preserve the original.

##### Deterministic serialization and versioning

Canonical serialization uses stable field ordering, stable entity-ID ordering, explicit timestamp/numeric encoding, deterministic handling of mappings/collections, and a recorded serialization version. Artifact digests cover the canonical frozen inputs and raw artifact identity as appropriate. The schema, metric-definition, experiment-configuration, source-interpretation, and implementation versions are recorded; this decision does not prescribe a physical storage format.

##### Provenance chain and replay audit

The minimum traceability chain is:

`source/configuration -> RunIdentity -> AttemptRecord -> EventRecord -> Decision/Transition -> typed raw observation -> MetricObservation -> later statistical result`

Every matched result must demonstrate the same scenario, workload, failure schedule, initial-state/replay digest, horizon configuration, and repetition identity with only `method_id` and method-local configuration/stream differing. CMP-RD-004 seed formulas are not redefined.

##### Common and method-specific boundary

Common records include run identity, scenario/replay references, workload requests, failure/recovery, topology state, replica state, transfers, timing, decisions, validation, transitions, metrics, and provenance. Method-specific records may include native objective values, optimizer populations, fitness, Pareto fronts, and intermediate variables, but they must carry the same run/attempt/method/provenance identity and must not be flattened into common metrics.

##### Implementation capability audit

Currently supported in part: `RunMetadata`, `RawObservation`, `RawRecorder`, `MetricRecord`, `Scenario`/`Experiment`, `Event`, `DecisionEnvelope`, validation/execution results, replica mutation, node health mutation, frozen scenario cloning, and deterministic event sequence. Missing or incomplete: attempt lifecycle, repetition/workload/failure IDs, event IDs/causal parents/priorities, typed request outcomes/completions, failure/link/recovery records, explicit primary/replica history, transfer ledger, decision timing, metric provenance links, missing-value statuses, canonical serialization/digests, immutable nested payloads, termination provenance, and schema enforcement. These are schema/instrumentation gaps, not fabricated observations.

Decision status:
RESOLVED / RESEARCHER-DECIDED.

Dependencies:
- CMP-RD-003 — Dataset and Workload
- CMP-RD-004 — Randomness and Reproducibility
- CMP-RD-005 — Failure and Dynamic Scenario Protocol
- CMP-RD-006 — Simulation Horizon and Termination
- CMP-RD-007 — Common Evaluation Metrics
- CMP-RD-009 — Statistical Analysis Protocol
- CMP-RD-010 — Visualization Protocol
- CMP-RD-011 — Experiment Matrix
- CMP-RD-012 — Normalization and Scaling Boundary

Affected methods:
- Proposed Method / Proposed NSGA-III
- HRS
- DPRS
- EIMORM
- OGSA

Classification vocabulary for this section:
- SOURCE-DEFINED
- RESEARCHER-DEFINED
- SIMULATOR-DEFINED
- UNRESOLVED

Only one label is used for each property.

A. Raw simulation observations

1. Raw request-level observations
   - Classification: SIMULATOR-DEFINED.
   - Evidence: the common architecture and domain model both require request records, event timestamps, success/failure status, file identifiers, and request state.
   - Important boundary: these are raw execution data, not aggregated statistics.
   - The exact final field set is UNRESOLVED; the simulator must at minimum preserve enough raw request facts to support later metric calculation.

2. Raw node-level state observations
   - Classification: SIMULATOR-DEFINED.
   - Evidence: the architecture requires node, host, storage, health, and resource-state tracking in the shared environment.
   - Example categories that may matter later: node identifier, node state, storage capacity, storage utilization, load, health, and relevant timestamps.
   - The exact final field list remains UNRESOLVED.

3. Raw replica state and replica event observations
   - Classification: SIMULATOR-DEFINED.
   - Evidence: replica catalog, storage accounting, and state transitions are part of the common simulator.
   - Example categories: replica creation, replica deletion, replica relocation, source node, destination node, file identifier, replica identifier, triggering event, timestamp.
   - The exact final field set remains UNRESOLVED.
   - Important boundary: the common result schema must not require every method to produce the same replica operations if the source method does not define them.

4. Raw network transfer observations
   - Classification: SIMULATOR-DEFINED.
   - Evidence: network state, data transfer, bandwidth, and latency are part of the shared domain and evaluation model.
   - Example categories: transfer event, source site, destination site, file identifier, amount transferred, timestamp, transfer completion status.
   - Exact field set remains UNRESOLVED.

5. Raw failure and recovery observations
    - Classification: SIMULATOR-DEFINED for the runtime recording of events; RESEARCHER-DEFINED for whether the experiment includes them; CMP-RD-005-defined for the registered schedule and UNRESOLVED for any later extension.
   - Evidence: the common architecture explicitly contains a failure/recovery model, and CMP-RD-005 distinguishes common failure generation from source-defined response.
   - Important boundary: the schema should preserve actual failure/recovery events if the final experiment includes them, but it does not resolve the failure protocol itself.

6. Raw simulation event stream
   - Classification: SIMULATOR-DEFINED.
   - Evidence: the common simulator owns the event scheduling and event queue.
   - Important boundary: raw event records are not final result summaries and must remain distinct from run-level metrics.

7. Raw metric observations before aggregation
   - Classification: SIMULATOR-DEFINED.
   - Evidence: architecture documents state that raw observations and raw metric values must be preserved before statistical aggregation.
   - Important boundary: these are raw metric values, not final aggregated statistics.

B. Raw per-run results

8. Raw per-run result record
   - Classification: SIMULATOR-DEFINED for the record-generation mechanism; RESEARCHER-DEFINED for the final required metadata and inclusion policy.
   - Evidence: project overview and architecture documents require run-level results and metadata, but no final schema or fixed field list is specified.
   - Important boundary: this is one complete execution of one method under one scenario/run, not an aggregate over several runs.

9. Run identity
   - Classification: RESEARCHER-DEFINED for the final identity design; SIMULATOR-DEFINED for assigning runtime IDs.
   - Evidence: the architecture and overview collectively require method, scenario, workload configuration, and run identity to be preserved for reproducibility, but the exact field pattern remains unresolved.
   - Candidate identity components are conceptual only, not final schema: method identifier, scenario identifier, run identifier, seed identity, configuration instance, execution instance.
   - Exact final identity key remains UNRESOLVED.

10. Experiment metadata required for re-traceability
    - Classification: RESEARCHER-DEFINED for which metadata is required; SIMULATOR-DEFINED for recording it when available.
    - Evidence: the overview requires algorithm name, experiment ID, random seed, number of nodes, number of files, number of requests, simulation duration, failure model, algorithm parameters, and evaluation metric values, but this is not a final schema decision.
    - Important boundary: these are candidate metadata categories, not final field names or final schema requirements.

11. Scenario and configuration identity
    - Classification: RESEARCHER-DEFINED for the experiment design; SIMULATOR-DEFINED for runtime tagging.
    - Evidence: the common architecture uses scenarios, topology, network, workload, and failure configuration as common experiment elements, but the final method-neutral tagging convention remains unresolved.

12. Seed identity
    - Classification: RESEARCHER-DEFINED for the policy; SIMULATOR-DEFINED for recording the actual seed used.
    - Evidence: the project overview requires a configurable random seed, and CMP-RD-004 handles seed policy separately.
    - Important boundary: seed identity is required for raw-run provenance but does not define a final statistical protocol.

13. Termination reason and execution status
    - Classification: SIMULATOR-DEFINED for recording; RESEARCHER-DEFINED for the final allowed status vocabulary if any.
    - Evidence: the architecture and CMP-RD-006 both refer to simulation end, termination conditions, and recorded run status, but no exact final status taxonomy is fixed.
    - Example conceptual statuses: completed, failed, incomplete, invalid, excluded, timeout. The actual status vocabulary remains OPEN.

14. Actual simulation-horizon metadata
    - Classification: SIMULATOR-DEFINED for the recorded actual run boundary; RESEARCHER-DEFINED for the CMP-RD-006 horizon policy; UNRESOLVED only for any later extension beyond the registered policy.
    - Evidence: the project requires the simulator to know the simulation duration and run termination boundary, but the exact horizon and termination conditions are not set in source evidence.

C. Aggregated results and later analysis layers

15. Aggregated run summaries
    - Classification: RESEARCHER-DEFINED.
    - Evidence: mean, median, standard deviation, confidence intervals, and min/max are later statistical outputs, not raw simulation results.
    - Important boundary: aggregated results must be computed from raw per-run data, not stored in place of it.

16. Final visualization data
    - Classification: RESEARCHER-DEFINED.
    - Evidence: chart generation and report formatting belong to CMP-RD-010 and are not part of the raw result schema.
    - Important boundary: visualization data must be derived from analyzed result data, not manually entered or fabricated.

D. Provenance and versioning

17. Provenance from source paper to final chart
    - Classification: RESEARCHER-DEFINED for policy; SIMULATOR-DEFINED for execution metadata capture.
    - Evidence: the project needs auditable comparison results but does not specify a final provenance model. The architectural requirement is traceability, not a final implementation document.
    - Important boundary: the schema should support provenance for method identity, source specification version, configuration version, simulator version, scenario version, and execution version when those are eventually chosen.

18. Versioning information
    - Classification: RESEARCHER-DEFINED for whether version metadata is required; SIMULATOR-DEFINED for runtime capture if enabled.
    - Evidence: the architecture and project overview require reproducibility, but no final versioning policy is fixed.
    - Important boundary: a version record is not required to be used on every result unless the final experiment policy decides it.

E. Native objectives versus common result structure

19. Method-native objective values as part of the raw result stream
    - Classification: SOURCE-DEFINED for the objective semantics; SIMULATOR-DEFINED for recording the emitted values when they are generated.
    - Evidence: Proposed Method has a five-objective NSGA-III objective vector; OGSA has an MFU/MST/LV/EC/ML objective structure; HRS, DPRS, and EIMORM each have native source-defined decision quantities.
    - Important boundary: these native objective records must not be flattened into a universal common objective schema unless the future comparison explicitly requires a common representation.

20. Common evaluation metric values as part of the result stream
    - Classification: RESEARCHER-DEFINED for the final chosen common metric set; SIMULATOR-DEFINED for the raw measurement capture.
    - Evidence: common metrics are still open in CMP-RD-007.
    - Important boundary: the result schema must be general enough to hold either native objective values or common comparison values, but it must not assume they are the same thing.

F. Structural safeguards

21. Raw data must not be overwritten by aggregated data
    - Classification: SIMULATOR-DEFINED and RESEARCHER-DEFINED.
    - Evidence: this is a required integrity principle in the comparison design, and it belongs to the execution and aggregation pipeline rather than a source paper.
    - Important boundary: the raw result store must remain accessible even after derived statistics are computed.

22. Failed or incomplete runs must remain identifiable
    - Classification: SIMULATOR-DEFINED for recording; RESEARCHER-DEFINED for the policy on whether they are excluded from later analysis.
    - Evidence: the comparison design requires traceability and prohibit silent removal of unfavorable or failed runs.
    - Important boundary: exclusion policy is later researcher decision and belongs to CMP-RD-009 or a later protocol decision, not here.

23. Final schema design and final field list
    - Classification: UNRESOLVED.
    - Evidence: the project provides architectural and conceptual requirements but not a final executable schema or exact field list.
    - Important boundary: a final implementation schema must not be invented in this section.

24. Exact file format (for example, a machine-readable result serialization format)
    - Classification: UNRESOLVED.
    - Evidence: the project overview says raw results must be saved in machine-readable form, but it does not select a final format.
    - Important boundary: this decision is intentionally left open and is not resolved in CMP-RD-008.

25. Exact names and ordering of fields in a result record
    - Classification: UNRESOLVED.
    - Evidence: project requirements state that result metadata must include certain categories, but no final field list or ordering is specified.

26. Exact aggregation, significance, or chart-generation schema
    - Classification: UNRESOLVED.
    - Evidence: those decisions belong to later sections (CMP-RD-009 and CMP-RD-010), not to raw-result preservation.

Key guardrails:
- Do not invent a final implementation schema.
- Do not pick a final file format.
- Do not define a field list as though it were implementation-ready.
- Do not collapse raw observations into aggregated values.
- Do not force all methods to share the same objective representation.
- Do not remove failed or incomplete runs from the traceable result stream.
- Do not define the final statistical analysis or visualization pipeline here.
- Do not claim that a method native objective is automatically a common evaluation metric.
- Do not create metric values or fabricated results.

Decision:
OPEN — NOT YET DECIDED

---

### CMP-RD-009 — Statistical Analysis Protocol

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Define how real raw simulation results will eventually be statistically analyzed before they are used in thesis tables and charts, while preserving the evidence chain:

REAL SIMULATION EXECUTION
        ↓
RAW PER-RUN RESULTS
        ↓
STATISTICAL ANALYSIS
        ↓
AGGREGATED RESULTS
        ↓
FINAL TABLES / CHARTS

Why this decision is required:
The project architecture and evaluation metrics documents require raw results and repeated runs, but they do not define a single final statistical protocol for the five-method comparison. The statistical layer must therefore be treated as a later comparison decision, not as a source-defined algorithm behavior.

Current evidence:
The relevant evidence is distributed across the project overview, architecture, metric definitions, and method-source documents, but none of them jointly specify a final statistical rule set.

- [docs/01-project-overview.md](docs/01-project-overview.md) requires reproducible runs, configurable random seeds, and raw machine-readable output, but it does not fix the repeated-run count or its statistical policy.
- [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) says each experiment must be repeated multiple times and that mean, standard deviation, minimum, and maximum should be reported, but it does not state the actual run count, confidence level, or significance method.
- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) clearly separates common simulator execution from algorithm-specific logic and states that result aggregation is a common evaluation concern, not a source paper behavior.
- [docs/06-common-domain-model.md](docs/06-common-domain-model.md) distinguishes raw runtime state from algorithm-internal state and supports raw record retention before aggregation.
- [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md) states that common scenario randomness must be shared across matched runs, while algorithm-local randomness remains method-specific; it does not define a statistical test or run-count policy.
- [docs/02-proposed-method.md](docs/02-proposed-method.md) describes a dynamic multi-objective method but does not give a repeated-run statistical protocol.
- [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) states that initial placement is random, but it does not specify repeated runs, confidence intervals, or significance tests.
- [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md) defines a placement formulation and response-time model, but not repeated-run statistical reporting.
- [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md) defines a multi-objective replication strategy and relevant objective concepts, but it does not define any statistical reporting protocol.
- [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) defines the five objective structure and optimization model, but it does not define repeated-run reporting, statistical aggregation, or significance testing.

Researcher decision:
The statistical protocol used to convert raw per-run results into summaries and method comparisons is fixed below. Source papers do not prescribe these procedures; all statistical choices are RESEARCHER-DECIDED and are applied identically to all methods and cells.

Dependencies:
- CMP-RD-004 — Randomness and Reproducibility
- CMP-RD-005 — Failure and Dynamic Scenario Protocol
- CMP-RD-007 — Common Evaluation Metrics
- CMP-RD-008 — Common Result Schema
- CMP-RD-010 — Visualization Protocol
- CMP-RD-011 — Experiment Matrix
- CMP-RD-012 — Normalization and Scaling Boundary

Affected methods:
- Proposed Method / Proposed NSGA-III
- HRS
- DPRS
- EIMORM
- OGSA

Classification vocabulary for this section:
- SOURCE-DEFINED
- RESEARCHER-DEFINED
- SIMULATOR-DEFINED
- UNRESOLVED

Only one label is used for each property.

A. Repeated runs and independence

1. Requirement for repeated independent executions
   - Classification: RESEARCHER-DEFINED.
   - Evidence: [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) requires repeated runs, but it does not specify the final number of repetitions.
   - Important boundary: the need for repetition is project-level guidance, not a source-defined statistical rule.

2. Final number of independent runs per method/scenario
    - Classification: RESEARCHER-DECIDED by CMP-RD-004.
    - Evidence: CMP-RD-004 fixes 30 repetitions with IDs `rep-01` through `rep-30`.

3. Definition of independent runs
   - Classification: RESEARCHER-DEFINED or UNRESOLVED depending on final experiment design.
   - Evidence: [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md) distinguishes common scenario randomness from algorithm-local randomness, which matters for independence, but it does not resolve the final statistical definition of independence.
   - Important boundary: different random seeds do not automatically define statistical independence if the same common scenario is replayed across methods.

4. Common scenario replay across matched methods
   - Classification: RESEARCHER-DEFINED for final fairness policy; SIMULATOR-DEFINED for recording and replay capacity.
   - Evidence: the project requires matched methods to operate under the same external conditions, but the exact replay mechanism is not fixed.
   - Important boundary: matched methods may share the same realized scenario while still possessing method-specific internal randomness.

5. Independent complete experimental realization
   - Classification: RESEARCHER-DEFINED or UNRESOLVED.
   - Evidence: the project architecture supports repeated runs and scenario-based comparison, but the final statistical treatment of multi-scenario experiments is not fixed.

6. Algorithm-local randomness versus common scenario randomness
   - Classification: SOURCE-DEFINED for the existence of randomness in a source method where explicitly stated; RESEARCHER-DEFINED for the final comparison policy; SIMULATOR-DEFINED for runtime seeding and execution support.
   - Evidence: HRS explicitly has random initial placement; OGSA explicitly has random initial solution generation and random [0,1] values; the project architecture distinguishes common scenario randomness from algorithm randomness; the precise final policy remains unresolved.

7. Seed assignment policy
   - Classification: RESEARCHER-DEFINED for the final policy; SIMULATOR-DEFINED for execution support.
   - Evidence: [docs/01-project-overview.md](docs/01-project-overview.md) requires a configurable random seed, and [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) describes seed management as part of the simulator, but the final seed policy is not fixed.

8. Warm-up or burn-in periods
   - Classification: UNRESOLVED.
   - Evidence: no source paper or project document specifies a warm-up rule.

B. Source-defined statistical practices by method

9. Proposed Method / Proposed NSGA-III statistical reporting
   - Classification: UNRESOLVED.
   - Evidence: [docs/02-proposed-method.md](docs/02-proposed-method.md) defines the method structure and objectives but does not define repeated-run reporting, means, medians, variance, or significance tests.

10. HRS statistical reporting
    - Classification: UNRESOLVED.
    - Evidence: [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) defines fuzzy replacement, centrality, and cost terms, but not repeated-run statistical reporting or significance tests.

11. DPRS statistical reporting
    - Classification: UNRESOLVED.
    - Evidence: [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md) defines response-time and placement behavior, but not experiment-level statistical reporting.

12. EIMORM statistical reporting
    - Classification: UNRESOLVED.
    - Evidence: [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md) defines availability, cost, and multi-objective terms, but not repeated-run statistics.

13. OGSA statistical reporting
    - Classification: UNRESOLVED.
    - Evidence: [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) defines objective functions and optimization behavior, but not a final statistical protocol.

14. Source-defined reporting of mean, median, standard deviation, variance, or confidence intervals
    - Classification: UNRESOLVED.
    - Evidence: no source paper in the final five-method comparison defines a final repeated-run statistical reporting regime.

C. Aggregation design and units of analysis

15. Mean aggregation across runs
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) mentions mean, but the final decision on when to use mean is not fixed.
    - Important boundary: mean is a later aggregation decision, not a source-defined algorithm objective.

16. Median aggregation across runs
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: project documents mention repeated runs and summary statistics generally but do not finalize a median policy.

17. Standard deviation and variance across runs
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) names them as expected outputs, but no final rule is fixed.

18. Minimum and maximum across runs
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: these appear as summary statistics in the project evaluation section, but the final aggregation policy remains unchosen.

19. Percentile or robust aggregation policy
    - Classification: UNRESOLVED.
    - Evidence: no source paper or project document defines a percentile-based or robust-statistics protocol.

20. Per-request versus per-run aggregation
    - Classification: RESEARCHER-DEFINED for final policy; SIMULATOR-DEFINED for raw observation capture.
    - Evidence: the architecture records raw request observations and raw run data, but the project does not define whether a metric is first aggregated within a run and then across runs.
    - Important boundary: this is a methodological distinction, not a metric definition.

21. Per-node or time-series metrics versus per-run metrics
    - Classification: RESEARCHER-DEFINED for final reporting protocol; SIMULATOR-DEFINED for recording the underlying observations.
    - Evidence: node-state, storage-state, load, health, request events, and failure events are all part of the common domain model, but no final policy defines the unit of analysis for each metric.

D. Failure, incompleteness, and outliers

22. Treatment of failed, incomplete, or timeout runs
    - Classification: RESEARCHER-DEFINED for the final policy; SIMULATOR-DEFINED for recording the run status.
    - Evidence: the project requires run-level traceability and failure handling but does not define whether failed runs are excluded, retained, or separately reported.
    - Critical rule: a run must not be silently removed purely because it is unfavorable.

23. Outlier handling policy
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: no source paper defines an outlier rule, and no project document chooses a robust or trimming policy.
    - Important boundary: no outlier policy may be selected based on outcome favoritism.

24. Confidence intervals
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: the project mentions repeated runs and summary statistics, but no source paper or project document fixes a confidence level or interval method.
    - Important boundary: 95% and 99% are candidate choices only and are not fixed here.

25. Hypothesis testing
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) mentions significance testing as a possible output, but it does not specify a test family, p-value policy, or threshold.
    - Important boundary: hypothesis testing is not source-defined algorithm behavior.

26. Effect size
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: no source paper or project document defines a required effect-size metric or threshold.

E. Multi-objective and common-metric treatment

27. Proposed Method / OGSA multi-objective reporting
    - Classification: SOURCE-DEFINED for the native objective semantics; RESEARCHER-DEFINED for the later comparison policy; UNRESOLVED for any final aggregation across those objectives.
    - Evidence: Proposed Method is explicitly a five-objective NSGA-III strategy, and OGSA is explicitly a five-objective optimization model. Both papers define the objective forms but not a final multi-objective statistical reduction rule for thesis comparison.
    - Important boundary: the statistical layer must not change the source-defined optimization semantics.

28. Common comparison metric aggregation across methods
    - Classification: RESEARCHER-DEFINED for the final metric set and aggregation policy; SIMULATOR-DEFINED for raw measurement capture.
    - Evidence: [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) names common metric concepts; CMP-RD-007 now fixes the primary metric definitions while CMP-RD-009 retains statistical aggregation.

29. Normalization and scaling
    - Classification: UNRESOLVED.
    - Evidence: the project architecture explicitly requires a later normalization/scaling boundary, but [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) and the source materials do not fix any normalization formula or vector scaling policy.
    - Important boundary: this belongs to CMP-RD-012, not CMP-RD-009.

30. Ranking of methods across multiple metrics
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: the project may eventually compare methods across several metrics, but no source paper specifies an overall ranking function and no project decision fixes one.
    - Important boundary: a ranking formula must not be created merely to produce a single winner score.

F. Raw-data-to-chart traceability

31. Raw per-run results retained for later analysis
    - Classification: SIMULATOR-DEFINED for storage and export, RESEARCHER-DEFINED for the final requirement policy.
    - Evidence: [docs/01-project-overview.md](docs/01-project-overview.md) requires raw machine-readable output; [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) requires result export; [docs/06-common-domain-model.md](docs/06-common-domain-model.md) preserves runtime state.

32. Aggregated results derived from raw data
    - Classification: RESEARCHER-DEFINED for the final protocol; SIMULATOR-DEFINED for the calculation mechanism.
    - Evidence: the architecture requires traceability from raw run outputs to final tables and charts, but it does not define the exact aggregation formula.

33. Final chart value traceability
    - Classification: RESEARCHER-DEFINED for the policy; SIMULATOR-DEFINED for the raw capture and metadata.
    - Evidence: the project requires traceability from real execution to final chart, but no final chart source or aggregation pipeline is fixed.
    - Required chain: FINAL CHART VALUE → STATISTICAL AGGREGATION → RAW PER-RUN RESULTS → REAL SIMULATION EXECUTION.

G. Experimental integrity safeguards

34. Raw data must not be overwritten by aggregated values
    - Classification: SIMULATOR-DEFINED and RESEARCHER-DEFINED.
    - Evidence: this is a strict traceability requirement of the project environment, independent of any source paper.

35. Failed or incomplete runs remain identifiable
    - Classification: SIMULATOR-DEFINED for recording; RESEARCHER-DEFINED for whether they are excluded from analysis.
    - Evidence: the experiment design requires auditability and prohibits silent removal of unfavorable results.

36. No statistical selection based on post-hoc outcome preference
    - Classification: RESEARCHER-DEFINED as an integrity rule.
    - Evidence: the comparison protocol must preserve experimental integrity, but no source paper defines a result-driven statistical rule.

37. No fabricated results or numerical values
    - Classification: RESEARCHER-DEFINED as a guardrail; SIMULATOR-DEFINED for recording actual values.
    - Evidence: the project requires reproducibility and source fidelity, and the comparison design explicitly forbids fabricated results.

H. Explicit open status and guardrails

Key guardrails:
- Do not invent a ranking formula in this section.
- Do not define normalization or scaling in this section.
- Do not collapse request-level observations and run-level observations into a single statistical population without explicit justification.
- Do not interpret source-defined objectives as final common metrics.
- Do not remove failed or incomplete runs simply because they look unfavorable.
- Do not convert raw per-run data into chart values without preserving the traceability chain.
- Do not create numerical summaries that were not produced by a real simulation execution.

#### CMP-RD-009 Researcher Decision

##### Experimental unit and hierarchy

The experimental unit is one run-level metric value for one method, configuration, workload scenario, failure scenario, and repetition. Requests, events, files, transfers, and decisions are observations within a run, not independent experimental repetitions.

Aggregation hierarchy:

`raw observations -> request/event/file-level derived observations -> one run-level metric value -> 30-repetition distribution -> method/cell statistical summary`

Methods are compared within the same configuration, workload, failure class, and repetition block. Requests are never pooled across repetitions as independent method samples.

##### Run-level aggregation

- Response time: derive the run value from the CMP-RD-007 request-level response-time observations; retain completed count and failed count separately. The arithmetic mean is the primary run estimand and the median is a planned robustness summary.
- Reliability: compute the CMP-RD-007 successful-admitted-read numerator divided by all admitted-read requests for that run.
- Service availability: use the one CMP-RD-007 availability value produced over `[0,7200]` for that repetition; do not concatenate repetitions into one interval.
- Active replica count: retain the run-level values defined by CMP-RD-007, including initial/final/time-weighted/peak diagnostics where observed; do not redefine them as a new objective.
- Network transfer volume: retain separate run-level request-service and replication/movement totals, plus their observed sum where defined by the metric record.
- Algorithm decision time: retain run-level total and per-decision observations with clock type; do not combine with request response time.

##### Primary summary and dispersion

For each metric and cell, the arithmetic mean across eligible run-level values is the primary central-tendency summary. Median is retained as a planned robustness summary. Report sample standard deviation, interquartile range, minimum, and maximum descriptively. This fixed rule is selected before results and is not changed by skewness or method ranking.

##### Confidence intervals

Report two-sided **95% percentile paired-bootstrap confidence intervals** in native metric units. Resample matched repetition IDs with replacement, preserving all method values within each selected repetition. Use exactly 10,000 bootstrap resamples and a pre-registered deterministic analysis stream identity; do not resample individual requests. For method differences, bootstrap the paired repetition-level difference. Bounded reliability and availability remain on their native `[0,1]` scale; no data-dependent logit or other transformation is used.

##### Validity, missingness, and outliers

- `VALID` runs with observed metric values are eligible for normal run-level summaries.
- `INVALID`, `FAILED`, and `TIMED_OUT` attempts remain retained and reported but are not silently treated as scientific metric values.
- `UNRESOLVED` runs or method decisions produce explicit missingness for affected metrics; they are not zero and are not silently successful.
- Scientific request failures, unavailable data, and legitimate no-op decisions within an otherwise valid run remain valid observations, not technical failures.
- Technical failures, invalid state, uncaught exceptions, and drain timeouts are not outliers and are never deleted.
- No run deletion, trimming, winsorization, or result-driven outlier removal is permitted. Robust summaries are supplementary only.
- No scientific imputation is permitted for missing metric values.

The analysis reports planned repetitions (`30`), eligible observed run count, missing count, invalid/failed/unresolved/timed-out counts, and usable matched-pair count for every method/cell/metric. If fewer than two usable matched pairs exist, an inferential comparison is not estimable and is reported as such rather than fabricated.

##### Paired comparison and significance

The matched-repetition design supports paired comparisons. For each metric and cell:

1. Apply a prespecified Friedman repeated-measures omnibus test across the five methods when a complete block set is available.
2. Only after a significant omnibus result, perform all ten paired method comparisons.
3. Use a paired permutation test on repetition-level differences with exactly 10,000 pre-registered sign-flip resamples.
4. Apply Holm correction across the ten pairwise comparisons within that metric/cell family at two-sided `alpha = 0.05`.

The procedure is selected before result inspection. No independent-sample test is used for matched methods, and no pair is selectively reported because of its p-value. Separate metrics and cells are not silently pooled into one multiplicity family; family labels are retained for later reporting.

##### Effect sizes and practical significance

Report unstandardized paired effects: mean paired difference, median paired difference, and percentage-point difference for reliability/availability. Also report paired rank-biserial effect size for pairwise comparisons. If a standardized effect denominator is zero, report it as not defined rather than inserting an epsilon. No domain-specific practical-significance threshold is invented; effect magnitudes are reported descriptively alongside native metric values.

##### Bounded and zero-variance metrics

Reliability and availability must remain in `[0,1]`; exact zero and one are valid. SD is `0` when all eligible repetition values are identical. A confidence interval may be degenerate when the resampled values are identical. All-zero paired differences are reported as no observed difference, and rank/standardized effect sizes that are mathematically undefined are explicitly marked not defined.

##### Provenance

Every statistical result records experiment/configuration/scenario/workload/failure IDs, method IDs, included repetition IDs and raw observation IDs, metric-definition and schema versions, analysis-protocol version, implementation version/commit, bootstrap/permutation resample count, analysis stream identity, status/missingness counts, and the procedure/family/alpha labels. This extends CMP-RD-008 provenance without redefining its schema.

##### Implementation gaps and limitations

The repository has no run-level extraction, repetition grouping, status-aware aggregation, confidence-interval, bootstrap, permutation, Friedman, Holm, effect-size, missingness, or statistical-provenance implementation. These are implementation gaps only; no statistical analysis is executed in this phase. The protocol cannot claim inferential results until the required raw observations and run-level metric values exist.

##### Downstream boundary

CMP-RD-010 remains responsible for visualization. CMP-RD-011 remains responsible for the final experiment matrix. CMP-RD-012 remains responsible for normalization/scaling. No chart, ranking, normalization, or experiment matrix is resolved here.

Decision:
RESOLVED — RESEARCHER-DECIDED

---

### CMP-RD-010 — Visualization Protocol

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Document the downstream visualization layer used to present real simulation results after raw data collection and statistical aggregation, without inventing chart types, scales, normalization, or numerical summaries.

Why this decision is required:
The project architecture and evaluation metrics documents require result export, aggregated summaries, and comparison reporting, but they do not define a final charting protocol. The evidence chain is explicitly:

REAL SIMULATION EXECUTION
        ↓
RAW PER-RUN RESULTS
        ↓
STATISTICAL ANALYSIS
        ↓
AGGREGATED RESULTS
        ↓
FINAL TABLES / CHARTS

This means visualization is downstream of actual execution and analysis; it must not be used to generate or reshape values.

Current evidence:
The repository provides evidence for the need for comparison output but not for a source-defined charting scheme.

- [docs/01-project-overview.md](docs/01-project-overview.md) requires raw results in machine-readable form and lists metric outputs, but it does not define a chart format, plot family, or visual presentation rule.
- [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) defines the primary metrics and states that repeated runs should be summarized, but it does not prescribe exact chart types, axes, or display conventions.
- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) defines metrics collection and result export as common simulator concerns, but not a visualization protocol.
- [docs/06-common-domain-model.md](docs/06-common-domain-model.md) preserves the raw runtime state needed for future statistics and charts, but it does not specify visual encoding.
- [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md) separates decision generation from simulator execution/recording and therefore keeps visualization outside algorithm semantics.
- [docs/02-proposed-method.md](docs/02-proposed-method.md) defines the Proposed Method's multi-stage logic and five native objectives, but it does not specify objective plots, Pareto fronts, or convergence charts.
- [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) defines HRS formulas and fuzzy replacement logic, but it does not specify performance figures or any chart type.
- [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md) defines placement and response-time equations, but it does not provide a source-defined visualization protocol.
- [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md) defines objective concepts and cost-aware behavior, but it does not specify a chart family or display semantics.
- [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) defines multi-objective optimization terms and objective functions, but it does not define Pareto-front or convergence figures as a source requirement.

Researcher decision:
The result-independent presentation protocol is fixed below. It consumes CMP-RD-009 statistical outputs and does not resolve the experiment matrix or normalization boundary.

Dependencies:
- CMP-RD-007 — Common Evaluation Metrics
- CMP-RD-008 — Common Result Schema
- CMP-RD-009 — Statistical Analysis Protocol
- CMP-RD-011 — Experiment Matrix
- CMP-RD-012 — Normalization and Scaling Boundary

Affected methods:
- Proposed Method / Proposed NSGA-III
- HRS
- DPRS
- EIMORM
- OGSA

Classification vocabulary for this section:
- SOURCE-DEFINED
- RESEARCHER-DEFINED
- SIMULATOR-DEFINED
- UNRESOLVED

Only one label is used for each property.

A. Source-defined visualization evidence by method

1. Proposed Method / Proposed NSGA-III source-defined visualization
   - Classification: UNRESOLVED.
   - Evidence: the source documents define the multi-stage method, OIS logic, dynamic replica timing, replica count logic, NSGA-III placement, and five objective terms, but no source document specifies a Pareto-front plot, convergence chart, iteration plot, or other specific figure type for the thesis comparison.
   - Important boundary: NSGA-III is a source-defined optimizer family, not a source-defined chart family.

2. HRS source-defined visualization
   - Classification: UNRESOLVED.
   - Evidence: HRS source material defines centrality, total cost, fuzzy replacement, and performance metrics, but no chart type or figure protocol is explicitly specified in the paper.

3. DPRS source-defined visualization
   - Classification: UNRESOLVED.
   - Evidence: DPRS provides a response-time model and graph-based placement formulation, but no source-defined visualization standard is described.

4. EIMORM source-defined visualization
   - Classification: UNRESOLVED.
   - Evidence: EIMORM defines cost-aware, multi-objective, dynamic replication behavior, but no final figure type or chart protocol is source-defined.

5. OGSA source-defined visualization
   - Classification: UNRESOLVED.
   - Evidence: OGSA defines a five-objective optimization model (MFU, MST, LV, EC, ML), but the source does not specify a visualization family such as Pareto plots, convergence curves, or objective-value charts.

6. Any source-defined chart, figure, or plot for the five methods
   - Classification: UNRESOLVED.
   - Evidence: no project or method-source document identifies a final source-defined visualization protocol shared across all five methods.

B. Visualization is downstream of execution and analysis

7. Raw result capture for later chart generation
   - Classification: SIMULATOR-DEFINED.
   - Evidence: the simulator owns raw observations, event logs, per-run records, and metrics export.
   - Important boundary: the simulator records real data; it does not produce final chart semantics.

8. Statistical aggregation before charting
   - Classification: RESEARCHER-DEFINED.
   - Evidence: [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) requires repeats and summary statistics, but the exact statistical policy is not fixed.
   - Important boundary: chart values must be derived from the statistical layer, not manually fabricated.

9. Final chart generation
   - Classification: RESEARCHER-DEFINED.
   - Evidence: final presentation is a later research decision that depends on the chosen metric set, raw data schema, statistical analysis protocol, and experiment matrix.
   - Important boundary: chart production must be traceable to actual simulation results and analysis outputs.

10. Traceability from final chart to raw simulation result
    - Classification: RESEARCHER-DEFINED.
    - Evidence: the project requires result traceability and auditability; the final chart must be linked to raw per-run data and downstream aggregation.
    - Required chain: FINAL CHART VALUE → STATISTICAL AGGREGATION → RAW PER-RUN RESULTS → REAL SIMULATION EXECUTION.

11. Candidate common comparison chart variables
    - Classification: UNRESOLVED.
    - Evidence: CMP-RD-007 fixes six primary common metrics; conditional metrics remain outside the primary visualization protocol.
    - Examples of candidate variables that remain unresolved: response time, energy consumption, data node load, total cost, centrality, availability, reliability, failed requests, successful requests, request completion rate, replica count, storage utilization, network traffic, replication time, replication overhead, algorithm execution time.

12. Chart axes and units
    - Classification: UNRESOLVED.
    - Evidence: the project does not fix x-axis, y-axis, units, scales, or transformations. The source papers do not provide one universal charting convention that applies across all five methods.

13. Error bars, confidence intervals, and significance shading
    - Classification: UNRESOLVED.
    - Evidence: CMP-RD-009 specifies confidence intervals and significance summaries; CMP-RD-010 now fixes their result-independent visualization semantics.

14. Pareto-front or objective-space visualization for multi-objective methods
    - Classification: UNRESOLVED.
    - Evidence: the source papers define native objective systems, but they do not define a universally required multi-objective plot for the comparison study.
    - Important boundary: native objective semantics must not be converted into a universal chart type unless explicitly required later.

15. Convergence or generation-by-performance plots
    - Classification: UNRESOLVED.
    - Evidence: no source paper or project document identifies convergence plotting as a required comparison output for all five methods.

16. Ranking or winner-order visualization
    - Classification: UNRESOLVED.
    - Evidence: no source-defined ranking formula or winner metric is identified. [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) does not define a final ranking method; CMP-RD-009 supplies statistical comparisons but not a winner score, and CMP-RD-012 explicitly prohibits one.

17. Normalized display scaling or transformation in plots
    - Classification: UNRESOLVED.
    - Evidence: normalization and scaling belong to CMP-RD-012, not the final visualization section.

18. Method-specific visualization versus common comparison visualization
    - Classification: RESEARCHER-DEFINED.
    - Evidence: the project needs both method-specific interpretation and cross-method comparison, but the final separation is not fixed in the source papers.
    - Important boundary: method-specific visualizations must not be confused with the common comparison protocol.

C. Multi-objective method boundaries

19. Proposed Method native objective visualization
    - Classification: UNRESOLVED.
    - Evidence: the Proposed Method's native objective set is fixed as energy consumption, response time, data node load, total cost, and network centrality, but no source-defined plot format is given.

20. OGSA native objective visualization
    - Classification: UNRESOLVED.
    - Evidence: OGSA's native objective model is MFU, MST, LV, EC, and ML, but no source-defined plot family is stated for these objectives.

21. EIMORM native objective visualization
    - Classification: UNRESOLVED.
    - Evidence: EIMORM contains multi-objective, dynamic cost-aware replication logic, but no five-objective chart or equivalent visualization is source-defined.

22. HRS / DPRS / EIMORM native objective visualization is not a common comparison chart
    - Classification: UNRESOLVED.
    - Evidence: each algorithm has distinct source-defined values and optimization logic, but their native objective semantics do not automatically imply one shared plot format.

D. Fairness and integrity constraints relevant to visualization

23. Common metric semantics must remain stable across methods when compared
    - Classification: RESEARCHER-DEFINED.
    - Evidence: fairness in the comparison requires the same interpretation for common metrics across methods, but the exact common metric set and semantics are still open.

24. Visualization must not fabricate or adjust values
    - Classification: RESEARCHER-DEFINED.
    - Evidence: the project explicitly requires real executable result generation and forbids fabricated results. Visualization must therefore be a presentation layer after analysis, not a source of invented numbers.

25. Visualization must not hide unfavorable runs or values
    - Classification: RESEARCHER-DEFINED.
    - Evidence: the comparison design requires the raw results and run statuses to remain traceable and available for later audit.

26. Method-specific charting must not be confused with common cross-method charting
    - Classification: RESEARCHER-DEFINED.
    - Evidence: the common architecture separates common simulation concerns from source-defined method logic; the charting layer must enforce the same separation.

27. Charting must not imply a winner without an explicit, later decision
    - Classification: UNRESOLVED.
    - Evidence: no source-defined ranking or winner score has been identified; CMP-RD-009 supplies effect/statistical comparisons and CMP-RD-012 prohibits a composite winner score.

E. Required open decisions

28. Exact chart types
   - Classification: UNRESOLVED.

29. Exact axes and axis units
   - Classification: UNRESOLVED.

30. Exact plot scaling or display normalization
   - Classification: UNRESOLVED.

31. Exact summary statistics displayed with charts
   - Classification: UNRESOLVED.

32. Exact confidence or error-bar representation
   - Classification: UNRESOLVED.

33. Exact method ordering or ranking in figures
   - Classification: UNRESOLVED.

34. Final table layout for thesis output
   - Classification: UNRESOLVED.

35. Final figure count and composition
   - Classification: UNRESOLVED.

36. Exact mapping from common metrics to final charts
   - Classification: UNRESOLVED.

37. Exact mapping from native objectives to common presentation variables
   - Classification: UNRESOLVED.

Key guardrails:
- Do not change the fixed chart type or axis definition after observing results.
- Do not define normalization or scaling here; CMP-RD-012 owns that boundary.
- Do not define ranking formulas or winner displays in this document.
- Do not create or invent numerical results for charting.
- Do not plot values absent from raw simulation outputs.
- Do not use visualization to imply a source-defined method behavior that the paper never specified.
- Do not force a method-specific objective into a common chart unless the final metric decision explicitly supports it.
- Do not redefine the statistical summaries selected by CMP-RD-009 here; visualization remains CMP-RD-010's responsibility.
- Do not implement plotting code or simulation output generation in this document.

Decision:
OPEN — NOT YET DECIDED

---

### CMP-RD-011 — Experiment Matrix

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Define the pre-registered final comparison experiment matrix without selecting cells after observing results.

Why this decision is required:
The project architecture requires a common comparison framework across all five methods, but the final experiment matrix is not yet defined. The purpose of this decision is structural and scientific: to classify the dimensions that will eventually compose the matrix, while preserving the source-faithful boundary between common external conditions and method-specific internal behavior.

Current evidence:
The repository provides consistent evidence that the experiment must eventually compare five methods under common conditions, but it does not fix the final matrix dimensions or actual values.

- [docs/01-project-overview.md](docs/01-project-overview.md) states that all five methods must be compared under the same system environment, dataset, workload, topology, node characteristics, failure model, and request patterns.
- [docs/03-comparison-methods.md](docs/03-comparison-methods.md) states that only the replication strategy should differ across algorithms while the external environment remains common.
- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) defines the common simulation environment, event scheduling, scenario management, fairness enforcement, result export, and seed management.
- [docs/06-common-domain-model.md](docs/06-common-domain-model.md) defines shared runtime entities such as files, data nodes, users, requests, replicas, failures, and time-aware state transitions.
- [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md) defines the common adapter boundary: algorithms read common state and return decisions, while the simulator validates and executes them.
- [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) defines the common metric set and notes the need for repeated runs, but it does not specify the final experiment matrix.
- [docs/02-proposed-method.md](docs/02-proposed-method.md) defines the Proposed Method's multi-stage process and five native objectives, but it does not fix the experimental matrix to be used in the research comparison.
- [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md), [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md), [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md), and [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) each define method-specific behavior, but none of them defines a common experiment matrix for all five methods together.

Researcher decision required:
The researcher must eventually decide the structure of the experiment matrix used for the five-method comparison. This document preserves the matrix as a structural decision only and does not select any numerical dimension values.

Dependencies:
- CMP-RD-002 — Common Experimental Environment
- CMP-RD-003 — Dataset and Workload
- CMP-RD-004 — Randomness and Reproducibility
- CMP-RD-005 — Failure and Dynamic Scenario Protocol
- CMP-RD-006 — Simulation Horizon and Termination
- CMP-RD-007 — Common Evaluation Metrics
- CMP-RD-008 — Common Result Schema
- CMP-RD-009 — Statistical Analysis Protocol
- CMP-RD-010 — Visualization Protocol
- CMP-RD-012 — Normalization and Scaling Boundary

Affected methods:
- Proposed Method / Proposed NSGA-III
- HRS
- DPRS
- EIMORM
- OGSA

Classification vocabulary for this section:
- SOURCE-DEFINED
- RESEARCHER-DEFINED
- SIMULATOR-DEFINED
- UNRESOLVED

Only one label is used for each property.

A. Structural concept of the experiment matrix

1. Method axis
   - Classification: RESEARCHER-DEFINED.
   - Evidence: the final comparison roster is fixed at five methods, but the formal experiment matrix still needs a method identity convention and a common method label scheme.
   - Important boundary: method identity is not source-defined algorithm behavior; it is a comparison-configuration concern.

2. Dataset / workload scenario axis
   - Classification: RESEARCHER-DEFINED for the final design; SIMULATOR-DEFINED for implementation support.
   - Evidence: [docs/01-project-overview.md](docs/01-project-overview.md) requires a common dataset and workload, and [docs/06-common-domain-model.md](docs/06-common-domain-model.md) defines file and request state, but the final scenario set and scenario labels remain unresolved.

3. System scale axis
   - Classification: RESEARCHER-DEFINED or UNRESOLVED.
   - Evidence: the common architecture requires a topology and node/resource model, but the project does not fix final system sizes or scale levels.

4. Dynamic or failure condition axis
   - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) defines failure infrastructure and dynamic execution support; CMP-RD-005 now defines the registered scenario categories.

5. Repetition / run axis
   - Classification: RESEARCHER-DEFINED or UNRESOLVED.
   - Evidence: the project requires repeated runs, but the final repetition scheme and run axis are not fixed.

6. Matrix structure of the form method × scenario × run
   - Classification: RESEARCHER-DEFINED in principle; UNRESOLVED in final detail.
   - Evidence: the architecture requires planning across methods, scenarios, and repeated runs, but the final matrix organization is not fixed.

B. Common experiment dimensions versus method-specific dimensions

7. Common topology dimension
   - Classification: RESEARCHER-DEFINED for the final experiment; SIMULATOR-DEFINED for runtime support.
   - Evidence: fairness requires all five methods to see the same topology, but the specific graph, scale, and link structure remain unresolved.

8. Common node/resource dimension
   - Classification: RESEARCHER-DEFINED for the final experiment; SIMULATOR-DEFINED for runtime support.
   - Evidence: the common environment includes node capacity, storage, memory, CPU, bandwidth, and latency, but no concrete values are fixed.

9. Common dataset dimension
   - Classification: RESEARCHER-DEFINED for the final experiment; SIMULATOR-DEFINED for runtime state creation.
   - Evidence: [docs/01-project-overview.md](docs/01-project-overview.md) and [docs/06-common-domain-model.md](docs/06-common-domain-model.md) require a common dataset model, but the exact dataset parameters remain unresolved.

10. Common workload dimension
    - Classification: RESEARCHER-DEFINED for the final experiment; SIMULATOR-DEFINED for runtime request generation.
    - Evidence: the project requires identical workload execution across methods, but the final workload definition remains open.

11. Common failure / dynamic scenario dimension
    - Classification: RESEARCHER-DEFINED for the final experiment; SIMULATOR-DEFINED for runtime scheduling.
    - Evidence: the architecture supports failure-event infrastructure and dynamic state changes, but the final dynamic scenario protocol is still open under CMP-RD-005.

12. Common simulation-horizon dimension
    - Classification: RESEARCHER-DEFINED for the final experiment; SIMULATOR-DEFINED for runtime time management.
    - Evidence: the project requires simulation time awareness and run termination handling, but no final horizon is selected.

13. Method-specific internal parameters
    - Classification: SOURCE-DEFINED for the algorithmic parameter meaning; RESEARCHER-DEFINED for experimental configuration when the source is silent; UNRESOLVED when the source does not define them precisely.
    - Evidence: each source method has a distinct internal optimization or decision logic and cannot be assumed to share the same parameter dimensions.
    - Important boundary: method-specific parameters are not dimensions of the common experiment matrix unless the project explicitly chooses to expose them as part of the comparison design.

14. Proposed Method internal algorithm dimensions
    - Classification: SOURCE-DEFINED for conceptual quantities; UNRESOLVED for exact runtime configuration.
    - Evidence: the Proposed Method defines OIS, weighted access frequency, file-type importance, dynamic replica timing, replica count determination, and NSGA-III placement. These are internal to the method and not automatically part of a universal experiment matrix.

15. HRS internal algorithm dimensions
    - Classification: SOURCE-DEFINED for conceptual quantities; UNRESOLVED for final runtime configuration.
    - Evidence: HRS defines centrality, Merit, TotalCost, fuzzy replacement logic, and selection parameters, but it does not define a universal experiment matrix for all methods.

16. DPRS internal algorithm dimensions
    - Classification: SOURCE-DEFINED for conceptual quantities; UNRESOLVED for final runtime configuration.
    - Evidence: DPRS defines response time, transfer time, deployment graph, and placement optimization. The placement model is source-specific and not assumed to be a common comparison dimension.

17. EIMORM internal algorithm dimensions
    - Classification: SOURCE-DEFINED for conceptual quantities; UNRESOLVED for final runtime configuration.
    - Evidence: EIMORM defines multi-objective cost-aware replication, ETBDF, EARF, IEK, availability concepts, and replica-factor logic. It does not provide a final common experiment matrix for the five-method comparison.

18. OGSA internal algorithm dimensions
    - Classification: SOURCE-DEFINED for conceptual quantities; UNRESOLVED for final runtime configuration.
    - Evidence: OGSA defines a decision matrix, file-to-node assignment, objective functions MFU, MST, LV, EC, ML, and optimizer-like population update steps. These remain source-specific and must not be forced onto other methods.

C. Source-defined experiment dimensions actually present in method papers

19. Number of files in source papers
    - Classification: UNRESOLVED.
    - Evidence: source papers discuss files and file sets, but they do not jointly provide a final common file count for the comparison study.

20. Number of data nodes in source papers
    - Classification: UNRESOLVED.
    - Evidence: each method discusses node sets or data-center sets, but the project has not selected a common node-count configuration across the five methods.

21. Number of users or clients
    - Classification: UNRESOLVED.
    - Evidence: the common domain model mentions users and request sources, but no final user-count dimension is fixed.

22. File-size distributions and dataset size
    - Classification: UNRESOLVED.
    - Evidence: file size and dataset size appear as domain variables, but no final generation rule or common dataset size is selected.

23. Request counts and request arrival rates
    - Classification: UNRESOLVED.
    - Evidence: the architecture supports request generation and time-aware simulation, but no final request-rate configuration is fixed.

24. Network topology and graph properties
    - Classification: UNRESOLVED.
    - Evidence: the system is described as a heterogeneous Edge-Cloud environment with data centers, hosts, links, and latency, but no final common network topology is fixed.

25. Failure probability or failure schedule
    - Classification: UNRESOLVED.
    - Evidence: failure concepts appear in the architecture and evaluation metrics; CMP-RD-005 defines deterministic timings without selecting source failure probabilities.

26. Population size / generation count in evolutionary methods
    - Classification: UNRESOLVED.
    - Evidence: OGSA and the Proposed Method describe stochastic optimization populations and iterations, but no common optimizer configuration is fixed across methods and not all methods share the same optimizer family.

27. Data-center, host, and VM counts
    - Classification: UNRESOLVED.
    - Evidence: source papers mention these entities as part of the system architecture, but no final cross-method resource count is selected.

28. Storage, memory, and compute capacities
    - Classification: UNRESOLVED.
    - Evidence: the common experimental environment requires these capacities, but no final values are fixed.

D. Specific scenario categories that are conceptually possible but not fixed

29. Baseline static scenario
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: the project architecture supports common static conditions, but the final inclusion of a baseline static scenario is not fixed.

30. Workload-intensity scenarios
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: dynamic workload and stress scenarios are discussed conceptually, but no final intensity levels are selected.

31. Storage-pressure scenarios
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: storage pressure is a known concern in replica management, but the scenario set is not defined.

32. Network-condition scenarios
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: network latency and bandwidth are common domain concepts, but the project does not fix scenario categories or conditions.

33. Failure scenarios
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: failure events are part of the common architecture and a separate decision document, but the final failure scenario family remains unchosen.

34. Dynamic workload scenarios
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: the environment is time-aware with dynamic events, but no final dynamic scenario set is selected.

35. Sensitivity or scalability scenarios
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: the project mentions dynamic and varying conditions generally, but no source evidence fixes a sensitivity or scaling experiment regime.

E. Fairness and common-configuration principles

36. Common external configuration across all five methods
    - Classification: RESEARCHER-DEFINED for the actual experiment design; SIMULATOR-DEFINED for runtime support.
    - Evidence: the architecture requires that matched methods face the same external environment, but the exact common conditions remain unresolved.

37. Method-specific configuration within each source method
    - Classification: SOURCE-DEFINED or RESEARCHER-DEFINED depending on whether the source is explicit.
    - Evidence: internal parameters belong to each method's own algorithm definition, and different methods cannot be assumed to share the same internal configuration dimensions.

38. Common experiment matrix must not override source-specific algorithm behavior
    - Classification: RESEARCHER-DEFINED as a guardrail.
    - Evidence: the comparison architecture explicitly separates common environment from algorithm-specific logic.

39. Common matrix must remain compatible with real simulation execution
    - Classification: SIMULATOR-DEFINED for support, RESEARCHER-DEFINED for design.
    - Evidence: real simulation execution requires the matrix to correspond to actual runtime configuration and raw result capture.

#### CMP-RD-011 Researcher Decision

##### Primary matrix

The final primary comparison uses exactly one frozen CMP-RD-002 common configuration, the three CMP-RD-003 workloads, the five CMP-RD-005 failure classes, the five canonical methods, and the 30 CMP-RD-004 repetitions.

```text
1 configuration
 x 3 workloads
 x 5 failure scenarios
 x 5 methods
 x 30 repetitions
= 2,250 planned method runs
```

The scenario cross-product contains `3 x 5 = 15` matched workload/failure cells. Each matched cell contains five method executions for each of `rep-01` through `rep-30`, so there are `15 x 30 = 450` matched repetition cells and `2,250` planned method runs. Requests, files, optimizer generations, and individual events are not experiment units.

##### Frozen factors and replay

- Configuration: one `cmp-rd-002-common-env-v1` frozen environment; no additional topology, resource, storage, bandwidth, latency, file-count, or request-rate cells are included in the primary matrix.
- Workloads: W01 Balanced, W02 Stationary Skew, W03 Phase Shift.
- Failures: F0-control, F1-node-transient, F2-site-transient, F3-link-transient, F4-node-persistent.
- Methods: Proposed, HRS, DPRS, OGSA, EIMORM.
- Repetitions: `rep-01` through `rep-30` for every method/workload/failure cell.
- Each repetition receives one frozen scenario, workload artifact, failure artifact, initial state, horizon/drain configuration, and method-local stream identities; all five methods receive identical common artifacts and independent state clones.
- The deterministic method execution order is Proposed, HRS, DPRS, OGSA, EIMORM. Order is operational only and cannot affect results because clones and common artifacts are isolated.

##### Cell and run identities

Each planned execution is identified by canonical serialization of:

`experiment_id | configuration_id | workload_id | failure_scenario_id | repetition_id | method_id`

The identity links to CMP-RD-002 environment/replay digest, CMP-RD-003 workload digest, CMP-RD-005 failure digest, CMP-RD-004 seed identities, CMP-RD-006 horizon/drain version, and CMP-RD-008 run/attempt records. A method attempt receives a distinct `attempt_id` without changing the planned cell identity.

##### Parameter, tuning, and scalability policy

No parameter sweep is included in the primary matrix. CMP-RD-002 common values are not varied, and workload rates, file counts, node counts, failure timings, or failure targets are not changed. Method-specific parameters remain source-defined or separately researcher-required within each method boundary; they are pre-registered before execution and are not forced identical across methods or tuned from final results.

There is no result-driven calibration phase. Any future tuning, sensitivity, scalability, convergence, or native-objective diagnostic experiment is supplementary, separately versioned, and excluded from the primary CMP-RD-009 dataset. No scalability claim is made by this matrix; it evaluates comparative behavior under the frozen common environment.

##### Research-question traceability

| Research purpose | Matrix factor | Primary metrics/statistical evidence |
|---|---|---|
| Balanced versus concentrated access | W01 versus W02 | Response time, reliability, availability, replica count, transfer volume, decision time; CMP-RD-009 summaries/comparisons. |
| Response to predefined popularity change | W03 Phase Shift | Same six metrics across the two workload phases/cell identities; no result-dependent phase changes. |
| No-failure baseline | F0-control | Same six metrics against the common healthy environment. |
| Isolated node outage | F1-node-transient | Reliability, availability, response, transfer, replica, and decision observations under the frozen outage. |
| Correlated site outage | F2-site-transient | Same metrics under site-level loss. |
| Gateway connectivity disruption | F3-link-transient | Response, reliability, availability, transfer, and decision observations under link loss. |
| Persistent primary-node outage | F4-node-persistent | Reliability, availability, response, transfer, replica, and decision observations through the registered boundary. |

This matrix does not create a composite winner score, alter metric directions, or resolve normalization.

##### Technical failure, rerun, and insufficient-data policy

Every planned run is attempted and retained. Technical invalidity, exceptions, malformed artifacts, and timeouts preserve the original attempt and may receive a new rerun `attempt_id` using the same repetition identity and frozen common artifacts. Reruns are not allowed to rescue an unfavorable result.

Scientific request failures and legitimate no-op decisions remain scientific observations in otherwise valid runs. `VALID`, `INVALID`, `UNRESOLVED`, `FAILED`, and `TIMED_OUT` statuses remain visible. CMP-RD-009 determines statistical eligibility; no cell, method, repetition, or scenario is added or removed after result observation. A cell with insufficient usable observations remains reported as statistically insufficient.

##### Experiment manifest

Before execution, the immutable manifest records experiment/configuration/version identities, five methods and fixed order, W01–W03, F0–F4, 30 repetitions, CMP-RD-004 seed/stream policy, CMP-RD-007 metric version, CMP-RD-008 schema version, CMP-RD-009 analysis version, CMP-RD-010 visualization version, CMP-RD-006 horizon/drain and event-order versions, replay/artifact digests, execution-order policy, and prohibitions on tuning, selective exclusion, and result-driven matrix changes. The manifest is a plan, not result data.

##### Computational assessment and implementation gaps

The primary matrix requires 2,250 planned method runs across 450 matched repetition cells. This is a substantial but finite design; its common-state dimensions are fixed at 12 nodes, 100 files, 1,200 requests, and the registered event artifacts. Algorithm-internal population/generation work is not counted as additional experiment runs. No execution-time benchmark is claimed here.

The repository partially supports method registration, frozen-state cloning, deterministic event ordering, provenance scaffolding, and raw observation recording. It lacks a complete matrix manifest loader, workload/failure generators, end-to-end request lifecycle, failure/link execution, causal drain, active RNG streams, canonical artifact digests, complete attempt/result provenance, and executable adapters for all unresolved method policies. These are implementation gaps; the matrix is not executed in this phase.

##### Pre-registration and result independence

The matrix, cell identities, factor levels, repetition count, method order, replay rules, and no-tuning/no-cherry-picking rules are fixed before final execution. Observed metrics, statuses, statistical results, and charts are post-execution data and cannot alter the matrix. Any future matrix change requires a new experiment version and cannot overwrite the original manifest.

F. Matrix structure that remains open

40. Exact method × scenario × run organization
    - Classification: UNRESOLVED.
    - Evidence: the architecture suggests a matrix-like comparison structure, but the final organization and values remain open.

41. Exact scenario set and scenario labels
    - Classification: UNRESOLVED.
    - Evidence: no final set of scenarios has been chosen.

42. Exact scale levels and parameter levels
    - Classification: UNRESOLVED.
    - Evidence: no source paper or project design selects numeric levels for scale, stress, or sensitivity.

43. Exact experiment cell definition
    - Classification: UNRESOLVED.
    - Evidence: the project has not fixed what an experiment cell contains in terms of workload, system scale, failure condition, and repetition.

44. Exact algorithm configuration to be included in the matrix
    - Classification: UNRESOLVED.
    - Evidence: algorithm-specific parameters are method-local and not unified across the five methods.

45. Exact common value selection for network, storage, and topology conditions
    - Classification: UNRESOLVED.
    - Evidence: such values exist as potential experiment dimensions but are not fixed.

46. Exact workload dimensions for all methods
    - Classification: UNRESOLVED.
    - Evidence: the dataset and workload workstream is still open under CMP-RD-003, and the experiment matrix cannot choose them without that decision.

47. Exact repetition axis and ranking across runs
    - Classification: UNRESOLVED.
    - Evidence: repetition and run identity are fixed by CMP-RD-004; run-level aggregation and statistical summaries are fixed by CMP-RD-009.

Key guardrails:
- Do not change the final experiment count, scenarios, workload levels, node/file/request counts, failure protocol, or resource capacities fixed above.
- Do not change the run count or seed policy fixed by CMP-RD-004; do not redefine statistical aggregation fixed by CMP-RD-009.
- Do not force one method's source configuration into the common comparison matrix.
- Do not invent a universal objective vector for all methods.
- Do not convert source-specific parameter values into common experiment dimensions without explicit project approval.
- Do not implement or execute the experiment matrix in this document.

Decision:
RESOLVED — RESEARCHER-DECIDED

---

### CMP-RD-012 — Normalization and Scaling Boundary

Status: RESOLVED / RESEARCHER-DECIDED

Purpose:
Document the methodological boundary between source-defined internal transformations, common simulator measurements, common comparison-layer normalization, and visualization-only scaling, without finalizing any normalization formula or common comparison rule.

Why this decision is required:
The source papers and project architecture do not define one shared normalization policy for all five methods. The project must preserve the distinction between:

A. source-defined internal transformation within an algorithm,
B. raw simulator measurements in native measurable form,
C. a possible future common comparison-layer normalization,
D. visualization-only display scaling.

This decision is therefore about boundary definition and classification, not value selection.

Current evidence:
The repository contains explicit evidence for some source-defined transformations, but not for a universal common comparison normalization protocol.

- [docs/02-proposed-method.md](docs/02-proposed-method.md) states that the Proposed Method's five objectives are normalized before reference-point association in NSGA-III.
- [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) states that the parameters must be transformed into a 1–10 scale before Merit is computed and that the weight vector must satisfy a normalization condition.
- [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) defines a source-internal weighted objective MOF(Ψ) = α1 × U1(Ψ) + α2 × U2(Ψ) + α3 × U3(Ψ) + α4 × U4(Ψ) + α5 × U5(Ψ) and reports equal weights α1 = ... = α5 = 0.2 in the experimental discussion.
- [docs/04-evaluation-metrics.md](docs/04-evaluation-metrics.md) defines common metrics in native operational terms such as energy, time, cost, and centrality, but it does not define a common normalization or comparison-layer scaling policy.
- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) and [docs/06-common-domain-model.md](docs/06-common-domain-model.md) preserve raw simulation state and metric measurements, which supports the requirement that raw values remain available before any future normalization or aggregation.
- [docs/07-algorithm-adapter-contract.md](docs/07-algorithm-adapter-contract.md) requires a clean separation between algorithm decision generation and simulator execution/measurement. That boundary prevents raw metrics from being silently transformed into a common normalized objective at the adapter layer.
- [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md) and [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md) do not provide a comparable source-defined normalization rule for the project-wide comparison layer.

Researcher decision:
The normalization and scaling boundary is resolved below. Primary common comparison uses native metrics; method-internal transformations remain method-owned; display unit conversion is permitted without changing scientific values.

Dependencies:
- CMP-RD-002 — Common Experimental Environment
- CMP-RD-003 — Dataset and Workload
- CMP-RD-004 — Randomness and Reproducibility
- CMP-RD-007 — Common Evaluation Metrics
- CMP-RD-008 — Common Result Schema
- CMP-RD-009 — Statistical Analysis
- CMP-RD-010 — Visualization Protocol
- CMP-RD-011 — Experiment Matrix

Affected methods:
- Proposed Method / Proposed NSGA-III
- HRS
- DPRS
- EIMORM
- OGSA

Classification vocabulary for this section:
- SOURCE-DEFINED
- RESEARCHER-DEFINED
- SIMULATOR-DEFINED
- UNRESOLVED

Only one label is used for each property.

#### CMP-RD-012 Researcher Decision

##### Primary common comparison policy

Primary CMP-RD-007 metrics are compared independently in native units:

- response time: seconds;
- request reliability: proportion `[0,1]`;
- service availability: proportion `[0,1]`;
- active replica count: replica count;
- network transfer volume: bytes/GiB;
- algorithm decision time: milliseconds with clock type.

Raw observations, run-level native metrics, CMP-RD-009 statistical summaries, native confidence intervals, and provenance remain authoritative and immutable. No cross-metric normalization is required or permitted for the primary comparison. Different units represent different research questions and are not combined merely to create a common numerical scale.

No composite score, weighted overall performance score, universal winner index, TOPSIS/SAW/AHP/entropy-weighted ranking, or other overall method rank is defined. Methods are interpreted metric-by-metric using CMP-RD-007 directions; raw values are not inverted to make every metric appear higher-is-better.

##### Method-internal boundary

- Proposed NSGA-III may perform source/contract-required objective normalization, direction handling, OIS weighting, or reference-point preparation internally. Its unresolved formulas/bounds remain unresolved in the Proposed decision boundary. Proposed internal normalized objectives must not be compared directly with other methods' common metrics.
- OGSA may use source/internal MFU/MST/LV/EC/ML, MOF weighting, mass normalization, OBL, and GSA transformations within its method execution. These remain OGSA-native and are not common comparison normalization.
- HRS's source/internal 1–10 transformations, Merit weights, reciprocal terms, and fuzzy scaling remain HRS-owned; unresolved boundaries are not generalized.
- DPRS's source response/transfer/edge-weight transformations remain DPRS-owned and are not a common metric normalizer.
- EIMORM's recency/ratio/cost transformations remain source-specific or unresolved; no formal common objective vector is created.

No method-internal transformation may overwrite common raw observations or change another method's execution.

##### Unit conversion and display boundary

Unit conversion is not normalization. Deterministic conversions such as seconds to milliseconds, bytes to GiB, and proportions to percentages are permitted only for explicitly labeled display or same-quantity reporting. They preserve mathematical meaning, do not alter raw/statistical values, and use one pre-registered rule across the relevant figure/table scope under CMP-RD-010.

##### Cross-method, scenario, and configuration policy

No cross-method min-max, z-score, robust, percentile, vector, pooled, theoretical-bound, ideal/nadir, or reference-point normalization is used for primary metrics. No normalization parameters are estimated from final evaluation results. No normalization varies by method, workload, failure scenario, configuration, or repetition. The same native-unit policy applies across every CMP-RD-011 cell.

Secondary normalized analysis is not part of the pre-registered comparison. Any future proposal would require a new versioned decision before execution and could not overwrite or replace native analysis.

##### Formula and edge-case policy

Min-max, z-score, and robust scaling are **not adopted**. No zero-denominator epsilon is introduced. If a future method-internal transformation encounters a zero range, zero variance, undefined reciprocal, NaN/infinity, invalid dimension, negative physical quantity, or out-of-range value, it retains the raw value where valid and records `UNRESOLVED`, `INVALID`, or `FAILED_MEASUREMENT` according to the owning method/schema policy; it does not fabricate, clamp, or silently drop a value.

Reliability and availability must remain in `[0,1]`; violations are invalid observations, not clipped values. Missing values remain explicit and are never normalized to zero.

##### Statistical and confidence-interval boundary

CMP-RD-009 computes primary summaries, paired bootstrap confidence intervals, permutation tests, multiplicity correction, and effect sizes from native run-level metric values. No normalization occurs before primary metric computation or native statistical analysis. CMP-RD-010 may perform only its pre-registered display unit conversions and layout rules. CMP-RD-012 does not change confidence-interval endpoints or statistical conclusions.

##### Provenance and immutability

Any permitted derived unit-conversion or future explicitly approved normalized value must retain raw observation IDs, metric/method/repetition/scenario/configuration IDs, transformation type, formula/version, scope, units, parameters/bounds, and status. Raw and native derived values remain immutable and are never replaced by transformed values.

##### Governance and readiness boundary

This decision closes the common normalization boundary, not method-specific algorithm ambiguity. Remaining execution-critical method decisions are identified but not resolved here: Proposed objective/NSGA-III policies; HRS weights/fuzzy/tie and normalization boundaries; DPRS graph/tie/lifecycle rules; OGSA binary/feasibility/objective handling; and EIMORM executable ETBDF/IEK/placement/lifecycle policies. These may block final execution, but CMP-RD-012 does not invent their solutions.

Implementation-readiness categories:

- **A. Directly source-supported:** common raw metric recording, native-unit comparison, CMP-RD-004/009/010 identity use, and preservation of method-native quantities as diagnostics.
- **B. Requires explicit method interpretation:** Proposed NSGA-III normalization/association and unresolved objective policies; HRS weights/fuzzy boundaries; DPRS tie/graph/lifecycle interpretation; OGSA assignment/feasibility/objective handling; EIMORM ETBDF/IEK/placement/lifecycle behavior.
- **C. Implementation detail:** unit conversion, canonical serialization, raw-to-derived provenance links, explicit status handling, and immutable artifact retention, provided they do not alter scientific meaning.
- **D. Blocks final comparative execution:** any unresolved method policy required to produce a valid adapter decision, plus missing request/transfer/availability instrumentation and common result execution support. CMP-RD-012 itself does not resolve these blockers.

A. Source-defined normalization and scaling evidence by method

1. Proposed Method / Proposed NSGA-III internal normalization
   - Classification: SOURCE-DEFINED.
   - Evidence: [docs/02-proposed-method.md](docs/02-proposed-method.md) explicitly states that the five objectives must be normalized before reference-point association in NSGA-III.
   - Important boundary: this is an internal algorithm transformation required by the source algorithm. It does not automatically become a common cross-method normalization rule.

2. HRS internal normalization
   - Classification: SOURCE-DEFINED.
   - Evidence: [docs/algorithms/HRS-spec.md](docs/algorithms/HRS-spec.md) states that parameter values differ in scale and therefore must be transformed to a 1–10 scale before Merit is computed; it also specifies a uniform normalization rule and the weight-sum condition Σ W_i = 1.
   - Important boundary: this source-defined normalization belongs to HRS and must not be applied to the other methods.

3. DPRS internal normalization
   - Classification: UNRESOLVED.
   - Evidence: [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md) defines response-time and placement behavior, but no explicit source-defined normalization or scaling procedure is identified for the project-wide comparison layer.

4. EIMORM internal normalization
   - Classification: UNRESOLVED.
   - Evidence: [docs/algorithms/EIMORM-spec.md](docs/algorithms/EIMORM-spec.md) discusses multi-objective cost, load, and availability trade-offs but does not provide a formal normalized objective vector or source-defined scaling rule in the source-faithful specification.

5. OGSA internal objective transformation
   - Classification: SOURCE-DEFINED.
   - Evidence: [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) defines a weighted objective function MOF(Ψ) = α1 × U1(Ψ) + α2 × U2(Ψ) + α3 × U3(Ψ) + α4 × U4(Ψ) + α5 × U5(Ψ) and the paper reports equal weights α1 = ... = α5 = 0.2 in the experimental discussion.
   - Important boundary: this is OGSA's source-defined weighted objective treatment. It is not a universal common comparison normalization protocol.

6. Generalized cross-method normalization
   - Classification: UNRESOLVED.
   - Evidence: no project document states that all five methods must be normalized in the same way before comparison.
   - Important boundary: algorithm-internal objective normalization is not equivalent to a common comparison-layer normalization policy.

B. Algorithm-internal normalization versus common comparison-layer normalization

7. Algorithm-internal transformation required by a source method
   - Classification: SOURCE-DEFINED when explicitly stated by the source.
   - Evidence: Proposed Method normalization prior to NSGA-III reference-point association; HRS uniform 1–10 scaling before Merit; OGSA weighted objective formulation.

8. Raw common simulator measurements
   - Classification: SIMULATOR-DEFINED for measurement capture, RESEARCHER-DEFINED for the metric choice.
   - Evidence: response time, energy consumption, total cost, data node load, request counts, replica counts, network traffic, availability, and reliability should remain in their native measurable form unless the source or project explicitly says otherwise.
   - Important boundary: raw simulator state must remain available before any future normalization or statistical analysis.

9. Common comparison-layer normalization
   - Classification: RESEARCHER-DEFINED or UNRESOLVED.
   - Evidence: the project architecture allows a later comparison layer that might aggregate or compare metrics across methods, but no explicit common normalization rule is specified in the source papers or comparison design.
   - Important boundary: no final common normalization formula is chosen here.

10. Visualization-only scaling
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: display scaling such as linear, logarithmic, percentage, scientific notation, or axis remapping is downstream of raw measurement and analysis; it is not algorithmic normalization.
    - Important boundary: visualization scaling must not be treated as source-defined algorithm behavior.

C. Direction and units of metrics

11. Proposed Method objective directions
    - Classification: SOURCE-DEFINED.
    - Evidence: the Proposed Method explicitly minimizes energy consumption, response time, data-node load, and total cost, and maximizes closeness centrality.
    - Important boundary: direction is source-specific to the Proposed Method and must not be generalized to other methods without explicit evidence.

12. HRS objective and cost direction
    - Classification: SOURCE-DEFINED.
    - Evidence: HRS minimizes TotalCost and uses a Merit-based selection logic in a cost-sensitive replica evaluation framework.
    - Important boundary: the source-defined direction is HRS-specific and not a universal comparison rule.

13. DPRS metric direction
    - Classification: UNRESOLVED.
    - Evidence: DPRS defines response-time and placement behavior, but the project has not yet fixed a common comparison direction for this method at the cross-method level.

14. EIMORM metric direction
    - Classification: UNRESOLVED.
    - Evidence: EIMORM discusses availability, cost, load, and dynamic re-replication trade-offs conceptually, but it does not establish a final common direction or unit convention for a method-wide comparison layer.

15. OGSA objective direction
    - Classification: SOURCE-DEFINED.
    - Evidence: OGSA states that the objective is to minimize MOF and that availability is improved indirectly by minimizing MFU; the source defines the optimization direction internally.
    - Important boundary: this direction is OGSA's model, not a universal direction for the common method comparison.

16. Metric units and native scales
    - Classification: UNRESOLVED for the final comparison layer.
    - Evidence: the source documents provide examples of native units or quantities such as time, energy, cost, centrality, probability, and load, but the project has not chosen a final mapping of all common metrics to units, scales, or dimensionless forms.
    - Important boundary: unit conversion is not automatic normalization.

D. Cross-method fairness and comparability

17. Raw metric comparison without common-layer normalization
    - Classification: RESEARCHER-DEFINED or UNRESOLVED.
    - Evidence: the project may eventually compare raw common metrics directly when they are genuinely common and measured in the same native way. However, the source papers and current project docs do not define a universal cross-method rule for when raw values may be compared directly versus first transformed.
    - Important boundary: this is an unresolved comparison policy, not a source-defined scientific fact.

18. Method-specific objective normalization compared with common metric normalization
    - Classification: RESEARCHER-DEFINED as a boundary rule; UNRESOLVED in final policy.
    - Evidence: a method's internal objective normalization does not imply a common metric normalization for all five methods.
    - Important boundary: HRS normalization, Proposed Method objective normalization, and OGSA weighted objective formulation are not automatically the same mechanism as a common comparison-layer normalization.

19. Fairness doctrine for future normalization
    - Classification: RESEARCHER-DEFINED as a methodological principle.
    - Evidence: any future comparison-layer normalization must not change algorithm behavior, must not hide unfavorable results, must preserve raw values, and must remain traceable to the exact raw observations used to produce the normalized value.
    - Important boundary: fairness is a project rule, not a mathematical normalization formula.

E. Rejected or prohibited common-normalization options

20. Exact common normalization formula
    - Classification: RESEARCHER-DEFINED.
    - Evidence: CMP-RD-012 explicitly prohibits a common normalization formula for the primary comparison; min-max, z-score, vector, percentile, theoretical-bound, pooled, and per-run normalization are not adopted.

21. Exact common weighting scheme
    - Classification: RESEARCHER-DEFINED.
    - Evidence: no cross-method weighting scheme is permitted; source-method weights remain internal.

22. Exact threshold or significance boundary for normalization
    - Classification: UNRESOLVED.
    - Evidence: no threshold or cut-off rule is identified in the source or project documents.

23. Exact reference point, ideal point, or nadir point policy
    - Classification: UNRESOLVED.
    - Evidence: the project does not define a comparison-layer reference-point policy.

24. Exact normalization data boundary
    - Classification: RESEARCHER-DEFINED.
    - Evidence: no primary normalization data boundary exists because common normalization is prohibited; future secondary proposals require a new decision.

25. Exact ranking or composite score built from normalized metrics
    - Classification: UNRESOLVED.
    - Evidence: no source-defined common ranking formula or composite score has been identified; CMP-RD-009 provides statistical comparisons but does not create a composite winner score.

26. Exact visualization scaling policy for charts
    - Classification: RESEARCHER-DEFINED by CMP-RD-010.
    - Evidence: display-only unit conversion and layout belong to CMP-RD-010; CMP-RD-012 does not alter that resolved policy.

27. Exact handling of mixed-direction objectives, benefit/cost semantics, and units
    - Classification: UNRESOLVED.
    - Evidence: the source papers do not fix a common benefit/cost direction for all metrics across the five methods.

F. Traceability and data boundary

28. Raw values remain recoverable
    - Classification: SIMULATOR-DEFINED for storage and export; RESEARCHER-DEFINED for requirement policy.
    - Evidence: raw per-run measurements must remain available before any future normalization, aggregation, or chart generation.

29. Normalized values must be traceable to raw values
    - Classification: RESEARCHER-DEFINED.
    - Evidence: the project requires result auditability; any normalized value must be fully traceable to the exact raw simulation observation and the exact normalization rule used.

30. No manual construction of normalized values
    - Classification: RESEARCHER-DEFINED as a guardrail.
    - Evidence: fabricated normalized values are not permitted.

31. Source-defined internal normalization must not be generalized to the comparison layer
    - Classification: RESEARCHER-DEFINED as a boundary rule.
    - Evidence: the project architecture and source evidence require separation of method-specific internal behavior from common comparison behavior.

Key guardrails:
- Do not add a min-max, z-score, robust, vector, pooled, or reference-bound normalization to the primary comparison.
- Do not choose weights for cross-method comparison.
- Do not choose thresholds, ideal/nadir points, or cost/benefit scaling constants for a common score.
- Do not impose HRS, Proposed Method, or OGSA internal normalization on other methods.
- Do not modify any source-defined objective function.
- Do not create a common ranking formula or composite score in this section.
- Do not convert raw simulator measurements into normalized values; any future exception requires a new explicit project decision.
- Do not use display scaling as a hidden algorithmic transformation.
- Do not implement normalization code or execute simulations in this document.

Decision:
RESOLVED — RESEARCHER-DECIDED

---

### CMP-RD-013 — OGSA Gravitational Search Identity

Status: DECIDED — SCOPED EXECUTABLE INTERPRETATION

Related decisions:
- CMP-RD-002 — Common Experimental Environment
- CMP-RD-004 — Randomness and Reproducibility

Purpose:
Record the executable project interpretation of the contradictory gravitational-search terminology in the OGSA source without rewriting the source ambiguity as if it did not exist.

Source evidence:
- OBL is explicitly source-supported, including the opposite-solution relation.
- GSA-style mass, acceleration, gravitational constant, velocity, and position equations are explicitly present.
- The optimization workflow is GSA-oriented.
- GSO appears as conflicting terminology in the source.
- The source does not provide GSO-specific equations, update rules, parameters, or pseudocode sufficient for a source-faithful executable GSO implementation.

Researcher decision:
For the executable project interpretation of OGSA, use OBL + GSA.

Interpretation boundary:
1. The researcher selects GSA because it has direct equation-level and workflow-level source evidence.
2. This selection is a RESEARCHER-REQUIRED interpretation used to make the source executable; it is not a claim that the paper unambiguously says GSA.
3. The contradictory GSO terminology remains documented in [docs/algorithms/OGSA-spec.md](docs/algorithms/OGSA-spec.md) and [docs/algorithms/OGSA-implementation-contract.md](docs/algorithms/OGSA-implementation-contract.md).
4. GSO terminology is not silently rewritten or erased.
5. No GSO implementation, equations, parameters, update rules, or pseudocode may be invented.

Remaining OGSA OPEN items:
- continuous-to-binary assignment conversion;
- infeasible-solution handling;
- constraint repair, rejection, or penalty policy;
- exact initialization distribution;
- complete optimizer parameterization;
- exact OBL/GSA interaction order where the source remains unspecified.

This decision does not change CMP-RD-012 or any unrelated decision.

Decision:
DECIDED — SCOPED EXECUTABLE INTERPRETATION

---

## 7. Cross-Method Fairness

---

## 7. Cross-Method Fairness

Fairness across the five methods must be achieved primarily through common experimental conditions and common evaluation procedures, while preserving legitimate algorithm-specific behavior.

The comparison layer must not silently impose one method's internal logic onto another method.

Examples of prohibited fairness shortcuts:

- forcing the same optimizer across methods
- forcing the same objective across methods
- forcing the same replica factor across methods
- forcing the same placement algorithm across methods
- forcing the same file-selection mechanism across methods
- forcing the same internal normalization across methods
- importing behavior from one method into another

Any such choice must be a separate researcher decision and must be documented explicitly as a deliberate experimental policy, not as a common scientific fact.

The comparison layer must preserve the following distinction:

- common conditions: shared topology, workload, dataset, simulation time, metrics, fairness checks
- algorithm-specific conditions: source-defined optimizer, objective formulation, replica-count logic, placement logic, provider logic, file selection, internal parameters, and method-specific repair or recovery behavior

---

## 8. Comparison-Level Prohibited Shortcuts

The following must not be silently introduced as if they were part of the source papers or common comparison design:

- inventing behavior from methods outside the final five-method scope
- inventing DPRS behavior
- inventing Proposed Method behavior
- importing NSGA-III into other methods
- importing EIMORM IEK / ETBDF / EARF into other methods
- importing OGSA GSA / OBL behavior into other methods
- inventing common replica factors
- inventing common placement heuristics
- silently repairing formulas
- treating common metrics as algorithm objectives
- treating visualization normalization as algorithm normalization

If any of these are later used, they must be recorded as explicit researcher-defined extensions, not as paper-defined or comparison-default behavior.

---

## 9. Implementation Blockers

The following issues block implementation if unresolved.

These blockers are derived from the common architecture audit and remain OPEN at this stage.

### A. Common environment blockers
- common topology
- common node/site/resource specification
- common initial state
- common storage and network assumptions

### B. Workload blockers
- common dataset generator
- common workload generator
- common file-size and request distribution policy

### C. Reproducibility blockers
- seed policy
- repetition count
- independent-run policy
- scenario replay policy

### D. Evaluation blockers
- common metric definition set
- measurement rules for raw metric values
- result schema
- aggregation protocol
- statistical protocol

### E. Comparison blockers
- experiment matrix
- fairness review policy
- normalization boundary
- visualization contract

These issues are identified as decision blockers only. They are not implemented here and are not resolved in this file.

---

## 10. Self-Audit

- [ ] No algorithm source behavior invented
- [ ] No obsolete or out-of-scope method behavior was invented
- [ ] No DPRS behavior invented
- [ ] No Proposed Method behavior invented
- [ ] No EIMORM behavior imported
- [ ] No OGSA behavior imported
- [ ] No NSGA behavior imported into other methods
- [ ] No formula silently repaired
- [ ] No common objective imposed
- [ ] No common replica factor invented
- [ ] No common placement heuristic invented
- [ ] No unrelated researcher decision accidentally marked DECIDED
- [ ] Common vs algorithm-specific behavior preserved
- [ ] Evaluation metrics separated from algorithm objectives
- [ ] Visualization normalization separated from algorithm normalization
- [ ] No implementation code added

All unrelated genuine researcher decisions remain OPEN; CMP-RD-001, CMP-RD-002, CMP-RD-002-HRS-001, and CMP-RD-013 are the explicitly decided roster, environment, replay, and OGSA identity decisions.

---

## 11. Final Status

This document is a comparison-level researcher decision register only.
It exists to ensure that the common comparison architecture is made executable and reproducible without converting unresolved or simulator-defined behavior into source-defined algorithm behavior.

At the time of creation:

- CMP-RD-001 is DECIDED; other unresolved comparison-level researcher decisions remain OPEN
- no implementation behavior is introduced
- no method-specific scientific behavior is invented
- no source paper is modified
- no comparison-level decision is prematurely closed

---

## 12. Cross-Decision Audit Report

A. Overall audit status: CLEAN WITH MINOR FINDINGS

The current register is internally coherent in its high-level intention: CMP-RD-001, CMP-RD-002, and the two scoped decisions are explicitly identified as DECIDED, the remaining unresolved parent comparison decisions remain OPEN, the five-method roster is preserved, and no implementation or fabricated result generation is introduced in the current document. The minor findings below are consistency and wording issues, not evidence of any additional finalized decision or a source violation.

B. Method roster consistency
- Status: PASS WITH MINOR OBSERVATION
- Findings:
  - The register consistently keeps the five-method comparison scope: Proposed Method / Proposed NSGA-III, HRS, DPRS, EIMORM, and OGSA.
  - The obsolete legacy-replication labels are absent.
  - The legacy HSR-style label is not treated as a separate method.
  - No sixth method is introduced in the current document.
- Minor observation:
  - Some wording contains shorthand and explanatory aliases that are acceptable for clarity, but they must not be confused with a separate method identity.

C. Decision-status consistency
- Status: PASS
- Findings:
    - CMP-RD-001 through CMP-RD-012, CMP-RD-002-HRS-001, and CMP-RD-013 are DECIDED.
    - No unrelated decision is marked DECIDED, FROZEN, FINAL, or equivalent in the current text; the four explicitly resolved decisions are identified.
  - The open-status pattern is consistent with the document's purpose and scope.

D. Cross-decision contradictions
- Status: NO DIRECT CONTRADICTION FOUND
- Findings:
  - The major distinction between common environment, workload, method-specific behavior, and statistical/visualization layers is preserved.
  - No direct contradiction was found between the five-method scope and the later decision sections.
- Minor risk:
  - The document occasionally uses broad wording such as "common evaluation layer" and "common comparison layer" without yet defining the exact final boundary, which is an OPEN-design risk rather than a contradiction.

E. Possible SOURCE-DEFINED misclassifications
- Status: MINOR FINDINGS
- Findings:
  - A few statements in later sections rely on broad classification language rather than source-specific evidence when discussing common or project-wide behavior.
  - This is not a direct misclassification in the current file, but some sections may read as if a project requirement is source-defined when it is actually a researcher or simulator concern.
- Examples of audit concern:
  - statements describing common randomness, common charting requirements, and comparison-layer fairness rules are project-level decision concerns, not source-defined method behavior.
  - This is acceptable only if clearly documented as project design rather than manuscript evidence.

F. Accidental numerical decisions
- Status: PASS
- Findings:
  - No final workload counts, node counts, file counts, request counts, failure probabilities, significance thresholds, confidence levels, or repetition counts were found as finalized values in the current decision register.
  - No exact plotting or ranking numbers were introduced by the current document.
- Minor observation:
  - Some sections explicitly mention candidate metric names and candidate properties, but these remain unresolved and therefore do not become accidental numerical decisions.

G. Common-vs-method-specific boundary issues
- Status: PASS WITH MINOR RISK
- Findings:
  - The register consistently distinguishes common experiment conditions from method-specific logic.
  - The main guardrails repeatedly preserve the separation between external fairness conditions and internal algorithm behavior.
- Minor risk:
  - Because the document remains OPEN, the common environment and workload sections are intentionally broad. This creates a risk of reading those sections as if they had already decided a common topology or workload profile, but the current text does not do so.

H. Normalization boundary issues
- Status: PASS
- Findings:
  - The normalization section clearly distinguishes algorithm-internal transformation from comparison-layer normalization and visualization scaling.
  - The document does not invent a cross-method normalization formula.
  - The document does not impose HRS, Proposed Method, or OGSA internal normalization on the other methods.
- Minor observation:
    - The boundary is structurally correct; CMP-RD-012 is resolved as a prohibition on common normalization while remaining separate from source-specific algorithm formulas.

I. Raw-result traceability issues
- Status: PASS
- Findings:
  - The register preserves the intended traceability path:
    REAL SIMULATION EXECUTION
    → RAW OBSERVATIONS
    → RAW PER-RUN RESULTS
    → STATISTICAL ANALYSIS
    → AGGREGATED RESULTS
    → FINAL TABLES / CHARTS
  - Raw values are not replaced by aggregated values in the current document.
- Minor risk:
  - Future sections must preserve raw values as the authoritative source even when normalization or plotting becomes relevant later.

J. Fabrication-risk issues
- Status: PASS
- Findings:
  - No fabricated result values, chart values, numerical summaries, or hand-authored performance curves were introduced.
  - No implementation or simulation execution was performed in the current document.
  - The register explicitly preserves open decisions and rejects fabricated outputs.

K. Dependency inconsistencies
- Status: PASS WITH MINOR NOTE
- Findings:
  - The dependency framework is conceptually consistent: common environment and workload decisions precede metric, result-schema, statistics, and visualization decisions.
    - CMP-RD-011 is resolved as the primary matrix; CMP-RD-012 is resolved as the normalization/scaling boundary.
- Minor note:
  - The dependency model is intentionally conceptual and does not impose a strict one-to-one ordering; this is acceptable for the decision register and should remain conceptual only.

L. Required corrections, if any
- Status: NO MANDATORY CORRECTION REQUIRED
- Findings:
  - No mandatory correction is required to keep the decision register in a source-faithful, open, and non-finalized state.
  - Optional wording-only cleanup would be the only possible refinement, but such cleanup is not required for scientific correctness or process compliance.
- Audit conclusion:
  - The register is acceptable as an OPEN decision register and does not require a decision-level correction at this time.

---

## 13. Final Status

This document remains a comparison-level researcher decision register only.
It exists to preserve source-faithful boundaries without finalizing algorithm behavior, simulator behavior, statistical methods, visualization methods, or common normalization rules.

At the time of this audit:

- CMP-RD-001 is DECIDED; other unresolved comparison-level researcher decisions remain OPEN
- the five-method roster remains consistent
- no implementation or simulation executes from this document
- no fabricated results are introduced
- no decision was silently finalized during this audit
- the document remains suitable for future implementation planning without prematurely closing scientific or methodological questions

---

## 14. Freeze Readiness Audit

### Audit purpose
This audit determines whether the current researcher-decision register is sufficiently complete, internally consistent, and appropriately bounded to serve as the governing decision boundary for the next implementation phase, while remaining open and source-faithful.

This is a readiness assessment only. It does not freeze any parent decision or resolve any unrelated unresolved issue; the four explicitly resolved decisions are recorded separately and explicitly.

### Audited decisions
- CMP-RD-001 — Final Method Roster and Naming
- CMP-RD-002 — Common Experimental Environment
- CMP-RD-003 — Dataset and Workload
- CMP-RD-004 — Randomness and Reproducibility
- CMP-RD-005 — Failure / Dynamic Scenario
- CMP-RD-006 — Simulation Horizon and Termination
- CMP-RD-007 — Common Evaluation Metrics
- CMP-RD-008 — Common Result Schema
- CMP-RD-009 — Statistical Analysis Protocol
- CMP-RD-010 — Visualization Protocol
- CMP-RD-011 — Experiment Matrix
- CMP-RD-012 — Normalization and Scaling Boundary

### Source-faithfulness assessment
- Status: PASS WITH MINOR RISKS
- Findings:
  - The register keeps source-defined behavior distinct from researcher-defined decisions and simulator-defined behavior.
  - The main risk is not a contradiction but the possibility that some sections read as if a project design rule were source-defined when it is actually a common-experiment or researcher decision.
  - This is acceptable in an OPEN register if the classification remains explicit; the current document does maintain that distinction in most sections.
- Risk summary:
  - Proposed Method: source-defined multi-stage logic and native objectives are preserved.
  - HRS: source-defined merit/cost/fuzzy behavior is preserved as internal to HRS.
  - DPRS: not over-specified; no invented logic found.
  - EIMORM: no invented five-objective vector or normalization rule was introduced.
  - OGSA: source-defined objective set and weighted MOF treatment are preserved as internal to OGSA.

### Method-scope assessment
- Status: PASS
- Findings:
  - The register consistently contains exactly the five-method scope:
    1. Proposed Method / Proposed NSGA-III
    2. HRS — Hybrid Replication Strategy
    3. DPRS
    4. EIMORM
    5. OGSA
  - HRS and HSR are not treated as separate methods.
  - HER and APRS are absent.
  - Proposed Method remains a multi-stage method, not merely NSGA-III.
  - The multi-stage structure is preserved in the register's conceptual framing and source-boundary statements.

### Common-vs-method-specific assessment
- Status: PASS
- Findings:
  - The register repeatedly distinguishes common external experimental conditions from method-specific internal algorithm conditions.
  - This separation is a critical readiness feature because it prevents hidden cross-method behavior changes.
  - The project is not yet ready to encode concrete experimental parameter values, but the boundary itself is well documented.
- Risk:
  - The boundary is conceptually strong even while unresolved; the implementation phase must continue to respect it.

### Numerical-value assessment
- Status: PASS
- Findings:
  - The document does not finalize concrete experiment values such as file counts, request counts, node counts, failure probabilities, run counts, significance thresholds, or chart metrics.
  - The register does not contain a silent conversion from source-specific numbers to common experimental values.
  - This is a major readiness strength because it prevents accidental over-specification before implementation.
- Risk:
  - Only future experiment design decisions can add final numeric values, and those must remain explicit and intentionally selected.

### Dependency assessment
- Status: PASS WITH MINOR RISKS
- Findings:
  - The dependency structure is conceptually consistent between environment, workload, randomness, metrics, schema, statistics, visualization, experiment matrix, and normalization.
  - The cross-dependencies are documented well enough to identify future ordering without forcing a false linearization.
- Minor risks:
  - Several decisions remain intentionally broad; this is not a contradiction, but future implementation will need exact dependency expansion when the experimental design is eventually frozen.

### Implementation-readiness assessment
- Status: READY FOR IMPLEMENTATION CONTRACTS WITH OPEN DECISIONS
- Findings:
  - The register is sufficiently explicit to let an implementation team understand what is source-defined, what is researcher-defined, what is simulator-defined, and what remains unresolved.
  - This is the key boundary needed before implementation contracts are written.
  - The document does not require developers to invent or infer method behavior beyond the source boundaries.
- Important caveat:
  - The implementation phase still cannot proceed to executable simulation without the later researcher decisions that remain intentionally OPEN.

### Criteria A–J
A. Five-method scope is stable. — PASS
B. Source-defined algorithm behavior is protected. — PASS
C. Common-vs-method-specific boundary is explicit. — PASS
D. Open researcher decisions are explicitly documented. — PASS
E. No accidental numerical experiment decisions exist. — PASS
F. Raw-result traceability is protected. — PASS
G. Statistical and visualization layers are downstream. — PASS
H. Normalization boundary is explicit. — PASS
I. Dependencies are documented. — PASS WITH MINOR RISKS
J. No critical contradiction remains. — PASS

### Final readiness classification
READY FOR FREEZE WITH MINOR RISKS

The register is sufficiently complete and internally consistent to serve as the governing boundary for the next implementation phase, provided that the decisions remain OPEN and the future implementation work does not silently resolve them.

### Minor risks
- The decision descriptions remain intentionally broad in several places, which is correct for OPEN decisions but requires future tightening when a freeze is eventually attempted.
- Some classification statements may still be read too casually as source-defined when they are actually project-level design concerns; the line is clear enough in most sections, but not every wording instance is equally explicit.
    - The dependency model is conceptually sound; CMP-RD-012 is a completed boundary contract even though method-specific execution gaps remain.

### Blocking risks
- No blocking risk is found in the current register for freeze-readiness as a decision-boundary document.
- The only block to implementation itself is the absence of later final decisions (metrics, statistical protocol, visualization protocol, experiment matrix, etc.), which is intentional and not a flaw in the archive.

### Required actions before freeze
- Required actions are not a correction of the current register; they are future design actions to be completed after the freeze-readiness audit if the project chooses to move toward a final implementation phase.
- These findings remain audit-only and do not change the status of any CMP-RD.
- The required future actions are:
  1. finalize the final common metric set under CMP-RD-007
  2. finalize the raw result schema under CMP-RD-008
  3. finalize the statistical analysis protocol under CMP-RD-009
  4. finalize the visualization protocol under CMP-RD-010
  5. finalize the experiment matrix under CMP-RD-011
  6. finalize the common normalization boundary under CMP-RD-012, if and when a common comparison-layer normalization is explicitly justified
  7. keep method-specific source semantics separate from common comparison semantics throughout later implementation work

---

## 15. Final Status

The current researcher-decision register is suitable as an OPEN governing boundary for the next implementation phase, subject to the standard requirement that future design work must continue to respect the source-faithful and method-specific boundaries already documented in this file.

The parent register is not frozen or finalized here. It remains ready as a decision boundary, with only the two explicitly scoped decisions recorded as decided, and not as an executable implementation plan.

---

## 16. Governance Freeze

### Freeze purpose
This document is now subject to a governance freeze. The purpose of this freeze is to lock the current decision boundaries, source-faithful constraints, method scope, and open/unresolved status for the next implementation phase without inventing missing values or resolving currently OPEN decisions.

This is a boundary freeze only. It does not mean that every OPEN researcher decision has been numerically resolved.

### Freeze scope
This freeze governs the following boundary conditions:

- the source-faithful method roster and naming constraints
- the source vs researcher vs simulator vs unresolved classification scheme
- the common-vs-method-specific boundary
- the preservation of method-specific algorithm behavior and objective sets
- the requirement that all explicitly unresolved decisions remain unresolved
- the requirement that implementation must not silently invent missing values
- the requirement that raw result traceability be preserved
- the requirement that no implementation or simulation work is performed from this document

### Freeze date
2026-09-05

### Freeze scope: method roster
The comparison roster is frozen as exactly these five methods:

1. Proposed Method / Proposed NSGA-III
2. HRS — Hybrid Replication Strategy
3. DPRS
4. EIMORM
5. OGSA

Naming constraints frozen by governance:
- HRS and HSR are the same method.
- HSR must not become a separate method.
- no additional method alias may be introduced as a separate method.
- No sixth method may be introduced.

### Freeze scope: source-faithful boundary
The following source-faithful boundaries are frozen:

- Proposed Method is not simply NSGA-III and remains a multi-stage method.
- Proposed Method's native objectives remain unchanged: Energy Consumption, Response Time, Data Node Load, Total Cost, and Network Centrality.
- HRS preserves its source-defined logic, merit/fuzzy/replacement behavior, and internal normalization semantics.
- DPRS preserves its source-defined behavior without invented optimizer or recovery mechanisms.
- EIMORM preserves its source-faithful ETBDF/EARF/IEK interpretation without inventing a formal five-objective vector or Pareto formulation.
- OGSA preserves MFU, MST, LV, EC, ML, the source-defined weighted MOF formulation, and OGSA-specific optimizer behavior.
- No baseline is to receive Proposed Method behavior merely for experimental convenience.

### Freeze scope: classification boundary
The classification framework is frozen as:

- SOURCE_DEFINED
- RESEARCHER_DEFINED
- SIMULATOR_DEFINED
- UNRESOLVED

This freeze prevents silent conversion of UNRESOLVED items into researcher choices during implementation.

### Freeze scope: common vs method-specific boundary
The distinction between common external experimental conditions and method-specific internal algorithm behavior is frozen.

Common external experimental conditions may eventually include the topology, resource environment, dataset, workload, network environment, initial state, externally imposed dynamic/failure conditions, simulation horizon, and reproducibility controls, but any unresolved numerical values remain unresolved.

Method-specific behavior includes objectives, fitness functions, OIS logic, selection mechanisms, placement strategies, replication timings, replacement rules, optimizer parameters, source-specific thresholds, algorithm-specific iteration limits, and source-defined internal mechanisms.

This boundary is not a justification to standardize baselines by convenience.

### Freeze scope: randomness and reproducibility boundary
The following distinctions are frozen:

- COMMON SCENARIO RANDOMNESS
- ALGORITHM-INTERNAL RANDOMNESS

Source-defined algorithm randomness must remain source-defined.
The common experiment must preserve reproducibility without converting source-specific random behavior into a universal comparison rule.
No exact run count, seed values, seed schedule, replay policy, or repetition protocol is invented by this freeze.

### Freeze scope: failure and dynamic behavior boundary
The distinction between failure occurrence, failure detection, replica unavailability, algorithm response, reconstruction, node recovery, and replacement is frozen.

This freeze prevents:
- reinterpretation of replacement as recovery
- invented runtime recovery behavior for methods where it is not source-defined
- invented failure-triggered NSGA-III reoptimization
- conversion of OGSA availability or failure-probability logic into an assumed common runtime simulator policy

### Freeze scope: metrics, schema, statistics, visualization, matrix, and normalization
The following remain frozen as open, unresolved comparison decisions unless and until a later, explicit researcher choice is made:

- CMP-RD-007 — Common Evaluation Metrics
- CMP-RD-008 — Common Result Schema
- CMP-RD-009 — Statistical Analysis Protocol
- CMP-RD-010 — Visualization Protocol
- CMP-RD-011 — Experiment Matrix
- CMP-RD-012 — Normalization and Scaling Boundary

This freeze preserves the conceptual separation between:
- native algorithm objectives
- common comparison metrics
- raw per-run observations
- statistical analysis
- visualization and charting
- method-internal normalization
- common comparison-layer normalization

### Open decisions after freeze
The following remain OPEN and must be resolved explicitly before they are required for final experimental execution:

- CMP-RD-004 randomness/repetition details
- CMP-RD-005 failure/dynamic protocol
- CMP-RD-006 simulation horizon
- CMP-RD-007 final common metrics
- CMP-RD-008 concrete result schema
- CMP-RD-009 statistical protocol
- CMP-RD-010 visualization protocol
- CMP-RD-011 final experiment matrix
- CMP-RD-012 common normalization/scaling rule, if justified

Important clarification:
These decisions remain OPEN after the freeze. The freeze locks the boundary, not the missing numerical or procedural values. These items are not numerically resolved by this freeze.

### Implementation governance statement
After this freeze, implementation must not silently make research decisions.

If implementation encounters an unresolved research decision that affects correctness, the issue must be surfaced as a researcher-decision change rather than silently choosing a value or behavior.

Algorithm implementations must remain traceable to their corresponding source specification and implementation contract.

### Freeze record
- Freeze purpose: lock the governing boundary for the next implementation phase without finalizing unresolved comparison decisions
- Freeze scope: comparison-level research boundaries, source-faithful constraints, method roster, and decision-status governance
- Freeze date: 2026-09-05
- CMP-RD IDs: CMP-RD-001 through CMP-RD-012 remain, and CMP-RD-013 is added for OGSA identity; CMP-RD-002-HRS-001 is linked to CMP-RD-002 and CMP-RD-004.
- Method roster: Proposed Method / Proposed NSGA-III; HRS; DPRS; EIMORM; OGSA
- Decision-status statement: CMP-RD-001 through CMP-RD-012, CMP-RD-002-HRS-001, and CMP-RD-013 are DECIDED.
- Numerical-value statement: no numerical values were invented during this freeze
- Source-behavior statement: source-defined algorithm behavior remains protected
- Implementation-governance statement: implementation must not silently resolve research decisions

### Freeze conclusion
This document is now governance-frozen as the decision boundary for the next implementation phase.

The freeze preserves the current research boundary, retains the five-method roster, keeps unrelated decisions OPEN, protects source-faithful method semantics, forbids silent invention of missing values, and blocks implementation from treating unresolved research choices as settled decisions.

---

## 17. Self-Audit Summary

This freeze satisfies the requested governance boundary requirement without introducing implementation or simulation work.

Self-audit checks:
- Only [docs/algorithms/comparison-researcher-decisions.md](docs/algorithms/comparison-researcher-decisions.md) was modified.
- CMP-RD-001 through CMP-RD-012 still exist; CMP-RD-001 records the roster, CMP-RD-002 records the common environment, CMP-RD-002-HRS-001 records the scoped HRS replay decision, and CMP-RD-013 records the OGSA identity decision.
- Their existing statuses were not silently changed.
- The five-method roster remains exactly: Proposed Method / Proposed NSGA-III, HRS, DPRS, EIMORM, OGSA.
- no legacy method alias is introduced as a separate method.
- HSR is not a separate method.
- Proposed remains multi-stage.
- Proposed's five native objectives remain unchanged.
- OGSA native objectives remain unchanged.
- EIMORM has no invented objective vector.
- No baseline received Proposed behavior.
- No common experiment values were invented.
- No run count was invented.
- No statistical protocol was invented.
- No visualization protocol was invented.
- No normalization formula was invented.
- No ranking formula was invented.
- No simulation was executed.
- No implementation was performed.
- No fabricated result was produced.
- The freeze is a governance/boundary freeze, not a claim that all OPEN decisions are numerically resolved.

This final freeze is therefore a governance boundary lock and not an implementation decision.

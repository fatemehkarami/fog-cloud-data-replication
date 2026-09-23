# Common domain model for the comparative replication study

## 1. Purpose

This document defines the conceptual domain model shared by the five replication methods under study:

- Proposed NSGA-III
- HRS
- DPRS
- EIMORM
- OGSA

This document is a specification, not an implementation.

It defines the common simulation domain entities and shared state required by the simulator, while preserving the architectural boundary established in [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md).

This domain model is intentionally limited to common infrastructure and shared runtime concepts. It does not alter any source-defined algorithm behavior, scientific equations, or implementation contract.

The following classification terms are used throughout this document:

- SOURCE-DEFINED
- COMMON-SIMULATOR DESIGN
- RESEARCHER-DEFINED
- UNRESOLVED

This document explicitly states that:

- the domain model is common infrastructure
- source-specific algorithm behavior remains in algorithm-specific contracts
- the common model must not silently impose capabilities on algorithms
- algorithm-specific metadata may exist, but its semantics remain source-specific
- algorithm adapters may read shared state but do not directly mutate authoritative simulation state

The architecture rule remains unchanged:

Algorithm Adapter:
READ common simulation state
→ COMPUTE source-defined decision
→ RETURN decision

Common Simulator:
VALIDATE decision
→ EXECUTE decision
→ MUTATE simulation state
→ RECORD state transition/events/metrics

Algorithm adapters must NEVER directly mutate:

- storage state
- replica catalog
- file catalog
- node health
- network state
- simulation clock
- event queue

---

## 2. Domain model principles

### 2.1 Common state vs algorithm-specific state

The common domain model distinguishes between authoritative common simulation state and algorithm-internal state.

COMMON SIMULATION STATE includes:

- topology
- nodes
- VMs
- files
- replicas
- users
- requests
- network
- health
- storage
- resource utilization
- simulation time
- events

ALGORITHM-INTERNAL STATE includes:

- algorithm-specific caches
- optimization population
- fuzzy intermediate values
- graph structures
- objective values
- reference points
- method-specific statistics
- any other state explicitly required by a source method

This distinction is mandatory.

Algorithm-internal state must not replace or duplicate authoritative simulator state.

Classification:

- COMMON-SIMULATOR DESIGN for the shared runtime state model
- SOURCE-DEFINED for method-specific internal state semantics where explicitly required by a paper
- RESEARCHER-DEFINED when a method-specific internal state must be configured or interpreted outside the source paper
- UNRESOLVED when the source does not specify enough detail to define semantics precisely

### 2.2 Authoritative state ownership

The common simulator is the authoritative owner of runtime state.

Algorithm adapters may READ state but may not mutate it.

The simulator owns and validates all mutations to:

- file catalog
- replica catalog
- node health
- storage accounting
- link status
- request timing state
- queue and scheduling state
- event queue
- simulation clock

Classification:

- COMMON-SIMULATOR DESIGN

### 2.3 Decision objects

Algorithms return decisions rather than directly changing entities.

Conceptually, the common domain model recognizes decision objects such as:

- placement decision
- provider selection decision
- replica creation decision
- replica deletion decision
- replica movement decision
- replica selection decision
- failure handling decision when explicitly defined by a source paper

These are decisions, not direct state mutations.

They are part of the source-defined algorithm behavior and therefore remain outside the implementation of the simulator itself.

Classification:

- SOURCE-DEFINED for actual decision semantics and meaning
- COMMON-SIMULATOR DESIGN for the fact that decisions are returned and validated by the simulator

### 2.4 Validation

The simulator validates decisions before executing them.

Examples of validation include:

- target node/site exists
- target node/site is healthy when required
- sufficient storage is available
- requested replica does not already exist where invalid
- source/provider is valid
- network path is available when required
- deletion does not violate common system validity constraints

This validation is common simulator functionality.

The domain model must not invent algorithm-specific constraints beyond those explicitly defined in source contracts.

Classification:

- COMMON-SIMULATOR DESIGN for validation mechanism
- SOURCE-DEFINED when a paper defines a method-specific validity rule or constraint
- RESEARCHER-DEFINED when the exact policy is chosen experimentally rather than fixed by the source
- UNRESOLVED when a paper leaves the validity condition unspecified

---

## 3. Core domain entities

The following entities are part of the common domain model. Each entity is defined conceptually, not as an implementation class or schema.

For every entity below, the relevant perspective is:

- Purpose
- Identity
- Required state
- Optional state
- Relationships
- Who owns or mutates the state
- Classification
- Important semantic constraints

The common domain model is intentionally generic and must remain subordinate to source-specific algorithm contracts.

### 3. Core domain entities

The common domain model includes the following core entities:

- Experiment
- Scenario
- Site/DataCenter
- DataNode/Host
- VM/Compute Resource
- File
- Replica
- User/Client
- Request
- Task
- Network Link
- Simulation Clock
- Simulation Event
- Metrics Record

These entities represent the shared conceptual model for the comparative simulation study. Detailed definitions and authoritative semantics for each entity are provided in the subsequent sections of this document.

The common domain model is intentionally generic and remains subordinate to source-specific algorithm contracts.

---

## 4. Experiment and scenario model

The common domain model defines the relationship:

Experiment
→ contains multiple Scenarios/Runs
→ executes one algorithm per comparative run
→ produces metrics and aggregated results

A Scenario must conceptually contain:

- topology
- sites/nodes
- VM/resource configuration
- file catalog
- initial file placement
- initial replica state
- network configuration
- workload
- exogenous failure/recovery schedule
- simulation duration
- scenario seed

Classification:

- COMMON-SIMULATOR DESIGN for scenario infrastructure
- RESEARCHER-DEFINED for parameterization choices not fixed by a source paper
- SOURCE-DEFINED when a source paper explicitly fixes an initialization rule or parameter behavior

### Fairness rule

All algorithms in a matched comparison receive the same scenario definition and an independent deep-cloned initial state.

This is a mandatory fairness condition.

Important rule:

- Do not say that algorithms share the same mutable runtime state.
- Each algorithm run starts from an equivalent copy of the same initial scenario.

This ensures that cross-method comparisons are fair while preserving the boundary between common and algorithm-specific behavior.

Classification:

- COMMON-SIMULATOR DESIGN

---

## 5. Site / data center

A Site is a common simulation entity.

Purpose:

- represent a logical hosting location in the distributed environment

Required state:

- site identifier
- topology position or region if applicable
- host/node membership
- local storage capacity
- local storage usage
- health state
- network connectivity
- site-level access statistics

Optional state:

- labels or service markers
- metadata used by a source paper

Relationships:

- contains nodes
- connects to other sites via network links
- stores replicas and file data at the site level

Ownership:

- common simulator owns runtime site state
- algorithms may read it
- algorithms may not mutate it directly

Classification:

- COMMON-SIMULATOR DESIGN

Important semantic constraints:

- site is a common structure, not a method-specific optimization object
- not every algorithm uses every site attribute
- site state should be treated as simulation state unless a source contract explicitly defines otherwise

---

## 6. Data node / host

Purpose:

- represent a host or data node in the simulator

Required state:

- node identifier
- parent site
- health
- storage capacity
- storage usage
- CPU capacity
- memory capacity
- VM membership
- network connectivity
- resource utilization

Important distinction:

- capacity = configured maximum resource amount
- current usage = active consumption during the run
- available/free capacity = remaining resource headroom

These are simulator state values.

Ownership:

- common simulator owns the authoritative node state
- algorithm adapters may read it
- algorithm adapters must not directly mutate it

Classification:

- COMMON-SIMULATOR DESIGN

Important semantic constraints:

- health and reachability are simulator concepts
- exact algorithmic interpretation may vary by source paper, but that interpretation must remain source-specific

---

## 7. VM / compute resource

Purpose:

- represent compute capability associated with a host and a site

Required state:

- VM identifier
- host
- site
- processing capacity
- MIPS or equivalent metric where applicable
- number of processing elements if applicable
- memory capacity/usage
- queue state
- service rate where applicable
- network capability where applicable

Important rule:

Do not assume that every algorithm uses all VM attributes.

For example:

- HRS may use source-defined capability, load, and network-performance aspects
- another method may not use those same attributes at all

Ownership:

- common simulator owns VM runtime state
- algorithm adapters may read it when relevant to a source contract
- algorithm adapters do not directly mutate VM state

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED when a method explicitly defines a specific VM metric or computation semantics
- RESEARCHER-DEFINED when VM parameters are configured by the experimenter
- UNRESOLVED when the source leaves VM semantics under-defined

---

## 8. File model

Purpose:

- represent the logical data object in the system

Required state:

- file identifier
- file size
- creation time
- original/primary location where applicable
- replica membership
- access history
- access statistics
- popularity information where available

Clarification:

- A File is the logical data object.
- A Replica is a physical/logical copy of that File at a specific location.

Do not treat File and Replica as the same entity.

File availability is derived from the current set of valid, healthy, reachable replicas according to the common simulator's operational rules.

Ownership:

- common simulator owns the file catalog
- algorithms may read file state
- algorithms do not directly mutate the file catalog

Classification:

- COMMON-SIMULATOR DESIGN

Important semantic constraints:

- the file catalog is authoritative runtime state
- replica membership is a relationship, not a duplicate file object

---

## 9. Replica model

Purpose:

- represent a copy of a file stored in the environment

Required state:

- replica identifier
- file identifier
- location site
- location node/host where applicable
- creation time
- last access time
- access count
- size
- validity state
- health/reachability state
- storage occupancy contributed by the replica

Optional state:

- algorithm-specific metadata when required by the source contract
- cost metadata where source-defined

Replica existence:
The replica is present in the authoritative replica catalog.

Replica validity:
The replica references an existing file and a valid hosting location and has not been deleted.

Replica operational availability:
The replica's hosting resources are healthy and the required communication path is reachable according to the common simulator's operational rules.

A request may use a replica only when the operational conditions required for serving that request are satisfied.

Ownership:

- common simulator owns the replica catalog and replica lifecycle
- algorithm adapters may compute decisions involving replicas
- algorithm adapters do not directly mutate the replica catalog

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED when a paper defines extra metadata or semantics
- RESEARCHER-DEFINED when a specific operational interpretation is chosen externally
- UNRESOLVED when a source leaves behavior unspecified

Important semantic constraints:

- Do not define deadline semantics here.
- Do not invent additional reliability semantics here.

---

## 10. User / client model

Purpose:

- represent a logical requester generating demand

Required state:

- user identifier
- requesting/home site where applicable
- request generation characteristics
- traffic class where applicable

Optional state:

- behavioral metadata
- communication profile

Relationships:

- creates requests
- may belong to a site or region

Ownership:

- common simulator owns workload-generation and user-context state
- algorithms may read user context only if the source method uses it
- algorithms do not directly mutate user state

Classification:

- COMMON-SIMULATOR DESIGN

Important semantic constraints:

- not every algorithm uses user identity directly
- user semantics belong to workload and request generation, not algorithmic optimization behavior

---

## 11. Request model

Purpose:

- represent access demand submitted to the system

Required state:

- request identifier
- user/client
- source site
- requested file
- submission timestamp
- completion timestamp
- selected replica/provider if applicable
- request status
- success/failure
- response time
- relevant communication information

Optional state:

- task association
- input/output data volume
- local vs remote request context

Relationships:

- belongs to a user or client
- references a file
- may be associated with a task
- leads to request completion and metrics recording

Ownership:

- common simulator owns the authoritative request state and history
- algorithms may compute a decision that influences request handling, but do not directly mutate the request record

Classification:

- COMMON-SIMULATOR DESIGN

Important semantic constraints:

- REQUEST ARRIVAL and REQUEST COMPLETION are distinct events
- request completion cannot occur before request arrival
- success/failure is observed by the simulator based on the actual state transitions and request execution outcome

---

## 12. Task model

Purpose:

- represent computation associated with a request or service invocation when relevant

Required state:

- task identifier where applicable
- associated request if applicable
- workload length or processing requirement where necessary
- source site or node where applicable
- submission time
- completion time
- status

Optional state:

- processing metadata
- queue or scheduling metadata
- cost or resource metadata

Relationships:

- may be associated with a Request
- may be placed on a VM or compute resource

Ownership:

- common simulator owns task scheduling and execution state
- algorithms may read task information only where the source method defines it
- algorithms do not directly mutate task queues or execution state

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED when a paper directly uses task semantics
- UNRESOLVED when task semantics vary across papers and are not explicit

Important semantic constraints:

- task semantics are not forced onto methods that do not define them
- a Request may reference a Task, but not every method uses all task attributes

---

## 13. Network model

Purpose:

- provide common communication capability between sites or nodes

Network Link required state:

- source
- destination
- bandwidth
- latency
- propagation delay where applicable
- availability/status
- failure state if modeled

Additional conceptual values:

- connectivity
- path
- effective bandwidth
- effective latency

But:

- do not invent a routing algorithm
- do not invent a network path-selection algorithm
- do not define additional network equations unless they already exist in an algorithm-specific contract

The common network model provides state.
Algorithms decide how to use source-defined network metrics.

Ownership:

- common simulator owns the network model and link state
- algorithms may read network state for decision-making
- algorithms do not directly mutate network state

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED when a method explicitly defines network metric usage
- RESEARCHER-DEFINED when the experimenter chooses a network configuration outside the source paper
- UNRESOLVED when no formal metric or path definition exists in the source

---

## 14. Health and reachability model

Purpose:

- represent operational status of entities in the common simulation environment

Required operational concepts:

- healthy
- failed
- recovering
- unavailable
- reachable
- unreachable

Clarification:

- health and reachability are simulator state
- the exact algorithmic interpretation of these states remains method-specific where the source defines special behavior
- for common reliability/availability evaluation, use the definitions already established in [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md)

Important constraints:

- Do not introduce a deadline or SLA threshold here.
- Do not invent new operational semantics beyond the architecture's definitions.

Classification:

- COMMON-SIMULATOR DESIGN for the state vocabulary itself
- SOURCE-DEFINED for algorithm-specific interpretation where explicitly defined
- UNRESOLVED when the source paper does not specify the interpretation precisely

---

## 15. Storage model

Purpose:

- represent the capacity and usage of the storage resources in the simulation

Required state:

- total capacity
- used capacity
- free capacity
- replica occupancy
- storage state transitions

Invariant:

used capacity + free capacity = total capacity

where applicable to the chosen storage model.

The simulator is responsible for maintaining storage consistency.

Algorithms only request decisions such as:

- create replica
- delete replica
- move replica

They do not directly modify storage counters.

Ownership:

- common simulator owns storage accounting and capacity state
- algorithms may read storage state
- algorithms may not mutate storage state directly

Classification:

- COMMON-SIMULATOR DESIGN

Important semantic constraints:

- storage model is authoritative runtime state
- direct mutation by adapters is forbidden

---

## 16. Replica validity and system invariants

This section defines common invariants for the simulator.

Examples of common invariants:

- a replica references an existing file
- a replica has exactly one physical/logical hosting location at a given time
- a replica cannot occupy more storage than available capacity
- a deleted replica cannot remain in the active replica catalog
- storage accounting remains consistent after creation/deletion/movement
- a failed node cannot serve requests while unavailable
- no duplicate replica of the same file exists on the same hosting location unless a source explicitly requires such behavior
- a file must retain at least one valid replica if this is a common system constraint

Important rule:

If an invariant is not universally justified by the dissertation or system design, it must be classified as RESEARCHER-DEFINED rather than silently attributed to an algorithm.

Classification:

- COMMON-SIMULATOR DESIGN for core invariants
- RESEARCHER-DEFINED for policy choices not already fixed by the design
- UNRESOLVED when the invariant is not sufficiently specified by the source or design

---

## 17. Event model

Purpose:

- represent scheduled or triggered transitions in the simulation

Conceptual event types:

- RequestArrival
- RequestCompletion
- ReplicaCreation
- ReplicaDeletion
- ReplicaMovement
- NodeFailure
- NodeRecovery
- SimulationEnd

For each event define:

- purpose
- triggering source
- required information
- whether it is exogenous or endogenous
- who is allowed to generate/execute it

Important distinction:

EXOGENOUS EVENTS:
Events generated by the scenario and independent of algorithm decisions.

Examples:

- workload request arrivals
- scheduled failures
- scheduled recoveries

ENDOGENOUS EVENTS:
Events resulting from algorithm decisions.

Examples:

- replica creation
- replica deletion
- replica movement

The same exogenous event schedule must be used for all compared algorithms.
Endogenous events may differ because algorithms make different decisions.

Ownership:

- common simulator owns the event queue and event lifecycle
- algorithms may return decisions that cause the simulator to schedule the appropriate event
- algorithms do not directly schedule arbitrary simulator events

Classification:

- COMMON-SIMULATOR DESIGN

---

## 18. Decision vs state transition

This section defines the critical distinction between decision generation and simulator-side execution.

Algorithm:
"Create replica of File F at Site S using Provider P."

This is a DECISION.

Common Simulator:
- validates S
- validates P
- checks storage
- creates Replica
- updates storage
- updates replica catalog
- records ReplicaCreation event
- updates metrics

This is STATE TRANSITION.

Similarly:

Algorithm:
"Delete Replica R."

Common Simulator:
- validates R
- removes R
- releases storage
- updates replica catalog
- records ReplicaDeletion
- updates metrics

The algorithm never directly performs those mutations.

This separation is mandatory and authoritative.

Classification:

- SOURCE-DEFINED for decision semantics
- COMMON-SIMULATOR DESIGN for execution semantics

---

## 19. Algorithm-specific metadata

The common domain model allows method-specific metadata as long as it remains subordinate to the common authoritative state.

Examples include:

HRS:

- access count
- last access interval
- replication cost
- fuzzy value

Proposed NSGA-III:

- objective values
- normalized objective values
- reference-point association
- population-specific state

DPRS:

- graph-related metadata required by its source method

EIMORM:

- source-defined optimization or replication metadata

OGSA:

- optimization-specific state related to the source method

Important rule:

These are examples only.
Do not invent fields or semantics not already defined in the corresponding algorithm contract.

Algorithm-specific metadata must not become authoritative replacements for common simulator state.

Classification:

- SOURCE-DEFINED for the semantics of metadata in each method
- COMMON-SIMULATOR DESIGN for the fact that the metadata is read and used by the adapter but not authoritative runtime state
- UNRESOLVED when the source contract is incomplete or ambiguous

---

## 20. State ownership matrix

The following conceptual matrix is part of the domain model.

| State / Entity | Common Simulator owns? | Algorithm may read? | Algorithm may mutate directly? | Notes |
| --- | --- | --- | --- | --- |
| simulation clock | Yes | Yes | No | Clock is simulator-owned runtime state |
| event queue | Yes | Yes | No | Event scheduling is simulator-owned |
| node health | Yes | Yes | No | Health state is authoritative simulator state |
| storage capacity | Yes | Yes | No | Capacity is simulator-owned |
| storage usage | Yes | Yes | No | Usage is simulator-owned and reconciled with free space |
| file catalog | Yes | Yes | No | Domain catalog is authoritative |
| replica catalog | Yes | Yes | No | Replica lifecycle is simulator-owned |
| network state | Yes | Yes | No | Links and connectivity are simulator-owned |
| request history | Yes | Yes | No | Requests remain simulator-observed state |
| metrics | Yes | Yes, when required by source-defined logic | No | Metrics are simulator-owned; algorithms may read relevant metric state but cannot modify the metrics store |
| algorithm-internal state | No | Yes | Yes | Owned by the algorithm adapter internally |

Expected principle:

- Common Simulator: YES / YES / NO
- Algorithm-internal state: Algorithm owns / Algorithm may read-write internally

Important constraint:

Do not allow algorithm adapters to mutate common simulator state.

Classification:

- COMMON-SIMULATOR DESIGN

---

## 21. Decision ownership matrix

The following conceptual matrix clarifies responsibility for decisions and execution.

| Decision type | Who computes? | Who validates? | Who executes? |
| --- | --- | --- | --- |
| replica selection | Algorithm adapter if source-defined | Common simulator | Common simulator |
| provider selection | Algorithm adapter if source-defined | Common simulator | Common simulator |
| replica creation | Algorithm adapter returns decision | Common simulator | Common simulator |
| replica deletion | Algorithm adapter returns decision | Common simulator | Common simulator |
| replica movement | Algorithm adapter returns decision if source-defined | Common simulator | Common simulator |
| failure handling decision | Algorithm adapter only if source-defined | Common simulator | Common simulator |

General rule:

Algorithm Adapter → computes
Common Simulator → validates
Common Simulator → executes

Important constraint:

A particular algorithm may not support every decision type.

Classification:

- SOURCE-DEFINED for algorithmic decision computation
- COMMON-SIMULATOR DESIGN for validation and execution responsibility

---

## 22. Relationship model

The conceptual relationship model is as follows:

Experiment
  └── Scenario
       ├── Sites
       │    └── Nodes
       │         └── VMs
       ├── Files
       │    └── Replicas
       ├── Users
       │    └── Requests
       ├── Network Links
       ├── Events
       └── Simulation Clock

Algorithm Adapter
  ├── reads Scenario State
  ├── maintains Algorithm-internal State
  └── returns Decisions

Common Simulator
  ├── validates Decisions
  ├── executes Decisions
  ├── mutates Common State
  └── records Events/Metrics

This model is conceptual only and not an implementation schema.

Classification:

- COMMON-SIMULATOR DESIGN

---

## 23. Domain model invariants

The following are common simulator invariants only.

At minimum, the model includes:

- entity identifiers are unique within their entity type
- file references are valid
- replica references are valid
- storage accounting is consistent
- failed/unreachable resources cannot serve requests
- request completion cannot occur before request arrival
- deleted replicas are not selectable
- state transitions are timestamp ordered
- scenario state is isolated between algorithm runs
- algorithm-generated events cannot modify state without simulator validation

Each invariant is a domain constraint rather than a scientific algorithm rule.

Classification:

- COMMON-SIMULATOR DESIGN for infrastructure invariants
- RESEARCHER-DEFINED when a policy needs to be chosen outside the common model
- UNRESOLVED when the source design does not yet specify the exact condition

---

## 24. Fairness and state isolation

This section is mandatory.

For each matched comparative run:

1. Generate one scenario.
2. Freeze the scenario's initial state.
3. Create an independent deep-cloned initial state for each algorithm.
4. Run each algorithm independently.
5. Do not allow one algorithm's state changes to affect another algorithm.
6. Reuse the same exogenous workload and failure/recovery schedule.
7. Allow endogenous algorithm-generated events to differ.
8. Keep scenario randomness separate from algorithm-local randomness.

This is critical for scientific fairness.

Classification:

- COMMON-SIMULATOR DESIGN

Important rule:

The common simulator must not allow a mutable shared state to be reused across different algorithms in the same comparison set.

---

## 25. Source-faithfulness rule

The common domain model defines only shared simulation concepts.

Whenever a source paper defines:

- a different initialization rule
- a method-specific state variable
- a method-specific constraint
- a method-specific event trigger
- a method-specific decision
- a method-specific metric calculation

that definition remains in the corresponding algorithm-specific contract.

The common domain model must not override or reinterpret it.

If the source is ambiguous, the issue must be marked UNRESOLVED and resolved explicitly in the relevant implementation contract.

Classification:

- SOURCE-DEFINED for source-specific semantics
- COMMON-SIMULATOR DESIGN for the shared infrastructure boundary
- UNRESOLVED when a source definition is incomplete or ambiguous

---

## 26. Comparative experiment vs source-reproduction experiment

### Comparative experiment

Purpose:

- Compare all five algorithms under one controlled common scenario.

Requirements:

- same scenario definition
- same initial state
- same exogenous workload
- same exogenous failures/recoveries
- independent runtime state per algorithm
- same common evaluation metrics

### Source-reproduction experiment

Purpose:

- Validate an individual algorithm against the configuration or behavior described in its source paper.

Requirements:

- source-defined initialization and parameters may be used
- source-specific assumptions may differ from the common comparative scenario
- this experiment is not directly used as the primary fairness comparison unless the same controlled conditions are maintained

This distinction is important because source papers may use different simulation configurations.

Classification:

- COMMON-SIMULATOR DESIGN for the experiment categories
- SOURCE-DEFINED for the source-specific setup used by a given method
- RESEARCHER-DEFINED when the study team selects experimental conditions beyond a direct paper reproduction

---

## 27. Unresolved items

The following items remain unresolved until specified elsewhere and must not be guessed or silently resolved:

- exact topology parameterization
- exact failure semantics beyond the common state model
- exact reachability semantics beyond the common state model
- deadline/SLA semantics
- source-specific metadata not yet formally specified
- any algorithm-specific state whose definition is incomplete in the source contract

These items must remain explicitly marked as UNRESOLVED or RESEARCHER-DEFINED rather than being treated as common facts.

Classification:

- UNRESOLVED for missing scientific or source-specific details
- RESEARCHER-DEFINED when the study team chooses parameters or policies outside the source contracts

---

## 28. Implementation boundary

This document defines the conceptual domain model only.

It does not:

- implement C#
- define interfaces
- define classes
- define database schemas
- implement algorithms
- define source-specific equations
- introduce hidden optimization
- decide unresolved scientific questions

The next implementation specification must translate this domain model into a technical design only after the domain model is reviewed and frozen.

This statement is a required architectural boundary and must be preserved.

Classification:

- COMMON-SIMULATOR DESIGN for the boundary itself
- UNRESOLVED for any scientific questions not yet closed by source contracts or research design

---

## Final validation

This document is consistent with [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md) and keeps the following constraints intact:

- [ ] Scenario Definition is immutable during a run.
- [ ] Runtime State is mutable only by the common simulator.
- [ ] Each algorithm receives an independent runtime-state copy.
- [ ] Exogenous events are identical across matched runs.
- [ ] Endogenous algorithm-generated events may differ.
- [ ] Scenario randomness is separated from algorithm randomness.
- [ ] Algorithm adapters generate decisions but do not mutate authoritative state.
- [ ] The simulator validates and executes decisions.
- [ ] File availability is derived from replica state.
- [ ] Replica existence, validity, and operational availability are distinguished.
- [ ] At-least-one-replica preservation is not silently imposed as a universal algorithm rule.
- [ ] Metrics are observed/calculated by the common simulator.
- [ ] Algorithm-internal objective values are distinct from common evaluation metrics.
- [ ] Reliability and availability remain distinct.
- [ ] Deadline/SLA semantics remain UNRESOLVED.
- [ ] Failure response is algorithm-specific even though failure injection is common infrastructure.
- [ ] Source-specific behavior remains in algorithm-specific contracts.
- [ ] No scientific equations or algorithm behavior were invented or changed.

This document therefore serves as the common conceptual domain model for the five-method simulation study without altering any source-specific algorithm behavior.

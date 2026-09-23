# Common simulation architecture for the comparative replication study

## 1. Purpose and scope

This document defines the common simulation architecture that supports the comparative evaluation of five replication methods under the same simulation environment and identical experimental conditions:

- Proposed NSGA-III method
- HRS
- DPRS
- EIMORM
- OGSA

This is a software/research architecture specification only. It does not implement any C# code, does not define or modify algorithm-specific scientific equations, and does not add hidden optimization behavior to any method.

The architecture is designed to separate:

- A. Common simulation environment
- B. Algorithm-specific decision logic
- C. Workload/request generation
- D. Network model
- E. Data/file/replica model
- F. Node/VM/resource model
- G. Failure/recovery model
- H. Event scheduling
- I. Metrics collection
- J. Experiment configuration
- K. Random seed management
- L. Result aggregation/export

All items are labeled according to their origin:

- SOURCE-DEFINED
- COMMON-SIMULATOR DESIGN
- RESEARCHER-DEFINED
- UNRESOLVED

The architecture deliberately enforces a strict rule:

- the common simulator may provide capabilities and state, but it must not silently grant an algorithm behavior that the source method does not define.

Examples:

- HRS must not be given NSGA-III optimization solely because the simulator supports multi-objective search.
- A placement-only baseline must not be assigned dynamic replica-count optimization unless the source paper explicitly defines it.
- A method without a failure-recovery mechanism must not be given one merely because the simulator can simulate failures.

---

## 2. Architectural principles

### 2.1 Single shared environment

All five methods must be tested inside a single common environment with the same:

- topology
- node capacities
- initial file placement
- initial replica state
- workload generation
- request sequence and timestamps
- file sizes
- user/request distribution
- network conditions
- failure and recovery schedule
- simulation time horizon
- random seeds

This is a COMMON-SIMULATOR DESIGN requirement.

### 2.2 Algorithm adapter boundary

The architecture uses a common algorithm abstraction layer. Each method receives the same simulation state relevant to that method and returns method-specific decisions only within the bounds of its source paper.

This means:

- the simulator is common
- the decision logic is algorithm-specific
- the algorithm interface is capability-aware, not universal

### 2.3 Source-faithful separation

The simulator must expose state and events, but the algorithm decides whether to consume them.

This is a required boundary:

- common simulator: scenario management, topology, resources, scheduling, metrics
- algorithm adapter: placement decision, provider selection, replacement decision, failure handling if supported by source

### 2.4 Explicit decision-generation vs. state-mutation boundary

The architecture must explicitly separate algorithm decision generation from common simulator state mutation.

Required architectural rule:

- Algorithm adapters READ the common simulation state.
- Algorithm adapters COMPUTE source-defined decisions.
- Algorithm adapters RETURN decisions.
- Algorithm adapters MUST NOT directly mutate:
  - storage state
  - replica catalog
  - file catalog
  - node health
  - network state
  - simulation clock
  - event queue

The common simulator is the only component authorized to execute accepted algorithm decisions and perform physical/state transitions.

This separation is required even when an algorithm logically appears to "make a change". The algorithm's role is to decide, not to mutate the runtime world directly.

Conceptual flow:

Request/Event
    ↓
Common Simulator
    ↓
Algorithm Adapter
    ↓
Source-defined Decision
    ↓
Common Simulator validates/executes decision
    ↓
State Mutation
    ↓
Metrics/Event Recording

This is a COMMON-SIMULATOR DESIGN rule.

#### 2.4.1 Examples of the required separation

HRS:

- HRS computes PlacementDecision, ProviderSelectionDecision, and ReplacementDecision.
- The common simulator performs ReplicaCreation and ReplicaDeletion.
- The adapter does not directly modify storage or the replica catalog.

DPRS:

- DPRS computes its source-defined placement decision.
- The common simulator performs the resulting state transition.
- The adapter does not directly mutate the file or replica catalog.

EIMORM:

- EIMORM computes its source-defined replication, placement, and replacement decisions only where explicitly defined.
- The common simulator performs the state transition.
- The adapter does not directly alter node health or storage state.

OGSA:

- OGSA computes its source-defined optimization or placement decision.
- The common simulator performs the resulting state transition.
- The adapter does not directly schedule arbitrary simulator actions.

Proposed NSGA-III:

- The proposed method computes its source-defined selection, replica-count, placement, and replacement decisions according to its own implementation contract.
- The common simulator performs the resulting state transitions.
- The adapter does not directly mutate the simulation clock, event queue, or physical topology.

### 2.5 No implicit scientific invention

The architecture must not infer behaviors missing from the source papers.

Examples of forbidden silent extension:

- adding dynamic replica-count optimization to a method that never defines it
- adding failure recovery to a method that does not define it
- adding reliability objectives to a method that never used them
- converting an algorithm into another optimization family simply because the simulator supports it

---

## 3. System decomposition

### A. Common simulation environment

This layer contains the shared runtime and experimental infrastructure required by all algorithms.

Responsibilities:

- scenario definition and setup
- simulation time management
- global event scheduler
- global topology and network state
- node, VM, file, and replica catalog
- fairness enforcement across algorithms
- metric collection and aggregation
- seed management and reproducibility
- result export

Classification:

- COMMON-SIMULATOR DESIGN

### B. Algorithm-specific decision logic

This layer contains only the source-defined logic used by each algorithm.

Responsibilities:

- placement decision
- provider selection
- replacement decision
- failure handling only when supported by the source method
- algorithm-local state updates

Classification:

- SOURCE-DEFINED for each method
- COMMON-SIMULATOR DESIGN for the adapter boundary itself

### C. Workload/request generation

This layer generates the tasks and requests used by all methods under identical conditions.

Responsibilities:

- request arrival generation
- request type generation
- requested file distribution
- user/site distribution
- time stamping and sequence control
- request batching or stream generation

Classification:

- COMMON-SIMULATOR DESIGN for generation infrastructure
- SOURCE-DEFINED if a paper explicitly specifies special workloads or distributions
- RESEARCHER-DEFINED for choosing the workload configuration within the experiment design

### D. Network model

This layer models communication among sites/nodes and the transmission costs used by algorithms.

Responsibilities:

- inter-node link bandwidth
- link latency
- link availability and failure state
- propagation delay contribution
- hop/path cost when relevant
- network state for selection and placement decisions

Classification:

- COMMON-SIMULATOR DESIGN for the model container
- SOURCE-DEFINED when the algorithm explicitly defines the network metric it uses
- RESEARCHER-DEFINED for parameter setting
- UNRESOLVED if a source paper provides insufficient formal detail

### E. Data/file/replica model

This layer tracks file metadata and replica state across nodes.

Responsibilities:

- file catalog and size
- file ownership and creation provenance
- replica list and locations
- replica metadata such as access level and age
- deletion and movement events
- storage occupancy per file/replica

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED when a method uses additional metadata or dynamic state in its own rule set

### F. Node/VM/resource model

This layer maintains resource capacities and live utilization.

Responsibilities:

- site/node state
- host count and capacity
- VM count and capacity
- CPU, memory, and storage state
- load state of compute resources
- health status and reachability
- scheduling point for task execution queues

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED when the source paper defines specific resource equations or constraints

### G. Failure/recovery model

This layer models failures and recovery events as part of the shared simulation environment.

Responsibilities:

- node failure events
- recovery events
- connectivity disruption
- failure schedule and recovery schedule
- health state propagation to algorithms

Classification:

- COMMON-SIMULATOR DESIGN for the infrastructure
- SOURCE-DEFINED when a paper explicitly defines a failure-aware mechanism
- RESEARCHER-DEFINED for failure schedule generation
- UNRESOLVED when the source does not provide the failure semantics needed by an algorithm

### H. Event scheduling

This layer owns simulation-time progression and event ordering.

Responsibilities:

- event queue management
- deterministic ordering
- timestamp semantics
- event dispatch to algorithms
- state mutation tracking

Classification:

- COMMON-SIMULATOR DESIGN

### I. Metrics collection

This layer records raw values during simulation and computes final metrics.

Responsibilities:

- request-level timing
- replica-level state changes
- site-level utilization
- algorithm execution accounting
- metric aggregation across runs

Classification:

- COMMON-SIMULATOR DESIGN for collection infrastructure
- SOURCE-DEFINED for formulas that appear in a paper
- UNRESOLVED if no formal metric equation exists in the source
- RESEARCHER-DEFINED for derived reporting views

### J. Experiment configuration

This layer defines each experiment scenario and run configuration.

Responsibilities:

- scenario metadata
- algorithm selection
- seeds
- run count
- duration and stopping criteria
- parameter values used per simulation run
- fairness configuration checks

Classification:

- COMMON-SIMULATOR DESIGN for the experiment runner
- RESEARCHER-DEFINED for parameter choices
- SOURCE-DEFINED when a specific paper fixes a parameter or initialization rule

### K. Random seed management

This layer guarantees reproducible scenario generation and algorithm execution.

Responsibilities:

- master experiment seed
- per-run seed
- scenario generation seed
- algorithm randomness seed
- deterministic regeneration of identical scenarios

Classification:

- COMMON-SIMULATOR DESIGN
- RESEARCHER-DEFINED for how seeds are assigned per run

### L. Result aggregation/export

This layer gathers metrics from repeated runs and produces summary results.

Responsibilities:

- per-run metric values
- aggregated mean/variance/min/max summaries
- output files and data tables
- matched-seed comparison across algorithms

Classification:

- COMMON-SIMULATOR DESIGN

---

## 4. Simulation entities

### 4.1 DataCenter/Site

Concept:

- A logical site or data center participating in the distributed system.

Required attributes:

- site identifier
- parent topology region or cluster if applicable
- list of hosts/data nodes
- local storage capacity
- local storage usage
- health status
- network connectivity state
- site-level access statistics

Classification:

- COMMON-SIMULATOR DESIGN

### 4.2 DataNode/Host

Concept:

- A physical hosting resource within a site.

Required attributes:

- node identifier
- parent site
- health status
- storage capacity
- storage usage
- CPU capacity
- memory capacity
- VM list
- network links
- load state

Classification:

- COMMON-SIMULATOR DESIGN

### 4.3 VM/Compute resource

Concept:

- A compute unit associated with a host and a site.

Required attributes:

- VM identifier
- host identifier
- site identifier
- available processing capacity
- MIPS or equivalent processing metric if used by a method
- memory state
- queue length or pending tasks
- service rate if used by a method
- network capability exposure for provider selection

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED when a method explicitly defines a specific VM metric formula or interpretation

### 4.4 File

Concept:

- A logical data object in the simulation.

Required attributes:

- file identifier
- size
- creation time
- owner or original site if applicable
- replica locations
- access history
- popularity statistics
- current availability state

Classification:

- COMMON-SIMULATOR DESIGN

### 4.5 Replica

Concept:

- A file copy stored at a site or node.

Required attributes:

- replica identifier
- file identifier
- location site/node
- creation time
- last access time
- access count
- size
- storage cost metadata if used by a method
- current validity/health status

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED when a paper defines additional replica valuation or cost semantics

### 4.6 User/Client

Concept:

- A logical requester generating access demand.

Required attributes:

- user identifier
- home site if defined
- request generation profile
- traffic class if used

Classification:

- COMMON-SIMULATOR DESIGN

### 4.7 Request/Task

Concept:

- A unit of workload submitted to the system.

Required attributes:

- request identifier
- task identifier if applicable
- requesting user or source site
- requested file identifier
- submission timestamp
- completion timestamp
- outcome status
- local access success/failure
- chosen provider or replica selection result

Classification:

- COMMON-SIMULATOR DESIGN

### 4.8 Network link

Concept:

- Communication link between two sites or nodes.

Required attributes:

- source site/node
- destination site/node
- bandwidth
- latency
- status
- failure/recovery state if modeled

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED when a paper defines a network metric or specific tuning formula

### 4.9 Simulation clock

Concept:

- Global time used to order events and compute request timing metrics.

Required attributes:

- current time
- event ordering
- duration horizon
- time unit semantics

Classification:

- COMMON-SIMULATOR DESIGN

---

## 5. Common state model

The simulator maintains shared state used by every method, with algorithm-specific use determined by the adapter.

### 5.1 Node health/status

Required state:

- healthy
- failed
- recovering
- unavailable
- reachable

Classification:

- COMMON-SIMULATOR DESIGN

### 5.2 Storage capacity and usage

Required state:

- total storage capacity per node/site
- used storage
- free storage
- replica occupancy at each site

Classification:

- COMMON-SIMULATOR DESIGN

### 5.3 CPU/load state

Required state:

- current CPU usage or queue length
- service rate if required by a method
- resource utilization

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED when a paper defines a load formula directly used by its method

### 5.4 Memory state

Required state:

- memory usage
- memory capacity
- memory pressure indicator if the simulator uses it

Classification:

- COMMON-SIMULATOR DESIGN

### 5.5 Bandwidth and latency

Required state:

- per-link bandwidth
- per-link latency
- available bandwidth at a time step if dynamic
- propagation delay contribution

Classification:

- COMMON-SIMULATOR DESIGN

### 5.6 File catalog

Required state:

- known files
- file metadata
- file size
- original references
- access counts

Classification:

- COMMON-SIMULATOR DESIGN

### 5.7 Replica locations

Required state:

- replica membership by file
- replica location map
- replica counts per file

Classification:

- COMMON-SIMULATOR DESIGN

### 5.8 Request history

Required state:

- historical request timestamps
- request outcomes
- request source site
- requested file identity
- latency and success/failure results

Classification:

- COMMON-SIMULATOR DESIGN

### 5.9 Access statistics

Required state:

- file access count
- replica access count
- site access counts
- user access counts
- cumulative statistics for metrics

Classification:

- COMMON-SIMULATOR DESIGN

---

## 6. Common events

The event system is a shared mechanism for all algorithms. Algorithm-specific methods decide whether they respond to an event.

### 6.1 RequestArrival

Meaning:

- a user request reaches the simulation.

Required payload:

- request identifier
- timestamp
- requesting site/user
- requested file
- request origin information

Classification:

- COMMON-SIMULATOR DESIGN

### 6.2 RequestCompletion

Meaning:

- a request finishes successfully or unsuccessfully.

Required payload:

- request identifier
- final status
- completion time
- service time
- response time

Classification:

- COMMON-SIMULATOR DESIGN

### 6.3 ReplicaCreation

Meaning:

- a new replica is created.

Required payload:

- file identifier
- replica identifier
- target site/node
- source/provider if relevant
- timestamp
- storage occupied

Classification:

- COMMON-SIMULATOR DESIGN

### 6.4 ReplicaDeletion

Meaning:

- a replica is deleted.

Required payload:

- file identifier
- replica identifier
- source site/node
- timestamp
- space released

Classification:

- COMMON-SIMULATOR DESIGN

### 6.5 ReplicaMovement (if required by an algorithm)

Meaning:

- an algorithm chooses to relocate a replica.

Required payload:

- file identifier
- replica identifier
- previous site/node
- target site/node
- timestamp

Classification:

- COMMON-SIMULATOR DESIGN as a generic event type
- SOURCE-DEFINED when the algorithm explicitly defines movement behavior
- RESEARCHER-DEFINED if used by an implementation design

### 6.6 NodeFailure

Meaning:

- a node or site becomes unavailable.

Required payload:

- affected node/site
- timestamp
- impact scope
- health transition

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED if a specific algorithm has special logic tied to failures

### 6.7 NodeRecovery

Meaning:

- a failed node or site returns to health.

Required payload:

- affected node/site
- timestamp
- health transition

Classification:

- COMMON-SIMULATOR DESIGN
- SOURCE-DEFINED if a specific algorithm uses it directly

### 6.8 SimulationEnd

Meaning:

- the experiment run ends.

Required payload:

- end timestamp
- final metric snapshot
- termination status

Classification:

- COMMON-SIMULATOR DESIGN

### 6.9 Event-use policy

The simulator must allow events to exist as common event types but must not require every algorithm to consume every event.

Therefore:

- event types are generic
- event handling is capability-specific
- algorithm-specific behavior determines whether and how an event is used
- algorithm adapters must not directly schedule arbitrary simulator events
- an adapter may return a decision that causes the common simulator to schedule the appropriate event

This is a required architectural rule.

---

## 7. Algorithm abstraction

The architecture uses a capability-aware conceptual adapter contract. This is not an implementation requirement in C#, but a specification contract for the simulator design.

### 7.1 Mandatory common simulator operations

The common simulator must provide these operations regardless of algorithm:

- initialize scenario state
- advance simulation clock
- schedule events
- deliver events to the active algorithm adapter
- maintain global state and resource accounting
- collect metrics
- finalize the run

Classification:

- COMMON-SIMULATOR DESIGN

### 7.2 Optional algorithm capabilities

Each algorithm may support a subset of the following capabilities:

- Initialize(...)
- HandleRequest(...)
- SelectReplica(...)
- DecideReplication(...)
- DecideReplacement(...)
- HandleFailure(...) only if the source paper defines failure logic
- Finalize(...)

Classification:

- COMMON-SIMULATOR DESIGN for the conceptual interface shape
- SOURCE-DEFINED for actual capability support
- UNRESOLVED for any capability not formally defined in the paper

### 7.3 Capability contract rules

The simulator must not require a method to implement operations that are not defined by its source paper.

Required rule:

- if a source method does not define a replacement mechanism, the adapter must not force replacement behavior
- if a source method does not define explicit failure recovery, the adapter must not inject it
- if a source method does not define dynamic replica count optimization, the simulator must not provide it automatically
- algorithm adapters must read the common state and compute only source-defined decisions
- algorithm adapters must return decisions, not directly mutate the simulation state or schedule arbitrary simulator events

### 7.4 Conceptual adapter contract

The following is the specification-level contract, not an implementation outline:

- Initialize(...)
  - initialize algorithm-specific state from common simulator state
- HandleRequest(...)
  - read the current request and simulator state and compute the method's source-defined response
  HandleRequest does not imply that every algorithm performs replication, replacement, or replica selection for every request.

The adapter must invoke only the source-defined operations that are applicable to the algorithm and the current event.
- SelectReplica(...)
  - read candidate replica/provider state and return a source-defined replica or provider decision
- DecideReplication(...)
  - read storage and file state and return a source-defined replication decision if the source method defines it
- DecideReplacement(...)
  - read storage pressure and candidate replicas and return a source-defined replacement or deletion decision if the source method defines it
- HandleFailure(...)
  - optional; only for algorithms that explicitly support failure-aware behavior
- Finalize(...)
  - flush any method-specific statistics or state at run end

The adapter may read the global simulation state, compute a decision, and return it. The common simulator alone is responsible for validating the decision and performing the resulting state mutation, event generation, and metrics recording.

This contract must be interpreted as capability-based and source-faithful.

---

## 8. Experimental fairness

The same simulation environment and scenario must be used across all algorithms.

### 8.1 Mandatory fairness conditions

All algorithms must use identical:

- topology
- node capacities
- initial file placement
- initial replica state
- workload
- request sequence
- request timestamps
- file sizes
- user/request distribution
- network conditions
- failure schedule
- recovery schedule
- simulation duration
- random seeds

Classification:

- COMMON-SIMULATOR DESIGN

### 8.2 Source-defined initialization policy

If a source paper requires a specific initialization or parameter behavior, that must be treated as:

- SOURCE-DEFINED

It must not be silently replaced by a common default.

### 8.3 Fairness enforcement

The common simulator must enforce fairness by:

- single scenario generation for all algorithms
- same deep-cloned initial state snapshot for each algorithm run
- same exogenous workload and failure/recovery event schedule
- same result-collection instrumentation across methods
- separated scenario randomness and algorithm-local randomness

Algorithm-generated endogenous events, such as replica creation, deletion, or movement, may differ between algorithms as a consequence of their decisions.

---

## 9. Metrics layer

The simulator must provide a common metrics layer that can collect both algorithm-specific and evaluation-only metrics.

### 9.1 Core metric categories

The following metrics must be supported by the common metrics layer:

- Average Response Time
- Energy Consumption
- Data-node Load
- Total Cost
- Closeness Centrality
- Availability
- Reliability
- Replica Count
- Successful Requests
- Failed Requests
- Algorithm Execution Time

Classification:

- COMMON-SIMULATOR DESIGN for collection capability
- SOURCE-DEFINED when the metric is directly defined in a source paper
- UNRESOLVED when the source does not provide a formal equation or definition

### 9.2 Metric type separation

The architecture must distinguish between:

- metrics optimized by an algorithm
- metrics used only for evaluation

Important rule:

- the simulator must not assume that a metric is optimized merely because it is reported.

The common metrics interface must therefore separate:

- algorithm objective metrics
- evaluation metrics
- derived metrics

### 9.3 Availability and reliability definitions used by this specification

Availability:

- fraction of simulation time during which data can be accessed through at least one valid, healthy and reachable replica.

Reliability:

- successful data access requests / total data access requests

Classification:

- COMMON-SIMULATOR DESIGN for the general metric definition
- RESEARCHER-DEFINED for the exact operational interpretation of a healthy and reachable replica in the chosen topology
- UNRESOLVED for any tighter SLA or deadline semantics not explicitly supported by the dissertation or source papers

### 9.4 Deadline/SLA semantics

The architecture must not define a deadline or SLA metric unless it is explicitly supported by the dissertation or source specification.

Therefore:

- deadline-based availability or reliability semantics are marked as RESEARCHER-DECISION-REQUIRED
- any quality-of-service deadline policy not explicitly grounded in the source is UNRESOLVED

---

## 10. Reproducibility and randomization

### 10.1 Required reproducibility controls

The architecture must define:

- master experiment seed
- per-run seed
- scenario generation seed
- algorithm-local randomness seed
- deterministic scenario generation
- matched-seed comparison across algorithms

Classification:

- COMMON-SIMULATOR DESIGN

### 10.2 Reproducibility rule

The same generated scenario must be reusable by all algorithms.

This means:

- one scenario definition
- same initial conditions
- same exogenous workload and failure/recovery event schedule
- same scenario seed and scenario-generated data
- separated algorithm-local random streams

Algorithm-generated endogenous events may differ across algorithms because they result from algorithm-specific decisions.

### 10.3 Separation of randomness

The architecture must separate:

- scenario randomness
- algorithm randomness

The simulation must be able to regenerate identical scenario data even if algorithm randomization differs.

---

## 11. Experiment structure

The architecture must support the following experiment structure:

- scenario
- algorithm
- seed
- run
- metrics
- aggregated results

### 11.1 Scenario

A scenario is a fully defined simulation instance including:

- topology
- workloads
- failure model
- recovery model
- file catalog and initial replica placement
- network conditions
- simulation duration

Classification:

- COMMON-SIMULATOR DESIGN

### 11.2 Algorithm

An algorithm is a method adapter bound to a source paper definition.

Classification:

- SOURCE-DEFINED for the method behavior
- COMMON-SIMULATOR DESIGN for the adapter interface

### 11.3 Seed and run

Each experiment must provide:

- base experiment seed
- per-run seed assignment
- reproducible random stream generation
- matched-seed run comparison across algorithms

Classification:

- COMMON-SIMULATOR DESIGN

### 11.4 Metrics and aggregated results

The run outputs must support:

- per-run metrics
- cross-run aggregation
- summary tables for comparison
- matched-seed statistical comparison

Classification:

- COMMON-SIMULATOR DESIGN

---

## 12. Research boundaries and classification

Every item in the architecture must be explicitly classified as one of the following:

- SOURCE-DEFINED
- COMMON-SIMULATOR DESIGN
- RESEARCHER-DEFINED
- UNRESOLVED

Examples:

- HRS placement/selection/replacement logic is SOURCE-DEFINED for HRS
- the common event queue is COMMON-SIMULATOR DESIGN
- the chosen workload distribution is RESEARCHER-DEFINED if not fixed by a source paper
- fuzzy membership function parameters for HRS remain UNRESOLVED because the source paper does not provide them exactly

The architecture must never silently convert an UNRESOLVED item into a definite algorithmic mechanism.

---

## 13. Constraint: no silent capability injection

The common simulator must not add capabilities to algorithms that the source papers do not define.

Examples:

- HRS must not automatically get NSGA-III optimization.
- DPRS must not automatically get replacement if the source paper does not define replacement semantics in the same way.
- OGSA must not automatically get adaptive failure-recovery logic unless explicitly defined.
- The simulator may expose events and state, but the algorithm-specific adapter decides whether to use them.

This is a mandatory architecture rule.

---

## 14. Text-based architecture diagram

The following ASCII diagram describes the separation of concerns:

+---------------------------------------------------------------------+
| Common Simulation Environment                                        |
|                                                                     |
|  - Scenario config                                                   |
|  - Simulation clock                                                  |
|  - Event scheduler                                                   |
|  - Global topology                                                   |
|  - Node/VM/File/Replica catalog                                      |
|  - Network model                                                     |
|  - Failure/recovery model                                            |
|  - Metrics collection                                                 |
|  - Seed management                                                    |
|  - Result aggregation                                                 |
+--------------------------------------+------------------------------+
                                       |
                                       v
        +--------------------------+--------------------------+
        | Algorithm Adapter Layer                              |
        |                                                    |
        |  Algorithm A: method-specific state                 |
        |  Algorithm B: method-specific state                 |
        |  Algorithm C: method-specific state                 |
        |  Algorithm D: method-specific state                 |
        |  Algorithm E: method-specific state                 |
        +--------------------------+--------------------------+
                                       |
                                       v
        +--------------------------+--------------------------+
        | Source-defined algorithm logic                      |
        |                                                    |
        | - Placement decision                                |
        | - Provider selection                                |
        | - Replacement decision                              |
        | - Failure handling only if supported                |
        | - Finalization                                      |
        +------------------------------------------------------+

---

## 15. Entity relationship overview

The common simulation state can be described conceptually as:

- DataCenter/Site contains many DataNode/Host entities
- DataNode/Host contains many VM entities
- File has many Replica entities
- Replica is associated with a Site and/or Node
- User produces Request/Task events
- Request/Task references a requested File
- Network link connects Site/Node pairs
- SimulationClock drives all events
- Metrics layer records effects from requests, replicas, nodes, and timing
- ExperimentConfig binds scenario, seed, algorithm, and run settings

This relationship model is a COMMON-SIMULATOR DESIGN view.

---

## 16. Event lifecycle

Conceptual event flow:

1. Scenario initialization

2. Generate workload requests

3. Deliver RequestArrival to the active algorithm adapter

4. Algorithm adapter reads the relevant common simulation state

5. Algorithm adapter computes and returns a source-defined decision, if applicable

6. Common simulator validates the returned decision

7. Common simulator executes the accepted decision and performs the required state mutation

8. Trigger and process the corresponding ReplicaCreation, ReplicaDeletion, or ReplicaMovement event if applicable

9. If a failure event is relevant and the algorithm explicitly supports failure-aware behavior, invoke the corresponding algorithm capability

10. Record metrics and request completion status

11. Schedule the next exogenous or simulator-generated event until the end of the run

12. Finalize and aggregate metrics

This event lifecycle is COMMON-SIMULATOR DESIGN.

---

## 17. Algorithm adapter contract

Conceptual contract:

- Initialize(...)
- HandleRequest(...)
- SelectReplica(...)
- DecideReplication(...)
- DecideReplacement(...)
- HandleFailure(...) only when supported by source method
- Finalize(...)

Constraints:

- not all algorithms implement all methods
- the simulator must not force unsupported operations
- the adapter must be capability-aware and method-aware
- the adapter is the boundary between generic simulation state and source-specific decision logic

Classification:

- COMMON-SIMULATOR DESIGN for the adapter abstraction
- SOURCE-DEFINED for each algorithm's actual capability support
- UNRESOLVED if a source does not define the behavior formally

---

## 18. Metric collection boundary

The common metrics layer must record values at the simulation level while keeping method semantics separate.

Required collection boundary:

- raw request and event traces
- resource and topology state snapshots
- replica state transitions
- site and node utilization
- failures and recoveries
- per-run metrics
- aggregated metrics

The metrics system must not decide that a method optimizes a metric without source support.

This means:

- optimized metric classification is algorithm-specific and source-based
- evaluation metrics are simulator-level and cross-method

---

## 19. Reproducibility rules

The architecture must enforce the following:

1. one master experiment seed drives scenario generation
2. each run receives a deterministic per-run seed
3. the same scenario instance is reused across all algorithms
4. scenario randomness and algorithm randomness are separated
5. matched-seed comparison is supported for all methods
6. results must be exportable in a reproducible format

Classification:

- COMMON-SIMULATOR DESIGN

---

## 20. Open research decisions

These items are not yet fixed as scientific rules and therefore require explicit researcher decision.

- exact topology parameterization beyond the common environment requirements
- exact workload characteristics if broader than the common generation design permits
- exact interpretation of healthy and reachable replica in availability calculations
- exact deadline/SLA semantics if introduced
- exact scenario-specific parameter choices for each study configuration
- any additional aggregator or reporting format beyond the common metrics layer

Classification:

- RESEARCHER-DEFINED or UNRESOLVED depending on the absence of source support

---

## 21. Implementation order

This architecture can be implemented in the following order without changing the scientific behavior of any algorithm:

1. Common simulation core
   - clock
   - event scheduler
   - experiment runner
   - seed management
2. Shared environment model
   - site
   - node
   - VM
   - file
   - replica
   - network link
3. Workload generation and fairness setup
4. Metrics collection infrastructure
5. Algorithm adapter shells for each method
6. Scenario generation and matched-seed runs
7. Aggregation and export

Classification:

- COMMON-SIMULATOR DESIGN for ordering
- SOURCE-DEFINED for each algorithm's adapters only when explicit

---

## 22. Summary

This architecture makes the common simulation environment explicit and separates it from source-defined algorithm logic. It supports a fair, matched-seed, same-environment comparison of the five methods while preserving scientific fidelity.

The key rule is simple:

- the simulator provides the common infrastructure
- the algorithm adapter decides what the source method chooses to use
- no algorithm silently receives capabilities not present in its paper

This document is a specification only and does not implement any C# code.

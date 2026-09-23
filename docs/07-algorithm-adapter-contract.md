# Algorithm adapter contract

## 1. Purpose

This document defines the integration contract between the common simulation environment and source-defined algorithm logic.

It is a specification document only. It does not implement any algorithm, does not define source-specific scientific behavior, and does not create C# or other executable code.

This document is designed to be compatible with:

- [docs/05-common-simulation-architecture.md](docs/05-common-simulation-architecture.md)
- [docs/06-common-domain-model.md](docs/06-common-domain-model.md)

The purpose of the adapter contract is to preserve the architectural separation:

Common Simulation Environment
→ Algorithm Adapter
→ Source-defined algorithm logic
→ Decision returned to simulator
→ Common Simulator validation/execution

The architecture is intentionally common, while the scientific behavior remains algorithm-specific.

Classification:

- COMMON-SIMULATOR DESIGN for the adapter boundary and validation pipeline
- SOURCE-DEFINED for algorithm decision semantics
- UNRESOLVED when a source paper does not provide conclusive behavior

---

## 2. Core architectural rule

The adapter follows the strict pattern:

READ → COMPUTE → RETURN

The common simulator follows:

VALIDATE → EXECUTE → MUTATE → RECORD

This is mandatory.

Algorithm adapters MUST NOT directly mutate authoritative common simulation state.

They must not directly modify:

- storage usage or capacity
- replica catalog
- file catalog
- node health
- network state
- request state
- task queues
- simulation clock
- event queue
- common metrics store

The algorithm adapter may maintain and modify algorithm-internal state, including:

- optimization populations
- fuzzy intermediate values
- graph structures
- caches
- method-specific statistics
- internal objective values
- other source-defined runtime state

This state is not common simulation state and is not part of the simulator's authoritative model.

Classification:

- COMMON-SIMULATOR DESIGN

---

## 3. Capability awareness and source fidelity

The system must remain capability-aware.

The five methods under comparison are:

1. Proposed NSGA-III
2. HRS
3. DPRS
4. EIMORM
5. OGSA

The adapter contract must not assume that all five methods support the same operations.

For example, an algorithm may define operations such as:

- replica placement
- replica selection
- provider selection
- replica replacement or deletion
- dynamic replica-number determination
- failure handling

These capabilities may exist for one algorithm and not for another.

The adapter must only invoke a behavior when it is explicitly supported by the corresponding algorithm's source-specific contract.

Important rule:

Do not add missing capabilities merely to make the interfaces uniform.

Uniform architecture does not imply uniform algorithm behavior.

Classification:

- COMMON-SIMULATOR DESIGN for the adapter interface pattern
- SOURCE-DEFINED for actual operation semantics
- UNRESOLVED when a source contract is incomplete or ambiguous

---

## 4. Conceptual adapter responsibilities

### 4.1 Initialize

Purpose:

- initialize algorithm-internal state
- read initial common simulation state when required by source logic

The algorithm may initialize:

- population
- graph
- fuzzy state
- caches
- optimization state
- method-specific statistics

During initialization, the algorithm must not mutate authoritative common simulation state except through simulator-approved decisions when such behavior is explicitly source-defined.

Classification:

- SOURCE-DEFINED when the algorithm defines initialization behavior
- COMMON-SIMULATOR DESIGN for the simulator-approved decision route
- UNRESOLVED when the source contract does not specify initialization semantics

### 4.2 HandleRequest

Purpose:

- handle a request or event in the context of the algorithm's source-defined logic

HandleRequest does not imply that every algorithm performs replication, replacement, or selection for every request.

The adapter must invoke only source-defined operations applicable to:

- the algorithm
- the current event
- the current simulation state

If an algorithm does not define an operation, the adapter must not invent one.

Classification:

- SOURCE-DEFINED
- UNRESOLVED when the method does not specify the relevant behavior

### 4.3 SelectReplica

Purpose:

- return a replica-selection decision when such logic is explicitly defined by the source method

The adapter reads common state and returns a decision.

It must not directly modify request state, replica state, or the catalog.

Classification:

- SOURCE-DEFINED
- UNRESOLVED when not specified

### 4.4 SelectProvider

Purpose:

- return a provider-selection decision when explicitly defined by the source method

The adapter reads the relevant common state and returns a provider choice. It does not mutate the authoritative state.

Classification:

- SOURCE-DEFINED
- UNRESOLVED when not specified

### 4.5 DecideReplication

Purpose:

- return the source-defined replication decision when explicitly defined by the algorithm

The decision may include creation, duplication, or placement actions, but it is still a decision object rather than a state mutation.

Classification:

- SOURCE-DEFINED
- UNRESOLVED when not specified

### 4.6 DecideReplacement

Purpose:

- return a deletion/replacement decision when explicitly defined by the source method

The algorithm may decide to remove, replace, or rotate replicas, but the simulator performs the actual catalog and storage changes.

Classification:

- SOURCE-DEFINED
- UNRESOLVED when not specified

### 4.7 DecideReplicaCount

Purpose:

- return a replica-count decision where the source method explicitly defines dynamic replica-number determination

This capability is not universal across methods.

The adapter must not assume that every algorithm determines the number of replicas.

Classification:

- SOURCE-DEFINED
- UNRESOLVED when not specified

### 4.8 HandleFailure

Purpose:

- react to failure events only when the algorithm's source contract explicitly defines algorithm-specific failure handling

Failure injection itself belongs to the common simulator.

The adapter must not directly change:

- node health
- node availability
- replica availability
- network reachability

Classification:

- SOURCE-DEFINED only when the method explicitly defines failure-reaction logic
- COMMON-SIMULATOR DESIGN for failure injection itself
- UNRESOLVED when the source does not specify reaction behavior

### 4.9 Finalize

Purpose:

- finalize algorithm-internal state
- return algorithm-specific results when required by the source contract

Finalization is not a mutation of common simulator state.

Classification:

- SOURCE-DEFINED
- COMMON-SIMULATOR DESIGN for final result collection infrastructure

---

## 5. Input to the adapter

The adapter is allowed to read common simulation state. The set of common-state concepts is defined by the shared domain model and includes:

- current simulation time
- file metadata
- replica locations
- replica validity
- node and site state
- VM and resource state
- storage capacity and usage
- network bandwidth
- network latency
- access history
- request information
- task information
- failure and health state
- source-defined metric context

These are available common-state concepts.

Important constraint:

Do NOT state that every algorithm uses every field.

Actual usage depends on the corresponding source-specific contract.

The adapter may read only the fields relevant to the algorithm's source-defined logic.

Classification:

- COMMON-SIMULATOR DESIGN for the common-state surface
- SOURCE-DEFINED for algorithm-specific field usage

---

## 6. Output from the adapter

The adapter returns decisions, not state mutations.

Conceptual decision categories include:

- ReplicaSelectionDecision
- ProviderSelectionDecision
- ReplicaCreationDecision
- ReplicaDeletionDecision
- ReplicaMovementDecision
- ReplicaCountDecision
- FailureHandlingDecision

These are conceptual categories only.

They do not force every algorithm to emit every decision type.

If a decision category is not applicable to an algorithm, it remains unsupported rather than being artificially implemented.

The adapter's output is a request to the simulator to validate and later execute a permitted state transition.

Classification:

- COMMON-SIMULATOR DESIGN for the decision envelope
- SOURCE-DEFINED for decision semantics
- UNRESOLVED when the method has no source-defined decision for a category

---

## 7. Decision validation

After an adapter returns a decision, the common simulator performs the integration flow:

1. receives the decision
2. validates it against the common rules
3. rejects invalid decisions
4. executes valid decisions
5. mutates authoritative state
6. records corresponding events
7. updates common metrics

The algorithm adapter does not perform these operations directly.

Example:

Algorithm returns:

"Create replica of File F at Site S."

The simulator validates:

- file exists
- target site exists
- target site is eligible
- storage is sufficient
- provider is valid
- required common constraints are satisfied

Only after validation does the simulator execute the actual state transformation.

This is the authoritative mutation boundary.

Classification:

- COMMON-SIMULATOR DESIGN

---

## 8. Decision vs state transition

A decision is not a mutation.

A state transition is the simulator-owned execution of that decision.

Example:

Algorithm:

"Delete Replica R."

This is a decision.

Simulator:

- validates Replica R
- removes Replica R from the active replica catalog
- releases storage
- updates storage accounting
- records ReplicaDeletion
- updates relevant metrics

This is the state transition.

The adapter must never directly perform these actions.

Classification:

- COMMON-SIMULATOR DESIGN

---

## 9. Event interaction

The simulator owns the event queue.

Adapters do not directly schedule arbitrary simulator events.

The interaction flow is:

Event occurs
→ Simulator provides relevant state/context
→ Adapter computes source-defined decision
→ Adapter returns decision
→ Simulator validates decision
→ Simulator executes decision
→ Simulator schedules any resulting endogenous event if applicable
→ Simulator records state transition and metrics

### 9.1 Exogenous events

Exogenous events are common across matched algorithm runs.

Examples:

- request arrivals
- scheduled failures
- scheduled recoveries

These are part of the common scenario infrastructure and must be the same for matched comparative runs.

### 9.2 Endogenous events

Endogenous events are caused by decisions made during simulation.

Examples:

- replica creation
- replica deletion
- replica movement
- other events generated by a valid algorithm-driven decision

Endogenous events may differ across algorithms because their decision sequences may differ, but they must be generated only by the simulator after validation.

Classification:

- COMMON-SIMULATOR DESIGN for event ownership and scheduling
- SOURCE-DEFINED for the semantics of the algorithms' decisions

---

## 10. State ownership table

| State | Owner | Adapter may read? | Adapter may mutate? |
| --- | --- | --- | --- |
| simulation clock | Common simulator | Yes | No |
| event queue | Common simulator | Yes | No |
| node health | Common simulator | Yes | No |
| storage capacity | Common simulator | Yes | No |
| storage usage | Common simulator | Yes | No |
| file catalog | Common simulator | Yes | No |
| replica catalog | Common simulator | Yes | No |
| network state | Common simulator | Yes | No |
| request history | Common simulator | Yes | No |
| common metrics | Common simulator | Yes, when required by source-defined logic | No |
| algorithm-internal state | Algorithm | Yes | Yes |

Rule:

- Common simulator owns authoritative common state.
- The adapter may read common state.
- The adapter may not mutate common state.
- Algorithm-internal state is owned by the algorithm and is mutable only within the algorithm.

Classification:

- COMMON-SIMULATOR DESIGN for ownership rules

---

## 11. Metrics boundary

Common metrics are simulator-owned.

Algorithms may read relevant metric context only when required by their source-defined logic.

Algorithms must not directly modify the common metrics store.

### 11.1 Common evaluation metrics

Examples include:

- response time
- energy
- data-node load
- total cost
- closeness centrality
- availability
- reliability
- replica count
- successful requests
- failed requests

These are common evaluation metrics and must be calculated consistently by the simulator from authoritative state and event history.

### 11.2 Algorithm-internal values

Examples include:

- HRS fuzzy value
- NSGA-III objective values
- DPRS graph values
- EIMORM optimization state
- OGSA fitness or gravitational-search state

These values are algorithm-internal and must not be confused with common evaluation metrics.

Classification:

- COMMON-SIMULATOR DESIGN for common metrics ownership
- SOURCE-DEFINED for algorithm-internal value semantics
- UNRESOLVED when an algorithm-specific objective or metric value is not clearly specified by source documentation

---

## 12. Fairness

The adapter contract must preserve comparative fairness.

For matched comparative runs:

- same scenario definition
- same frozen initial state
- independent deep-cloned runtime state
- same exogenous request workload
- same exogenous failure/recovery schedule
- same file sizes
- same network configuration
- same simulation duration
- same scenario randomness

Algorithm-local randomness may differ.

The system must not require:

- identical random-number consumption across algorithms
- identical endogenous event sequences across algorithms

Comparative fairness means common inputs and common environment, not identical algorithm execution traces.

Classification:

- COMMON-SIMULATOR DESIGN

---

## 13. Algorithm-specific contract boundary

This adapter architecture is common.

The algorithm behavior is not common.

For each algorithm, source-specific behavior remains authoritative in its own source contract:

- Proposed NSGA-III → Proposed method implementation contract if defined by the project
- HRS → [docs/algorithms/HRS-implementation-contract.md](docs/algorithms/HRS-implementation-contract.md)
- DPRS → [docs/algorithms/DPRS-spec.md](docs/algorithms/DPRS-spec.md) and/or implementation contract if present
- EIMORM → corresponding source-specific contract
- OGSA → corresponding source-specific contract

This document does not duplicate scientific equations or source algorithm logic.

It only defines the integration boundary between the common simulator and a source-defined algorithm.

Classification:

- COMMON-SIMULATOR DESIGN for the adapter boundary
- SOURCE-DEFINED for source algorithm behavior

---

## 14. Unsupported operations

If an algorithm does not support an operation according to its source contract:

- the adapter must not call it
- the simulator must not fabricate a result
- no default algorithm behavior may be silently substituted
- the operation must remain unsupported or not applicable

Do not use "do nothing" as a hidden replacement for an unsupported scientific operation unless the source contract explicitly requires that behavior.

Classification:

- COMMON-SIMULATOR DESIGN for unsupported-operation handling
- SOURCE-DEFINED when a method explicitly defines a no-op or fallback behavior
- UNRESOLVED when the source does not specify the fallback rule

---

## 15. Failure handling

Failure injection belongs to the common simulator.

NodeFailure and NodeRecovery are common simulation events.

An algorithm may react to a failure only if its source contract explicitly defines failure handling.

The adapter must never:

- mark a node failed
- restore a node
- directly change replica availability
- directly modify network reachability

The simulator owns these state transitions.

Classification:

- COMMON-SIMULATOR DESIGN for failure injection and state transition ownership
- SOURCE-DEFINED for algorithm-specific response semantics
- UNRESOLVED when a source method does not formalize failure response

---

## 16. Invalid decisions

If the adapter returns an invalid decision, the common simulator must:

- reject the decision
- prevent unauthorized state mutation
- record the invalid decision for diagnostics
- include appropriate failure or diagnostic information

This diagnostic behavior must not silently invent algorithm-specific recovery logic.

If a source defines a specific recovery policy, that policy belongs in the algorithm-specific contract.

Classification:

- COMMON-SIMULATOR DESIGN

---

## 17. Determinism and randomness

### 17.1 Scenario randomness

Scenario randomness controls common scenario generation, workload generation, and failure schedule generation.

It must be reproducible and must be the same across matched algorithm runs.

### 17.2 Algorithm randomness

Algorithm randomness belongs to the algorithm.

It may differ between algorithms and does not have to be consumed in the same order or quantity.

It must be independently seedable and reproducible for the algorithm itself.

Do not force algorithms to consume identical random streams.

Classification:

- COMMON-SIMULATOR DESIGN for scenario randomness
- SOURCE-DEFINED or RESEARCHER-DEFINED for algorithm-local randomness setup

---

## 18. Conceptual pseudocode interaction

The following pseudocode describes the interaction pattern at a conceptual level only.

```text
OnEvent(event):

    simulatorState = Simulator.GetReadOnlyState()

    if Adapter.Supports(event):
        decision = Adapter.Handle(event, simulatorState)
        validatedDecision = Simulator.Validate(decision)

        if validatedDecision is valid:
            Simulator.Execute(validatedDecision)

    Simulator.RecordStateAndMetrics()
```

Important:

- this is conceptual pseudocode only
- it is not C# code
- it is not an implementation contract for a specific class or interface
- it expresses the required architecture and data flow

Classification:

- COMMON-SIMULATOR DESIGN

---

## 19. Five-algorithm capability matrix

This matrix records only capabilities that are explicitly supported by the relevant source-specific contract. Any capability not established conclusively remains UNRESOLVED.

| Capability | Proposed NSGA-III | HRS | DPRS | EIMORM | OGSA |
| --- | --- | --- | --- | --- | --- |
| Replica selection | YES | YES | UNRESOLVED | UNRESOLVED | UNRESOLVED |
| Provider selection | UNRESOLVED | YES | UNRESOLVED | UNRESOLVED | UNRESOLVED |
| Replica creation | UNRESOLVED | YES | UNRESOLVED | UNRESOLVED | UNRESOLVED |
| Replica deletion/replacement | YES | YES | UNRESOLVED | UNRESOLVED | UNRESOLVED |
| Dynamic replica count | YES | NO / NOT DEFINED | UNRESOLVED | UNRESOLVED | UNRESOLVED |
| Placement optimization | YES | YES | YES | YES | YES |
| Failure handling | UNRESOLVED | NO / NOT DEFINED | UNRESOLVED | UNRESOLVED | UNRESOLVED |

Important rule:

- Use only YES, NO / NOT DEFINED, or UNRESOLVED.
- YES means the capability is explicitly established by the source-specific contract.
- NO / NOT DEFINED means the existing source contract explicitly establishes that the method does not define the capability.
- UNRESOLVED means the current source contract does not provide enough information to determine the capability conclusively.
- The matrix must not invent capabilities merely because they are common in replication systems.

Classification:

- SOURCE-DEFINED when the source contract is explicit
- UNRESOLVED when the source does not provide enough formal detail
- NO / NOT DEFINED when the algorithm contract explicitly does not define that capability

---

## 20. Classification summary

The adapter architecture itself is:

- COMMON-SIMULATOR DESIGN

Algorithm decision semantics are:

- SOURCE-DEFINED

Any unresolved source behavior remains:

- UNRESOLVED

Researcher-defined configuration choices remain:

- RESEARCHER-DEFINED

This classification is strict and must be preserved consistently throughout the architecture.

---

## 21. Final validation checklist

- [ ] Adapter reads common state but does not mutate it.
- [ ] Simulator owns authoritative common state.
- [ ] Adapter returns decisions.
- [ ] Simulator validates decisions.
- [ ] Simulator executes decisions.
- [ ] Simulator performs state mutations.
- [ ] Simulator owns event queue.
- [ ] Adapter cannot schedule arbitrary events.
- [ ] Unsupported algorithm operations are not invented.
- [ ] Common architecture does not imply common algorithm behavior.
- [ ] Exogenous events are common across matched runs.
- [ ] Endogenous events may differ.
- [ ] Scenario randomness is separated from algorithm randomness.
- [ ] Common metrics remain simulator-owned.
- [ ] Algorithm-internal values remain algorithm-specific.
- [ ] Failure injection is simulator-owned.
- [ ] Algorithm-specific failure handling is source-dependent.
- [ ] No scientific equations were invented.
- [ ] No source-specific behavior was duplicated or redefined.
- [ ] No implementation code was created.

---

## 22. Contract conclusion

This document defines the adapter boundary, not the algorithm behavior itself.

The interrelationship is:

- common environment provides shared state
- the adapter reads state and computes a source-defined decision
- the simulator validates and executes the decision
- the simulator mutates authoritative state and records results

This preserves scientific fidelity, comparative fairness, and a clear ownership boundary between common simulation infrastructure and source-specific algorithm logic.

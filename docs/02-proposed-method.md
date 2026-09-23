# Proposed Replication Method

## 1. Overview

The proposed method is a dynamic and multi-objective data replication
strategy for Edge-Cloud computing.

It consists of four major components:

1. Replica selection
2. Replica number and timing determination
3. Replica placement using NSGA-III
4. Replica replacement

The method dynamically adapts replica decisions according to
data importance, access behavior, node capacity, and system conditions.

---

# 2. Component 1: Replica Selection

The proposed method calculates an Overall Importance Score (OIS)
for every data file.

For file fi:

OIS_i =
w1 * AF_i +
w2 * FS_i +
w3 * RF_i +
w4 * T_i +
w5 * UC_i

where:

AF_i = weighted access frequency

FS_i = file size score

RF_i = replication frequency score

T_i = file type importance

UC_i = number of users accessing the file

w1 ... w5 are configurable weights.

The default configuration uses equal weights unless another
experimental configuration is explicitly specified.

---

## 2.1 Access Frequency

Recent access events must have higher importance than older events.

For access event j:

weight_j = exp(-lambda * t_j)

where:

t_j = time difference between the current time and the timestamp
of the access event

lambda = exponential decay parameter

The weighted access frequency is:

AF_i =
sum(weight_j * v_j) / sum(weight_j)

where:

v_j = value/frequency associated with access event j.

---

## 2.2 File Size Score

The file-size score is:

FS_i = log(S_i)

where:

S_i = file size.

The logarithmic transformation prevents very large files from
dominating the importance score.

---

## 2.3 Replication Frequency

The replication-frequency score is:

RF_i = Nrf_i * w_i

where:

Nrf_i = number of times file fi has required replication

w_i = time-based weighting factor.

---

## 2.4 File Type

T_i represents the importance of the file type.

File types must be configurable.

The simulator must not arbitrarily assign file-type priorities.

The configuration must explicitly specify the priority of each
file type.

---

## 2.5 User Count

UC_i represents the number of users accessing file fi.

A larger number of users increases the importance of the file.

---

# 3. Component 2: Replica Number and Timing

The proposed method periodically evaluates the required number
of replicas.

The number of required new replicas is calculated as:

Nn = ceil(WA / Rj-max) - Nc

where:

WA = weighted access rate

Rj-max = maximum request-processing rate considered for the node

Nc = current number of replicas.

---

## 3.1 Replica Decision

If:

Nn = 0

No replication action is required.

If:

Nn > 0

Additional replicas must be created.

If:

Nn < 0

Some existing replicas should be removed.

The replica decision must be performed dynamically during simulation.

---

# 4. Component 3: Replica Placement Using NSGA-III

The placement problem is formulated as a five-objective optimization problem.

The objectives are:

1. Minimize energy consumption
2. Minimize response time
3. Minimize data-node load
4. Minimize total cost
5. Maximize closeness centrality

NSGA-III is used as the multi-objective optimization algorithm.

NSGA-III is a reference-point-based many-objective evolutionary
optimization method designed for problems with multiple objectives.
The original method is based on the NSGA-II framework and uses
reference points to maintain diversity among non-dominated solutions.
(Deb and Jain, 2014)

Reference:
DOI: 10.1109/TEVC.2013.2281535

---

# 5. Decision Variables

The decision variable determines whether file fi is placed on
data node Dj.

Define:

psi(i,j) = 1

if file fi is replicated on node Dj.

psi(i,j) = 0

otherwise.

A candidate solution therefore represents a complete replica-placement
configuration.

---

# 6. Objective 1: Energy Consumption

The system energy consumption consists of:

- Renewable/operational energy component
- Cooling energy component

For node Dj:

ERE(j) =
sum over i [
psi(i,j) * l(i,j) *
(Pmax(j) - Pidle(j))
]
+ Pidle(j)

Total energy:

ERE = sum_j ERE(j)

Cooling energy is calculated using the coefficient of performance:

Q = 1 / (Tout / Tin - 1)

and:

ECE(j) = ERE(j) / Q

Total cooling energy:

ECE = sum_j ECE(j)

Total system energy:

E(system) = ERE + ECE

Objective:

Minimize E(system)

---

# 7. Objective 2: Response Time

Response time includes:

- queue waiting time
- read/write time
- data transfer time

For file fi:

RT_i = Tw + Tw/r + Ttrsf

where:

Tw = queue waiting/service-related waiting component

Ttrsf = data transfer time.

Queue parameters include:

lambda_m = request arrival rate

mu_m = service rate

rho_m = utilization ratio

rho_m = lambda_m / mu_m

The exact queueing formulation must follow the equations defined
in the dissertation.

---

# 8. Objective 3: Data Node Load

Node load consists of four components:

1. Storage capacity/load
2. CPU capacity/load
3. Memory capacity/load
4. Disk read/write activity

Storage:

Cj,ds = Dj,size - Dj,usage

CPU:

Cj,cpu = fr_j * nc_j * (1 - uf_j)

Memory:

Cj,mem = ms_j * (1 - mc_j)

Disk I/O:

Cj,w/r =
alpha * Sj,r +
(1-alpha) * Sj,w

Overall node load:

LP_j =
w1*Cj,ds +
w2*Cj,cpu +
w3*Cj,mem +
w4*Cj,w/r

Objective:

Minimize overall data-node load.

---

# 9. Objective 4: Total Cost

Total cost:

TC = DTC + DSC

Data transfer cost:

DTC(dn_j1,dn_j2) =
size(fi) / BW(j1,j2) * CC(j1,j2)

Storage cost:

DSC(fi,Dj) =
sum over i,j [
psi(i,j) * uc * size(fi)
]

Storage unit cost satisfies:

uce <= ucf <= ucc

where:

uce = edge storage cost

ucf = fog/edge-cloud intermediate storage cost

ucc = cloud storage cost

Objective:

Minimize total cost.

---

# 10. Objective 5: Closeness Centrality

For node Dj:

Centrality_j =
sum over k != j d(j,k)

The dissertation currently uses this distance-based formulation
as the network centrality objective.

The implementation must preserve the exact definition used in
the dissertation.

The intended optimization direction is:

Maximize closeness-centrality-related placement quality.

IMPORTANT:
Before implementation, verify whether the reported metric is
raw distance, inverse distance, or conventional closeness centrality.
Do not silently change the definition.

---

# 11. NSGA-III Procedure

The NSGA-III implementation must include:

1. Population initialization
2. Fitness evaluation
3. Non-dominated sorting
4. Reference-point generation
5. Normalization of objectives
6. Association of solutions with reference points
7. Selection
8. Crossover
9. Mutation
10. Generation replacement
11. Termination
12. Selection of the final placement solution

The five objectives must be normalized before reference-point
association.

---

# 12. Constraints

Replica placement must satisfy:

- Node storage capacity
- Node availability
- Valid replica locations
- Maximum/minimum replica limits
- Network constraints where applicable

A failed node cannot be selected as a valid placement target.

---

# 13. Component 4: Replica Replacement

When sufficient storage space is unavailable, the system must
identify replicas that can be removed.

Replacement procedure:

1. Calculate the importance score of existing replicas.
2. Identify low-importance replicas.
3. Select candidates for removal.
4. Remove selected replicas.
5. Allocate the released storage to new replicas.
6. Update replica metadata.
7. Update the system catalogue.

High-importance replicas should be preserved whenever possible.

Replacement must never cause a file to become unavailable if the
replication constraints require at least one valid replica.

---

# 14. Dynamic Behavior

The proposed method is dynamic.

At defined evaluation intervals:

1. Update access history.
2. Recalculate file importance.
3. Recalculate required replica count.
4. Detect changes in node state.
5. Detect failures.
6. Run replica placement when necessary.
7. Perform replacement when necessary.
8. Update metadata.

---

# 15. Important Implementation Rule

Do not simplify the proposed method into "NSGA-III placement only."

The complete proposed method is:

OIS-based selection
+
dynamic replica-number/timing decision
+
NSGA-III placement
+
replica replacement.

All four components must be implemented.
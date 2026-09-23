# HRS specification extracted from the original paper

## Source-Verified Facts

### A. Algorithm identity

- Exact algorithm name: Hybrid Replication Strategy
- Paper title: "A hybrid data replication strategy with fuzzy-based deletion for heterogeneous cloud data centers"
- Authors: N. Mansouri and M. M. Javidi
- Publication year: 2018
- Acronym used by the paper: HRS
- Alias: No alternative project alias is provided in the paper; HRS remains the source name.

### B. Overall HRS workflow

The paper states that the replication process has three phases: placement, selection, and replacement.

From the paper:

- "When a task needs the file, and it is not present in the local storage, replication takes place."
- In the first phase, HRS "selects the best site (i.e., that is the most central site with high number of access) for storing new replica to reduce access time."
- In the second phase, HRS "considers the best replica node for users based on different parameters such as CPU process capability, network transmission capability, I/O capability of disks, load, and network latency."
- In the third phase, the replacement decision is made "in order to provide better response time."
- The placement step is driven by the centrality factor and the number of accesses.
- The selection step is driven by VM capability, VM load, and network performance.
- The replacement step is triggered when storage is not sufficient in the best site for the new replica.

The paper also states the following decision flow in the flowchart:

1. Get the next logical file (f) from job description.
2. If f is available in local site, do nothing.
3. Otherwise, select the best site (S) based on the Merit value (Eq. (2)).
4. Select the best provider based on the TotalCost value (Eq. (6)).
5. If replica of f exists in site S, do nothing.
6. If enough space does not exist in replica in site S, apply fuzzy replacement.

### C. Replica placement

The paper explains that the relative importance of a site is determined by the centrality of a node in a graph. It selects closeness centrality as the metric for placement, because it considers both the maximum distance and the sum of distances to all other sites, and it can separate global centrality from local centrality.

The paper gives the following closeness centrality definition exactly:

- Centrality(v) = (N - 1) / Σ_{a ≠ v} d(v,a)    (Eq. (1))

Where:

- N is the total number of sites in the system.
- d(v,a) is the distance between site v and site a.

The paper also states: "A site is set as closeness in a network, if it has the lowest value for the summation of the distances from all of the other sites. The lower the sum of distances from the other sites, the more centrality has the site."

The placement formula is given as:

- Merit = W1 × Number of access + W2 × Centrality    (Eq. (2))

The text states that the values of W1 and W2 are determined empirically and that normalization is required because the scales of the parameters are different.

Normalization rule from the paper:

- "We know that the scale of above parameters is different. Therefore, it is necessary to transform value of parameters into a scale of 1–10 before applying them in the Eq. (2). We assume that the scale of normalization is uniform. Let us assume that Inc. = (max–min)/10. Then, value of factors between min and min+Inc. should be normalized to 1, value between min+Inc. to min+2 × Inc. should be normalized to 2, and so on."

The paper gives the empirical weight values in Table 3, reproduced as:

| W1 | W2 | Response time (s) |
| --- | --- | --- |
| 0.1 | 0.9 | 64 |
| 0.3 | 0.7 | 53 |
| 0.5 | 0.5 | 51 |
| 0.6 | 0.4 | 49 |
| 0.8 | 0.2 | 56 |
| 1 | 0 | 68 |

The paper text then says:

- "Experiment results highlight that the best performances are reached when W1 = 6 and W1 = 4."

This wording is internally inconsistent because the surrounding text discusses W1 and W2 and the table shows W1/W2 pairs less than 1. The original PDF is therefore treated as containing an apparent typographical inconsistency in the weight statement. This is retained as a source fact, not silently corrected.

Candidate site definition:

- The paper describes the selected site as the best site, i.e., the site with the highest Merit value.

Site-selection rule:

- The site with the highest Merit value is selected for storing the new replica.

### D. Replica selection

The paper defines the replica-selection objective as choosing the provider with minimum TotalCost.

#### D.1 Capacity of VM (C)

The paper states:

- CPU process capability, communication bandwidth ability, and storage are the most common parameters in determining VM capability.
- "Since VMs with high CPU capability have high RAM size, we do not consider storage parameter in replica selection process."
- "In the proposed replica selection method, C represents virtual machine capability. We can determine C by considering two parameters as CPU process capability (Mips) and communication bandwidth ability (Gbps), denoted by α and β, respectively. In addition, n is the number processors. In the sequel, C is found by Eq. (3) [36]:"

Exact equation:

- C = (n × α) + β    (Eq. (3))

Where:

- n = number of processors
- α = CPU process capability (Mips)
- β = communication bandwidth ability (Gbps)

#### D.2 Load of VM (L)

The paper states:

- "The load of a VM_i is determined as the total length of tasks at time t to service queue of VM_i divided by the service rate of VM_i at time t [36, 37]."

Exact equation:

- L = N_t / S_r    (Eq. (4))

Where:

- N_t indicates total length of tasks on service queue.
- S_r shows service rate.

#### D.3 Network performance (N)

The paper states:

- "It is generally true that higher bandwidth and lower latency are both good. We compute the network performance between nodes a and b based on the bandwidth (in Mbits/s) and latency (in ms) as following [38]:"

Exact equation:

- N(a,b) = Bandwidth(a,b) / Network_Latency(a,b)    (Eq. (5))

#### D.4 TotalCost

The paper states:

- "TotalCost function that is given by Eq. (6) must be tailored, because it is defined as a weighted combination of three former parameters. It is obvious that the higher load of VM (L), lower capability of VM (C), and lower network performance (N) makes total cost higher. Therefore, capabilities of VM and network performance have reverse effect."

Exact equation:

- TotalCost = W3 × 1/C + W4 × L + W5 × 1/N    (Eq. (6))

Where:

- W3, W4, W5 are appropriate weights.

The paper then says:

- "For W3, W4, and W5, we consider the weight vector to adjust performance ratio factors when choosing replica in order to meet the users’ satisfaction better."
- "In our simulation W3, W4, and W5 have equal value."
- "Finally, if necessary file does not exist in the local site, then HRS method creates a list of candidate replica providers and selects a provider with the minimum TotalCost value based on Eq. (6)."

Weight vector:

- W = [W3, W4, W5]    (Eq. (7))

The paper also gives the normalization condition:

- Σ_{i=3}^{5} W_i = 1    (Eq. (8))

Direction of optimization:

- Minimize TotalCost.

Candidate-provider definition:

- The set of replica providers that are candidates when the required file is not present locally.

Selection rule:

- Select the provider with the minimum TotalCost value.

### E. Replica replacement

The paper states:

- "When sufficient storage space is not available in the best site for storing new replica, one or more of the existing replicas should be deleted."
- HRS takes into account three parameters as number of accesses, cost, and the last time the replica was accessed.
- The number of access and the last time the replica was requested identify the probability of requesting the file again.
- "It is obvious that a file with high cost value is not a good candidate for deletion. This is because, if a site requires that file in the future, we must pay high charge for replicating it again, and this is not economical."

#### E.1 Replication cost

The paper defines replication cost as Eq. (9), citing [40]:

- Cost = Size / Bandwidth(x,y) + Propagation Delay Time (x,y)    (Eq. (9))

The paper then explains:

- Size is size of replica.
- Bandwidth(x, y) is bandwidth between provider site x and requester site y.
- PropagationDelayTime(x, y) indicates the time required to propagate the needed replica from provider x to the requester site y.
- The paper notes: "We know that a closer site can quickly transfer replica."

It also states:

- "The higher replica size makes the replication cost higher."
- "The lower bandwidth between provider and requester sites, the higher replication cost is."
- "Propagation delay time depend on network traffic conditions. The greater delay time makes the replication cost higher. This parameter must be considered since the data may wait in network queues before submitted."

#### E.2 Fuzzy system

The paper says HRS uses a fuzzy inference system with three input parameters:

- number of accesses
- cost
- last time the replica was accessed

and one output:

- Value of replica

The three input parameters are described in Figure 4 and Figure 5, and the paper states: "Figure 4 indicates fuzzy inference system for assigning the value to each replica."

It also states that the fuzzy system is implemented in Matlab Fuzzy Logic Toolbox.

The paper states the input and output ranges exactly:

- Number of accesses range: 0 to 55
- Replication cost range: 0 to 25
- Last access time interval range: 0 to 12 × 10^5
- Output parameter (Value of replica) range: 0 to 1

The paper states:

- "A replica that has lowest value is an appropriate candidate for deletion."
- "Also 21 rules have been defined for the proposed fuzzy system. Table 4 describes some of the proposed fuzzy system rules."

The paper further states:

- "HRS calculates the Value of all files that are available in the best site by a fuzzy function. Then it sorts list in ascending order of Value. It selects candidate files from list until enough space is available."
- The deletion rule is therefore: select the lowest-value replicas first, and delete candidate files until enough space is available.
- The stopping condition is: stop when enough space is available.

Fuzzy-system table entries shown in the paper (examples only):

1. If (Number of Accesses is high) and (Replication Cost is high) and (Last Access Time Interval is low) then (Value of Replica is very high)
2. If (Number of Accesses is high) and (Replication Cost is average) and (Last Access Time Interval is low) then (Value of Replica is high)
3. If (Number of Accesses is high) and (Replication Cost is high) and (Last Access Time Interval is average) then (Value of Replica is high)
4. If (Number of Accesses is low) and (Replication Cost is low) and (Last Access Time Interval is average) then (Value of Replica is low)
5. If (Number of Accesses is low) and (Replication Cost is low) and (Last Access Time Interval is average) then (Value of Replica is low)

The paper says Table 4 describes some of the rules; it does not include the full set of 21 rules in text or a fully legible table. This is therefore a source-defined but incomplete rule set from the paper.

Important source-fidelity note:

- The paper provides Figure 5, which visually shows triangular membership functions for the three inputs and output.
- Figure 5 labels the terms as follows:
  - Number of accesses: Low / Average / High
  - Replication cost: Low / Average / High
  - Last access time interval: Low / Average / High
  - Value of replica: Very low / Low / Average / High / Very high
- However, the exact numeric breakpoints and membership-function parameters are not recoverable with enough certainty from the visible image alone, so the precise membership-function parameters are marked as SOURCE-UNRESOLVED.

### F. Simulation configuration

The paper gives Table 5: "Parameters setting of cloud simulator".

Table 5 text, as visible in the PDF, is:

| Type | Parameters | Value |
| --- | --- | --- |
| Data center | Number of data center | 20 |
|  | Number of host | 3–10 |
|  | Type of manager | Space_shared / Time_shared |
| Virtual machine | Total number of VMs | 60 |
|  | MIPS of processing element | 300–2500 |
|  | Number of processing element per VM | 2–5 |
|  | VM memory (RAM) | 512–2048 (MB) |
| Task | Total number of task | 100–1000 |
|  | Length of task | 100–500 |
|  | Number of processing elements requirement | 1–4 |

Additional simulation statements from the paper:

- "The parameter of simulation is set based on the existing studies [43] to realistically represent a typical cloud environment."
- "We set cloud system with 20 data centers and 100–1000 tasks in CloudSim."
- "Each task is assigned based on the Poisson distribution after the previous task and number of files requirement is 1–5."
- "The computation workload of the task is from 100 to 500 Million Instructions."
- "At the beginning of simulation, we randomly placed the primary copy of each data file in different sites."
- The paper states: "We have extended different classes of CloudSim toolkit to test replication algorithms. CloudSim is an event-driven simulator and contains four layers: SimJava, GridSim, CloudSim, and User code."
- The paper states: "For task scheduling, we consider Time_shared strategy by CloudletSchedulerTimeShared class."
- The paper states: "We implement makeReplica() method in File class based on the proposed strategy."

Network/topology parameter note:

- The paper does not provide a complete explicit topology specification, network graph, or bandwidth matrix in the HRS paper itself.
- Therefore, those topology-level network details are not present as a source-verified HRS specification.

### G. Complexity

The paper states the following complexity results in the final section before the implementation environment:

- "Replica Placement complexity is O(m). Since HRS finds the best node based on the highest Merit value."
- "Replica Replacement complexity is O(n log n). Because HRS needs a sorting algorithm based on the value of replica."
- "Replica Selection complexity is O(m). Since HRS finds the best node based on the TotalCost value."

There is no explicit end-to-end overall HRS complexity statement in the paper; therefore the aggregate complexity is not source-specified.

### H. Evaluation metrics

The paper names the performance metrics evaluated in Section 5:

- average response time
- mean latency
- hit ratio
- bandwidth consumption
- number of communications
- storage usage
- load variance

#### H.1 Average response time

Exact formula as printed in the paper:

- Average Response Time = [Σ_{j=1}^{m} Σ_{k=1}^{m_j} (ts_jk(rt) - ts_jk(st))] / [Σ_{j=1}^{m} m_j]    (Eq. (10))

Where:

- ts_jk(st) is the submission time of task k for user j.
- ts_jk(rt) is the return time of the result for task k of user j.
- m_j is the number of tasks for user j.

#### H.2 Mean latency

The paper states that latency L_i of file f_i is obtained as follows:

- L_i = (1 / r_i) × Σ_{j=1}^{m} θ(i,j) × s_i / B_j × A(i,j)    (Eq. (11))

Where:

- r_i indicates number of replicas for file f_i.
- s_i shows the size of file f_i.
- θ(i,j) is a decision variable with value 1 when file f_i is available on site D_j; otherwise 0.
- A(i,j) indicates the percentage of requests coming from site D_j asking for f_i.
- B_j shows the bandwidth of D_j.

#### H.3 Hit ratio

The paper defines it qualitatively as:

- "Hit ratio is as the proportion of total number of local file accesses to all accesses (i.e., local file accesses, total number of replications, and total number of remote file accesses)."

No exact equation is supplied in the HRS paper.

#### H.4 Bandwidth consumption

The paper says:

- CloudSim determines bandwidth usage by the BwProvisioner class in the Cloudbus package.
- The bandwidth allocated and the utilized bandwidth are obtained by AvailableBw() and getUsedBw() methods, respectively.

No exact equation is supplied in the HRS paper.

#### H.5 Number of communications

The paper discusses the metric qualitatively but does not provide an algebraic equation.

#### H.6 Storage usage

The paper gives the formula:

- Storage Usage = Filled_Space / Available_Space    (Eq. (11))

The text describes it as the storage usage for replicas.

#### H.7 Load variance

The paper explains the concept qualitatively:

- "The load balancing technique is used for distributing the load (computing tasks) among different resources (nodes) in the system."
- "Usually, load balancing within the network depicts by load variance, i.e., the standard deviation of data nodes in the cloud storage."
- "The lower value of load variance shows the lower value of degree deviation and the greater degree of load balancing."
- "When the load becomes totally balanced (i.e., in the best case), the load variance is zero."

The paper does not include an explicit equation for load variance.

## Source-Unresolved Items

The following items cannot be recovered exactly from the original paper without inventing behavior or silently correcting the source text:

- Exact continuous membership-function parameters (breakpoints and shapes) for all fuzzy sets in Figure 5.
- Exact complete set of all 21 fuzzy rules; the paper only shows examples in Table 4 and explicitly states that 21 rules exist.
- Exact inference engine used by the fuzzy system (e.g., Mamdani vs Sugeno) is not stated.
- Exact defuzzification method is not stated.
- The precise numerical values of the triangular membership function breakpoint parameters are not legible enough from the PDF to reproduce faithfully.
- The written phrase "when W1 = 6 and W1 = 4" is internally inconsistent; the paper appears to contain a typographical error in the weight statement.
- No explicit equation for hit ratio is given.
- No explicit equation for bandwidth consumption is given.
- No explicit equation for number of communications is given.
- No explicit equation for load variance is given.
- No explicit end-to-end overall HRS complexity expression is given.
- No complete network topology specification or bandwidth matrix is given in the HRS paper itself.

## Implementation Interpretation

This section does not add scientific claims beyond what is required to interpret the paper in an implementation context.

- Replica placement is a centralized site-ranking problem in which the site with the greatest Merit value is selected for the new replica.
- Replica selection is a minimum-cost choice among candidate providers, using TotalCost as the decision value.
- HRS replacement is triggered only when a replica must be stored in a site that has insufficient free storage.
- The replacement logic sorts available replicas by fuzzy Value in ascending order and deletes the lowest-value replicas until enough space exists.
- The fuzzy output is a scalar value in [0,1]. Lower values are more deletion-prone.
- The paper explicitly states that the fuzzy system is implemented with Matlab Fuzzy Logic Toolbox, but it does not specify the exact fuzzy implementation details beyond the name of the tool.
- Any implementation must preserve the paper's source wording and must not silently substitute missing formulae or parameters.

## Extraction Audit

| Item | Status | Evidence |
| --- | --- | --- |
| Placement formula | Verified | Page 9, Eq. (1); page 10, Eq. (2) |
| Placement weights | Unresolved | Table 3; paper text says "W1 = 6 and W1 = 4" but wording is inconsistent; source text itself is internally inconsistent |
| Capability formula | Verified | Page 10, Eq. (3) |
| Load formula | Verified | Page 11, Eq. (4) |
| Network formula | Verified | Page 11, Eq. (5) |
| TotalCost formula | Verified | Page 11, Eq. (6); page 12, Eq. (7) and Eq. (8) |
| Replication cost | Verified | Page 13, Eq. (9) |
| Fuzzy membership functions | Unresolved | Figure 5; the paper states ranges but exact numerical breakpoints are not recoverable from the PDF |
| 21 fuzzy rules | Unresolved | Page 14, Table 4 gives examples only; paper states 21 rules exist but does not print full rule base |
| Simulation parameters | Verified | Page 15, Table 5; page 16, implementation environment text |
| Complexity | Verified for placement/selection/replacement | Page 15, complexity bullets |

## Final source-faithfulness note

This specification is intentionally limited to what the original HRS paper explicitly states. Missing equations, membership parameters, exact fuzzy-rule sets, and some network settings are recorded as SOURCE-UNRESOLVED rather than reconstructed from assumptions.

## A hybrid data replication strategy with fuzzy-based deletion for heterogeneous cloud data centers

N. Mansouri1,2 · M. M. Javidi1,2

© Springer Science+Business Media, LLC, part of Springer Nature 2018

Abstract At present, huge cloud-based applications have put forward higher requests for data center storage. In a large-scale Cloud environment, data replication provides an appropriate solution for managing data files, which improves data reliability and availability. In this paper, we propose a data replication algorithm called hybrid repli- cation strategy (HRS) that is applied into replica placement, selection, and replacement steps. HRS has three main phases and is suitable for replicating data files in cloud. In the first phase, it selects the best site (i.e., that is the most central site with high number of access) for storing new replica to reduce access time. In the second phase, HRS considers the best replica node for users based on different parameters such as CPU process capability, network transmission capability, I/O capability of disks, load, and network latency. In the third phase, the replacement decision is made in order to provide better response time. HRS can ascertain the importance of valuable replicas on the basis of a fuzzy inference system with three input parameters (i.e., number of accesses, cost, and the last time the replica was accessed). The new replication policy is simulated using the CloudSim toolkit package. Our proposed mechanism replicates the data over the cloud nodes reasonably well and is easily implementable in a real environment. Experiment results prove that HRS can significantly enhance availabil- ity, performance and load balance for data-intensive applications. In addition, it stands good without increasing additional overheads.


Keywords Cloud computing · Replication · CloudSim · Fuzzy system

## 1 Introduction

Unique features of cloud storage cause high desirability of cloud computing in scien- tific researches as well as industries [1–3]. Large-scale data centers present the main infrastructure of cloud for both organizations and service providers [4, 5]. Similar strategies with lower capability were investigated in past as grid computing context. Grid and cloud are closely related and sometimes even show the very same mean- ing. Foster et al. presented a survey and compared cloud and grid characteristics to each other [5]. Table 1 abbreviates side-by-side comparison ofcloud and grid. Accord- ingly, cloud computing is an advanced methodology on the base ofon-demand service. Figure 1 shows Software as a Service (SaaS), Platform as a Service (PaaS) and Infras- tructure as a Service (IaaS) were the main parts of cloud computing. [URL 🔗](#page-0)

IaaS is self-service model for providing and managing data centers infrastructure such as storage and networking [6]. PaaS is applied for application development and provides capabilities needed to deploy applications such as database management. SaaS is where software is hosted by a third party and can be used over Web. [URL 🔗](#page-0)

Cloud needs massive computing and storage capacities that are provided by data centers with high-performance distributed strategies and technologies. On the one hand, the necessity oflarge-scale cloud-based application andon the other the necessity ofmassive data centers increased the key role ofstorage cost reduction. Employment of data replication to support data reliability is a powerful technique in new distributed storage system. Amazon S3, Google File System [7] and Hadoop Distributed File System [8] are typically the major data storages that employed replication algorithm with the ability to create 3 copies from data at time to improve data reliability. Storing huge data files is being recognized as a main bottleneck, so effective data management for a large-scale distributed environment such as cloud is critical. [URL 🔗](#page-0)

*Table 1 Grid versus cloud*

| Parameter | Grid | Cloud |
| --- | --- | --- |
| Goal | Collaborative sharing of | Use of service (eliminates the |
|   | resources | detail) |
| Transparency | Low | High |
| Security | Low (grid certificate service) | High (virtualization) |
| User friendly | Low | High |
| Resource | Restrictions due to hardware | Unlimited |
| Degree of scalability | Normal | High |
| Multitask | Yes | Yes |
| Infrastructure | Low-level command | High-level services (SaaS) |
| Virtualization | Not a commodity | Vital |


*Fig. 1 Schematic representation of cloud computing services [6] [URL 🔗](#page-0)*

## 1.1 Data replication problem

As there is an explosive amount ofdata in cloud day after day, storing the static number of replicas in the dynamic environment is inefficient. To address this issue, adaptive data replication algorithm is necessary. Data replication strategies are able to prepare large-scale parallel read/query data by distribution of various data replicas within different nodes of cloud and consequently decrease waiting time of user, enhance the data availability as well as decrease bandwidth consumption [9]. Figure 2 indicates a replication structure for heterogeneous data centers of cloud. Moreover, with today’s network heterogeneity, it is necessary that mobility problems are considered within any distributed environment. Satisfaction of users’ is directly related to the quality of service and availability. So, service providers must present a highly dynamic and adaptive method to provide service and data access in cloud. [URL 🔗](#page-0)

There are three steps in data replication process, namely replica placement, replica selection, and replica replacement. Replica placement determines the best possible location to copy data file based on network protocol and user request. Replica selection chooses the appropriate replica location to access the data file for job execution and has important effect on user satisfaction as well as cloud service provider, since users can achieve optimal experiences, such as low latency, the least packet loss, or high available bandwidth by choosing the right replicas.

Replica selection is one of the main steps in replication process that determines the most appropriate replica provider from those available to reduce response time. Additionally, suitable replica selection is a multi-attribute decision-making problem, since each site has its own characteristics such as CPU speed, disks, bandwidth, failure probability, storage, etc. At the same time, users have their own preferences in the sys- tem [10]. Replica replacement plays a vital role when storage is restricted. This step determines which replica to be replaced for the new one. Different replica placement, selection, and replacement methods are available in the literature [11–13]. These algo- [URL 🔗](#page-0)


*Fig. 2 Replication structure for heterogeneous data centers of cloud*

rithms measured and analyzed different parameters such as bandwidth consumption, access time, load balancing, fault tolerance, and storage consumption.

In this paper, different replicationmanagement strategies along with theirmerits and demerits are discussed. This paper also analyses the performance of new replication methods with respect to the parameters mentioned above. We propose a new data replication strategy called hybrid replication strategy (HRS) that consists of replica placement, selection, and replacement during data management. Firstly, it selects the best site based on the centrality factor and number of access for storing replica to reduce access time. Then, it selects the appropriate data centers for a particular service that helps both customers and service providers to improve data center utilization. Due to the restricted storage space of each node, replicas that are not popular for future jobs should be replaced with valuable ones. Therefore, we design replacement strategy, which uses fuzzy system for evaluating the value ofeach replica. TheHRScan be adapted based on the changes in distributed environment. Simulation results with CloudSim demonstrated that HRS works well for heterogeneous cloud environment in different metrics such as storage usage, hit ratio, number of communications and balances the nonpreemptive independent tasks.

The rest of this paper is organized as follows. Section 2 discusses about the related works on existing data replication strategies in cloud system. Section 3 focuses on our proposed replication approach with detailed algorithm, and Sect. 4 presents implemen- tation environment. Section 5 shows the experimental results along with performance evaluation of the algorithm in comparison with current replication algorithms. Finally, Sect. 6 concludes the paper and outlines future work. [URL 🔗](#page-0)

## 2 Related work

Replication technique plays a key role in all distributed systems. To the best of our knowledge, comparatively less works have been attempted for proposing dynamic replication algorithms for cloud systems; instead, most of the works exist in grid


environments. Replication can be classified into two types: static replication [14, 15] and dynamic replication [16–21]. Based on these two methods, different replication strategies and schemes have been presented by different performance levels. In static replication strategy, the number ofreplicas for each data file is set in advance, manually. In this type strategy, the placement ofreplicas is also pre-decided and these replicas are controlled manually. It cannot be adapted according to the changes in the system and users’ access patterns. However, in dynamic replication strategies, the replicas of each data file are generated, stored and maintained dynamically according to the changes in the system and users’ access patterns. In cloud computing environments, users’ access patterns may keep on changing time to time; hence, to achieve high availability along with better performance, the replication algorithms should be adapted continually to changes in the system. In cloud, dynamic replication algorithms are considered to be more acceptable than static replication algorithms. Here, a review of recent researches from these topics is presented. [URL 🔗](#page-0)

Sun et al. [22] considered cloud system as hierarchal structure in their proposed replication strategy. They supposed that more recently accessed data have higher desirability in the near future and used temporal locality [23, 24] as criteria for the determination ofmost popular data file. System availability and failure probability are employed to determine the number of necessary replicas. Then replica is placed in the nearest location that triggers the higher number ofrequests for the data. This strategy is combined with the checkpoint technique to present dynamic adaptive fault-tolerance (DAFT) method [25]. The main drawback of DAFT is neglecting the load balancing of system resources. [URL 🔗](#page-0)

Zhang et al. [26] proposed a Plant Growth Simulation Algorithm (PGSA)-based data replica selection approach for cloud system by considering the load of storage, information of replica selection history. By the consideration of plant phototropism features, their strategy employed morphactin concentration as threshold for fitting the data replicas for user access request. Selection of suitable data replica is done using regulation and comparison of its feature to morphactin concentration [27]. They evaluated PGSA by CloudSim simulator based on the replica utilization and average access time. The results confirmed that PGSA has a reasonable performance in access time. Unfortunately, PGSA did not investigate the fault tolerance in data center. [URL 🔗](#page-0)

Li et al. [28] developed a cost-based replica selection named Energy-Aware Dis- tributed Running system (EDR). This decentralized systemwas implemented with two distributed optimization algorithms. Firstly, they modeled energy cost of data centers in cloud. Then, they formulated the replica selection problem as a convex optimization problem, which reduced data center energy cost based on the bandwidth and latency of each data center. The analytical results showed that EDR achieved 12% energy savings for the data-intensive applications such as online video streaming and distributed file sharing. [URL 🔗](#page-0)

By the consideration of QoS requirements as criterion, two various strategies are presented for replication process by Lin et al. [29] as High QoS First Replication (HQFR) and Minimize Cost Maximum Flow (MCMF). The former, i.e., a greedy technique, is performed by the consideration of QoS requirements to copy necessary files from higher to lower priority, while the later technique selects the best solution. Validation of HQFR and MCMF is carried out by MATLAB, and the results are [URL 🔗](#page-0)


compared with random Hadoop strategies. Modeling of cost in terms of time and neglecting from monetary/economical unit are the main weaknesses of their proposed strategy.

Long et al. [30] designed a Multi-objective Optimized Replication Management strategy (MORM) in cloud environment. It is based on the artificial immune algo- rithm [31]. In determining relation between replica number and performance metrics, MORM uses several parameters such as unavailability of file, service time, load vari- ance, energy usage, and latency value. Then, number of replicas for each data file and replica placement among nodes is determined based on the five above objec- tives. They evaluated MORM using the extended CloudSim simulator and MATLAB toolkit. The experimental results demonstrated that the presented strategy improved file availability, load balancing, service time, latency, and energy usage for large-scale cloud storage cluster. Neglecting the fault tolerance and replacement issues are the main disadvantages for the MORM strategy. [URL 🔗](#page-0)

By the consideration of transmission cost, evaluation information ofhistory, system load, and usersQoSpreference as criteria, Louet al. [32] proposed a strategyon the base of individual QoS sensitivity restrictions. This strategy answers to this question: Does appropriate file exist in local node? If yes, it is used directly. Else, feature of replica and historical evaluation information must be checked. QoS preference is able to estimate the availability level, time line and reliability. By doing so, it is responsible to estimate the similarities between current demanding environments with the historical replica. Finally, the replica with the highest credibility similarity environment is selected. The analytical results indicated that the proposed strategy could increase data availability in an adaptive manner by adjusting the reliability parameters in the environment. [URL 🔗](#page-0)

Kumar et al. [33] illustrated a workload-aware data replication strategy (SWORD), to reduce consumption of resource in cloud. SWORD reduces the mean number of machines engaged in execution of a request or a transaction by using partition tech- niques. They adjusted query span usage as an optimization metric for analytical and transactional workloads. In addition, the authors presented a data placement method by drawing connections to different concepts of graph theoretic. SWORD uses a Hypergraph Partitioning Algorithm (HPA) for determining a balanced partitioning. For decreasing the query spans and enhancing throughputs, they used fine-grained quorums. With help of fine-grained quorums, their framework can seamlessly handle different workloads in cloud systems. SWORD strategy has Pre-Replication-based Algorithm (PRA) that finds a set of nodes to copy a priori, changes the input graph, and then calls HPA to determine a final placement. Finally, SWORD modifies Local Move-Based Replication (LMBR) algorithm for finding dense subgraph based on the cost/benefit ratio. By the consideration of two various classes of workloads as case study, the effectiveness of framework is confirmed within simulation. Employment- only average query span within replication is the main drawback of this strategy. [URL 🔗](#page-0)

Table

2 considers various metrics for side-by-side comparison of replication strate- [URL 🔗](#page-0)

gies.

- Architecture shows the architecture type that is used in the work. The common architectures used are listed as: multi-tier hierarchical, multi-tier sibling tree, HDFS (master–slave), and graph-based architectures.


A hybrid data replication strategy with fuzzy-based…

*Table 2 Side-by-side comparison of replication strategies in literatures*

| References [22][26][28][29][30][33] |   |   |   |   |
| --- | --- | --- | --- | --- |
| Architecture Multi-tier | Multi-tier | Multi-tier | Multi-tier Graph | Graph |
| Hierarchical |   |   |   |   |
| Nature Hom | Hom | Het | Het Het | Het |
| Availability + | – ++++ |   |   |   |
| Bandwidth ++– +++ |   |   |   |   |
| consump- |   |   |   |   |
| tion |   |   |   |   |
| Response ++++++ |   |   |   |   |
| time |   |   |   |   |
| Load + | + | –+ |   | –+ |
| balancing |   |   |   |   |
| Fault –––+ + |   |   |   | + |
| tolerant |   |   |   |   |
| QoS-based – | – | + | – + | – |
| Energy |   | –––+ –– |   |   |
| efficiency |   |   |   |   |
| Fuzzy –––––– |   |   |   |   |
| inference |   |   |   |   |
| simulator | CloudSim CloudSim MATLAB HDFS |   |   | CloudSim Trace-driven |
| used |   |   |   | simulator |
| Main idea Modeling | Using Plant | Modeling | Proposing Proposing | Developing |
| the rela- | Growth | dynamic | multi- node com- | partition- |
| tionship of | Simulation | energy | objective bination | ing |
| availability | Algorithm | costs | offline technique | technique |
| and replica |   |   | optimiza- |   |
| numbers |   |   | tion |   |
|   |   |   | approach |   |

- Nature indicates whether the system nature is homogeneous (Hom) or heteroge- neous (Het).

- Availability specifies whether the study considers the availability improvement. ‘+’ shows that the study focuses on increasing the availability, and ‘−’ shows that the study does not focuses on the availability aspect.

- Bandwidth consumption determines whether the bandwidth consumption is reduced by the replication approach.

- Response time specifies whether the study focuses on reducing the response time for submitted jobs.

- Load balancing determines whether the workload is balanced on most of the data centers.

- Fault tolerant parameter shows whether the proposed replication algorithm is able to improve the fault tolerance of the environment.

- QoS-based factor shows whether the replication algorithm considers different QoS metrics during the process of replication decision.


- Energy efficiency indicates the study focuses on advancing energy efficiency in data centers.

- Fuzzy inference determines whether the replication algorithm uses the fuzzy theory in its decisions.

- Simulator used factor specifies the name of the simulator applied for replication algorithm evaluation.

- Main idea shows the key contribution of that replication strategy.

Current replication algorithms are targeted at only reducing response time. There exists a lack of QoS-based replication strategy that can consider different parame- ters such as scalability and resource utilization. One way to deal with the scalability problem is to design appropriate performance models. Moreover, no works focus on the fuzzy theory in replication decision for cloud environment. This motivates us to develop an adaptive replication strategy for heterogeneous cloud systems using fuzzy inference in replacement step along with maintaining higher data availability and better performance.

## 3 Proposed data replication strategy

When a task needs the file, and it is not present in the local storage, replication takes place.

## 3.1 Replica placement

One of the serious concerns in cloud with high-speed growth of data is finding the best site for replica placement. We store replicas based on the centrality and number of replica access.

The relative importance of a site in the system can be determined by the centrality of a node in a graph. The main goal of reduced retrieval time in replication technique makes the centrality factor more serious. Therefore, the vital site in the system has some characteristics such as the following. (1) It connects more sites than others. (2) It can access other sites easily. (3) Other sites can access to it easily. There are different centrality metrics such as eccentricity, betweenness, and closeness [34]. Eccentricity measure only uses the maximum distance among all the shortest paths to the other sites. Therefore, the main drawback of eccentricity centrality is that it is sensitive to the a few unusual paths. The betweenness measure considers fraction of shortest paths between node pairs that pass through the node of interest. The main disadvantage of betweenness centrality is its computational complexity. In comparison, closeness measure considers not only the maximum distance between the target node and all other vertices but also considers the sum of the distances of this node and all other vertices. Therefore, closeness can eliminate the disturbance through summarizing the distances. Degree centrality determines the most connected nodes by measuring the number of direct connections to others. [URL 🔗](#page-0)

The main advantage of closeness measure compared with degree centrality is that closeness measure can be used for indirect connections in network. This benefit is


of nodes)

N=

*Fig. 3 The closeness centrality calculations*

more important when there are disconnected parts (cluster of nodes) in the system. In such situation, closeness measure, in contrast to degree centrality, can separate global centrality from local centrality. With these explanations, we select closeness criterion in placement process. According to the temporal locality (recently accessed file are likely to be accessed again), number of replica access has a main role in replica placement decision [35]. Therefore, we prefer to place new replica in a site with the high number of accesses and which relatively belongs to the central nodes. [URL 🔗](#page-0)

A site is set as closeness in a network, if it has the lowest value for the summation of the distances from all of the other sites. The lower the sum of distances from the other sites, the more centrality has the site. The closeness centrality value for site v can be defined as the following [34]: [URL 🔗](#page-0)

The parameter N is used to indicate total number of sites in the system and d(v, a) shows the distance between site v and site a.

For example, consider following the distances matrix for the graph in Fig. 3.The closeness centrality calculations are presented on the right of Fig. 3. Therefore, site B is the most central site based on this factor. [URL 🔗](#page-0)

In the sequel, replica is stored in the best site (i.e., best site has the highest value of Merit). Merit value is computed by Eq. (2). [URL 🔗](#page-0)

Meri t  W1 × Number of access + W2 × Centrali ty

where W1 and W2 are the proportion weights corresponding to the above two main parameters. We know that the scale of above parameters is different. Therefore, it is necessary to transform value of parameters into a scale of 1–10 before applying them in the Eq. (2). We assume that the scale of normalization is uniform. Let us assume that Inc.(max–min)/10. Then, value of factors between min and min+Inc. should [URL 🔗](#page-0)

be normalized to 1, value between mini+Inc. to mini+2 × Inc. should be normalized to 2, and so on.

The values of W1 and W2 have been determined empirically. In this respect, we measure the impact of varying the value of W1 and W2 on response time for the


*Table 3 Different values for W1 and W2*

| W1 | W2 | Response time (s) |
| --- | --- | --- |
| 0.1 | 0.9 | 64 |
| 0.3 | 0.7 | 53 |
| 0.5 | 0.5 | 51 |
| 0.6 | 0.4 | 49 |
| 0.8 | 0.2 | 56 |
| 1068 |   |   |

proposed replication algorithm.We test different values and select the best ones. Some values for W1 and W2 are shown in Table 3. Experiment results highlight that the best performances are reached when W1 6 and W1 4. [URL 🔗](#page-0)

These values for weights are reasonable since if all of the replicas are placed on the nodes based on only centrality parameter, then there is a possibility that some central nodes have high load. In addition, replica placement by considering only centrality parameter can showclues to an attacker as to where datamight be stored, decreasing the data security level. On the other hand, the number of access identifies the probability of requesting the file again. Therefore, we prefer to place new replica (R) in a site with the high number of accesses for R and relatively is belonged to the central nodes.

## 3.2 Replica selection

Data nodes are heterogeneous with various disk types, network bandwidth,CPUspeed, etc., in large-scale cloud storage system. If replica of files is available in multiple sites, then there is a considerable benefit by choosing the suitable replica provider. Therefore, we present a replica selection strategy that uses a combined cost function based on capacity of VM, load of VM, and network performance.

## 3.2.1 Capacity ofVM (C)

CPU process capability, communication bandwidth ability, and storage are the most common parameters in determining VM capability. Since VMs with high CPU capa- bility have high RAM size, we do not consider storage parameter in replica selection process.

In the proposed replica selection method, C represents virtual machine capability. We can determine C by considering two parameters as CPU process capability (Mips) and communication bandwidth ability (Gbps), denoted by α and β, respectively. In addition, n is the number processors. In the sequel, C is found by Eq. (3)[36]: [URL 🔗](#page-0)


## 3.2.2 Load ofVM (L)

The load of a VMi is determined as the total length of tasks at time to service queue of VMi divided by the service rate of VMi at time t [36, 37]. In the sequel, load (L) can be calculated as below [36]: [URL 🔗](#page-0)

where Nt indicates total length of tasks on service queue and Sr shows service rate.

## 3.2.3 Network performance (N)

It is generally true that higher bandwidth and lower latency are both good.We compute the network performance between nodes a and b based on the bandwidth (in Mbits/s) and latency (in ms) as following [38]: [URL 🔗](#page-0)

TotalCost function that is given by Eq. (6) must be tailored, because it is defined as a weighted combination of three former parameters. It is obvious that the higher load of VM (L), lower capability of VM (C), and lower network performance (N) makes total cost higher. Therefore, capabilities ofVMand network performance have reverse effect. [URL 🔗](#page-0)

where W3, W4, and W5 are appropriate weights. It is not easy to optimize the value of weights; one idea could be that more general the factor, higher is the value of weight. Another logic is preference of user or influence given to a particular factor over the other [39]. In our work, the later idea has been applied. [URL 🔗](#page-0)

For W3, W4, and W5, we consider the weight vector to adjust performance ratio factors when choosing replica in order to meet the users’ satisfaction better. In other words, users can determine values based on their own goals and type of task such as a higher weight on more concerned performance which makes replication strategy adaptable. For example, when cloud tasks are computation intensive (i.e., need a strong computing capability), the capacity of VM should have a larger weight value.

Let consider that the weight vector is given by:

where, W3, W4, and W5 represent the weight vector of capacity of VM, load of VM, and network performance, and


In our simulation W3, W4, and W5 have equal value. Finally, if necessary file does not exist in the local site, then HRSmethod creates a list of candidate replica providers and selects a provider with the minimum TotalCost value based on Eq. (6). [URL 🔗](#page-0)

## 3.3 Replica replacement

When sufficient storage space is not available in the best site for storing new replica, one or more of the existing replicas should be deleted. HRS takes into account three parameters as number of accesses, cost, and the last time the replica was accessed. The number of access and the last time the replica was requested identify the probability of requesting the file again. It is obvious that a file with high cost value is not a good candidate for deletion. This is because, if a site requires that file in the future, we must pay high charge for replicating it again, and this is not economical. We consider the replication cost as Eq. (9) which is defined in [40]. [URL 🔗](#page-0)

- The higher replica size makes the replication cost higher.

- The lower bandwidth between provider and requester sites, the higher replication cost is.

- Propagation delay time depend on network traffic conditions. The greater delay time makes the replication cost higher. This parameter must be considered since the data may wait in network queues before submitted.

Where Size is size of replica, Bandwidth (x, y) is bandwidth between provider site x and requester site y, and PropagationDelayTime (x, y) indicates the time required to propagate the needed replica from provider x to the requester site y. We know that a closer site can quickly transfer replica.

HRS considers the fuzzy inference system with three input parameters (i.e., number ofaccesses, cost, and time interval between the current time and the last time the replica was accessed) and one output (i.e., Value). Figure 4 indicates fuzzy inference system for assigning the value to each replica. [URL 🔗](#page-0)

Fuzzy set theory can show the real-world knowledge in the face of uncertainty. It assigns a grade of membership to the fuzzy set. In fuzzy, different degrees of mem- bership are given, between 0 and 1.

A membership function maps the elements of universe in range of 0 to 1. HRS calculates the Value of all files that are available in the best site by a fuzzy function. Then it sorts list in ascending order of Value. It selects candidate files from list until enough space is available. We implement our proposed fuzzy function based on the Matlab Fuzzy Logic Toolbox. Matlab presents useful tools to propose and modify fuzzy inference systems. Figure 5 indicates the membership function plots of factors. [URL 🔗](#page-0)


*Fig. 4 Fuzzy system for determining the value of replica*

Value of replica

*Fig. 5 Input and output of fuzzy inference system*

The range of “Number of accesses” is from 0 to 55; it shows that maximum number of accessing a file is 55 in the simulation. ‘Replication cost’ ranges from 0 to 25, ‘Last access time interval’ ranges from 0 to 12×105. Consequently, output parameter (i.e., value of replica) ranges from zero to one. A replica that has lowest value is an appropriate candidate for deletion. Also 21 rules have been defined for the proposed fuzzy system. Table 4 describes some of the proposed fuzzy system rules. Flowchart of HRS algorithm is shown in Fig. 6. [URL 🔗](#page-0)


*Table 4 Examples of rules in fuzzy system*

## Rules

- If (Number ofAccesses is high) and (Replication Cost is high) and (Last Access Time Interval is low) then (Value ofReplica is very high)

- If (Number ofAccesses is high) and (Replication Cost is average) and (Last Access Time Interval is low) then (Value ofReplica is high)

- If (Number ofAccesses is high) and (Replication Cost is high) and (Last Access Time Interval is average) then (Value ofReplica is high)

- If (Number ofAccesses is low) and (Replication Cost is low) and (Last Access Time Interval is average) then (Value ofReplica is low)

- If (Number ofAccesses is low) and (Replication Cost is low) and (Last Access Time Interval is average) then (Value ofReplica is low)

*Fig. 6 Flowchart of HRS*

Before empirically comparing HRS with the related replication algorithms, we determine time complexity of the HRS algorithm as follows. Consider, a set of data nodes D  {D1,…, Dm}, a set of replicas R  {R1,…, Rn}.

- Replica Selection complexity is O(m). Since HRS finds the best node based on the TotalCost value.


A hybrid data replication strategy with fuzzy-based…

*Table 5 Parameters setting of cloud simulator*

| Type | Parameters | Value |
| --- | --- | --- |
| Data center | Number of data center | 20 |
|   | Number of host | 3–10 |
|   | Type of manager | Space_shared |
|   |   | Time_shared |
| Virtual machine | Total number of VMs | 60 |
|   | MIPS of processing element | 300–2500 |
|   | Number of processing element per VM | 2–5 |
|   | VM memory (RAM) | 512–2048 (MB) |
| Task | Total number of task | 100–1000 |
|   | Length of task | 100–500 |
|   | Number of processing elements requirement | 1–4 |

- Replica Placement complexity is O(m). Since HRS finds appropriate node with the highest Merit value.

- Replica Replacement complexity is O(n log(n)). Because HRS needs a sorting algorithm based on the value of replica.

Time complexity of MORM is O(mn). Consider Nc is clone number, N is initial population, and G is max generation. Fitness evaluation complexity is O(N). Suppres- sion operation complexity is O(N logN) since needs to sort the individuals. Mutation operation complexity is O(Ncmn). It is necessary to note that G, N, and Nc are prede- fined constants, which has nothing to do with the problem size.

Timecomplexity ofSWORD isO(N2).SWORDstrategy contains several processes so complexity of each process is analyzed. Complexity of Iterative HPA and Dense Subgraph-based algorithms are O(N) where N is the number of partitions. Complexity of Pre-Replication-based Algorithm (PRA) is O(VSE) where V is size of vertex set, E is size of edge set, and S is size of partition set. Complexity of Improved LMBR algorithm is O(N2).

## 4 Implementation environment

We have extended different classes of CloudSim toolkit to test replication algorithms. CloudSim is an event-driven simulator and contains four layers: SimJava, GridSim, CloudSim, and User code [41, 42]. It can provide the core components execution such as data centers, virtual machines, hosts, and applications. Table 5 shows the parameters’ setting of cloud simulator. The parameter of simulation is set based on the existing studies [43] to realistically represent a typical cloud environment. We set cloud system with 20 data centers and 100–1000 tasks in CloudSim. Each task is assigned based on the Poisson distribution after the previous task and number of files requirement is 1–5. The computation workload of the task is from 100 to500 Million Instructions. At the beginning of simulation, we randomly placed the primary copy of each data file in different sites. [URL 🔗](#page-0)


To simulate the system, startsimulation() method is called in the user code. This method calls other methods such as runStart(), runClockTick(), and runStop() in sequence. Characteristics of VMs and data centers have been defined in Vm class and DatacenterCharacteristics class, respectively. For task scheduling, we consider Time_shared strategy by CloudletSchedulerTimeShared class that extends CloudletScheduler class. In addition, we implement makeReplica() method in File class based on the proposed strategy.

## 5 Performance evaluation

We used average response time, mean latency, hit ratio, bandwidth consumption, num- ber of communications, storage usage, and load variance as performance metrics for analytical evaluation.

## 5.1 Average response time

If time interval between submission of task and return of results named as response time, then the average response time is calculated by Eq. (10): [URL 🔗](#page-0)

Here, ts jk(st) and ts jk(rt) are the submission time and the return time of the result for task k of the user j, respectively, and mj shows the number of the tasks for user j.

Comparison of the average response time for six dynamic replication strategies (Fig. 7) indicates that EDR strategy and HRS have the highest and lowest average response time, respectively. Since EDR strategy could not distribute the load of replica access verywell and so the average response time is increased. Furthermore, compared with SWORD and HQFR, the average response time of MORM reduces up to 24% and 32%, respectively. MORM algorithm considers various parameters, i.e., mean file unavailability, mean service time, load variance, energy consumption and mean access latency, to determine the relation between replica layout, number and theirs performances. As depicted in Fig. 7, PGSA strategy outperforms the EDR algorithm by up to 5% when number of task is 1100. This is because PGSA dynamically creates appropriate replicas in the system. [URL 🔗](#page-0)

## 5.2 Mean latency

As each file has multiple replicas, latency Li of file fi is obtained as follows [30]: [URL 🔗](#page-0)

where ri indicates number of replicas for file fi, si shows the size of file fi, decision variable θ(i, j ) has one value when the file fi in available on site Dj; otherwise, it has


*Fig. 7 Average response time by varying number of tasks*

zero value, A(i, j) indicates the percentage of requests coming from site Dj asking for fi, and Bj shows the bandwidth of Dj.

Figure 8 shows mean latency for different replication algorithms. We can see that HQFR behavior is more desirable than EDR, since EDR strategy neglects latency from optimization target. The experiments show that EDR strategy works properly only when the bandwidth of the network links is the unique criteria for the network. However, this is not a realistic condition in the cloud environment. Compared with HQFR and EDR, MORM strategy reduces the mean latency around 14 and 27%, respectively. The main reason is that MORM considers the mean access latency as one of the main optimization parameters.We can find that the mean latency ofHRS is 15% better than MORM. This phenomenon is because HRS selects the more appropriate sites by the consideration of network performance, CPU power, and load of site. [URL 🔗](#page-0)

## 5.3 Hit ratio

Hit ratio is as the proportion of total number of local file accesses to all accesses (i.e., local file accesses, total number of replications, and total number of remote file accesses). Figure 9 explains the hit ratio among different replication algorithms, when number of jobs is 1000. It is easy to see through the results of Fig. 9 that HRS has the highest value of hit ratio in comparison with other replication algorithms. In HRS strategy, total number of local accesses has been increased by storing replica in appropriate location based on the number of file access and centrality factor and avoiding unnecessary replication. Therefore, total number of replications and remote accesses has been decreased and consequently hit ratio has been increased. [URL 🔗](#page-0)


*Fig. 8 Mean latency based on varying number of files*

*Fig. 9 Hit ratio for six replication strategies*

## 5.4 Bandwidth consumption

Figure 10 represents the total bandwidth consumption of typically 6 replication strate- gies at various file size. CloudSim determines bandwidth usage by BwProvisioner class in the Cloudbus package. The bandwidth allocated and the utilized bandwidth are obtained by AvailableBw() and getUsedBw() methods, respectively. [URL 🔗](#page-0)

As shown, HRS is able to increase the performance especially in large number of size. When compared to the EDR, PGSA, HQFR, SWORD, and MORM algorithms, the HRS strategy performs better because of considering centrality and number of replica access in file placement. Most of the time, necessary files are available in the local site. Accordingly, the proposed strategy can be employed in distributed envi- ronment and improve the data access performance and bandwidth consumption. As


*Fig. 10 Total bandwidth consumption for six replication strategies*

depicted in Fig. 10, the bandwidth consumption of PGSA is lower by 24% compared to EDR algorithm. This is because PGSA takes into account status of network, load of node, and data history in replica selection step. It chooses the appropriate replica provider to respond to the data requester based on the idea of PGSA. [URL 🔗](#page-0)

## 5.5 Number of communications

The next evaluation is planned to study the number of communication for HRS in comparison with other replication methods. It is crucial to reduce the total number of communications for decreasing the data access latency and preventing the bandwidth congestion. Comparing the curves shown in Fig. 11, we can find that HRS outperforms by 8% over MORM and by 19% over SWORD. HRS stores replicas in the best site (i.e., best site that has the great number of access and most central) based on the temporal and geographical locality concepts. Consequently, most of necessary files are locally available and so number of communications is decreased. [URL 🔗](#page-0)

## 5.6 Storage usage

We know that various methods proposed for data replication may lead to different storage usage. The storage usage for replicas by replication schema can be expressed as in Eq. (11): [URL 🔗](#page-0)

Storage is undoubtedly one of the key elements in cloud environment, so beneficial information can be provided by monitoring the use of storage resources. This can


*Fig. 11 Total number of communications for six replication strategies*

be valuable and useful in proposing an efficient replication methodology from two important points of view: firstly, the goal may be the reduction of storage usage since storage cost is proportional to the amount being consumed. Secondly, the goal may be maximization of storage usage since cost of storage is constant.

Figure 12 depicts the obtained storage usage for the current algorithms. InMORM, instead of storing replicas in many sites, they can be placed in the best location so that the storage usage can be reduced. We can see that HQFR strategy has higher storage usage about 17% compared to the SWORD strategy. This is because SWORD places replica basis on the workload and uses the partitioning techniques that reduce the average query span and resource consumption. HRS strategy consumes almost half of the storage capacity used by EDR, while EDR method fills more than half of the entire storage capacity available in the cloud environment. This is because HRS only keeps the critical files based on the value assignment to each file. Fuzzy rules select replica(s) with low value for replacing when storage space of a site is full. [URL 🔗](#page-0)

## 5.7 Load variance

The load balancing technique is used for distributing the load (computing tasks) among different resources (nodes) in the system. Kim et al. [44] used the load variance as the metric for load balancing. [URL 🔗](#page-0)

Usually, load balancing within the network depicts by load variance, i.e., the stan- dard deviation of data nodes in the cloud storage. The higher value of variance shows the higher degree of deviation and the lower value of variance indicates the lower degree of deviation. Therefore, variance can be used to measure the degree of load balancing. The lower value of load variance shows the lower value of degree devia- tion and the greater degree of load balancing. While the higher value of load variance shows the higher value of degree deviation and the lower for degree of load balancing.


*Fig. 12 Storage usage for six replication strategies*

*Fig. 13 Variation of load variance based on different number of files*

When the load becomes totally balanced (i.e., in the best case), the load variance is zero.

Form Fig. 13, HRS reduces load variance by an average of 30 and 34% compared with the SWORD and HQFR strategy, respectively. This can be related to the ability of HRS in replica selection among the large number of providers based on the load of site and I/site capability. [URL 🔗](#page-0)


## 6 Conclusion

Cloud computing system is getting more and more attentions as a novel trend in management of data. Data replication technique has been widely used to improve data retrieval in cloud.To reduce the response time ofapplications, provide high availability, and make system load balancing, a new replication strategy (HRS) is proposed. To reduce response time (over 25%), the sites are chosen according to the centrality and number of replica access in replica placement step. Then, it combines the network performance and site capability (e.g., CPU process capability, and communication bandwidth) in replica selection process. However, due to restricted storage space, a replica replacement method is necessary to make the dynamic replica management efficient. The replica is selected for deletion based on its value, which is assigned using fuzzy inference system. HRS not only guarantees availability, but also reduces access latency, and keeps the whole storage system stable. From the experiment results with CloudSim, we find that HRS can achieve a good improvement ofperformance in terms of average response time, effective network usage, hit ratio, load variance, number of communications, bandwidth consumption, and storage usage over former similar works. In future, we want to extend this kind of load balancing for workflows with dependent tasks. We intend to use an energy consumption model to reduce resource wasting, by balancing the quality of service requirements.

## References

- 1. Liu Q, Wang G, Liu X, Peng T, Wu J (2017) Achieving reliable and secure services in cloud computing environments. Comput Electr Eng 59:153–164

- 2. Jakóbik A, Grzonk D, Palmieri F (2017) Non-deterministic security driven meta scheduler for dis- tributed cloud organizations. Simul Model Pract Theory 76:67–81

- 3. Mishra SK, Puthal D, Sahoo B, Jena SK, Obaidat MS (2017) An adaptive task allocation technique for green cloud computing. J Supercomput 74(1):370–385

- 4. Wang T, Zhiyang S, Yu X, Mounir H (2014) Rethinking the data center networking: architecture, network protocols, and resource sharing. IEEE Access 2:1481–1496

- 5. Wang T, Mounir H (2016) Presto: Towards efficient online virtual network embedding in virtualized cloud data centers. Comput Netw 106:196–208

- 6. Foster I, Zhao Y, Raicu I, Lu S (2008) Cloud computing and grid computing 360-degree compared. In: Grid Computing Environments Workshop, GCE’08, pp 1–10

- 7. Rajkumar B, Rajiv R, Calheiros RN (2009) Modeling and simulation of scalable cloud computing environments and the CloudSim toolkit: challenges and opportunities. High Perform Comput Simul 1:1–11

- 8. Ghemawat S, Gobioff H, Leung S (2003) The Google file system. In: ACM Symposium on Operating Systems Principles, pp 29–43

- 9. Mansouri N, Javidi MMA (2017) survey of dynamic replication strategies for improving response time in data grid environment. AUT J Model Simul 49:239–264

- [10. Borthakur D (2007) The Hadoop distributed file system: architecture and design. http://hadoop.apach e.org/common/docs/r0.18.3/hdfs_design.html](http://hadoop.apache.org/common/docs/r0.18.3/hdfs_design.html)

- 11. FengD,QinL(2006) Adaptive object placement in object-based storage systemswith minimalblocking probability. In: Proceeding of the 20th International Conference on Advanced Information Networking and Application [URL 🔗](http://hadoop.apache.org/common/docs/r0.18.3/hdfs_design.html)


- 12. López-Pires F, Barán B (2017) Many-objective virtual machine placement. J Grid Comput 15(2):161–176

- 13. Tao M, Ota O, Dong M (2017) Dependency-aware dependable scheduling workflow applications with active replica placement in the cloud. In: IEEE Transactions on Cloud Computing, p 99

- 14. Mansouri N, Kuchaki Rafsanjani M, Javidi MMDPRS (2017) A dynamic popularity aware replication strategy with parallel download scheme in cloud environments. Simul Model Theory 77:177–196

- 15. Rahman RM, Barker K, Alhajj R (2006) Replica placement design with static optimality and dynamic maintainability. In: Sixth IEEE International Symposium on Cluster Computing and the Grid, pp 434–437

- 16. Shvachko K, Kuang H, Radia S, Chansler R (2010) The Hadoop distributed file system. In: IEEE 26th Symposium on Mass Storage Systems and Technologies, pp 1–10

- 17. Mansouri N, Dastghaibyfard GHA (2012) dynamic replica management strategy in data grid. J Netw Comput Appl 35:1297–1303

- 18. Ibrahim IA, DaiW, Bassiouni M (2016) Intelligent data placement mechanism for replicas distribution in cloudstorage systems. In: IEEE International Conference on SmartCloud (SmartCloud), pp 134–139

- 19. Mansouri N, Dastghaibyfard GH, Mansouri E (2013) Combination of data replication and scheduling algorithm for improving data availability in data grids. J Netw Comput Appl 36:711–722

- 20. Mansouri N, Dastghaibyfard GH (2013) Enhanced dynamic hierarchical replication and weighted scheduling strategy in data grid. J Parallel Distrib Comput 73:534–543

- 21. Mansouri N (2016) Adaptive data replication strategy in cloud computing for performance improve- ment. Front Comput Sci 10(5):925–935

- 22. Sun DW, Chang GR, Gao S, Jin LZ, Wang XW (2012) Modeling a dynamic data replication strategy to increase system availability in cloud computing environments. J Comput Sci Technol 27:256–272

- 23. Chang RS, Chang HP (2008) A dynamic data replication strategy using access-weights in data grids. J Supercomput 45(3):277–295

- 24. KimYH, Jung MJ,LeeCH(2010) Energy-aware real-time task scheduling exploiting temporal locality. IEICE Trans Inform Syst 93(5):1147–1153

- 25. Sun DW, Chang GR, Miao C, Jin LZ, Wang XW (2013) Analyzing modeling and evaluating dynamic adaptive fault tolerance strategies in cloud computing environments. J Supercomput 66:193–228

- 26. Zhang B, Wang X, Huang M (2014) A PGSA based data replica selection scheme for accessing cloud storage system. Adv Comput Archit 451:140–151

- 27. Ding X, You J (2011) Plant growth simulation algorithm. Shanghai People’s Publishing House, Shang- hai, pp 1–59

- 28. Li B, Song SL, Bezakova I, Cameron KW (2013) EDR: An energy-aware runtime load distribution system for data-intensive applications in the cloud. In: IEEE International Conference on Cluster Computing

- 29. Lin JW, Chen CH, Chang JM (2013) QoS-aware data replication for data-intensive applications in cloud computing systems. IEEE Trans Cloud Comput 1:101–115

- 30. Long SQ, Zhao YL, Chen W (2014) MORM: a multi-objective optimized replication management strategy for cloud storage cluster. J Syst Architect 60:234–244

- 31. Luo Y, Li R, Tian F (2004) Application of artificial immune algorithm to function optimization. Fifth World Congr Intel Control Autom 3:2248–2252

- 32. Lou C, Zheng M, Liu X, Li X (2014) Replica selection strategy based on individual QoS sensitivity constraints in cloud environment. Pervasive Comput Netw World 8351:393–399

- 33. Kumar KA, Quamar A, Deshpande A, Khuller S (2014) SWORD: workload-aware data placement and replica selection for cloud data management systems. VLDB J 23:845–870

- 34. Newman MN (2009) An introduction. Oxford University Press, Oxford

- 35. Saleh A, Javidan R, Fatehikhaje MT (2015) A four-phase data replication algorithm for data grid. J Adv Comput Sci Technol 4:163

- 36. Bhardwaj T, Chander Sharma S (2018) Fuzzy logic-based elasticity controller for autonomic resource provisioning in parallel scientific applications: a cloud computing perspective. Comput Electr Eng. https://doi.org/10.1016/j.compeleceng.2018.02.050 [URL 🔗](https://doi.org/10.1016/j.compeleceng.2018.02.050)

- 37. Dhinesh Babu LD, Venkata KP (2013) Honey bee behavior inspired load balancing of tasks in cloud computing environments. Appl Soft Comput 13:2292–2303 [URL 🔗](https://doi.org/10.1016/j.compeleceng.2018.02.050)

- 38. Pérez JM, García-Carballeira F, Carretero J, Calderón A, Fernández J (2010) Branch replication scheme: a newmodel for data replication in large scale data grids. Future Gener Comput Syst 26:12–20


- 39. DasguptaK, Kumar Mondal J, Dutta P (2013) Optimized video steganography using genetic algorithm. Int Conf Comput Intell Model Tech Appl 10:131–137

- 40. Saadat N, Rahmani AM (2012) PDDRA: a new pre-fetching based dynamic data replication algorithm in data grids. Future Gener Comput Syst 28:666–681

- 41. Calheiros RN, Ranjan R, Beloglazov A, De Rose CAF, Buyya R (2011) CloudSim: a toolkit for modeling and simulation of cloud computing environments and evaluation of resource provisioning algorithms. Softw Pract Exp 41:23–50

- 42. Howell F, Mcnab R (1998) SimJava: a discrete event simulation library for java. In: Proceedings of the First International Conference on Web-Based Modeling and Simulation

- 43. Barroso LA, Clidaras J, Holzle U (2013) The datacenter as a computer: an introduction to the design of warehouse-scale machines, vol 2. Morgan and Claypool Publishers, San Rafael

- 44. Kim YJ, Kim BK (2000) Load balancing algorithm of parallel vision processing system for real-time navigation. In Proceedings of 2000 IEEE/RSJ International Conference on Intelligent Robots and Systems, Takamatsu, Japan, pp 1860–1865

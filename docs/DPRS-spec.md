74 Int. J. Information Technology and Management, Vol. 18, No. 1, 2019

### Dataset replica placement strategy under a response

### time constraint in the cloud

### Xiuguo Wu* and Wei Su

School of Management Science and Engineering, Shandong University of Finance and Economics, SDUFE, No. 7366, Erhuan East Road, LiXia District, Jinan, 250014, China Email: xiuguosd@163.com Email: echorainbow@msn.com *Corresponding author

Abstract: In cloud computing environment, especially data-intensive systems, large amounts of datasets are stored in distributed data centres, and are often retrieved by users in different regions. To reduce the users’ response time, replicating the popular datasets to multiple suitable data centres is an advisable choice, as tasks can access the datasets from a nearby site. Nevertheless, the dataset replicas’ suitable storage placement selection is still an important issue that should be solved urgently from the response time constraint view, for the reason that too many replicas are infeasible in practice. In this paper, we first propose a comprehensive dataset response time estimation model, then present a replica placement model based on Steiner tree. After that, an approximate replica placement algorithm under a response time constraint in the cloud is given using Kruskal minimum spanning tree. At last, a practical and reasonable performance evaluation is designed and implemented. Both the theoretical analysis and simulations conducted on general (random) datasets show the efficiency and effectiveness of the proposed strategy in the cloud.

Keywords: cloud computing; cloud storage; data; replicas placements; response time constraint; wait access latency; average wait access latency; data transfer time; Kruskal minimum spanning tree; Steiner tree.

Reference to this paper should be made as follows: Wu, X. and Su, W. (2019) ‘Dataset replica placement strategy under a response time constraint in the cloud’, Int. J. Information Technology and Management, Vol. 18, No. 1, pp.74–92.

Biographical notes: Xiuguo Wu is an Associate Professor in the School of Management Science and Engineering, Shandong University of Finance and Economics, SDUFE. His main research interests include data storage in cloud computing environment and scientific workflow technology.

Wei Su is a Lecturer in the School of Management Science and Engineering, Shandong University of Finance and Economics, SDUFE. Her main research interests include access control in cloud computing environment and migrating workflow technology.

This paper is a revised and expanded version of a paper entitled ‘Data set replica placement strategy under a response time constraint in the cloud’ presented at The Ninth International Conference on Management of e-Commerce and e-Government (ICMeCG), Jinan, China, 29–30 October 2016.

Copyright © 2019 Inderscience Enterprises Ltd.

Dataset replica placement strategy under a response time constraint 75

1 Introduction

In recent years, huge collections of datasets have been popular with the development of digital sensors, communications, computation and storage devices (Foster et al., 2008). In this way, how can we ensure the users’ requests response as soon as possible, in order to meet the system requirements under the premise that massive datasets movements appear more and more frequently in the cloud? That is to say, one of the major problems to be solved urgently is to predicate the dataset's response time, which is defined as the time that elapses from when a service request for a dataset until it receives the complete dataset. Some researchers have done much to address this problem in recent years, and measures have been proposed in cloud storage systems (Grossman et al., 2009; Mell and Grance, 2011; Amazon Elastic computing Cloud, 2016; Ghemawat et al., 2003). Also there is a consensus that response time is a crucial factor that influences the replica placements and thus the task scheduling. Nevertheless, it is still not an easy task to estimate the data response time accurately in the cloud storage system. In addition, the response time is estimated by considering the data transfer time only. That is to say, the data transfer time that mainly depends on the network bandwidth, is considered to be exclusive to predict the response time in the previous studies, but the transfer time alone is not sufficient. Furthermore, there are at least two other factors playing an important role in estimating dataset response time: storage latency and write/read time, except for transfer time. Therefore, in this study, we focus on estimating the response time accurately, which is used to be an important foundation for dataset replica placement in the cloud. And then, we will propose a replica placement strategy under a response time constraint. This study has achieved the following objectives: 1 propose models for estimating the users’ dataset requests response time 2 present a dataset placement model under a response time constraint based on Steiner tree 3 provide an approximate replicas placements algorithm based on Kruskal minimum spanning tree 4 give theoretical analysis and simulations conducted on random datasets in the cloud. The rest of paper is structured as follows: Section 2 presents related works; Section 3 gives a comprehensive response time estimation model, including transfer time, access latency and write/read time; Section 4 describes a replica placement model under a response time constraint, and then proposes an approximate algorithm using minimum spanning tree. Section 5 addresses performance evaluations and simulations; conclusions and future works are given in Section 6.

2 Related works

In this section, two broad categories of related works are presented: data replica placement technology and dataset response time in the cloud environment.

76 X. Wu and W. Su

2.1 Data replica placement technology

Data replica technology is one important measure in order to get high availability, high tolerance and high efficiency access to cloud data centres (DC), and has been widely used in distributed systems. With the advancement and development of various technologies, dataset replicas and their management have been studied in many works, which are referenced and adopted. Table 1 summarises the related replica technologies in recent years. From Table 1, we can conclude that there are two main types of approaches: static and dynamic. The static replica selection approaches select the nearest replica to the user according to some static metric such as the geographical distance in miles, topological distance in number of hops, and HTTP request latency (Li et al., 2015). The dynamic replica selection approaches have emerged to improve the estimation of the expected user response time based on network factors such as round-trip time, network bandwidth, and server request latency (Qiu et al., 2015; Grace and Manimegalai, 2016). Table 1 Comparisons of replicates technology in distribute system

Model Replication technology Descriptions GFS (ShvachkoStatic distributed High fault tolerance is maintained because et al., 2010)replicas are placed on three different data nodes. D2RS (Sun et al.,Dynamic replicaBased on system availability and data 2012)strategypopularity. CDRM (Wei et al.,Dynamic distributed Based on capacity and location according to 2010)workload changing and node capacity. Dynamic blockDynamic centralised Proposed several constant-factor local search replication (Zhangapproximation algorithms, and present a et al., 2015)dynamic replica distribution mechanism that implements the algorithms in HDFS. Load balancingDynamic centralised Proposed a new placement policy that split the (Dai et al., 2016)nodes in to three different sections and run an algorithm to distribute the replicas on the three sections across all cluster nodes. p-median (Li et al.,DynamicFound p replica placements sites with 2015)maintainabilityminimum distance.

2.2 Response time in the cloud

There are some studies focused on the best replica placement with minimum response time in recent years, and the main difference among these studies is how to estimate the response time, because the response time cannot be computed in advance (Deng and Shi, 2016; Wang et al., 2012), rather there are some criteria that play a role in estimating the response time. Shi et al. (2016) have considered historical data information about storage latency and data transfer time as a predictor of future time, but future prediction for storage access latency is not accurate, because the grid resources, such as storage, are changed and upgraded over time. Three techniques: uniform technique, greedy technique and assigning with predication technique, have been proposed in retrieving the required replica (Almuttairi et al., 2013).

Dataset replica placement strategy under a response time constraint 77

Obviously, the above mentioned approaches that use the parallel download are feasible if and only if there are many replicas and few requests, but this kind of scenario has rarely happened in the reality of clouds. However, the most common case of scenario often occurred when there are many requests and only a few replicas, because storage capacities and other cloud resources are limited. Nevertheless, the storage request queue and the storage media speed were not of concern as factors that influence the response time in previous works. In this paper, we have considered these two factors for the following reasons: 1 The datasets are stored in storage media with different write/read speed. Each storage media has a specific speed which can be measured as a write/read data transfer rate. For example, the hard disk is faster than the tape drive and the tape drives have many types with different speeds. 2 Most of the storage media such as the mass storage media can serve only one request at a time and thus the other incoming requests must wait for the current request to be served. In the cloud computing environment, the number of requests to a high capacity data storage device can be thousands, thus each request is queued in a storage handler queue.

3 Response time estimation model

In this section, we will propose a response time estimation model in the cloud environment, including DCs, data and response time models.

3.1 Models of the cloud computing environment

There are some distributed DCs in cloud environment for data storage, and different DCs are equipped with different storage devices, therefore indicating different performance, because of diverse storage system architectures, network connectivity features, and load characteristics. Figure 1 depicts the architecture of a cloud computing environment with eight DCs.

Figure 1 Architecture of cloud computing environment (see online version for colours)

78 X. Wu and W. Su

Definition 1: Data centre Each DC dci can be described as a four-tuple (dci, sp i, ts i, vs i), where 1 dci is the identifier of DC, which is a unique identification in cloud. 2 sp i means the average storage price of data, determined by the cloud storage service provider. 3 ts i is the total space of DC dci, with unit TB. 4 vs i is the size of vacant space on DC; means the extra storage capacity of dci. In the cloud environment, different types of storage services are provided for application datasets placements. And each dataset involves a number of properties. Definition 2: Dataset (dm). Dataset dm in the cloud computing environment can be described as a four-tuple (d m, s i, s p, UF), where 1 d m is the identifier of dataset, and is unique in the whole cloud environment. 2 s i is the size of dataset. 3 s is the store place, s ∈ DC. p p 4 UF is usage frequency in a certain period.

3.2 Dataset response time model

Evidences have shown that significant variations of application response time are caused by some factors, such as access latency, transfer time, and write/read speed, etc. (Almuttairi et al., 2013). Thus the response time includes the data transfer time between the two DCs, the storage access latency for serving the current request, and the wait latency before being served. Definition 3: Response time of dataset request (T ). di Response time for requesting a dataset d can be stated as: T= T + T + T , where i di w w/r trsf 1 T represents the total response time of dataset d . di i 2 T is wait access latency on a DC from request arrival until start to be served. w 3 T is write/read time for dataset d w/r i 4 T is data transfer time from source DC to the destination. trsf In the following part, we will discuss each element in the response time model respectively in order. In the cloud environment, one dataset transfer request arrives on a DC, and then is put into a queue immediately. However, each DC has many requests and it serves only one request at a time. The current request needs to wait a period of time T until all prior w requests have been finished under a first-come-first-served rule. Figure 2 describes the architecture of a request queue. And each DC maintains its own requests queue during the running process.

Dataset replica placement strategy under a response time constraint 79

Figure 2 Data transfer requests queue model (see online version for colours)

In this way, we use T representing the delay time for the DC to serve other requests, w which is heavily reliant upon the DC’s system performance, such as CPU speed, RAM size, the number of requests during a period of time, etc. Queuing theory is a subject that studies the waiting time, lengths and other properties of queues. In such a circumstance, the request wait access latency can be regarded as a queue model (Bandic et al., 2015). Definition 4: Wait access latency (T ) w The whole process that the DC receives the data transfer request, then put into requests queue for future transportation, can be represented by a queue model: M/M/1/∞/∞, where 1 the first M represents data transfer requests arrivals frequency, which is determined by a Poisson process distribution 2 the second M represents service time, which is determined by an exponential distribution 3 one means the number of CPU or a single server 4 the first ∞ is infinite, means the number of permitted waiting requests is abundant 5 the second ∞ means the number of requests is infinite. More generally, the DC wait access latency is considered to be a stable state over the long-term. Then, we can calculate the average wait access latency during a period of time. Theorem 1: Average wait access latency T of DC dccan be described as follows: w m

ρm Tw = , where λm  −μm

λm 1 ρm = ,represents the data transfer requests frequency (density). μm

2λm means dataset requests arrival rate; and then 1/λm means the average interval between two successive requests. 3 μm means service rate per DC, and then 1/ μm means service time per data transfer request. Referenced from Little’s formula and noted that the arrival and service pattern, it is not difficult to prove the above theorem (http://en. wikipedia.org/wiki/Little’s law).

80 X. Wu and W. Su

When reading dataset from a DC, the processor needs to wait for the dataset to be read (the same goes for writing). This is the time required for a computer to process a data request from the processor and then retrieve the required data from the storage device. Since hard disks are mechanical, it is necessary to wait for the disk to rotate to the required disk sector (http://www.cmdln.org/2010/04/22/analyzing-io-performance-in- linux/). Therefore, the increase in volume of data file size causes the write/read time to be longer. On the other hand, different storage media have different speeds in write/read operations. And in most cases, the time of disk write/read operation can be measured by hard disk rotational speed, as many researchers have proven (Robins and Zelikovsky, 2000). Definition 5: Time of disk write/read (T w/r). Time of disk write/read for a dataset d i is proportional to its data size, and inversely with the hard disk rotational speed to some extent. We can calculate the time of disk write/read by the following equation:

d si . i Tw r/=×γ, where RS

1 T w/r is the time of disk write/read 2 d i.s i is the size of dataset d i 3 RS is the hard disk rotational speed with unit rpm 4 γ is a proportional control coefficient, used to adjust the proportion value and unit of T w/r. For example, suppose the data size is 1 G, and the hard disk works with 5,400 rpm, then the disk read time is nearly ten seconds with the γ = 55. Data transfer time represents the whole time from source DC to its destination via a wide area network. It is usually represented by showing how fast the device can send a certain amount of data. For example, 50 kilobytes per second, which can be abbreviated to 50 kB/s. The factors that determine the length of data transfer time usually involve the size of the dataset and the network bandwidth. Definition 6: Dataset transfer time (T trsf) Dataset transfer time (T trsf) is proportional to its data size, and inversely with the bandwidth (data transfer ratio). We can calculate the time as follows:

d si . i T = ×ξ, where trsf bandwidth(dc j , dc )k

1 T trsf represents single dataset transfer time 2 d i.s i is the size of dataset d i 3 bandwidth(dcj, dck) is the network transport capacity between DC dcj and dck 4 ξ is an adjustment coefficient, used to adjust the proportion and unit of T trsf. There is usually more than one path between DCs dci and dcj during dataset transfer process, which leads to different transfer times. In order to simply the problem, the time

Dataset replica placement strategy under a response time constraint 81

of single dataset transfer always means the minimum transfer time among all the possible transfer paths in this study. Definition 7: Total response time of dataset don DC dc. i m The total response time of one dataset d on DC dcis the sum of all dataset response i m times, and can be described as follows:

k di di

## T = ∑( x × Tdi  × ηti ×T), where

dcm dcm m=1

di 1 T is the total response time of dataset d i on DC dcm dcm 2 k means the number of datasets in DC dc m

didi 3 x ∈ {0, 1},is a variable, where x is set to one if DC dcm stores a replica of dcmdcm dataset d ; else zero i 4 Tis the one dataset response time, as defined in Definition 6 di 5 ηis usage frequency of dataset during a period of T ti 6 T is the time span, representing a period of one day in this paper. In this way, we can calculate the average response time and maximum response time in cloud environment based on the above definitions, indicating the necessity of reducing the response time of dataset requests, therefore improving system performance.

4 Dataset replica placement algorithm under a response time constraint

In this section, we first present a replica placement model in the cloud, then propose an approximate algorithm for replica placements under a response time constraint.

4.1 Replica placement model in the cloud

Figure 3 describes an expected replicas distribution in the cloud, where there are eight DCs, and the grey square represents the DC with replica, while the white square represents the DC without replica, needing to transfer from grey one. It can be concluded that all the DCs are divided into three different parts, and each part has only one DC with replica (or primitive data). Also, the DC without replica always selects the dataset with the shortest path linked to a grey square. In this way, we will discuss the transformation from replica placement distribution to graph theory using the following rules: 1 each DC dci can be regarded as a vertex vi, and all the vertices constitute a vertex set V 2 each connection between two DCs can be converted to an edge e, and all the edges constitute an edge set E

82 X. Wu and W. Su

3 the transfer time between two DCs can be regard as the weight of an edge, called a + function f: e → Z 4 the vertices from DC with replica constitute subset P, P ⊆ V. Then, the primitive problem can be converted into a graph G(V, E, f), and a subset P, P ⊆ V. The question is how to find a tree T from graph G, where

1 P ⊆ VT ⊆ V, ET ⊆ E

## 2 min ⎛∑f e( )  +∑f v( ) .⎞

⎜ ⎟ ⎝ e∈ E T  e V∈T⎠

The question is the same as a well-known Steiner tree problem (STP) if we omit the wait latency and write/read time on each DC (vertex). Regretfully, STP is known to be NP- hard even in the Euclidean or rectilinear metrics (http://www.cmdln.org/ 2010/04/22/analyzing-io-performance-in-linux/), that is, there does not exist a polynomial-time exact algorithm for it, unless P = NP. Up to now, the best solution for STP is a 1.55-approximation one given by Robins and Zelikovsky (2000). In this way, the problem of replica placements with minimum response time is also an NP-hard problem.

Figure 3 Expected replica placement in the cloud (see online version for colours)

data center with replica data center without replica

dc dc

dc1dc8 dc

dc7 dc2 dc

4.2 Replica placement strategy under a response-time constraint

In this sub-section, we propose a replica placement strategy under a response-time constraint, which include two phases: 1 transform the weight from edges to vertices 2 present an approximate algorithm using Kruskal minimal spanning tree. In the cloud environment, each DC has two properties: users (tasks) access frequency and write/read speed, which cause the access time latency Tw and write/read time T w/r respectively. However, in order to find the suitable place to store replicas, the time

Dataset replica placement strategy under a response time constraint 83

expended on the DCs, such as Tand T, should be apportioned with their adjacent w w/r edges. Suppose there are two DCs dcand dc, and their access times (including wait access p q latency and write/read time) for dataset d in a certain period are T(dc) and T(dc) i wpwq respectively. Then the new weight of edge between dcand dccan be calculated using p q the following formula: ( T w / r dcp(  ) + T w dcp(  ) )( T w / r dcq(  ) +Tw dcq( ))

### w′  ( dcp  , dcq  ) = w dc( p  , dcq ) + + (1)

deg dc( p  )deg dc( q)

where

1 w dc′(   p , dcq)is the new edge weight between dcp and dcq

2 w(dc, dc) is the old edge weight pq 3 T and T are write/read time from hard disk on DCs dcand dc w/r(dcp) w/r(dcq) p q respectively 4 T and T are wait access latency on DCs dcand dcrespectively w(dcp) w(dcq) p q 5 deg(dc) and deg(dc) means the number of connections between DC dcand dc pqp q respectively. The main idea of transition from vertices to edges is to assign the wait access latency and write/read time of each DC to adjacent edges. Algorithm 1 describes how to move the weight of vertices to edges. Algorithm 1 Move the weight of vertices to edges

Input: Graph G(V, E, f(e), f1(v), f2(v)); Output: Graph G V′(   ′,  E ′, f e( ))

(1) Initialise an edge-weighed graph G V′(   ′,  E ′,  f e( ))by setting V ′ = V , E ′=E;

(2) For each edge e(v , v ) in Graph G′ do ij (3) Assign the weight of this edge using Formula (1); (4) ( f ( v ) +f ( v))( f ( v ) +f ( v)) 1 i 2 i1 j 2j Set f ′(  vi  , v j ) = f v( i  , v j) + +; deg( vi  ) deg( vj)

(5) EndFor (6) End.

+ + In Algorithm 1, f(v) : v → Zmeans the wait access latency function; and f(v) : v → Z, means write/read time function, indicating the static time taken on the DCs. It is obvious that there is only one loop in Algorithm 1, and the number of loop times is the same as number of edges. Also, the graph is represented using a two-dimensional matrix, and the degree of each vertex can be acquired through calculation using adjacent matrix in O(n). Therefore, the time complexity of Algorithm 1 is O(n). Subsequently, we will present an approximate algorithm for replicas placements strategy under a response-time constraint. The algorithm will solve the problem using

84 X. Wu and W. Su

Kruskal minimal spanning tree algorithm for general-purpose source. Approximate algorithm is shown in Algorithm 2. Algorithm 2 Approximate algorithm for replica placements based on response-time constraint (RPRC)

Input: G(V, E, f(e)); vwith primitive dataset di; Output: Subset Sof V for Replicas store CRD (1) Initialise a virtual vertex setV′ by settingv′ =vif and only ifv∈V; i   i  i (2) Initialise an edge-weighed graphG′′ =(V′′, E′′, f′′( ))eby setting:V′′ =VUV′;

(3) Adding edges by setting: any vertexv∈V′,v∈V, adding edge (v,v) and (v,v) i   j  i jj i respectively; (4) Set the weight of edges (v, v) with the shortest path in graph G corresponding vertex; ij (5) Generate a minimum spanning tree T of G″ using Kruskal’s algorithm. (6) For each vertex v ∈ V ′do i (7) Delete the vertex and adjacent edge from T whose degree is 1; (8) EndFor (9) For each vertexv∈Vdo i (10) If vi ′ ∈ V′then (11) Delete v and its adjacent edges from V; i (12) EndIf (13) EndFor (14) For each vertex v ∈ V do i (15) If∃(v,v),v∈V′and (v,v),v∈V′Then i  j  j   i  k k (16) Delete the edge with larger weight (17) EndIf (18) EndFor (19) S={v}UV′; CRD  1 (20) Output S. CRD

Algorithm 2 first creates a set of virtual vertices as candidate replica store places, and then constructs a spanning graph G″. However, there are only edges from primitive vertices to candidate vertices, where the weight means the response time to destination DC. Line (6) generates a minimum spanning tree based on graph G″, and Line (8) deletes the vertices with lower degree. Also, Line (8) mainly deletes the redundant vertices, for example, v2 cannot coexist with v2′  .If there is more than one edge from vi to v′j ,that means the data have more choices, we need to delete the edges with larger weight as in Line (16). Vertex vis the source place, so it must be embraced in set S as in 1 CRD Line (19). Here, we will analyse the time complexity of Algorithm 2. A simple implementation using an adjacency matrix graph representation and searching an array of weights to find the minimum weight edge to add requires O(|V|) running time. Kruskal algorithm is a greedy algorithm that runs in polynomial time, whose time complexity is O(n), n is the

Dataset replica placement strategy under a response time constraint 85

number of vertices. In the other steps, such as Line (7) and Line (10), the time complexity is O(n). So, the total time complexity of RPRC is O(n).

5 Performance evaluation

In this section, we will first analyse the factors that affect the dataset response time in cloud environment, and then discuss the whole procedures of RPRC algorithm using an example. Next, we simulate the response time constraint replica placement strategy, and compare RPRC with other dataset replica placement strategies.

5.1 Factors analysis affecting the dataset response time

In this section, we will test the factors that affect the dataset response time in cloud environment, including access wait access latency, write/read process and datasets transfer.

5.1.1 Wait access latency T w Generally, each DC usually receives more than one request for data process, which is very common in real world. The operating system schedules the write/read requests in order to enhance system performance. Access wait latency lasts from when the request arrives until the system write/read begins. Scheduling can be implemented by maintaining a queue of requests for the device. Thus, the number of requests and the write/read speed in queue play a major role in the average response time experienced by application. Figure 4 shows relationship between the approximate response time and wait latency time under a certain workload with different numbers of dataset requests. We can see that the changes of response time are always consistent with the fluctuation of wait latency with different numbers of dataset requests.

Figure 4 Comparison of response time and access wait latency with different numbers of dataset requests (see online version for colours)

90Wait Latency Time Response time

Time

10 30 50 70 90 110 130 150 170 190 Number of Data Requests

86 X. Wu and W. Su

5.1.2 Write/read time T w/r Generally, time will be taken to find the requested dataset and move it to the transfer line since the operating system starts to process data transfer request. As discussed, there is a percentage of response time caused by write/read process in the total dataset response time. Figures 5(a) and 5(b) describe the different hard disk speeds with 5,400 rpm and 7,200 rpm respectively. As can be seen, the results of simulations show that the response time and write/read time become greater simultaneously with an increasing number of dataset requests. Furthermore, the differences between the response time and write/read time do not exceed the reasonable bounds with different data sizes.

Figure 5 Comparisons of response time and write/read time, (a) RS = 5,400 rpm (b) RS = 7,200 rpm (see online version for colours)

I/O time Response time

Time

10 30 50 70 90 110 130 150 170 190 Number of Data Requests

(a)

140I/OtimeResponsetime

Time

10 30 50 70 90 110 130 150 170 190 Number of Data Requests

(b)

Dataset replica placement strategy under a response time constraint 87

5.1.3 Transfer time Ttrfs Transfer time represents the time taken during data transmission via a wide area network, which depends on the network bandwidth and the size of dataset. Typically, with the as the transfer distance and data size increase, the transfer state is sustained over the long- term, which leads to a long response time. Therefore, transfer time is an important part of whole response time, which usually fluctuates from time to time owing to outside factors. Figure 6 shows the comparison between total response time and transfer time with different numbers of dataset requests. And we can see that the difference between response time and transfer time is basically fixed in a certain range. The reason is that data transfer process is a main activity in the whole process.

Figure 6 Comparison between response time and dataset transfer time (see online version for colours)

Transfer time Response time

Time

10 30 50 70 90 110 130 150 170 190 Number of Data Requests

5.2 Analysis of replica placement algorithm under a response-time constraint

In this subsection, we will analyse the algorithm RPRC process proposed in Section 4.2. There are eight DCs in the cloud environment, and the architecture of these DCs is described in Figure 1, where the value on each edge represents the distance between a pair of DCs. In the analysis, we set the running conditions for a period of T = 24 hours. The whole process consists of six steps independently. Step 1 Create eight virtual DCs with grey colour (the number is the same as real DCs), as is shown in Figure 7(a). Step 2 Add edges between virtual DCs and real DCs, indicating the shortest path between them. Step 3 Construct minimum-spanning tree from Figure 7(b). As is well known, the number of edges in the spanning tree is 15. Step 4 Delete the virtual vertices (grey) and their linked edges with only one connection in minimum-spanning tree. The result after deletion is shown in Figure 7(c).

88 X. Wu and W. Su

Step 5 Delete the redundant DCs and their connections. And the result after deletion is shown in Figure 7(d). Step 6 Delete the redundant edges from DCs where there are two virtual DCs. And the result after deletion is shown in Figure 7(e).

Figure 7 Example for replicas placements strategy under a response time constraint (see online version for colours)

(a) (b)

(c) (d)

(e)

At the end, the rest of candidate DC is the place selected to store the replicas. That is the vertex set {dc 1 ′  , dc4 ′  , dc6′ }.Then the final replica storage places are their corresponding DCs: {dc, dc, dc}. In the analysis, the upper limit of the response time in a single request T is set to upper 10 s. We define replicas degree to represent the number of replicas in the system, and will compare our replica placement mechanism with other four strategies: BestClient, MinimiseExpectedUtil, MaximiseTimeDiffUtil, and RTRM. As smaller replica degree means less cost of management, we compare the smallest replica degree of each strategy to make sure that the response time of a single request is smaller than T . The result is shown in Table 2. upper From the analysis above, we can see that our replicas placement strategy has the smallest replicas degree, indicating the least cost in replica management. Though MinimiseExpectedUtil also has smallest replica degree, its total response time is bigger.

Dataset replica placement strategy under a response time constraint 89

Table 2 Results of replicas degree comparisons

Mechanism Replicas degree Vertex to host replica RPRC 3 dc1, dc4, dc6 BestClient 4 dc1, dc4, dc5, dc6 MinimiseExpectedUtil 3 dc1, dc5, dc6 MaximiseTimeDiffUtil 4 dc1, dc4, dc5, dc7 RTRM 4 dc1, dc4, dc5, dc6

5.3 Simulation of replica strategy based on response-time constraint

In this section, some simulation results will be given with different configurations. And the best replica placement strategy is to minimum the reduced response time in cloud environment.

5.3.1 Simulation environments In order to testify the validity of the proposed replica strategy, we simulate a series of tests on the SwinDew-C [22], a cloud computing simulation environment built on the computing facilitates at Swinburne University of Technology, which consists of ten servers and ten high-end PCs. In SwinDew-C, we have installed VMWare (http://ww.vmware.com), so that it can offer unified computing and storage resources. By utilising the unified resources we set up DCs that can host applications. In the DCs, Hadoop (http://hadoop.apache.org) is installed that can facilitate the MapReduce computing paradigm and distributed data management. The hardware and software environment of the server machine is shown in Table 3.

Table 3 Hardware and software environment

Hardware and software Environments CPU Intel Core i7 6700 Memory 4G DDR II RAM Hard disk 500 GB SATA II Hard Driver 7200 RPM OS 64-bit CentOS5.6 with Linux 2.6.18.8 kernel

5.3.2 Simulations We first generate a series of datasets, whose size ranges from 1 G to 2 G, and distribute them on the DCs randomly. Then, we design different numbers of tasks, which will be scheduled the related datasets in cloud. The system will automatically take the start time and end time down respectively using timestamp in the corresponding data requests. There are three simulations. Simulation 1 The number of replicas with different placement strategies It is an important issue to determine the number and the store place for replicas. Different numbers and store places can lead to different system

90 X. Wu and W. Su

performance. Table 4 shows the average response time of replica strategy comparisons: sequential, random, and RPRC proposed in previous section. Table 4 Average response time of replica placement comparisons with different replica numbers

Replica number Sequential Random RPRC 0 138.87 0 0 1 123.87 98.87 79.65 3 101.77 76.87 41.76 5 98.76 70.64 50.54 7 80.76 68.87 49.66

It is clear that with the replicas added, the response time has decreased with different number of tasks. Therefore, the replica strategy can effectively reduce the response time in cloud environment. We can see from Table 4 that the response time of RPRC is the smallest among the three strategies in different replica numbers. And RPRC can achieve the best result with replica degree 3. Simulation 2 The average response time with different replica placement strategies Figure 8 shows the average response time of replica strategy comparisons under different number of tasks. In each circumstance, RPRC strategy performs better than any others.

Figure 8 Comparisons of average response time with different number of tasks (see online version for colours)

140NoReplicasSequential

Random RPRC

Time

10 30 50 70 90 110 130 150 170 190 Number of Data Requests

Through the analysis of simulation results, it can be deduced that RPRC strategy is very suitable for user access mode, and can effectively improve the system performance.

Dataset replica placement strategy under a response time constraint 91

6 Conclusions and future works

Cloud computing is emerging as one of the best solutions to utilise existing resources for catering for the massive computational and data handling requirements of today’s high performance application. Data replications technology allows reducing user waiting time and speeding up data access. It increases data availability by providing users with different replicas of the same service, and all of them in coherent state. In this paper, we present a novel response-time constraint based replica placement strategy in cloud computing environment. It strives to increase data availability, and to improve cloud system bandwidth consumption. Our contributions can be summarised as follows: 1 a response time estimation model is formulated to describe the user waiting time in cloud environment, including wait access latency, disk write/read time and data transfer time 2 a model to describe the dataset replica placement in the cloud environment 3 an approximate algorithm to determine the replicas’ places 4 analysis and simulation are given to testify the validity of above conclusions. Through extensive simulations, we have shown that RPRC strategy behaves much better than the other replica management strategies in terms of average response time and service response time. However, there are still some studies that need to be done in the near future, such as: 1 replica placement can also be extended by considering additional parameters, for instance, security and cost 2 replication strategy should further increase data availability in the near future under the premise of reducing the user waiting time thus, speeding up data access. In a word, replica strategies can be investigated to complement the dynamic replacement algorithms to further improve the overall system performance.

References

Almuttairi, R.M., Wankar, R., Negi, A. et al. (2013) ‘A two phased service oriented broker for replica selection in data grids’, Future Generation Computer Systems, Vol. 29, No. 4, pp.953–972. Amazon Elastic Computing Cloud (2016) [online] http://aws.amazon.com/ec2. (accessed 24 August 2016). Bandic, Z., Blagojevic, F., Guyot, C. et al. (2015) ‘Deadline-based scheduling in a distributed file system’, Proc of Syrnposinnz on Operatrrrg Systettts Prirzctples, pp.95–98. Dai, W., Ibrahim, I. and Bassiouni, M. (2016) ‘A new replica placement policy for Hadoop distributed file system’, 2016 IEEE 2nd International Conference on Big Data Security on Cloud. Deng, A. and Shi, X. (2016) ‘Data-driven metric development for online controlled experiments: seven lessons learned’, ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, ACM, pp.77–86. Foster, I., Zhao, Y., Raicu, I. et al. (2008) ‘Cloud computing and grid computing 360-degree compared’, in Proceeding of Grid Computing Environments Workshop, pp.1–10.

92 X. Wu and W. Su

Ghemawat, S., Gobioff, H. and Leung, S.T. (2003) ‘The google file system’, ACM SIGOPS Operating Systems Review, Vol. 37, No. 5, pp.29–43. Grace, R.K. and Manimegalai, R. (2016) ‘Replica placement and predictive replica selection techniques to improve the performance of data grid’, Asian Journal of Research in Social Sciences and Humanities, October, Vol. 6, No. 10, pp.1824–1839. Grossman, R.L., Gu, Y., Sabala, M. et al. (2009) ‘Compute and storage clouds using wide area high performance networks’, Future Generation Computer Systems, Vol. 25, No. 2, pp.179–183. Li, Y., Dai, W., Ming, Z. and Qiu, M. (2015) ‘Privacy protection for preventing data over-collection in smart city’, in IEEE Transactions on Computers, August, No. 99. Mell, P. and Grance, T. (2011) ‘The nist definition of cloud computing, recommendations of the national institute of standards and technology’, National Institute of Standards and Technology, pp.800–145. Qiu, M., Ming, Z., Li, J., Gai, K. and Zong, Z. (2015) ‘Phase-change memory optimization for green cloud with genetic algorithm’, in IEEE Transactions on Computers, December, Vol. 64, No. 12, pp.3528–3540. Robins, G. and Zelikovsky, A. (2000) ‘Improved Steiner tree approximation in graphs’, in Proceeding of 11th Annual ACM-SIAM Symposium on Discrete Algorithms, pp.770–779. Shi, Y., Zhao, X., Guo, S. et al. (2016) ‘SRConfig: an empirical method of interdependent soft configurations for improving performance in n-tier application’, IEEE International Conference on Services Computing, IEEE, pp.601–608. Shvachko, K., Kuang, H., Radia, S. et al. (2010) ‘The Hadoop distributed file system’, Proceeding of 2012 IEEE 31st Symposium on Reliable Distributed Systems (SRDS), IEEE, pp.378–383. Sun, D.W., Chang, G.R., Gao, S. et al. ‘Modeling a dynamic data replication strategy to increase system availability in cloud computing environments’, Journal of Computer Science and Technology, Vol. 27, No. 2, pp.256–272. Wang, Q., Kanemasa, Y., Li, J. et al. (2012) ‘Response time reliability in cloud environments: an empirical study of n-tier applications at high resource utilization’, in Proceeding of 2012 IEEE 31st Symposium on Reliable Distributed Systems (SRDS), IEEE, pp.378–383. Wei, Q., Veeravalli, B., Gong, B. et al. (2010) ‘CDRM: a cost-effective dynamic replication management scheme for cloud storage cluster’, in Proceeding of 2010 IEEE International Conference on Cluster Computing (CLUSTER), IEEE, pp.188–196. Yang, Y., Liu, K., Chen, J. et al. (2008) ‘An algorithm in SwinDeW-C for scheduling transaction-intensive cost-constrained cloud workflows’, in Proceeding of IEEE Fourth International Conference on e-Science, IEEE, pp.374–375. Zhang, Q., Zhang, S.Q., Leon-Garcia, A. and Boutaba, R. (2015) ‘Aurora: adaptive block replication in distributed file systems’, in Proceedings of the 2015 IEEE 35th International Conference on Distributed Computing Systems, Columbus, USA.

Websites http://en. wikipedia.org/wiki/Little’s law http://www.cmdln.org/2010/04/22/analyzing-io-performance-in-linux/
International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

## An Efficient Multi-Objective Model

## for Data Replication in Cloud

## Computing Environment

K. Sasikumar, BITS Pilani, Dubai, UAE B. Vijayakumar, BITS Pilani, Dubai, UAE

ABSTRACT

The main aim of the proposed methodology is to design a multi-objective function for replica management system using oppositional gravitational search algorithm (OGSA), in which we analyze the various factors influencing replication decisions such as mean service time, mean file availability, energy consumption, load variance, and mean access latency. The OGSA algorithm is hybridization of oppositional-based learning (OBL) and gravitational search algorithm (GSA), which is change existing solution, and to adopt a new good solution based on objective function. Here, firstly we create a set of files and data node to generate a population by assigning the file to data node randomly and evaluate the fitness which is minimizing the objective function. Secondly, we regenerate the population to produce optimal or suboptimal population using OGSA. The experimental results show that the performance of the proposed methods is better than the other methods of data replication problem.

KEywORDS Energy Consumption, File Replication, Gravitational Search Algorithm, Load Variance and Mean Access Latency, Mean File Availability, Mean Service Time, Multi-Objective, Oppositional-Based Learning

1. INTRODUCTION

The main aim for the clients putting away the information in the cloud is to protect the information and recoup it at whatever point required. Any failure in server ought not to bring about the loss in data. Cloud applications incorporate gaming, voice, and video conferencing, online office, stockpiling, reinforcement, social networking. These applications’ execution depends generally on the accessibility of superior correspondence assets and system productivity (Sasikumar & Madiajagan 2016; Kliazovich et al., 2016). Data replication is a usually utilized strategy to form the information accessibility. It requires a high transfer speed information throughput path. Cloud recreates the elements and preserves them deliberately on different servers situated at different geographic areas. Replication is making different duplicates of a current element (Haider & Nazir, 2016). A few approaches in distributed systems are occupied with improving the dependability and also the accessibility. The replication method is one of the techniques in Cloud registering, which gives a various copy of a specific service

DOI: 10.4018/IJEIS.2020010104

Copyright © 2020, IGI Global. Copying or distributing in print or electronic forms without written permission of IGI Global is prohibited.

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

of the client on different hubs for chopping down the client period of waiting and additionally the bandwidth utilization in the cloud framework and furthermore to raise the accessibility of data (Nguyen et al. 2016). For instance, data stockpiling frameworks such as Amazon S3 (Amazon, 2018), Google File System (Borthakur, 2007) and Hadoop Distributed File System (Ghemawat et al., 2003) all receive a 3-copies data replication methodology automatically, i.e. store 3 data duplicates at one time, for the motivations behind data reliable quality. There are two sorts of replications of data and they are the dynamic replication algorithm (Gopinath & Sherly, 2017) and the static replication algorithm (Bhuvaneswari & Ravi, 2018). Replication is utilized to advance framework accessibility (by guiding traffic to a reproduction after a failure), prevent loss of data (by retrieving lost information from a copy), and enhance execution (by spreading the load over various copies and by making the low-latency availability of access to clients around the globe). And there are various ways to deal with replication. Synchronous replication guarantees all duplicates are cutting-edge, yet possibly brings about high inactivity on updates. Additionally, accessibility might be affected if synchronously recreated updates can’t fulfill while a few copies are offline. Asynchronous replication prohibits high write latency (in demanding, influencing it to fit for wide range of replications) however allows reproductions to be stale. Besides, loss of data may occur if an update is lost because of breakdown before duplication can be performed (Sann & Soe, 2017). High accessibility, high adaptation to internal failure and high proficiency access to cloud data centers where failures are ordinary as opposed to exceptional are critical issues, because of the substantial scale data support. Replication of data permits diminishing client waiting time, accelerating access of data by expanding data accessibility by giving the client diverse copies of a similar service, every one of them with the consistent state (Yadav et al, 2016). So as to accomplish element replication, there are two critical inquiries in reproducing information in distributed storage groups that must be comprehended: (1) what number appropriate imitations of every datum ought to be made in the cloud to meet a sensible framework prerequisite is an imperative issue for additional research. As the framework support cost will fundamentally maximize quantity of replicas expanding, keeping excessively numerous or settled reproductions are not a decent decision. (2) Where should these imitations be set to meet the framework task fast execution rate and load adjusting necessities is another essential issue to be altogether explored. These two related issues are by and large alluded to as the replica management issue (Bijolin et al., 2017). In the replication framework, the vitality utilization increases as the quantity of reproductions increments. So as to limit the vitality cost, consequently, the quantity of reproductions ought to be as little as could be allowed. This is clashing with the previously mentioned. Thus, planning replication administration techniques include adjusting an assortment of tradeoffs. As the present replication systems don’t take total data center vitality cost as the essential streamlining focus to tackle the replica management issue. A significant number of them are constrained by the way that they consider just few execution parameters. With the expanding vitality cost in data centers, a vitality effective way to deal with overseeing data and its reproductions in the cloud is very popular (Gill & Singh 2016). To overcome the above-mentioned issues, in this paper we propose a multi-objective optimized data replication strategy for cloud storage system using oppositional gravitational search algorithm (OGSA). OGSA migration is used to change existing solutions and to adopt new good solutions. Here, OBL strategy is combined with GSA which is increase the searching ability of the replication strategy. To calculate the replica number and replica layout, here we consider the five components such as mean file unavailability (MFU), mean service time (MST), load variance (LV), energy consumption (EC) and mean access latency (MAL) to capture the relationship among replica number, replica layout and these performances. The five objectives are to provide close to optimal values for these objectives. The main contribution of the proposed methodology is given below:

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

- The mathematical expression of the Multiobjective function is designed based on five single objective functions such as mean file unavailability (MFU), mean service time (MST), load variance (LV), energy consumption (EC) and mean latency (ML);
- The proposed system should decreases file service time and access latency increases file availability and enhances system load balancing;
- Based on the five objective function, replicas are located among data node;
- The particular number of replicas is maintained for each node to reach optimal value.

2. RELATED wORK

A lot of researchers have explained a research related to replication management strategy. Among them some of the research works are analyzed here; Sun et al. (2012) have presented a dynamic data replication technique along with an elaborate survey on replication techniques suitable for cloud computing environments. The main objective of this approach has been to maximize data availability, enhance the successful execution of cloud system task and to reduce the bandwidth consumption of cloud system. Mohamed-K Hussein and Mohamed-H Mousa (2012) have presented a data replication technique that adaptively chooses the data files for replication so as to enhance the general reliability of the system and to attain the needed QoS. The presented approach chooses dynamically the quantity of replicas as well as the efficient data nodes for replication. The adaptive method has detected the best replication-based location depending on a heuristic search for the best replication factor of each file. Pritaj Yadav and Alka Gulati (2012) have proposed a new technique for quickly detecting replicate identification to fasten the process of searching and indexing. Any match in even a single, leads to a potential replicate match indication. This approach has been useful in the area of replicate document detection utilizing cloud-based computing. Meroufel et al. (2013) have proposed a replication strategy. Also, a placement and replacement strategies has been proposed which aims on placing and replacing the replicas that guarantees the desired availability with the least possible quantity of replicas even when there have been any node failures and without overloading the system. Esma Insaf Djebbar and Ghalem Belalem (2013) have presented a new optimization technique that has considered an effective data placement and scheduling of tasks by replicating data in cloud environments. The presented approach and the techniques utilized in it have been able to reduce response time and enhance data placement by scheduling tasks to the data centers that incorporate most of the needed data. Kirubakaran et al. (2013). The modified dynamic data replication strategy has been compared dynamic data replication strategy. Also, the synchronous and asynchronous replica data file updation on updating the main data center has been incorporated. The modification has been depending on the double exponential moving average function and the access frequency based on users. Zeng Zeng and Bharadwaj Veeravalli (2014) have presented an approach for determining the total number of Metadata Servers (MDS) that every data object in the system can have and the overall request rates that every MDS can serve, so as to attain the minimum mean response time of all metadata requests which is one of the primary performance indexes. Lena Wiese (2014) has studied a clustering-based fragmentation for the generalization operator anti instantiation with which related information can be detected in distributed data. A standard clustering algorithm has been utilized for deriving a semantic fragmentation of data in the database. Agrawal et al. (2015) have presented a taxonomy of large scale partitioned replicated transactional databases with the aim of giving a clear knowledge of growing space of highly available and scalable database systems. The presented taxonomy has been based on the connection among replica management and transaction management. Milani et al., (2016) have reviewed the past and the state-of-the-art mechanisms in the field of cloud data replication. Also, taxonomy of the reviewed cloud data replication mechanisms has been introduced. Using this study, some related open issues and some procedures for solving the challenges have been mapped out. Sookhtsaraei et al. (2016) have presented a replication manager known as locality replication manager. The simulation results

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

have clearly shown that the presented approach can be a suitable option for distributed systems as it had consumed less resources and energy, has more availability, less delay and had optimized the distribution of load. Najme Mansouri (2016) has proposed an adaptive data replication strategy. The presented approach replicates the data dynamically in advance. Fu et al. (2016) have presented an approach known as cadros which is a cloud assisted data replication and storage scheme for enhancing the data availability in DOSN. The quantitative analysis on storage capacity of cadros has been performed. The data in cadros have been segmented in a way that overhead caused by storing the data in cloud has been reduced at the same time satisfying the desired data availability. Li et al. (2016) have presented cloud storage systems, data storage cost and data reliability can be considered as the two main concerns. A cost-efficient data reliability management technique known as PRCR based on a generalized data reliability model also proposed. Malik et al. (2016) have performed a survey on data management and data replication techniques which have been presented by both research and industrial communities. The survey has mainly concentrated on elaborating and classifying the current approaches which tackle the resource usage and quality of service provisioning with various levels of effectiveness. Galen J. Maclaurin and Stefan Leyk (2016) have proposed an active machine learning framework for temporal updating of land cover data. The presented approach uses a maximum entropy classifier for extracting information from one landsat image utilizing the National Land Cover Database (NLCD). Najme Mansouri (2016) have presented a new replica placement. The presented replica management has been based on five parameters such as failure probability, mean service time, storage usage, load variance and latency. Also, a new replica placement technique has been presented based on the last time the replica was requested, size of replica, the availability of the file and number of access. Casas et al. (2017) have presented a strategy for scientific workflow in cloud computing. For balancing system utilization through parallelization, the presented approach splits scientific workflows into many sub workflows. The data reuse and replication methods have been utilized for optimizing the amount of data that is needed to be transferred between tasks at run-time. The presented approach has provided optimal solutions. Wang et al. (2017) have developed a new reliability model to analyze the system reliability of multi-way de-clustering data layouts and to investigate their potential parallel recovery possibilities. Nagarajan et al. (2017) have designed an intelligent replica manager and have implemented it in the middleware of the grid to schedule data intensive applications. The developed approach has taken into account of multiple parameters such as storage capacity, bandwidth and communication cost of the nearby sites previous to decision making for the selection and placement of replica. Li et al. (2017) have presented a study that has described the generation and placement of replicas on distributed caching servers for improving load balancing and reducing the cache occupation while balancing the utilization rate of distributed servers. Tiles with related position and access times have been considered for distributing tile requests and for supporting current access by a huge number of users. Milani et al. (2017) have presented a systematic review of data replication. The existing and state of the art techniques in the area of cloud data replication have been reviewed. Moreover, taxonomy of the surveyed mechanisms for data replication has been provided. Tziritas et al. (2017) have presented an investigative approach on the utilization of data replication in conjunction with the virtual machine assignment problem. Also, the development of algorithms that decide which data should be replicated where and which virtual machine should be migrated so that the network overhead can be minimized has been focused on. Mansouri et al. (2017) have presented a new replication strategy called dynamic popularity aware replication strategy. To improve the general performance, a parallel downloading method has been introduced which replicate data segments and parallel download replicated data segments. The presented approach has been analyzed and compared with some of the existing algorithms. The results have shown that the proposed approach has outperformed all the compared approaches. Tos

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

et al. (2017) proposed a data replication strategy that fulfils the response time objective to execute queries and enable the provider to return a profit from each execution at the same time. The presented approach has predicted the queries’ response time and has executed data replication in a manner that the execution of any specific query is still estimated to be profitable for the provider. The simulation results have shown that the proposed approach has satisfied the response time guarantees with less usage of the cloud resources. Rachhpal Singh (2017) have presented the GVNSTR technique for using threads balancing have been considered as the NP-hard problem. The advantages of Genetic Algorithm and Variable Neighborhood Search have been used in the presented approach with threat replication for overcoming the issue of Variable Neighborhood Search and Genetic Algorithm. S. Ahamed Ali and M. Ramakrishnan (2017) have presented a new protocol known as ‘Secure Provable Data Possession scheme with Replication support in the Cloud using Tweaks’ that avoids the cloud service provider cheating the owner of the data by handling fewer replicas than agreed one in the SLAs. Stavros Souravlas and Angelo Sifaleras (2017) have surveyed and classified the techniques of data replication for data grids. The data replication strategies have been classified into time based, space based, and geography based. For various access patterns and for various kinds of architectures, the strategies have been developed. Also, a discussion has been provided for the main parameters computed to evaluate the developed strategies. Krupskii et al. (2018) have presented a new copula model which can be utilized with the replicated spatial data. The proposed approach has been based on the assumption of existence of common factor and has influence over the joint dependence of every measurements of the process. Zhang et al. (2018) have presented IR+ directing various processes’ requests to various storage servers by replicating chosen file area and leveraging the heterogeneous storage devices. For removing I/O interference for a single MPI program on disks by utilizing the merits of optimized access patterns and heterogeneous storage devices. It has detected file segments that could have been incorporated in the interfering accesses and have replicated them to their respectively designated storage servers. Spivak et al. (2018 have suggested an enhanced algorithm. Also, an algorithm customization has been introduced for immediate computations that need particular approaches in terms of execution time and reliability. Modern data storage aspects like the capacity to work with data on various layers that can significantly enhance the overall performance of the presented approach. Shafi’i Muhammad Abdulhamid et al. (2018) have presented a dynamic clustering league championship algorithm (DCLCA) scheduling technique for fault tolerance awareness to address cloud task execution which would reflect on the current available resources and reduce the untimely failure of autonomous tasks. Sandeep Kumar Polu (2018) have presented a division and Replication of Data in Cloud for Optimal Performance and Security approach for fragment data objects which are uploaded by the data provider and execute a graph-based approach to calculate the distances utilizing the TColoring technique to foresee the data nodes for putting fragmented data. Mouna Jouini and Latifa Ben Arfa Rabai (2019) have presented the authors will deal with security problems in cloud computing systems and show how to solve these problems using a quantitative security risk assessment model named Multi-dimensional Mean Failure Cost (M2FC). In fact, they summarize first security issues related to cloud computing environments and then propose a generic framework that analysis and evaluate cloud security problems and then propose appropriate countermeasures to solve these problems. Riad Mokadem et al. (2018), have presented a data replication strategy for cloud systems that satisfies the response time objective for executing queries while simultaneously enables the provider to return a profit from each execution. The proposed strategy estimates the response time of the queries and performs data replication in a way that the execution of any particular query is still estimated to be profitable for the provider. Yalda Ebadi and Nima Jafari Navimipour (2019), have presented the problem is formulated as an optimization problem and a hybrid metaheuristic algorithm is offered to solve it. The algorithm uses the global search capability of the Particle Swarm Optimization (PSO)

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

algorithm and the local search capability of the Tabu Search (TS) to get high-quality solutions. The efficiency of the method is shown by comparing it with simple PSO, TS, and Ant Colony Optimization (ACO) algorithm on different test cases. Bahram Hajimirzaei and Nima Jafari Navimipour (2019), have presented a new intrusion detection system (IDS) based on a combination of a multilayer perceptron (MLP) network, and artificial bee colony (ABC) and fuzzy clustering algorithms. Normal and abnormal network traffic packets are identified by the MLP, while the MLP training is done by the ABC algorithm through optimizing the values of linkage weights and biases. Yanling Shao et al. (2019), have presented a novel data replica placement strategy for coordinated processing data-intensive IoT workflows in collaborative edge and cloud computing environment. Firstly, data replica placement can be modelled as a 0–1 integer programming problem to consider the overall data dependency, data reliability and user cooperation. And then, the ITÖ algorithm, a variant of intelligent swarm optimization, is presented to address this model. Gregory Levitin et al. (2018), have presented to one of such risks, co-residence attacks where a user’s information in one VM can be accessed (stolen) or corrupted through side channels by a malicious attacker’s VM co-residing on the same server. We model and optimize users’ data protection policy in which sensitive data are partitioned into several blocks to enhance data security and multiple replicas are further created for each block to provide data survivability in a cloud environment subject to the co-residence attacks. Dejene Boru et al. (2015), have presented the data replication in cloud computing data centers. Unlike other approaches available in the literature, we consider both energy efficiency and bandwidth consumption of the system. This is in addition to the improved quality of service QoS obtained as a result of the reduced communication delays. Pooya Shahrokh and Faramarz Safi-Esfahani (2016), have presented a semi-heuristic genetic algorithm that is a combination of both a heuristic method and the genetic algorithm. This heuristic method changes chromosomes based on unsatisfied constraints. Research findings show that the proposed method can be applied to find a composition plan that satisfies user’s requirements more efficiently than other methods. Ledmi et al. (2018), have presented the authors propose a new architecture for the volunteer cloud computing systems to allow balancing the load between volunteer clouds in a decentralized manner, and between resources inside a volunteer cloud in centralized manner. Moreover, their proposal shows more advantages: First, selecting a resource according to the user requirements and to the system performance. Second, estimating the volunteer resource failure probability by using the stochastic process Markov chain model. Amma, NG Nageswari, and F. Ramesh Dhanaseelan (2019), have presented an efficient method for secure privacy preserving in cloud. Initially, the shared file is encrypted using a Vigenere encryption algorithm before uploading. For creating the privacy map, the efficient classification algorithm is recommended. Here, a Modified Artificial Neural Network (MANN) is used to generate the privacy map. The weight value of the neural network is optimized using a Particle Swarm Optimization (PSO) algorithm. Usman et al. (2019), have presented to explore and gain an understanding of the determinants of adoption factors for cloud ERP and its relative advantage to small and medium enterprises (SME) organisations. The manufacturing SMEs in Nigeria are specifically targeted. This study also seeks to develop a research model that integrates the innovation characteristics and technology-organisation- environment (TOE) perspectives that underlie its adoption. Chi, Yongfang (2018), have presented to discusses the network system structure design for data centers in large enterprises using cloud computing. First, she designs a framework for a cloud data center in large enterprise systems. Second, she establishes the data center network frame based on software-defined networking (SDN) and the algorithm procedure. Third, she studies the moving algorithm of a virtual machine and the broadband allocation mechanism of a data center of a large enterprise network system along with the mathematical model.

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

3. MATHEMATICAL EXPRESSION OF MULTI OBJECTIVE FUNCTION (MOF)

To develop a Replication Management strategy for cloud storage cluster, in this paper we design a multi-objective function (MOF). The MOF consist of optimizing a set of single objectives. In this paper, we have formulated to design a five objective function such as mean file unavailability (MFU), mean service time (MST), load variance (LV), energy consumption (EC) and mean latency (ML). To design a MOF, we have to handle some problems because some the objectives are may be conflicting with one another. For example, we obtain improved MFU means it making additional replicas, however, a similar way it will expand the energy consumption. Also, locating replicas on the data hubs with the most reduced disk space use will not be perfect from the latency minimization perspective. The issue at hand manages with these conflicting goals by developing a set of solutions that compromise these conflicting goals. In this section, we model each of the objectives in detail dependent upon how well the objectives are formulated. In this section, we model each of the objectives in detail.

3.1. Calculation Mean File Unavailability U(Ψ) The first objective function of the proposed methodology is Mean file unavailability (MFU). The g o o d s ys t e m p r ov i d e s t h e h i g h e s t ava i l a b i l i t y. T h e b i n a r y d e c i s i o n m a t r i x

## Ψ = ( Ψ) (i  = 1 2, ,... ; n j  =i, ,... 2m )is used to denote decision variable:

ij

 1if F is assigned to data node DN i j Ψ=(1) ij 0 otherwise 

### Here, each data node DN (1  ≤ j ≤m) has different failure probability P. The probability of

j j file Funavailable is defined as follows: i

m *

### P F(  )= Π Ψ(i j , )×P(2)

i j j=1

* where Πrepresents the cumulative multiplier of non-zero elements. From equation (2), we can calculate the file availability:

### P F(  )= 1 − P F( )(3)

i i

m *

### P F(  )= 1 − Π Ψ(i j ,  )×P(4)

i j j=1

Compare to file availability, the system availability is more important. So, the system availability is defined as below equation:

nnm * 

### P SA( )=  Π P F(  )= Π 1 − Π Ψ(i j ,  )×P(5)

i j i=1  i=1  j=1 

The main objective is, our system maximizes the system availability. In this multi-objective function, maximization process it affects the other objective function. So, we design the mean file

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

unavailability. The availability maximization objective is achieved by minimizing the MFU. The MFU calculation is given in Equation 8:

nnm 1 1

### MFU = U (Ψ )= × ∑P F( )= × ∑Π Ψ (i j,  )×P(6)

1 ij j=1 n i=1  n i=1

3.2. Mean Service Time U(Ψ) The second objective function of the proposed methodology is calculating mean service time (MST). The MST is depended upon the system process rate. The good system provides a less mean service time. The expected service time is calculated using Equation 7:

S i

### ST i j( ,  ) = Ψ (i j , )×(7)

TR j

### where ST i j( ,) is the expected service time of the file Fon the data node DN , S is the size of

i j i the data and TRis the data transfer rate on node D then mean service time of file Fis calculated j j i using Equation 8:



### mA i j( ,)



### ST i( )=  ∑ST i j( ,  )× (8)



### j=1A i( )



m

### A i( )=  ∑A i j( ,)(9)

j=1

### where A i j( ,) is the access rate and A (i) is the mean access rate. Using above equation, we can

calculate the mean service time of the system:

nnm

### 11A i j( ,)



### MST = U (Ψ ) = × ∑ST i( ) =  × ∑∑ST i j(,  )× (10)

 

### n i=1n i=1j=1A i( )



 nm

### 1SA i j( , )

 i

### = × ∑∑Ψ (i j,  )× × (11)

 TR

### ni=1j=1jA i( )

3.3. Load Variance U(Ψ) The third objective function of the proposed methodology is load variance. The load of the data hub should not extend the actual capacity of the data node. The lower value of the load variance, the better load balancing is achieved. The load variance is calculated based on access rate and service time of the file F: i

### L i j( ,  )= A i j( ,  )× ST i j( ,) (12)

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

The load of data node Dcan be calculated by: j

n

### L j( )=  ∑L i j(,)(13)

i=1

The mean value of the system is calculated using Equation (14):

n

### L = × ∑L j( )(14)

m j=1

The load variance objective function is calculated using Equation (15):

m

## ∑(L j( ) − L)

j=1

### LV =U (Ψ ) = (15)

m−1

3.4. Energy Consumption U(Ψ) The total energy consumption is mainly composed of renewable energy consumption (RE) and cooling energy consumption (CE). The energy consumption objective function EC is given in Equation (16):

mn 1

## EC = 1 +× ∑∑Ψ (i j ,  )× L i j( ,  )×( P ( ) −j  P ( )j )+P( )jj(16)

  max idle idle Q  j=1i=1

### Q = U ( Ψ ) =(17)

T out −1 T in

3.5. Mean Latency U(Ψ) The fifth objective function is called the mean latency. Minimizing latency is important for any storage system. Minimizing latency depends on utilizing high bandwidth channels, as high bandwidth channels yield lesser latency. Mean latency of file Fis calculated using following Equation (18): i

m 1S i

### L = × ∑Ψ (i j,  )× × A i j(, )(18)

i

### r j=1B ( )j

i

The mean latency system is calculated using Equation (19):

m 1S i

### × ∑Ψ (i j ,  )× × A i j( ,)

 nnr   

### Li j=1B( )j

i

### ML = U (Ψ) = ∑=∑(19)

nn i=1ii=1

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

Using Equations (6) (11) (15) (17) (19) we can design the objective function. Minimizing objective function is important for the storage system. The parameter used in proposed replica management system is given in Table 1.

## Consider the file set F =(F F,  ...F ), for any i j,  (i  ≠ j). Each file Fhas a file size (s)

i 1 2ni

## and access rate (R). The set of file size is S =(S , S ...S  )and the set of access rate is

1 2n

## R =(R , R ...R ). Similarly, assume a set of data node DN is DN = (DN , DN ,....DN )and

1 2nj 1 2m each node has particular failure probability, transfer rate, and capacity. The set of DN failure

### probability is P = (P P ,  ,..., P), the set of transfer rate is TR = (TR TR ,  ,...,TR )and the

1 2m1 2m

### set of capacity C = (C , C ,..., C ). The main objective is to effectively generate the file

1 2m replication which efficiently reduces file service time and access latency, increases file availability and improves system load balancing. Let Ψ defined an individual. When we apply multi-objective optimization to our problem, the problem can be defined as:

Table 1. Parameter used in the proposed data replication strategy

Parameters Description

FNumber of files (1≤i≤n) i

th S ifile size i

th Rifile access rate i

DNNumber of data node (1≤j≤m) j

th P jfailure probability of DN j j

th TRjtransfer rate j

th CCapacity of jdata node DN j j

α,…..,αProportion variables

### P F( ) ProbabilityoffileFunavailability

i i

### P F( ) ProbabilityoffileFavailability

i i

### P SA( ) Systemavailability

### ST i j( ,) Expectedservicetime

### ST i j( ,) MeanservicetimeoffileF

i

L(j) Load value of data node D j

* ΠCumulativemultiplierofnon-zeroelements

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020



## minU  = {U ( Ψ ) ,U  ( Ψ ) ,U  ( Ψ ) ,U  ( Ψ ) ,U( Ψ)}

1 2 3 4 5   n

### Ψ (i j,  )×S  ≤ C ,U(Ψ )== MFU , U (Ψ ) = MST ,U(Ψ)

i j12 3

### s t. .  ∑(20)

 i=1  

### U ( Ψ )= EC ,U ( Ψ) =L

4 5 

Based on the above model, in this paper, we design a multi-objective function which is a combination of five objective functions:

### MOF ( Ψ )= α ×U  ( Ψ )+ α ×U  ( Ψ )+ α ×U  ( Ψ )+ α ×U  ( Ψ )+ αU( Ψ)(21)

1 1 2 2 3 3 4 4 5 5

where, α ,...α are propor tion var iables cor responding to the objective functions 1 5

### U (Ψ ),....U (Ψ), respectively.

1 5

4. PROPOSED FILE REPLICATION METHODOLOGy

The main intention of proposed Replica Management system is to provide an efficient storage system which achieved by creating replicas, which effectively reduce the file service time and access latency, increases file availability and improves system load balancing. However, replication entails various costs such as storage and energy consumption for holding replicas. The replica process is mainly used to reduce the data loss when a disaster occurs. The disaster is happening in a framework which is based on natural disasters or human activities. When a disaster happens in business progression the organization may get enormous loss of information and also financial loss. In addition, the disaster happens in customer side means backup will be stored in the cloud but disaster happens in the cloud means data will be lost. To avoid the data loss the replicas are generated. May, any disaster occurs on the cloud side also; we have retrieved the files without any difficulties. Two important problems are arises in the proposed replication management system such as How many suitable replicas of each data should be created in the cloud and where should these replicas be placed. To find out the solution for that optimization algorithms are needed. In this paper, we propose a multi-objective function- based replica management using Oppositional Gravitational search algorithm (OGSA). Here, OGSA algorithm is a hybridization of Oppositional Based Learning (OBL) and Group Search Optimizer (GSO). To improve the searching ability of the proposed system OBL strategy is hybrid to the GSO. The designed multi-objective function consists of mean file unavailability, mean service time, load variance, energy consumption and means access latency. Figure 1 shows the data replication strategy. The step by step process of proposed replica management system is given below.

4.1. Step 1: Solution Initialization Solution initialization is an important process of resource allocation. Here, at first, we randomly generate the initial solution base on a number of files and data nodes. For example, we consider five files and five data node. The randomly generated initial solution is given in Table 2. In Table 2, the first row represents the data node and the each of the other nodes represents the replica layout scheme of a file. Here, F files replicas are stored in two locations, F files replicas are stored in three 1 2 locations, F files replicas are stored in three locations, F files replicas are stored in two location and 3 4 F files replicas are stored in three location. Any file is assigned to at least one data node. Here, each file has two constraints such as integrity constraint and capacity constraints. For integrity constraint, the file F must satisfy the condition: i

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

Figure 1. Data replication strategy

Table 2. Initial solution format

DNDNDNDNDN 1 2 3 4 5 F1 0 1 0 0

F0 1 1 1 0

F1 0 0 1 1

F0 1 0 0 1

F1 0 1 1 0

m

### ∑Ψ (i j ,)>0

j=1

For capacity constraints, the sum of files size assigned to a data node must be less than the capacity of the data node.

4.2. Step 2: Opposite Solution Generation

### Then, author generates the opposite solution (OS  ) . The position of the opposite agent’s positions

i

### are entirely well explained by constituents of S (OS  ) :

i i

1 dD OS = [ oS ,..., oS ,..., oS](22) i i ii

dddddddth th where oS = L +U  − Swith oS ∈ L U, is the position of i opposite agent OS in the d iiiii iii dimension of opposite population.

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

4.3. Step 3: Fitness Calculation Once the initial solution created, we have to calculate the fitness of each solution. The fitness is a combination of a five single objective function. The fitness calculation is explained in section 3. The proposed replicas management system multi-objective function is given in Equation (23):

### MOF ( Ψ )= α ×U  ( Ψ )+ α ×U  ( Ψ )+ α ×U  ( Ψ )+ α ×U  ( Ψ )+ αU( Ψ)(23)

1 1 2 2 3 3 4 4 5 5

### best fit = min (MOF )(24)

### worst fit = max (MOF )(25)

4.4. Step 4: Agent Acceleration In GSA, before calculating agent’s acceleration, we find out the agent’s mass. Each agent’s the mass shrewdness is as follows:

### Fit ( ) −k  worst fit k( )

i

### m ( ) =k  (26)

i

### best fit k( ) −  worst fit k( )

### m ( )k

i

### M ( ) =k  (27)

iN

### ∑m ( )k

j j=1

th th

### where, M ( )k is the standardized mass of iagent at kiteration and worst k( ) , best k( ) are the

i th d th

### best and worst fitness of all agents at k iteration. The acceleration A ( )k acting on i agent at

i iteration k is assessed as follows:

### M ( )k

didd

## A ( ) =k  ∑rand G k( )  (s  ( ) −k  s ( )k)(28)

i jji

### j ∈gbest j , ≠iR ( ) +k  ε

ij

where gis the set of first 2% agents with the best fitness value and biggest mass, rand is the best j

### uniform haphazard number within the interval [0,1], R ( )k is the Euclidean distance within two

ij th th th agents iand j at kiteration and ε is a small positive constant. The rapid reduction of

### gravitational constant G k( ) instigating a debauched decay of investigation is one among the

difficulties of GSA. So as to acquire linear consideration with the iterative procedure, the gravitational

### function G k( ) is demarcated as given:

 k 

### G k( ) =  G × 1 −(29)

0  K

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

dd

## G = g max(y −y)(30)

0  UL d ∈{1 2 , ,...D }

where g is the coefficient of search interval parameter

4.5. Step 5: Agent’s Velocity and Position Updates

th

### The agent’s velocity and position for next (k +1) iteration are considered as follows:

ddd

### V (k +1) =  rand ×V  ( ) +k  a ( )k(31)

ii ii

ddd

### S (k +1) =  S ( ) +k  V (k+1) (32)

iii

d th

### where, rand is the haphazard number within the interval [0,1]. V (k+1) is the velocity of i

i i th th d th th

### agent at ddimension at the time of titeration and S (k +1) is the position of iagent at d

i th dimension at the period of k iteration.

4.6. Step 6: Termination Criteria The algorithm discontinues its execution only if a maximum number of iterations are achieved and the solution which is holding the best fitness value is selected and it is specified as the best solution to proposed replication management system. Once the best fitness is attained by means of OGSA, solution-based replicas are generated. The pseudo code of proposed data replication strategy is given in Table 3.

5. RESULT AND DISCUSSION

In this section, we discuss the result obtained from the proposed data replication management in cloud computing environment. We have implemented our proposed work using Java (jdk 1.6) with cloud Sim tools and a series of experiments have been performed on a PC with Windows 7 Operating system at 2 GHz dual-core PC machine with 4 GB main memory running a 64-bit version of Windows
2007. The experimental result is carried out mainly based on file availability, mean service time, load variance, energy consumption and mean latency. The parameter used in the proposed simulation is given in Table 4. Here, we check the performance of our work with different node resources, different types of nodes and different network configuration (see Table 5).

5.1. Experimental Result The main objective of proposed work is to file replication while speeding up data access, reducing access latency and increase data availability. To achieve this in this paper we used oppositional gravitational search algorithm. For experimentation, here we used 8 data node. The configuration of 8 data node is given in Table 4. The default number of generations in the proposed data replication system is set to 100. Here, we compare our proposed work with GSA based data replication and MOE method (Li et al., 2017). In “A Replication Strategy for a Distributed High-Speed Caching System Based on Spatiotemporal Access Patterns of Geospatial Data” (Li et al., 2017), they explained a multi-objective Evolutionary algorithm for data replication, which is unique in the sense that they view the various factors influencing replication decisions such as access latency, storage costs, and data availability as objectives.

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

Table 3. Input/Output

Input: Number of file F i Number of data node DN i Output: Replication file Initialization: Failure probability of each data node, Transfer rate of each data node(MB/s), Capacity of each data node(GB), Network speed of each node (Mbit) Start: Generate the initial solution S , i = 1 2, ,.....n (refer Table 2) i Calculate the corresponding opposite solution OS , i = 1 2, ,.....n using Equation (22) i

### Evaluate the fitness ( MOF (Ψ)) of each solution using Equation (23)

### Find out best fitness best fit = min(MOF)

### Find out worst fit = max(MOF )

Set cycle k= 1 Repeat: Update the solution using GSA { Compute Mass of each agent using Equation 27 Calculate acceleration of agent’s using Equation 28 Calculate the gravitational constant using Equation 30 Update agent’s velocity using Equation 31 Update the position of agent’s using Equation 32 Set k=k+1; } Repeat Output: Replicated files

Table 4. Multi-objective data replication system configuration

Parameter Value

Number of generation 200

Population size 20

Non-uniformity parameter 2

α, α,α,α,α0.2 12 34 5

Table 5. Data node configuration

Parameter Value

Total number of nodes 8

Failure probability of each data node 0.002, 0.003, 0.005, 0.004,0.001,0.006, 0.001,0.001

Transfer rate of each data node(MB/s) 350,200,150,225,250,175,325,300

Capacity of each data node(GB) 200, 150,100,120,200,250,100,150

Network speed of each node (Mbit) 1000

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

Figure 2 shows the performance comparison using mean file unavailability by varying file size. Here, the x-axis represents the files size and the y-axis represents the mean file unavailability. Here, the file size varies from 50-200. The good replication system has higher availability. In this paper, we calculate mean file unavailability (MFU) which is the opposite of file availability. If the MFU is minimum means our system got higher file availability. When analyzing Figure 2, our proposed approach achieves the minimum MFU of 0.07 which is 0.09 for GSA based replication and 0.12 for using MOE (Nagarajan et al., 2017). As per the analysis, the mean unavailability is gradually increased when the file size goes on increasing. Moreover, Figure 3 shows the performance of proposed approach using mean latency by varying files size. Minimizing latency is essential for any storage system. Minimizing latency depends on

Figure 2. Performance comparison using mean file unavailability

Figure 3. Performance comparison using mean latency

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

utilizing high bandwidth channels, as high bandwidth channels yield lesser latency. Thus, it is better to place popular files in data nodes with high bandwidth to minimizing their latency. When analyzing, Figure 3 our proposed approach achieves the minimum latency of 0.368 which is very much low compared to other approaches. Similarly, Figure 4 shows the Performance comparison using mean service time. We have minimum time to complete the work means our system is good. Here, if the number of file increase means the mean service time also increase. When analyzing Figure 4, our proposed approach obtains the minimum to achieve the result compare to other two methods. Figure 5 shows the performance comparison using load variance. The lower value of load variance, the better load balancing is achieved. One of the main constraints of replication, when generating replication the size of data node shouldn’t exceed. When analyzing Figure 5, our proposed approach

Figure 4. Performance comparison using mean service time

Figure 5. Performance comparison using load variance

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

achieves the minimum load variance of 0.368 (ms), which is 0.06 for using GAS based replication and 0.5543 for using MOE (Nagarajan et al., 2017). Similarly, Figure 6 shows the Performance comparison using energy consumption. From Figure 5, we understand our proposed approach saves more energy than other two algorithms. With the increase of the total number of files, the energy saving becomes more apparent. When the total number of files reaches 200, our approach uses 1.3 KJ but other two works are utilized 1.8 KJ and 2KJ. Figure 7 shows the performance of multi-objective function. With the increase of the total number of files, the objective function also increases. The multi-objective function is a combination of five simple objective functions such as mean file unavailability, mean latency, mean service time, mean latency and energy consumption. The five objective functions are analyzed using Figures 1-5. Figure 8 shows the performance of fitness function by varying iterations. From the result section, we clearly understand our proposed approach is better than other two replication methodology.

Figure 6. Performance comparison using energy consumption

Figure 7. Performance comparison using multi objective function

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

Figure 8. Performance of fitness function

6. CONCLUSION

In this section, we have implemented a multi-objective data replication strategy using oppositional gravitational search algorithm (OGSA). To selecting the replication for files that optimize the five objectives such as file availability, mean service time, load variance, energy consumption and mean latency. Here, all the five single objectives are analyzed and based on the five objective functions, we introduced the multi-objective function to decreases file service time and access latency increases file availability and improves system load balancing. Experimental results are carried out each individual objective function and finally analyzed the performance using multi-objective function. Experimental results clearly show our proposed approach got the better results compare to other works. In future work, we validate our proposed. Model on real cloud storage cluster to ensure mush higher availability. Also, we are exploring different replication algorithm and cost mode.

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

REFERENCES

Agrawal, D., El Abbadi, A., & Salem, K. (2015). A Taxonomy of Partitioned Replicated Cloud-based Database Systems. IEEE Data Eng. Bull., 38(1), 4–9.

Ali, S. (2017). Secure provable data possession scheme with replication support in the cloud using Tweaks. Cluster Computing, 1–11.

Amazon. (2008). Amazon simple storage service (Amazon S3). Available: http://aws.amazon.com/s3

Amma, N. G., & Dhanaseelan, F. R. (2019). Optimal Privacy Preserving Scheme Based on Modified ANN and PSO in Cloud. International Journal of Enterprise Information Systems, 15(1), 116–134. doi:10.4018/ IJEIS.2019010107

Bhuvaneswari, R., & Ravi, T. N. (2018). A Review of Static and Dynamic Data Replication Mechanisms for Distributed Systems. International Journal on Computer Science and Engineering, 6(5).

Bijolin Edwin, Umamaheswari, & Roshni Thanka. (2017). An efficient and improved multi-objective optimized replication management with dynamic and cost aware strategies in cloud computing data center. Journal of Cluster Computing.

Borthakur, D. (2007). The Hadoop distributed file system: Architecture and design. Available: http://hadoop. apache.org/common/docs/r0.18.3/ hdfs_design.html

Boru, D., Kliazovich, D., Granelli, F., Bouvry, P., & Zomaya, A. Y. (2015). Energy-efficient data replication in cloud computing datacenters. Cluster Computing, 18(1), 385–402. doi:10.1007/s10586-014-0404-x

Casas, I., Taheri, J., Ranjan, R., Wang, L., & Zomaya, A. Y. (2017). A balanced scheduler with data reuse and replication for scientific workflows in cloud computing systems. Future Generation Computer Systems, 74, 168–178. doi:10.1016/j.future.2015.12.005

Chi, Y. (2018). Network System Structure Design for Data Centers in Large Enterprises Using Cloud Computing. International Journal of Enterprise Information Systems, 14(2), 87–97. doi:10.4018/IJEIS.2018040106

Djebbar, E. I., & Belalem, G. (2013). Optimization of tasks scheduling by an efficacy data placement and replication in cloud computing. In International Conference on Algorithms and Architectures for Parallel Processing (pp. 22-29). Springer. doi:10.1007/978-3-319-03889-6_3

Ebadi, Y., & Navimipour, N. J. (2019). An energy‐aware method for data replication in the cloud environments using a Tabu search and particle swarm optimization algorithm. Concurrency and Computation, 31(1), e4757. doi:10.1002/cpe.4757

Fu, S., He, L., Liao, X., & Huang, C. (2016). Developing the Cloud-integrated data replication framework in decentralized online social networks. Journal of Computer and System Sciences, 82(1), 113–129. doi:10.1016/j. jcss.2015.06.010

Ghemawat, S., Gobioff, H., & Leung, S. (2003). The Google file system. ACM Symposium on Operating Systems Principles, 29 - 43.

Gill, N. K., & Singh, S. (2016). A dynamic, cost-aware, optimized data replication strategy for heterogeneous cloud data centers. Future Generation Computer Systems, 65, 10–32. doi:10.1016/j.future.2016.05.016

Gopinath, S., & Sherly, E. (2017). A Weighted Dynamic Data Replication Management for Cloud Data Storage Systems. International Journal of Applied Engineering Research, 12(24).

Haider, S., & Nazir, B. (2016). Fault tolerance in computational grids: Perspectives, challenges, and issues. SpringerPlus, 5(1), 1991. doi:10.1186/s40064-016-3669-0 PMID:27933247

Hajimirzaei, B., & Navimipour, N. J. (2019). Intrusion detection for cloud computing using neural networks and artificial bee colony optimization algorithm. ICT Express, 5(1), 56–59. doi:10.1016/j.icte.2018.01.014

(2012). Hussein, Mohamed-K., and Mohamed-H. Mousa. A light-weight data replication for cloud data centers environment. International Journal of Engineering and Innovative Technology, 1(6), 169–175.

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

Jouini, M., & Latifa, B. A. R. (2019). A security framework for secure cloud computing environments. In Cloud security: Concepts, methodologies, tools, and applications (pp. 249–263). IGI Global. doi:10.4018/978-1-5225- 8176-5.ch011

Kirubakaran, Valarmathy, & Kamalanathan. (2013). Data replication using modified D2RS in cloud computing for performance improvement. Journal of Theoretical & Applied Information Technology, 58(2).

Kliazovich, D., Pecero, J. E., Tchernykh, A., Bouvry, P., Khan, S. U., & Zomaya, A. Y. (2016). CA-DAG: Modeling Communication-Aware Applications for Scheduling in Cloud Computing. Journal of Grid Computing, 14(1), 23–39.

Krupskii, P., Huser, R., & Genton, M. G. (2018). Factor copula models for replicated spatial data. Journal of the American Statistical Association, 113(521), 467–479. doi:10.1080/01621459.2016.1261712

Latiff, M. S. A., Syed, H. H. M., & Abdullahi, M. (2018). Fault tolerance aware scheduling technique for cloud computing environment using dynamic clustering algorithm. Neural Computing & Applications, 29(1), 279–293. doi:10.1007/s00521-016-2448-8

Ledmi, A., Bendjenna, H., & Mounine, H. S. (2018). Optimizing Both the User Requirements and the Load Balancing in the Volunteer Computing System by using Markov Chain Model. International Journal of Enterprise Information Systems, 14(1), 35–62. doi:10.4018/IJEIS.2018010103

Levitin, G., Xing, L., & Dai, Y. (2018). Co-residence based data vulnerability vs. security in cloud computing system with random server assignment. European Journal of Operational Research, 267(2), 676–686. doi:10.1016/j.ejor.2017.11.064

Li, R., Feng, W., Wu, H., & Huang, Q. (2017). A replication strategy for a distributed high-speed caching system based on spatiotemporal access patterns of geospatial data. Computers, Environment and Urban Systems, 61, 163–171. doi:10.1016/j.compenvurbsys.2014.02.009

Li, W., Yang, Y., & Yuan, D. (2016). Ensuring cloud data reliability with minimum replication by proactive replica checking. IEEE Transactions on Computers, 65(5), 1494–1506. doi:10.1109/TC.2015.2451644

Maclaurin, G. J., & Leyk, S. (2016). Temporal replication of the national land cover database using active machine learning. GIScience amp. Remote Sensing, 53(6), 759–777.

Malik, S. U. R., Khan, S. U., Ewen, S. J., Tziritas, N., Kolodziej, J., Zomaya, A. Y., & Li, H. et al. (2016). Performance analysis of data intensive cloud systems based on data management and replication: A survey. Distributed and Parallel Databases, 34(2), 179–215. doi:10.1007/s10619-015-7173-2

Mansouri, N. (2016). Adaptive data replication strategy in cloud computing for performance improvement. Frontiers of Computer Science, 10(5), 925–935. doi:10.1007/s11704-016-5182-6

Mansouri, N. (2016). Adaptive data replication strategy in cloud computing for performance improvement. Frontiers of Computer Science, 10(5), 925–935. doi:10.1007/s11704-016-5182-6

Mansouri, N., Rafsanjani, M. K., & Javidi, M. M. (2017). DPRS: A dynamic popularity aware replication strategy with parallel download scheme in cloud environments. Simulation Modelling Practice and Theory, 77, 177–196. doi:10.1016/j.simpat.2017.06.001

Meroufel, B., & Belalem, G. (2013). Managing data replication and placement based on availability. AASRI Procedia, 5, 147–155. doi:10.1016/j.aasri.2013.10.071

Milani, B. A., & Navimipour, N. J. (2016). A comprehensive review of the data replication techniques in the cloud environments: Major trends and future directions. Journal of Network and Computer Applications, 64, 229–238. doi:10.1016/j.jnca.2016.02.005

Milani, B. A., & Navimipour, N. J. (2017). A systematic literature review of the data replication techniques in the cloud environments. Big Data Research, 10, 1–7. doi:10.1016/j.bdr.2017.06.003

Nagarajan, V., & Mulk, A. M. M. (2017). A prediction-based dynamic replication strategy for data-intensive applications. Computers amp. Electrical Engineering, 57, 281–293.

Nguyen, T., Cutway, A., & Shi, W. (2016). Adaptive data replication strategy in cloud computing for performance improvement. Frontiers of Computer Science, 10(5).

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

Polu, S. K., & Polu, S. K. (2018). Security Enhancement for Data Objects in Cloud Computing. International Journal for Innovative Research in Science Technology, 5(6), 18–21.

Sann & Soe. (2017). Agricultural Loan System Using Data Replication Method. Academic Press.

Sasikumar, K. (2016). Literature Survey of Dynamic Data Replication in Cloud Computing. Journal of Applied Sciences. Engineering and Technology, 13(2), 158–172.

Shahrokh, P., & Safi-Esfahani, F. (2016). QoS-based Web Service Composition Applying an Improved Genetic Algorithm (IGA) Method. International Journal of Enterprise Information Systems, 12(3), 60–77. doi:10.4018/ IJEIS.2016070104

Shao, Y., Li, C., & Tang, H. (2019). A data replica placement strategy for IoT workflows in collaborative edge and cloud environments. Computer Networks, 148, 46–59. doi:10.1016/j.comnet.2018.10.017

Singh, R. (2017). Genetic-variable neighborhood search with thread replication for mobile cloud computing. International Journal of Parallel. Emergent and Distributed Systems, 32(5), 486–501. doi:10.1080/17445760. 2016.1188386

Sookhtsaraei, , Artin, , Ghorbani, , & Faraahi, , & Adineh. (2016). A locality-based replication manager for data cloud. Frontiers of Information Technology & Electronic Engineering 17 (12), 1275-1286.

Souravlas & Sifaleras. (2017). Trends in data replication strategies: A survey. International Journal of Parallel, Emergent and Distributed Systems, 1-18.

Spivak, A., Razumovskiy, A., Nasonov, D., Boukhanovsky, A., & Redice, A. (2018). Storage tier-aware replicative data reorganization with prioritization for efficient workload processing. Future Generation Computer Systems, 79, 618–629. doi:10.1016/j.future.2017.04.010

Sun, D.-W., Chang, G.-R., Gao, S., Jin, L.-Z., & Wang, X.-W. (2012). Modeling a dynamic data replication strategy to increase system availability in cloud computing environments. Journal of Computer Science and Technology, 27(2), 256–272. doi:10.1007/s11390-012-1221-4

Tos, U., Mokadem, R., Hameurlain, A., Ayav, T., & Bora, S. (2017). Ensuring performance and provider profit through data replication in cloud systems. Cluster Computing, 1–14.

Tos, U., Mokadem, R., Hameurlain, A., Ayav, T., & Bora, S. (2018). Ensuring performance and provider profit through data replication in cloud systems. Cluster Computing, 21(3), 1479–1492. doi:10.1007/s10586-017-1507-y

Tziritas, N., Koziri, M., Bachtsevani, A., Loukopoulos, T., Stamoulis, G., Khan, S. U., & Xu, C.-Z. (2017). Data replication and virtual machine migrations to mitigate network overhead in edge computing systems. IEEE Transactions on Sustainable Computing, 2(4), 320–332. doi:10.1109/TSUSC.2017.2715662

Usman, U. M. Z., Ahmad, M. N., & Zakaria, N. H. (2019). The Determinants of Adoption of Cloud-Based ERP of Nigerian’s SMES Manufacturing Sector Using Toe Framework and Doi Theory. International Journal of Enterprise Information Systems, 15(3), 27–43. doi:10.4018/IJEIS.2019070102

Wang, J., Wu, H., & Wang, R. (2017). A new reliability model in replication-based big data storage systems. Journal of Parallel and Distributed Computing, 108, 14–27. doi:10.1016/j.jpdc.2017.02.001

Wiese, L. (2014). Clustering-based fragmentation and data replication for flexible query answering in distributed databases. Journal of Cloud Computing, 3(1), 18. doi:10.1186/s13677-014-0018-0

Yadav, P. A. G. (2012). A novel approach for cloud-based computing using replicate data detection. Journal of Global Research in Computer Science, 3(8), 12–16.

Yadav, S. K., Singh, G., & Yadav, D. S. (2016). analysis of a database replication algorithm under load sharing in networks. Journal of Engineering Science and Technology, 11, 193–211.

Zeng, Z., & Veeravalli, B. (2014). Optimal metadata replications and request balancing strategy on cloud data centers. Journal of Parallel and Distributed Computing, 74(10), 2934–2940. doi:10.1016/j.jpdc.2014.06.010

Zhang, X., Jiang, S., Diallo, A., & Wang, L. (2018). IR+: Removing parallel I/O interference of MPI programs via data replication over heterogeneous storage devices. Parallel Computing, 76, 91–105. doi:10.1016/j. parco.2018.01.004

International Journal of Enterprise Information Systems Volume 16 • Issue 1 • January-March 2020

K. Sasikumar obtained his Bachelor’s degree in Computer Science & Engineering from University of Bharathiyar, India. Then he obtained his Master’s degree in Software Systems and from Birla Institute of Technology & Science, Pilani, Rajasthan, India. Currently, he is a research scholar at BITS Pilani, Dubai. His specializations include Software Architecture, Cloud Computing, Computer Networks, Data Mining, Network Security and Parallel Computing. His current research interests are Cloud Computing, Replication strategies, Dynamic Data, Distributed systems.

B. Vijayakumar is a Professor in the department of Computer Science at BITS Pilani, Dubai Campus. His research interests include Software Architecture, Multimedia Systems, Web Data Mining, Component Based Software Development and Distributed Database Systems. He has 30+ publications in refereed journals and conferences. He has served as Technical Program Chair for the International Conference on Cloud Computing Technologies, Applications and Management-ICCCTAM-2012 held at BITS Pilani, Dubai Campus in December 2012.
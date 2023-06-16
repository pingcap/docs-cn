---
title: TiDB Introduction
summary: Learn about the key features and usage scenarios of TiDB.
aliases: ['/docs/dev/key-features/','/tidb/dev/key-features','/docs/dev/overview/']
---

# TiDB Introduction

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

[TiDB](https://github.com/pingcap/tidb) (/’taɪdiːbi:/, "Ti" stands for Titanium) is an open-source distributed SQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. It is MySQL compatible and features horizontal scalability, strong consistency, and high availability. The goal of TiDB is to provide users with a one-stop database solution that covers OLTP (Online Transactional Processing), OLAP (Online Analytical Processing), and HTAP services. TiDB is suitable for various use cases that require high availability and strong consistency with large-scale data.

The following video introduces key features of TiDB.

<iframe width="600" height="450" src="https://www.youtube.com/embed/aWBNNPm21zg?enablejsapi=1" title="Why TiDB?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Key features

- **Easy horizontal scaling**

    The TiDB architecture design separates computing from storage, letting you scale out or scale in the computing or storage capacity online as needed. The scaling process is transparent to application operations and maintenance staff.

- **Financial-grade high availability**

    Data is stored in multiple replicas, and the Multi-Raft protocol is used to obtain the transaction log. A transaction can only be committed when data has been successfully written into the majority of replicas. This guarantees strong consistency and availability when a minority of replicas go down. You can configure the geographic location and number of replicas as needed to meet different disaster tolerance levels.

- **Real-time HTAP**

    TiDB provides two storage engines: [TiKV](/tikv-overview.md), a row-based storage engine, and [TiFlash](/tiflash/tiflash-overview.md), a columnar storage engine. TiFlash uses the Multi-Raft Learner protocol to replicate data from TiKV in real time, ensuring consistent data between the TiKV row-based storage engine and the TiFlash columnar storage engine. TiKV and TiFlash can be deployed on different machines as needed to solve the problem of HTAP resource isolation.

- **Cloud-native distributed database**

    TiDB is a distributed database designed for the cloud, providing flexible scalability, reliability, and security on the cloud platform. Users can elastically scale TiDB to meet the requirements of their changing workloads. In TiDB, each piece of data has at least 3 replicas, which can be scheduled in different cloud availability zones to tolerate the outage of a whole data center. [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview) helps manage TiDB on Kubernetes and automates tasks related to operating the TiDB cluster, making TiDB easier to deploy on any cloud that provides managed Kubernetes. [TiDB Cloud](https://pingcap.com/tidb-cloud/), the fully-managed TiDB service, is the easiest, most economical, and most resilient way to unlock the full power of [TiDB in the cloud](https://docs.pingcap.com/tidbcloud/), allowing you to deploy and run TiDB clusters with just a few clicks.

- **Compatible with the MySQL 5.7 protocol and MySQL ecosystem**

    TiDB is compatible with the MySQL 5.7 protocol, common features of MySQL, and the MySQL ecosystem. To migrate applications to TiDB, you do not need to change a single line of code in many cases, or only need to modify a small amount of code. In addition, TiDB provides a series of [data migration tools](/ecosystem-tool-user-guide.md) to help easily migrate application data into TiDB.

## Use cases

- **Financial industry scenarios**

    TiDB is ideal for financial industry scenarios with high requirements for data consistency, reliability, availability, scalability, and disaster tolerance. Traditional solutions are costly and inefficient, with low resource utilization and high maintenance costs. TiDB uses multiple replicas and the Multi-Raft protocol to schedule data to different data centers, racks, and machines, ensuring system RTO ≦ 30 seconds and RPO = 0.

- **Massive data and high concurrency scenarios**

    Traditional standalone databases cannot meet the data capacity requirements of rapidly growing applications. TiDB is a cost-effective solution that adopts a separate computing and storage architecture, enabling easy scaling of computing or storage capacity separately. The computing layer supports a maximum of 512 nodes, each node supports a maximum of 1,000 concurrencies, and the maximum cluster capacity is at the PB (petabytes) level.

- **Real-time HTAP scenarios**

    TiDB is ideal for scenarios with massive data and high concurrency that require real-time processing. TiDB introduces the TiFlash columnar storage engine in v4.0, which combines with the TiKV row-based storage engine to build TiDB as a true HTAP database. With a small amount of extra storage cost, you can handle both online transactional processing and real-time data analysis in the same system, which greatly saves cost.

- **Data aggregation and secondary processing scenarios**

    TiDB is suitable for companies that need to aggregate scattered data into the same system and execute secondary processing to generate a T+0 or T+1 report. Compared with Hadoop, TiDB is much simpler. You can replicate data into TiDB using ETL (Extract, Transform, Load) tools or data migration tools provided by TiDB. Reports can be directly generated using SQL statements.

## See also

- [TiDB Architecture](/tidb-architecture.md)
- [TiDB Storage](/tidb-storage.md)
- [TiDB Computing](/tidb-computing.md)
- [TiDB Scheduling](/tidb-scheduling.md)

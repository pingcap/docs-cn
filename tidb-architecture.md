---
title: TiDB Architecture
summary: The key architecture components of the TiDB platform
aliases: ['/docs/dev/architecture/','/tidb/dev/architecture']
---

# TiDB Architecture

Compared with the traditional standalone databases, TiDB has the following advantages:

* Has a distributed architecture with flexible and elastic scalability.
* Fully compatible with the MySQL 5.7 protocol, common features and syntax of MySQL. To migrate your applications to TiDB, you do not need to change a single line of code in many cases.
* Supports high availability with automatic failover when a minority of replicas fail; transparent to applications.
* Supports ACID transactions, suitable for scenarios requiring strong consistency such as bank transfer.
* Provides a rich series of [data migration tools](/migration-overview.md) for migrating, replicating, or backing up data.

As a distributed database, TiDB is designed to consist of multiple components. Theses components communicate with each other and form a complete TiDB system. The architecture is as follows:

![TiDB Architecture](/media/tidb-architecture-v3.1.png)

## TiDB server

The TiDB server is a stateless SQL layer that exposes the connection endpoint of the MySQL protocol to the outside. The TiDB server receives SQL requests, performs SQL parsing and optimization, and ultimately generates a distributed execution plan. It is horizontally scalable and provides the unified interface to the outside through the load balancing components such as Linux Virtual Server (LVS), HAProxy, or F5. It does not store data and is only for computing and SQL analyzing, transmitting actual data read request to TiKV nodes (or TiFlash nodes).

## Placement Driver (PD) server

The PD server is the metadata managing component of the entire cluster. It stores metadata of real-time data distribution of every single TiKV node and the topology structure of the entire TiDB cluster, provides the TiDB Dashboard management UI, and allocates transaction IDs to distributed transactions. The PD server is "the brain" of the entire TiDB cluster because it not only stores metadata of the cluster, but also sends data scheduling command to specific TiKV nodes according to the data distribution state reported by TiKV nodes in real time. In addition, the PD server consists of three nodes at least and has high availability. It is recommended to deploy an odd number of PD nodes.

## Storage servers

### TiKV server

The TiKV server is responsible for storing data. TiKV is a distributed transactional key-value storage engine. [Region](/glossary.md#regionpeerraft-group) is the basic unit to store data. Each Region stores the data for a particular Key Range which is a left-closed and right-open interval from StartKey to EndKey. Multiple Regions exist in each TiKV node. TiKV APIs provide native support to distributed transactions at the key-value pair level and supports the Snapshot Isolation level isolation by default. This is the core of how TiDB supports distributed transactions at the SQL level. After processing SQL statements, the TiDB server converts the SQL execution plan to an actual call to the TiKV API. Therefore, data is stored in TiKV. All the data in TiKV is automatically maintained in multiple replicas (three replicas by default), so TiKV has native high availability and supports automatic failover.

### TiFlash server

The TiFlash Server is a special type of storage server. Unlike ordinary TiKV nodes, TiFlash stores data by column, mainly designed to accelerate analytical processing.

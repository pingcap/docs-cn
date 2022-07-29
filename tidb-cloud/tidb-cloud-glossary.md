---
title: TiDB Cloud Glossary
summary: Learn the terms used in TiDB Cloud.
category: glossary
aliases: ['/tidbcloud/glossary']
---

# TiDB Cloud Glossary

## A

### ACID

ACID refers to the four key properties of a transaction: atomicity, consistency, isolation, and durability. Each of these properties is described below.

- **Atomicity** means that either all the changes of an operation are performed, or none of them are. TiDB ensures the atomicity of the [TiDB Region](#region) that stores the Primary Key to achieve the atomicity of transactions.

- **Consistency** means that transactions always bring the database from one consistent state to another. In TiDB, data consistency is ensured before writing data to the memory.

- **Isolation** means that a transaction in process is invisible to other transactions until it completes. This allows concurrent transactions to read and write data without sacrificing consistency. TiDB currently supports the isolation level of `REPEATABLE READ`.

- **Durability** means that once a transaction is committed, it remains committed even in the event of a system failure. TiKV uses persistent storage to ensure durability.

## C

### cluster tier

Determines the functionality and capacity of your cluster. Different cluster tiers provide different numbers of TiDB, TiKV, and TiFlash nodes in your cluster.

## M

### member

A user that has been invited to an organization, with access to the organization and the clusters of this organization.

## N

### node

Refers to either a data instance (TiKV) or a compute instance (TiDB) or an analytical instance (TiFlash).

## O

### organization

An entity that you create to manage your TiDB Cloud accounts, including a management account with any number of multiple member accounts.

### organization members

Organization members are users who are invited by the organization owner to join an organization. Organization members can view members of the organization and can be invited to projects within the organization.

## P

### policy

A document that defines permissions applying to a role, user, or organization, such as the access to specific actions or resources.

### project

Based on the projects created by the organization, resources such as personnel, instances, and networks can be managed separately according to projects, and resources between projects do not interfere with each other.

### project members

Project members are users who are invited to join one or more projects of the organization. Project members can manage clusters, network access, backups, etc.

## R

### Recycle Bin

The place where the data of deleted clusters with valid backups is stored. Once a backed-up cluster is deleted, the existing backup files of the cluster are moved to the recycle bin. For backup files from automatic backups, the recycle bin will retain them for 7 days. For backup files from manual backups, there is no expiration date. To avoid data loss, remember to restore the data to a new cluster in time. Note that if a cluster **has no backup**, the deleted cluster will not be displayed here.

### region

- TiDB Cloud region

    A set of [TiKV](https://docs.pingcap.com/tidb/stable/tidb-storage) nodes deployed in the same geographical area. The set of TiKV nodes will be deployed across at least three different Availability Zones within that region.

- TiDB Region

    The basic unit of data in TiDB. TiKV divides the Key-Value space into a series of consecutive Key segments, and each segment is called a Region. The default size limit for each Region is 96 MB and can be configured.

### replica

A separate database that can be located in the same or different region and contains the same data. A replica is often used for disaster recovery purposes or to improve performance.

## T

### TiDB cluster

The collection of [TiDB](https://docs.pingcap.com/tidb/stable/tidb-computing), [TiKV](https://docs.pingcap.com/tidb/stable/tidb-storage), [the Placement Driver](https://docs.pingcap.com/tidb/stable/tidb-scheduling) (PD), and [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) nodes that form a functional working database.

### TiDB node

The computing node that aggregates data from queries returned from transactional or analytical stores. Increasing the number of TiDB nodes will increase the number of concurrent queries that the cluster can handle.

### TiFlash node

The analytical storage node that replicates data from TiKV in real time and supports real-time analytical workloads.

### TiKV node

The storage node that stores the online transactional processing (OLTP) data. It is scaled in multiples of 3 nodes (for example, 3, 6, 9) for high availability, with two nodes acting as replicas. Increasing the number of TiKV nodes will increase the total throughput.

### traffic filter

A list of IP addresses and Classless Inter-Domain Routing (CIDR) addresses that are allowed to access the TiDB Cloud cluster via a SQL client. The traffic filter is empty by default.

## V

### Virtual Private Cloud

A logically isolated virtual network partition that provides managed networking service for your resources.

### VPC

Short for Virtual Private Cloud.

### VPC peering

Enables you to connect Virtual Private Cloud ([VPC](#vpc)) networks so that workloads in different VPC networks can communicate privately.

### VPC peering connection

A networking connection between two Virtual Private Clouds (VPCs) that enables you to route traffic between them using private IP addresses and helps you to facilitate data transfer.

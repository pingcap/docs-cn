---
title: TiCDC Overview
summary: Learn what TiCDC is, what features TiCDC provides, and how to install and deploy TiCDC.
aliases: ['/docs/dev/ticdc/ticdc-overview/','/docs/dev/reference/tools/ticdc/overview/']
---

# TiCDC Overview

[TiCDC](https://github.com/pingcap/tiflow/tree/master/cdc) is a tool used to replicate incremental data from TiDB. Specifically, TiCDC pulls TiKV change logs, sorts captured data, and exports row-based incremental data to downstream databases.

## Usage scenarios

TiCDC has multiple usage scenarios, including:

- Providing high availability and disaster recovery solutions for multiple TiDB clusters. TiCDC ensures eventual data consistency between primary and secondary clusters in case of a disaster.
- Replicating real-time data changes to homogeneous systems. This provides data sources for various scenarios, such as monitoring, caching, global indexing, data analysis, and primary-secondary replication between heterogeneous databases.

## Major features

### Key capabilities

TiCDC has the following key capabilities:

- Replicating incremental data between TiDB clusters with second-level RPO and minute-level RTO.
- Bidirectional replication between TiDB clusters, allowing the creation of a multi-active TiDB solution using TiCDC.
- Replicating incremental data from a TiDB cluster to a MySQL database or other MySQL-compatible databases with low latency.
- Replicating incremental data from a TiDB cluster to a Kafka cluster. The recommended data format includes [Canal-JSON](/ticdc/ticdc-canal-json.md) and [Avro](/ticdc/ticdc-avro-protocol.md).
- Replicating incremental data from a TiDB cluster to storage services, such as Amazon S3, GCS, Azure Blob Storage, and NFS.
- Replicating tables with the ability to filter databases, tables, DMLs, and DDLs.
- High availability with no single point of failure, supporting dynamically adding and deleting TiCDC nodes.
- Cluster management through [Open API](/ticdc/ticdc-open-api-v2.md), including querying task status, dynamically modifying task configuration, and creating or deleting tasks.

### Replication order

- For all DDL or DML statements, TiCDC outputs them **at least once**.
- When the TiKV or TiCDC cluster encounters a failure, TiCDC might send the same DDL/DML statement repeatedly. For duplicated DDL/DML statements:

    - The MySQL sink can execute DDL statements repeatedly. For DDL statements that can be executed repeatedly in the downstream, such as `TRUNCATE TABLE`, the statement is executed successfully. For those that cannot be executed repeatedly, such as `CREATE TABLE`, the execution fails, and TiCDC ignores the error and continues with the replication process.
    - The Kafka sink provides different strategies for data distribution.
        - You can distribute data to different Kafka partitions based on the table, primary key, or timestamp. This ensures that the updated data of a row is sent to the same partition in order.
        - All these distribution strategies send `Resolved TS` messages to all topics and partitions periodically. This indicates that all messages earlier than the `Resolved TS` have already been sent to the topics and partitions. The Kafka consumer can use the `Resolved TS` to sort the messages received.
        - The Kafka sink sometimes sends duplicated messages, but these duplicated messages do not affect the constraints of `Resolved Ts`. For example, if a changefeed is paused and then resumed, the Kafka sink might send `msg1`, `msg2`, `msg3`, `msg2`, and `msg3` in order. You can filter out the duplicated messages from Kafka consumers.

### Replication consistency

- MySQL sink

    - TiCDC enables the redo log to ensure eventual consistency of data replication.
    - TiCDC ensures that the order of single-row updates is consistent with the upstream.
    - TiCDC does not ensure that the downstream transactions are executed in the same order as the upstream transactions.

    > **Note:**
    >
    > Since v6.2, you can use the sink URI parameter [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb) to control whether to split single-table transactions. Splitting single-table transactions can greatly reduce the latency and memory consumption of replicating large transactions.

## TiCDC architecture

TiCDC is an incremental data replication tool for TiDB, which is highly available through PD's etcd. The replication process consists of the following steps:

1. Multiple TiCDC processes pull data changes from TiKV nodes.
2. TiCDC sorts and merges the data changes.
3. TiCDC replicates the data changes to multiple downstream systems through multiple replication tasks (changefeeds).

The architecture of TiCDC is illustrated in the following figure:

![TiCDC architecture](/media/ticdc/cdc-architecture.png)

The components in the architecture diagram are described as follows:

- TiKV Server: TiKV nodes in a TiDB cluster. When data changes occur, TiKV nodes send the changes as change logs (KV change logs) to TiCDC nodes. If TiCDC nodes detect that the change logs are not continuous, they will actively request the TiKV nodes to provide change logs.
- TiCDC: TiCDC nodes where TiCDC processes run. Each node runs a TiCDC process. Each process pulls data changes from one or more tables in TiKV nodes and replicates the changes to the downstream system through the sink component.
- PD: The scheduling module in a TiDB cluster. This module is responsible for scheduling cluster data and usually consists of three PD nodes. PD provides high availability through the etcd cluster. In the etcd cluster, TiCDC stores its metadata, such as node status information and changefeed configurations.

As shown in the architecture diagram, TiCDC supports replicating data to TiDB, MySQL, Kafka, and storage services.

## Best practices

- When you use TiCDC to replicate data between two TiDB clusters, if the network latency between the two clusters is higher than 100 ms:

    - For TiCDC versions earlier than v6.5.2, it is recommended to deploy TiCDC in the region (IDC) where the downstream TiDB cluster is located.
    - With a series of improvements introduced starting from TiCDC v6.5.2, it is recommended to deploy TiCDC in the region (IDC) where the upstream TiDB cluster is located.

- TiCDC only replicates tables that have at least one valid index. A valid index is defined as follows:

    - A primary key (`PRIMARY KEY`) is a valid index.
    - A unique index (`UNIQUE INDEX`) is valid if every column of the index is explicitly defined as non-nullable (`NOT NULL`) and the index does not have a virtual generated column (`VIRTUAL GENERATED COLUMNS`).

- To use TiCDC in disaster recovery scenarios, you need to configure [redo log](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios).

## Unsupported scenarios

Currently, the following scenarios are not supported:

- A TiKV cluster that uses RawKV alone.
- The [`CREATE SEQUENCE` DDL operation](/sql-statements/sql-statement-create-sequence.md) and the [`SEQUENCE` function](/sql-statements/sql-statement-create-sequence.md#sequence-function) in TiDB. When the upstream TiDB uses `SEQUENCE`, TiCDC ignores `SEQUENCE` DDL operations/functions performed upstream. However, DML operations using `SEQUENCE` functions can be correctly replicated.

TiCDC only partially supports scenarios involving large transactions in the upstream. For details, refer to the [TiCDC FAQ](/ticdc/ticdc-faq.md#does-ticdc-support-replicating-large-transactions-is-there-any-risk), where you can find details on whether TiCDC supports replicating large transactions and any associated risks.

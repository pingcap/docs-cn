---
title: TiCDC Overview
summary: Learn what TiCDC is, what features TiCDC provides, etc.
aliases: ['/docs/dev/ticdc/ticdc-overview/','/docs/dev/reference/tools/ticdc/overview/']
---

# TiCDC Overview

> **Warning:**
>
> TiCDC is still an experimental feature. It is **NOT** recommended that you use it in the production environment.

[TiCDC](https://github.com/pingcap/ticdc) is a tool for replicating the incremental data of TiDB. This tool is implemented by pulling TiKV change logs. It can restore data to a consistent state with any upstream TSO, and provides [TiCDC Open Protocol](/ticdc/ticdc-open-protocol.md) to support other systems to subscribe to data changes.

## TiCDC Architecture

When TiCDC is running, it is a stateless node that achieves high availability through etcd in PD. The TiCDC cluster supports creating multiple replication tasks to replicate data to multiple different downstream platforms.

The architecture of TiCDC is shown in the following figure:

![TiCDC architecture](/media/cdc-architecture.png)

### System roles

- TiKV CDC component: Only outputs key-value (KV) change logs.

    - Assembles KV change logs in the internal logic.
    - Provides the interface to output KV change logs. The data sent includes real-time change logs and incremental scan change logs.

- `capture`: The operating process of TiCDC. Multiple `capture`s form a TiCDC cluster that replicates KV change logs.

    - Each `capture` pulls a part of KV change logs.
    - Sorts the pulled KV change log(s).
    - Restores the transaction to downstream or outputs the log based on the TiCDC open protocol.

## Replication features

This section introduces the replication features of TiCDC.

### Sink support

Currently, the TiCDC sink component supports replicating data to the following downstream platforms:

- Databases compatible with MySQL protocol. The sink component provides the final consistency support.
- Kafka based on the TiCDC Open Protocol. The sink component ensures the row-level order, final consistency or strict transactional consistency.

### Ensure replication order and consistency

#### Replication order

- For all DDL or DML statements, TiCDC outputs them **at least once**.
- When the TiKV or TiCDC cluster encounters failure, TiCDC might send the same DDL/DML statement repeatedly. For duplicated DDL/DML statements:

    - MySQL sink can execute DDL statements repeatedly. For DDL statements that can be executed repeatedly in the downstream, such as `truncate table`, the statement is executed successfully. For those that cannot be executed repeatedly, such as `create table`, the execution fails, and TiCDC ignores the error and continues the replication.
    - Kafka sink sends messages repeatedly, but the duplicate messages do not affect the constraints of `Resolved Ts`. Users can filter the duplicated messages from Kafka consumers.

#### Replication consistency

- MySQL sink

    - TiCDC does not split in-table transactions. This is to **ensure** the transactional consistency within a single table. However, TiCDC does **not ensure** that the transactional order in the upstream table is consistent.
    - TiCDC splits cross-table transactions in the unit of tables. TiCDC does **not ensure** that cross-table transactions are always consistent.
    - TiCDC **ensures** that the order of single-row updates are consistent with that in the upstream.

- Kafka sink

    - TiCDC provides different strategies for data distribution. You can distribute data to different Kafka partitions based on the table, primary key, or timestamp.
    - For different distribution strategies, the different consumer implementations can achieve different levels of consistency, including row-level consistency, eventual consistency, or cross-table transactional consistency.
    - TiCDC does not have an implementation of Kafka consumers, but only provides [TiCDC Open Protocol](/ticdc/ticdc-open-protocol.md). You can implement the Kafka consumer according to this protocol.

## Restrictions

To replicate data to TiDB or MySQL, you must ensure that the following requirements are satisfied to guarantee data correctness:

- The table to be replicated has the primary key or a unique index.
- If the table to be replicated only has unique indexes, each column of at least one unique index is explicitly defined in the table schema as `NOT NULL`.

### Unsupported scenarios

Currently, The following scenarios are not supported:

- The TiKV cluster that uses RawKV alone.
- The [DDL operation `CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) and the [SEQUENCE function](/sql-statements/sql-statement-create-sequence.md#sequence-function) in TiDB v4.0. When the upstream TiDB uses `SEQUENCE`, TiCDC ignores `SEQUENCE` DDL operations/functions performed upstream. However, DML operations using `SEQUENCE` functions can be correctly replicated.
- The [TiKV Hibernate Region](https://github.com/tikv/tikv/blob/master/docs/reference/configuration/raftstore-config.md#hibernate-region). TiCDC prevents the Region from entering the hibernated state.
- The scheduling of existing replication tables to new TiCDC nodes, after the capacity of the TiCDC cluster is scaled out.

## Install and deploy TiCDC 

You can deploy TiCDC components in the process of deploying a new TiDB cluster using TiUP. You only need to [add TiCDC](/production-deployment-using-tiup.md#step-3-edit-the-initialization-configuration-file) to the configuration file when TiUP starts the TiDB cluster.

Currently, you can also add TiCDC components to an existing TiDB cluster using either TiUP or binary. For details, see [Deploy and install TiCDC](/ticdc/manage-ticdc.md#deploy-and-install-ticdc).

## Manage TiCDC Cluster and Replication Tasks

Currently, you can use the `cdc cli` tool to manage the status of a TiCDC cluster and data replication tasks. For details, see: 

- [Use `cdc cli` to manage cluster status and data replication task](/ticdc/manage-ticdc.md#use-cdc-cli-to-manage-cluster-status-and-data-replication-task)
- [Use HTTP interface to manage cluster status and data replication task](/ticdc/manage-ticdc.md#use-http-interface-to-manage-cluster-status-and-data-replication-task)

## Troubleshoot TiCDC

For details, refer to [Troubleshoot TiCDC](/ticdc/troubleshoot-ticdc.md).

## TiCDC Open Protocol

TiCDC Open Protocol is a row-level data change notification protocol that provides data sources for monitoring, caching, full-text indexing, analysis engines, and primary-secondary replication between different databases. TiCDC complies with TiCDC Open Protocol and replicates data changes of TiDB to third-party data medium such as MQ (Message Queue). For more information, see [TiCDC Open Protocol](/ticdc/ticdc-open-protocol.md).

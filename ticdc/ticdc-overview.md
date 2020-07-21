---
title: TiCDC Overview
summary: Learn what TiCDC is, what features TiCDC provides, etc.
aliases: ['/docs/dev/ticdc/ticdc-overview/','/docs/dev/reference/tools/ticdc/overview/']
---

# TiCDC Overview

> **Note:**
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
    - Sorts the pulled the KV change log(s).
    - Restores the transaction to downstream or outputs the log based on the TiCDC open protocol.

## Replication features

This section introduces the replication features of TiCDC.

### Sink support

Currently, the TiCDC sink component supports replicating data to the following downstream platforms:

- Databases compatible with MySQL protocol. The sink component provides the final consistency support.
- Kafka based on the TiCDC Open Protocol. The sink component ensures the row-level order, final consistency or strict transactional consistency.

## Restrictions

To replicate data to TiDB or MySQL, you must ensure that the following requirements are satisfied to guarantee data correctness:

- The table to be replicated has the primary key or a unique index.
- If the table to be replicated only has unique indexes, each column of at least one unique index is explicitly defined in the table schema as `NOT NULL`.

### Unsupported scenarios

Currently, The following scenarios are not supported:

- The TiKV cluster that uses RawKV alone.
- The [new framework for collations](/character-set-and-collation.md#new-framework-for-collations) in TiDB v4.0. Before you enable this feature, make sure that the downstream cluster is the TiDB cluster with the same collation as those in the upstream; otherwise, inconsistent collations lead to the issue that the data cannot be located.
- The [DDL operation `CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) and the [SEQUENCE function](/sql-statements/sql-statement-create-sequence.md#sequence-function) in TiDB v4.0. When the upstream TiDB uses `SEQUENCE`, TiCDC ignores `SEQUENCE` DDL operations/functions performed upstream. However, DML operations using `SEQUENCE` functions can be correctly replicated.
- The [TiKV Hibernate Region](https://github.com/tikv/tikv/blob/master/docs/reference/configuration/raftstore-config.md#hibernate-region). TiCDC prevents the Region from entering the hibernated state.
- The scheduling of existing replication tables to new TiCDC nodes, after the capacity of the TiCDC cluster is scaled out.

## Manage TiCDC Cluster and Replication Tasks

For details, see [Manage TiCDC Cluster and Replication Tasks](/ticdc/manage-ticdc.md).

## Troubleshoot TiCDC

For details, refer to [Troubleshoot TiCDC](/ticdc/troubleshoot-ticdc.md).

## TiCDC Open Protocol

TiCDC Open Protocol is a row-level data change notification protocol that provides data sources for monitoring, caching, full-text indexing, analysis engines, and primary-secondary replication between different databases. TiCDC complies with TiCDC Open Protocol and replicates data changes of TiDB to third-party data medium such as MQ (Message Queue). For more information, see [TiCDC Open Protocol](/ticdc/ticdc-open-protocol.md).

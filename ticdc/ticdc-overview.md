---
title: TiCDC Overview
summary: Learn what TiCDC is, what features TiCDC provides, etc.
category: reference
---

# TiCDC Overview

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

### Black and white table lists

You can write blacklist and whitelist filtering rules to filter or only replicate all changed data in certain databases or tables. The filtering rules are similar to those of MySQL such as `replication-rules-db` or `replication-rules-table`.

## Restrictions

To replicate data to TiDB or MySQL, you must ensure that the following requirements are satisfied to guarantee data correctness:

- The table to be replicated has the primary key or a unique index.
- If the table to be replicated only has unique indexes, each column of at least one unique index is explicitly defined in the table schema as `NOT NULL`.

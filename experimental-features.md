---
title: TiDB Experimental Features
summary: Learn the experimental features of TiDB.
aliases: ['/tidb/dev/experimental-features-4.0/']
---

# TiDB Experimental Features

This document introduces the experimental features of TiDB in different versions. It is **NOT** recommended to use these features in the production environment.

## Stability

+ TiFlash limits the use of I/O resources by compressing or sorting data, mitigating the contention for I/O resources between background tasks and front-end data reading and writing (Introduced in v5.0)
+ Improve the stability of the optimizer's choice of indexes (Introduced in v5.0)
    + Extend the statistics feature by collecting the multi-column order dependency information.
    + Refactor the statistics module, including deleting the `TopN` value from `CMSKetch` and the histogram, and adding NDV information for histogram buckets of each table index.

## Scheduling

+ Cascading Placement Rules feature. It is a replica rule system that guides PD to generate corresponding schedules for different types of data. By combining different scheduling rules, you can finely control the attributes of any continuous data range, such as the number of replicas, the storage location, the host type, whether to participate in Raft election, and whether to act as the Raft leader. See [Cascading Placement Rules](/configure-placement-rules.md) for details. (Introduced in v4.0)
+ Elastic scheduling feature. It enables the TiDB cluster to dynamically scale out and in on Kubernetes based on real-time workloads, which effectively reduces the stress during your application's peak hours and saves overheads. See [Enable TidbCluster Auto-scaling](https://docs.pingcap.com/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling) for details. (Introduced in v4.0)

## SQL

+ List Partition (Introduced in v5.0)
+ List COLUMNS Partition (Introduced in v5.0)
+ [Dynamic Mode for Partitioned Tables](/partitioned-table.md#dynamic-mode). (Introduced in v5.1)
+ The expression index feature. The expression index is also called the function-based index. When you create an index, the index fields do not have to be a specific column but can be an expression calculated from one or more columns. This feature is useful for quickly accessing the calculation-based tables. See [Expression index](/sql-statements/sql-statement-create-index.md) for details. (Introduced in v4.0)
+ [Generated Columns](/generated-columns.md).
+ [User-Defined Variables](/user-defined-variables.md).
+ [JSON data type](/data-type-json.md) and [JSON functions](/functions-and-operators/json-functions.md).
+ [View](/information-schema/information-schema-views.md).
+ [Stale Read](/stale-read.md).

## Configuration management

+ Persistently store configuration parameters in PD, and support dynamically modifying configuration items. (Introduced in v4.0)
+ [SHOW CONFIG](/sql-statements/sql-statement-show-config.md) (Introduced in v4.0)

## Data sharing and subscription

+ [Integrate TiCDC with Kafka Connect (Confluent Platform)](/ticdc/integrate-confluent-using-ticdc.md) (Introduced in v5.0)
+ [The cyclic replication feature of TiCDC](/ticdc/manage-ticdc.md#cyclic-replication) (Introduced in v5.0)
+ [Bit flags of columns](/ticdc/ticdc-open-protocol.md#bit-flags-of-columns) in [TiCDC Open Protocol](/ticdc/ticdc-open-protocol.md#row-changed-event).

## Storage

+ [Disable Titan](/storage-engine/titan-configuration.md#disable-titan-experimental).
+ [Titan Level Merge](/storage-engine/titan-configuration.md#level-merge-experimental).
+ TiFlash supports distributing the new data of the storage engine on multiple hard drives to share the I/O pressure. (Introduced in v4.0)

## Backup and restoration

+ [Back up Raw KV](/br/use-br-command-line-tool.md#back-up-raw-kv-experimental-feature).

## Garbage collection

+ [Green GC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50).

## Diagnostics

+ [SQL diagnostics](/information-schema/information-schema-sql-diagnostics.md).
+ [Cluster diagnostics](/dashboard/dashboard-diagnostics-access.md).

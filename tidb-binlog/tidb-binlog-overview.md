---
title: TiDB Binlog Overview
summary: Learn overview of the cluster version of TiDB Binlog.
aliases: ['/docs/dev/tidb-binlog/tidb-binlog-overview/','/docs/dev/reference/tidb-binlog/overview/','/docs/dev/reference/tidb-binlog-overview/','/docs/dev/reference/tools/tidb-binlog/overview/']
---

# TiDB Binlog Cluster Overview

This document introduces the architecture and the deployment of the cluster version of TiDB Binlog.

TiDB Binlog is a tool used to collect binlog data from TiDB and provide near real-time backup and replication to downstream platforms.

TiDB Binlog has the following features:

* **Data replication:** replicate the data in the TiDB cluster to other databases
* **Real-time backup and restoration:** back up the data in the TiDB cluster and restore the TiDB cluster when the cluster fails

> **Note:**
>
> TiDB Binlog is not compatible with some features introduced in TiDB v5.0 and they cannot be used together. For details, see [Notes](#notes). It is recommended to use [TiCDC](/ticdc/ticdc-overview.md) instead of TiDB Binlog.

## TiDB Binlog architecture

The TiDB Binlog architecture is as follows:

![TiDB Binlog architecture](/media/tidb-binlog-cluster-architecture.png)

The TiDB Binlog cluster is composed of Pump and Drainer.

### Pump

[Pump](https://github.com/pingcap/tidb-binlog/blob/master/pump) is used to record the binlogs generated in TiDB, sort the binlogs based on the commit time of the transaction, and send binlogs to Drainer for consumption.

### Drainer

[Drainer](https://github.com/pingcap/tidb-binlog/tree/master/drainer) collects and merges binlogs from each Pump, converts the binlog to SQL or data of a specific format, and replicates the data to a specific downstream platform.

### `binlogctl` guide

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl) is an operations tool for TiDB Binlog with the following features:

* Obtaining the current `tso` of TiDB cluster
* Checking the Pump/Drainer state
* Modifying the Pump/Drainer state
* Pausing or closing Pump/Drainer

## Main features

* Multiple Pumps form a cluster which can scale out horizontally
* TiDB uses the built-in Pump Client to send the binlog to each Pump
* Pump stores binlogs and sends the binlogs to Drainer in order
* Drainer reads binlogs of each Pump, merges and sorts the binlogs, and sends the binlogs downstream
* Drainer supports [relay log](/tidb-binlog/tidb-binlog-relay-log.md). By the relay log, Drainer ensures that the downstream clusters are in a consistent state.

## Notes

* In v5.1, the incompatibility between the clustered index feature introduced in v5.0 and TiDB Binlog has been resolved. After you upgrade TiDB Binlog and TiDB Server to v5.1 and enable TiDB Binlog, TiDB will support creating tables with clustered indexes; data insertion, deletion, and update on the created tables with clustered indexes will be replicated to the downstream via TiDB Binlog. When you use TiDB Binlog to replicate the tables with clustered indexes, pay attention to the following:

    - If you have upgraded the cluster to v5.1 from v5.0 by manually controlling the upgrade sequence, make sure that TiDB binlog is upgraded to v5.1 before upgrading the TiDB server to v5.1.
    - It is recommended to configure the system variable [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50) to a same value to ensure that the structure of TiDB clustered index tables between the upstream and downstream is consistent.

* TiDB Binlog is incompatible with the following features introduced in TiDB v5.0 and they cannot be used together.

    - [TiDB Clustered Index](/clustered-indexes.md#limitations): After TiDB Binlog is enabled, TiDB does not allow creating clustered indexes with non-single integer columns as primary keys; data insertion, deletion, and update of the created clustered index tables will not be replicated downstream via TiDB Binlog. If you need to replicate tables with clustered indexes, upgrade your cluster to v5.1 or use [TiCDC](/ticdc/ticdc-overview.md) instead.
    - TiDB system variable [tidb_enable_async_commit](/system-variables.md#tidb_enable_async_commit-new-in-v50): After TiDB Binlog is enabled, performance cannot be improved by enabling this option. It is recommended to use [TiCDC](/ticdc/ticdc-overview.md) instead of TiDB Binlog.
    - TiDB system variable [tidb_enable_1pc](/system-variables.md#tidb_enable_1pc-new-in-v50): After TiDB Binlog is enabled, performance cannot be improved by enabling this option. It is recommended to use [TiCDC](/ticdc/ticdc-overview.md) instead of TiDB Binlog.

* Drainer supports replicating binlogs to MySQL, TiDB, Kafka or local files. If you need to replicate binlogs to other Drainer unsuppored destinations, you can set Drainer to replicate the binlog to Kafka and read the data in Kafka for customized processing according to binlog consumer protocol. See [Binlog Consumer Client User Guide](/tidb-binlog/binlog-consumer-client.md).

* To use TiDB Binlog for recovering incremental data, set the config `db-type` to `file` (local files in the proto buffer format). Drainer converts the binlog to data in the specified [proto buffer format](https://github.com/pingcap/tidb-binlog/blob/master/proto/pb_binlog.proto) and writes the data to local files. In this way, you can use [Reparo](/tidb-binlog/tidb-binlog-reparo.md) to recover data incrementally.

    Pay attention to the value of `db-type`:

    - If your TiDB version is earlier than 2.1.9, set `db-type="pb"`.
    - If your TiDB version is 2.1.9 or later, set `db-type="file"` or `db-type="pb"`.

* If the downstream is MySQL, MariaDB, or another TiDB cluster, you can use [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) to verify the data after data replication.

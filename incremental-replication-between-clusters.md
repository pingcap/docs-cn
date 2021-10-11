---
title: Replicate Incremental Data between TiDB Clusters in Real Time
summary: Learns how to replicate incremental data from one TiDB cluster to another cluster in real time
---

# Replicate Incremental Data between TiDB Clusters in Real Time

This document describes how to configure a TiDB cluster and its secondary MySQL or TiDB cluster, and how to replicate the incremental data from the primary cluster to the secondary cluster in real time.

If you need to configure a running TiDB cluster and its secondary cluster for replicating incremental data in real time, use the [Backup & Restore (BR)](/br/backup-and-restore-tool.md), [Dumpling](/dumpling-overview.md) and [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md).

## Implementation principles

Each transaction written to TiDB is allocated a unique commit timestamp (commit TS). Through this TS, you can get the global consistency status of a TiDB cluster.

The cluster data is exported using BR or Dumpling at a globally consistent point in time. Then starting from this point in time, TiDB Binlog is used to replicate incremental data. That is, the replication process is divided into two stages: full replication and incremental replication.

1. Perform a full backup and get the commit TS of the backup data.
2. Perform incremental replication. Make sure that the start time of incremental replication is the commit TS of the backup data.

> **Note:**
>
> The commit TS obtained after exporting the backup data is a closed interval. The initial-commit-ts obtained after starting the replication process using TiDB Binlog is an open interval.

## Replication process

Suppose that the existing cluster A works properly. First, you need to create a new cluster B as the secondary cluster of cluster A and then replicate the incremental data in cluster A to cluster B in real time. See the following steps for instruction.

### Step 1. Enable TiDB Binlog

Make sure that TiDB Binlog has been deployed and enabled in cluster A.

### Step 2. Export all cluster data

1. Export the data in cluster A (with global consistency ensured) to the specified path by using any of the following tools:

    - Use [BR for full backup](/br/use-br-command-line-tool.md#back-up-all-the-cluster-data)

    - Use [Dumpling to import full data](/dumpling-overview.md)

2. Obtain a globally consistent timestamp `COMMIT_TS`:

    - Use the BR `validate` command to obtain the backup timestamp. For example:

        {{< copyable "shell-regular" >}}

        ```shell
        COMMIT_TS=`br validate decode --field="end-version" -s local:///home/tidb/backupdata | tail -n1`
        ```

    - Or check the Dumpling metadata and obtain Pos (`COMMIT_TS`).

        {{< copyable "shell-regular" >}}

        ```shell
        cat metadata
        ```

        ```shell
        Started dump at: 2020-11-10 10:40:19
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 420747102018863124

        Finished dump at: 2020-11-10 10:40:20
        ```

3. Export the data in cluster A to cluster B.

### Step 3. Replicate incremental data

Modify the `drainer.toml` configuration file of TiDB Binlog by adding the following configuration to specify the `COMMIT_TS` from which TiDB Binlog starts replicating data to cluster B.

{{< copyable "" >}}

```toml
initial-commit-ts = COMMIT_TS
[syncer.to]
host = {the IP address of cluster B}
port = 3306
```

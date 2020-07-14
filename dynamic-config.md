---
title: Dynamic Configuration Change
summary: Learn how to use dynamic configuration change.
aliases: ['/docs/dev/dynamic-config/']
---

# Dynamic Configuration Change

This document describes how to use the dynamic configuration change feature.

> **Note:**
>
> This feature is experimental. It is **NOT** recommended to use this feature in the production environment.

The feature of dynamic configuration change is to online update the configuration of components (including TiKV and PD) using SQL statements.

Dynamic configuration change cannot be used to update the TiDB configuration. If you want to change the behavior of TiDB, modify TiDB's corresponding SQL variables.

## Common Operations

This section describes the common operations of dynamic configuration change.

### View instance configuration

To view the configuration of all instances in the cluster, use the `show config` SQL statement. The result is as follows:

{{< copyable "sql" >}}

```sql
show config;
```

```sql
+------+-----------------+-----------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Type | Instance        | Name                                                      | Value                                                                                                                                                                                                                                                                            |
+------+-----------------+-----------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb | 127.0.0.1:4001  | advertise-address                                         | 127.0.0.1                                                                                                                                                                                                                                                                        |
| tidb | 127.0.0.1:4001  | alter-primary-key                                         | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.binlog-socket                                      |                                                                                                                                                                                                                                                                                  |
| tidb | 127.0.0.1:4001  | binlog.enable                                             | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.ignore-error                                       | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.strategy                                           | range                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.write-timeout                                      | 15s                                                                                                                                                                                                                                                                              |
| tidb | 127.0.0.1:4001  | check-mb4-value-in-utf8                                   | true                                                                                                                                                                                                                                                                             |
...
```

You can filter the result in terms of fields. For example:

```sql
show config where type='tidb'
show config where instance in (...)
show config where name like '%log%'
show config where type='tikv' and name='log-level'
```

### Modify instance configuration

To modify configuration according to the instance address and type, use the `set config` SQL statement:

```sql
set config tikv log.level="info"
set config "127.0.0.1:2379" log.level="info"
```

If the modification is successful, `Query OK` is returned:

```sql
Query OK, 0 rows affected (0.01 sec)
```

If an error occurs during the batch modification, a warning is returned:

{{< copyable "sql" >}}

```sql
set config tikv log-level='warn';
```

```sql
Query OK, 0 rows affected, 1 warning (0.04 sec)
```

{{< copyable "sql" >}}

```sql
show warnings;
```

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                       |
+---------+------+---------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | bad request to http://127.0.0.1:20180/config: fail to update, error: "config log-level can not be change" |
+---------+------+---------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

To avoid confusing dynamic configuration with SQL variables, you can view TiDB configuration using `show config`, but you cannot modify the configuration, which causes an error. If you want to dynamically modify TiDB behaviors, use the corresponding SQL variables.

The names of some configuration items might conflict with TiDB keywords, such as `limit` and `key`. For these configuration items, use backtick `` ` `` to enclose them. For example, ``tikv-client.`store-limit` ``.

The batch modification operation cannot guarantee atomicity. On some instances, this operation might succeed, while on other instances, it might fail. If you modify the configuration of the entire TiKV cluster using `set tikv key=val`, your modification might fail on some instances. You can use `show warnings` to check the result.

## Supported parameters

This section lists the parameters supported by dynamic configuration change.

### PD

| Parameter | Description |
| :--- | :--- |
| `log.level` | The log level |
| `cluster-version` | The cluster version |
| `schedule.max-merge-region-size` | Controls the size limit of `Region Merge` (in MB) |
| `schedule.max-merge-region-keys` | Specifies the upper limit of the `Region Merge` key |
| `schedule.patrol-region-interval` | Determines the frequency at which `replicaChecker` checks the health state of a Region |
| `schedule.split-merge-interval` | Determines the time interval of performing split and merge operations on the same Region |
| `schedule.max-snapshot-count` | Determines the maximum number of snapshots that a single store can send or receive at one time |
| `schedule.max-pending-peer-count` | Determines the maximum number of pending peers in a single store |
| `schedule.max-store-down-time` | The downtime after which PD judges that the disconnected store can not be recovered |
| `schedule.leader-schedule-policy` | Determines the policy of Leader scheduling |
| `schedule.leader-schedule-limit` | The number of Leader scheduling tasks performed at the same time |
| `schedule.region-schedule-limit` | The number of Region scheduling tasks performed at the same time |
| `schedule.replica-schedule-limit` | The number of Replica scheduling tasks performed at the same time |
| `schedule.merge-schedule-limit` | The number of the `Region Merge` scheduling tasks performed at the same time |
| `schedule.hot-region-schedule-limit` | The number of hot Region scheduling tasks performed at the same time |
| `schedule.hot-region-cache-hits-threshold` | Determines the threshold at which a Region is considered hot |
| `schedule.high-space-ratio` | The threshold ratio below which the capacity of the store is sufficient |
| `schedule.low-space-ratio` | The threshold ratio above which the capacity of the store is insufficient |
| `schedule.tolerant-size-ratio` | Controls the `balance` buffer size|
| `schedule.enable-remove-down-replica` | Determines whether to enable the feature that automatically removes `DownReplica` |
| `schedule.enable-replace-offline-replica` | Determines whether to enable the feature that migrates `OfflineReplica` |
| `schedule.enable-make-up-replica` | Determines whether to enable the feature that automatically supplements replicas |
| `schedule.enable-remove-extra-replica` | Determines whether to enable the feature that removes extra replicas |
| `schedule.enable-location-replacement` | Determines whether to enable isolation level check |
| `schedule.enable-cross-table-merge` | Determines whether to enable cross-table merge |
| `schedule.enable-one-way-merge` | Enables one-way merge, which only allows merging with the next adjacent Region |
| `replication.max-replicas` | Sets the maximum number of replicas |
| `replication.location-labels` | The topology information of a TiKV cluster |
| `replication.enable-placement-rules` | Enables Placement Rules |
| `replication.strictly-match-label` | Enables the label check |
| `pd-server.use-region-storage` | Enables independent Region storage |
| `pd-server.max-gap-reset-ts` | Sets the maximum interval of resetting timestamp (BR) |
| `pd-server.key-type` | Sets the cluster key type |
| `pd-server.metric-storage` | Sets the storage address of the cluster metrics |
| `pd-server.dashboard-address` | Sets the dashboard address |
| `replication-mode.replication-mode` | Sets the backup mode |

For detailed parameter description, refer to [PD Configuration File](/pd-configuration-file.md).

### TiKV

| Parameter | Description |
| :--- | :--- |
| `refresh-config-interval` | The time interval at which the configuration is updated |
| `raftstore.sync-log` | Determines whether to force commits to be flushed to raft-log synchronously for persistent storage |
| `raftstore.raft-entry-max-size` | The maximum size of a single log |
| `raftstore.raft-log-gc-tick-interval` | The time interval at which the polling task of deleting Raft logs is scheduled |
| `raftstore.raft-log-gc-threshold` | The soft limit on the maximum allowable count of residual Raft logs |
| `raftstore.raft-log-gc-count-limit` | The hard limit on the allowable number of residual Raft logs|
| `raftstore.raft-log-gc-size-limit` | The hard limit on the allowable size of residual Raft logs |
| `raftstore.raft-entry-cache-life-time` | The maximum remaining time allowed for the log cache in memory |
| `raftstore.raft-reject-transfer-leader-duration` | Determines the smallest duration that a Leader is transferred to a newly added node |
| `raftstore.split-region-check-tick-interval` | The time interval at which to check whether the Region split is needed |
| `raftstore.region-split-check-diff` | The maximum value by which the Region data is allowed to exceed before Region split |
| `raftstore.region-compact-check-interval` | The time interval at which to check whether it is necessary to manually trigger RocksDB compaction |
| `raftstore.region-compact-check-step` | The number of Regions checked at one time for each round of manual compaction |
| `raftstore.region-compact-min-tombstones` | The number of tombstones required to trigger RocksDB compaction |
| `raftstore.region-compact-tombstones-percent` | The proportion of tombstone required to trigger RocksDB compaction |
| `raftstore.pd-heartbeat-tick-interval` | The time interval at which a Region's heartbeat to PD is triggered |
| `raftstore.pd-store-heartbeat-tick-interval` | The time interval at which a store's heartbeat to PD is triggered |
| `raftstore.snap-mgr-gc-tick-interval` | The time interval at which the recycle of expired snapshot files is triggered |
| `raftstore.snap-gc-timeout` | The longest time for which a snapshot file is saved |
| `raftstore.lock-cf-compact-interval` | The time interval at which TiKV triggers a manual compaction for the Lock Column Family |
| `raftstore.lock-cf-compact-bytes-threshold` | The size out of which TiKV triggers a manual compaction for the Lock Column Family |
| `raftstore.messages-per-tick` | The maximum number of messages processed per batch |
| `raftstore.max-peer-down-duration` | The longest inactive duration allowed for a peer |
| `raftstore.max-leader-missing-duration` | The longest duration allowed for a peer to be in the state where a Raft group is missing the leader. If this value is exceeded, the peer verifies with PD whether the peer has been deleted. |
| `raftstore.abnormal-leader-missing-duration` | The longest duration allowed for a peer to be in the state where a Raft group is missing the leader. If this value is exceeded, the peer is seen as abnormal and marked in metrics and logs. |
| `raftstore.peer-stale-state-check-interval` | The time interval to trigger the check for whether a peer is in the state where a Raft group is missing the leader |
| `raftstore.consistency-check-interval` | The time interval at which the consistency check is triggered |
| `raftstore.raft-store-max-leader-lease` | The longest trusted period of a Raft Leader |
| `raftstore.allow-remove-leader` | Determines whether to allow deleting the main switch |
| `raftstore.merge-check-tick-interval` | The time interval at which TiKV checks whether a Region needs merge |
| `raftstore.cleanup-import-sst-interval` | The time interval at which the expired SST file is checked |
| `raftstore.local-read-batch-size` | The maximum number of read requests processed in one batch |
| `coprocessor.split-region-on-table` | Enables to split Region by table |
| `coprocessor.batch-split-limit` | The threshold of Region split in batches |
| `coprocessor.region-max-size` | The maximum size of a Region |
| `coprocessor.region-split-size` | The size of the newly split Region |
| `coprocessor.region-max-keys` | The maximum number of keys allowed in a Region |
| `coprocessor.region-split-keys` | The number of keys in the newly split Region |
| `pessimistic-txn.wait-for-lock-timeout` | The max time that a pessimistic transaction in TiKV waits for other transactions to release the lock |
| `pessimistic-txn.wake-up-delay-duration` | The duration after which a pessimistic transaction is woken up |
| `gc.ratio-threshold` | The threshold at which Region GC is skipped (the number of GC versions/the number of keys) |
| `gc.batch-keys` | The number of keys processed in one batch |
| `gc.max-write-bytes-per-sec` | The max number of bytes that can be written into RocksDB per second |
| `{db-name}.max-total-wal-size` | The max size of total WAL |
| `{db-name}.max-background-jobs` | The number of background threads in RocksDB |
| `{db-name}.max-open-files` | The total number of files that RocksDB can open |
| `{db-name}.compaction-readahead-size` | The size of `readahead` when compaction is being performed |
| `{db-name}.bytes-per-sync` | The rate at which OS incrementally synchronizes files to disk while these files are being written asynchronously |
| `{db-name}.wal-bytes-per-sync` | The rate at which OS incrementally synchronizes WAL files to disk while the WAL files are being written |
| `{db-name}.writable-file-max-buffer-size` | The maximum buffer size used in WritableFileWrite |
| `{db-name}.{cf-name}.block-cache-size` | The cache size of a block |
| `{db-name}.{cf-name}.write-buffer-size` | The size of memtable |
| `{db-name}.{cf-name}.max-write-buffer-number` | The max number of memtables |
| `{db-name}.{cf-name}.max-bytes-for-level-base` | The maximum number of bytes at base level (L1) |
| `{db-name}.{cf-name}.target-file-size-base` | The size of the target file at base level |
| `{db-name}.{cf-name}.level0-file-num-compaction-trigger` | The maximum number of files at L0 that trigger compaction |
| `{db-name}.{cf-name}.level0-slowdown-writes-trigger` | The maximum number of files at L0 that trigger write stall |
| `{db-name}.{cf-name}.level0-stop-writes-trigger` | The maximum number of files at L0 required to completely block write |
| `{db-name}.{cf-name}.max-compaction-bytes` | The maximum number of bytes written into disk per compaction |
| `{db-name}.{cf-name}.max-bytes-for-level-multiplier` | The default amplification multiple for each layer |
| `{db-name}.{cf-name}.disable-auto-compactions` | Enables or disables automatic compaction |
| `{db-name}.{cf-name}.soft-pending-compaction-bytes-limit` | The soft limit on the pending compaction bytes |
| `{db-name}.{cf-name}.hard-pending-compaction-bytes-limit` | The hard limit on the pending compaction bytes |
| `{db-name}.{cf-name}.titan.blob-run-mode` | The mode of processing blob files |

In the table above, parameters with the `{db-name}` or `{db-name}.{cf-name}` prefix are configurations related to RocksDB. The optional values of `db-name` are `rocksdb` and `raftdb`.

- When `db-name` is `rocksdb`, the optional values of `cf-name` are `defaultcf`, `writecf`, `lockcf`, and `raftcf`.
- When `db-name` is `raftdb`, the value of `cf-name` can be `defaultcf`.

For detailed parameter description, refer to [TiKV Configuration File](/tikv-configuration-file.md).

---
title: TiDB 5.3.1 Release Notes
---

# TiDB 5.3.1 Release Notes

Release Date: March 3, 2022

TiDB version: 5.3.1

## Compatibility changes

- Tools

    + TiDB Lightning

        - Change the default value of `regionMaxKeyCount` from 1_440_000 to 1_280_000, to avoid too many empty Regions after data import [#30018](https://github.com/pingcap/tidb/issues/30018)

## Improvements

- TiDB

    - Optimize the mapping logic of user login mode to make the logging more MySQL-compatible [#30450](https://github.com/pingcap/tidb/issues/32648)

- TiKV

    - Reduce the TiCDC recovery time by reducing the number of the Regions that require the Resolve Locks step [#11993](https://github.com/tikv/tikv/issues/11993)
    - Speed up the Garbage Collection (GC) process by increasing the write batch size when performing GC to Raft logs [#11404](https://github.com/tikv/tikv/issues/11404)
    - Update the proc filesystem (procfs) to v0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)

- PD

    - Optimize the content format of the `DR_STATE` file [#4341](https://github.com/tikv/pd/issues/4341)

- Tools

    - TiCDC

        - Expose configuration parameters of the Kafka producer to make them configurable in TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - Add a pre-cleanup process upon TiCDC startup if S3 is used as backend storage [#3878](https://github.com/pingcap/tiflow/issues/3878)
        - The TiCDC client works when no certificate name is specified [#3627](https://github.com/pingcap/tiflow/issues/3627)
        - Manage sink checkpoints per table to avoid unexpected advance of checkpoint timestamps [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - Add the exponential backoff mechanism for restarting a changefeed. [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - Change the default value of Kafka Sink `partition-num` to 3 so that TiCDC distributes messages across Kafka partitions more evenly [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - Reduce the count of "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - Set the default value of `max-message-bytes` to 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)
        - Add more Prometheus and Grafana monitoring metrics and alerts, including `no owner alert`, `mounter row`, `table sink total row`, and `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        - Reduce the time for the KV client to recover when a TiKV store is down [#3191](https://github.com/pingcap/tiflow/issues/3191)

    - TiDB Lightning

        - Refine the output message of the precheck to make it more user-friendly when the local disk space check fails [#30395](https://github.com/pingcap/tidb/issues/30395)

## Bug fixes

- TiDB

    - Fix the issue that `date_format` in TiDB handles `'\n'` in a MySQL-incompatible way [#32232](https://github.com/pingcap/tidb/issues/32232)
    - Fix the issue that `alter column set default` wrongly updates the table schema [#31074](https://github.com/pingcap/tidb/issues/31074)
    - Fix a bug that `tidb_super_read_only` is not automatically enabled when `tidb_restricted_read_only` is enabled [#31745](https://github.com/pingcap/tidb/issues/31745)
    - Fix the issue that the `greatest` or `least` function with collation gets a wrong result [#31789](https://github.com/pingcap/tidb/issues/31789)
    - Fix the MPP task list empty error when executing a query [#31636](https://github.com/pingcap/tidb/issues/31636)
    - Fix wrong results of index join caused by an innerWorker panic [#31494](https://github.com/pingcap/tidb/issues/31494)
    - Fix wrong query results after changing the column type from `FLOAT` to `DOUBLE` [#31372](https://github.com/pingcap/tidb/issues/31372)
    - Fix the `invalid transaction` error when executing a query using index lookup join [#30468](https://github.com/pingcap/tidb/issues/30468)
    - Fix wrong query results due to the optimization of `Order By` [#30271](https://github.com/pingcap/tidb/issues/30271)
    - Fix the issue that the configurations of `MaxDays` and `MaxBackups` do not take effect on the slow log [#25716](https://github.com/pingcap/tidb/issues/25716)
    - Fix the issue that executing the `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` statement gets panic [#28078](https://github.com/pingcap/tidb/issues/28078)

- TiKV

    - Fix the panic issue caused by deleting snapshot files when the peer status is `Applying` [#11746](https://github.com/tikv/tikv/issues/11746)
    - Fix the issue of QPS drop when flow control is enabled and `level0_slowdown_trigger` is set explicitly [#11424](https://github.com/tikv/tikv/issues/11424)
    - Fix the panic issue that occurs when the cgroup controller is not mounted [#11569](https://github.com/tikv/tikv/issues/11569)
    - Fix the issue that the latency of Resolved TS increases after TiKV stops operating [#11351](https://github.com/tikv/tikv/issues/11351)
    - Fix a bug that TiKV cannot delete a range of data (`unsafe_destroy_range` cannot be executed) when the GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    - Fix the issue that destroying a peer might cause high latency [#10210](https://github.com/tikv/tikv/issues/10210)
    - Fix a bug that the `any_value` function returns a wrong result when regions are empty [#11735](https://github.com/tikv/tikv/issues/11735)
    - Fix the issue that deleting an uninitialized replica might cause an old replica to be recreated [#10533](https://github.com/tikv/tikv/issues/10533)
    - Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#11526](https://github.com/tikv/tikv/issues/11526)
    - Fix the deadlock issue that happens occasionally when coroutines run too fast [#11549](https://github.com/tikv/tikv/issues/11549)
    - Fix the issue that a down TiKV node causes the resolved timestamp to lag [#11351](https://github.com/tikv/tikv/issues/11351)
    - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    - Fix the issue that TiKV cannot detect the memory lock when TiKV performs a reverse table scan [#11440](https://github.com/tikv/tikv/issues/11440)
    - Fix the issue that RocksDB flush or compaction causes panic when the disk capacity is full [#11224](https://github.com/tikv/tikv/issues/11224)
    - Fix a bug that tikv-ctl cannot return the correct Region-related information [#11393](https://github.com/tikv/tikv/issues/11393)
    - Fix the issue that the average latency of the by-instance gRPC requests is inaccurate in TiKV metrics [#11299](https://github.com/tikv/tikv/issues/11299)

- PD

    - Fix a bug that the scheduling process has the unnecessary JointConsensus steps in certain cases [#4362](https://github.com/tikv/pd/issues/4362)
    - Fix a bug that the scheduling cannot be executed when demoting a voter directly [#4444](https://github.com/tikv/pd/issues/4444)
    - Fix a data race issue that occurs when updating the configuration of the replication mode of replicas [#4325](https://github.com/tikv/pd/issues/4325)
    - Fix a bug that the Read lock is not released in certain cases [#4354](https://github.com/tikv/pd/issues/4354)
    - Fix the issue that the cold hotspot data cannot be deleted from the hotspot statistics [#4390](https://github.com/tikv/pd/issues/4390)

- TiFlash

    - Fix the issue that `cast(arg as decimal(x,y))` returns a wrong result when the input argument `arg` overflows the range of `decimal(x,y)`
    - Fix the TiFlash crash issue that occurs when `max_memory_usage` and `max_memory_usage_for_all_queries` are enabled
    - Fix the issue that `cast(string as real)` returns a wrong result
    - Fix the issue that `cast(string as decimal)` returns a wrong result
    - Fix potential data inconsistency after altering a primary key column to a larger int data type
    - Fix the bug that when `in` has multiple arguments in the statements like `select (arg0, arg1) in (x,y)`, `in` returns a wrong result
    - Fix the issue that TiFlash might panic when an MPP query is stopped
    - Fix the issue that `str_to_date` returns a wrong result when the input argument has leading zeros
    - Fix the issue that the query returns a wrong result when the filter is in the `where <string>` format
    - Fix the issue that `cast(string as datetime)` returns a wrong result when the input argument `string` is in the `%Y-%m-%d\n%H:%i:%s` format

- Tools

    - Backup & Restore (BR)

        - Fix the potential issue that Regions might be unevenly distributed after a restore operation is finished [#31034](https://github.com/pingcap/tidb/issues/31034)

    - TiCDC

        - Fix a bug that long varchars report an error `Column length too big` [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - Fix a bug that a TiCDC node exits abnormally when a PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - Fix the issue that execution errors of the update statement in safemode may cause the DM-worker panic [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - Fix the issue that cached region metric of the TiKV client may be negative [#4300](https://github.com/pingcap/tiflow/issues/4300)
        - Fix the bug that HTTP API panics when the required processor information does not exist [#3840](https://github.com/pingcap/tiflow/issues/3840)
        - Fix a bug that redo logs are not cleaned up when removing a paused changefeed [#4740](https://github.com/pingcap/tiflow/issues/4740)
        - Fix OOM in container environments [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - Fix a bug that stopping a loading task results in unexpected transfer of the task [#3771](https://github.com/pingcap/tiflow/issues/3771)
        - Fix the issue that wrong progress is returned for the `query-status` command on loader [#3252](https://github.com/pingcap/tiflow/issues/3252)
        - Fix the issue that HTTP API fails to work if there are TiCDC nodes of different versions in a cluster [#3483](https://github.com/pingcap/tiflow/issues/3483)
        - Fix the issue that TiCDC exits abnormally when the S3 storage is configured with TiCDC Redo Log [#3523](https://github.com/pingcap/tiflow/issues/3523)
        - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Fix a bug that MySQL sink generates duplicated `replace` SQL statements if `batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - Fix the issue that syncer metrics are updated only when querying the status [#4281](https://github.com/pingcap/tiflow/issues/4281)
        - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix the issue that replication cannot be performed when `min.insync.replicas` is smaller than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix the potential panic issue that occurs when a replication task is removed [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - Fix the potential issue that the deadlock causes a replication task to get stuck [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - Fix the TiCDC panic issue that occurs when manually cleaning the task status in etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - Fix the issue that special comments in DDL statements cause the replication task to stop [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - Fix the issue of replication stop caused by the incorrect configuration of `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - Fix the issue that the service cannot be started because of a timezone issue in some RHEL releases [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix the issue that `stopped` changefeeds resume automatically after a cluster upgrade [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Fix the issue of overly frequent warnings caused by MySQL sink deadlock [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - Fix the bug that the `enable-old-value` configuration item is not automatically set to `true` on Canal and Maxwell protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - Fix the issue that Avro sink does not support parsing JSON type columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/tiflow/issues/3010)

    - TiDB Data Migration (DM)

        - Fix a bug that the relay status in the DM-master is wrong after restarting the DM-master and DM-worker in a particular order [#3478](https://github.com/pingcap/tiflow/issues/3478)
        - Fix a bug that the DM-worker fails to boot up after a restart [#3344](https://github.com/pingcap/tiflow/issues/3344)
        - Fix a bug that a DM task fails if running a PARTITION DDL takes too long time [#3854](https://github.com/pingcap/tiflow/issues/3854)
        - Fix a bug that DM may report `invalid sequence` when upstream is MySQL 8.0 [#3847](https://github.com/pingcap/tiflow/issues/3847)
        - Fix a bug of data loss when DM does finer grained retry [#3487](https://github.com/pingcap/tiflow/issues/3487)
        - Fix the issue that the `CREATE VIEW` statement interrupts data replication [#4173](https://github.com/pingcap/tiflow/issues/4173)
        - Fix the issue the schema needs to be reset after a DDL statement is skipped [#4177](https://github.com/pingcap/tiflow/issues/4177)

    - TiDB Lightning

        - Fix the bug that TiDB Lightning may not delete the metadata schema when some import tasks do not contain source files [#28144](https://github.com/pingcap/tidb/issues/28144)
        - Fix the bug that TiDB Lightning returns an error if the storage URL prefix is "gs://xxx", instead of "gcs://xxx" [#32742](https://github.com/pingcap/tidb/issues/32742)
        - Fix the issue that setting --log-file="-" does not print any log to stdout [#29876](https://github.com/pingcap/tidb/issues/29876)
        - Fix the issue that TiDB Lightning does not report errors when the S3 storage path does not exist [#30709](https://github.com/pingcap/tidb/issues/30709)

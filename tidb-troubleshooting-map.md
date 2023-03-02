---
title: TiDB Troubleshooting Map
summary: Learn how to troubleshoot common errors in TiDB.
aliases: ['/docs/dev/tidb-troubleshooting-map/','/docs/dev/how-to/troubleshoot/diagnose-map/']
---

# TiDB Troubleshooting Map

This document summarizes common issues in TiDB and other components. You can use this map to diagnose and solve issues when you encounter related problems.

## 1. Service Unavailable

### 1.1 The client reports `Region is Unavailable` error

- 1.1.1 The `Region is Unavailable` error is usually because a Region is not available for a period of time. You might encounter `TiKV server is busy`, or the request to TiKV fails due to `not leader` or `epoch not match`, or the request to TiKV time out. In such cases, TiDB performs a `backoff` retry mechanism. When the `backoff` exceeds a threshold (20s by default), the error will be sent to the client. Within the `backoff` threshold, this error is not visible to the client.

- 1.1.2 Multiple TiKV instances are OOM at the same time, which causes no Leader during the OOM period. See [case-991](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case991.md) in Chinese.

- 1.1.3 TiKV reports `TiKV server is busy`, and exceeds the `backoff` time. For more details, refer to [4.3](#43-the-client-reports-the-server-is-busy-error). `TiKV server is busy` is a result of the internal flow control mechanism and should not be counted in the `backoff` time. This issue will be fixed.

- 1.1.4 Multiple TiKV instances failed to start, which causes no Leader in a Region. When multiple TiKV instances are deployed in a physical machine, the failure of the physical machine can cause no Leader in a Region if the label is not properly configured. See [case-228](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case228.md) in Chinese.

- 1.1.5 When a Follower apply is lagged in a previous epoch, after the Follower becomes a Leader, it rejects the request with `epoch not match`. See [case-958](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case958.md) in Chinese (TiKV needs to optimize its mechanism).

### 1.2 PD errors cause service unavailable

Refer to [5 PD issues](#5-pd-issues).

## 2. Latency increases significantly

### 2.1 Transient increase

- 2.1.1 Wrong TiDB execution plan causes latency increase. Refer to [3.3](#33-wrong-execution-plan).
- 2.1.2 PD Leader election issue or OOM. Refer to [5.2](#52-pd-election) and [5.3](#53-pd-oom).
- 2.1.3 A significant number of Leader drops in some TiKV instances. Refer to [4.4](#44-some-tikv-nodes-drop-leader-frequently).
- 2.1.4 For other causes, see [Troubleshoot Increased Read and Write Latency](/troubleshoot-cpu-issues.md).

### 2.2 Persistent and significant increase

- 2.2.1 TiKV single thread bottleneck

    - Too many Regions in a TiKV instance causes a single gRPC thread to be the bottleneck (Check the **Grafana** -> **TiKV-details** -> **Thread CPU/gRPC CPU Per Thread** metric). In v3.x or later versions, you can enable `Hibernate Region` to resolve the issue. See [case-612](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case612.md) in Chinese.

    - For versions earlier than v3.0, when the raftstore thread or the apply thread becomes the bottleneck (**Grafana** -> **TiKV-details** -> **Thread CPU/raft store CPU** and **Async apply CPU** metrics exceed `80%`), you can scale out TiKV (v2.x) instances or upgrade to v3.x with multi-threading. <!-- See [case-517](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese. -->

- 2.2.2 CPU load increases.

- 2.2.3 TiKV slow write. Refer to [4.5](#45-tikv-write-is-slow).

- 2.2.4 TiDB wrong execution plan. Refer to [3.3](#33-wrong-execution-plan).

- 2.2.5 For other causes, see [Troubleshoot Increased Read and Write Latency](/troubleshoot-cpu-issues.md).

## 3. TiDB issues

### 3.1 DDL

- 3.1.1 An error `ERROR 1105 (HY000): unsupported modify decimal column precision` is reported when you modify the length of the `decimal` field.<!--See [case-1004](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese.--> TiDB does not support changing the length of the `decimal` field.

- 3.1.2 TiDB DDL job hangs or executes slowly (use `admin show ddl jobs` to check DDL progress)

    - Cause 1: Network issue with other components (PD/TiKV).

    - Cause 2: Early versions of TiDB (earlier than v3.0.8) have heavy internal load because of a lot of goroutine at high concurrency.

    - Cause 3: In early versions (v2.1.15 & versions < v3.0.0-rc1), PD instances fail to delete TiDB keys, which causes every DDL change to wait for two leases.

    - For other unknown causes, [report a bug](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&template=bug-report.md).

    - Solution:

        - For cause 1, check the network connection between TiDB and TiKV/PD.
        - For cause 2 and 3, the issues are already fixed in later versions. You can upgrade TiDB to a later version.
        - For other causes, you can use the following solution of migrating the DDL owner.

    - DDL owner migration:

        - If you can connect to the TiDB server, execute the owner election command again: `curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`
        - If you cannot connect to the TiDB server, use `tidb-ctl` to delete the DDL owner from the etcd of the PD cluster to trigger re-election: `tidb-ctl etcd delowner [LeaseID] [flags] + ownerKey`

- 3.1.3 TiDB reports `information schema is changed` error in log

    - For the detailed causes and solution, see [Why the `Information schema is changed` error is reported](/faq/sql-faq.md#what-triggers-the-information-schema-is-changed-error).

    - Background: The increased number of `schema version` is consistent with the number of `schema state` of each DDL change operation. For example, the `create table` operation has 1 version change, and the `add column` operation has 4 version changes. Therefore, too many column change operations might cause `schema version` to increase fast. For details, refer to [online schema change](https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41376.pdf).

- 3.1.4 TiDB reports `information schema is out of date` in log

    - Cause 1: The TiDB server that is executing the DML statement is stopped by `graceful kill` and prepares to exit. The execution time of the transaction that contains the DML statement exceeds one DDL lease. An error is reported when the transaction is committed.

    - Cause 2: The TiDB server cannot connect to PD or TiKV when it is executing the DML statement. As a result, the TiDB server did not load the new schema within one DDL lease (`45s` by default), or the TiDB server disconnects from PD with the `keep alive` setting.

    - Cause 3: TiKV has high load or network timed out. Check the node loads in **Grafana** -> **TiDB** and **TiKV**.

    - Solution:

        - For cause 1, retry the DML operation when TiDB is started.
        - For cause 2, check the network between the TiDB server and PD/TiKV.
        - For cause 3, investigate why TiKV is busy. Refer to [4 TiKV issues](#4-tikv-issues).

### 3.2 OOM issues

- 3.2.1 Symptom

    - Client: The client reports the error `ERROR 2013 (HY000): Lost connection to MySQL server during query`.

    - Check the log

        - Execute `dmesg -T | grep tidb-server`. The result shows the OOM-killer log around the time point when the error occurs.

        - Grep the "Welcome to TiDB" log in `tidb.log` around the time point after the error occurs (namely, the time when tidb-server restarts).

        - Grep `fatal error: runtime: out of memory` or `cannot allocate memory` in `tidb_stderr.log`.

        - In v2.1.8 or earlier versions, you can grep `fatal error: stack overflow` in the `tidb_stderr.log`.

    - Monitor: The memory usage of tidb-server instances increases sharply in a short period of time.

- 3.2.2 Locate the SQL statement that causes OOM. (Currently all versions of TiDB cannot locate SQL accurately. You still need to analyze whether OOM is caused by the SQL statement after you locate one.)

    - For versions >= v3.0.0, grep "expensive_query" in `tidb.log`. That log message records SQL queries that timed out or exceed memory quota.
    - For versions < v3.0.0, grep "memory exceeds quota" in `tidb.log` to locate SQL queries that exceed memory quota.

  > **Note:**
  >
  > The default threshold for a single SQL memory usage is `1GB`. You can set this parameter by configuring the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query).

- 3.2.3 Mitigate OOM issues

    - By enabling `SWAP`, you can mitigate the OOM issue caused by overuse of memory by large queries. When the memory is insufficient, this method can have impact on the performance of large queries due to the I/O overhead. The degree to which the performance is affected depends on the remaining memory space and the disk I/O speed.

- 3.2.4 Typical reasons for OOM

    - The SQL query has `join`. If you view the SQL statement by using `explain`, you can find that the `join` operation selects the `HashJoin` algorithm and the `inner` table is large.

    - The data volume of a single `UPDATE/DELETE` query is too large. See [case-882](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case882.md) in Chinese.

    - The SQL contains multiple sub-queries connected by `Union`. See [case-1828](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1828.md) in Chinese.

For more information about troubleshooting OOM, see [Troubleshoot TiDB OOM Issues](/troubleshoot-tidb-oom.md).

### 3.3 Wrong execution plan

- 3.3.1 Symptom

    - SQL query execution time is much longer compared with that of previous executions, or the execution plan suddenly changes. If the execution plan is logged in the slow log, you can directly compare the execution plans.

    - SQL query execution time is much longer compared with that of other databases such as MySQL. Compare the execution plan with other databases to see the differences, such as `Join Order`.

    - In slow log, the number of SQL execution time `Scan Keys` is large.

- 3.3.2 Investigate the execution plan

    - `explain analyze {SQL}`. When the execution time is acceptable, compare `count` in the result of `explain analyze` and the number of `row` in `execution info`. If a large difference is found in the `TableScan/IndexScan` row, it is likely that the statistics is incorrect. If a large difference is found in other rows, the problem might not be in the statistics.

    - `select count(*)`. When the execution plan contains a `join` operation, `explain analyze` might take a long time. You can check whether the problem is in the statistics by executing `select count(*)` for the conditions on `TableScan/IndexScan` and comparing the `row count` information in the `explain` result.

- 3.3.3 Mitigation

    - For v3.0 and later versions, use the `SQL Bind` feature to bind the execution plan.

    - Update the statistics. If you are roughly sure that the problem is caused by the statistics, [dump the statistics](/statistics.md#export-statistics). If the cause is outdated statistics, such as the `modify count/row count` in `show stats_meta` is greater than a certain value (for example, 0.3), or the table has an index of time column, you can try recovering by using `analyze table`. If `auto analyze` is configured, check whether the `tidb_auto_analyze_ratio` system variable is too large (for example, greater than 0.3), and whether the current time is between `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time`.

    - For other situations, [report a bug](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&template=bug-report.md).

### 3.4 SQL execution error

- 3.4.1 The client reports the `ERROR 1265(01000) Data Truncated` error. This is because the way TiDB internally calculates the precision of `Decimal` type is incompatible with that of MySQL. This issue has been fixed in v3.0.10 ([#14438](https://github.com/pingcap/tidb/pull/14438)).

    - Cause:

        In MySQL, if two large-precision `Decimal` are divided and the result exceeds the maximum decimal precision (`30`), only `30` digits are reserved and no error is reported;

        In TiDB, the calculation result is the same as in MySQL, but inside the data structure that represents `Decimal`, a field for decimal precision still retains the actual precision.

        Take `(0.1^30) / 10` as an example. The results in TiDB and MySQL are both `0`, because the precision is `30` at most. However, in TiDB, the field for decimal precision is still `31`.

        After multiple `Decimal` divisions, even though the result is correct, this precision field could grow larger and larger, and eventually exceeds the threshold in TiDB (`72`), and the `Data Truncated` error is reported.

        The multiplication of `Decimal` does not have this issue, because the out-of-bounds is bypassed, and the precision is set to the maximum precision limit.

    - Solution: You can bypass this issue by manually adding `Cast(xx as decimal(a, b))`, in which `a` and `b` are the target precisions.

### 3.5 Slow query issues

To identify slow queries, see [Identify slow queries](/identify-slow-queries.md). To analyze and handle slow queries, see [Analyze slow queries](/analyze-slow-queries.md).

### 3.6 Hotspot issues

As a distributed database, TiDB has a load balancing mechanism to distribute the application loads as evenly as possible to different computing or storage nodes, to make better use of server resources. However, in certain scenarios, some application loads cannot be well distributed, which can affect the performance and form a single point of high load, also known as a hotspot.

TiDB provides a complete solution to troubleshooting, resolving or avoiding hotspots. By balancing load hotspots, overall performance can be improved, including improving QPS and reducing latency. For detailed solutions, see [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md).

### 3.7 High disk I/O usage

If TiDB's response slows down after you have troubleshot the CPU bottleneck and the bottleneck caused by transaction conflicts, you need to check I/O metrics to help determine the current system bottleneck. For how to locate and handle the issue of high I/O usage in TiDB, see [Troubleshoot High Disk I/O Usage](/troubleshoot-high-disk-io.md).

### 3.8 Lock conflicts

TiDB supports complete distributed transactions. Starting from v3.0, TiDB provides optimistic transaction mode and pessimistic transaction mode. To learn how to troubleshoot lock-related issues and how to handle optimistic and pessimistic lock conflicts, see [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md).

### 3.9 Inconsistency between data and indexes

TiDB checks consistency between data and indexes when it executes transactions or the [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) statement. If the check finds that a record key-value and the corresponding index key-value are inconsistent, that is, a key-value pair storing row data and the corresponding key-value pair storing its index are inconsistent (for example, more indexes or missing indexes), TiDB reports a data inconsistency error and prints the related errors in error logs.

To learn more about the inconsistency error and how to bypass the check, see [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md).

## 4. TiKV issues

### 4.1 TiKV panics and fails to start

- 4.1.1 `sync-log = false`. The `unexpected raft log index: last_index X < applied_index Y` error is returned after the machine is powered off.

    This issue is expected. You can restore the Region using `tikv-ctl`.

- 4.1.2 If TiKV is deployed on a virtual machine, when the virtual machine is killed or the physical machine is powered off, the `entries[X, Y] is unavailable from storage` error is reported.

    This issue is expected. The `fsync` of virtual machines is not reliable, so you need to restore the Region using `tikv-ctl`.

- 4.1.3 For other unexpected causes, [report a bug](https://github.com/tikv/tikv/issues/new?template=bug-report.md).

### 4.2 TiKV OOM

- 4.2.1 If the `block-cache` configuration is too large, it might cause OOM.

    To verify the cause of the problem, check the `block cache size` of RocksDB by selecting the corresponding instance in the monitor **Grafana** -> **TiKV-details**.

    Meanwhile, check whether the `[storage.block-cache] capacity = # "1GB"`parameter is set properly. By default, TiKV's `block-cache` is set to `45%` of the total memory of the machine. You need to explicitly specify this parameter when you deploy TiKV in the container, because TiKV obtains the memory of the physical machine, which might exceed the memory limit of the container.

- 4.2.2 Coprocessor receives many large queries and returns a large volume of data. gRPC fails to send data as quickly as the coprocessor returns data, which results in OOM.

    To verify the cause, you can check whether `response size` exceeds the `network outbound` traffic by viewing the monitor **Grafana** -> **TiKV-details** -> **coprocessor overview**.

- 4.2.3 Other components occupy too much memory.

    This issue is unexpected. You can [report a bug](https://github.com/tikv/tikv/issues/new?template=bug-report.md).

### 4.3 The client reports the `server is busy` error

Check the specific cause for busy by viewing the monitor **Grafana** -> **TiKV** -> **errors**. `server is busy` is caused by the flow control mechanism of TiKV, which informs `tidb/ti-client` that TiKV is currently under too much pressure and will retry later.

- 4.3.1 TiKV RocksDB encounters `write stall`.

    A TiKV instance has two RocksDB instances, one in `data/raft` to save the Raft log, another in `data/db` to save the real data. You can check the specific cause for stall by running `grep "Stalling" RocksDB` in the log. The RocksDB log is a file starting with `LOG`, and `LOG` is the current log.

    - Too many `level0 sst` causes stall. You can add the `[rocksdb] max-sub-compactions = 2` (or 3) parameter to speed up `level0 sst` compaction. The compaction task from level0 to level1 is divided into several subtasks (the max number of subtasks is the value of `max-sub-compactions`) to be executed concurrently. See [case-815](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case815.md) in Chinese.

    - Too many `pending compaction bytes` causes stall. The disk I/O fails to keep up with the write operations in business peaks. You can mitigate this problem by increasing the `soft-pending-compaction-bytes-limit` and `hard-pending-compaction-bytes-limit` of the corresponding CF.

        - The default value of `[rocksdb.defaultcf] soft-pending-compaction-bytes-limit` is `64GB`. If the pending compaction bytes reaches the threshold, RocksDB slows down the write speed. You can set `[rocksdb.defaultcf] soft-pending-compaction-bytes-limit` to `128GB`.

        - The default value of `hard-pending-compaction-bytes-limit` is `256GB`. If the pending compaction bytes reaches the threshold (this is not likely to happen, because RocksDB slows down the write after the pending compaction bytes reaches `soft-pending-compaction-bytes-limit`), RocksDB stops the write operation. You can set `hard-pending-compaction-bytes-limit` to `512GB`.<!-- See [case-275](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case275.md) in Chinese.-->

        - If the disk I/O capacity fails to keep up with the write for a long time, it is recommended to scale up your disk. If the disk throughput reaches the upper limit and causes write stall (for example, the SATA SSD is much lower than NVME SSD), while the CPU resources is sufficient, you may apply a compression algorithm of higher compression ratio. This way, the CPU resources is traded for disk resources, and the pressure on the disk is eased.

        - If the default CF compaction sees a high pressure, change the `[rocksdb.defaultcf] compression-per-level` parameter from `["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]` to `["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`.

    - Too many memtables causes stall. This usually occurs when the amount of instant writes is large and the memtables flush to the disk slowly. If the disk write speed cannot be improved, and this issue only occurs during business peaks, you can mitigate it by increasing the `max-write-buffer-number` of the corresponding CF.

        - For example, set `[rocksdb.defaultcf] max-write-buffer-number` to `8` (`5` by default). Note that this might cause more memory usage in the peak, because more memtables might be in the memory.

- 4.3.2 `scheduler too busy`

    - Serious write conflict. `latch wait duration` is high. You can view `latch wait duration` in the monitor **Grafana** -> **TiKV-details** -> **scheduler prewrite**/**scheduler commit**. When the write tasks pile up in the scheduler, the pending write tasks exceed the threshold set in `[storage] scheduler-pending-write-threshold` (100MB). You can verify the cause by viewing the metric corresponding to `MVCC_CONFLICT_COUNTER`.

    - Slow write causes write tasks to pile up. The data being written to TiKV exceeds the threshold set by `[storage] scheduler-pending-write-threshold` (100MB). Refer to [4.5](#45-tikv-write-is-slow).

- 4.3.3 `raftstore is busy`. The processing of messages is slower than the receiving of messages. The short-term `channel full` status does not affect the service, but if the error persists for a long time, it might cause Leader switch.

    - `append log` encounters stall. Refer to [4.3.1](#43-the-client-reports-the-server-is-busy-error).
    - `append log duration` is high, which causes slow processing of messages. You can refer to [4.5](#45-tikv-write-is-slow) to analyze why `append log duration` is high.
    - raftstore receives a large batch of messages in an instant (check in the TiKV Raft messages dashboard), and fails to process them. Usually the short-term `channel full` status does not affect the service.

- 4.3.4 TiKV coprocessor is in a queue. The number of piled up tasks exceeds `coprocessor threads * readpool.coprocessor.max-tasks-per-worker-[normal|low|high]`. Too many large queries leads to the tasks piling up in coprocessor. You need to check whether a execution plan change causes a large number of table scan operations. Refer to [3.3](#33-wrong-execution-plan).

### 4.4 Some TiKV nodes drop Leader frequently

- 4.4.1 Re-election because TiKV is restarted

    - After TiKV panics, it is pulled up by systemd and runs normally. You can check whether panic has occurred by viewing the TiKV log. Because this issue is unexpected, [report a bug](https://github.com/tikv/tikv/issues/new?template=bug-report.md) if it happens.

    - TiKV is stopped or killed by a third party and then pulled up by systemd. Check the cause by viewing `dmesg` and the TiKV log.

    - TiKV is OOM, which causes restart. Refer to [4.2](#42-tikv-oom).

    - TiKV is hung because of dynamically adjusting `THP` (Transparent Hugepage). See case [case-500](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case500.md) in Chinese.

- 4.4.2 TiKV RocksDB encounters write stall and thus results in re-election. You can check if the monitor **Grafana** -> **TiKV-details** -> **errors** shows `server is busy`. Refer to [4.3.1](#43-the-client-reports-the-server-is-busy-error).

- 4.4.3 Re-election because of network isolation.

### 4.5 TiKV write is slow

- 4.5.1 Check whether the TiKV write is low by viewing the `prewrite/commit/raw-put` duration of TiKV gRPC (only for RawKV clusters). Generally, you can locate the slow phase according to the [performance-map](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png). Some common situations are listed as follows.

- 4.5.2 The scheduler CPU is busy (only for transaction kv).

    The `scheduler command duration` of prewrite/commit is longer than the sum of `scheduler latch wait duration` and `storage async write duration`. The scheduler worker has a high CPU demand, such as over 80% of `scheduler-worker-pool-size` * 100%, or the CPU resources of the entire machine are relatively limited. If the write workload is large, check if `[storage] scheduler-worker-pool-size` is set too small.

    For other situations, [report a bug](https://github.com/tikv/tikv/issues/new?template=bug-report.md).

- 4.5.3 Append log is slow.

    The **Raft IO**/`append log duration` in TiKV Grafana is high, usually because the disk write operation is slow. You can verify the cause by checking the `WAL Sync Duration max` value of RocksDB - raft.

    For other situations, [report a bug](https://github.com/tikv/tikv/issues/new?template=bug-report.md).

- 4.5.4 The raftstore thread is busy.

    The **Raft Propose**/`propose wait duration` is significantly larger than the append log duration in TiKV Grafana. Take the following methods:

    - Check whether the `[raftstore] store-pool-size` configuration value is too small. It is recommended to set the value between `1` and `5` and not too large.
    - Check whether the CPU resources on the machine are insufficient.

- 4.5.5 Apply is slow.

    The **Raft IO**/`apply log duration` in TiKV Grafana is high, which usually comes with a high **Raft Propose**/`apply wait duration`. The possible causes are as follows:

    - `[raftstore] apply-pool-size` is too small (it is recommended to set the value between `1` and `5` and not too large), and the **Thread CPU**/`apply CPU` is large.

    - The CPU resources on the machine are insufficient.

    - Region write hot spot. A single apply thread has high CPU usage. Currently, we cannot properly address the hot spot problem on a single Region, which is being improved. To view the CPU usage of each thread, modify the Grafana expression and add `by (instance, name)`.

    - RocksDB write is slow. **RocksDB kv**/`max write duration` is high. A single Raft log might contain multiple KVs. When writing into RocksDB, 128 KVs are written into RocksDB in a write batch. Therefore, an apply log might be associated with multiple writes in RocksDB.

    - For other situations, [report a bug](https://github.com/tikv/tikv/issues/new?template=bug-report.md).

- 4.5.6 Raft commit log is slow.

    The **Raft IO**/`commit log duration` in TiKV Grafana is high (this metric is only supported in Grafana after v4.x). Every Region corresponds to an independent Raft group. Raft has a flow control mechanism, similar to the sliding window mechanism of TCP. You can control the size of the sliding window by configuring the `[raftstore] raft-max-inflight-msgs = 256` parameter. If there is a write hot spot and the `commit log duration` is high, you can adjust the parameter, such as increasing it to `1024`.

- 4.5.7 For other situations, refer to the write path on [performance-map](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png) and analyze the cause.

## 5. PD issues

### 5.1 PD scheduling

- 5.1.1 Merge

    - Empty Regions across tables cannot be merged. You need to modify the `[coprocessor] split-region-on-table` parameter in TiKV, which is set to `false` in v4.x by default. See [case-896](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case896.md) in Chinese.

    - Region merge is slow. You can check whether the merged operator is generated by accessing the monitor dashboard in **Grafana** -> **PD** -> **operator**. To accelerate the merge, increase the value of `merge-schedule-limit`.

- 5.1.2 Add replicas or take replicas online/offline

    - The TiKV disk uses 80% of the capacity, and PD does not add replicas. In this situation, the number of miss peers increases, so TiKV needs to be scaled out. See [case-801](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case801.md) in Chinese.

    - When a TiKV node is taken offline, some Region cannot be migrated to other nodes. This issue has been fixed in v3.0.4 ([#5526](https://github.com/tikv/tikv/pull/5526)). See [case-870](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case870.md) in Chinese.

- 5.1.3 Balance

    - The Leader/Region count is not evenly distributed. See [case-394](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case394.md) and [case-759](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case759.md) in Chinese. The major cause is that the balance performs scheduling based on the size of Region/Leader, so this might result in the uneven distribution of the count. In TiDB 4.0, the `[leader-schedule-policy]` parameter is introduced, which enables you to set the scheduling policy of Leader to be `count`-based or `size`-based.

### 5.2 PD election

- 5.2.1 PD switches Leader.

    - Cause 1: Disk. The disk where the PD node is located has full I/O load. Investigate whether PD is deployed with other components with high I/O demand and the health of the disk. You can verify the cause by viewing the monitor metrics in **Grafana** -> **disk performance** -> **latency**/**load**. You can also use the FIO tool to run a check on the disk if necessary. See [case-292](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case292.md) in Chinese.

    - Cause 2: Network. The PD log shows `lost the TCP streaming connection`. You need to check whether there is a problem with the network between PD nodes and verify the cause by viewing `round trip` in the monitor **Grafana** -> **PD** -> **etcd**. See [case-177](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case177.md) in Chinese.

    - Cause 3: High system load. The log shows `server is likely overloaded`. See [case-214](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case214.md) in Chinese.

- 5.2.2 PD cannot elect a Leader or the election is slow.

    - PD cannot elect a Leader: The PD log shows `lease is not expired`. [This issue](https://github.com/etcd-io/etcd/issues/10355) has been fixed in v3.0.x and v2.1.19. See [case-875](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case875.md) in Chinese.

    - The election is slow: The Region loading duration is long. You can check this issue by running `grep "regions cost"` in the PD log. If the result is in seconds, such as `load 460927 regions cost 11.77099s`, it means the Region loading is slow. You can enable the `region storage` feature in v3.0 by setting `use-region-storage` to `true`, which significantly reduce the Region loading duration. See [case-429](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case429.md) in Chinese.

- 5.2.3 PD timed out when TiDB executes SQL statements.

    - PD doesn't have a Leader or switches Leader. Refer to [5.2.1](#52-pd-election) and [5.2.2](#52-pd-election).

    - Network issue. Check whether the network from TiDB to PD Leader is running normally by accessing the monitor **Grafana** -> **blackbox_exporter** -> **ping latency**.

    - PD panics. [Report a bug](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&template=bug-report.md).

    - PD is OOM. Refer to [5.3](#53-pd-oom).

    - If the issue has other causes, get goroutine by running `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2` and [report a bug](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&template=bug-report.md).

- 5.2.4 Other issues

    - PD reports the `FATAL` error, and the log shows `range failed to find revision pair`. This issue has been fixed in v3.0.8 ([#2040](https://github.com/pingcap/pd/pull/2040)). For details, see [case-947](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case947.md) in Chinese.

    - For other situations, [report a bug](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&template=bug-report.md).

### 5.3 PD OOM

- 5.3.1 When the `/api/v1/regions` interface is used, too many Regions might cause PD OOM. This issue has been fixed in v3.0.8 ([#1986](https://github.com/pingcap/pd/pull/1986)).

- 5.3.2 PD OOM during the rolling upgrade. The size of gRPC messages is not limited, and the monitor shows that TCP InSegs is relatively large. This issue has been fixed in v3.0.6 ([#1952](https://github.com/pingcap/pd/pull/1952)). <!--For details, see [case-852](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case852.md).-->

### 5.4 Grafana display

- 5.4.1 The monitor in **Grafana** -> **PD** -> **cluster** -> **role** displays follower. The Grafana expression issue has been fixed in v3.0.8.

## 6. Ecosystem tools

### 6.1 TiDB Binlog

- 6.1.1 TiDB Binlog is a tool that collects changes from TiDB and provides backup and replication to downstream TiDB or MySQL platforms. For details, see [TiDB Binlog on GitHub](https://github.com/pingcap/tidb-binlog).

- 6.1.2 The `Update Time` in Pump/Drainer Status is updated normally, and no anomaly shows in the log, but no data is written to the downstream.

    - Binlog is not enabled in the TiDB configuration. Modify the `[binlog]` configuration in TiDB.

- 6.1.3 `sarama` in Drainer reports the `EOF` error.

    - The Kafka client version in Drainer is inconsistent with the version of Kafka. You need to modify the `[syncer.to] kafka-version` configuration.

- 6.1.4 Drainer fails to write to Kafka and panics, and Kafka reports the `Message was too large` error.

    - The binlog data is too large, so the single message written to Kafka is too large. You need to modify the following configuration of Kafka:

        ```conf
        message.max.bytes=1073741824
        replica.fetch.max.bytes=1073741824
        fetch.message.max.bytes=1073741824
        ```

        For details, see [case-789](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case789.md) in Chinese.

- 6.1.5 Inconsistent data in upstream and downstream

    - Some TiDB nodes do not enable binlog. For v3.0.6 or later versions, you can check the binlog status of all the nodes by accessing the <http://127.0.0.1:10080/info/all> interface. For versions earlier than v3.0.6, you can check the binlog status by viewing the configuration file.

    - Some TiDB nodes go into the `ignore binlog` status. For v3.0.6 or later versions, you can check the binlog status of all the nodes by accessing the <http://127.0.0.1:10080/info/all> interface. For versions earlier than v3.0.6, check the TiDB log to see whether it contains the `ignore binlog` keyword.

    - The value of the timestamp column is inconsistent in upstream and downstream.

        - This is caused by different time zones. You need to ensure that Drainer is in the same time zone as the upstream and downstream databases. Drainer obtains its time zone from `/etc/localtime` and does not support the `TZ` environment variable. See [case-826](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case826.md) in Chinese.

        - In TiDB, the default value of timestamp is `null`, but the same default value in MySQL 5.7 (not including MySQL 8) is the current time. Therefore, when the timestamp in upstream TiDB is `null` and the downstream is MySQL 5.7, the data in the timestamp column is inconsistent. You need to run `set @@global.explicit_defaults_for_timestamp=on;` in the upstream before enabling binlog.

    - For other situations, [report a bug](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&template=bug-report.md).

- 6.1.6 Slow replication

    - The downstream is TiDB/MySQL, and the upstream performs frequent DDL operations. See [case-1023](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1023.md) in Chinese.

    - The downstream is TiDB/MySQL, and the table to be replicated has no primary key and no unique index, which causes reduced performance in binlog. It is recommended to add the primary key or unique index.

    - If the downstream outputs to files, check whether the output disk or network disk is slow.

    - For other situations, [report a bug](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&template=bug-report.md).

- 6.1.7 Pump cannot write binlog and reports the `no space left on device` error.

    - The local disk space is insufficient for Pump to write binlog data normally. You need to clean up the disk space and then restart Pump.

- 6.1.8 Pump reports the `fail to notify all living drainer` error when it is started.

    - Cause: When Pump is started, it notifies all Drainer nodes that are in the `online` state. If it fails to notify Drainer, this error log is printed.

    - Solution: Use the binlogctl tool to check whether each Drainer node is normal or not. This is to ensure that all Drainer nodes in the `online` state are working normally. If the state of a Drainer node is not consistent with its actual working status, use the binlogctl tool to change its state and then restart Pump. See the case [fail-to-notify-all-living-drainer](/tidb-binlog/handle-tidb-binlog-errors.md#fail-to-notify-all-living-drainer-is-returned-when-pump-is-started).

- 6.1.9 Drainer reports the `gen update sqls failed: table xxx: row data is corruption []` error.

    - Trigger: The upstream performs DML operations on this table while performing `DROP COLUMN` DDL. This issue has been fixed in v3.0.6. See [case-820](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case820.md) in Chinese.

- 6.1.10 Drainer replication is hung. The process remains active but the checkpoint is not updated.

    - This issues has been fixed in v3.0.4. See [case-741](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case741.md) in Chinese.

- 6.1.11 Any component panics.

    - [Report a bug](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&template=bug-report.md).

### 6.2 Data Migration

- 6.2.1 TiDB Data Migration (DM) is a migration tool that supports data migration from MySQL/MariaDB into TiDB. For details, see [DM on GitHub](https://github.com/pingcap/dm/).

- 6.2.2 `Access denied for user 'root'@'172.31.43.27' (using password: YES)` shows when you run `query status` or check the log.

    - The database related passwords in all the DM configuration files should be encrypted by `dmctl`. If a database password is empty, it is unnecessary to encrypt the password. Cleartext passwords can be used since v1.0.6.
    - During DM operation, the user of the upstream and downstream databases must have the corresponding read and write privileges. Data Migration also [prechecks the corresponding privileges](/dm/dm-precheck.md) automatically while starting the data replication task.
    - To deploy different versions of DM-worker/DM-master/dmctl in a DM cluster, see the [case study on AskTUG](https://asktug.com/t/dm1-0-0-ga-access-denied-for-user/1049/5) in Chinese.

- 6.2.3 A replication task is interrupted with the `driver: bad connection` error returned.

    - The `driver: bad connection` error indicates that an anomaly has occurred in the connection between DM and the downstream TiDB database (such as network failure and TiDB restart), and that the data of the current request has not yet been sent to TiDB.

        - For versions earlier than DM 1.0.0 GA, stop the task by running `stop-task` and then restart the task by running `start-task`.
        - For DM 1.0.0 GA or later versions, an automatic retry mechanism for this type of error is added. See [#265](https://github.com/pingcap/dm/pull/265).

- 6.2.4 A replication task is interrupted with the `invalid connection` error.

    - The `invalid connection` error indicates that an anomaly has occurred in the connection between DM and the downstream TiDB database (such as network failure, TiDB restart, and TiKV busy), and that a part of the data for the current request has been sent to TiDB. Because DM has the feature of concurrently replicating data to the downstream in replication tasks, several errors might occur when a task is interrupted. You can check these errors by running `query-status` or `query-error`.

        - If only the `invalid connection` error occurs during the incremental replication process, DM retries the task automatically.
        - If DM does not retry or fails to retry automatically because of version problems (automatic retry is introduced in v1.0.0-rc.1), use `stop-task` to stop the task and then use `start-task` to restart the task.

- 6.2.5 The relay unit reports the error `event from * in * diff from passed-in event *`, or a replication task is interrupted with an error that fails to get or parse binlog, such as `get binlog error ERROR 1236 (HY000) and binlog checksum mismatch, data may be corrupted returned`

    - During the process that DM pulls relay log or the incremental replication, this two errors might occur if the size of the upstream binlog file exceeds 4 GB.

    - Cause: When writing relay logs, DM needs to perform event verification based on binlog positions and the binlog file size, and store the replicated binlog positions as checkpoints. However, the official MySQL uses uint32 to store binlog positions, which means the binlog position for a binlog file over 4 GB overflows, and then the errors above occur.

    - Solution:

        - For relay processing units, [manually recover replication](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned).
        - For binlog replication processing units, [manually recover replication](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned).

- 6.2.6 The DM replication is interrupted, and the log returns `ERROR 1236 (HY000) The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.`

    - Check whether the master binlog is purged.
    - Check the position information recorded in `relay.meta`.

        - `relay.meta` has recorded the empty GTID information. DM-worker saves the GTID information in memory to `relay.meta` when it exits or in every 30s. When DM-worker does not obtain the upstream GTID information, it saves the empty GTID information to `relay.meta`. See [case-772](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case772.md) in Chinese.

        - The binlog event recorded in `relay.meta` triggers the incomplete recover process and records the wrong GTID information. This issue is fixed in v1.0.2, and might occur in earlier versions. <!--See [case-764](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case764.md).-->

- 6.2.7 The DM replication process returns an error `Error 1366: incorrect utf8 value eda0bdedb29d(\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd)`.

    - This value cannot be successfully written into MySQL 8.0 or TiDB, but can be written into MySQL 5.7. You can skip the data format check by enabling the `tidb_skip_utf8_check` parameter.

### 6.3 TiDB Lightning

- 6.3.1 TiDB Lightning is a tool for fast full import of large amounts of data into a TiDB cluster. See [TiDB Lightning on GitHub](https://github.com/pingcap/tidb/tree/master/br/pkg/lightning).

- 6.3.2 Import speed is too slow.

    - `region-concurrency` is set too high, which causes thread contention and reduces performance. Three ways to troubleshoot:

        - The setting can be found from the start of the log by searching `region-concurrency`.
        - If TiDB Lightning shares a server with other services (for example, Importer), you must manually set `region-concurrency` to 75% of the total number of CPU cores on that server.
        - If there is a quota on CPU (for example, limited by Kubernetes settings), TiDB Lightning might not be able to read this out. In this case, `region-concurrency` must also be manually reduced.

    - Every additional index introduces a new KV pair for each row. If there are N indices, the actual size to be imported would be approximately (N+1) times the size of the [Mydumper](https://docs.pingcap.com/tidb/v4.0/mydumper-overview) output. If the indices are negligible, you may first remove them from the schema, and add them back via `CREATE INDEX` after the import is complete.
    - The version of TiDB Lightning is old. Try the latest version, which might improve the import speed.

- 6.3.3 `checksum failed: checksum mismatched remote vs local`.

    - Cause 1: The table might already have data. These old data can affect the final checksum.

    - Cause 2: If the checksum of the target database is 0, which means nothing is imported, it is possible that the cluster is too hot and fails to take in any data.

    - Cause 3: If the data source is generated by the machine and not backed up by [Mydumper](https://docs.pingcap.com/tidb/v4.0/mydumper-overview), ensure it respects the constrains of the table. For example:

        - `AUTO_INCREMENT` columns need to be positive, and do not contain the value "0".
        - UNIQUE and PRIMARY KEYs must not have duplicate entries.

    - Solution: See [Troubleshooting Solution](/tidb-lightning/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local).

- 6.3.4 `Checkpoint for … has invalid status:(error code)`

    - Cause: Checkpoint is enabled, and Lightning/Importer has previously abnormally exited. To prevent accidental data corruption, TiDB Lightning will not start until the error is addressed. The error code is an integer less than 25, with possible values as `0, 3, 6, 9, 12, 14, 15, 17, 18, 20 and 21`. The integer indicates the step where the unexpected exit occurs in the import process. The larger the integer is, the later the exit occurs.

    - Solution: See [Troubleshooting Solution](/tidb-lightning/troubleshoot-tidb-lightning.md#checkpoint-for--has-invalid-status-error-code).

- 6.3.5 `ResourceTemporarilyUnavailable("Too many open engines …: 8")`

    - Cause: The number of concurrent engine files exceeds the limit specified by tikv-importer. This could be caused by misconfiguration. In addition, even when the configuration is correct, if tidb-lightning has exited abnormally before, an engine file might be left at a dangling open state, which could cause this error as well.
    - Solution: See [Troubleshooting Solution](/tidb-lightning/troubleshoot-tidb-lightning.md#resourcetemporarilyunavailabletoo-many-open-engines--).

- 6.3.6 `cannot guess encoding for input file, please convert to UTF-8 manually`

    - Cause: TiDB Lightning only supports the UTF-8 and GB-18030 encodings. This error means the file is not in any of these encodings. It is also possible that the file has mixed encoding, such as containing a string in UTF-8 and another string in GB-18030, due to historical ALTER TABLE executions.

    - Solution: See [Troubleshooting Solution](/tidb-lightning/troubleshoot-tidb-lightning.md#cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually).

- 6.3.7 `[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 0 45 0 0}'`

    - Cause: A timestamp type entry has a time value that does not exist. This is either because of DST changes or because the time value has exceeded the supported range (from Jan 1, 1970 to Jan 19, 2038).

    - Solution: See [Troubleshooting Solution](/tidb-lightning/troubleshoot-tidb-lightning.md#sql2kv-sql-encode-error--types1292invalid-time-format-1970-1-1-).

## 7. Common log analysis

### 7.1 TiDB

- 7.1.1 `GC life time is shorter than transaction duration`.

    The transaction duration exceeds the GC lifetime (10 minutes by default).

    You can increase the GC lifetime by modifying the [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) system variable. Generally, it is not recommended to modify this parameter, because changing it might cause many old versions to pile up if this transaction has a large number of `UPDATE` and `DELETE` statements.

- 7.1.2 `txn takes too much time`.

    This error is returned when you commit a transaction that has not been committed for a long time (over 590 seconds).

    If your application needs to execute a transaction of such a long time, you can increase the `[tikv-client] max-txn-time-use = 590` parameter and the GC lifetime to avoid this issue. It is recommended to check whether your application needs such a long transaction time.

- 7.1.3 `coprocessor.go` reports `request outdated`.

    This error is returned when the coprocessor request sent to TiKV waits in a queue at TiKV for over 60 seconds.

    You need to investigate why the TiKV coprocessor is in a long queue.

- 7.1.4 `region_cache.go` reports a large number of `switch region peer to next due to send request fail`, and the error message is `context deadline exceeded`.

    The request for TiKV timed out and triggers the region cache to switch the request to other nodes. You can continue to run the `grep "<addr> cancelled` command on the `addr` field in the log and take the following steps according to the `grep` results:

    - `send request is cancelled`: The request timed out during the sending phase. You can investigate the monitoring **Grafana** -> **TiDB** -> **Batch Client**/`Pending Request Count by TiKV` and see whether the Pending Request Count is greater than 128:

        - If the value is greater than 128, the sending goes beyond the processing capacity of KV, so the sending piles up.
        - If the value is not greater than 128, check the log to see if the report is caused by the operation and maintenance changes of the corresponding KV; otherwise, this error is unexpected, and you need to [report a bug](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&template=bug-report.md).

    - `wait response is cancelled`: The request timed out after it is sent to TiKV. You need to check the response time of the corresponding TiKV address and the Region logs in PD and KV at that time.

- 7.1.5 `distsql.go` reports `inconsistent index`.

    The data index seems to be inconsistent. Run the `admin check table <TableName>` command on the table where the reported index is. If the check fails, disable garbage collection by running the following command, and [report a bug](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&template=bug-report.md):

    ```sql
    SET GLOBAL tidb_gc_enable = 0;
    ```

### 7.2 TiKV

- 7.2.1 `key is locked`.

    The read and write have conflict. The read request encounters data that has not been committed and needs to wait until the data is committed.

    A small number of this error has no impact on the business, but a large number of this error indicates that the read-write conflict is severe in your business.

- 7.2.2 `write conflict`.

    This is the write-write conflict in optimistic transactions. If multiple transactions modify the same key, only one transaction succeed and other transactions automatically obtain the timestamp again and retry the operation, with no impact on the business.

    If the conflict is severe, it might cause transaction failure after multiple retries. In this case, it is recommended to use the pessimistic lock. For more details about the error and the solution, see [Troubleshoot Write Conflicts in Optimistic Transactions](/troubleshoot-write-conflicts.md).

- 7.2.3 `TxnLockNotFound`.

    This transaction commit is too slow, causing it to be rolled back by other transactions after Time To Live (TTL). This transaction will automatically retry, so the business is usually not affected. For a transaction with a size of 0.25 MB or smaller, the default TTL is 3 seconds. For more details, see the [`LockNotFound` error](/troubleshoot-lock-conflicts.md#locknotfound-error).

- 7.2.4 `PessimisticLockNotFound`.

    Similar to `TxnLockNotFound`. The pessimistic transaction commit is too slow and thus rolled back by other transactions.

- 7.2.5 `stale_epoch`.

    The request epoch is outdated, so TiDB re-sends the request after updating the routing. The business is not affected. Epoch changes when Region has a split/merge operation or a replica is migrated.

- 7.2.6 `peer is not leader`.

    The request is sent to a replica that is not Leader. If the error response indicates which replica is the latest Leader, TiDB updates the local routing according the error and sends a new request to the latest Leader. Usually, the business is not affected.

    In v3.0 and later versions, TiDB tries other peers if the request to the previous Leader fails, which might lead to frequent `peer is not leader` in TiKV log. You can check the `switch region peer to next due to send request fail` log of the corresponding Region in TiDB to determine the root cause of the sending failure. For details, refer to [7.1.4](#71-tidb).

    This error might also be returned if a Region has no Leader due to other reasons. For details, see [4.4](#44-some-tikv-nodes-drop-leader-frequently).

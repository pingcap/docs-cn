---
title: TiDB 5.3.2 Release Notes
---

# TiDB 5.3.2 Release Notes

Release Date: June 29, 2022

TiDB version: 5.3.2

> **Warning:**
>
> It is not recommended to use v5.3.2, because this version has a known bug. For details, see [#12934](https://github.com/tikv/tikv/issues/12934). This bug has been fixed in v5.3.3. It is recommended to use [v5.3.3](/releases/release-5.3.3.md).

## Compatibility Changes

+ TiDB

    - Fix the issue that the `REPLACE` statement incorrectly changes other rows when the auto ID is out of range [#29483](https://github.com/pingcap/tidb/issues/29483)

+ PD

    - Disable compiling swagger server by default [#4932](https://github.com/tikv/pd/issues/4932)

## Improvements

+ TiKV

    - Reduce the system call by the Raft client and increase CPU efficiency [#11309](https://github.com/tikv/tikv/issues/11309)
    - Improve the health check to detect unavailable Raftstore, so that the TiKV client can update Region Cache in time [#12398](https://github.com/tikv/tikv/issues/12398)
    - Transfer the leadership to CDC observer to reduce latency jitter [#12111](https://github.com/tikv/tikv/issues/12111)
    - Add more metrics for the garbage collection module of Raft logs to locate performance problems in the module [#11374](https://github.com/tikv/tikv/issues/11374)

+ Tools

    + TiDB Data Migration (DM)

        - Support Syncer using the working directory of the DM-worker rather than `/tmp` to write internal files, and cleaning the directory after the task is stopped [#4107](https://github.com/pingcap/tiflow/issues/4107)

    + TiDB Lightning

        - Optimize Scatter Region to batch mode to improve the stability of the Scatter Region process [#33618](https://github.com/pingcap/tidb/issues/33618)

## Bug Fixes

+ TiDB

    - Fix the issue that Amazon S3 cannot correctly calculate the size of compressed data [#30534](https://github.com/pingcap/tidb/issues/30534)
    - Fix the issue of potential data index inconsistency in optimistic transaction mode [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the issue that a SQL operation is canceled when its JSON type column joins its `CHAR` type column [#29401](https://github.com/pingcap/tidb/issues/29401)
    - Previously, when a network connectivity issue occurred, TiDB did not always correctly free the resources held by the disconnected session. This issue has been fixed so that open transactions can be rolled back and other associated resources can be released. [#34722](https://github.com/pingcap/tidb/issues/34722)
    - Fix the issue of the `data and columnID count not match` error that occurs when inserting duplicated values with TiDB Binlog enabled [#33608](https://github.com/pingcap/tidb/issues/33608)
    - Fix the issue that query result might be wrong when Plan Cache is started in the RC isolation level [#34447](https://github.com/pingcap/tidb/issues/34447)
    - Fix the session panic that occurs when executing the prepared statement after table schema change with the MySQL binary protocol [#33509](https://github.com/pingcap/tidb/issues/33509)
    - Fix the issue that the table attributes are not indexed when a new partition is added and the issue that the table range information is not updated when the partition changes [#33929](https://github.com/pingcap/tidb/issues/33929)
    - Fix the issue that the TiDB server might run out of memory when the `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` table is queried. This issue can be triggered when you check slow queries on the Grafana dashboard [#33893](https://github.com/pingcap/tidb/issues/33893)
    - Fix the issue that some DDL statements might be stuck for a period after the PD node of a cluster is replaced [#33908](https://github.com/pingcap/tidb/issues/33908)
    - Fix the issue that granting the `all` privilege might fail in clusters that are upgraded from v4.0 [#33588](https://github.com/pingcap/tidb/issues/33588)
    - Fix wrong results of deleting data of multiple tables using `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)
    - Fix a bug that TiDB may dispatch duplicate tasks to TiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)
    - Fix the issue that the background HTTP service of TiDB might not exit successfully and makes the cluster in an abnormal state [#30571](https://github.com/pingcap/tidb/issues/30571)
    - Fix the panic issue caused by the `fatal error: concurrent map read and map write` error [#35340](https://github.com/pingcap/tidb/issues/35340)

+ TiKV

    - Fix the issue of frequent PD client reconnection that occurs when the PD client meets an error [#12345](https://github.com/tikv/tikv/issues/12345)
    - Fix the issue of time parsing error that occurs when the `DATETIME` values contain a fraction and `Z` [#12739](https://github.com/tikv/tikv/issues/12739)
    - Fix the issue that TiKV panics when performing type conversion for an empty string [#12673](https://github.com/tikv/tikv/issues/12673)
    - Fix the possible duplicate commit records in pessimistic transactions when async commit is enabled [#12615](https://github.com/tikv/tikv/issues/12615)
    - Fix the bug that TiKV reports the `invalid store ID 0` error when using Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)
    - Fix the issue of TiKV panic caused by the race between destroying peers and batch splitting Regions [#12368](https://github.com/tikv/tikv/issues/12368)
    - Fix the issue that successfully committed optimistic transactions may report the `Write Conflict` error when the network is poor [#34066](https://github.com/pingcap/tidb/issues/34066)
    - Fix the issue that TiKV panics and destroys peers unexpectedly when the target Region to be merged is invalid [#12232](https://github.com/tikv/tikv/issues/12232)
    - Fix a bug that stale messages cause TiKV to panic [#12023](https://github.com/tikv/tikv/issues/12023)
    - Fix the issue of intermittent packet loss and out of memory (OOM) caused by the overflow of memory metrics [#12160](https://github.com/tikv/tikv/issues/12160)
    - Fix the potential panic issue that occurs when TiKV performs profiling on Ubuntu 18.04 [#9765](https://github.com/tikv/tikv/issues/9765)
    - Fix the issue that tikv-ctl returns an incorrect result due to its wrong string match [#12329](https://github.com/tikv/tikv/issues/12329)
    - Fix a bug that replica reads might violate the linearizability [#12109](https://github.com/tikv/tikv/issues/12109)
    - Fix the TiKV panic issue that occurs when the target peer is replaced with the peer that is destroyed without being initialized when merging a Region [#12048](https://github.com/tikv/tikv/issues/12048)
    - Fix a bug that TiKV might panic if it has been running for 2 years or more [#11940](https://github.com/tikv/tikv/issues/11940)

+ PD

    - Fix the PD panic that occurs when a hot region has no leader [#5005](https://github.com/tikv/pd/issues/5005)
    - Fix the issue that scheduling cannot start immediately after the PD leader transfer [#4769](https://github.com/tikv/pd/issues/4769)
    - Fix the issue that a removed tombstone store appears again after the PD leader transfer ​​[#4941](https://github.com/tikv/pd/issues/4941)
    - Fix a bug of TSO fallback in some corner cases [#4884](https://github.com/tikv/pd/issues/4884)
    - Fix the issue that when there exists a Store with large capacity (2T for example), fully allocated small Stores cannot be detected, which results in no balance operator being generated [#4805](https://github.com/tikv/pd/issues/4805)
    - Fix the issue that schedulers do not work when `SchedulerMaxWaitingOperator` is set to `1` [#4946](https://github.com/tikv/pd/issues/4946)
    - Fix the issue that the label distribution has residual labels in the metrics [#4825](https://github.com/tikv/pd/issues/4825)

+ TiFlash

    - Fix the bug that invalid storage directory configurations lead to unexpected behaviors [#4093](https://github.com/pingcap/tiflash/issues/4093)
    - Fix `TiFlash_schema_error` reported when `NOT NULL` columns are added [#4596](https://github.com/pingcap/tiflash/issues/4596)
    - Fix repeated crashes caused by the `commit state jump backward` errors [#2576](https://github.com/pingcap/tiflash/issues/2576)
    - Fix potential data inconsistency after a lot of INSERT and DELETE operations [#4956](https://github.com/pingcap/tiflash/issues/4956)
    - Fix a bug that canceled MPP queries might cause tasks to hang forever when the local tunnel is enabled [#4229](https://github.com/pingcap/tiflash/issues/4229)
    - Fix false reports of inconsistent TiFlash versions when TiFlash uses remote read [#3713](https://github.com/pingcap/tiflash/issues/3713)
    - Fix a bug that an MPP query might fail due to random gRPC keepalive timeout [#4662](https://github.com/pingcap/tiflash/issues/4662)
    - Fix a bug that an MPP query might hang forever if there are retries in the exchange receiver [#3444](https://github.com/pingcap/tiflash/issues/3444)
    - Fix the wrong result that occurs when casting `DATETIME` to `DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - Fix the overflow that occurs when casting `FLOAT` to `DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - Fix the potential `index out of bounds` error if calling `json_length` with empty string [#2705](https://github.com/pingcap/tiflash/issues/2705)
    - Fix wrong decimal comparison results in corner cases [#4512](https://github.com/pingcap/tiflash/issues/4512)
    - Fix bug that MPP query may hang forever if query failed in join build stage [#4195](https://github.com/pingcap/tiflash/issues/4195)
    - Fix possible wrong results when a query contains the `where <string>` clause [#3447](https://github.com/pingcap/tiflash/issues/3447)
    - Fix the issue that the `CastStringAsReal` behavior is inconsistent in TiFlash and in TiDB or TiKV [#3475](https://github.com/pingcap/tiflash/issues/3475)
    - Fix incorrect `microsecond` when casting string to datetime [#3556](https://github.com/pingcap/tiflash/issues/3556)
    - Fix potential errors when querying on a table with many delete operations [#4747](https://github.com/pingcap/tiflash/issues/4747)
    - Fix a bug that TiFlash reports many "Keepalive watchdog fired" errors randomly [#4192](https://github.com/pingcap/tiflash/issues/4192)
    - Fix a bug that data not matching any region range remains on a TiFlash node [#4414](https://github.com/pingcap/tiflash/issues/4414)
    - Fix a bug that MPP tasks might leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238)
    - Fix a bug that empty segments cannot be merged after GC [#4511](https://github.com/pingcap/tiflash/issues/4511)
    - Fix the panic issue that occurs when TLS is enabled [#4196](https://github.com/pingcap/tiflash/issues/4196)
    - Fix the issue that expired data is recycled slowly [#4146](https://github.com/pingcap/tiflash/issues/4146)
    - Fix the bug that invalid storage directory configurations lead to unexpected behaviors [#4093](https://github.com/pingcap/tiflash/issues/4093)
    - Fix the bug that some exceptions are not handled properly [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - Fix the potential query error after adding columns under heavy read workload [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - Fix the bug that the `STR_TO_DATE()` function incorrectly handles leading zeros when parsing microseconds [#3557](https://github.com/pingcap/tiflash/issues/3557)
    - Fix the issue that TiFlash might return the `EstablishMPPConnection` error after it is restarted [#3615](https://github.com/pingcap/tiflash/issues/3615)

+ Tools

    + Backup & Restore (BR)

        - Fix duplicate primary keys when inserting a record into a table after incremental restoration [#33596](https://github.com/pingcap/tidb/issues/33596)
        - Fix the issue that schedulers do not resume after BR or TiDB Lightning exits abnormally [#33546](https://github.com/pingcap/tidb/issues/33546)
        - Fix a bug that BR incremental restore returns errors mistakenly due to DDL jobs with empty query [#33322](https://github.com/pingcap/tidb/issues/33322)
        - Fix the issue that BR does not retry enough times when Regions are not consistent during restoration [#33419](https://github.com/pingcap/tidb/issues/33419)
        - Fix a bug that BR gets stuck when the restore operation meets some unrecoverable errors [#33200](https://github.com/pingcap/tidb/issues/33200)
        - Fix the issue that BR fails to back up RawKV [#32607](https://github.com/pingcap/tidb/issues/32607)
        - Fix the issue that BR cannot handle S3 internal errors [#34350](https://github.com/pingcap/tidb/issues/34350)

    + TiCDC

        - Fix incorrect metrics caused by owner changes [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - Fix the bug that the redo log manager flushes logs before writing logs [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Fix the bug that the resolved ts moves too fast when some tables are not maintained by the redo writer [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Add the UUID suffix to the redo log file name to fix the issue that file name conflicts may cause data loss [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Fix the bug that MySQL Sink may save a wrong checkpointTs [#5107](https://github.com/pingcap/tiflow/issues/5107)
        - Fix the issue that TiCDC clusters may panic after upgrade [#5266](https://github.com/pingcap/tiflow/issues/5266)
        - Fix the issue that changefeed gets stuck when tables are repeatedly scheduled in the same node [#4464](https://github.com/pingcap/tiflow/issues/4464)
        - Fix the issue that TiCDC fails to start when the first PD set in `--pd` is not available after TLS is enabled [#4777](https://github.com/pingcap/tiflow/issues/4777)
        - Fix a bug that querying status through open API may be blocked when the PD node is abnormal [#4778](https://github.com/pingcap/tiflow/issues/4778)
        - Fix a stability problem in workerpool used by Unified Sorter [#4447](https://github.com/pingcap/tiflow/issues/4447)
        - Fix a bug that sequence is incorrectly replicated in some cases [#4563](https://github.com/pingcap/tiflow/issues/4552)

    + TiDB Data Migration (DM)

        - Fix the issue that DM occupies more disk space after the task automatically resumes [#3734](https://github.com/pingcap/tiflow/issues/3734) [#5344](https://github.com/pingcap/tiflow/issues/5344)
        - Fix an issue that the uppercase table cannot be replicated when `case-sensitive: true` is not set [#5255](https://github.com/pingcap/tiflow/issues/5255)
        - Fix the issue that in some cases manually executing the filtered DDL in the downstream might cause task resumption failure [#5272](https://github.com/pingcap/tiflow/issues/5272)
        - Fix the DM worker panic issue that occurs when the primary key is not first in the index returned by the `SHOW CREATE TABLE` statement [#5159](https://github.com/pingcap/tiflow/issues/5159)
        - Fix the issue that CPU usage may increase and a large amount of log is printed when GTID is enabled or when the task is automatically resumed [#5063](https://github.com/pingcap/tiflow/issues/5063)
        - Fix the issue that the relay log may be disabled after the DM-master reboots [#4803](https://github.com/pingcap/tiflow/issues/4803)

    + TiDB Lightning

        - Fix the issue of Local-backend import failure caused by out-of-bounds data in the `auto_increment` column [#27937](https://github.com/pingcap/tidb/issues/27937)
        - Fix the issue that the precheck does not check local disk resources and cluster availability [#34213](https://github.com/pingcap/tidb/issues/34213)
        - Fix the checksum error "GC life time is shorter than transaction duration" [#32733](https://github.com/pingcap/tidb/issues/32733)

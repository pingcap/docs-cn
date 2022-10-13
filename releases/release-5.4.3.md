---
title: TiDB 5.4.3 Release Notes
---

# TiDB 5.4.3 Release Notes

Release date: October 13, 2022

TiDB version: 5.4.3

## Improvements

+ TiKV

    - Support configuring the RocksDB write stall settings to a value smaller than the flow control threshold [#13467](https://github.com/tikv/tikv/issues/13467)
    - Support configuring the `unreachable_backoff` item to avoid Raftstore broadcasting too many messages after one peer becomes unreachable [#13054](https://github.com/tikv/tikv/issues/13054)

+ Tools

    + TiDB Lightning

        - Optimize Scatter Region to batch mode to improve the stability of the Scatter Region process [#33618](https://github.com/pingcap/tidb/issues/33618)

    + TiCDC

        - Reduce performance overhead caused by runtime context switching in multi-Region scenarios [#5610](https://github.com/pingcap/tiflow/issues/5610)

## Bug fixes

+ TiDB

    - Fix the incorrect output of `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526)
    - Fix the issue that some DDL statements might be stuck for a period after the PD node of a cluster is replaced [#33908](https://github.com/pingcap/tidb/issues/33908)
    - Fix the issue that `KILL TIDB` cannot take effect immediately on idle connections [#24031](https://github.com/pingcap/tidb/issues/24031)
    - Fix the issue that incorrect results are returned in the `DATA_TYPE` and `COLUMN_TYPE` columns when querying the `INFORMSTION_SCHEMA.COLUMNS` system table [#36496](https://github.com/pingcap/tidb/issues/36496)
    - Fix the issue that when TiDB Binlog is enabled, executing the `ALTER SEQUENCE` statement might cause a wrong metadata version and cause Drainer to exit [#36276](https://github.com/pingcap/tidb/issues/36276)
    - Fix the issue that the `UNION` operator might return unexpected empty result [#36903](https://github.com/pingcap/tidb/issues/36903)
    - Fix the wrong result that occurs when enabling dynamic mode in partitioned tables for TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254)
    - Fix the issue that `INL_HASH_JOIN` might hang when used with `LIMIT` [#35638](https://github.com/pingcap/tidb/issues/35638)
    - Fix the issue that TiDB might return the `invalid memory address or nil pointer dereference` error when executing the `SHOW WARNINGS` statement [#31569](https://github.com/pingcap/tidb/issues/31569)
    - Fix the `invalid transaction` error that occurs when performing Stale Read in the RC isolation level [#30872](https://github.com/pingcap/tidb/issues/30872)
    - Fix the issue that the `EXPLAIN ANALYZE` statement with DML executors might return result before the transaction commit finishes [#37373](https://github.com/pingcap/tidb/issues/37373)
    - Fix the issue of the `data and columnID count not match` error that occurs when inserting duplicated values with TiDB Binlog enabled [#33608](https://github.com/pingcap/tidb/issues/33608)
    - Fix the issue that in the static partition prune mode, SQL statements with an aggregate condition might return wrong result when the table is empty [#35295](https://github.com/pingcap/tidb/issues/35295)
    - Fix the issue that TiDB might panic when executing the `UPDATE` statement [#32311](https://github.com/pingcap/tidb/issues/32311)
    - Fix the issue of wrong query result because the `UnionScan` operator cannot maintain the order [#33175](https://github.com/pingcap/tidb/issues/33175)
    - Fix the issue that the UPDATE statements incorrectly eliminate the projection in some cases, which causes the `Can't find column` error [#37568](https://github.com/pingcap/tidb/issues/37568)
    - Fix the issue that partitioned tables cannot fully use indexes to scan data in some cases [#33966](https://github.com/pingcap/tidb/issues/33966)
    - Fix the issue that the `EXECUTE` might throw an unexpected error in specific scenarios [#37187](https://github.com/pingcap/tidb/issues/37187)
    - Fix the issue that TiDB might return wrong results when using a `BIT` type index with prepared plan cache enabled [#33067](https://github.com/pingcap/tidb/issues/33067)

+ TiKV

    - Fix the issue of continuous SQL execution errors in the cluster after the PD leader is switched or PD is restarted [#12934](https://github.com/tikv/tikv/issues/12934)
        - Cause: This issue is caused by a TiKV bug that TiKV does not retry sending heartbeat information to PD client after heartbeat requests fail, until TiKV reconnects to PD client. As a result, the Region information on the failed TiKV node becomes outdated, and TiDB cannot get the latest Region information, which causes SQL execution errors.
        - Affected versions: v5.3.2 and v5.4.2. This issue has been fixed in v5.3.3 and v5.4.3. If you are using v5.4.2, you can upgrade your cluster to v5.4.3.
        - Workaround: In addition to upgrade, you can also restart the TiKV nodes that cannot send Region heartbeat to PD, until there is no Region heartbeat to send.
    - Fix the issue that causes permission denied error when TiKV gets an error from the web identity provider and fails back to the default provider [#13122](https://github.com/tikv/tikv/issues/13122)
    - Fix the issue that the PD client might cause deadlocks [#13191](https://github.com/tikv/tikv/issues/13191)
    - Fix the issue that Regions might be overlapped if Raftstore is busy [#13160](https://github.com/tikv/tikv/issues/13160)

+ PD

    - Fix the issue that PD cannot correctly handle dashboard proxy requests [#5321](https://github.com/tikv/pd/issues/5321)
    - Fix the issue that a removed tombstone store appears again after the PD leader transfer ​​[#4941](https://github.com/tikv/pd/issues/4941)
    - Fix the issue that the TiFlash learner replica might not be created [#5401](https://github.com/tikv/pd/issues/5401)

+ TiFlash

    - Fix the issue that the `format` function might return a `Data truncated` error [#4891](https://github.com/pingcap/tiflash/issues/4891)
    - Fix the issue that TiFlash might crash due to an error in parallel aggregation [#5356](https://github.com/pingcap/tiflash/issues/5356)
    - Fix the panic that occurs after creating the primary index with a column containing the `NULL` value [#5859](https://github.com/pingcap/tiflash/issues/5859)

+ Tools

    + TiDB Lightning

        - Fix the issue that an auto-increment column of the `BIGINT` type might be out of range [#27397](https://github.com/pingcap/tidb/issues/27937)
        - Fix the issue that de-duplication might cause TiDB Lightning to panic in extreme cases [#34163](https://github.com/pingcap/tidb/issues/34163)
        - Fix the issue that TiDB Lightning does not support columns starting with slash, number, or non-ascii characters in Parquet files [#36980](https://github.com/pingcap/tidb/issues/36980)
        - Fix the issue that TiDB Lightning fails to connect to TiDB when TiDB uses an IPv6 host [#35880](https://github.com/pingcap/tidb/issues/35880)

    + TiDB Data Migration (DM)

        - Fix the issue that DM Worker might get stuck when getting DB Conn [#3733](https://github.com/pingcap/tiflow/issues/3733)
        - Fix the issue that DM reports the `Specified key was too long` error [#5315](https://github.com/pingcap/tiflow/issues/5315)
        - Fix the issue that latin1 data might be corrupted during replication [#7028](https://github.com/pingcap/tiflow/issues/7028)
        - Fix the issue that DM fails to start when TiDB uses an IPv6 host [#6249](https://github.com/pingcap/tiflow/issues/6249)
        - Fix the issue of possible data race in `query-status` [#4811](https://github.com/pingcap/tiflow/issues/4811)
        - Fix goroutine leak when relay meets an error [#6193](https://github.com/pingcap/tiflow/issues/6193)

    + TiCDC

        - Fix the TiCDC panic issue when you set `enable-old-value = false` [#6198](https://github.com/pingcap/tiflow/issues/6198)

    + Backup & Restore (BR)

        - Fix the issue that might lead to backup and restoration failure if special characters exist in the authorization key of external storage [#37469](https://github.com/pingcap/tidb/issues/37469)
        - Fix the issue that the regions are not balanced because the concurrency is set too large during the restoration [#37549](https://github.com/pingcap/tidb/issues/37549)

    + Dumpling

        - Fix the issue that GetDSN does not support IPv6 [#36112](https://github.com/pingcap/tidb/issues/36112)

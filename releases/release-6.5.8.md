---
title: TiDB 6.5.8 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.8.
---

# TiDB 6.5.8 Release Notes

Release date: February 2, 2024

TiDB version: 6.5.8

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.8#version-list)

## Compatibility changes

- Introduce the TiKV configuration item [`gc.num-threads`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#num-threads-new-in-v658) to set the number of GC threads when `enable-compaction-filter` is `false`  [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)

## Improvements

+ TiFlash

    - Reduce the impact of background GC tasks on read and write task latency [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiCDC

        - Support [querying the downstream synchronization status of a changefeed](https://docs.pingcap.com/tidb/v6.5/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed), which helps you determine whether the upstream data changes received by TiCDC have been synchronized to the downstream system completely [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)

    + TiDB Lightning

        - Improve the performance of `ALTER TABLE` when importing a large number of small tables [#50105](https://github.com/pingcap/tidb/issues/50105) @[D3Hunter](https://github.com/D3Hunter)

## Bug fixes

+ TiDB

    - Fix the issue that enforced sorting might become ineffective when a query uses optimizer hints (such as `STREAM_AGG()`) that enforce sorting and its execution plan contains `IndexMerge` [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that histogram statistics might not be parsed into readable strings when the histogram boundary contains `NULL` [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that hints cannot be used in `REPLACE INTO` statements [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that query results are incorrect due to `STREAM_AGG()` incorrectly handling CI [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the query result of a range partitioned table is incorrect in some cases due to wrong partition pruning [#50082](https://github.com/pingcap/tidb/issues/49823) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the auto-increment ID allocation reports an error due to concurrent conflicts when using an auto-increment column with `AUTO_ID_CACHE=1` [#50519](https://github.com/pingcap/tidb/issues/50519) @[tiancaiamao](https://github.com/tiancaiamao)
    - Mitigate the issue that TiDB nodes might encounter OOM errors when dealing with a large number of tables or partitions [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - Fix the issue that data is inconsistent under the TiDB Distributed eXecution Framework (DXF) when executing `ADD INDEX` after the DDL Owner is network isolated [#49773](https://github.com/pingcap/tidb/issues/49773) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiDB might panic when a query contains the Apply operator and the `fatal error: concurrent map writes` error occurs [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that the `COMMIT` or `ROLLBACK` operation executed through `COM_STMT_EXECUTE` fails to terminate transactions that have timed out [#49151](https://github.com/pingcap/tidb/issues/49151) @[zyguan](https://github.com/zyguan)
    - Fix the issue that executing `SELECT INTO OUTFILE` using the `PREPARE` method incorrectly returns a success message instead of an error [#49166](https://github.com/pingcap/tidb/issues/49166) @[qw4990](https://github.com/qw4990)
    - Fix the issue that executing `UNIQUE` index lookup with an `ORDER BY` clause might cause an error [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - Fix the issue that the `DELETE` and `UPDATE` statements using index lookup might report an error when `tidb_multi_statement_mode` mode is enabled [#50012](https://github.com/pingcap/tidb/issues/50012) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiDB might not simultaneously establish the new statistics metadata when executing a large number of `CREATE TABLE` statements in a short period of time [#36004](https://github.com/pingcap/tidb/issues/36004) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that the `LEADING` hint does not take effect in `UNION ALL` statements [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that using old interfaces might cause inconsistent metadata for tables [#49751](https://github.com/pingcap/tidb/issues/49751) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that common hints do not take effect in `UNION ALL` statements [#50068](https://github.com/pingcap/tidb/issues/50068) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that TiDB returns wrong query results when processing `ENUM` or `SET` types by constant propagation [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)

+ TiKV

    - Fix the issue that TiKV might panic when gRPC threads are checking `is_shutdown` [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)
    - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - Fix the issue that TiDB and TiKV might produce inconsistent results when processing `DECIMAL` arithmetic multiplication truncation [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)

+ PD

    - Fix the issue that querying a Region without a leader using `pd-ctl` might cause PD to panic [#7630](https://github.com/tikv/pd/issues/7630) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Fix the issue that the `lowerUTF8` and `upperUTF8` functions do not allow characters in different cases to occupy different bytes [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that TiFlash panics after executing `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`, which changes nullable columns to non-nullable [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that after terminating a query, TiFlash crashes due to concurrent data conflicts when a large number of tasks on TiFlash are canceled at the same time [#7432](https://github.com/pingcap/tiflash/issues/7432) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the `Unsupported collation` error is reported when you restore data from backups of an old version [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)
        - Fix the issue that BR cannot retry when encountering an error while reading file content from S3 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that log backup gets stuck after changing the TiKV IP address on the same node [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Fix the issue that after filtering out `add table partition` events is configured in `ignore-event`, TiCDC does not replicate other types of DML changes for related partitions to the downstream [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the changefeed reports an error after `TRUNCATE PARTITION` is executed on the upstream table [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that the changefeed `resolved ts` does not advance in extreme cases [#10157](https://github.com/pingcap/tiflow/issues/10157) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC returns the `ErrChangeFeedAlreadyExists` error when concurrently creating multiple changefeeds [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning might fail to import data when EBS BR is running [#49517](https://github.com/pingcap/tidb/issues/49517) @[mittalrishabh](https://github.com/mittalrishabh)
        - Fix the issue that data might be lost when TiDB Lightning ingests files in batches [#50198](https://github.com/pingcap/tidb/issues/50198) @[D3Hunter](https://github.com/D3Hunter)

---
title: TiDB 6.1.3 Release Notes
---

# TiDB 6.1.3 Release Notes

Release date: December 5, 2022

TiDB version: 6.1.3

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.1.3#version-list)

## Compatibility changes

- Tools

    - TiCDC

        - Change the default value of [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb) from `table` to `none`, which helps reduce replication latency and reduce OOM risks, and ensures that only a few transactions (the size of a single transaction exceeds 1024 rows) are split, instead of all transactions [#7505](https://github.com/pingcap/tiflow/issues/7505) [#5231](https://github.com/pingcap/tiflow/issues/5231) @[asddongmen](https://github.com/asddongmen)

## Improvements

- PD

    - Optimize the granularity of locks to reduce lock contention and improve the capability of processing heartbeat in high concurrency [#5586](https://github.com/tikv/pd/issues/5586) @[rleungx](https://github.com/rleungx)

- Tools

    - TiCDC

        - Enable transaction split and disable the safe mode of a changefeed in TiCDC by default to improve performance [#7505](https://github.com/pingcap/tiflow/issues/7505) @[asddongmen](https://github.com/asddongmen)
        - Improve the performance of Kafka protocol encoder [#7540](https://github.com/pingcap/tiflow/issues/7540), [#7532](https://github.com/pingcap/tiflow/issues/7532), [#7543](https://github.com/pingcap/tiflow/issues/7543) @[sdojjy](https://github.com/sdojjy) @[3AceShowHand](https://github.com/3AceShowHand)

- Others

    - Upgrade the Go compiler version of TiDB from go1.18 to [go1.19](https://go.dev/doc/go1.19), which improves the TiDB stability. Specifically, a Go environment variable [`GOMEMLIMIT`](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables) is introduced to keep the memory usage of TiDB below a certain threshold. This helps mitigate most OOM issues. For more information, see [Mitigate OOM issues by configuring the `GOMEMLIMIT`](/configure-memory-usage.md#mitigate-oom-issues-by-configuring-gomemlimit).

## Bug fixes

+ TiDB

    - Fix the issue that the `grantor` field is missing in the `mysql.tables_priv` table [#38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue of the wrong query result that occurs when the mistakenly pushed-down conditions are discarded by Join Reorder [#38736](https://github.com/pingcap/tidb/issues/38736) @[winoros](https://github.com/winoros)
    - Fix the issue that the lock acquired by `get_lock()` cannot hold for more than 10 minutes [#38706](https://github.com/pingcap/tidb/issues/38706) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the auto-increment column cannot be used with check constraint [#38894](https://github.com/pingcap/tidb/issues/38894) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the gPRC log is output to a wrong file [#38941](https://github.com/pingcap/tidb/issues/38941) @[xhebox](https://github.com/xhebox)
    - Fix the issue that the TiFlash sync status of a table is not deleted from etcd when the table is truncated or dropped [#37168](https://github.com/pingcap/tidb/issues/37168) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that data files can be accessed unrestrainedly via data source name injection (CVE-2022-3023) [#38541](https://github.com/pingcap/tidb/issues/38541) @[lance6716](https://github.com/lance6716)
    - Fix the issue that the function `str_to_date` returns wrong result in the `NO_ZERO_DATE` SQL mode [#39146](https://github.com/pingcap/tidb/issues/39146) @[mengxin9014](https://github.com/mengxin9014)
    - Fix the issue that statistics collection tasks in the background might panic [#35421](https://github.com/pingcap/tidb/issues/35421) @[lilinghai](https://github.com/lilinghai)
    - Fix the issue that in some scenarios the pessimistic lock is incorrectly added to the non-unique secondary index [#36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)

- PD

    - Fix inaccurate Stream timeout and accelerate leader switchover [#5207](https://github.com/tikv/pd/issues/5207) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiKV

    - Fix abnormal Region competition caused by expired lease during snapshot acquisition [#13553](https://github.com/tikv/tikv/issues/13553) @[SpadeA-Tang](https://github.com/SpadeA-Tang)

+ TiFlash

    - Fix the issue that logical operators return wrong results when the argument type is `UInt8` [#6127](https://github.com/pingcap/tiflash/issues/6127) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that wrong data input for `CAST(value AS DATETIME)` causing high TiFlash sys CPU [#5097](https://github.com/pingcap/tiflash/issues/5097) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that heavy write pressure might generate too many column files in the delta layer [#6361](https://github.com/pingcap/tiflash/issues/6361) @[lidezhu](https://github.com/lidezhu)
    - Fix the issue that column files in the delta layer cannot be compacted after restarting TiFlash [#6159](https://github.com/pingcap/tiflash/issues/6159) @[lidezhu](https://github.com/lidezhu)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that restore tasks fail when using old framework for collations in databases or tables [#39150](https://github.com/pingcap/tidb/issues/39150) @[MoCuishle28](https://github.com/MoCuishle28)

    + TiCDC

        - Fix data loss occurred in the scenario of executing DDL statements first and then pausing and resuming the changefeed [#7682](https://github.com/pingcap/tiflow/issues/7682) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the sink component gets stuck if the downstream network is unavailable [#7706](https://github.com/pingcap/tiflow/issues/7706) @[hicqu](https://github.com/hicqu)

    + TiDB Data Migration (DM)

        - Fix the issue that when `collation_compatible` is set to `"strict"`, DM might generate SQL with duplicated collations [#6832](https://github.com/pingcap/tiflow/issues/6832) @[lance6716](https://github.com/lance6716)
        - Fix the issue that DM tasks might stop with an `Unknown placement policy` error [#7493](https://github.com/pingcap/tiflow/issues/7493) @[lance6716](https://github.com/lance6716)
        - Fix the issue that relay logs might be pulled from upstream again in some cases [#7525](https://github.com/pingcap/tiflow/issues/7525) @[liumengya94](https://github.com/liumengya94)
        - Fix the issue that data is replicated for multiple times when a new DM worker is scheduled before the existing worker exits [#7658](https://github.com/pingcap/tiflow/issues/7658) @[GMHDBJD](https://github.com/GMHDBJD)

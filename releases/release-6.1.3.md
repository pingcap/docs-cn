---
title: TiDB 6.1.3 Release Notes
---

# TiDB 6.1.3 Release Notes

发版日期：2022 年 xx 月 xx 日

TiDB 版本：6.1.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.1.3#version-list)

## 提升改进

## Bug 修复

+ TiDB

    <!--sql-infra and tidb owner: bb7133-->

    - (dup) 修复 `mysql.tables_priv` 表中 `grantor` 字段缺失的问题 [#38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup) 修复错误下推的条件被 Join Reorder 丢弃后导致查询结果错误的问题 [#38736](https://github.com/pingcap/tidb/issues/38736) @[winoros](https://github.com/winoros)
    - Fix an issue that `get_lock()` cannot hold for more than 10 minutes. [#38706](https://github.com/pingcap/tidb/issues/38706) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the auto increment column cannot be used with check constraint. [#38894](https://github.com/pingcap/tidb/issues/38894) @[YangKeao](https://github.com/YangKeao)
    - Fix broken log rotation of grpc [#38941](https://github.com/pingcap/tidb/issues/38941) @[xhebox](https://github.com/xhebox)
    - Delete TiFlash sync status from etcd when table is truncated or dropped [#37168](https://github.com/pingcap/tidb/issues/37168) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue of arbitrary file read via data source name injection (CVE-2022-3023). [#38541](https://github.com/pingcap/tidb/issues/38541) @[lance6716](https://github.com/lance6716)

    <!--executor owner: zanmato1984-->

    <!--planner owner: qw4990-->

    <!--transaction owner:cfzjywxk -->

    - (dup) 修复部分场景非唯一二级索引被误加悲观锁的问题 [#36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)

- PD

    <!--owner: nolouch -->

    - (dup) 修复 Stream 超时问题，提高 Leader 切换的速度 [#5207](https://github.com/tikv/pd/issues/5207) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiKV

    <!--owner: tonyxuqqi-->

    - (dup) 修复获取 Snapshot 时 Lease 过期引发的异常竞争问题  [#13553](https://github.com/tikv/tikv/issues/13553) @[SpadeA-Tang](https://github.com/SpadeA-Tang)

+ TiFlash

    <!--compute owner: zanmato1984 -->

    - (dup) 修复逻辑运算符在 UInt8 类型下查询结果出错的问题 [#6127](https://github.com/pingcap/tiflash/issues/6127)
    - (dup) 修复 `CAST(value AS datetime)` 输入数据无法转成 `DATETIME` 时会导致 TiFlash sys CPU 异常高的问题 [#5097](https://github.com/pingcap/tiflash/issues/5097) @[xzhangxian1008](https://github.com/xzhangxian1008)

    <!--storage owner: flowbehappy -->

    - 修复高压力写可能产生太多 delta 层小文件的问题 [#6361](https://github.com/pingcap/tiflash/issues/6361) @[lidezhu](https://github.com/lidezhu)
    - Fix the problem that column files in delta layer cannot be compacted after restart tiflash [#6159](https://github.com/pingcap/tiflash/issues/6159) @[lidezhu](https://github.com/lidezhu)

+ Tools

    + Backup & Restore (BR)

    <!--owner: @3pointer-->

        - Fix a bug that: "Error Unsupported collation when new collation is enabled: 'utf8mb4_0900_ai_ci'" even if new_collation_enabled is false. [#39150](https://github.com/pingcap/tidb/issues/39150) @[MoCuishle28](https://github.com/MoCuishle28)

    + Dumpling

    <!--owner: @niubell-->

    + TiCDC

    <!--owner: @nongfushanquan-->

        - Fix an issue that causes data lost when pause and resume changefeed while executing DDL. [#7682](https://github.com/pingcap/tiflow/issues/7682) @[asddongmen](https://github.com/asddongmen)

    + TiDB Binlog

    <!--owner: @niubell-->

    + TiDB Data Migration (DM)

    <!--owner: @niubell-->

        - Fix the issue that when `collation_compatible` is set to `"strict"`, DM might generate SQL with duplicated collations [#6832](https://github.com/pingcap/tiflow/issues/6832) @[lance6716](https://github.com/lance6716)
        - Fix sometime DM task is stopped with error "Unknown placement policy" [#7493](https://github.com/pingcap/tiflow/issues/7493) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

    <!--owner: @niubell-->

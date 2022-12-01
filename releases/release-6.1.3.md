---
title: TiDB 6.1.3 Release Notes
---

# TiDB 6.1.3 Release Notes

发版日期：2022 年 xx 月 xx 日

TiDB 版本：6.1.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.1.3#version-list)

## 提升改进

- PD

<!--owner: nolouch -->

    - 优化锁粒度，提升高并发下心跳的处理能力 [#5586](https://github.com/tikv/pd/issues/5586) @[rleungx](https://github.com/rleungx)

- Tools

    - TiCDC

    <!--owner: @nongfushanquan-->

        - 修改同步任务 safe-mode 和拆分大事务默认值提升性能  [#7505](https://github.com/pingcap/tiflow/issues/7505) @[asddongmen](https://github.com/asddongmen)
        - 提升 Kafka 相关协议的编码性能. [#7540](https://github.com/pingcap/tiflow/issues/7540), [#7532](https://github.com/pingcap/tiflow/issues/7532), [#7543](https://github.com/pingcap/tiflow/issues/7543) @[sdojjy](https://github.com/sdojjy) @[3AceShowHand](https://github.com/3AceShowHand)

## Bug 修复

+ TiDB

    <!--sql-infra and tidb owner: hawkingrei-->

    - (dup) 修复 `mysql.tables_priv` 表中 `grantor` 字段缺失的问题 [#38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup) 修复错误下推的条件被 Join Reorder 丢弃后导致查询结果错误的问题 [#38736](https://github.com/pingcap/tidb/issues/38736) @[winoros](https://github.com/winoros)
    - 修复 `get_lock()` 无法持续 10 分钟以上的问题 [#38706](https://github.com/pingcap/tidb/issues/38706) @[tangenta](https://github.com/tangenta)
    - 修复自增列不能和检查约束一起使用的问题 [#38894](https://github.com/pingcap/tidb/issues/38894) @[YangKeao](https://github.com/YangKeao)
    - 修复了 gRPC 日志导出到错误文件的问题 [#38941](https://github.com/pingcap/tidb/issues/38941) @[xhebox](https://github.com/xhebox)
    - 修复当表被截断或删除时 TiFlash 同步状态未从 etcd 中删除的问题 [#37168](https://github.com/pingcap/tidb/issues/37168) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复通过数据源名称注入可读取任意文件的问题 (CVE-2022-3023) [#38541](https://github.com/pingcap/tidb/issues/38541) @[lance6716](https://github.com/lance6716)

    <!--executor owner: zanmato1984-->

    - 修复函数 `str_to_date` 在 `NO_ZERO_DATE` SQL Mode 下返回结果不正确的问题 [#39146](https://github.com/pingcap/tidb/issues/39146) @[mengxin9014](https://github.com/mengxin9014)

    <!--planner owner: qw4990-->

    - 修复后台统计信息任务可能崩溃的问题 [#35421](https://github.com/pingcap/tidb/issues/35421) @[lilinghai](https://github.com/lilinghai)

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
    - 修复 TiFlash 重启后 delta 层小文件无法合并的问题 [#6159](https://github.com/pingcap/tiflash/issues/6159) @[lidezhu](https://github.com/lidezhu)

+ Tools

    + Backup & Restore (BR)

    <!--owner: @3pointer-->

        - 修复数据库中使用旧的 collation 时恢复失败的问题  [#39150](https://github.com/pingcap/tidb/issues/39150) @[MoCuishle28](https://github.com/MoCuishle28)

    + Dumpling

    <!--owner: @niubell-->

    + TiCDC

    <!--owner: @nongfushanquan-->

        - 修复在执行 DDL 时，恢复暂停的 changefeed 会导致数据丢失的问题 [#7682](https://github.com/pingcap/tiflow/issues/7682) @[asddongmen](https://github.com/asddongmen)

    + TiDB Binlog

    <!--owner: @niubell-->

    + TiDB Data Migration (DM)

    <!--owner: @niubell-->

        - (dup) 修复当 `collation_compatible` 设置为 `"strict"` 时，DM 可能生成有重复排序规则的 SQL 语句的问题[#6832](https://github.com/pingcap/tiflow/issues/6832) @[lance6716](https://github.com/lance6716)
        - 修复 DM 可能由于 "Unknown placement policy" 错误导致任务暂停的问题 [#7493](https://github.com/pingcap/tiflow/issues/7493) @[lance6716](https://github.com/lance6716)
        - 修复在某些场景下 relay log 文件会从上游重新拉取的问题 [#7719](https://github.com/pingcap/tiflow/pull/7719) @[liumengya94](https://github.com/liumengya94)
        - 修复当 DM worker 即将退出时新 worker 调度过快导致数据被重复同步的问题 [#7745](https://github.com/pingcap/tiflow/pull/7745) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

    <!--owner: @niubell-->

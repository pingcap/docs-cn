---
title: TiDB 6.1.3 Release Notes
---

# TiDB 6.1.3 Release Notes

发版日期：2022 年 12 月 5 日

TiDB 版本：6.1.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup)

## 兼容性变更

- Tools

    - TiCDC

        - 将 [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#sink-uri-配置-mysqltidb) 的默认值从 `table` 修改为 `none`，降低同步延迟，减少系统出现 OOM 的风险。同时，系统只拆分少量的事务（即超过 1024 行的事务），而不再拆分所有事务 [#7505](https://github.com/pingcap/tiflow/issues/7505) [#5231](https://github.com/pingcap/tiflow/issues/5231) @[asddongmen](https://github.com/asddongmen)

## 提升改进

- PD

    - 优化锁的粒度以减少锁争用，提升高并发下心跳的处理能力 [#5586](https://github.com/tikv/pd/issues/5586) @[rleungx](https://github.com/rleungx)

- Tools

    - TiCDC

        - 默认情况下关闭 safeMode 并开启大事务拆分功能，提升同步的稳定性 [#7505](https://github.com/pingcap/tiflow/issues/7505) @[asddongmen](https://github.com/asddongmen)
        - 提升 Kafka 相关协议的编码性能 [#7540](https://github.com/pingcap/tiflow/issues/7540) [#7532](https://github.com/pingcap/tiflow/issues/7532) [#7543](https://github.com/pingcap/tiflow/issues/7543) @[sdojjy](https://github.com/sdojjy) @[3AceShowHand](https://github.com/3AceShowHand)

- 其他

    - 为了提升 TiDB 稳定性，缓解 OOM 问题，TiDB 的 Go 编译器版本从 go1.18 升级到了 [go1.19](https://go.dev/doc/go1.19)。通过设置 Go 环境变量 [`GOMEMLIMIT`](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables)，可以将 TiDB 的内存使用维持在预定的水位线以下，缓解大部分 OOM 问题。更多信息，详见[设置环境变量 `GOMEMLIMIT` 缓解 OOM 问题](/configure-memory-usage.md#设置环境变量-gomemlimit-缓解-oom-问题)。

## Bug 修复

+ TiDB

    - 修复 `mysql.tables_priv` 表中 `grantor` 字段缺失的问题 [#38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复错误下推的条件被 Join Reorder 丢弃后导致查询结果错误的问题 [#38736](https://github.com/pingcap/tidb/issues/38736) @[winoros](https://github.com/winoros)
    - 修复使用 `get_lock()` 获得的锁无法持续 10 分钟以上的问题 [#38706](https://github.com/pingcap/tidb/issues/38706) @[tangenta](https://github.com/tangenta)
    - 修复自增列不能和检查约束一起使用的问题 [#38894](https://github.com/pingcap/tidb/issues/38894) @[YangKeao](https://github.com/YangKeao)
    - 修复了 gRPC 日志导出到错误文件的问题 [#38941](https://github.com/pingcap/tidb/issues/38941) @[xhebox](https://github.com/xhebox)
    - 修复当表被截断或删除时 TiFlash 同步状态未从 etcd 中删除的问题 [#37168](https://github.com/pingcap/tidb/issues/37168) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复通过数据源名称注入可读取任意文件的问题 (CVE-2022-3023) [#38541](https://github.com/pingcap/tidb/issues/38541) @[lance6716](https://github.com/lance6716)
    - 修复函数 `str_to_date` 在 `NO_ZERO_DATE` SQL 模式下返回结果不正确的问题 [#39146](https://github.com/pingcap/tidb/issues/39146) @[mengxin9014](https://github.com/mengxin9014)
    - 修复后台统计信息任务可能崩溃的问题 [#35421](https://github.com/pingcap/tidb/issues/35421) @[lilinghai](https://github.com/lilinghai)
    - 修复部分场景非唯一二级索引被误加悲观锁的问题 [#36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)

- PD

    - 修复 Stream 超时问题，提高 Leader 切换的速度 [#5207](https://github.com/tikv/pd/issues/5207) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiKV

    - 修复获取 Snapshot 时 Lease 过期引发的异常竞争问题 [#13553](https://github.com/tikv/tikv/issues/13553) @[SpadeA-Tang](https://github.com/SpadeA-Tang)

+ TiFlash

    - 修复逻辑运算符在 `UInt8` 类型下查询结果出错的问题 [#6127](https://github.com/pingcap/tiflash/issues/6127) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 `CAST(value AS datetime)` 输入数据无法转成 `DATETIME` 时会导致 TiFlash sys CPU 异常高的问题 [#5097](https://github.com/pingcap/tiflash/issues/5097) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复高压力写入可能产生太多 delta 层小文件的问题 [#6361](https://github.com/pingcap/tiflash/issues/6361) @[lidezhu](https://github.com/lidezhu)
    - 修复 TiFlash 重启后 delta 层的小文件无法合并 (compact) 的问题 [#6159](https://github.com/pingcap/tiflash/issues/6159) @[lidezhu](https://github.com/lidezhu)

+ Tools

    + Backup & Restore (BR)

        - 修复数据库或数据表中使用旧的排序规则框架时数据恢复失败的问题 [#39150](https://github.com/pingcap/tidb/issues/39150) @[MoCuishle28](https://github.com/MoCuishle28)

    + TiCDC

        - 修复在执行 DDL 后，暂停然后恢复 changefeed 会导致数据丢失的问题 [#7682](https://github.com/pingcap/tiflow/issues/7682) @[asddongmen](https://github.com/asddongmen)
        - 修复下游网络发生异常时 sink 模块不能正确处理导致卡住的问题 [#7706](https://github.com/pingcap/tiflow/issues/7706) @[hicqu](https://github.com/hicqu)

    + TiDB Data Migration (DM)

        - 修复当 `collation_compatible` 设置为 `"strict"` 时，DM 可能生成有重复排序规则的 SQL 语句的问题 [#6832](https://github.com/pingcap/tiflow/issues/6832) @[lance6716](https://github.com/lance6716)
        - 修复 DM 可能由于 `Unknown placement policy` 错误导致任务停止的问题 [#7493](https://github.com/pingcap/tiflow/issues/7493) @[lance6716](https://github.com/lance6716)
        - 修复在某些场景下 relay log 文件会从上游重新拉取的问题 [#7525](https://github.com/pingcap/tiflow/issues/7525) @[liumengya94](https://github.com/liumengya94)
        - 修复当 DM worker 即将退出时新 worker 调度过快导致数据被重复同步的问题 [#7658](https://github.com/pingcap/tiflow/issues/7658) @[GMHDBJD](https://github.com/GMHDBJD)

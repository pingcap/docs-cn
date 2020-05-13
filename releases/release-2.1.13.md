---
title: TiDB 2.1.13 Release Notes
category: Releases
---

# TiDB 2.1.13 Release Notes

发版日期：2019 年 6 月 21 日

TiDB 版本：2.1.13

TiDB Ansible 版本：2.1.13

## TiDB

- 新增列属性包含 `AUTO_INCREMENT` 时利用 `SHARD_ROW_ID_BITS` 打散行 ID 功能，缓解热点问题 [#10788](https://github.com/pingcap/tidb/pull/10788)
- 优化无效 DDL 元信息存活时间，缩短集群升级后恢复 DDL 操作正常执行所需的时间 [#10789](https://github.com/pingcap/tidb/pull/10789)
- 修复因持有 `execdetails.ExecDetails` 指针时 Coprocessor 的资源无法快速释放导致的在大并发场景下 OOM 的问题 [#10833](https://github.com/pingcap/tidb/pull/10833)
- 新增 `update-stats`配置项，控制是否更新统计信息 [#10772](https://github.com/pingcap/tidb/pull/10772)
- 新增 3 个 TiDB 特有语法，支持预先切分 Region，解决热点问题：
    - 新增 Table Option `PRE_SPLIT_REGIONS` 选项 [#10863](https://github.com/pingcap/tidb/pull/10863)
    - 新增 `SPLIT TABLE table_name INDEX index_name` 语法 [#10865](https://github.com/pingcap/tidb/pull/10865)
    - 新增 `SPLIT TABLE [table_name] BETWEEN (min_value...) AND (max_value...) REGIONS [region_num]` 语法 [#10882](https://github.com/pingcap/tidb/pull/10882)
- 修复某些情况下 `KILL` 语句导致的 panic 问题 [#10879](https://github.com/pingcap/tidb/pull/10879)
- 增强 `ADD_DATE` 在某些情况下跟 MySQL 的兼容性 [#10718](https://github.com/pingcap/tidb/pull/10718)
- 修复 index join 中内表过滤条件在某些情况下的选择率估计错误的问题 [#10856](https://github.com/pingcap/tidb/pull/10856)

## TiKV

- 修复因迭代器未检查状态导致系统生成残缺 snapshot 的问题 [#4940](https://github.com/tikv/tikv/pull/4940)
- 新增检查 `block-size` 配置的有效性功能 [#4930](https://github.com/tikv/tikv/pull/4930)

## Tools

TiDB Binlog

- 修复 Pump 因写入失败时未检查返回值导致偏移量错误问题 [#640](https://github.com/pingcap/tidb-binlog/pull/640)
- Drainer 新增 `advertise-addr` 配置，支持容器环境中使用桥接模式 [#634](https://github.com/pingcap/tidb-binlog/pull/634)

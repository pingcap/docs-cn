---
title: TiDB 2.0.6 release notes
category: Releases
---

# TiDB 2.0.6 Release Notes

2018 年 8 月 6 日，TiDB 发布 2.0.6 版。该版本在 2.0.5 版的基础上，对系统兼容性、稳定性做出了改进。

## TiDB

- Improvements
    - 精简 "set system variable" 日志的长度，减少日志文件体积 [#7031](https://github.com/pingcap/tidb/pull/7031)
    - 在日志中记录 `ADD INDEX` 执行过程中的慢操作，便于定位问题 [#7083](https://github.com/pingcap/tidb/pull/7083)
    - 减少更新统计信息操作中的事务冲突 [#7138](https://github.com/pingcap/tidb/pull/7138)
    - 当待估算的值超过统计信息范围时，提高行数估计的准确度 [#7185](https://github.com/pingcap/tidb/pull/7185)
    - 当使用 `Index Join` 时，选择行数估计较小的表作为驱动表，提高 `Index Join` 的执行效率 [#7227](https://github.com/pingcap/tidb/pull/7227)
    - 为 `ANALYZE TABLE` 语句执行过程中发生的 panic 添加 recover 机制，避免收集统计信息过程中的异常行为导致 tidb-server 不可用 [#7228](https://github.com/pingcap/tidb/pull/7228)
    - 当 `RPAD`/`LPAD` 的结果超过设置系统变量 `max_allowed_packet` 时，返回 `NULL` 和对应的 warning，兼容 MySQL [#7244](https://github.com/pingcap/tidb/pull/7244)
    - 设置 `PREPARE` 语句中占位符数量上限为 65535，兼容 MySQL [#7250](https://github.com/pingcap/tidb/pull/7250)
- Bug Fixes
    - 修复某些情况下，`DROP USER` 语句和 MySQL 行为不兼容的问题 [#7014](https://github.com/pingcap/tidb/pull/7014)
    - 修复当 `tidb_batch_insert` 打开后，`INSERT`/`LOAD DATA` 等语句在某些场景下 OOM 的问题 [#7092](https://github.com/pingcap/tidb/pull/7092)
    - 修复某个表的数据持续更新时，其统计信息自动更新失效的问题 [#7093](https://github.com/pingcap/tidb/pull/7093)
    - 修复防火墙断掉不活跃的 gRPC 连接的问题 [#7099](https://github.com/pingcap/tidb/pull/7099)
    - 修复某些场景下使用前缀索引结果不正确的问题 [#7126](https://github.com/pingcap/tidb/pull/7126)
    - 修复某些场景下统计信息过时导致 panic 的问题 [#7155](https://github.com/pingcap/tidb/pull/7155)
    - 修复某些场景下 `ADD INDEX` 后索引数据少一条的问题 [#7156](https://github.com/pingcap/tidb/pull/7156)
    - 修复某些场景下查询唯一索引上的 `NULL` 值结果不正确的问题 [#7172](https://github.com/pingcap/tidb/pull/7172)
    - 修复某些场景下 `DECIMAL` 的乘法结果出现乱码的问题 [#7212](https://github.com/pingcap/tidb/pull/7212)
    - 修复某些场景下 `DECIMAL` 的取模运算结果不正确的问题 [#7245](https://github.com/pingcap/tidb/pull/7245)
    - 修复某些特殊语句序列下在事务中执行 `UPDATE`/`DELETE` 语句后结果不正确的问题 [#7219](https://github.com/pingcap/tidb/pull/7219)
    - 修复某些场景下 `UNION ALL`/`UPDATE` 语句在构造执行计划过程中 panic 的问题 [#7225](https://github.com/pingcap/tidb/pull/7225)
    - 修复某些场景下前缀索引的索引范围计算错误的问题 [#7231](https://github.com/pingcap/tidb/pull/7231)
    - 修复某些场景下 `LOAD DATA` 语句不写 binlog 的问题 [#7242](https://github.com/pingcap/tidb/pull/7242)
    - 修复某些场景下在 `ADD INDEX` 过程中 `SHOW CREATE TABLE` 结果不正确的问题 [#7243](https://github.com/pingcap/tidb/pull/7243)
    - 修复某些场景下 `Index Join` 因为没有初始化事务时间戳而 panic 的问题 [#7246](https://github.com/pingcap/tidb/pull/7246)
    - 修复 `ADMIN CHECK TABLE` 因为误用 session 中的时区而导致误报的问题 [#7258](https://github.com/pingcap/tidb/pull/7258)
    - 修复 `ADMIN CLEANUP INDEX` 在某些场景下索引没有清除干净的问题 [#7265](https://github.com/pingcap/tidb/pull/7265)
    - 禁用 Read Committed 事务隔离级别 [#7282](https://github.com/pingcap/tidb/pull/7282)

## TiKV

- Improvements
    - 扩大默认 scheduler slots 值以减少假冲突现象
    - 减少回滚事务的连续标记以提升冲突极端严重下的读性能
    - 限制 RocksDB log 文件的大小和个数以减少长时间运行下不必要的磁盘占用
- Bug Fixes
    - 修复字符串转 Decimal 时出现的 crash

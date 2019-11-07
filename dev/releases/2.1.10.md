---
title: TiDB 2.1.10 Release Notes
category: Releases
---

# TiDB 2.1.10 Release Notes

发版日期：2019 年 5 月 22 日

TiDB 版本：2.1.10

TiDB Ansible 版本：2.1.10

## TiDB

- 修复在使用 `tidb_snapshot` 读取历史数据的时候，某些异常情况导致的表结构不正确 [#10359](https://github.com/pingcap/tidb/pull/10359)
- 修复 `NOT` 函数在某些情况下导致的读取结果错误的问题 [#10363](https://github.com/pingcap/tidb/pull/10363)
- 修复 `Generated Column` 在 `Replace` 或者 `Insert on duplicate update` 语句中的错误行为 [#10385](https://github.com/pingcap/tidb/pull/10385)
- 修复 `BETWEEN` 函数在 `DATE`/`DATETIME` 类型比较的一个 bug [#10407](https://github.com/pingcap/tidb/pull/10407)
- 修复使用 `SLOW_QUERY` 表查询慢日志时，单行慢日志长度过长导致的报错 [#10412](https://github.com/pingcap/tidb/pull/10412)
- 修复某些情况下 `DATETIME` 和 `INTERVAL` 相加的结果跟 MySQL 不一致的问题 [#10416](https://github.com/pingcap/tidb/pull/10416)，[#10418](https://github.com/pingcap/tidb/pull/10418)
- 增加闰年二月的非法时间的检查 [#10417](https://github.com/pingcap/tidb/pull/10417)
- 内部的初始化操作限制只在 DDL Owner 中执行，避免了初始化集群的时候出现的大量冲突报错 [#10426](https://github.com/pingcap/tidb/pull/10426)
- 修复 `DESC` 在输出时间戳列的默认值为 `default current_timestamp on update current_timestamp` 时跟 MySQL 不兼容的问题 [#10337](https://github.com/pingcap/tidb/issues/10337)
- 修复 `Update` 语句中权限检查出错的问题 [#10439](https://github.com/pingcap/tidb/pull/10439)
- 修复 `CHAR` 类型的列在某些情况下 `RANGE` 计算错误导致的错误结果的问题 [#10455](https://github.com/pingcap/tidb/pull/10455)
- 避免 `ALTER SHARD_ROW_ID_BITS` 缩小 shard bits 位数在极低概率下，可能导致的数据错误 [#9868](https://github.com/pingcap/tidb/pull/9868)
- 修复 `ORDER BY RAND()` 不返回随机数字的问题 [#10064](https://github.com/pingcap/tidb/pull/10064)
- 禁止 `ALTER` 语句修改 DECIMAL 的精度 [#10458](https://github.com/pingcap/tidb/pull/10458)
- 修复 `TIME_FORMAT` 函数与 MySQL 的兼容问题 [#10474](https://github.com/pingcap/tidb/pull/10474)
- 检查 `PERIOD_ADD` 中参数的合法性 [#10430](https://github.com/pingcap/tidb/pull/10430)
- 修复非法的 `YEAR` 字符串在 TiDB 中的表现跟 MySQL 不兼容的问题 [#10493](https://github.com/pingcap/tidb/pull/10493)
- 支持 `ALTER DATABASE` 语法 [#10503](https://github.com/pingcap/tidb/pull/10503)
- 修复 `SLOW_QUERY` 内存表在慢语句没有 `;` 的情况下报错的问题 [#10536](https://github.com/pingcap/tidb/pull/10536)
- 修复某些情况下 `Partitioned Table` 的表 `Add index` 操作没有办法取消的问题 [#10533](https://github.com/pingcap/tidb/pull/10533)
- 修复在某些情况下无法抓住内存使用太多导致 OOM 的问题 [#10545](https://github.com/pingcap/tidb/pull/10545)
- 增强 DDL 操作改写表元信息的安全性 [#10547](https://github.com/pingcap/tidb/pull/10547)

## PD

- 修复 Leader 优先级不生效的问题 [#1533](https://github.com/pingcap/pd/pull/1533)

## TiKV

- 拒绝在最近发生过成员变更的 Region 上执行 transfer leader，防止迁移失败 [#4684](https://github.com/tikv/tikv/pull/4684)
- Coprocessor metrics 上添加 priority 标签 [#4643](https://github.com/tikv/tikv/pull/4643)
- 修复 transfer leader 中可能发生的脏读问题 [#4724](https://github.com/tikv/tikv/pull/4724)
- 修复某些情况下 `CommitMerge` 导致 TiKV 不能重启的问题 [#4615](https://github.com/tikv/tikv/pull/4615)
- 修复 unknown 的日志 [#4730](https://github.com/tikv/tikv/pull/4730)

## Tools

- TiDB Lightning
    - 新增 TiDB Lightning 发送数据到 importer 失败时进行重试 [#176](https://github.com/pingcap/tidb-lightning/pull/176)
- TiDB Binlog
    - 优化 Pump storage 组件 log，以利于排查问题 [#607](https://github.com/pingcap/tidb-binlog/pull/607)

## TiDB Ansible

- 更新 TiDB Lightning 配置文件，新增 `tidb_lightning_ctl` 脚本 [#d3a4a368](https://github.com/pingcap/tidb-ansible/commit/d3a4a368810a421c49980899a286cf010569b4c7)

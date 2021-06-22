---
title: TiDB 3.0.11 Release Notes
---

# TiDB 3.0.11 Release Notes

发版日期：2020 年 3 月 4 日

TiDB 版本：3.0.11

TiDB Ansible 版本：3.0.11

> **警告：**
>
> 该版本存在一些已知问题，已在新版本中修复，建议使用 3.0.x 的最新版本。

## 兼容性变化

* TiDB
    + 新增 `max-index-length` 配置项，用于控制索引支持的最大长度，用户可自由选择兼容 v3.0.7 之前版本或者兼容 MySQL [#15057](https://github.com/pingcap/tidb/pull/15057)

## 新功能

* TiDB
    + 新增在 `information_schema`.`PARTITIONS` 表中显示分区表的分区元信息的功能 [#14849](https://github.com/pingcap/tidb/pull/14849)

* TiDB Binlog
    + 新增 TiDB 集群之间数据双向复制功能 [#884](https://github.com/pingcap/tidb-binlog/pull/884) [#909](https://github.com/pingcap/tidb-binlog/pull/909)

* TiDB Lightning
    + 新增配置 TLS 功能 [#44](https://github.com/tikv/importer/pull/44) [#270](https://github.com/pingcap/tidb-lightning/pull/270)

* TiDB Ansible
    + 优化 `create_user.yml` 的逻辑，中控机使用的用户不必和 `ansible_user` 一致 [#1184](https://github.com/pingcap/tidb-ansible/pull/1184)

## Bug 修复

* TiDB
    + 修复由于涉及 `Union` 的查询没有标记为只读，在乐观事务开启重试时会导致 Goroutine 泄露的问题 [#15076](https://github.com/pingcap/tidb/pull/15076)
    + 修复执行 `SET SESSION tidb_snapshot = 'xxx';` 语句后，由于执行时未正确使用 `tidb_snapshot` 变量的值，导致 `SHOW TABLE STATUS` 未正确输出快照时刻表状态的问题 [#14391](https://github.com/pingcap/tidb/pull/14391)
    + 修复 `Sort Merge Join` 与 `ORDER BY DESC` 在同一条 SQL 语句中时，输出结果不正确的问题 [#14664](https://github.com/pingcap/tidb/pull/14664)
    + 修复创建分区表时，由于使用不支持的表达式，导致 TiDB server panic 的问题，修复后返回 `This partition function is not allowed` 错误信息 [#14769](https://github.com/pingcap/tidb/pull/14769)
    + 修复执行 `select max() from subquery` 语句且 Subquery 包含 `Union` 的子查询时，输出结果不正确的问题 [#14944](https://github.com/pingcap/tidb/pull/14944)
    + 修复执行 `DROP BINDING` 语句解除执行计划绑定后，执行 `SHOW BINDINGS` 语句系统返回错误信息的问题 [#14865](https://github.com/pingcap/tidb/pull/14865)
    + 修复查询语句中别名长度大于 256 时，由于在查询结果中未按照 MySQL 协议对[别名截断](https://dev.mysql.com/doc/refman/8.0/en/identifier-length.html)，导致连接被断开的问题 [#14940](https://github.com/pingcap/tidb/pull/14940)
    + 修复字符串类型被用作 `DIV` 中时，查询结果可能不正确的问题，例如：`select 1 / '2007' div 1` 现在可以被正确地执行 [#14098](https://github.com/pingcap/tidb/pull/14098)

* TiKV
    + 优化日志输出，删除部分不必要的日志 [#6657](https://github.com/tikv/tikv/pull/6657)
    + 修复 peer 在高负载情况下若被删除可能导致 panic 的问题 [#6704](https://github.com/tikv/tikv/pull/6704)
    + 修复 Hibernate Region 在某些特殊条件下未被正确唤醒的问题 [#6732](https://github.com/tikv/tikv/pull/6732) [#6738](https://github.com/tikv/tikv/pull/6738)

* TiDB Ansible
    + 修复 `tidb-ansible` 中失效、过期的文档链接 [#1169](https://github.com/pingcap/tidb-ansible/pull/1169)
    + 修复 `wait for region replication complete` task 可能出现未定义变量的问题 [#1173](https://github.com/pingcap/tidb-ansible/pull/1173)

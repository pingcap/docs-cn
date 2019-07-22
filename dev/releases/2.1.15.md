---
title: TiDB 2.1.15 Release Notes
category: Releases
---

# TiDB 2.1.15 Release Notes

发版日期：2019 年 7 月 18 日

TiDB 版本：2.1.15

TiDB Ansible 版本：2.1.15

## TiDB

+ 修复 `DATE_ADD` 函数处理微秒时由于没有对齐导致结果不正确的问题 [#11289](https://github.com/pingcap/tidb/pull/11289)
+ 修复 `DELETE` 语句中，字符串列中的空值与 FLOAT/INT 做比较时会报错的问题 [#11279](https://github.com/pingcap/tidb/pull/11279)
+ 修复 `INSERT` 函数参数有 `NULL` 值时，未正确返回 `NULL` 值的问题 [#11249](https://github.com/pingcap/tidb/pull/11249)
+ 修复在非字符串类型且长度为 0 的列建立索引时出错的问题 [#11215](https://github.com/pingcap/tidb/pull/11215)
+ 新增 `SHOW TABLE REGIONS` 的语句，支持通过 SQL 查询表的 Region 分布情况 [#11238](https://github.com/pingcap/tidb/pull/11238)
+ 修复 `UPDATE … SELECT` 语句因 `SELECT` 子查询中使用投影消除来优化规则所导致的报错 [#11254](https://github.com/pingcap/tidb/pull/11254)
+ 新增 `ADMIN PLUGINS ENABLE/DISABLE` SQL 语句，支持通过 SQL 动态开启/关闭 Plugin [#11189](https://github.com/pingcap/tidb/pull/11189)
+ Audit Plugin 新增审记连接功能 [#11189](https://github.com/pingcap/tidb/pull/11189)
+ 修复点查时，某列被查询多次而且结果为 NULL 时会 Panic 的问题 [#11227](https://github.com/pingcap/tidb/pull/11227)
+ 新增 `tidb_scatter_region` 配置项，控制创建表时是否开启自己打散 Record Region [#11213](https://github.com/pingcap/tidb/pull/11213)
+ 修复 `RAND` 函数由于非线程安全的 `rand.Rand` 导致的 Data Race 问题 [#11170](https://github.com/pingcap/tidb/pull/11170)
+ 修复某些情况下整数和非整数比较结果不正确的问题 [#11191](https://github.com/pingcap/tidb/pull/11191)
+ 支持修改 Database/Table 的 Collate，条件限制为 Database/Table 字符集必须是 UTF8/UTF8MB4 [#11085](https://github.com/pingcap/tidb/pull/11085)
+ 修复 `CURRENT_TIMESTAMP` 作为列的默认值且指定浮点精度时，`SHOW CREATE TABLE` 等语句显示精度不完整的问题 [#11087](https://github.com/pingcap/tidb/pull/11087)

## TiKV

+ 统一日志格式 [#5083](https://github.com/tikv/tikv/pull/5083)
+ 提高 region approximate size/key 在极端情况下的准确性，提升调度准确度 [#5085](https://github.com/tikv/tikv/pull/5085)

## PD

+ 统一日志格式 [#1625](https://github.com/pingcap/pd/pull/1625)

## Tools

TiDB Binlog

+ 优化 Pump GC 策略，去掉了未被在线 drainer 消费到的 binlog 保证不清理的限制 [#663](https://github.com/pingcap/tidb-binlog/pull/663)

TiDB Lightning

+ 修复 SQL dump 指明的列名不是小写时导入错误的问题 [#210](https://github.com/pingcap/tidb-lightning/pull/210)

## TiDB Ansible

+ TiDB Dashboard 新增 `parse duration` 和 `compile duration` 监控项，用于监测 SQL 语句解析耗时和执行计划编译耗时 [#815](https://github.com/pingcap/tidb-ansible/pull/815)

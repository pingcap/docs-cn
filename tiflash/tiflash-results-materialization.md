---
title: TiFlash 计算结果物化
summary: 介绍如何在同一个事务处理中物化保存 TiFlash 的计算结果。本功能为实验功能。
---

# TiFlash 计算结果物化

本文介绍如何在同一个事务处理中实现 TiFlash 计算结果的物化保存。

## 支持下推的算子

TiFlash 查询的结果可以通过 `INSERT INTO SELECT` 语句保存在一个 TiDB 表中：

```sql
INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name
    [PARTITION (partition_name [, partition_name] ...)]
    [(col_name [, col_name] ...)]
    SELECT ...
    [ON DUPLICATE KEY UPDATE assignment_list]value:
    {expr | DEFAULT}

assignment:
    col_name = valueassignment_list:
    assignment [, assignment] ...
```


## 使用场景和限制


### 执行过程


* SELECT 子句在 TiFlash 上执行，一般情况下优化器会自动选择，需要用户手动干预时可以通过设置 "tidb_enforce_mpp = TRUE" 来强制查询计划走 TiFlash
* SELECT 子句返回的结果首先回到集群中某单一 TiDB Server 节点，然后写入目标表（可以有 TiFlash 副本）
* 整条语句的执行保证 ACID 特性


### 限制
* 对写入部分事务大小（SELECT 子句返回的结果集）的硬性限制为 1 GB，推荐的使用场景是 100 MB以下。

* 若 SELECT 返回结果大小超过了 1GB，那么整条语句将会被强制终止
  * 用户会得到以下出错信息: "The query produced a too large intermediate result and thus failed"
* 并发限制
  * 目前并没有硬性限制，但是推荐用户考虑一下用法
  * 当“写事务”较大时，例如接近 1GB， 建议控制并发不超过 10
  * 当“写事务”较小时，例如小于 100MB， 建议控制并发不超过 30
  * 请基于测试和具体情况做出合理选择


### 典型和推荐的使用场景

1. 更高效的 BI 解决方案
很多报表类应用有较重的分析查询，如果有很多用户在同时打开和刷新报表则会产生较多的查询请求。一个有效的解决方案是使用本功能在 TiDB 表中保存报表查询的结果，报表刷新时从结果表中抽取数据，则可以避免多次重复的分析计算。同理，在保存历史分析记录的基础上，可以进一步优化长时间历史数据分析的计算量。例如某报表 A 分析每日的销售利润，使用本功能保存了每日的分析结果在某结果记录表 T 中，那么在生成报表 B 分析过去一月窗口的销售利润时，可以直接使用 T 中的每日分析结果数据，不仅大幅降低计算量也提升了查询响应速度，减轻系统负载。

2. 使用 TiFlash 服务在线应用
TiFlash 通常可以支持的并发请求视数据量和查询复杂度不同，但一般不会超过 100 QPS。用户可以通过保存 TiFlash 查询结果的方式，使用结果表来支持在线的高并发请求。后台的结果表数据更新可以以较低的频率进行，例如以 0.5s 间隔更新结果表数据也远低于 TiFlash 的并发上限，同时仍然较好地保证了数据新鲜度。

---
title: TiFlash 查询结果物化
summary: 介绍如何在同一个事务中保存 TiFlash 的查询结果。
---

# TiFlash 查询结果物化

> **警告：**
>
> 该功能目前是实验性功能，请注意使用场景限制。该功能会在未事先通知的情况下发生变化或删除。语法和实现可能会在 GA 前发生变化。如果发现 bug，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues) 反馈。

本文介绍如何在同一个事务 (`INSERT INTO SELECT`) 中实现 TiFlash 查询结果物化至某一指定的 TiDB 表中。

从 v6.5.0 起，执行 `INSERT INTO SELECT` 语句时，通过将 `SELECT` 子句下推到 TiFlash 可以把 TiFlash 计算得到的查询结果保存到指定的 TiDB 表中，即物化了 TiFlash 的查询结果。v6.5.0 之前的 TiDB 版本不允许此类行为，即通过 TiFlash 执行的查询必须是只读的，你需要从应用程序层面接收 TiFlash 返回的结果，然后另行在其它事务或处理中保存结果。

> **注意：**
>
> - 默认情况下 ([`tidb_allow_mpp = ON`](/system-variables#tidb_allow_mpp-从-v50-版本开始引入))，TiDB 优化器将依据查询代价智能选择下推查询到 TiKV 或 TiFlash。如需强制使用 TiFlash 查询，你可以设置系统变量 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-从-v51-版本开始引入) 为 `ON`。
> - 在实验特性阶段，该功能默认关闭。要开启此功能，请设置系统变量 [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-从-v630-版本开始引入) 为 `ON`。

`INSERT INTO SELECT` 语法如下：

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

例如，通过以下 `INSERT INTO SELECT` 语句，你可以将 `SELECT` 子句中表 `t1` 的查询结果保存到表 `t2` 中：

```sql
INSERT INTO t2 (name, country)
SELECT app_name, country FROM t1;
```

## 典型和推荐的使用场景

- 高效的 BI 解决方案

    很多报表类应用有较重的分析查询，如果有很多用户同时打开和刷新报表，则会产生较多的查询请求。一个有效的解决方案是使用本功能在 TiDB 表中保存报表查询的结果，报表刷新时再从结果表中抽取数据，则可以避免多次重复的分析计算。同理，在保存历史分析记录的基础上，可以进一步优化长时间历史数据分析的计算量。例如，某报表 A 用于分析每日的销售利润，使用本功能你可以将报表 A 中每日的分析结果保存到某结果表 T 中。那么，在生成报表 B 分析过去一个月的销售利润时，可以直接使用表 T 中的每日分析结果数据，不仅大幅降低计算量也提升了查询响应速度，减轻系统负载。

- 使用 TiFlash 服务在线应用

    TiFlash 支持的并发请求数量视数据量和查询复杂度不同，但一般不会超过 100 QPS。你可以使用本功能保存 TiFlash 的查询结果，然后通过查询结果表来支持在线的高并发请求。后台的结果表数据更新可以以较低的频率进行，例如以 0.5 秒间隔更新结果表数据也远低于 TiFlash 的并发上限，同时仍然较好地保证了数据新鲜度。

## 执行过程

* 在 `INSERT INTO SELECT` 语句的执行过程中，TiFlash 首先将 `SELECT` 子句的查询结果返回到集群中某单一 TiDB server 节点，然后再写入目标表（可以有 TiFlash 副本）。
* `INSERT INTO SELECT` 语句的执行保证 ACID 特性。

## 限制

* TiDB 对 `INSERT INTO SELECT` 语句的内存限制可以通过系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 调整。

    更多信息，请参考 [TiDB 内存控制](/configure-memory-usage.md)。

* TiDB 对 `INSERT INTO SELECT` 语句的并发没有硬性限制，但是推荐考虑以下用法：

    * 当“写事务”较大时，例如接近 1 GiB，建议控制并发不超过 10。
    * 当“写事务”较小时，例如小于 100 MiB，建议控制并发不超过 30。
    * 请基于测试和具体情况做出合理选择。
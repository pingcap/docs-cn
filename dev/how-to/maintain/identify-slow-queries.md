---
title: 定位慢查询
category: how-to
---

# 定位慢查询

TiDB 慢查询日志中记录了所有执行时间超过 [`slow-threshold`](/reference/configuration/tidb-server/configuration-file.md#slow-threshold) 的查询。从慢查询日志中找到一个慢查询后，接下来需要做的是分析它为什么慢，怎么优化。本文会从 TiDB SQL 执行原理层面列列举有哪些情况导致查询慢以及如何改进。

## 找到慢查询

需要注意的是，慢查询可以分为两类：

1. 确实执行的慢
2. 受集群上其他大查询拖累

要解决前者，首先需要能够在大量慢查询日志中剔除后者，甄别出真正执行慢的。这里推荐使用 TiDB 的慢查询解析功能。使用该功能，只需要在内置的慢查询表上执行几个查询即可大致筛选出真正执行慢的 SQL 语句。真正执行慢的 SQL 语句通常满足以下条件：

1. 它是一条用户 SQL 语句，也就是说 `is_internal` 需要为 `false`。
2. 它大部分的 cop task 执行时间都很长。

可以通过下面的查询从慢查询日志中找出 Cop Task 的执行时间最长的前 10 种用户 SQL 语句：

{{< copyable "sql" >}}

```sql
SELECT MAX(cop_proc_p90) AS max_cop_proc_p90,
       digest
FROM information_schema.slow_query
WHERE is_internal = false
GROUP BY digest
ORDER BY max_cop_proc_p90 DESC, digest
LIMIT 10;
```

如果通过上面的查询没有发现执行时间比较大的 SQL 语句，那么很可能集群某个 Region 成为了热点，这个 Region 上的请求非常多，导致 Cop Task 排队比较严重，查询的时间主要开销在了排队上。

如果发现了执行时间比较大的 SQL，那么可以再通过下面的查询看看具体是哪些 SQL 执行的慢：

{{< copyable "sql" >}}

```sql
SELECT query
FROM information_schema.slow_query
WHERE digest = ?;
```

## 常见慢查询原因

造成查询慢的原因有很多，这里常见的几种如下：

* 没有索引可用，只能全表扫描
* 优化器异常：
    * 没有选上最佳索引
    * 选错 Join 算法或者 Join Order
    * 选错聚合算法
* 执行引擎异常：
    * Region 有热点
    * MVCC 版本过多
    * 事务冲突

### 全表扫描

通过下面的查询能够发现那些有全表扫的慢查询 SQL 语句：

{{< copyable "sql" >}}

```sql
SELECT digest,
       count(*) AS no_index_count
FROM information_schema.slow_query
WHERE index_ids = ""
  AND is_internal = false
GROUP BY digest
ORDER BY no_index_count DESC
LIMIT 10;
```

然后再根据下面的查询找出这些具体的 SQL 语句：

{{< copyable "sql" >}}

```sql
SELECT query
FROM information_schema.slow_query
WHERE digest = ?;
```

是否有索引可用需要根据表结构和 SQL 查询具体分析，这里不再赘述。

### 优化器异常

优化器异常通常是统计信息过时导致的。统计信息过时后，TiDB 优化器会使用一个基于经验假设的代价估算逻辑对表上的查询进行代价估算。可以通过如下查询发现那些统计信息过时导致的慢查询：

{{< copyable "sql" >}}

```sql
SELECT digest,
       count(*) AS no_index_count
FROM information_schema.slow_query
WHERE stats like "%pseudo%"
  AND is_internal = false
GROUP BY digest
ORDER BY no_index_count DESC
LIMIT 10;
```

然后根据查询出来的 digest 值反查哪些表使用了 pseudo 的统计信息：

{{< copyable "sql" >}}

```sql
SELECT query, stats
FROM information_schema.slow_query
WHERE stats like "%pseudo%"
  AND digest = ?;
```

对于那些使用了 `pseudo` 统计信息的表，我们需要执行 [`ANALYZE`](/dev/reference/performance/statistics.md) 语句重新收集表的统计信息。

如果所有表的统计信息都已经是最新，但优化器做出来的执行计划仍然不是最优的，请[给 TiDB 提一个 issue](https://github.com/pingcap/tidb/issues/new/choose)，由官方人员处理。

### 执行引擎异常

1. Region 有热点

2. MVCC 旧版本过多

频繁的修改数据，比如 `INSERT`/`DELETE`/`UPDATE`/`REPLACE` 等语句，会导致数据的版本过多。MVCC 版本过多会导致查询处理时，TiKV 上扫描的 `Total_keys` 远大于 `Process_keys`。可以通过如下查询找到这类慢 SQL 语句：

{{< copyable "sql" >}}

```sql
SELECT digest,
       MAX(total_keys/process_keys) AS max_avg_version
FROM information_schema.slow_query
WHERE is_internal = false
GROUP BY digest
ORDER BY max_avg_version DESC
LIMIT 10;
```

3. 事务冲突

冲突会导致事务回退重试，可以通过下面的查询找到这类慢 SQL 语句：

{{< copyable "sql" >}}

```sql
SELECT digest,
       MAX(backoff_time) AS max_backoff_time
FROM information_schema.slow_query
GROUP BY digest
ORDER BY max_backoff_time DESC
LIMIT 10;
```

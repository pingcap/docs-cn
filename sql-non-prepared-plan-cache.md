---
title: 非 Prepare 语句执行计划缓存
summary: 介绍 TiDB 中非 Prepare 语句执行计划缓存的原理、使用方法及示例。
---

# 非 Prepare 语句执行计划缓存

对于某些非 `PREPARE` 语句，TiDB 可以像 [`Prepare`/`Execute` 语句](/sql-prepared-plan-cache.md)一样支持执行计划缓存。这可以让这些语句跳过优化器阶段，以提升性能。

开启非 Prepare 语句执行计划缓存可能会带来额外的内存和 CPU 开销，并不一定适用于所有场景。建议参考[性能收益](#性能收益)和[内存监控](#监控)章节，根据具体的使用情况决定是否开启该功能。

## 原理

Non-Prepared Plan Cache 为会话级别，并且与 [Prepared Plan Cache](/sql-prepared-plan-cache.md) 共用一个缓存。Non-Prepared Plan Cache 功能的基本原理如下：

1. 开启 Non-Prepared Plan Cache 后，TiDB 首先根据 AST（抽象语法树）对查询进行参数化。例如，将 `SELECT * FROM t WHERE b < 10 AND a = 1` 参数化为 `SELECT * FROM t WHERE b < ? and a = ?`。
2. 然后，使用参数化后的查询在 Plan Cache 中查找。
3. 如果能找到可以直接复用的计划，则直接使用，并跳过整个优化过程。
4. 否则，继续进行查询优化，并在最后将生成的计划放回到缓存中，以便下次复用。

## 使用方法

目前，你可以通过 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 开启或关闭 Non-Prepared Plan Cache。同时，你还可以通过 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-从-v710-版本开始引入) 来控制 Plan Cache 的大小。当缓存的计划数超过 `tidb_session_plan_cache_size` 时，TiDB 会使用 LRU (Least Recently Used) 策略进行逐出。

从 v7.1.0 开始，你可以通过变量 [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-从-v710-版本开始引入) 来设置可以缓存的计划的最大大小，默认为 2 MB。超过该值的执行计划将不会被缓存到 Plan Cache 中。

> **注意：**
>
> `tidb_session_plan_cache_size` 定义的内存会被 Prepared 和 Non-Prepared Plan Cache 共享。如果集群已经开启 Prepared Plan Cache，那么开启 Non-Prepared Plan Cache 可能降低原先 Prepared Plan Cache 的命中率。

## 示例

下面是一个使用示例：

1. 创建用于测试的表 `t`：

    ```sql
    CREATE TABLE t (a INT, b INT, KEY(b));
    ```

2. 开启 Non-Prepared Plan Cache：

    ```sql
    SET tidb_enable_non_prepared_plan_cache = ON;
    ```

3. 依次执行以下查询：

    ```sql
    SELECT * FROM t WHERE b < 10 AND a = 1;
    SELECT * FROM t WHERE b < 5 AND a = 2;
    ```

4. 查看第二个查询语句是否命中缓存：

    ```sql
    SELECT @@last_plan_from_cache;
    ```

    输出结果中 `last_plan_from_cache` 的值为 `1`，表示第二次执行的查询计划来自于缓存：

    ```sql
    +------------------------+
    | @@last_plan_from_cache |
    +------------------------+
    |                      1 |
    +------------------------+
    1 row in set (0.00 sec)
    ```

## 限制

### 缓存限制

TiDB 对参数化后形式相同的查询，只能缓存一个计划。例如，对于 `SELECT * FROM t WHERE a < 1` 和 `SELECT * FROM t WHERE a < 100000` 这两个查询语句，由于参数化后的形式相同，均为 `SELECT * FROM t WHERE a < ?`，因此它们会共用一个计划。

如果由此产生性能问题，可以使用 `ignore_plan_cache()` Hint 忽略计划缓存中的计划，让优化器每次重新为 SQL 生成执行计划。如果无法修改 SQL，可以通过创建 binding 来解决，例如 `CREATE BINDING FOR SELECT ... USING SELECT /*+ ignore_plan_cache() */ ...`。

### 使用限制

由于上述风险以及执行计划缓存只在简单查询上有明显收益（如果查询较为复杂，查询本身执行时间较长，使用执行计划缓存收益不大），TiDB 目前对 Non-Prepared Plan Cache 的生效范围有严格的限制。具体限制如下：

- [Prepared Plan Cache](/sql-prepared-plan-cache.md) 不支持的查询或者计划，Non-Prepared Plan Cache 也不支持。
- 不支持包含 `Window` 或 `Having` 的查询。
- 不支持包含三张表及以上 `Join` 或子查询的查询。
- 不支持 `ORDER BY` 或者 `GROUP BY` 后直接带数字或者表达式的查询，如 `ORDER BY 1`、`GROUP BY a+1`。仅支持 `ORDER BY column_name` 和 `GROUP BY column_name`。
- 不支持过滤条件中包含 `JSON`、`ENUM`、`SET` 或 `BIT` 类型的列的查询，例如 `SELECT * FROM t WHERE json_col = '{}'`。
- 不支持过滤条件中出现 `NULL` 值的查询，例如 `SELECT * FROM t WHERE a is NULL`。
- 默认不支持参数化后参数个数超过 200 个的查询，例如 `SELECT * FROM t WHERE a in (1, 2, 3, ... 201)`。从 v7.3.0 开始，你可以通过在 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-从-v653-和-v710-版本开始引入) 系统变量中设置 [`44823`](/optimizer-fix-controls.md#44823-从-v730-版本开始引入) 这个 Fix 来调整该限制。
- 不支持访问虚拟列、临时表、视图、或内存表的查询，例如 `SELECT * FROM INFORMATION_SCHEMA.COLUMNS`，其中 `COLUMNS` 为 TiDB 内存表。
- 不支持带有 Hint 或有 Binding 的查询。
- 默认不支持 DML 语句或包含 `FOR UPDATE` 的查询语句。若要启用支持，你可以执行 `SET tidb_enable_non_prepared_plan_cache_for_dml = ON`。

开启此功能后，优化器会对查询进行快速判断，如果不满足 Non-Prepared Plan Cache 的支持条件，则会走正常的优化流程。

## 性能收益

在内部测试中，开启 Non-Prepared Plan Cache 功能在大多数 TP 场景下可以获得显著的性能收益。例如：TPCC 测试中性能提升约 4%，一些 Bank 负载上提升超过 10%，在 Sysbench RangeScan 上提升达到 15%。

但是这个功能本身也会带来额外的 CPU 和内存开销，包括判断查询是否支持、对查询进行参数化、在 Plan Cache 中进行搜索等。如果负载中的多数查询无法被 Cache 命中，开启此功能反而可能影响性能。

此时，你需要观察 Grafana 监控中的 **Queries Using Plan Cache OPS** 面板中的 `non-prepared` 指标和 **Plan Cache Miss OPS** 面板中的 `non-prepared-unsupported` 指标。如果大多数查询都无法被支持，只有少部分查询能命中 Plan Cache，此时你可以关闭此功能。

![non-prepared-unsupported](/media/non-prepapred-plan-cache-unsupprot.png)

## 诊断

开启 Non-Prepared Plan Cache 后，可以使用 `EXPLAIN FORMAT='plan_cache' SELECT ...` 语句验证查询是否能够命中缓存。对于无法命中缓存的查询，系统会通过 warning 的方式返回无法命中的原因。

需要注意的是，如果不加 `FORMAT='plan_cache'`，则 `EXPLAIN` 语句永远不会命中缓存。

执行下面 `EXPLAIN FORMAT='plan_cache'` 语句，查看查询是否能够命中：

```sql
EXPLAIN FORMAT='plan_cache' SELECT * FROM (SELECT a+1 FROM t) t;
```

输出结果示例如下：

```sql
3 rows in set, 1 warning (0.00 sec)
```

通过 `SHOW warnings;` 查看无法命中缓存的查询信息：

```sql
SHOW warnings;
```

输出结果示例如下：

```sql
+---------+------+-------------------------------------------------------------------------------+
| Level   | Code | Message                                                                       |
+---------+------+-------------------------------------------------------------------------------+
| Warning | 1105 | skip non-prepared plan-cache: queries that have sub-queries are not supported |
+---------+------+-------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

可以看到在上述例子中，由于 Non-Prepared Plan Cache 不支持 `+` 操作，所以无法命中缓存。

## 监控

开启 Non-Prepared Plan Cache 后，可以在以下几个面板中查看缓存的内存使用情况、缓存中计划的个数、缓存命中的情况等信息。

![non-prepared-plan-cache](/media/tidb-non-prepared-plan-cache-metrics.png)

`statements_summary` 表和慢查询日志也会体现缓存的命中情况。下面是查看 `statements_summary` 表中缓存命中情况的例子：

1. 创建表 `t`：

    ```sql
    CREATE TABLE t (a int);
    ```

2. 打开 Non-Prepared Plan Cache 开关：

    ```sql
    SET @@tidb_enable_non_prepared_plan_cache = ON;
    ```

3. 依次执行以下三个查询：

    ```sql
    SELECT * FROM t WHERE a<1;
    SELECT * FROM t WHERE a<2;
    SELECT * FROM t WHERE a<3;
    ```

4. 查询 `statements_summary` 表查看查询命中缓存的情况：

    ```sql
    SELECT digest_text, query_sample_text, exec_count, plan_in_cache, plan_cache_hits FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE query_sample_text LIKE '%SELECT * FROM %';
    ```

    输出结果如下：

    ```sql
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | digest_text                     | query_sample_text                        | exec_count | plan_in_cache | plan_cache_hits |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | SELECT * FROM `t` WHERE `a` < ? | SELECT * FROM t WHERE a<1                |          3 |             1 |               2 |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    1 row in set (0.01 sec)
    ```

    可以看到，查询执行了三次且命中缓存两次。
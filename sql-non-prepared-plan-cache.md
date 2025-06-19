---
title: SQL 非预处理执行计划缓存
summary: 了解 TiDB 中 SQL 非预处理执行计划缓存的原理、用法和示例。
---

# SQL 非预处理执行计划缓存

TiDB 支持对某些非 `PREPARE` 语句进行执行计划缓存，类似于 [`Prepare`/`Execute` 语句](/sql-prepared-plan-cache.md)。此功能允许这些语句跳过优化阶段并提高性能。

启用非预处理计划缓存可能会带来额外的内存和 CPU 开销，可能并不适合所有情况。要确定是否在您的场景中启用此功能，请参考[性能优势](#性能优势)和[内存监控](#监控)部分。

## 原理

非预处理计划缓存是一个会话级别的功能，与[预处理计划缓存](/sql-prepared-plan-cache.md)共享一个缓存。非预处理计划缓存的基本原理如下：

1. 启用非预处理计划缓存后，TiDB 首先基于抽象语法树（AST）对查询进行参数化。例如，`SELECT * FROM t WHERE b < 10 AND a = 1` 被参数化为 `SELECT * FROM t WHERE b < ? and a = ?`。
2. 然后，TiDB 使用参数化的查询在计划缓存中搜索。
3. 如果找到可重用的计划，则直接使用它并跳过优化阶段。
4. 否则，优化器生成一个新计划并将其添加回缓存中，以供后续查询重用。

## 用法

要启用或禁用非预处理计划缓存，您可以设置 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 系统变量。您还可以使用 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) 系统变量控制非预处理计划缓存的大小。当缓存的计划数量超过 `tidb_session_plan_cache_size` 时，TiDB 使用最近最少使用（LRU）策略淘汰计划。

从 v7.1.0 开始，您可以使用系统变量 [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710) 控制可以缓存的计划的最大大小。默认值为 2 MB。如果计划的大小超过此值，则不会缓存该计划。

> **注意：**
>
> `tidb_session_plan_cache_size` 指定的内存在预处理和非预处理计划缓存之间共享。如果您已经为当前集群启用了预处理计划缓存，启用非预处理计划缓存可能会降低原有预处理计划缓存的命中率。

## 示例

以下示例展示如何使用非预处理计划缓存：

1. 创建一个测试表 `t`：

    ```sql
    CREATE TABLE t (a INT, b INT, KEY(b));
    ```

2. 启用非预处理计划缓存：

    ```sql
    SET tidb_enable_non_prepared_plan_cache = ON;
    ```

3. 执行以下两个查询：

    ```sql
    SELECT * FROM t WHERE b < 10 AND a = 1;
    SELECT * FROM t WHERE b < 5 AND a = 2;
    ```

4. 检查第二个查询是否命中缓存：

    ```sql
    SELECT @@last_plan_from_cache;
    ```

    如果输出中 `last_plan_from_cache` 的值为 `1`，表示第二个查询的执行计划来自缓存：

    ```sql
    +------------------------+
    | @@last_plan_from_cache |
    +------------------------+
    |                      1 |
    +------------------------+
    1 row in set (0.00 sec)
    ```

## 限制

### 缓存次优计划

TiDB 对于一个参数化查询只缓存一个计划。例如，查询 `SELECT * FROM t WHERE a < 1` 和 `SELECT * FROM t WHERE a < 100000` 共享相同的参数化形式 `SELECT * FROM t WHERE a < ?`，因此共享相同的计划。

如果这导致性能问题，您可以使用 `ignore_plan_cache()` 提示来忽略缓存中的计划，这样优化器每次都会为该 SQL 生成新的执行计划。如果无法修改 SQL，您可以创建绑定来解决问题。例如，`CREATE BINDING FOR SELECT ... USING SELECT /*+ ignore_plan_cache() */ ...`。

### 使用限制

由于上述风险，以及执行计划缓存仅对简单查询提供显著优势（如果查询复杂且执行时间较长，使用执行计划缓存可能帮助不大），TiDB 对非预处理计划缓存的范围有严格限制。限制如下：

- [预处理计划缓存](/sql-prepared-plan-cache.md)不支持的查询或计划，非预处理计划缓存也不支持。
- 不支持包含 `Window` 或 `Having` 等复杂运算符的查询。
- 不支持包含三个或更多 `Join` 表或子查询的查询。
- 不支持在 `ORDER BY` 或 `GROUP BY` 后直接包含数字或表达式的查询，如 `ORDER BY 1` 和 `GROUP BY a+1`。仅支持 `ORDER BY column_name` 和 `GROUP BY column_name`。
- 不支持对 `JSON`、`ENUM`、`SET` 或 `BIT` 类型列进行过滤的查询，如 `SELECT * FROM t WHERE json_col = '{}'`。
- 不支持对 `NULL` 值进行过滤的查询，如 `SELECT * FROM t WHERE a is NULL`。
- 默认不支持参数化后参数超过 200 个的查询，如 `SELECT * FROM t WHERE a in (1, 2, 3, ... 201)`。从 v7.3.0 开始，您可以通过在 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) 系统变量中设置 [`44823`](/optimizer-fix-controls.md#44823-new-in-v730) 修复来修改此限制。
- 不支持访问虚拟列、临时表、视图或内存表的查询，如 `SELECT * FROM INFORMATION_SCHEMA.COLUMNS`，其中 `COLUMNS` 是 TiDB 内存表。
- 不支持带有提示或绑定的查询。
- 默认不支持 DML 语句或带有 `FOR UPDATE` 子句的 `SELECT` 语句。要移除此限制，您可以执行 `SET tidb_enable_non_prepared_plan_cache_for_dml = ON`。

启用此功能后，优化器会快速评估查询。如果不满足非预处理计划缓存的支持条件，查询会回退到常规优化过程。

## 性能优势

在内部测试中，启用非预处理计划缓存功能在大多数 TP 场景下都能获得显著的性能优势。例如，在 TPC-C 测试中性能提升约 4%，在某些银行工作负载中提升超过 10%，在 Sysbench RangeScan 中提升 15%。

然而，此功能也会带来一些额外的内存和 CPU 开销，包括确定查询是否受支持、参数化查询和在缓存中搜索计划。如果缓存无法命中您工作负载中的大多数查询，启用它可能实际上会对性能产生不利影响。

在这种情况下，您需要观察 Grafana 上 **Queries Using Plan Cache OPS** 面板中的 `non-prepared` 指标和 **Plan Cache Miss OPS** 面板中的 `non-prepared-unsupported` 指标。如果大多数查询不受支持，只有少数能命中计划缓存，您可以禁用此功能。

![non-prepared-unsupported](/media/non-prepapred-plan-cache-unsupprot.png)

## 诊断

启用非预处理计划缓存后，您可以执行 `EXPLAIN FORMAT='plan_cache' SELECT ...` 语句来验证查询是否能命中缓存。对于无法命中缓存的查询，系统会在警告中返回原因。

请注意，如果您不添加 `FORMAT='plan_cache'`，`EXPLAIN` 语句将永远不会命中缓存。

要验证查询是否命中缓存，执行以下 `EXPLAIN FORMAT='plan_cache'` 语句：

```sql
EXPLAIN FORMAT='plan_cache' SELECT * FROM (SELECT a+1 FROM t) t;
```

输出如下：

```sql
3 rows in set, 1 warning (0.00 sec)
```

要查看无法命中缓存的查询，执行 `SHOW warnings;`：

```sql
SHOW warnings;
```

输出如下：

```sql
+---------+------+-------------------------------------------------------------------------------+
| Level   | Code | Message                                                                       |
+---------+------+-------------------------------------------------------------------------------+
| Warning | 1105 | skip non-prepared plan-cache: queries that have sub-queries are not supported |
+---------+------+-------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

在上述示例中，由于非预处理计划缓存不支持 `+` 操作，查询无法命中缓存。

## 监控

启用非预处理计划缓存后，您可以在以下面板中监控内存使用情况、缓存中的计划数量和缓存命中率：

![non-prepare-plan-cache](/media/tidb-non-prepared-plan-cache-metrics.png)

您还可以在 `statements_summary` 表和慢查询日志中监控缓存命中率。以下展示如何在 `statements_summary` 表中查看缓存命中率：

1. 创建表 `t`：

    ```sql
    CREATE TABLE t (a int);
    ```

2. 启用非预处理计划缓存：

    ```sql
    SET @@tidb_enable_non_prepared_plan_cache=ON;
    ```

3. 执行以下三个查询：

    ```sql
    SELECT * FROM t WHERE a<1;
    SELECT * FROM t WHERE a<2;
    SELECT * FROM t WHERE a<3;
    ```

4. 查询 `statements_summary` 表以查看缓存命中率：

    ```sql
    SELECT digest_text, query_sample_text, exec_count, plan_in_cache, plan_cache_hits FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE query_sample_text LIKE '%SELECT * FROM %';
    ```

    输出如下：

    ```sql
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | digest_text                     | query_sample_text                        | exec_count | plan_in_cache | plan_cache_hits |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | SELECT * FROM `t` WHERE `a` < ? | SELECT * FROM t WHERE a<1                |          3 |             1 |               2 |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    1 row in set (0.01 sec)
    ```

    从输出中可以看到，查询执行了三次，命中缓存两次。

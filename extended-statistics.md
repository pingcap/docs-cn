---
title: 使用扩展统计信息
summary: 了解如何使用扩展统计信息来指导 SQL 优化。
---

# 使用扩展统计信息

本文介绍如何使用扩展统计信息来指导 SQL 优化。TiDB 可以收集以下两种统计信息：

- 统计信息：如直方图和 Count-Min Sketch 等。更多详细信息，请参阅[统计信息](/statistics.md)。
- 扩展统计信息：按表和列过滤的统计信息。

> **建议：**
>
> 在阅读本文档之前，建议先阅读[使用统计信息](/statistics.md)。

手动或自动执行 `ANALYZE` 语句时，TiDB 默认只收集基础统计信息，不收集扩展统计信息。这是因为扩展统计信息仅用于特定场景下的优化器估算，而且收集扩展统计信息会造成额外的开销。

默认情况下，TiDB 不收集扩展统计信息。要使用扩展统计信息，你需要先启用扩展统计信息，然后单独注册每个扩展统计信息对象。

注册完成后，再执行 `ANALYZE` 语句时，TiDB 会同时收集常规统计信息和注册的扩展统计信息。

## 使用限制

在这些情况下，TiDB 不收集扩展统计信息：

- 仅收集索引的统计信息
- 使用 `ANALYZE INCREMENTAL` 命令收集统计信息
- 系统变量 `tidb_enable_fast_analyze` 的值为 `true` 时的统计信息收集

## 常用操作

### 启用扩展统计信息

要启用扩展统计，将系统变量 `tidb_enable_extended_stats` 的值设为 `ON`：

```sql
SET GLOBAL tidb_enable_extended_stats = ON;
```

该变量的默认值为 `OFF`。设置该变量会对所有扩展统计信息对象生效。

### 注册扩展统计信息

扩展统计信息的注册不是一次性任务，你需要单独注册每个扩展统计信息对象。

使用 SQL 语句 `ALTER TABLE ADD STATS_EXTENDED` 来注册，详细语法如下：

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

在以上语法中，你可以指定扩展统计信息的表名、统计信息名、统计信息类型和列名。

- `table_name` 指定目标表名，TiDB 将从该表收集扩展统计信息。
- `stats_name` 指定统计信息对象名，每张表的统计信息对象名必须是唯一的。
- `stats_type` 指定统计信息的类型，目前仅支持顺序相关性 (correlation) 类型。
- `column_name` 指定列组，可能包含多个列。目前只支持指定两个列名。

<details>
<summary>工作原理</summary>

每个 TiDB 节点都会在系统表 `mysql.stats_extended` 中维护一个缓存，以更高效地访问扩展统计信息。注册扩展统计信息后再执行 `ANALYZE` 语句时，如果系统表 `mysql.stats_extended` 中有对应的对象，TiDB 会收集扩展统计信息。

`mysql.stats_extended` 表中的每行都有 `version` 列。一旦某行更新了，该行对应的 `version` 值会增加。这样，TiDB 将表增量加载到内存中，而不是全量加载。

TiDB 会定期加载 `mysql.stats_extended` 表，以确保缓存与表中的数据保持一致。

> **警告：**
>
> **不推荐**直接对 `mysql.stats_extended` 系统表进行操作。否则，会出现不同 TiDB 节点的缓存不一致的情况。
>
> 如果误操作了该表，可以在每个 TiDB 节点上执行如下语句。执行后，当前缓存将被清除，`mysql.stats_extended` 表将被完全重新加载：
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 删除扩展统计信息

要删除扩展统计信息对象，使用以下语句：

```sql
ALTER TABLE table_name DROP STATS_EXTENDED stats_name;
```

<details>
<summary>工作原理</summary>

执行该语句后，TiDB 会将 `mysql.stats_extended` 表 `status` 列中对应对象的值标记为 `2`，而不是直接删除该对象。

其他 TiDB 节点会读取此更改，并将该对象从内存缓存中删除。后台垃圾回收 (GC) 最终会删除该对象。

> **警告：**
>
> **不推荐**直接对 `mysql.stats_extended` 系统表进行操作。否则，会出现不同 TiDB 节点的缓存不一致的情况。
>
> 如果误操作了该表，可以在每个 TiDB 节点上执行如下语句。执行后，当前缓存将被清除，`mysql.stats_extended` 表将被完全重新加载：
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 导出和导入扩展统计信息

导出或导入扩展统计信息的方式与导出或导入常规统计信息相同。详见[常规统计信息的导入导出](/statistics.md#统计信息的导入导出)。

## 顺序相关性扩展统计信息的使用示例

目前 TiDB 只支持顺序相关性类型 (correlation) 的扩展统计信息，用于估算范围查询 (range query) 中的行数并改进索引选择。以下示例展示了如何使用顺序相关性类型的扩展统计信息来估计范围查询中的行数。

### 第 1 步：定义表

定义一张表 `t`：

```sql
CREATE TABLE t(col1 INT, col2 INT, KEY(col1), KEY(col2));
```

假设表 `t` 中的 `col1` 和 `col2` 列的值都按行顺序服从单调递增的约束，即 `col1` 和 `col2` 的值在顺序上严格相关，相关因子为 `1`。

### 第 2 步：执行示例查询（不使用扩展统计信息）

在不使用扩展统计信息的情况下执行以下查询：

```sql
SELECT * FROM t WHERE col1 > 1 ORDER BY col2 LIMIT 1;
```

执行以上查询时，TiDB 优化器会通过以下其中一种方式来访问表 `t`：

- 使用 `col1` 上的索引访问表 `t`，然后将结果按 `col2` 排序以计算 `Top-1`。
- 对 `col2` 的索引按序扫描，直到遇到一条满足 `col1 > 1` 条件的记录后结束扫描。这种访问方式的开销主要取决于 TiDB 以 `col2` 的顺序扫描表时过滤掉了多少行。

在没有扩展统计的情况下，TiDB 优化器假设 `col1` 和 `col2` 是独立不相关的，这会**导致显著的估算误差**，使优化器选错索引。

### 第 3 步：启用扩展统计信息

将 `tidb_enable_extended_stats` 的值设为 `ON`，为 `col1` 和 `col2` 注册扩展统计信息对象：

```sql
ALTER TABLE t ADD STATS_EXTENDED s1 correlation(col1, col2);
```

注册后再执行 `ANALYZE` 时，TiDB 会计算表 `t` 上 `col` 和 `col2` 的[皮尔逊相关系数 (Pearson correlation coefficient)](https://zh.m.wikipedia.org/zh/皮尔逊积矩相关系数)，并将统计信息对象写入 `mysql.stats_extended` 表。

### 第 4 步：查看扩展统计信息的效果

在 TiDB 上开启了顺序相关性的扩展统计信息后，优化器可以更精确地估算要扫描的行数。

此时，对于[第 2 步：执行示例查询（不使用扩展统计信息）](#第-2-步执行示例查询不使用扩展统计信息)中的查询，`col1` 和 `col2` 满足严格顺序相关。如果 TiDB 对 `col2` 的索引按序扫描，直到遇到一条满足 `col1 > 1` 条件的记录后结束扫描，TiDB 优化器会将行数估计等价转换为以下查询：

```sql
SELECT * FROM t WHERE col1 <= 1 OR col1 IS NULL;
```

该查询结果加 1 即为对行数的最终估算值。这样可避免使用不恰当的独立不相关假设，并且**避免了重大的估算误差**。

如果列之间的相关因子（本例中为 `1`）小于系统变量 `tidb_opt_correlation_threshold` 的值，优化器会认为相关性不够从而依然使用独立不相关假设，但会对估算的行数启发式地调大。`tidb_opt_correlation_exp_factor` 的值越大，估算结果越大。相关因子的绝对值越大，估算结果越大。

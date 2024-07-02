---
title: 扩展统计信息
summary: 了解如何使用扩展统计信息指导优化器。
---

# 扩展统计信息

TiDB 可以收集以下两种类型的统计信息，本文主要介绍如何使用扩展统计信息来指导优化器。阅读本文前，建议先阅读[常规统计信息](/statistics.md)。

- 常规统计信息：主要关注单个列的统计信息，例如直方图和 Count-Min Sketch。这些统计信息对优化器估算查询成本至关重要。详情参见[常规统计信息](/statistics.md)。
- 扩展统计信息：主要关注指定列之间的数据相关性，指导优化器在查询有相关性的列时更精确地估算查询成本。

当手动或自动执行 `ANALYZE` 语句时，TiDB 默认只收集常规统计信息，不收集扩展统计信息。这是因为扩展统计信息仅在特定场景下用于优化器估算，而且收集扩展统计信息会增加额外开销。

扩展统计信息默认关闭。如果要收集扩展统计信息，请先启用扩展统计信息，然后逐个创建所需的扩展统计信息对象。创建完之后，下次执行 `ANALYZE` 语句时，TiDB 会同时收集常规统计信息和已创建对象的扩展统计信息。

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 使用限制

在以下场景下，TiDB 不会收集扩展统计信息：

- 仅在索引上收集统计信息
- 使用 `ANALYZE INCREMENTAL` 命令收集统计信息
- 系统变量 `tidb_enable_fast_analyze` 设置为 `true` 时收集统计信息

## 常用操作

### 启用扩展统计信息

要启用扩展统计信息，需要将系统变量 `tidb_enable_extended_stats` 设置为 `ON`：

```sql
SET GLOBAL tidb_enable_extended_stats = ON;
```

该变量的默认值为 `OFF`。该系统变量的设置对所有扩展统计信息对象生效。

### 创建扩展统计信息对象

创建扩展统计信息对象不是一次性任务，你需要为每个要收集的扩展统计信息分别创建对象。

要创建扩展统计信息对象，使用 SQL 语句 `ALTER TABLE ADD STATS_EXTENDED`。语法如下：

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

你可以在语法中指定要收集扩展统计信息的表名、统计信息名称、统计信息类型和列名。

- `table_name`：指定要收集扩展统计信息的表名。
- `stats_name`：指定统计信息对象的名称，每个表的统计信息对象名称必须唯一。
- `stats_type`：指定统计信息的类型。目前仅支持相关性 (correlation) 类型。
- `column_name`：指定列组，可以有多个列。目前只支持指定两个列名。

<details>
<summary>实现原理</summary>

为了提高访问性能，每个 TiDB 节点在系统表 `mysql.stats_extended` 中维护一份缓存，用于记录扩展统计信息。在创建扩展统计信息对象后，下次执行 `ANALYZE` 语句时，如果系统表 `mysql.stats_extended` 中有相应的对象，TiDB 将收集扩展统计信息。

`mysql.stats_extended` 系统表中的每一行都有一个 `version` 列。只要一行数据有更新，`version` 的值就会增加。这样，TiDB 会将表增量加载到内存中，而不是全量加载。

TiDB 定期加载 `mysql.stats_extended` 系统表，以确保缓存与表中的数据保持一致。

> **警告：**
>
> 不建议直接操作 `mysql.stats_extended` 系统表，否则不同 TiDB 节点上的缓存会不一致。如果误操作了该系统表，可以在每个 TiDB 节点上执行以下语句，以清除当前缓存，并重新加载 `mysql.stats_extended` 系统表：
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 删除扩展统计信息对象

要删除扩展统计信息对象，使用以下语句：

```sql
ALTER TABLE table_name DROP STATS_EXTENDED stats_name;
```

<details>
<summary>实现原理</summary>

在执行删除扩展统计信息对象的语句后，TiDB 不会直接删除 `mysql.stats_extended` 系统表中的对象，而是将相应对象的 `status` 列的值标记为 `2`。其它 TiDB 节点会读取这个变化，并删除内存缓存中的对象。后台的垃圾回收机制会最终删除该对象。

> **警告：**
>
> 不建议直接操作 `mysql.stats_extended` 系统表，否则不同 TiDB 节点上的缓存会不一致。如果误操作了该系统表，可以在每个 TiDB 节点上执行以下语句，以清除当前缓存，并重新加载 `mysql.stats_extended` 系统表：
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 导出和导入扩展统计信息

导出和导入扩展统计信息的方式与导出和导入常规统计信息的方式相同。详情参见[导出和导入常规统计信息](/statistics.md#导出和导入统计信息)。

## 相关性类型的扩展统计信息使用示例

目前，TiDB 仅支持相关性类型的扩展统计信息。该类型用于估算范围查询中的行数，并改善索引选择。以下示例展示了如何使用相关性类型的扩展统计信息来估算范围查询中的行数。

### 第 1 步：定义表

定义表 `t` 如下：

```sql
CREATE TABLE t(col1 INT, col2 INT, KEY(col1), KEY(col2));
```

假设表 `t` 的 `col1` 和 `col2` 在行顺序上都遵循单调递增的约束，这意味着 `col1` 和 `col2` 的值在顺序上严格相关，并且相关性系数为 `1`。

### 第 2 步：执行不使用扩展统计信息的示例查询

执行以下查询，不使用扩展统计信息：

```sql
SELECT * FROM t WHERE col1 > 1 ORDER BY col2 LIMIT 1;
```

对于上述查询的执行，TiDB 优化器会通过以下方式之一来访问表 `t`：

- 使用 `col1` 上的索引访问表 `t`，然后按 `col2` 对结果进行排序以计算 `Top-1`。
- 使用 `col2` 上的索引按顺序扫描表 `t`，直到遇到一条满足 `col1 > 1` 条件的记录后结束扫描。这种访问方式的代价主要取决于 TiDB 按 `col2` 的顺序扫描表时过滤掉了多少行。

在没有扩展统计信息的情况下，TiDB 优化器只会假设 `col1` 和 `col2` 是独立的，这会**导致显著的估算误差**。

### 第 3 步：启用扩展统计信息

将系统变量 `tidb_enable_extended_stats` 设置为 `ON`，并将 `col1` 和 `col2` 创建为扩展统计信息对象：

```sql
ALTER TABLE t ADD STATS_EXTENDED s1 correlation(col1, col2);
```

创建完统计信息对象后，当执行 `ANALYZE` 语句时，TiDB 会计算表 `t` 的 `col1` 和 `col2` 的[皮尔逊相关系数](https://zh.wikipedia.org/zh-cn/皮尔逊积矩相关系数)，并将对象写入 `mysql.stats_extended` 系统表。

### 第 4 步：查看扩展统计信息的效果

当 TiDB 有了相关性扩展统计信息后，优化器可以更准确地估算需要扫描的行数。

此时，对于上述[第 2 步](#第-2-步执行不使用扩展统计信息的示例查询)中的查询，`col1` 和 `col2` 在顺序上严格相关。如果 TiDB 通过 `col2` 上的索引按顺序扫描表 `t`，直到遇到一条满足 `col1 > 1` 条件的记录后结束扫描，优化器会将行数估算等价转换为以下查询：

```sql
SELECT * FROM t WHERE col1 <= 1 OR col1 IS NULL;
```

上述查询结果加 1 即为对行数的最终估算值。这样不再使用独立不相关假设，**避免了显著的估算误差**。

如果相关性系数（本例中为 `1`）小于系统变量 `tidb_opt_correlation_threshold` 的值，优化器会使用独立假设，但会试探性地调大估算值。`tidb_opt_correlation_exp_factor` 的值越大，估算结果越大。相关性系数的绝对值越大，估算结果越大。

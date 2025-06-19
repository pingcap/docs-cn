---
title: 扩展统计信息简介
summary: 了解如何使用扩展统计信息来指导优化器。
---

# 扩展统计信息简介

TiDB 可以收集以下两种类型的统计信息。本文介绍如何使用扩展统计信息来指导优化器。在阅读本文之前，建议您先阅读[统计信息简介](/statistics.md)。

- 基本统计信息：如直方图和 Count-Min Sketch 等统计信息，主要关注单个列。它们对优化器估算查询成本至关重要。详情请参见[统计信息简介](/statistics.md)。
- 扩展统计信息：关注指定列之间数据相关性的统计信息，当查询的列之间存在相关性时，可以指导优化器更精确地估算查询成本。

当手动或自动执行 `ANALYZE` 语句时，TiDB 默认只收集基本统计信息，不收集扩展统计信息。这是因为扩展统计信息仅在特定场景下用于优化器估算，且收集它们需要额外的开销。

扩展统计信息默认是禁用的。要收集扩展统计信息，您需要先启用扩展统计信息，然后逐个创建所需的扩展统计信息对象。创建对象后，下次执行 `ANALYZE` 语句时，TiDB 会同时收集基本统计信息和已创建对象的相应扩展统计信息。

> **警告：**
>
> 此功能是实验性的。不建议在生产环境中使用。此功能可能会在没有预先通知的情况下进行更改或删除。如果您发现 bug，可以在 GitHub 上提交[问题](https://github.com/pingcap/tidb/issues)。

## 限制

在以下场景中不会收集扩展统计信息：

- 仅对索引进行统计信息收集
- 使用 `ANALYZE INCREMENTAL` 命令进行统计信息收集
- 系统变量 `tidb_enable_fast_analyze` 的值设置为 `true` 时进行统计信息收集

## 常用操作

### 启用扩展统计信息

要启用扩展统计信息，请将系统变量 `tidb_enable_extended_stats` 设置为 `ON`：

```sql
SET GLOBAL tidb_enable_extended_stats = ON;
```

此变量的默认值为 `OFF`。此系统变量的设置适用于所有扩展统计信息对象。

### 创建扩展统计信息对象

创建扩展统计信息对象不是一次性任务。您需要为每个扩展统计信息对象重复创建。

要创建扩展统计信息对象，请使用 SQL 语句 `ALTER TABLE ADD STATS_EXTENDED`。语法如下：

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

在语法中，您可以指定要收集扩展统计信息的表名、统计信息名称、统计信息类型和列名。

- `table_name` 指定从中收集扩展统计信息的表的名称。
- `stats_name` 指定统计信息对象的名称，对于每个表必须是唯一的。
- `stats_type` 指定统计信息的类型。目前仅支持相关性类型。
- `column_name` 指定列组，可能有多个列。目前只能指定两个列名。

<details>
<summary>工作原理</summary>

为了提高访问性能，每个 TiDB 节点在系统表 `mysql.stats_extended` 中维护扩展统计信息的缓存。创建扩展统计信息对象后，下次执行 `ANALYZE` 语句时，如果系统表 `mysql.stats_extended` 有相应的对象，TiDB 将收集扩展统计信息。

`mysql.stats_extended` 表中的每一行都有一个 `version` 列。一旦行被更新，`version` 的值就会增加。这样，TiDB 就可以增量加载表，而不是完全加载。

TiDB 定期加载 `mysql.stats_extended` 以确保缓存与表中的数据保持一致。

> **警告：**
>
> **不建议**直接操作 `mysql.stats_extended` 系统表。否则，不同 TiDB 节点上会出现不一致的缓存。
>
> 如果您错误地操作了该表，可以在每个 TiDB 节点上执行以下语句。然后当前缓存将被清除，并且 `mysql.stats_extended` 表将被完全重新加载：
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 删除扩展统计信息对象

要删除扩展统计信息对象，请使用以下语句：

```sql
ALTER TABLE table_name DROP STATS_EXTENDED stats_name;
```

<details>
<summary>工作原理</summary>

执行语句后，TiDB 将 `mysql.stats_extended` 中相应对象的 `status` 列的值标记为 `2`，而不是直接删除对象。

其他 TiDB 节点将读取此更改并删除其内存缓存中的对象。后台垃圾收集最终会删除该对象。

> **警告：**
>
> **不建议**直接操作 `mysql.stats_extended` 系统表。否则，不同 TiDB 节点上会出现不一致的缓存。
>
> 如果您错误地操作了该表，可以在每个 TiDB 节点上使用以下语句。然后当前缓存将被清除，并且 `mysql.stats_extended` 表将被完全重新加载：
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 导出和导入扩展统计信息

导出或导入扩展统计信息的方式与导出或导入基本统计信息相同。详情请参见[统计信息简介 - 导入和导出统计信息](/statistics.md#导入和导出统计信息)。

## 相关性类型扩展统计信息的使用示例

目前，TiDB 仅支持相关性类型的扩展统计信息。此类型用于估算范围查询中的行数并改进索引选择。以下示例展示了如何使用相关性类型的扩展统计信息来估算范围查询中的行数。

### 步骤 1. 定义表

定义表 `t` 如下：

```sql
CREATE TABLE t(col1 INT, col2 INT, KEY(col1), KEY(col2));
```

假设表 `t` 的 `col1` 和 `col2` 都遵循行序单调递增约束。这意味着 `col1` 和 `col2` 的值在顺序上严格相关，相关因子为 `1`。

### 步骤 2. 在不使用扩展统计信息的情况下执行示例查询

在不使用扩展统计信息的情况下执行以下查询：

```sql
SELECT * FROM t WHERE col1 > 1 ORDER BY col2 LIMIT 1;
```

对于上述查询的执行，TiDB 优化器有以下选项来访问表 `t`：

- 使用 `col1` 上的索引访问表 `t`，然后按 `col2` 对结果进行排序以计算 `Top-1`。
- 使用 `col2` 上的索引来满足第一个满足 `col1 > 1` 的行。此访问方法的成本主要取决于 TiDB 按 `col2` 的顺序扫描表时过滤掉多少行。

没有扩展统计信息时，TiDB 优化器只假设 `col1` 和 `col2` 是独立的，这**会导致显著的估算误差**。

### 步骤 3. 启用扩展统计信息

将 `tidb_enable_extended_stats` 设置为 `ON`，并为 `col1` 和 `col2` 创建扩展统计信息对象：

```sql
ALTER TABLE t ADD STATS_EXTENDED s1 correlation(col1, col2);
```

在创建对象后执行 `ANALYZE` 时，TiDB 计算表 `t` 的 `col1` 和 `col2` 的[皮尔逊相关系数](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient)，并将对象写入 `mysql.stats_extended` 表。

### 步骤 4. 了解扩展统计信息带来的差异

在 TiDB 有了相关性的扩展统计信息后，优化器可以更精确地估算要扫描的行数。

此时，对于[步骤 2. 在不使用扩展统计信息的情况下执行示例查询](#步骤-2-在不使用扩展统计信息的情况下执行示例查询)中的查询，`col1` 和 `col2` 在顺序上严格相关。如果 TiDB 通过使用 `col2` 上的索引来访问表 `t` 以满足第一个满足 `col1 > 1` 的行，TiDB 优化器将等效地将行数估算转换为以下查询：

```sql
SELECT * FROM t WHERE col1 <= 1 OR col1 IS NULL;
```

上述查询结果加一将是最终的行数估算。这样，您就不需要使用独立性假设，并且**避免了显著的估算误差**。

如果相关因子（在本例中为 `1`）小于系统变量 `tidb_opt_correlation_threshold` 的值，优化器将使用独立性假设，但也会启发式地增加估算。`tidb_opt_correlation_exp_factor` 的值越大，估算结果越大。相关因子的绝对值越大，估算结果越大。

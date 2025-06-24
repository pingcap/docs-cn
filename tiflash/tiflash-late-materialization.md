---
title: TiFlash 延迟物化
summary: 介绍如何使用 TiFlash 延迟物化功能加速 OLAP 场景下的查询。
---

# TiFlash 延迟物化

> **注意：**
>
> TiFlash 延迟物化在[快速扫描模式](/tiflash/use-fastscan.md)下不生效。

TiFlash 延迟物化是一种用于加速 OLAP 场景查询的优化方法。您可以使用 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) 系统变量来控制是否启用或禁用 TiFlash 延迟物化。

- 当禁用时，为了处理带有过滤条件（`WHERE` 子句）的 `SELECT` 语句，TiFlash 会读取查询所需的所有列的数据，然后根据查询条件进行过滤和聚合。
- 当启用时，TiFlash 支持将部分过滤条件下推到 TableScan 算子。也就是说，TiFlash 首先扫描与下推到 TableScan 算子的过滤条件相关的列数据，过滤出满足条件的行，然后再扫描这些行的其他列数据进行进一步计算，从而减少数据处理的 IO 扫描和计算。

为了提高 OLAP 场景下某些查询的性能，从 v7.1.0 开始，TiFlash 延迟物化功能默认启用。TiDB 优化器可以根据统计信息和过滤条件决定下推哪些过滤条件，并优先下推过滤率高的过滤条件。有关详细算法，请参见 [RFC 文档](https://github.com/pingcap/tidb/tree/release-8.1/docs/design/2022-12-06-support-late-materialization.md)。

例如：

```sql
EXPLAIN SELECT a, b, c FROM t1 WHERE a < 1;
```

```
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
| id                      | estRows  | task         | access object | operator info                                         |
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
| TableReader_12          | 12288.00 | root         |               | MppVersion: 1, data:ExchangeSender_11                 |
| └─ExchangeSender_11     | 12288.00 | mpp[tiflash] |               | ExchangeType: PassThrough                             |
|   └─TableFullScan_9     | 12288.00 | mpp[tiflash] | table:t1      | pushed down filter:lt(test.t1.a, 1), keep order:false |
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
```

在这个例子中，过滤条件 `a < 1` 被下推到 TableScan 算子。TiFlash 首先读取列 `a` 的所有数据，然后过滤出满足 `a < 1` 条件的行。接下来，TiFlash 从这些过滤后的行中读取列 `b` 和 `c`。

## 启用或禁用 TiFlash 延迟物化

默认情况下，`tidb_opt_enable_late_materialization` 系统变量在会话和全局级别都为 `ON`，这意味着 TiFlash 延迟物化功能已启用。您可以使用以下语句查看相应的变量信息：

```sql
SHOW VARIABLES LIKE 'tidb_opt_enable_late_materialization';
```

```
+--------------------------------------+-------+
| Variable_name                        | Value |
+--------------------------------------+-------+
| tidb_opt_enable_late_materialization | ON    |
+--------------------------------------+-------+
```

```sql
SHOW GLOBAL VARIABLES LIKE 'tidb_opt_enable_late_materialization';
```

```
+--------------------------------------+-------+
| Variable_name                        | Value |
+--------------------------------------+-------+
| tidb_opt_enable_late_materialization | ON    |
+--------------------------------------+-------+
```

您可以在会话级别或全局级别修改 `tidb_opt_enable_late_materialization` 变量。

- 要在当前会话中禁用 TiFlash 延迟物化，使用以下语句：

    ```sql
    SET SESSION tidb_opt_enable_late_materialization=OFF;
    ```

- 要在全局级别禁用 TiFlash 延迟物化，使用以下语句：

    ```sql
    SET GLOBAL tidb_opt_enable_late_materialization=OFF;
    ```

    设置后，在新会话中 `tidb_opt_enable_late_materialization` 变量在会话和全局级别都将默认禁用。

要启用 TiFlash 延迟物化，使用以下语句：

```sql
SET SESSION tidb_opt_enable_late_materialization=ON;
```

```sql
SET GLOBAL tidb_opt_enable_late_materialization=ON;
```

## 实现机制

当过滤条件下推到 TableScan 算子时，TableScan 算子的执行过程主要包括以下步骤：

1. 读取 `<handle, del_mark, version>` 三列，执行多版本并发控制（MVCC）过滤，然后生成 MVCC Bitmap。
2. 读取与过滤条件相关的列，过滤出满足条件的行，然后生成 Filter Bitmap。
3. 对 MVCC Bitmap 和 Filter Bitmap 执行 `AND` 操作，生成 Final Bitmap。
4. 根据 Final Bitmap 读取剩余列的对应行。
5. 合并步骤 2 和步骤 4 中读取的数据，然后返回结果。

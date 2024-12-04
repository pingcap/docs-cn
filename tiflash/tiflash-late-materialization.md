---
title: TiFlash 延迟物化
summary: 介绍通过使用 TiFlash 延迟物化的方式来加速 OLAP 场景的查询。
---

# 延迟物化

> **注意：**
>
> 在 TiFlash [Fast Scan 模式](/tiflash/use-fastscan.md)下，延迟物化功能暂不可用。

TiFlash 延迟物化是加速 Online Analytical Processing (OLAP) 场景查询的一种优化方式。你可以通过修改变量 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-从-v700-版本开始引入) 来控制是否启用 TiFlash 延迟物化功能。

- 当关闭该功能时，如果 `SELECT` 语句中包含过滤条件（`WHERE` 子句），TiFlash 会先读取该查询所需列的全部数据，然后再根据查询条件对数据进行过滤、聚合等计算任务。
- 当开启该功能时，TiFlash 支持下推部分过滤条件到 TableScan 算子，即先扫描下推到 TableScan 算子的过滤条件相关的列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少 IO 扫描和数据处理的计算量。

为了提升 OLAP 场景部分查询的性能，从 v7.1.0 起，TiFlash 延迟物化功能默认开启，TiDB 优化器会根据统计信息和查询的过滤条件，决定哪些过滤条件会被下推。优化器会优先考虑下推过滤率高的过滤条件，详细算法可以参考 [RFC 文档](https://github.com/pingcap/tidb/tree/release-8.5/docs/design/2022-12-06-support-late-materialization.md)。

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

在此示例中，过滤条件 `a < 1` 被下推到了 TableScan 算子，TiFlash 会先读取列 `a` 的全部数据，然后根据过滤条件 `a < 1` 进行过滤，得到符合条件的行后，再读取这些行的列 `b` 和 `c` 的数据。

## 启用和禁用 TiFlash 延迟物化

默认情况下，session 和 global 级别的变量 `tidb_opt_enable_late_materialization=ON`，即开启 TiFlash 延迟物化功能。你可以通过以下语句来查看对应的变量信息。

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

变量 `tidb_opt_enable_late_materialization` 支持 session 级别和 global 级别的修改。

- 如果需要在当前 session 中关闭 TiFlash 延迟物化功能，可以通过以下语句设置:

    ```sql
    SET SESSION tidb_opt_enable_late_materialization=OFF;
    ```

- 如果需要在 global 级别关闭 TiFlash 延迟物化功能，可以通过以下语句设置：

    ```sql
    SET GLOBAL tidb_opt_enable_late_materialization=OFF;
    ```

    设置后，新建的会话中 session 和 global 级别 `tidb_opt_enable_late_materialization` 都将默认启用新值。

如需启用 TiFlash 延迟物化功能，可以通过以下语句设置：

```sql
SET SESSION tidb_opt_enable_late_materialization=ON;
```

```sql
SET GLOBAL tidb_opt_enable_late_materialization=ON;
```

## 实现机制

当有过滤条件下推到 TableScan 算子时，TableScan 算子的执行过程主要包括了以下步骤：

1. 读取 `<handle, del_mark, version>` 三列，执行多版本并发控制 (MVCC) 过滤，生成 MVCC Bitmap。
2. 读取过滤条件相关的列，过滤满足条件的行，生成 Filter Bitmap。
3. 将 MVCC Bitmap 和 Filter Bitmap 进行与操作 (AND)，生成 Final Bitmap。
4. 根据 Final Bitmap 读取剩余列的对应的行。
5. 合并第 2 步和第 4 步中读取的数据，返回结果。
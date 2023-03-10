---
title: TiFlash 延迟物化
summary: 介绍通过使用 TiFlash 延迟物化来加速 OLAP 场景的查询的方法。
---

# 延迟物化

> **警告：**
>
> 该功能目前是实验性功能，其形式和使用方法可能会在未来版本中发生变化。

本文档介绍通过使用 TiFlash 延迟物化来加速 Online Analytical Processing (OLAP) 场景中查询的方法。

默认情况下，TiFlash 会先读取查询所需列的全部数据，然后再根据查询条件进行过滤，聚合等计算任务。延迟物化是一种优化方式，它支持将部分过滤条件下推。先扫描过滤条件相关列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少扫描 IO 和数据解析的计算量。

如果希望提升部分查询的性能，可以在 session 级别或 global 级别开启 TiFlash 延迟物化功能，你可以通过修改变量 `tidb_enable_late_materialization` 的值来选择是否启用 TiFlash 延迟物化功能。

启用 TiFlash 延迟物化功能后，TiDB 优化器会根据统计信息和查询的过滤条件，决定哪些过滤条件会被下推。优化器会优化考虑下推过滤率高的过滤条件，详细算法可以参考 [RFC 文档]()。

## 启用和禁用 TiFlash 延迟物化

默认情况下，session 和 global 级别的变量 `tidb_enable_late_materialization=OFF`，即没有开启 TiFlash 延迟物化 功能。你可以通过以下语句来查看对应的变量信息。

```
show variables like 'tidb_enable_late_materialization';
```

```
+----------------------------------+-------+
| Variable_name                    | Value |
+----------------------------------+-------+
| tidb_enable_late_materialization | OFF   |
+----------------------------------+-------+
```

```
show global variables like 'tidb_enable_late_materialization';
```

```
+----------------------------------+-------+
| Variable_name                    | Value |
+----------------------------------+-------+
| tidb_enable_late_materialization | OFF   |
+----------------------------------+-------+
```

变量 `tidb_enable_late_materialization` 支持 session 级别和 global 级别的修改。如果需要在当前 session 中启用 TiFlash 延迟物化功能，可以通过以下语句设置:

```
set session tidb_enable_late_materialization=ON;
```

如果对 global 级别的 `tidb_enable_late_materialization` 进行设置，设置后新建的会话中默认 session 和 global 变量 `tidb_enable_late_materialization` 启用新值。设置方式如下：

```
set global tidb_enable_late_materialization=ON;
```

可以用下面语句禁用 TiFlash 延迟物化:

```sql
set session tidb_enable_late_materialization=OFF;
set global tidb_enable_late_materialization=OFF;
```

## 实现机制

当有过滤条件下推到 TableScan 算子时，TableScan 算子过程整体包括了以下步骤：

1. 读 <handle, del_mark, version> 三列，执行 MVCC 过滤，生成 MVCC Bitmap。
2. 读过滤条件相关的列，执行过滤条件，生成 Filter Bitmap。
3. 通过 MVCC Bitmap 和 Filter Bitmap 做与操作生成 Final Bitmap。
4. 根据 Final Bitmap 读取剩余列的对应行。
5. 返回结果。
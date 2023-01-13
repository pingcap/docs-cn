---
title: TiFlash 性能调优
summary: 介绍 TiFlash 性能调优的方法，包括机器资源规划和 TiDB 参数调优。
---

# TiFlash 性能调优

本文介绍了 TiFlash 性能调优的几种方式，包括机器资源规划和 TiDB 参数调优，通过这些方式，TiFlash 性能可以达到最优状态。

## 资源规划

对于希望节省机器资源，并且完全没有隔离要求的场景，可以使用 TiKV 和 TiFlash 联合部署。建议为 TiKV 与 TiFlash 分别留够资源，同时避免共享磁盘。

## TiDB 相关参数调优

本部分介绍如何通过调整 TiDB 相关参数来提升 TiFlash 性能，具体包括如下几个方面：

- [强制开启 MPP 模式](#强制开启-mpp-模式)
- [聚合下推 `Join` 或 `Union`](#聚合下推-join-或-union)
- [开启 `Distinct` 优化](#开启-distinct-优化)
- [使用 `ALTER TABLE...COMPACT` 整理数据](#使用-alter-tablecompact-整理数据)
- [使用 Broadcast Hash Join 代替 Shuffled Hash Join](#使用-broadcast-hash-join-代替-shuffled-hash-join)
- [设置更大的执行并发度](#设置更大的执行并发度)
- [设置细粒度 Shuffle 参数](#设置细粒度-shuffle-参数)

### 强制开启 MPP 模式

MPP 执行计划可以充分利用分布式计算资源，从而显著提高批量数据查询的效率。当查询没有生成 MPP 执行计划的时候，你可以强制开启 MPP：

[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-从-v51-版本开始引入) 变量用于控制是否忽略优化器代价估算，强制使用 TiFlash 的 MPP 模式执行查询。要开启 MPP 模式查询，执行如下命令：

```sql
set @@tidb_enforce_mpp = ON;
```

### 聚合下推 `Join` 或 `Union`

将聚合操作下推到 `Join` 或 `Union` 之前执行，有可能能显著减少 `Join` 或 `Union` 需要处理的数据量，从而提升性能。

[`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down) 变量用来设置优化器是否执行聚合函数下推到 Join 之前的优化操作。当查询中聚合操作执行很慢时，可以尝试设置该变量为 `ON`。

```sql
set @@tidb_opt_agg_push_down = ON;
```

### 开启 `Distinct` 优化

TiFlash 暂时还不支持部分可接受 `Distinct` 列的聚合函数，比如 `Sum` 。默认情况下，整个聚合函数运算都会在 TiDB 端执行。通过开启 `Distinct` 优化，部分操作可以下推到 TiFlash，从而提升查询性能：

[`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down) 变量用来设置优化器是否执行带有 `Distinct` 的聚合函数（比如 `select sum(distinct a) from t`）下推到 Coprocessor 的优化操作。当查询中带有 `Distinct` 的聚合操作执行很慢时，可以尝试设置该变量为 `ON`。

```sql
set @@tidb_opt_distinct_agg_push_down = ON;
```

### 使用 `ALTER TABLE...COMPACT` 整理数据

[`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) 可以触发 TiFlash 节点对某个表或者某个分区进行数据整理。数据整理时，表中的物理数据会被重写，如清理已删除的数据、合并多版本数据等，从而可以获得更高的访问性能，并减少磁盘空间占用。

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

```sql
ALTER TABLE employees COMPACT PARTITION pNorth, pEast TIFLASH REPLICA;
```

### 使用 Broadcast Hash Join 代替 Shuffled Hash Join

对于有小表的 `Join` 算子，Broadcast Hash Join 可以避免大表的网络传输，从而提升计算性能。

- [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入)，单位为 bytes。如果表大小（字节数）小于该值，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。

    ```sql
    set @@tidb_broadcast_join_threshold_size = 2000000;
    ```

- [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入)，单位为行数。如果 join 的对象为子查询，优化器无法估计子查询结果集大小，在这种情况下通过结果集行数判断。如果子查询的行数估计值小于该变量，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。

    ```sql
    set @@tidb_broadcast_join_threshold_count = 100000;
    ```

### 设置更大的执行并发度

设置更大的执行并发度，可以让 TiFlash 占用更多系统 CPU 资源，从而提升查询性能。

[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-从-v610-版本开始引入)，单位为线程。用来设置 TiFlash 中 request 执行的最大并发度。

```sql
set @@tidb_max_tiflash_threads = 20;
```

### 设置细粒度 Shuffle 参数

细粒度 Shuffle 可以通过参数增加窗口函数执行的并发度，让函数执行占用更多系统资源，从而提升查询性能。

[`tiflash_fine_grained_shuffle_stream_count`](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-从-v620-版本开始引入)，单位为线程数。当窗口函数下推到 TiFlash 执行时，可以通过该变量控制窗口函数执行的并行度。

```sql
set @@tiflash_fine_grained_shuffle_stream_count = 20;
```

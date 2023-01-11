---
title: TiFlash 性能调优
aliases: ['/docs-cn/dev/tiflash/tune-tiflash-performance/','/docs-cn/dev/reference/tiflash/tune-performance/']
---

# TiFlash 性能调优

本文介绍了使 TiFlash 性能达到最优的几种方式，包括规划机器资源、TiDB 参数调优、配置 TiKV Region 大小等。

## 资源规划

对于希望节省机器资源，并且完全没有隔离要求的场景，可以使用 TiKV 和 TiFlash 联合部署。建议为 TiKV 与 TiFlash 分别留够资源，并且不要共享磁盘。

## TiDB 相关参数调优

1. 当没有生成 MPP 执行计划的时候，可以尝试强制开启 MPP：

    [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-从-v5.1-版本开始引入) 变量用于控制是否忽略优化器代价估算，强制使用 TiFlash 的 MPP 模式执行查询。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_enforce_mpp = 1;
    ```

2. 尝试开启聚合推过 `Join` / `Union` 等 TiDB 算子的优化：

    [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down) 变量用来设置优化器是否执行聚合函数下推到 Join 之前的优化操作。当查询中聚合操作执行很慢时，可以尝试设置该变量为 1。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_opt_agg_push_down = 1;
    ```

3. 尝试开启 `Distinct` 推过 `Join` / `Union` 等 TiDB 算子的优化：

    [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down) 变量用来设置优化器是否执行带有 `Distinct` 的聚合函数（比如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作。当查询中带有 `Distinct` 的聚合操作执行很慢时，可以尝试设置该变量为 `1`。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_opt_distinct_agg_push_down = 1;
    ```

4. 尝试使用 `ALTER TABLE ... COMPACT` 进行数据整理：

    [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) 可以触发 TiFlash 节点对某个表或者某个分区进行数据整理。数据整理时，表中的物理数据会被重写，如清理已删除的数据、合并多版本数据等，从而可以获得更高的访问性能，并减少磁盘空间占用。

    ```sql
    ALTER TABLE employees COMPACT TIFLASH REPLICA;
    ```

    ```sql
    ALTER TABLE employees COMPACT PARTITION pNorth, pEast TIFLASH REPLICA;
    ```

5. 尝试使用 Broadcast Hash Join 来代替 Shuffled Hash Join：

    - [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入)，单位为 bytes。如果表大小（字节数）小于该值，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。
    - [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入)，单位为行数。如果 join 的对象为子查询，优化器无法估计子查询结果集大小，在这种情况下通过结果集行数判断。如果子查询的行数估计值小于该变量，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_broadcast_join_threshold_count = 100000;
    ```

6. 尝试设置更大的执行并发度：

    [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-从-v6.1.0-版本开始引入)，单位为 bytes。用来设置 TiFlash 中 request 执行的最大并发度果表大小。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_max_tiflash_threads = 20;
    ```

7. 尝试设置细粒度 Shuffle 的相关参数：

    - [`tiflash_fine_grained_shuffle_stream_count`](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-从-v6.2.0-版本开始引入)，单位为线程数。当窗口函数下推到 TiFlash 执行时，可以通过该变量控制窗口函数执行的并行度。
    - [`tiflash_fine_grained_shuffle_batch_size`](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-从-v6.2.0-版本开始引入)，单位为 bytes。细粒度 shuffle 功能开启时，下推到 TiFlash 的窗口函数可以并行执行。该变量控制发送端发送数据的攒批大小。

    {{< copyable "sql" >}}

    ```sql
    set @@tiflash_fine_grained_shuffle_stream_count = 20;
    set @@tiflash_fine_grained_shuffle_batch_size = 20000;
    ```

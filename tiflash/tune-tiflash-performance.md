---
title: TiFlash 性能调优
---

# TiFlash 性能调优

本文介绍了使 TiFlash 性能达到最优的几种方式，包括规划机器资源、TiDB 参数调优、配置 TiKV Region 大小等。

## 资源规划

对于希望节省机器资源，并且完全没有隔离要求的场景，可以使用 TiKV 和 TiFlash 联合部署。建议为 TiKV 与 TiFlash 分别留够资源，并且不要共享磁盘。

## TiDB 相关参数调优

1. 对于 OLAP/TiFlash 专属的 TiDB 节点，建议调大读取并发数 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 到 80：

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_distsql_scan_concurrency = 80;
    ```

2. 开启 Super batch 功能：

    [`tidb_allow_batch_cop`](/system-variables.md#tidb_allow_batch_cop-从-v40-版本开始引入) 变量用来设置从 TiFlash 读取时，是否把 Region 的请求进行合并。当查询中涉及的 Region 数量比较大，可以尝试设置该变量为 `1`（对带 `aggregation` 下推到 TiFlash Coprocessor 的请求生效），或设置该变量为 `2`（对全部下推到 TiFlash Coprocessor 请求生效）。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_allow_batch_cop = 1;
    ```

3. 尝试开启聚合推过 `Join` / `Union` 等 TiDB 算子的优化：

    [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down) 变量用来设置优化器是否执行聚合函数下推到 Join 之前的优化操作。当查询中聚合操作执行很慢时，可以尝试设置该变量为 1。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_opt_agg_push_down = 1;
    ```

4. 尝试开启 `Distinct` 推过 `Join` / `Union` 等 TiDB 算子的优化：

    [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down) 变量用来设置优化器是否执行带有 `Distinct` 的聚合函数（比如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作。当查询中带有 `Distinct` 的聚合操作执行很慢时，可以尝试设置该变量为 `1`。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_opt_distinct_agg_push_down = 1;
    ```

5. 如果 `Join` 算子没有选择 MPP 执行模式，你可以调整 `tidb_opt_network_factor` 变量值使 `Join` 算子选择 MPP 执行模式：

    `tidb_opt_network_factor` 变量用来设置优化器计算代价时考虑网络开销的比例。该变量值越小，TiDB 对于大量网络传输的开销估算就越小，从而更倾向于选择 MPP 算子。

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_opt_network_factor = 0.001;
    ```

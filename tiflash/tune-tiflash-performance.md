---
title: TiFlash 性能调优
aliases: ['/docs-cn/v3.1/tiflash/tune-tiflash-performance/','/docs-cn/v3.1/reference/tiflash/tune-performance/']
---

# TiFlash 性能调优

本文介绍了使 TiFlash 性能达到最优的几种方式，包括规划机器资源、TiDB 参数调优、配置 TiKV Region 大小等。

## 资源规划

对于希望节省机器资源，并且完全没有隔离要求的场景，可以使用 TiKV 和 TiFlash 联合部署。建议为 TiKV 与 TiFlash 分别留够资源，并且不要共享磁盘。

## TiDB 相关参数调优

1. 对于 OLAP/TiFlash 专属的 TiDB 节点，建议调大读取并发数 [`tidb_distsql_scan_concurrency`](/tidb-specific-system-variables.md#tidb_distsql_scan_concurrency) 到 80：

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_distsql_scan_concurrency = 80;
    ```

2. 开启聚合推过 JOIN / UNION 等 TiDB 算子的优化：

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_opt_agg_push_down = 1;
    ```

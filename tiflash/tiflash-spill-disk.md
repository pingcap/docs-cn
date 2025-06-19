---
title: TiFlash 数据落盘
summary: 了解 TiFlash 如何将数据落盘以及如何自定义落盘行为。
---

# TiFlash 数据落盘

本文介绍 TiFlash 在计算过程中如何将数据落盘。

从 v7.0.0 开始，TiFlash 支持将中间数据落盘以缓解内存压力。支持以下算子：

* 具有等值连接条件的 Hash Join 算子
* 具有 `GROUP BY` 键的 Hash Aggregation 算子
* TopN 算子和 Window 函数中的 Sort 算子

## 触发落盘

TiFlash 提供了两种触发数据落盘的机制。

* 算子级别落盘：通过为每个算子指定数据落盘阈值，你可以控制 TiFlash 何时将该算子的数据落盘。
* 查询级别落盘：通过指定 TiFlash 节点上查询的最大内存使用量和落盘的内存比例，你可以控制 TiFlash 何时根据需要将查询中支持的算子数据落盘。

### 算子级别落盘

从 v7.0.0 开始，TiFlash 支持算子级别的自动落盘。你可以使用以下系统变量控制每个算子的数据落盘阈值。当算子的内存使用超过阈值时，TiFlash 会触发该算子的落盘。

* [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700)
* [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)
* [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700)

#### 示例

本示例构造一个消耗大量内存的 SQL 语句来演示 Hash Aggregation 算子的落盘。

1. 准备环境。创建一个包含 2 个节点的 TiFlash 集群并导入 TPCH-100 数据。
2. 执行以下语句。这些语句不限制具有 `GROUP BY` 键的 Hash Aggregation 算子的内存使用。

    ```sql
    SET tidb_max_bytes_before_tiflash_external_group_by = 0;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

3. 从 TiFlash 的日志中可以看到，该查询在单个 TiFlash 节点上需要消耗 29.55 GiB 的内存：

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 29.55 GiB."] [source=MemoryTracker] [thread_id=468]
    ```

4. 执行以下语句。此语句将具有 `GROUP BY` 键的 Hash Aggregation 算子的内存使用限制为 10737418240（10 GiB）。

    ```sql
    SET tidb_max_bytes_before_tiflash_external_group_by = 10737418240;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

5. 从 TiFlash 的日志中可以看到，通过配置 `tidb_max_bytes_before_tiflash_external_group_by`，TiFlash 触发了中间结果的落盘，显著降低了查询使用的内存。

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 12.80 GiB."] [source=MemoryTracker] [thread_id=110]
    ```

### 查询级别落盘

从 v7.4.0 开始，TiFlash 支持查询级别的自动落盘。你可以使用以下系统变量控制此功能：

* [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)：限制 TiFlash 节点上单个查询的最大内存使用量。
* [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)：控制触发数据落盘的内存比例。

如果 `tiflash_mem_quota_query_per_node` 和 `tiflash_query_spill_ratio` 都设置为大于 0 的值，当查询的内存使用超过 `tiflash_mem_quota_query_per_node * tiflash_query_spill_ratio` 时，TiFlash 会自动触发查询中支持的算子的落盘。

#### 示例

本示例构造一个消耗大量内存的 SQL 语句来演示查询级别的落盘。

1. 准备环境。创建一个包含 2 个节点的 TiFlash 集群并导入 TPCH-100 数据。

2. 执行以下语句。这些语句不限制查询的内存使用或具有 `GROUP BY` 键的 Hash Aggregation 算子的内存使用。

    ```sql
    SET tidb_max_bytes_before_tiflash_external_group_by = 0;
    SET tiflash_mem_quota_query_per_node = 0;
    SET tiflash_query_spill_ratio = 0;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

3. 从 TiFlash 的日志中可以看到，该查询在单个 TiFlash 节点上消耗了 29.55 GiB 的内存：

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 29.55 GiB."] [source=MemoryTracker] [thread_id=468]
    ```

4. 执行以下语句。这些语句将 TiFlash 节点上查询的最大内存使用量限制为 5 GiB。

    ```sql
    SET tiflash_mem_quota_query_per_node = 5368709120;
    SET tiflash_query_spill_ratio = 0.7;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

5. 从 TiFlash 的日志中可以看到，通过配置查询级别落盘，TiFlash 触发了中间结果的落盘，显著降低了查询使用的内存。

    ```
    [DEBUG] [MemoryTracker.cpp:101] ["Peak memory usage (for query): 3.94 GiB."] [source=MemoryTracker] [thread_id=1547]
    ```

## 注意事项

* 当 Hash Aggregation 算子没有 `GROUP BY` 键时，不支持落盘。即使 Hash Aggregation 算子包含 distinct 聚合函数，也不支持落盘。
* 目前，算子级别落盘的阈值是针对每个算子单独计算的。对于包含两个 Hash Aggregation 算子的查询，如果未配置查询级别落盘，且聚合算子的阈值设置为 10 GiB，则两个 Hash Aggregation 算子只有在各自的内存使用超过 10 GiB 时才会落盘。
* 目前，Hash Aggregation 算子和 TopN/Sort 算子在恢复阶段使用归并聚合和归并排序算法。因此，这两个算子只触发一轮落盘。如果内存需求非常高，且恢复阶段的内存使用仍然超过阈值，则不会再次触发落盘。
* 目前，Hash Join 算子使用基于分区的落盘策略。如果恢复阶段的内存使用仍然超过阈值，则会再次触发落盘。但是，为了控制落盘的规模，落盘轮数限制为三轮。如果在第三轮落盘后恢复阶段的内存使用仍然超过阈值，则不会再次触发落盘。
* 当配置了查询级别落盘（即 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) 和 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740) 都大于 0）时，TiFlash 会忽略单个算子的落盘阈值，并根据查询级别落盘阈值自动触发查询中相关算子的落盘。
* 即使配置了查询级别落盘，如果查询中使用的算子都不支持落盘，该查询的中间计算结果仍然无法落盘。在这种情况下，当该查询的内存使用超过相关阈值时，TiFlash 会返回错误并终止查询。
* 即使配置了查询级别落盘且查询包含支持落盘的算子，在以下任一情况下，查询仍可能因超过内存阈值而返回错误：
    - 查询中其他不支持落盘的算子消耗了太多内存。
    - 支持落盘的算子未及时落盘。

  要解决支持落盘的算子未及时落盘的情况，你可以尝试降低 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740) 以避免内存阈值错误。

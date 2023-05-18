---
title: TiFlash 数据落盘
summary: 介绍 TiFlash 数据落盘功能。
---

# TiFlash 数据落盘

本文介绍 TiFlash 计算过程中的数据落盘功能。

从 v7.0.0 起，TiFlash 支持在计算过程中将中间数据落盘以缓解内存压力。目前支持落盘的算子有：

* 带有等值关联条件的 Hash Join 算子
* 带有 `GROUP BY` key 的 Hash Aggregation 算子
* TopN 算子以及窗口函数中的 Sort 算子

## TiFlash 数据落盘的触发机制

TiDB 提供了以下系统变量，来控制各算子数据落盘的阈值。当算子使用的内存超过阈值之后，TiFlash 会触发对应算子的落盘。

* [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-从-v700-版本开始引入)
* [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-从-v700-版本开始引入)
* [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-从-v700-版本开始引入)

## 示例

本示例构造一个占用大量内存的 SQL 语句来对 Hash Aggregation 的落盘功能进行演示：

1. 准备数据。创建一个包含 2 个节点的 TiFlash 集群，并导入 TPCH-100 的数据。
2. 执行以下语句。该语句不限制带 `GROUP BY` 的 Hash Aggregation 算子的内存使用量。

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

3. 从 TiFlash 的日志中可以看到，该查询在单个 TiFlash 节点上需要消耗 29.55 GiB 内存：

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 29.55 GiB."] [source=MemoryTracker] [thread_id=468]
    ```

4. 执行以下语句。该语句限制了带 `GROUP BY` 的 Hash Aggregation 算子的内存使用量，不超过 10737418240 (10 GiB)。

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

5. 从 TiFlash 的日志中可以看出，通过配置 `tidb_max_bytes_before_tiflash_external_group_by`，TiFlash 触发了中间结果落盘，显著减小了查询所需的内存。

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 12.80 GiB."] [source=MemoryTracker] [thread_id=110]
    ```

## 注意

* 当 Hash Aggregation 算子不带 `GROUP BY` key 时，不支持落盘。即使该 Hash Aggregation 中含有 `DISTINCT` 聚合函数，也不能触发落盘。
* 目前阈值是针对单个算子来计算的。如果一个查询里有两个 Hash Aggregation 算子，并且阈值设置为 10 GiB，那么两个 Hash Aggregation 算子仅会在各自占用的内存超过 10 GiB 时才会触发数据落盘。
* 目前 Hash Aggregation 与 TopN/Sort 在 restore 阶段采用的是 merge aggregation 和 merge sort 的算法，所以这两个算子只会触发一次数据落盘。如果需要的内存特别大以至于在 restore 阶段内存使用仍然超阈值，不会再次触发落盘。
* 目前 Hash Join 采用基于分区的落盘策略，在 restore 阶段如果内存使用仍然超过阈值，会继续触发落盘。但是为了控制落盘的规模，落盘的轮数限制为三轮。如果第三轮落盘之后的 restore 阶段内存使用仍然超过阈值，则不会触发新的落盘。

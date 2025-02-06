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

TiFlash 数据落盘的触发机制有两种：

* 算子级别的落盘，即通过指定各个算子的数据落盘阈值，来触发 TiFlash 将对应算子的数据进行落盘。
* 查询级别的落盘，即通过指定单个查询在单个 TiFlash 节点的最大内存使用量以及落盘的阈值，来触发 TiFlash 将查询中支持落盘的算子的数据按需进行落盘。

### 算子级别的落盘

从 v7.0.0 起，TiFlash 支持算子级别的自动落盘。你可通过以下系统变量，来控制各算子数据落盘的阈值。当算子使用的内存超过阈值之后，TiFlash 会触发对应算子的落盘。

* [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-从-v700-版本开始引入)
* [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-从-v700-版本开始引入)
* [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-从-v700-版本开始引入)

#### 示例

本示例构造一个占用大量内存的 SQL 语句来对 Hash Aggregation 算子的落盘功能进行演示：

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

### 查询级别的落盘

从 v7.4.0 开始，TiFlash 支持查询级别的自动落盘机制。你可以通过以下系统变量，来控制查询级别的自动落盘：

* [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-从-v740-版本开始引入)：用于控制单个查询在单个 TiFlash 节点内存使用的上限
* [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-从-v740-版本开始引入)：用于控制触发数据落盘的内存阈值

当 `tiflash_mem_quota_query_per_node` 与 `tiflash_query_spill_ratio` 均设置为一个大于 0 的值时，TiFlash 会在一个查询的内存使用量超过 `tiflash_mem_quota_query_per_node * tiflash_query_spill_ratio` 时自动触发该查询中可以支持落盘的算子的落盘。

#### 示例

本示例构造一个占用大量内存的 SQL 语句来对查询级别的落盘功能进行演示：

1. 准备数据。创建一个包含 2 个节点的 TiFlash 集群，并导入 TPCH-100 的数据。

2. 执行以下语句。该查询未限制查询级别的内存使用量，也未限制带 `GROUP BY` 的 Hash Aggregation 算子的内存使用量。

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

3. 从 TiFlash 的日志中可以看到，该查询在单个 TiFlash 节点上需要消耗 29.55 GiB 内存：

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 29.55 GiB."] [source=MemoryTracker] [thread_id=468]
    ```

4. 执行以下语句。该语句限制了单个查询在单个 TiFlash 节点的最大内存使用量为 5 GiB。

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

5. 从 TiFlash 的日志中可以看出，通过配置查询级别的自动落盘，TiFlash 触发了中间结果落盘，显著减小了查询所需的内存。

    ```
    [DEBUG] [MemoryTracker.cpp:101] ["Peak memory usage (for query): 3.94 GiB."] [source=MemoryTracker] [thread_id=1547]
    ```

## 注意

* 当 Hash Aggregation 算子不带 `GROUP BY` key 时，不支持落盘。即使该 Hash Aggregation 中含有 `DISTINCT` 聚合函数，也不能触发落盘。
* 目前算子级别落盘的阈值是针对单个算子来计算的。当未配置查询级别的数据落盘时，如果一个查询里有两个 Hash Aggregation 算子，并且算子的阈值设置为 10 GiB，那么两个 Hash Aggregation 算子仅会在各自占用的内存超过 10 GiB 时才会触发数据落盘。
* 目前 Hash Aggregation 与 TopN/Sort 在 restore 阶段采用的是 merge aggregation 和 merge sort 的算法，所以这两个算子只会触发一次数据落盘。如果需要的内存特别大以至于在 restore 阶段内存使用仍然超阈值，不会再次触发落盘。
* 目前 Hash Join 采用基于分区的落盘策略，在 restore 阶段如果内存使用仍然超过阈值，会继续触发落盘。但是为了控制落盘的规模，落盘的轮数限制为三轮。如果第三轮落盘之后的 restore 阶段内存使用仍然超过阈值，则不会触发新的落盘。
* 当配置了查询级别的落盘机制（即 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-从-v740-版本开始引入) 和 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-从-v740-版本开始引入) 均大于 0）时，TiFlash 单个算子的落盘阈值会被忽略，TiFlash 会根据查询级别的落盘阈值来自动触发该查询中相关算子的落盘。
* 即使配置了查询级别的落盘，如果该查询中用到的算子均不支持落盘，该查询的中间计算结果仍然无法落盘。此时，如果查询的内存使用超过了相关阈值，TiFlash 会报错并终止查询。
* 即使配置了查询级别的落盘，且查询中也含有支持落盘的算子，但是如果查询中其他不能落盘的算子占用了过多的内存或者支持落盘的算子落盘不及时，查询仍然有可能因为内存超过阈值而报错。对于落盘算子落盘不及时的情况，可以尝试调小 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-从-v740-版本开始引入) 来避免查询内存超阈值报错。

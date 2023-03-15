---
title: TiFlash 数据落盘
summary: 介绍 TiFlash 数据落盘功能。
---

# TiFlash 数据落盘

本文介绍 TiFlash 计算过程中的数据落盘功能。

从 v7.0.0 起，TiFlash 支持计算过程中将中间数据落盘以缓解内存压力。目前支持落盘的算子有

* 带有等值关联条件的 Hash Join
* 带有 group by key 的 Hash Aggregation
* TopN 算子以及 Window function 中的 Sort 算子

> **注意：**
>
> 当 Hash Aggregation 不带 group by key 时不支持落盘，即使该 Hash Aggregation 中含有 distinct 聚合函数也不能落盘。


## TiFlash 数据落盘的触发机制

目前 TiFlash 支持落盘的算子都有相应的配置来控制落盘的阈值
* max_bytes_before_external_join: 控制 Hash Join 算子是否落盘的阈值，设置为 0 则不落盘，否则当 Hash Join 内存使用超过该阈值时会触发数据落盘
* max_bytes_before_external_group_by: 控制 Hash Aggregation 算子是否落盘的阈值，设置为 0 则不落盘，否则当 Hash Aggregation 内存使用超过该阈值时会触发数据落盘
* max_bytes_before_external_sort: 控制 TopN 以及 Sort 算子是否落盘的阈值，设置为 0 则不落盘，否则当 TopN 或者 Sort 内存使用超过该阈值时会触发数据落盘

## 示例
本示例构造一个占用大量内存的 SQL 语句来对 Hash Aggregation 的落盘功能进行演示：
1. 准备数据：建立一个 2 节点的 TiFlash 集群并导入 TPCH-100 的数据
2. 通过 [tiup cluster edit-config](/tiup/tiup-component-cluster-edit-config.md) 将集群中 TiFlash 的 max_bytes_before_external_group_by 配置为 0
3. 执行以下语句
```sql
select l_orderkey, max(L_COMMENT), max(L_SHIPMODE), max(L_SHIPINSTRUCT), max(L_SHIPDATE), max(L_EXTENDEDPRICE) from lineitem group by l_orderkey having sum(l_quantity) > 314
```
4. 从 TiFlash 的 log 中可以看到
```
[DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 29.55 GiB."] [source=MemoryTracker] [thread_id=468]
```
说明该 query 在单个 TiFlash 节点上需要消耗 29 G 内存
5. 通过 [tiup cluster edit-config](/tiup/tiup-component-cluster-edit-config.md) 将集群中 TiFlash 的 max_bytes_before_external_group_by 配置为 10737418240 (10 G)，继续运行上述 query，从 TiFlash 的 log 里面可以看到
```
[DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 12.80 GiB."] [source=MemoryTracker] [thread_id=110]
```

可以看到通过配置 `max_bytes_before_external_group_by`, TiFlash 触发了中间结果落盘，显著减小了 query 所需要的内存。

## 注意
* 目前阈值只是针对单个算子来说的，如果一个 query 里面有两个 Hash Aggregation，而阈值设成 10 G 时，两个 Hash Aggregation 仅会在自己占用的内存超过 10 G 的时候才会触发数据落盘
* 目前 Hash Aggregation 与 TopN/Sort 在 restore 阶段采用的是 merge aggregation 和 merge sort 的算法，所以这两个算子只会触发一次数据落盘，如果需要的内存特别大以至于在 restore 阶段内存使用仍然超阈值，不会再次触发落盘
* 目前 Hash Join 采用基于分区的落盘策略，在 restore 阶段如果内存使用仍然超过阈值的话，会继续触发落盘，但是为了控制落盘的规模，落盘的轮数限定在了 3 轮，如果第三轮落盘之后的 restore 阶段内存使用仍然超过了阈值，则不会触发新的落盘

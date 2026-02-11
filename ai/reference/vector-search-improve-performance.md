---
title: 提升向量搜索性能
summary: 学习提升 TiDB 向量搜索性能的最佳实践。
aliases: ['/zh/tidb/stable/vector-search-improve-performance/','/zh/tidb/dev/vector-search-improve-performance/','/zh/tidbcloud/vector-search-improve-performance/']
---

# 提升向量搜索性能

TiDB 向量搜索支持执行近似最近邻（ANN）查询，用于查找与某个镜像、文档或其他输入相似的结果。要提升查询性能，请参考以下最佳实践。

> **注意：**
>
> - 向量搜索功能目前为 beta 版本，可能会在未提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

## 为向量列添加向量搜索索引

[向量搜索索引](/ai/reference/vector-search-index.md) 能显著提升向量搜索查询的性能，通常可提升 10 倍或以上，仅以极小的召回率下降为代价。

## 确保向量索引已完全构建

在你插入大量向量数据后，部分数据可能仍处于 Delta 层，等待持久化。TiDB 会在数据持久化后为这些数据构建向量索引。在所有向量数据都被索引之前，向量搜索性能会处于次优状态。要查看索引构建进度，请参见 [查看索引构建进度](/ai/reference/vector-search-index.md#view-index-build-progress)。

## 降低向量维度或缩短 embedding

随着向量维度的增加，向量搜索索引和查询的计算复杂度会显著提升，需要进行更多的浮点数比较。

为优化性能，建议在可行的情况下降低向量维度。这通常需要切换到其他 embedding 模型。切换模型时，你需要评估模型变更对向量查询准确性的影响。

某些 embedding 模型（如 OpenAI 的 `text-embedding-3-large`）支持[缩短 embedding](https://openai.com/index/new-embedding-models-and-api-updates/)，即在不丢失 embedding 概念表达能力的前提下，从向量序列末尾移除部分数值。你也可以使用此类 embedding 模型来降低向量维度。

## 从结果中排除向量列

向量 embedding 数据通常较大，仅在搜索过程中使用。通过在查询结果中排除向量列，可以大幅减少 TiDB 服务器与 SQL 客户端之间传输的数据量，从而提升查询性能。

要排除向量列，请在 `SELECT` 子句中显式列出你需要获取的列，而不是使用 `SELECT *` 获取所有列。

## 预热索引

当访问从未被使用过或长时间未被访问（冷访问）的索引时，TiDB 需要从云存储或磁盘（而非内存）加载整个索引。此过程需要一定时间，通常会导致更高的查询延时。此外，如果长时间（如数小时）没有 SQL 查询，计算资源会被回收，导致后续访问变为冷访问。

为避免此类查询延时，在实际负载前，可以通过执行命中向量索引的类似向量搜索查询来预热索引。
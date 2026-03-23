---
title: 向量搜索限制
summary: 了解 TiDB 向量搜索的限制。
aliases: ['/zh/tidb/stable/vector-search-limitations/','/zh/tidb/dev/vector-search-limitations/','/zh/tidbcloud/vector-search-limitations/']
---

# 向量搜索限制

本文档描述了 TiDB 向量搜索已知的限制。

> **注意：**
>
> - 向量搜索功能目前为 beta 版本，可能会在没有提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本必须为 v8.4.0 或以上版本（推荐使用 v8.5.0 或以上版本）。

## 向量数据类型限制

- 每个 [vector](/ai/reference/vector-search-data-types.md) 最多支持 16383 维。
- 向量数据类型无法存储 `NaN`、`Infinity` 或 `-Infinity` 值。
- 向量数据类型无法存储双精度浮点数。如果你在向量列中插入或存储双精度浮点数，TiDB 会将其转换为单精度浮点数。
- 向量列不能作为主键或主键的一部分。
- 向量列不能作为唯一索引或唯一索引的一部分。
- 向量列不能作为分区键或分区键的一部分。
- 目前，TiDB 不支持将向量列修改为其他数据类型（如 `JSON` 和 `VARCHAR`）。

## 向量索引限制

参见 [向量搜索限制](/ai/reference/vector-search-index.md#restrictions)。

## 与 TiDB 工具的兼容性

在使用向量搜索时，请注意以下兼容性问题：

- TiDB Cloud 功能：

    - [TiDB Cloud 控制台的数据迁移功能](https://docs.pingcap.com/zh/tidbcloud/migrate-from-mysql-using-data-migration/) 不支持将 MySQL 向量数据类型迁移或同步到 TiDB Cloud。

- TiDB 工具：

    - 请确保你使用的是 v8.4.0 或以上版本的 [BR](/br/backup-and-restore-overview.md) 进行数据备份和恢复。不支持将包含向量数据类型的表恢复到低于 v8.4.0 的 TiDB 集群。
    - [TiDB Data Migration (DM)](/dm/dm-overview.md) 不支持将 MySQL 向量数据类型迁移或同步到 TiDB。
    - 当 [TiCDC](/ticdc/ticdc-overview.md) 将向量数据同步到不支持向量数据类型的下游时，会将向量数据类型转换为其他类型。更多信息，参见 [与向量数据类型的兼容性](/ticdc/ticdc-compatibility.md#compatibility-with-vector-data-types)。

## 反馈

我们非常重视你的反馈，并随时为你提供帮助：

- 在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问
- [提交 TiDB Cloud 工单](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [提交 TiDB 工单](/support.md)

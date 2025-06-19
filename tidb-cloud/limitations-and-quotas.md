---
title: TiDB Cloud Dedicated 限制和配额
summary: 了解 TiDB Cloud 中的限制和配额。
---

# TiDB Cloud Dedicated 限制和配额

TiDB Cloud 限制了你在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中可以创建的每种组件的数量，以及 TiDB 的常见使用限制。此外，还有一些组织级别的配额来限制用户创建的资源数量，以防创建超出实际需要的资源。这些表格概述了限制和配额。

> **注意：**
>
> 如果这些限制或配额中的任何一个对你的组织造成问题，请联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)。

## 集群限制

| 组件 | 限制 |
|:-|:-|
| 每个[数据 region](/tidb-cloud/tidb-cloud-glossary.md#region) 的副本数量 | 3 |
| 跨可用区部署的可用区数量 | 3 |

> **注意：**
>
> 如果你想了解更多关于 TiDB 的常见使用限制，请参考 [TiDB 限制](https://docs.pingcap.com/tidb/stable/tidb-limitations)。

## 集群配额

| 组件 | 配额（默认） |
|:-|:-|
| 组织中所有集群的 TiDB 节点总数上限 | 10 |
| 组织中所有集群的 TiKV 节点总数上限 | 15 |
| 组织中所有集群的 TiFlash 节点总数上限 | 5 |

> **注意：**
>
> 如果这些限制或配额中的任何一个对你的组织造成问题，请联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)。

---
title: 在 Kubernetes 上部署 TiDB
summary: 了解如何在 Kubernetes 上部署 TiDB
---

# 在 Kubernetes 上部署 TiDB

你可以使用 [TiDB Operator](https://github.com/pingcap/tidb-operator) 在 Kubernetes 上部署 TiDB。TiDB Operator 是 Kubernetes 上的 TiDB 集群自动运维系统，提供包括部署、升级、扩缩容、备份恢复、配置变更的 TiDB 全生命周期管理。借助 TiDB Operator，TiDB 可以无缝运行在公有云或私有部署的 Kubernetes 集群上。

TiDB Operator 与适用的 TiDB 版本的对应关系如下。如无特殊需求，建议使用 TiDB Operator 的最新稳定版本 v1.2。

| TiDB Operator 版本 | 适用的 TiDB 版本 |
|:---|:---|
| v1.0 | v2.1, v3.0 |
| v1.1 | v3.0, v3.1, v4.0, v5.0 |
| v1.2 | v3.0 及以上版本 |
| dev | v3.0 及以上版本，dev |

TiDB Operator 的文档目前独立于 TiDB 文档。要访问 TiDB Operator 的文档，请点击以下链接：

- [TiDB Operator v1.0 文档](https://docs.pingcap.com/zh/tidb-data-migration/v1.0/)
- [TiDB Operator v1.1 文档](https://docs.pingcap.com/zh/tidb-data-migration/v2.0/)
- [TiDB Operator v1.2 文档](https://docs.pingcap.com/zh/tidb-data-migration/stable)
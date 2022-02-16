---
title: TiDB Operator
summary: 了解 Kubernetes 上的 TiDB 集群自动部署运维工具 TiDB Operator。
---

# TiDB Operator

[TiDB Operator](https://github.com/pingcap/tidb-operator) 是 Kubernetes 上的 TiDB 集群自动运维系统，提供包括部署、升级、扩缩容、备份恢复、配置变更的 TiDB 全生命周期管理。借助 TiDB Operator，TiDB 可以无缝运行在公有云或私有部署的 Kubernetes 集群上。

对于当前 TiDB 版本，TiDB Operator 的推荐稳定版本为 v1.3。TiDB Operator 与适用的 TiDB 版本的对应关系如下：

| TiDB 版本 | 适用的 TiDB Operator 版本 |
|:---|:---|
| TiDB >= v3.0 | dev |
| TiDB >= v3.0 | **v1.3（推荐）**|
| v3.0 <= TiDB < v5.4.0 | v1.2 |
| v3.0 <= TiDB < v5.1.0 | v1.1 |
| v2.1 <= TiDB < v3.1 | v1.0（停止维护）|

TiDB Operator 的文档目前独立于 TiDB 文档，文档名称为 **TiDB in Kubernetes 用户文档**。要访问 TiDB Operator 的文档，请点击以下链接：

- [TiDB in Kubernetes 用户文档](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/)

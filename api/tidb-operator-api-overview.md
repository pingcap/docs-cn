---
title: TiDB Operator API 概览
summary: 了解 TiDB Operator 的 API 接口。
---

# TiDB Operator API 概览

[TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/) 是 Kubernetes 上的 TiDB 集群自动运维系统，提供包括部署、升级、扩缩容、备份恢复、配置变更的 TiDB 全生命周期管理。借助 TiDB Operator，TiDB 可以无缝运行在公有云或自托管的 Kubernetes 集群上。

要在 Kubernetes 上管理 TiDB 集群，你可以使用以下 TiDB Operator API：

- [Backup](https://github.com/pingcap/tidb-operator/blob/{{{.tidb-operator-version}}}/docs/api-references/docs.md#backup)
- [BackupSchedule](https://github.com/pingcap/tidb-operator/blob/{{{.tidb-operator-version}}}/docs/api-references/docs.md#backupschedule)
- [DMCluster](https://github.com/pingcap/tidb-operator/blob/{{{.tidb-operator-version}}}/docs/api-references/docs.md#dmcluster)
- [Restore](https://github.com/pingcap/tidb-operator/blob/{{{.tidb-operator-version}}}/docs/api-references/docs.md#restore)
- [TidbCluster](https://github.com/pingcap/tidb-operator/blob/{{{.tidb-operator-version}}}/docs/api-references/docs.md#tidbcluster)
- [TidbInitializer](https://github.com/pingcap/tidb-operator/blob/{{{.tidb-operator-version}}}/docs/api-references/docs.md#tidbinitializer)
- [TidbMonitor](https://github.com/pingcap/tidb-operator/blob/{{{.tidb-operator-version}}}/docs/api-references/docs.md#tidbmonitor)

更多信息，请参阅 [TiDB Operator API 文档](https://github.com/pingcap/tidb-operator/blob/{{{.tidb-operator-version}}}/docs/api-references/docs.md)。

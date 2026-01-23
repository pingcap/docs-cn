---
title: TiDB API 概览
summary: 了解 TiDB Cloud 与 TiDB 的 API。
aliases: ['/tidbcloud/api-overview/']
---

# TiDB API 概览

TiDB 提供了多种 API，可用于集群的查询与运维、数据的同步管理、系统的状态监控等多种场景。本文为 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/) 和 [TiDB](https://docs.pingcap.com/tidb/stable/) 中可用的 API 提供了一个概览说明。

## TiDB Cloud API（beta）

[TiDB Cloud API](/api/tidb-cloud-api-overview.md) 是一个 [REST 接口](https://zh.wikipedia.org/wiki/表现层状态转换)。通过该API，你可以以编程方式访问和操作 TiDB Cloud 中的各类管理资源，例如项目、集群、备份、恢复、导入、账单以及 Data Service。

| API | 说明 |
| --- | --- |
| [v1beta1](/api/tidb-cloud-api-v1beta1.md) | 管理 TiDB Cloud Starter、Essential 与 Dedicated 集群，以及计费、Data Service 与 IAM 资源。 |
| [v1beta](/api/tidb-cloud-api-v1beta.md) | 管理 TiDB Cloud 的项目、集群、备份、导入与恢复。 |

## TiDB API

TiDB 为相关 TiDB 工具提供了多种 API。通过这些 API，你可以管理集群组件、监控系统状态，并控制数据同步工作流。

| API | 说明 |
| --- | --- |
| [TiProxy API](/tiproxy/tiproxy-api.md) | 获取 TiProxy 配置、健康状况以及监控数据。 |
| [Data Migration API](/dm/dm-open-api.md) | 管理 DM-master 与 DM-worker 节点、数据源以及数据同步任务。 |
| [Monitoring API](/tidb-monitoring-api.md) | 获取 TiDB 服务器运行状态、数据表的存储信息以及 TiKV 集群的详细信息。 |
| [TiCDC API](/ticdc/ticdc-open-api-v2.md) | 查询 TiCDC 节点状态并管理数据同步任务，包括任务的创建、暂停、恢复与更新等操作。 |
| [TiDB Operator API](<https://github.com/pingcap/tidb-operator/blob/{{{ .tidb-operator-version }}}/docs/api-references/docs.md>) | 管理 Kubernetes 上的 TiDB 集群，包括集群部署、升级、扩缩容、备份与故障切换等操作。 |

---
title: TiDB API Overview
summary: Learn about the APIs available for TiDB Cloud and TiDB Self-Managed.
aliases: ['/tidbcloud/api-overview/']
---

# TiDB API Overview

TiDB provides various APIs for querying and operating clusters, managing data replication, monitoring system status, and more. This document provides an overview of the available APIs for both [TiDB Cloud](https://docs.pingcap.com/tidbcloud/) and [TiDB Self-Managed](https://docs.pingcap.com/tidb/stable/).

## TiDB Cloud API (beta)

[TiDB Cloud API](/api/tidb-cloud-api-overview.md) is a REST interface that provides you with programmatic access to manage administrative objects within TiDB Cloud, such as projects, clusters, backups, restores, imports, billings, and Data Service resources.

| API | Description |
| --- | --- |
| [v1beta1](/api/tidb-cloud-api-v1beta1.md) | Manage TiDB Cloud Starter, Essential, and Dedicated clusters, as well as billing, Data Service, and IAM resources. |
| [v1beta](/api/tidb-cloud-api-v1beta.md) | Manage projects, clusters, backups, imports, and restores for TiDB Cloud. |

## TiDB Self-Managed API

TiDB Self-Managed provides various APIs for TiDB tools to help you manage cluster components, monitor system status, and control data replication workflows without relying solely on command-line tools.

| API | Description |
| --- | --- |
| [TiProxy API](/tiproxy/tiproxy-api.md) | Access TiProxy configuration, health status, and monitoring data. |
| [Data Migration API](/dm/dm-open-api.md) | Manage DM-master and DM-worker nodes, data sources, and data replication tasks. |
| [Monitoring API](/tidb-monitoring-api.md) | Get TiDB server running status, table storage information, and PD cluster details. |
| [TiCDC API](/ticdc/ticdc-open-api-v2.md) | Query TiCDC node status and manage replication tasks, including creating, pausing, resuming, and updating operations. |
| [TiDB Operator API](<https://github.com/pingcap/tidb-operator/blob/{{{ .tidb-operator-version }}}/docs/api-references/docs.md>) | Manage TiDB clusters on Kubernetes, including deployment, upgrades, scaling, backup, and failover. |

---
title: TiDB Cloud API v1beta1 概览
summary: 了解 TiDB Cloud 的 v1beta1 API。
---

# TiDB Cloud API v1beta1 概览

TiDB Cloud API v1beta1 是一个 RESTful API，提供了以编程方式访问和操作 TiDB Cloud 中的各类管理资源的能力。通过该 API，你可以自动且高效地管理集群级的资源（如集群与分支），以及组织或项目级的资源（如计费、Data Service 与 IAM）。

目前，你可以使用以下 v1beta1 API 来管理 TiDB Cloud 中的资源：

- 集群级资源：
    - [TiDB Cloud Starter 或 Essential 集群](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless)：管理 TiDB Cloud Starter 或 Essential 的集群、分支、数据导出任务与数据导入任务。
    - [TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated)：管理 TiDB Cloud Dedicated 的集群、区域 (region)、Private Endpoint 连接以及数据导入任务。
- 组织或项目级资源：
    - [Billing](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing)：管理 TiDB Cloud 集群的账单。
    - [Data Service](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)：管理 TiDB Cloud 集群 Data Service 中的资源。
    - [IAM](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam)：管理 TiDB Cloud 集群的 API key。
    - [MSP（已弃用）](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)
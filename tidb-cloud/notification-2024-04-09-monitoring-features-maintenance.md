---
title: 2024-04-09 TiDB Cloud 监控功能维护通知
summary: 了解 2024 年 4 月 9 日 TiDB Cloud 监控功能维护的详细信息，如维护时间窗口、原因和影响。
---

# [2024-04-09] TiDB Cloud 监控功能维护通知

本通知描述了你需要了解的关于 2024 年 4 月 9 日 TiDB Cloud [监控功能](/tidb-cloud/monitor-tidb-cluster.md)维护的详细信息。

## 维护时间窗口

- 开始时间：2024-04-09 08:00 (UTC+0)
- 结束时间：2024-04-09 12:00 (UTC+0)
- 持续时间：4 小时

## 影响

### 受影响的区域

在维护时间窗口期间，以下区域的监控功能将受到影响：

- TiDB Cloud Dedicated 集群：
    - 云服务提供商：AWS，区域：俄勒冈（us-west-2）
    - 云服务提供商：AWS，区域：首尔（ap-northeast-2）
    - 云服务提供商：AWS，区域：法兰克福（eu-central-1）
    - 云服务提供商：AWS，区域：俄勒冈（us-west-2）
    - 云服务提供商：Google Cloud，区域：俄勒冈（us-west1）
    - 云服务提供商：Google Cloud，区域：东京（asia-northeast1）
    - 云服务提供商：Google Cloud，区域：新加坡（asia-southeast1）
    - 云服务提供商：Google Cloud，区域：爱荷华（us-central1）
    - 云服务提供商：Google Cloud，区域：台湾（asia-east1）

- TiDB Cloud Serverless 集群：
    - 云服务提供商：AWS，区域：法兰克福（eu-central-1）
    - 云服务提供商：AWS，区域：俄勒冈（us-west-2）

### 受影响的监控功能

> **注意：**
>
> 维护仅影响 TiDB 集群中的监控功能。所有其他功能保持不受影响。你可以继续管理 TiDB 集群并照常执行读/写操作或其他操作。

- **指标**页面将在几个短时间段内暂时不可用（每次不超过 20 分钟）。
- **慢查询**页面将在几个短时间段内暂时不可用（每次不超过 5 分钟）。
- 与 Prometheus、DataDog 和 NewRelic 的指标集成可能会出现断点。

## 完成和恢复

一旦维护成功完成，受影响的功能将被恢复，为你提供更好的体验。

## 获取支持

如果你有任何问题或需要帮助，请联系我们的[支持团队](/tidb-cloud/tidb-cloud-support.md)。我们随时为你解答疑虑并提供必要的指导。

---
title: 2023-11-14 TiDB Cloud Dedicated 扩展功能维护通知
summary: 了解 2023 年 11 月 14 日 TiDB Cloud Dedicated 扩展功能维护的详细信息，如维护时间窗口和影响。
---

# [2023-11-14] TiDB Cloud Dedicated 扩展功能维护通知

本通知描述了你需要了解的 2023 年 11 月 14 日 TiDB Cloud Dedicated [扩展功能](https://docs.pingcap.com/tidbcloud/scale-tidb-cluster#scale-your-tidb-cluster)维护的详细信息。

## 维护时间窗口

- 开始时间：2023-11-14 16:00 (UTC+0)
- 结束时间：2023-11-21 16:00 (UTC+0)
- 持续时间：7 天

> **注意：**
>
> 2023-11-16 更新：维护时间窗口的结束时间已从 2023-11-16 延长至 2023-11-21。

## 影响

在维护时间窗口期间，[更改 vCPU 和内存](https://docs.pingcap.com/tidbcloud/scale-tidb-cluster#change-vcpu-and-ram)功能将被禁用，你无法更改 Dedicated 集群的 vCPU 和内存。但是，你仍然可以在修改集群页面中更改节点数量或存储。你的 TiDB 集群将保持正常的数据读写操作，确保不会对你的在线业务产生不利影响。

### 受影响的 TiDB Cloud 控制台 UI 功能

- 集群级别
    - 集群管理
        - 修改集群
            - 更改 TiDB、TiKV 或 TiFlash 节点的 vCPU 和内存。
 
### 受影响的 TiDB Cloud API 功能

- 集群管理
    - [UpdateCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)

## 完成和恢复

一旦维护成功完成，受影响的功能将恢复正常，为你提供更好的体验。

## 获取支持

如果你有任何问题或需要帮助，请联系我们的[支持团队](/tidb-cloud/tidb-cloud-support.md)。我们随时为你解答疑虑并提供必要的指导。

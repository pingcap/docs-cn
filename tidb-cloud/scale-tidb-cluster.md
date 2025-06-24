---
title: 扩缩容 TiDB 集群
summary: 了解如何扩缩容 TiDB Cloud 集群。
---

# 扩缩容 TiDB 集群

> **注意：**
>
> - [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 会根据应用程序的工作负载变化自动扩缩容。但是，您无法手动扩缩容 TiDB Cloud Serverless 集群。
> - 当集群处于**修改中**状态时，您无法对其执行任何新的扩缩容操作。

您可以在以下维度扩缩容 TiDB 集群：

- TiDB、TiKV 和 TiFlash 的节点数量
- TiDB、TiKV 和 TiFlash 的 vCPU 和内存
- TiKV 和 TiFlash 的存储空间

有关如何确定 TiDB 集群大小的信息，请参见[确定 TiDB 集群大小](/tidb-cloud/size-your-cluster.md)。

> **注意：**
>
> 如果 TiDB 或 TiKV 的 vCPU 和内存大小设置为 **4 vCPU，16 GiB**，请注意以下限制。要绕过这些限制，您可以先[增加 vCPU 和内存](#更改-vcpu-和内存)。
>
> - TiDB 的节点数量只能设置为 1 或 2，TiKV 的节点数量固定为 3。
> - 4 vCPU 的 TiDB 只能与 4 vCPU 的 TiKV 搭配使用，4 vCPU 的 TiKV 只能与 4 vCPU 的 TiDB 搭配使用。
> - TiFlash 不可用。

## 更改节点数量

您可以增加或减少 TiDB、TiKV 或 TiFlash 节点的数量。

> **警告：**
>
> 减少 TiKV 或 TiFlash 节点数量可能存在风险，这可能导致剩余节点的存储空间不足、CPU 使用率过高或内存使用率过高。

要更改 TiDB、TiKV 或 TiFlash 节点的数量，请执行以下步骤：

1. 在 TiDB Cloud 控制台中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。
2. 在要扩缩容的集群所在行，点击 **...**。

    > **提示：**
    >
    > 或者，您也可以在**集群**页面上点击要扩缩容的集群名称，然后点击右上角的 **...**。

3. 在下拉菜单中点击**修改**。此时会显示**修改集群**页面。
4. 在**修改集群**页面上，更改 TiDB、TiKV 或 TiFlash 节点的数量。
5. 在右侧窗格中查看集群大小，然后点击**确认**。

您也可以通过 [修改 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 端点使用 TiDB Cloud API 更改 TiDB、TiKV 或 TiFlash 节点的数量。目前，TiDB Cloud API 仍处于测试阶段。有关更多信息，请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta)。

## 更改 vCPU 和内存

您可以增加或减少 TiDB、TiKV 或 TiFlash 节点的 vCPU 和内存。

> **注意：**
>
> - 更改 vCPU 和内存仅适用于以下集群：
>     - 在 2022/12/31 之后创建的 AWS 托管集群。
>     - 在 2023/04/26 之后创建的 Google Cloud 托管集群。
>     - Azure 托管集群。
> - AWS 对 vCPU 和内存更改有冷却期限制。如果您的 TiDB 集群托管在 AWS 上，在更改 TiKV 或 TiFlash 的 vCPU 和内存后，必须等待至少六小时才能再次更改。
> - 在减少 vCPU 之前，请确保当前 TiKV 或 TiFlash 的节点存储空间不超过目标 vCPU 的最大节点存储空间。有关详细信息，请参见 [TiKV 节点存储空间](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)和 [TiFlash 节点存储空间](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。如果任何组件的当前存储空间超过其限制，您将无法减少 vCPU。

要更改 TiDB、TiKV 或 TiFlash 节点的 vCPU 和内存，请执行以下步骤：

1. 在 TiDB Cloud 控制台中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。
2. 在要扩缩容的集群所在行，点击 **...**。

    > **提示：**
    >
    > 或者，您也可以在**集群**页面上点击要扩缩容的集群名称，然后点击右上角的 **...**。

3. 在下拉菜单中点击**修改**。此时会显示**修改集群**页面。
4. 在**修改集群**页面上，更改 TiDB、TiKV 或 TiFlash 节点的 vCPU 和内存。
5. 在右侧窗格中查看集群大小，然后点击**确认**。

您也可以通过 [修改 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 端点使用 TiDB Cloud API 更改 TiDB、TiKV 或 TiFlash 节点的 vCPU 和内存。目前，TiDB Cloud API 仍处于测试阶段。有关更多信息，请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta)。

## 更改存储空间

您可以增加 TiKV 或 TiFlash 的存储空间。

> **警告：**
>
> - 对于正在运行的集群，AWS、Azure 和 Google Cloud 不允许原地降级存储容量。
> - AWS 和 Azure 对存储空间更改有冷却期限制。如果您的 TiDB 集群托管在 AWS 或 Azure 上，在更改 TiKV 或 TiFlash 的存储空间或 vCPU 和内存后，必须等待至少六小时才能再次更改。

要更改 TiKV 或 TiFlash 的存储空间，请执行以下步骤：

1. 在 TiDB Cloud 控制台中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。
2. 在要扩缩容的集群所在行，点击 **...**。

    > **提示：**
    >
    > 或者，您也可以在**集群**页面上点击要扩缩容的集群名称，然后点击右上角的 **...**。

3. 在下拉菜单中点击**修改**。此时会显示**修改集群**页面。
4. 在**修改集群**页面上，更改每个 TiKV 或 TiFlash 节点的存储空间。
5. 在右侧窗格中查看集群大小，然后点击**确认**。

您也可以通过 [修改 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 端点使用 TiDB Cloud API 更改 TiKV 或 TiFlash 节点的存储空间。目前，TiDB Cloud API 仍处于测试阶段。有关更多信息，请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta)。

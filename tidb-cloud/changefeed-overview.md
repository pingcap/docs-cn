---
title: Changefeed
summary: TiDB Cloud changefeed 帮助你将数据从 TiDB Cloud 流式传输到其他数据服务。
---

# Changefeed

TiDB Cloud changefeed 帮助你将数据从 TiDB Cloud 流式传输到其他数据服务。目前，TiDB Cloud 支持将数据流式传输到 Apache Kafka、MySQL、TiDB Cloud 和云存储。

> **注意：**
>
> - 目前，TiDB Cloud 每个集群最多允许 100 个 changefeed。
> - 目前，TiDB Cloud 每个 changefeed 最多允许 100 个表过滤规则。
> - 对于 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)，changefeed 功能不可用。

## 查看 Changefeed 页面

要访问 changefeed 功能，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

    > **提示：**
    >
    > 你可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **Changefeed**。此时会显示 changefeed 页面。

在 **Changefeed** 页面上，你可以创建 changefeed，查看现有 changefeed 列表，以及操作现有的 changefeed（如扩缩容、暂停、恢复、编辑和删除 changefeed）。

## 创建 changefeed

要创建 changefeed，请参考以下教程：

- [导出到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
- [导出到 MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)
- [导出到 TiDB Cloud](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)
- [导出到云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)

## 查询 Changefeed RCU

1. 导航到目标 TiDB 集群的 [**Changefeed**](#查看-changefeed-页面) 页面。
2. 找到要查询的相应 changefeed，然后在**操作**列中点击 **...** > **查看**。
3. 你可以在页面的**规格**区域看到当前的 TiCDC 复制容量单位（RCU）。

## 扩缩容 changefeed

你可以通过扩容或缩容 changefeed 来更改其 TiCDC 复制容量单位（RCU）。

> **注意：**
>
> - 要扩缩容集群的 changefeed，请确保该集群的所有 changefeed 都是在 2023 年 3 月 28 日之后创建的。
> - 如果集群有在 2023 年 3 月 28 日之前创建的 changefeed，则该集群的现有 changefeed 和新创建的 changefeed 都不支持扩容或缩容。

1. 导航到目标 TiDB 集群的 [**Changefeed**](#查看-changefeed-页面) 页面。
2. 找到要扩缩容的相应 changefeed，然后在**操作**列中点击 **...** > **扩缩容**。
3. 选择新的规格。
4. 点击**提交**。

完成扩缩容过程大约需要 10 分钟（在此期间 changefeed 正常工作），切换到新规格需要几秒钟（在此期间 changefeed 将自动暂停和恢复）。

## 暂停或恢复 changefeed

1. 导航到目标 TiDB 集群的 [**Changefeed**](#查看-changefeed-页面) 页面。
2. 找到要暂停或恢复的相应 changefeed，然后在**操作**列中点击 **...** > **暂停/恢复**。

## 编辑 changefeed

> **注意：**
>
> TiDB Cloud 目前仅允许编辑处于暂停状态的 changefeed。

1. 导航到目标 TiDB 集群的 [**Changefeed**](#查看-changefeed-页面) 页面。
2. 找到要暂停的 changefeed，然后在**操作**列中点击 **...** > **暂停**。
3. 当 changefeed 状态变为 `已暂停` 时，点击 **...** > **编辑**以编辑相应的 changefeed。

    TiDB Cloud 默认填充 changefeed 配置。你可以修改以下配置：

    - Apache Kafka 导出：所有配置。
    - MySQL 导出：**MySQL 连接**、**表过滤器**和**事件过滤器**。
    - TiDB Cloud 导出：**TiDB Cloud 连接**、**表过滤器**和**事件过滤器**。
    - 云存储导出：**存储端点**、**表过滤器**和**事件过滤器**。

4. 编辑配置后，点击 **...** > **恢复**以恢复相应的 changefeed。

## 删除 changefeed

1. 导航到目标 TiDB 集群的 [**Changefeed**](#查看-changefeed-页面) 页面。
2. 找到要删除的相应 changefeed，然后在**操作**列中点击 **...** > **删除**。

## Changefeed 计费

要了解 TiDB Cloud 中 changefeed 的计费情况，请参见 [Changefeed 计费](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md)。

## Changefeed 状态

复制任务的状态表示复制任务的运行状态。在运行过程中，复制任务可能因错误而失败，被手动暂停、恢复，或达到指定的 `TargetTs`。这些行为可能导致复制任务状态的变化。

状态说明如下：

- `CREATING`：正在创建复制任务。
- `RUNNING`：复制任务正常运行，checkpoint-ts 正常推进。
- `EDITING`：正在编辑复制任务。
- `PAUSING`：正在暂停复制任务。
- `PAUSED`：复制任务已暂停。
- `RESUMING`：正在恢复复制任务。
- `DELETING`：正在删除复制任务。
- `DELETED`：复制任务已删除。
- `WARNING`：复制任务返回警告。由于一些可恢复的错误，复制无法继续。处于此状态的 changefeed 会一直尝试恢复，直到状态转为 `RUNNING`。处于此状态的 changefeed 会阻塞 [GC 操作](https://docs.pingcap.com/tidb/stable/garbage-collection-overview)。
- `FAILED`：复制任务失败。由于某些错误，复制任务无法恢复且无法自动恢复。如果在增量数据的垃圾回收（GC）之前解决了问题，你可以手动恢复失败的 changefeed。增量数据的默认生存时间（TTL）为 24 小时，这意味着 GC 机制不会删除 changefeed 中断后 24 小时内的任何数据。

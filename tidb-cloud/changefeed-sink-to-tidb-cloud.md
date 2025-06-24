---
title: 同步到 TiDB Cloud
summary: 本文档介绍如何将数据从 TiDB Cloud Dedicated 集群流式传输到 TiDB Cloud Serverless 集群。该功能对 changefeed 数量和可用区域有限制。前提条件包括延长 tidb_gc_life_time、备份数据以及获取 TiDB Cloud sink 的起始位置。要创建 TiDB Cloud sink，需要导航到集群概览页面、建立连接、自定义表和事件过滤器、填写开始复制位置、指定 changefeed 规格、审查配置并创建 sink。最后，将 tidb_gc_life_time 恢复为原始值。
---

# 同步到 TiDB Cloud

本文档介绍如何将数据从 TiDB Cloud Dedicated 集群流式传输到 TiDB Cloud Serverless 集群。

> **注意：**
>
> 要使用 Changefeed 功能，请确保你的 TiDB Cloud Dedicated 集群版本为 v6.1.3 或更高版本。

## 限制

- 对于每个 TiDB Cloud 集群，你最多可以创建 100 个 changefeed。
- 因为 TiDB Cloud 使用 TiCDC 建立 changefeed，所以它具有与 [TiCDC 相同的限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果要复制的表没有主键或非空唯一索引，在某些重试场景下，由于缺少唯一约束，可能会导致下游插入重复数据。
- **同步到 TiDB Cloud** 功能仅适用于 2022 年 11 月 9 日之后创建的、位于以下 AWS 区域的 TiDB Cloud Dedicated 集群：

    - AWS 俄勒冈（us-west-2）
    - AWS 法兰克福（eu-central-1）
    - AWS 新加坡（ap-southeast-1）
    - AWS 东京（ap-northeast-1）

- 源 TiDB Cloud Dedicated 集群和目标 TiDB Cloud Serverless 集群必须在同一个项目和同一个区域中。
- **同步到 TiDB Cloud** 功能仅支持通过私有端点进行网络连接。当你创建 changefeed 将数据从 TiDB Cloud Dedicated 集群流式传输到 TiDB Cloud Serverless 集群时，TiDB Cloud 将自动在两个集群之间设置私有端点连接。

## 前提条件

**同步到 TiDB Cloud** 连接器只能在某个 [TSO](https://docs.pingcap.com/tidb/stable/glossary#tso) 之后将增量数据从 TiDB Cloud Dedicated 集群同步到 TiDB Cloud Serverless 集群。

在创建 changefeed 之前，你需要从源 TiDB Cloud Dedicated 集群导出现有数据并将数据加载到目标 TiDB Cloud Serverless 集群。

1. 将 [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) 延长至超过以下两个操作的总时间，这样 TiDB 就不会对这段时间内的历史数据进行垃圾回收。

    - 导出和导入现有数据的时间
    - 创建**同步到 TiDB Cloud**的时间

    例如：

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. 使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 从你的 TiDB Cloud Dedicated 集群导出数据，然后使用 [TiDB Cloud Serverless 导入](/tidb-cloud/import-csv-files-serverless.md)将数据加载到目标 TiDB Cloud Serverless 集群。

3. 从 [Dumpling 导出的文件](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files)中，从元数据文件获取 TiDB Cloud sink 的起始位置：

    以下是一个示例元数据文件的部分内容。`SHOW MASTER STATUS` 的 `Pos` 是现有数据的 TSO，也是 TiDB Cloud sink 的起始位置。

    ```
    Started dump at: 2023-03-28 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2023-03-28 10:40:20
    ```

## 创建 TiDB Cloud sink

完成前提条件后，你可以将数据同步到目标 TiDB Cloud Serverless 集群。

1. 导航到目标 TiDB 集群的集群概览页面，然后在左侧导航栏中点击**数据** > **Changefeed**。

2. 点击**创建 Changefeed**，并选择 **TiDB Cloud** 作为目标。

3. 在 **TiDB Cloud 连接**区域，选择目标 TiDB Cloud Serverless 集群，然后填写目标集群的用户名和密码。

4. 点击**下一步**以建立两个 TiDB 集群之间的连接，并测试 changefeed 是否可以成功连接它们：

    - 如果可以，你将进入下一步配置。
    - 如果不可以，将显示连接错误，你需要处理该错误。错误解决后，再次点击**下一步**。

5. 自定义**表过滤器**以过滤要复制的表。有关规则语法，请参考[表过滤规则](/table-filter.md)。

    - **过滤规则**：你可以在此列中设置过滤规则。默认有一个规则 `*.*`，表示复制所有表。当你添加新规则时，TiDB Cloud 会查询 TiDB 中的所有表，并在右侧框中只显示匹配规则的表。你最多可以添加 100 个过滤规则。
    - **具有有效键的表**：此列显示具有有效键（包括主键或唯一索引）的表。
    - **没有有效键的表**：此列显示缺少主键或唯一键的表。这些表在复制过程中会带来挑战，因为缺少唯一标识符可能会导致下游处理重复事件时数据不一致。为确保数据一致性，建议在开始复制之前为这些表添加唯一键或主键。或者，你可以添加过滤规则来排除这些表。例如，你可以使用规则 `"!test.tbl1"` 来排除表 `test.tbl1`。

6. 自定义**事件过滤器**以过滤要复制的事件。

    - **匹配表**：你可以在此列中设置事件过滤器将应用于哪些表。规则语法与前面的**表过滤器**区域使用的语法相同。每个 changefeed 最多可以添加 10 个事件过滤规则。
    - **忽略的事件**：你可以设置事件过滤器将从 changefeed 中排除哪些类型的事件。

7. 在**开始复制位置**区域，填写你从 Dumpling 导出的元数据文件中获取的 TSO。

8. 点击**下一步**以配置你的 changefeed 规格。

    - 在 **Changefeed 规格**区域，指定 changefeed 要使用的复制容量单位（RCU）数量。
    - 在 **Changefeed 名称**区域，为 changefeed 指定一个名称。

9. 点击**下一步**以审查 changefeed 配置。

    如果你确认所有配置都正确，请检查跨区域复制的合规性，然后点击**创建**。

    如果你想修改某些配置，点击**上一步**返回上一个配置页面。

10. sink 很快就会启动，你可以看到 sink 的状态从**创建中**变为**运行中**。

    点击 changefeed 名称，你可以看到有关 changefeed 的更多详细信息，如检查点、复制延迟和其他指标。

11. 在创建 sink 后，将 [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) 恢复为原始值（默认值为 `10m`）：

    ```sql
    SET GLOBAL tidb_gc_life_time = '10m';
    ```

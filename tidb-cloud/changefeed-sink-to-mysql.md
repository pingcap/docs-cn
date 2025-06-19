---
title: 同步到 MySQL
summary: 本文档介绍如何使用同步到 MySQL 的 changefeed 将数据从 TiDB Cloud 流式传输到 MySQL。它包括限制、前提条件以及创建 MySQL sink 进行数据复制的步骤。该过程涉及设置网络连接、将现有数据加载到 MySQL 以及在 MySQL 中创建目标表。完成前提条件后，用户可以创建 MySQL sink 以将数据复制到 MySQL。
---

# 同步到 MySQL

本文档介绍如何使用**同步到 MySQL** changefeed 将数据从 TiDB Cloud 流式传输到 MySQL。

> **注意：**
>
> - 要使用 changefeed 功能，请确保你的 TiDB Cloud Dedicated 集群版本为 v6.1.3 或更高版本。
> - 对于 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)，changefeed 功能不可用。

## 限制

- 对于每个 TiDB Cloud 集群，你最多可以创建 100 个 changefeed。
- 因为 TiDB Cloud 使用 TiCDC 建立 changefeed，所以它具有与 [TiCDC 相同的限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果要复制的表没有主键或非空唯一索引，在某些重试场景下，由于缺少唯一约束，可能会导致下游插入重复数据。

## 前提条件

在创建 changefeed 之前，你需要完成以下前提条件：

- 设置网络连接
- 导出并加载现有数据到 MySQL（可选）
- 如果你不加载现有数据，只想将增量数据复制到 MySQL，则需要在 MySQL 中创建相应的目标表

### 网络

确保你的 TiDB 集群可以连接到 MySQL 服务。

如果你的 MySQL 服务在没有公共互联网访问的 AWS VPC 中，请执行以下步骤：

1. 在 MySQL 服务的 VPC 和你的 TiDB 集群之间[设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
2. 修改 MySQL 服务关联的安全组的入站规则。

    你必须将[你的 TiDB Cloud 集群所在区域的 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) 添加到入站规则中。这样可以允许流量从你的 TiDB 集群流向 MySQL 实例。

3. 如果 MySQL URL 包含主机名，你需要允许 TiDB Cloud 能够解析 MySQL 服务的 DNS 主机名。

    1. 按照[为 VPC 对等连接启用 DNS 解析](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)中的步骤操作。
    2. 启用**接受者 DNS 解析**选项。

如果你的 MySQL 服务在没有公共互联网访问的 Google Cloud VPC 中，请执行以下步骤：

1. 如果你的 MySQL 服务是 Google Cloud SQL，你必须在 Google Cloud SQL 实例关联的 VPC 中暴露一个 MySQL 端点。你可能需要使用 Google 开发的 [**Cloud SQL Auth proxy**](https://cloud.google.com/sql/docs/mysql/sql-proxy)。
2. 在 MySQL 服务的 VPC 和你的 TiDB 集群之间[设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
3. 修改 MySQL 所在 VPC 的入站防火墙规则。

    你必须将[你的 TiDB Cloud 集群所在区域的 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) 添加到入站防火墙规则中。这样可以允许流量从你的 TiDB 集群流向 MySQL 端点。

### 加载现有数据（可选）

**同步到 MySQL** 连接器只能在某个时间戳之后将增量数据从你的 TiDB 集群同步到 MySQL。如果你的 TiDB 集群中已经有数据，你可以在启用**同步到 MySQL**之前将 TiDB 集群的现有数据导出并加载到 MySQL 中。

要加载现有数据：

1. 将 [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) 延长至超过以下两个操作的总时间，这样 TiDB 就不会对这段时间内的历史数据进行垃圾回收。

    - 导出和导入现有数据的时间
    - 创建**同步到 MySQL**的时间

    例如：

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. 使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 从你的 TiDB 集群导出数据，然后使用社区工具（如 [mydumper/myloader](https://centminmod.com/mydumper.html)）将数据加载到 MySQL 服务。

3. 从 [Dumpling 导出的文件](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files)中，从元数据文件获取 MySQL sink 的起始位置：

    以下是一个示例元数据文件的部分内容。`SHOW MASTER STATUS` 的 `Pos` 是现有数据的 TSO，也是 MySQL sink 的起始位置。

    ```
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ```

### 在 MySQL 中创建目标表

如果你不加载现有数据，你需要在 MySQL 中手动创建相应的目标表来存储来自 TiDB 的增量数据。否则，数据将不会被复制。

## 创建 MySQL sink

完成前提条件后，你可以将数据同步到 MySQL。

1. 导航到目标 TiDB 集群的集群概览页面，然后在左侧导航栏中点击**数据** > **Changefeed**。

2. 点击**创建 Changefeed**，并选择 **MySQL** 作为**目标**。

3. 在 **MySQL 连接**中填写 MySQL 端点、用户名和密码。

4. 点击**下一步**以测试 TiDB 是否可以成功连接到 MySQL：

    - 如果可以，你将进入下一步配置。
    - 如果不可以，将显示连接错误，你需要处理该错误。错误解决后，再次点击**下一步**。

5. 自定义**表过滤器**以过滤要复制的表。有关规则语法，请参考[表过滤规则](/table-filter.md)。

    - **过滤规则**：你可以在此列中设置过滤规则。默认有一个规则 `*.*`，表示复制所有表。当你添加新规则时，TiDB Cloud 会查询 TiDB 中的所有表，并在右侧框中只显示匹配规则的表。你最多可以添加 100 个过滤规则。
    - **具有有效键的表**：此列显示具有有效键（包括主键或唯一索引）的表。
    - **没有有效键的表**：此列显示缺少主键或唯一键的表。这些表在复制过程中会带来挑战，因为缺少唯一标识符可能会导致下游处理重复事件时数据不一致。为确保数据一致性，建议在开始复制之前为这些表添加唯一键或主键。或者，你可以添加过滤规则来排除这些表。例如，你可以使用规则 `"!test.tbl1"` 来排除表 `test.tbl1`。

6. 自定义**事件过滤器**以过滤要复制的事件。

    - **匹配表**：你可以在此列中设置事件过滤器将应用于哪些表。规则语法与前面的**表过滤器**区域使用的语法相同。每个 changefeed 最多可以添加 10 个事件过滤规则。
    - **忽略的事件**：你可以设置事件过滤器将从 changefeed 中排除哪些类型的事件。

7. 在**开始复制位置**中，配置 MySQL sink 的起始位置。

    - 如果你已经使用 Dumpling [加载了现有数据](#加载现有数据可选)，选择**从特定 TSO 开始复制**，并填写你从 Dumpling 导出的元数据文件中获取的 TSO。
    - 如果上游 TiDB 集群中没有任何数据，选择**从现在开始复制**。
    - 否则，你可以通过选择**从特定时间开始复制**来自定义开始时间点。

8. 点击**下一步**以配置你的 changefeed 规格。

    - 在 **Changefeed 规格**区域，指定 changefeed 要使用的复制容量单位（RCU）数量。
    - 在 **Changefeed 名称**区域，为 changefeed 指定一个名称。

9. 点击**下一步**以审查 changefeed 配置。

    如果你确认所有配置都正确，请检查跨区域复制的合规性，然后点击**创建**。

    如果你想修改某些配置，点击**上一步**返回上一个配置页面。

10. sink 很快就会启动，你可以看到 sink 的状态从**创建中**变为**运行中**。

    点击 changefeed 名称，你可以看到有关 changefeed 的更多详细信息，如检查点、复制延迟和其他指标。

11. 如果你已经使用 Dumpling [加载了现有数据](#加载现有数据可选)，你需要在创建 sink 后将 GC 时间恢复为原始值（默认值为 `10m`）：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

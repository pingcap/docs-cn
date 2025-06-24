---
title: 导出数据到云存储
summary: 本文介绍如何创建 changefeed 将数据从 TiDB Cloud 流式传输到 Amazon S3 或 GCS。包括限制、目标配置步骤、复制和规格配置，以及启动复制过程。
---

# 导出数据到云存储

本文介绍如何创建 changefeed 将数据从 TiDB Cloud 流式传输到云存储。目前支持 Amazon S3 和 GCS。

> **注意：**
>
> - 要将数据流式传输到云存储，请确保您的 TiDB 集群版本为 v7.1.1 或更高版本。要将 TiDB Cloud Dedicated 集群升级到 v7.1.1 或更高版本，请[联系 TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)。
> - 对于 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群，changefeed 功能不可用。

## 限制

- 每个 TiDB Cloud 集群最多可以创建 100 个 changefeed。
- 由于 TiDB Cloud 使用 TiCDC 建立 changefeed，因此它具有与 TiCDC 相同的[限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果要复制的表没有主键或非空唯一索引，在某些重试场景下，由于缺少唯一约束，可能会导致下游插入重复数据。

## 步骤 1. 配置目标

导航到目标 TiDB 集群的集群概览页面。在左侧导航栏中点击**数据** > **Changefeed**，点击**创建 Changefeed**，然后选择 **Amazon S3** 或 **GCS** 作为目标。配置过程根据您选择的目标而有所不同。

<SimpleTab>
<div label="Amazon S3">

对于 **Amazon S3**，填写 **S3 端点**区域：`S3 URI`、`Access Key ID` 和 `Secret Access Key`。确保 S3 存储桶与您的 TiDB 集群在同一区域。

![s3_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-s3-endpoint.jpg)

</div>
<div label="GCS">

对于 **GCS**，在填写 **GCS 端点**之前，您需要先授予 GCS 存储桶访问权限。请按照以下步骤操作：

1. 在 TiDB Cloud 控制台中，记录**服务账号 ID**，该 ID 将用于授予 TiDB Cloud 访问您的 GCS 存储桶的权限。

    ![gcs_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-endpoint.png)

2. 在 Google Cloud 控制台中，为您的 GCS 存储桶创建 IAM 角色。

    1. 登录 [Google Cloud 控制台](https://console.cloud.google.com/)。
    2. 转到[角色](https://console.cloud.google.com/iam-admin/roles)页面，然后点击**创建角色**。

        ![创建角色](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-create-role.png)

    3. 为角色输入名称、描述、ID 和角色启动阶段。角色创建后，角色名称无法更改。
    4. 点击**添加权限**。将以下权限添加到角色，然后点击**添加**。

        - storage.buckets.get
        - storage.objects.create
        - storage.objects.delete
        - storage.objects.get
        - storage.objects.list
        - storage.objects.update

    ![添加权限](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-assign-permission.png)

3. 转到[存储桶](https://console.cloud.google.com/storage/browser)页面，选择您希望 TiDB Cloud 访问的 GCS 存储桶。请注意，GCS 存储桶必须与您的 TiDB 集群在同一区域。

4. 在**存储桶详情**页面，点击**权限**标签，然后点击**授予访问权限**。

    ![授予存储桶访问权限](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-grant-access-1.png)

5. 填写以下信息以授予存储桶访问权限，然后点击**保存**。

    - 在**新主体**字段中，粘贴您之前记录的目标 TiDB 集群的**服务账号 ID**。
    - 在**选择角色**下拉列表中，输入您刚刚创建的 IAM 角色名称，然后从筛选结果中选择该名称。

    > **注意：**
    >
    > 要移除 TiDB Cloud 的访问权限，只需移除您已授予的访问权限即可。

6. 在**存储桶详情**页面，点击**对象**标签。

    - 要获取存储桶的 gsutil URI，点击复制按钮并添加 `gs://` 作为前缀。例如，如果存储桶名称为 `test-sink-gcs`，则 URI 为 `gs://test-sink-gcs/`。

        ![获取存储桶 URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri01.png)

    - 要获取文件夹的 gsutil URI，打开文件夹，点击复制按钮，并添加 `gs://` 作为前缀。例如，如果存储桶名称为 `test-sink-gcs`，文件夹名称为 `changefeed-xxx`，则 URI 为 `gs://test-sink-gcs/changefeed-xxx/`。

        ![获取存储桶 URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri02.png)

7. 在 TiDB Cloud 控制台中，转到 Changefeed 的**配置目标**页面，并填写**存储桶 gsutil URI** 字段。

</div>
</SimpleTab>

点击**下一步**以建立从 TiDB Cloud Dedicated 集群到 Amazon S3 或 GCS 的连接。TiDB Cloud 将自动测试并验证连接是否成功。

- 如果成功，您将进入下一步配置。
- 如果失败，将显示连接错误，您需要处理该错误。错误解决后，点击**下一步**重试连接。

## 步骤 2. 配置复制

1. 自定义**表过滤器**以过滤要复制的表。有关规则语法，请参考[表过滤规则](https://docs.pingcap.com/tidb/stable/ticdc-filter#changefeed-log-filters)。

    ![changefeed 的表过滤器](/media/tidb-cloud/changefeed/sink-to-s3-02-table-filter.jpg)

    - **过滤规则**：您可以在此列设置过滤规则。默认有一个规则 `*.*`，表示复制所有表。添加新规则时，TiDB Cloud 会查询 TiDB 中的所有表，并在右侧框中仅显示匹配规则的表。您最多可以添加 100 个过滤规则。
    - **具有有效键的表**：此列显示具有有效键（包括主键或唯一索引）的表。
    - **没有有效键的表**：此列显示缺少主键或唯一键的表。这些表在复制过程中会带来挑战，因为缺少唯一标识符可能会导致在处理下游重复事件时出现数据不一致。为确保数据一致性，建议在开始复制之前为这些表添加唯一键或主键。或者，您可以使用过滤规则排除这些表。例如，您可以使用规则 `"!test.tbl1"` 排除表 `test.tbl1`。

2. 自定义**事件过滤器**以过滤要复制的事件。

    - **匹配表**：您可以在此列设置事件过滤器将应用于哪些表。规则语法与前面的**表过滤器**区域使用的语法相同。每个 changefeed 最多可以添加 10 个事件过滤规则。
    - **忽略的事件**：您可以设置事件过滤器将从 changefeed 中排除哪些类型的事件。

3. 在**开始复制位置**区域，选择以下复制位置之一：

    - 从现在开始复制
    - 从特定 [TSO](https://docs.pingcap.com/tidb/stable/glossary#tso) 开始复制
    - 从特定时间开始复制

4. 在**数据格式**区域，选择 **CSV** 或 **Canal-JSON** 格式。

    <SimpleTab>
    <div label="配置 CSV 格式">

    要配置 **CSV** 格式，请填写以下字段：

    - **二进制编码方法**：二进制数据的编码方法。您可以选择 **base64**（默认）或 **hex**。如果要与 AWS DMS 集成，请使用 **hex**。
    - **日期分隔符**：根据年、月、日轮换数据，或选择不轮换。
    - **分隔符**：指定用于分隔 CSV 文件中值的字符。逗号（`,`）是最常用的分隔符。
    - **引号**：指定用于包围包含分隔符或特殊字符的值的字符。通常使用双引号（`"`）作为引号字符。
    - **空值/空值**：指定如何在 CSV 文件中表示空值或空值。这对于正确处理和解释数据很重要。
    - **包含提交时间戳**：控制是否在 CSV 行中包含 [`commit-ts`](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-cloud-storage#replicate-change-data-to-storage-services)。

    </div>
    <div label="配置 Canal-JSON 格式">

    Canal-JSON 是一种纯 JSON 文本格式。要配置它，请填写以下字段：

    - **日期分隔符**：根据年、月、日轮换数据，或选择不轮换。
    - **启用 TiDB 扩展**：启用此选项后，TiCDC 会发送 [WATERMARK 事件](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#watermark-event)并在 Canal-JSON 消息中添加 [TiDB 扩展字段](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field)。

    </div>
    </SimpleTab>

5. 在**刷新参数**区域，您可以配置两个项目：

    - **刷新间隔**：默认设置为 60 秒，可在 2 秒到 10 分钟范围内调整；
    - **文件大小**：默认设置为 64 MB，可在 1 MB 到 512 MB 范围内调整。

    ![刷新参数](/media/tidb-cloud/changefeed/sink-to-cloud-storage-flush-parameters.jpg)

    > **注意：**
    >
    > 这两个参数将影响每个数据库表在云存储中生成的对象数量。如果有大量表，使用相同的配置将增加生成的对象数量，从而增加调用云存储 API 的成本。因此，建议根据您的恢复点目标（RPO）和成本要求适当配置这些参数。

## 步骤 3. 配置规格

点击**下一步**以配置您的 changefeed 规格。

1. 在 **Changefeed 规格**区域，指定 changefeed 将使用的复制容量单位（RCU）数量。
2. 在 **Changefeed 名称**区域，为 changefeed 指定一个名称。

## 步骤 4. 查看配置并开始复制

点击**下一步**以查看 changefeed 配置。

- 如果您已验证所有配置都正确，点击**创建**以继续创建 changefeed。
- 如果您需要修改任何配置，点击**上一步**返回并进行必要的更改。

导出将很快开始，您将看到导出状态从**创建中**变为**运行中**。

点击 changefeed 的名称以转到其详情页面。在此页面上，您可以查看有关 changefeed 的更多信息，包括检查点状态、复制延迟和其他相关指标。

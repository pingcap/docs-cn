---
title: 从 TiDB Cloud Serverless 导出数据
summary: 了解如何从 TiDB Cloud Serverless 集群导出数据。
---

# 从 TiDB Cloud Serverless 导出数据

TiDB Cloud Serverless 导出功能（Beta）是一项服务，可让您将数据从 TiDB Cloud Serverless 集群导出到本地文件或外部存储服务。您可以将导出的数据用于备份、迁移、数据分析或其他用途。

虽然您也可以使用 [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) 和 TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview) 等工具导出数据，但 TiDB Cloud Serverless 导出功能提供了一种更便捷、高效的方式来从 TiDB Cloud Serverless 集群导出数据。它具有以下优势：

- 便捷性：导出服务提供了一种简单易用的方式来从 TiDB Cloud Serverless 集群导出数据，无需额外的工具或资源。
- 隔离性：导出服务使用独立的计算资源，确保与您的在线服务资源隔离。
- 一致性：导出服务确保导出数据的一致性，且不会造成锁定，不影响您的在线服务。

> **注意：**
>
> 目前最大导出大小为 1 TiB。如需导出更多数据或请求更高的导出速度，请联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)。

## 导出位置

您可以将数据导出到以下位置：

- 本地文件
- 外部存储，包括：

    - [Amazon S3](https://aws.amazon.com/s3/)
    - [Google Cloud Storage](https://cloud.google.com/storage)
    - [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
    - [阿里云对象存储服务（OSS）](https://www.alibabacloud.com/product/oss)

> **注意：**
>
> 如果要导出的数据量较大（超过 100 GiB），建议导出到外部存储。

### 本地文件

要将数据从 TiDB Cloud Serverless 集群导出到本地文件，您需要[使用 TiDB Cloud 控制台](#导出数据到本地文件)或[使用 TiDB Cloud CLI](/tidb-cloud/ticloud-serverless-export-create.md) 导出数据，然后使用 TiDB Cloud CLI 下载导出的数据。

导出数据到本地文件有以下限制：

- 不支持使用 TiDB Cloud 控制台下载导出的数据。
- 导出的数据保存在 TiDB Cloud 的暂存区域，两天后过期。您需要及时下载导出的数据。
- 如果暂存区域的存储空间已满，您将无法导出数据到本地文件。

### Amazon S3

要导出数据到 Amazon S3，您需要提供以下信息：

- URI：`s3://<bucket-name>/<folder-path>/`
- 以下访问凭证之一：
    - [访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)：确保访问密钥具有 `s3:PutObject` 和 `s3:ListBucket` 权限。
    - [角色 ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html)：确保角色 ARN（Amazon Resource Name）具有 `s3:PutObject` 和 `s3:ListBucket` 权限。注意，只有托管在 AWS 上的集群支持角色 ARN。

更多信息，请参见[配置 Amazon S3 访问](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)。

### Google Cloud Storage

要导出数据到 Google Cloud Storage，您需要提供以下信息：

- URI：`gs://<bucket-name>/<folder-path>/`
- 访问凭证：存储桶的 **base64 编码**[服务账号密钥](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)。确保服务账号密钥具有 `storage.objects.create` 权限。

更多信息，请参见[配置 GCS 访问](/tidb-cloud/serverless-external-storage.md#configure-gcs-access)。

### Azure Blob Storage

要导出数据到 Azure Blob Storage，您需要提供以下信息：

- URI：`azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` 或 `https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
- 访问凭证：Azure Blob Storage 容器的[共享访问签名（SAS）令牌](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)。确保 SAS 令牌对 `Container` 和 `Object` 资源具有 `Read` 和 `Write` 权限。

更多信息，请参见[配置 Azure Blob Storage 访问](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access)。

### 阿里云 OSS

要导出数据到阿里云 OSS，您需要提供以下信息：

- URI：`oss://<bucket-name>/<folder-path>/`
- 访问凭证：阿里云账号的 [AccessKey 对](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)。确保 AccessKey 对具有 `oss:PutObject`、`oss:ListBuckets` 和 `oss:GetBucketInfo` 权限，以允许将数据导出到 OSS 存储桶。

更多信息，请参见[配置阿里云对象存储服务（OSS）访问](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access)。

## 导出选项

### 数据过滤

- TiDB Cloud 控制台支持导出选定的数据库和表。
- TiDB Cloud CLI 支持使用 SQL 语句和[表过滤器](/table-filter.md)导出数据。

### 数据格式

您可以将数据导出为以下格式：

- `SQL`：以 SQL 格式导出数据。
- `CSV`：以 CSV 格式导出数据。您可以指定以下选项：
    - `delimiter`：指定导出数据中使用的分隔符。默认分隔符为 `"`。
    - `separator`：指定导出数据中用于分隔字段的字符。默认分隔符为 `,`。
    - `header`：指定是否在导出数据中包含标题行。默认值为 `true`。
    - `null-value`：指定导出数据中表示 NULL 值的字符串。默认值为 `\N`。
- `Parquet`：以 Parquet 格式导出数据。

模式和数据的导出遵循以下命名约定：

| 项目            | 未压缩                                                | 已压缩                                                                                                          |
|-----------------|-------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| 数据库模式 | {database}-schema-create.sql                          | {database}-schema-create.sql.{compression-type}                                                                     |
| 表模式    | {database}.{table}-schema.sql                         | {database}.{table}-schema.sql.{compression-type}                                                                    |
| 数据            | {database}.{table}.{0001}.{csv&#124;parquet&#124;sql} | {database}.{table}.{0001}.{csv&#124;sql}.{compression-type}<br/>{database}.{table}.{0001}.{compression-type}.parquet |

### 数据压缩

您可以使用以下算法压缩导出的 CSV 和 SQL 数据：

- `gzip`（默认）：使用 `gzip` 压缩导出的数据。
- `snappy`：使用 `snappy` 压缩导出的数据。
- `zstd`：使用 `zstd` 压缩导出的数据。
- `none`：不压缩导出的数据。

您可以使用以下算法压缩导出的 Parquet 数据：

- `zstd`（默认）：使用 `zstd` 压缩 Parquet 文件。
- `gzip`：使用 `gzip` 压缩 Parquet 文件。
- `snappy`：使用 `snappy` 压缩 Parquet 文件。
- `none`：不压缩 Parquet 文件。

### 数据转换

在导出数据到 Parquet 格式时，TiDB Cloud Serverless 和 Parquet 之间的数据转换如下：

| TiDB Cloud Serverless 类型 | Parquet 基本类型 | Parquet 逻辑类型                         |
|----------------------------|-------------------------|----------------------------------------------|
| VARCHAR                    | BYTE_ARRAY              | String(UTF8)                                 |
| TIME                       | BYTE_ARRAY              | String(UTF8)                                 |
| TINYTEXT                   | BYTE_ARRAY              | String(UTF8)                                 |
| MEDIUMTEXT                 | BYTE_ARRAY              | String(UTF8)                                 |
| TEXT                       | BYTE_ARRAY              | String(UTF8)                                 |
| LONGTEXT                   | BYTE_ARRAY              | String(UTF8)                                 |
| SET                        | BYTE_ARRAY              | String(UTF8)                                 |
| JSON                       | BYTE_ARRAY              | String(UTF8)                                 |
| DATE                       | BYTE_ARRAY              | String(UTF8)                                 |
| CHAR                       | BYTE_ARRAY              | String(UTF8)                                 |
| VECTOR                     | BYTE_ARRAY              | String(UTF8)                                 |
| DECIMAL(1<=p<=9)           | INT32                   | DECIMAL(p,s)                                 |
| DECIMAL(10<=p<=18)         | INT64                   | DECIMAL(p,s)                                 |
| DECIMAL(p>=19)             | BYTE_ARRAY              | String(UTF8)                                 |
| ENUM                       | BYTE_ARRAY              | String(UTF8)                                 |
| TIMESTAMP                  | INT64                   | TIMESTAMP(unit=MICROS,isAdjustedToUTC=false) |
| DATETIME                   | INT64                   | TIMESTAMP(unit=MICROS,isAdjustedToUTC=false) |
| YEAR                       | INT32                   | /                                            |
| TINYINT                    | INT32                   | /                                            |
| UNSIGNED TINYINT           | INT32                   | /                                            |
| SMALLINT                   | INT32                   | /                                            |
| UNSIGNED SMALLINT          | INT32                   | /                                            |
| MEDIUMINT                  | INT32                   | /                                            |
| UNSIGNED MEDIUMINT         | INT32                   | /                                            |
| INT                        | INT32                   | /                                            |
| UNSIGNED INT               | FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0)                                |
| BIGINT                     | FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0)                                |
| UNSIGNED BIGINT            | BYTE_ARRAY              | String(UTF8)                                 |
| FLOAT                      | FLOAT                   | /                                            |
| DOUBLE                     | DOUBLE                  | /                                            |
| BLOB                       | BYTE_ARRAY              | /                                            |
| TINYBLOB                   | BYTE_ARRAY              | /                                            |
| MEDIUMBLOB                 | BYTE_ARRAY              | /                                            |
| LONGBLOB                   | BYTE_ARRAY              | /                                            |
| BINARY                     | BYTE_ARRAY              | /                                            |
| VARBINARY                  | BYTE_ARRAY              | /                                            |
| BIT                        | BYTE_ARRAY              | /                                            |

## 示例

### 导出数据到本地文件

<SimpleTab>
<div label="控制台">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

   > **提示：**
   >
   > 您可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

3. 在**导入**页面，点击右上角的**导出数据到**，然后从下拉列表中选择**本地文件**。填写以下参数：

    - **任务名称**：输入导出任务的名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **导出数据**：选择要导出的数据库和表。
    - **数据格式**：选择 **SQL**、**CSV** 或 **Parquet**。
    - **压缩**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。

   > **提示：**
   >
   > 如果您的集群之前没有导入或导出任何数据，您需要点击页面底部的**点击此处导出数据到...**来导出数据。

4. 点击**导出**。

5. 导出任务成功后，您可以复制导出任务详情中显示的下载命令，然后在 [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 中运行该命令下载导出的数据。

</div>

<div label="CLI">

1. 创建导出任务：

    ```shell
    ticloud serverless export create -c <cluster-id>
    ```

    您将从输出中获得导出 ID。

2. 导出任务成功后，将导出的数据下载到本地文件：

    ```shell
    ticloud serverless export download -c <cluster-id> -e <export-id>
    ```

    有关下载命令的更多信息，请参见 [ticloud serverless export download](/tidb-cloud/ticloud-serverless-export-download.md)。
 
</div>
</SimpleTab>

### 导出数据到 Amazon S3

<SimpleTab>
<div label="控制台">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

   > **提示：**
   >
   > 您可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

3. 在**导入**页面，点击右上角的**导出数据到**，然后从下拉列表中选择 **Amazon S3**。填写以下参数：

    - **任务名称**：输入导出任务的名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **导出数据**：选择要导出的数据库和表。
    - **数据格式**：选择 **SQL**、**CSV** 或 **Parquet**。
    - **压缩**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。
    - **文件夹 URI**：输入 Amazon S3 的 URI，格式为 `s3://<bucket-name>/<folder-path>/`。
    - **存储桶访问**：选择以下访问凭证之一，然后填写凭证信息：
        - **AWS 角色 ARN**：输入具有访问存储桶权限的角色 ARN。建议使用 AWS CloudFormation 创建角色 ARN。更多信息，请参见[配置 TiDB Cloud Serverless 的外部存储访问](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)。
        - **AWS 访问密钥**：输入具有访问存储桶权限的访问密钥 ID 和访问密钥密钥。

4. 点击**导出**。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter "database.table"

ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.role-arn <role-arn> --filter "database.table"
```

- `s3.uri`：Amazon S3 URI，格式为 `s3://<bucket-name>/<folder-path>/`。
- `s3.access-key-id`：具有访问存储桶权限的用户的访问密钥 ID。
- `s3.secret-access-key`：具有访问存储桶权限的用户的访问密钥密钥。
- `s3.role-arn`：具有访问存储桶权限的角色 ARN。

</div>
</SimpleTab>

### 导出数据到 Google Cloud Storage

<SimpleTab>
<div label="控制台">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

   > **提示：**
   >
   > 您可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

3. 在**导入**页面，点击右上角的**导出数据到**，然后从下拉列表中选择 **Google Cloud Storage**。填写以下参数：

    - **任务名称**：输入导出任务的名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **导出数据**：选择要导出的数据库和表。
    - **数据格式**：选择 **SQL**、**CSV** 或 **Parquet**。
    - **压缩**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。
    - **文件夹 URI**：输入 Google Cloud Storage 的 URI，格式为 `gs://<bucket-name>/<folder-path>/`。
    - **存储桶访问**：上传具有访问存储桶权限的 Google Cloud 凭证文件。

4. 点击**导出**。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type GCS --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter "database.table"
```

- `gcs.uri`：Google Cloud Storage 存储桶的 URI，格式为 `gs://<bucket-name>/<folder-path>/`。
- `gcs.service-account-key`：base64 编码的服务账号密钥。

</div>
</SimpleTab>

### 导出数据到 Azure Blob Storage

<SimpleTab>
<div label="控制台">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

   > **提示：**
   >
   > 您可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

3. 在**导入**页面，点击右上角的**导出数据到**，然后从下拉列表中选择 **Azure Blob Storage**。填写以下参数：

    - **任务名称**：输入导出任务的名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **导出数据**：选择要导出的数据库和表。
    - **数据格式**：选择 **SQL**、**CSV** 或 **Parquet**。
    - **压缩**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。
    - **文件夹 URI**：输入 Azure Blob Storage 的 URI，格式为 `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`。
    - **SAS 令牌**：输入具有访问容器权限的 SAS 令牌。建议使用 [Azure ARM 模板](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/)创建 SAS 令牌。更多信息，请参见[配置 TiDB Cloud Serverless 的外部存储访问](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access)。

4. 点击**导出**。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type AZURE_BLOB --azblob.uri <uri> --azblob.sas-token <sas-token> --filter "database.table"
```

- `azblob.uri`：Azure Blob Storage 的 URI，格式为 `(azure|https)://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`。
- `azblob.sas-token`：Azure Blob Storage 的账号 SAS 令牌。

</div>
</SimpleTab>

### 导出数据到阿里云 OSS

<SimpleTab>
<div label="控制台">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

   > **提示：**
   >
   > 您可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

3. 在**导入**页面，点击右上角的**导出数据到**，然后从下拉列表中选择**阿里云 OSS**。

4. 填写以下参数：

    - **任务名称**：输入导出任务的名称。默认值为 `SNAPSHOT_{snapshot_time}`。
    - **导出数据**：选择要导出的数据库和表。
    - **数据格式**：选择 **SQL**、**CSV** 或 **Parquet**。
    - **压缩**：选择 **Gzip**、**Snappy**、**Zstd** 或 **None**。
    - **文件夹 URI**：输入要导出数据的阿里云 OSS URI，格式为 `oss://<bucket-name>/<folder-path>/`。
    - **AccessKey ID** 和 **AccessKey Secret**：输入具有访问存储桶权限的 AccessKey ID 和 AccessKey Secret。

5. 点击**导出**。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type OSS --oss.uri <uri> --oss.access-key-id <access-key-id> --oss.access-key-secret <access-key-secret> --filter "database.table"
```

- `oss.uri`：要导出数据的阿里云 OSS URI，格式为 `oss://<bucket-name>/<folder-path>/`。
- `oss.access-key-id`：具有访问存储桶权限的用户的 AccessKey ID。
- `oss.access-key-secret`：具有访问存储桶权限的用户的 AccessKey Secret。

</div>
</SimpleTab>

### 取消导出任务

要取消正在进行的导出任务，请执行以下步骤：

<SimpleTab>
<div label="控制台">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

   > **提示：**
   >
   > 您可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

3. 在**导入**页面，点击**导出**查看导出任务列表。

4. 选择要取消的导出任务，然后点击**操作**。

5. 从下拉列表中选择**取消**。注意，您只能取消处于**运行中**状态的导出任务。

</div>

<div label="CLI">

```shell
ticloud serverless export cancel -c <cluster-id> -e <export-id>
```

</div>
</SimpleTab>

## 导出速度

导出速度取决于您的[集群套餐](/tidb-cloud/select-cluster-tier.md#cluster-plans)。详情请参见下表：

| 套餐               | 导出速度       |
|:-------------------|:-------------------|
| 免费集群套餐      | 最高 25 MiB/s      |
| 可扩展集群套餐  | 最高 100 MiB/s     |

## 定价

导出服务在 beta 期间免费。您只需为成功或已取消的导出任务过程中产生的[请求单元（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit)付费。对于失败的导出任务，您将不会被收费。

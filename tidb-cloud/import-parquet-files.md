---
title: 从云存储导入 Apache Parquet 文件到 TiDB Cloud Dedicated
summary: 了解如何从 Amazon S3、GCS 或 Azure Blob Storage 导入 Apache Parquet 文件到 TiDB Cloud Dedicated。
---

# 从云存储导入 Apache Parquet 文件到 TiDB Cloud Dedicated

本文介绍如何从 Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS) 或 Azure Blob Storage 导入 Apache Parquet 文件到 TiDB Cloud Dedicated。你可以导入未压缩的 Parquet 文件或使用 [Google Snappy](https://github.com/google/snappy) 压缩的 Parquet 文件。不支持其他 Parquet 压缩编解码器。

## 限制

- 为确保数据一致性，TiDB Cloud 只允许将 Parquet 文件导入到空表中。要将数据导入到已包含数据的现有表中，你可以按照本文档将数据导入到临时空表中，然后使用 `INSERT SELECT` 语句将数据复制到目标现有表中。

- 如果 TiDB Cloud Dedicated 集群有 [changefeed](/tidb-cloud/changefeed-overview.md) 或启用了[时间点恢复](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)，则无法向该集群导入数据（**导入数据**按钮将被禁用），因为当前的数据导入功能使用[物理导入模式](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)。在此模式下，导入的数据不会生成变更日志，因此 changefeed 和时间点恢复无法检测到导入的数据。

## 步骤 1. 准备 Parquet 文件

> **注意：**
>
> 目前，TiDB Cloud 不支持导入包含以下任何数据类型的 Parquet 文件。如果要导入的 Parquet 文件包含此类数据类型，你需要首先使用[支持的数据类型](#支持的数据类型)（例如 `STRING`）重新生成 Parquet 文件。或者，你可以使用 AWS Glue 等服务轻松转换数据类型。
>
> - `LIST`
> - `NEST STRUCT`
> - `BOOL`
> - `ARRAY`
> - `MAP`

1. 如果 Parquet 文件大于 256 MB，建议将其拆分为较小的文件，每个文件大小约为 256 MB。

    TiDB Cloud 支持导入非常大的 Parquet 文件，但在处理大小约为 256 MB 的多个输入文件时性能最佳。这是因为 TiDB Cloud 可以并行处理多个文件，从而大大提高导入速度。

2. 按以下方式命名 Parquet 文件：

    - 如果 Parquet 文件包含整个表的所有数据，请按 `${db_name}.${table_name}.parquet` 格式命名文件，该文件在导入数据时会映射到 `${db_name}.${table_name}` 表。
    - 如果一个表的数据分散在多个 Parquet 文件中，请在这些 Parquet 文件后附加数字后缀。例如，`${db_name}.${table_name}.000001.parquet` 和 `${db_name}.${table_name}.000002.parquet`。数字后缀可以不连续，但必须按升序排列。你还需要在数字前添加额外的零，以确保所有后缀长度相同。

    > **注意：**
    >
    > - 如果在某些情况下无法按照上述规则更新 Parquet 文件名（例如，Parquet 文件链接也被你的其他程序使用），你可以保持文件名不变，并在[步骤 4](#步骤-4-将-parquet-文件导入到-tidb-cloud) 中使用**映射设置**将源数据导入到单个目标表中。
    > - Snappy 压缩文件必须采用[官方 Snappy 格式](https://github.com/google/snappy)。不支持其他变体的 Snappy 压缩。

## 步骤 2. 创建目标表架构

由于 Parquet 文件不包含架构信息，在将数据从 Parquet 文件导入到 TiDB Cloud 之前，你需要使用以下任一方法创建表架构：

- 方法 1：在 TiDB Cloud 中，为源数据创建目标数据库和表。

- 方法 2：在存放 Parquet 文件的 Amazon S3、GCS 或 Azure Blob Storage 目录中，按以下方式为源数据创建目标表架构文件：

    1. 为源数据创建数据库架构文件。

        如果你的 Parquet 文件遵循[步骤 1](#步骤-1-准备-parquet-文件) 中的命名规则，则数据导入时数据库架构文件是可选的。否则，数据库架构文件是必需的。

        每个数据库架构文件必须采用 `${db_name}-schema-create.sql` 格式，并包含一个 `CREATE DATABASE` DDL 语句。通过此文件，TiDB Cloud 将在导入数据时创建 `${db_name}` 数据库来存储你的数据。

        例如，如果你创建一个包含以下语句的 `mydb-scehma-create.sql` 文件，TiDB Cloud 将在导入数据时创建 `mydb` 数据库。

        {{< copyable "sql" >}}

        ```sql
        CREATE DATABASE mydb;
        ```

    2. 为源数据创建表架构文件。

        如果你没有在存放 Parquet 文件的 Amazon S3、GCS 或 Azure Blob Storage 目录中包含表架构文件，TiDB Cloud 在导入数据时将不会为你创建相应的表。

        每个表架构文件必须采用 `${db_name}.${table_name}-schema.sql` 格式，并包含一个 `CREATE TABLE` DDL 语句。通过此文件，TiDB Cloud 将在导入数据时在 `${db_name}` 数据库中创建 `${db_table}` 表。

        例如，如果你创建一个包含以下语句的 `mydb.mytable-schema.sql` 文件，TiDB Cloud 将在 `mydb` 数据库中创建 `mytable` 表。

        {{< copyable "sql" >}}

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **注意：**
        >
        > 每个 `${db_name}.${table_name}-schema.sql` 文件应该只包含一个 DDL 语句。如果文件包含多个 DDL 语句，只有第一个语句会生效。

## 步骤 3. 配置跨账户访问

要允许 TiDB Cloud 访问 Amazon S3 存储桶、GCS 存储桶或 Azure Blob Storage 容器中的 Parquet 文件，请执行以下操作之一：

- 如果你的 Parquet 文件位于 Amazon S3 中，[配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

    你可以使用 AWS 访问密钥或 Role ARN 访问你的存储桶。完成后，请记下访问密钥（包括访问密钥 ID 和密钥）或 Role ARN 值，因为你将在[步骤 4](#步骤-4-将-parquet-文件导入到-tidb-cloud) 中需要它。

- 如果你的 Parquet 文件位于 GCS 中，[配置 GCS 访问](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)。

- 如果你的 Parquet 文件位于 Azure Blob Storage 中，[配置 Azure Blob Storage 访问](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

## 步骤 4. 将 Parquet 文件导入到 TiDB Cloud

要将 Parquet 文件导入到 TiDB Cloud，请执行以下步骤：

<SimpleTab>
<div label="Amazon S3">

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**。

3. 在**从 Amazon S3 导入数据**页面上，提供以下信息：

    - **包含架构文件**：如果源文件夹包含目标表架构文件（如 `${db_name}-schema-create.sql`），选择**是**。否则，选择**否**。
    - **数据格式**：选择 **Parquet**。
    - **文件夹 URI**：以 `s3://[bucket_name]/[data_source_folder]/` 格式输入源文件夹 URI。路径必须以 `/` 结尾。例如，`s3://sampledata/ingest/`。
    - **存储桶访问**：你可以使用 AWS IAM 角色 ARN 或 AWS 访问密钥访问你的存储桶。
        - **AWS Role ARN**（推荐）：输入 AWS IAM 角色 ARN 值。如果你还没有存储桶的 IAM 角色，可以通过点击**点击此处使用 AWS CloudFormation 创建新角色**并按照屏幕上的说明使用提供的 AWS CloudFormation 模板创建。或者，你可以手动为存储桶创建 IAM 角色 ARN。
        - **AWS 访问密钥**：输入 AWS 访问密钥 ID 和 AWS 密钥。
        - 有关两种方法的详细说明，请参见[配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

4. 点击**连接**。

5. 在**目标**部分，选择目标数据库和表。

    导入多个文件时，你可以使用**高级设置** > **映射设置**来自定义各个目标表与其对应 Parquet 文件的映射。对于每个目标数据库和表：

    - **目标数据库**：从列表中选择相应的数据库名称。
    - **目标表**：从列表中选择相应的表名称。
    - **源文件 URI 和名称**：输入源文件的完整 URI，包括文件夹和文件名，确保其格式为 `s3://[bucket_name]/[data_source_folder]/[file_name].parquet`。例如，`s3://sampledata/ingest/TableName.01.parquet`。你也可以使用通配符（`?` 和 `*`）匹配多个文件。例如：
        - `s3://[bucket_name]/[data_source_folder]/my-data1.parquet`：`[data_source_folder]` 中名为 `my-data1.parquet` 的单个 Parquet 文件将被导入到目标表中。
        - `s3://[bucket_name]/[data_source_folder]/my-data?.parquet`：`[data_source_folder]` 中以 `my-data` 开头后跟一个字符的所有 Parquet 文件（如 `my-data1.parquet` 和 `my-data2.parquet`）将被导入到同一个目标表中。
        - `s3://[bucket_name]/[data_source_folder]/my-data*.parquet`：`[data_source_folder]` 中以 `my-data` 开头的所有 Parquet 文件（如 `my-data10.parquet` 和 `my-data100.parquet`）将被导入到同一个目标表中。

6. 点击**开始导入**。

7. 当导入进度显示**已完成**时，检查导入的表。

</div>

<div label="Google Cloud">

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**。

3. 在**从 GCS 导入数据**页面上，为源 Parquet 文件提供以下信息：

    - **包含架构文件**：如果源文件夹包含目标表架构文件（如 `${db_name}-schema-create.sql`），选择**是**。否则，选择**否**。
    - **数据格式**：选择 **Parquet**。
    - **文件夹 URI**：以 `gs://[bucket_name]/[data_source_folder]/` 格式输入源文件夹 URI。路径必须以 `/` 结尾。例如，`gs://sampledata/ingest/`。
    - **Google Cloud 服务账号 ID**：TiDB Cloud 在此页面上提供唯一的服务账号 ID（如 `example-service-account@your-project.iam.gserviceaccount.com`）。你必须在 Google Cloud 项目中为你的 GCS 存储桶授予此服务账号 ID 必要的 IAM 权限（如 "Storage Object Viewer"）。更多信息，请参见[配置 GCS 访问](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)。

4. 点击**连接**。

5. 在**目标**部分，选择目标数据库和表。

    导入多个文件时，你可以使用**高级设置** > **映射设置**来自定义各个目标表与其对应 Parquet 文件的映射。对于每个目标数据库和表：

    - **目标数据库**：从列表中选择相应的数据库名称。
    - **目标表**：从列表中选择相应的表名称。
    - **源文件 URI 和名称**：输入源文件的完整 URI，包括文件夹和文件名，确保其格式为 `gs://[bucket_name]/[data_source_folder]/[file_name].parquet`。例如，`gs://sampledata/ingest/TableName.01.parquet`。你也可以使用通配符（`?` 和 `*`）匹配多个文件。例如：
        - `gs://[bucket_name]/[data_source_folder]/my-data1.parquet`：`[data_source_folder]` 中名为 `my-data1.parquet` 的单个 Parquet 文件将被导入到目标表中。
        - `gs://[bucket_name]/[data_source_folder]/my-data?.parquet`：`[data_source_folder]` 中以 `my-data` 开头后跟一个字符的所有 Parquet 文件（如 `my-data1.parquet` 和 `my-data2.parquet`）将被导入到同一个目标表中。
        - `gs://[bucket_name]/[data_source_folder]/my-data*.parquet`：`[data_source_folder]` 中以 `my-data` 开头的所有 Parquet 文件（如 `my-data10.parquet` 和 `my-data100.parquet`）将被导入到同一个目标表中。

6. 点击**开始导入**。

7. 当导入进度显示**已完成**时，检查导入的表。

</div>

<div label="Azure Blob Storage">

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**。

3. 在**从 Azure Blob Storage 导入数据**页面上，提供以下信息：

    - **包含架构文件**：如果源文件夹包含目标表架构文件（如 `${db_name}-schema-create.sql`），选择**是**。否则，选择**否**。
    - **数据格式**：选择 **Parquet**。
    - **文件夹 URI**：使用格式 `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/` 输入源文件所在的 Azure Blob Storage URI。路径必须以 `/` 结尾。例如，`https://myaccount.blob.core.windows.net/mycontainer/data-ingestion/`。
    - **SAS 令牌**：输入账户 SAS 令牌以允许 TiDB Cloud 访问你的 Azure Blob Storage 容器中的源文件。如果你还没有，可以通过点击**点击此处使用 Azure ARM 模板创建新令牌**并按照屏幕上的说明使用提供的 Azure ARM 模板创建。或者，你可以手动创建账户 SAS 令牌。更多信息，请参见[配置 Azure Blob Storage 访问](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

4. 点击**连接**。

5. 在**目标**部分，选择目标数据库和表。

    导入多个文件时，你可以使用**高级设置** > **映射设置**来自定义各个目标表与其对应 Parquet 文件的映射。对于每个目标数据库和表：

    - **目标数据库**：从列表中选择相应的数据库名称。
    - **目标表**：从列表中选择相应的表名称。
    - **源文件 URI 和名称**：输入源文件的完整 URI，包括文件夹和文件名，确保其格式为 `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/[file_name].parquet`。例如，`https://myaccount.blob.core.windows.net/mycontainer/data-ingestion/TableName.01.parquet`。你也可以使用通配符（`?` 和 `*`）匹配多个文件。例如：
        - `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/my-data1.parquet`：`[data_source_folder]` 中名为 `my-data1.parquet` 的单个 Parquet 文件将被导入到目标表中。
        - `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/my-data?.parquet`：`[data_source_folder]` 中以 `my-data` 开头后跟一个字符的所有 Parquet 文件（如 `my-data1.parquet` 和 `my-data2.parquet`）将被导入到同一个目标表中。
        - `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/my-data*.parquet`：`[data_source_folder]` 中以 `my-data` 开头的所有 Parquet 文件（如 `my-data10.parquet` 和 `my-data100.parquet`）将被导入到同一个目标表中。

6. 点击**开始导入**。

7. 当导入进度显示**已完成**时，检查导入的表。

</div>

</SimpleTab>

运行导入任务时，如果检测到任何不支持或无效的转换，TiDB Cloud 会自动终止导入作业并报告导入错误。你可以在**状态**字段中查看详细信息。

如果遇到导入错误，请执行以下操作：

1. 删除部分导入的表。
2. 检查表架构文件。如果有任何错误，请更正表架构文件。
3. 检查 Parquet 文件中的数据类型。

    如果 Parquet 文件包含任何不支持的数据类型（例如 `NEST STRUCT`、`ARRAY` 或 `MAP`），你需要使用[支持的数据类型](#支持的数据类型)（例如 `STRING`）重新生成 Parquet 文件。

4. 重试导入任务。

## 支持的数据类型

下表列出了可以导入到 TiDB Cloud 的支持的 Parquet 数据类型。

| Parquet 基本类型 | Parquet 逻辑类型 | TiDB 或 MySQL 中的类型 |
|---|---|---|
| DOUBLE | DOUBLE | DOUBLE<br />FLOAT |
| FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0) | BIGINT UNSIGNED |
| FIXED_LEN_BYTE_ARRAY(N) | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT32 | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT32 | N/A | INT<br />MEDIUMINT<br />YEAR |
| INT64 | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT64 | N/A | BIGINT<br />INT UNSIGNED<br />MEDIUMINT UNSIGNED |
| INT64 | TIMESTAMP_MICROS | DATETIME<br />TIMESTAMP |
| BYTE_ARRAY | N/A | BINARY<br />BIT<br />BLOB<br />CHAR<br />LINESTRING<br />LONGBLOB<br />MEDIUMBLOB<br />MULTILINESTRING<br />TINYBLOB<br />VARBINARY |
| BYTE_ARRAY | STRING | ENUM<br />DATE<br />DECIMAL<br />GEOMETRY<br />GEOMETRYCOLLECTION<br />JSON<br />LONGTEXT<br />MEDIUMTEXT<br />MULTIPOINT<br />MULTIPOLYGON<br />NUMERIC<br />POINT<br />POLYGON<br />SET<br />TEXT<br />TIME<br />TINYTEXT<br />VARCHAR |
| SMALLINT | N/A | INT32 |
| SMALLINT UNSIGNED | N/A | INT32 |
| TINYINT | N/A | INT32 |
| TINYINT UNSIGNED | N/A | INT32 |

## 故障排除

### 解决数据导入期间的警告

点击**开始导入**后，如果看到类似 `can't find the corresponding source files` 的警告消息，请通过提供正确的源文件、按照[数据导入命名约定](/tidb-cloud/naming-conventions-for-data-import.md)重命名现有文件或使用**高级设置**进行更改来解决此问题。

解决这些问题后，你需要重新导入数据。

### 导入的表中行数为零

导入进度显示**已完成**后，检查导入的表。如果行数为零，则表示没有数据文件与你输入的存储桶 URI 匹配。在这种情况下，请通过提供正确的源文件、按照[数据导入命名约定](/tidb-cloud/naming-conventions-for-data-import.md)重命名现有文件或使用**高级设置**进行更改来解决此问题。之后，重新导入这些表。

---
title: 从 Amazon S3、GCS、Azure Blob Storage 或阿里云 OSS 导入 CSV 文件到 TiDB Cloud Serverless
summary: 了解如何从 Amazon S3、GCS、Azure Blob Storage 或阿里云对象存储服务（OSS）导入 CSV 文件到 TiDB Cloud Serverless。
---

# 从 Amazon S3、GCS、Azure Blob Storage 或阿里云 OSS 导入 CSV 文件到 TiDB Cloud Serverless

本文档描述如何从 Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS)、Azure Blob Storage 或阿里云对象存储服务（OSS）导入 CSV 文件到 TiDB Cloud Serverless。

## 限制

- 为确保数据一致性，TiDB Cloud Serverless 仅允许将 CSV 文件导入到空表中。如果要将数据导入到已包含数据的现有表中，你可以按照本文档将数据导入到临时空表中，然后使用 `INSERT SELECT` 语句将数据复制到目标现有表中。

## 步骤 1. 准备 CSV 文件

1. 如果 CSV 文件大于 256 MB，建议将其拆分为较小的文件，每个文件大小约为 256 MB。

    TiDB Cloud Serverless 支持导入非常大的 CSV 文件，但在处理大小约为 256 MB 的多个输入文件时性能最佳。这是因为 TiDB Cloud Serverless 可以并行处理多个文件，从而大大提高导入速度。

2. 按以下方式命名 CSV 文件：

    - 如果 CSV 文件包含整个表的所有数据，请按 `${db_name}.${table_name}.csv` 格式命名文件，导入数据时将映射到 `${db_name}.${table_name}` 表。
    - 如果一个表的数据分散在多个 CSV 文件中，请在这些 CSV 文件后附加数字后缀。例如，`${db_name}.${table_name}.000001.csv` 和 `${db_name}.${table_name}.000002.csv`。数字后缀可以不连续但必须按升序排列。你还需要在数字前添加额外的零以确保所有后缀长度相同。
    - TiDB Cloud Serverless 支持导入以下格式的压缩文件：`.gzip`、`.gz`、`.zstd`、`.zst` 和 `.snappy`。如果要导入压缩的 CSV 文件，请按 `${db_name}.${table_name}.${suffix}.csv.${compress}` 格式命名文件，其中 `${suffix}` 是可选的，可以是任何整数，如 '000001'。例如，如果要将 `trips.000001.csv.gz` 文件导入到 `bikeshare.trips` 表，你需要将文件重命名为 `bikeshare.trips.000001.csv.gz`。

    > **注意：**
    >
    > - 为获得更好的性能，建议将每个压缩文件的大小限制在 100 MiB 以内。
    > - Snappy 压缩文件必须采用[官方 Snappy 格式](https://github.com/google/snappy)。不支持其他变体的 Snappy 压缩。
    > - 对于未压缩的文件，如果在某些情况下无法按照上述规则更新 CSV 文件名（例如，CSV 文件链接也被其他程序使用），你可以保持文件名不变，并在[步骤 4](#步骤-4-将-csv-文件导入到-tidb-cloud-serverless) 中使用**映射设置**将源数据导入到单个目标表。

## 步骤 2. 创建目标表架构

由于 CSV 文件不包含架构信息，在将数据从 CSV 文件导入到 TiDB Cloud Serverless 之前，你需要使用以下任一方法创建表架构：

- 方法 1：在 TiDB Cloud Serverless 中，为源数据创建目标数据库和表。

- 方法 2：在存放 CSV 文件的 Amazon S3、GCS、Azure Blob Storage 或阿里云对象存储服务目录中，按以下方式为源数据创建目标表架构文件：

    1. 为源数据创建数据库架构文件。

        如果你的 CSV 文件遵循[步骤 1](#步骤-1-准备-csv-文件) 中的命名规则，则数据库架构文件对数据导入是可选的。否则，数据库架构文件是必需的。

        每个数据库架构文件必须采用 `${db_name}-schema-create.sql` 格式，并包含一个 `CREATE DATABASE` DDL 语句。通过此文件，TiDB Cloud Serverless 将在导入数据时创建 `${db_name}` 数据库来存储数据。

        例如，如果你创建一个包含以下语句的 `mydb-scehma-create.sql` 文件，TiDB Cloud Serverless 将在导入数据时创建 `mydb` 数据库。

        ```sql
        CREATE DATABASE mydb;
        ```

    2. 为源数据创建表架构文件。

        如果你没有在存放 CSV 文件的 Amazon S3、GCS、Azure Blob Storage 或阿里云对象存储服务目录中包含表架构文件，TiDB Cloud Serverless 在导入数据时将不会为你创建相应的表。

        每个表架构文件必须采用 `${db_name}.${table_name}-schema.sql` 格式，并包含一个 `CREATE TABLE` DDL 语句。通过此文件，TiDB Cloud Serverless 将在导入数据时在 `${db_name}` 数据库中创建 `${db_table}` 表。

        例如，如果你创建一个包含以下语句的 `mydb.mytable-schema.sql` 文件，TiDB Cloud Serverless 将在导入数据时在 `mydb` 数据库中创建 `mytable` 表。

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

要允许 TiDB Cloud Serverless 访问 Amazon S3、GCS、Azure Blob Storage 或阿里云对象存储服务存储桶中的 CSV 文件，请执行以下操作之一：

- 如果你的 CSV 文件位于 Amazon S3 中，[为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md#配置-amazon-s3-访问)。

    你可以使用 AWS 访问密钥或 Role ARN 来访问存储桶。完成后，请记下访问密钥（包括访问密钥 ID 和密钥）或 Role ARN 值，因为你将在[步骤 4](#步骤-4-将-csv-文件导入到-tidb-cloud-serverless) 中需要它。

- 如果你的 CSV 文件位于 GCS 中，[为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md#配置-gcs-访问)。

- 如果你的 CSV 文件位于 Azure Blob Storage 中，[为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md#配置-azure-blob-storage-访问)。

- 如果你的 CSV 文件位于阿里云对象存储服务（OSS）中，[为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md#配置阿里云对象存储服务-oss-访问)。

## 步骤 4. 将 CSV 文件导入到 TiDB Cloud Serverless

要将 CSV 文件导入到 TiDB Cloud Serverless，请执行以下步骤：

<SimpleTab>
<div label="Amazon S3">

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的 [**集群**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**，然后点击 **Amazon S3**。

3. 在**从 Amazon S3 导入数据**页面，为源 CSV 文件提供以下信息：

    - **导入文件数量**：根据需要选择**单个文件**或**多个文件**。
    - **包含架构文件**：此字段仅在导入多个文件时可见。如果源文件夹包含目标表架构，选择**是**。否则，选择**否**。
    - **数据格式**：选择 **CSV**。
    - **文件 URI** 或**文件夹 URI**：
        - 导入单个文件时，按以下格式输入源文件 URI 和名称 `s3://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`s3://sampledata/ingest/TableName.01.csv`。
        - 导入多个文件时，按以下格式输入源文件 URI 和名称 `s3://[bucket_name]/[data_source_folder]/`。例如，`s3://sampledata/ingest/`。
    - **存储桶访问**：你可以使用 AWS Role ARN 或 AWS 访问密钥来访问存储桶。更多信息，请参见[配置 Amazon S3 访问](/tidb-cloud/serverless-external-storage.md#配置-amazon-s3-访问)。
        - **AWS Role ARN**：输入 AWS Role ARN 值。
        - **AWS 访问密钥**：输入 AWS 访问密钥 ID 和 AWS 密钥。

4. 点击**连接**。

5. 在**目标**部分，选择目标数据库和表。

    导入多个文件时，你可以使用**高级设置** > **映射设置**为每个目标表及其对应的 CSV 文件定义自定义映射规则。之后，将使用提供的自定义映射规则重新扫描数据源文件。

    在**源文件 URI 和名称**中输入源文件 URI 和名称时，确保其格式为 `s3://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`s3://sampledata/ingest/TableName.01.csv`。

    你还可以使用通配符来匹配源文件。例如：

    - `s3://[bucket_name]/[data_source_folder]/my-data?.csv`：该文件夹中以 `my-data` 开头后跟一个字符的所有 CSV 文件（如 `my-data1.csv` 和 `my-data2.csv`）将导入到同一个目标表中。

    - `s3://[bucket_name]/[data_source_folder]/my-data*.csv`：该文件夹中以 `my-data` 开头的所有 CSV 文件将导入到同一个目标表中。

    注意，仅支持 `?` 和 `*`。

    > **注意：**
    >
    > URI 必须包含数据源文件夹。

6. 点击**开始导入**。

7. 当导入进度显示**已完成**时，检查导入的表。

</div>

<div label="Google Cloud">

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的 [**集群**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**，然后点击 **Google Cloud Storage**。

3. 在**从 Google Cloud Storage 导入数据**页面，为源 CSV 文件提供以下信息：

    - **导入文件数量**：根据需要选择**单个文件**或**多个文件**。
    - **包含架构文件**：此字段仅在导入多个文件时可见。如果源文件夹包含目标表架构，选择**是**。否则，选择**否**。
    - **数据格式**：选择 **CSV**。
    - **文件 URI** 或**文件夹 URI**：
        - 导入单个文件时，按以下格式输入源文件 URI 和名称 `[gcs|gs]://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`[gcs|gs]://sampledata/ingest/TableName.01.csv`。
        - 导入多个文件时，按以下格式输入源文件 URI 和名称 `[gcs|gs]://[bucket_name]/[data_source_folder]/`。例如，`[gcs|gs]://sampledata/ingest/`。
    - **存储桶访问**：你可以使用服务账号密钥来访问存储桶。更多信息，请参见[配置 GCS 访问](/tidb-cloud/serverless-external-storage.md#配置-gcs-访问)。

4. 点击**连接**。

5. 在**目标**部分，选择目标数据库和表。

    导入多个文件时，你可以使用**高级设置** > **映射设置**为每个目标表及其对应的 CSV 文件定义自定义映射规则。之后，将使用提供的自定义映射规则重新扫描数据源文件。

    在**源文件 URI 和名称**中输入源文件 URI 和名称时，确保其格式为 `[gcs|gs]://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`[gcs|gs]://sampledata/ingest/TableName.01.csv`。

    你还可以使用通配符来匹配源文件。例如：

    - `[gcs|gs]://[bucket_name]/[data_source_folder]/my-data?.csv`：该文件夹中以 `my-data` 开头后跟一个字符的所有 CSV 文件（如 `my-data1.csv` 和 `my-data2.csv`）将导入到同一个目标表中。

    - `[gcs|gs]://[bucket_name]/[data_source_folder]/my-data*.csv`：该文件夹中以 `my-data` 开头的所有 CSV 文件将导入到同一个目标表中。

    注意，仅支持 `?` 和 `*`。

    > **注意：**
    >
    > URI 必须包含数据源文件夹。

6. 点击**开始导入**。

7. 当导入进度显示**已完成**时，检查导入的表。

</div>

<div label="Azure Blob Storage">

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的 [**集群**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**，然后点击 **Azure Blob Storage**。

3. 在**从 Azure Blob Storage 导入数据**页面，为源 CSV 文件提供以下信息：

    - **导入文件数量**：根据需要选择**单个文件**或**多个文件**。
    - **包含架构文件**：此字段仅在导入多个文件时可见。如果源文件夹包含目标表架构，选择**是**。否则，选择**否**。
    - **数据格式**：选择 **CSV**。
    - **文件 URI** 或**文件夹 URI**：
        - 导入单个文件时，按以下格式输入源文件 URI 和名称 `[azure|https]://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`[azure|https]://sampledata/ingest/TableName.01.csv`。
        - 导入多个文件时，按以下格式输入源文件 URI 和名称 `[azure|https]://[bucket_name]/[data_source_folder]/`。例如，`[azure|https]://sampledata/ingest/`。
    - **存储桶访问**：你可以使用共享访问签名（SAS）令牌来访问存储桶。更多信息，请参见[配置 Azure Blob Storage 访问](/tidb-cloud/serverless-external-storage.md#配置-azure-blob-storage-访问)。

4. 点击**连接**。

5. 在**目标**部分，选择目标数据库和表。

    导入多个文件时，你可以使用**高级设置** > **映射设置**为每个目标表及其对应的 CSV 文件定义自定义映射规则。之后，将使用提供的自定义映射规则重新扫描数据源文件。

    在**源文件 URI 和名称**中输入源文件 URI 和名称时，确保其格式为 `[azure|https]://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`[azure|https]://sampledata/ingest/TableName.01.csv`。

    你还可以使用通配符来匹配源文件。例如：

    - `[azure|https]://[bucket_name]/[data_source_folder]/my-data?.csv`：该文件夹中以 `my-data` 开头后跟一个字符的所有 CSV 文件（如 `my-data1.csv` 和 `my-data2.csv`）将导入到同一个目标表中。

    - `[azure|https]://[bucket_name]/[data_source_folder]/my-data*.csv`：该文件夹中以 `my-data` 开头的所有 CSV 文件将导入到同一个目标表中。

    注意，仅支持 `?` 和 `*`。

    > **注意：**
    >
    > URI 必须包含数据源文件夹。

6. 点击**开始导入**。

7. 当导入进度显示**已完成**时，检查导入的表。

</div>

<div label="阿里云对象存储服务（OSS）">

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的 [**集群**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**，然后点击**阿里云 OSS**。

3. 在**从阿里云 OSS 导入数据**页面，为源 CSV 文件提供以下信息：

    - **导入文件数量**：根据需要选择**单个文件**或**多个文件**。
    - **包含架构文件**：此字段仅在导入多个文件时可见。如果源文件夹包含目标表架构，选择**是**。否则，选择**否**。
    - **数据格式**：选择 **CSV**。
    - **文件 URI** 或**文件夹 URI**：
        - 导入单个文件时，按以下格式输入源文件 URI 和名称 `oss://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`oss://sampledata/ingest/TableName.01.csv`。
        - 导入多个文件时，按以下格式输入源文件 URI 和名称 `oss://[bucket_name]/[data_source_folder]/`。例如，`oss://sampledata/ingest/`。
    - **存储桶访问**：你可以使用 AccessKey 对来访问存储桶。更多信息，请参见[配置阿里云对象存储服务（OSS）访问](/tidb-cloud/serverless-external-storage.md#配置阿里云对象存储服务-oss-访问)。

4. 点击**连接**。

5. 在**目标**部分，选择目标数据库和表。

    导入多个文件时，你可以使用**高级设置** > **映射设置**为每个目标表及其对应的 CSV 文件定义自定义映射规则。之后，将使用提供的自定义映射规则重新扫描数据源文件。

    在**源文件 URI 和名称**中输入源文件 URI 和名称时，确保其格式为 `oss://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`oss://sampledata/ingest/TableName.01.csv`。

    你还可以使用通配符来匹配源文件。例如：

    - `oss://[bucket_name]/[data_source_folder]/my-data?.csv`：该文件夹中以 `my-data` 开头后跟一个字符的所有 CSV 文件（如 `my-data1.csv` 和 `my-data2.csv`）将导入到同一个目标表中。

    - `oss://[bucket_name]/[data_source_folder]/my-data*.csv`：该文件夹中以 `my-data` 开头的所有 CSV 文件将导入到同一个目标表中。

    注意，仅支持 `?` 和 `*`。

    > **注意：**
    >
    > URI 必须包含数据源文件夹。

6. 点击**开始导入**。

7. 当导入进度显示**已完成**时，检查导入的表。

</div>

</SimpleTab>

运行导入任务时，如果检测到任何不支持或无效的转换，TiDB Cloud Serverless 会自动终止导入作业并报告导入错误。

如果遇到导入错误，请执行以下操作：

1. 删除部分导入的表。
2. 检查表架构文件。如果有任何错误，请更正表架构文件。
3. 检查 CSV 文件中的数据类型。
4. 重新尝试导入任务。

## 故障排除

### 解决数据导入过程中的警告

点击**开始导入**后，如果看到类似 `can't find the corresponding source files` 的警告消息，请通过提供正确的源文件、根据[数据导入命名约定](/tidb-cloud/naming-conventions-for-data-import.md)重命名现有文件或使用**高级设置**进行更改来解决此问题。

解决这些问题后，你需要重新导入数据。

### 导入的表中行数为零

导入进度显示**已完成**后，检查导入的表。如果行数为零，表示没有数据文件与你输入的存储桶 URI 匹配。在这种情况下，请通过提供正确的源文件、根据[数据导入命名约定](/tidb-cloud/naming-conventions-for-data-import.md)重命名现有文件或使用**高级设置**进行更改来解决此问题。之后，重新导入这些表。

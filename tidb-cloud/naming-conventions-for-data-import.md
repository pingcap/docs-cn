---
title: 数据导入的命名规范
summary: 了解 CSV、Parquet、Aurora Snapshot 和 SQL 文件在数据导入过程中的命名规范。
---

# 数据导入的命名规范

你可以将以下格式的文件导入到 TiDB Cloud：CSV、Parquet、Aurora Snapshot 和 SQL。为确保数据成功导入，你需要准备以下两类文件：

- **模式文件**。准备数据库模式文件（可选）和表模式文件，两者都是 SQL 格式（`.sql`）。如果未提供表模式文件，你需要提前在目标数据库中手动创建相应的表。
- **数据文件**。准备符合导入数据命名规范的数据文件。如果数据文件名称无法满足要求，建议使用[**文件模式**](#文件模式)执行导入任务。否则，导入任务将无法扫描到你想要导入的数据文件。

## 模式文件的命名规范

本节描述数据库和表模式文件的命名规范。对于以下所有类型的源文件（CSV、Parquet、Aurora Snapshot 和 SQL），模式文件的命名规范都是相同的。

模式文件的命名规范如下：

- 数据库模式文件（可选）：`${db_name}-schema-create.sql`
- 表模式文件：`${db_name}.${table_name}-schema.sql`

以下是数据库模式文件的示例：

- 名称：`import_db-schema-create.sql`
- 文件内容：

    ```sql
    CREATE DATABASE import_db;
    ```

以下是表模式文件的示例：

- 名称：`import_db.test_table-schema.sql`
- 文件内容：

    ```sql
    CREATE TABLE test_table (
        id INTEGER PRIMARY KEY,
        val VARCHAR(255)
    );
    ```

## 数据文件的命名规范

本节描述数据文件的命名规范。根据源文件的类型，数据文件的命名规范有所不同。

### CSV

导入 CSV 文件时，数据文件的命名规范如下：

`${db_name}.${table_name}${suffix}.csv.${compress}`

`${suffix}` 是可选的，可以是以下格式之一，其中 *`xxx`* 可以是任何数字：

- *`.xxx`*，例如 `.01`
- *`._xxx_xxx_xxx`*，例如 `._0_0_01`
- *`_xxx_xxx_xxx`*，例如 `_0_0_01`

`${compress}` 是压缩格式，是可选的。TiDB Cloud 支持以下格式：`.gzip`、`.gz`、`.zstd`、`.zst` 和 `.snappy`。

例如，以下所有文件的目标数据库和表都是 `import_db` 和 `test_table`：

- `import_db.test_table.csv`
- `import_db.test_table.01.csv`
- `import_db.test_table._0_0_01.csv`
- `import_db.test_table_0_0_01.csv`
- `import_db.test_table_0_0_01.csv.gz`

> **注意：**
>
> Snappy 压缩文件必须是[官方 Snappy 格式](https://github.com/google/snappy)。不支持其他变体的 Snappy 压缩。

### Parquet

导入 Parquet 文件时，数据文件的命名规范如下：

`${db_name}.${table_name}${suffix}.parquet`（`${suffix}` 是可选的）

例如：

- `import_db.test_table.parquet`
- `import_db.test_table.01.parquet`

### Aurora Snapshot

对于 Aurora Snapshot 文件，`${db_name}.${table_name}/` 文件夹中所有带有 `.parquet` 后缀的文件都符合命名规范。数据文件名可以包含由"a-z、0-9、-、_、."组成的任何前缀和后缀 ".parquet"。

例如：

- `import_db.test_table/mydata.parquet`
- `import_db.test_table/part001/mydata.parquet`
- `import_db.test_table/part002/mydata-part002.parquet`

### SQL

导入 SQL 文件时，数据文件的命名规范如下：

`${db_name}.${table_name}${suffix}.sql.${compress}`

`${suffix}` 是可选的，可以是以下格式之一，其中 *`xxx`* 可以是任何数字：

- *`.xxx`*，例如 `.01`
- *`._xxx_xxx_xxx`*，例如 `._0_0_01`
- *`_xxx_xxx_xxx`*，例如 `_0_0_01`

`${compress}` 是压缩格式，是可选的。TiDB Cloud 支持以下格式：`.gzip`、`.gz`、`.zstd`、`.zst` 和 `.snappy`。

例如：

- `import_db.test_table.sql`
- `import_db.test_table.01.sql`
- `import_db.test_table.01.sql.gz`

如果 SQL 文件是通过默认配置的 TiDB Dumpling 导出的，则默认符合命名规范。

> **注意：**
>
> Snappy 压缩文件必须是[官方 Snappy 格式](https://github.com/google/snappy)。不支持其他变体的 Snappy 压缩。

## 文件模式

如果 CSV 或 Parquet 的源数据文件不符合命名规范，你可以使用文件模式功能建立源数据文件与目标表之间的名称映射关系。此功能不支持 Aurora Snapshot 和 SQL 数据文件。

- 对于 CSV 文件，请参阅[步骤 4. 将 CSV 文件导入到 TiDB Cloud](/tidb-cloud/import-csv-files.md#步骤-4-将-csv-文件导入到-tidb-cloud) 中的**高级设置** > **映射设置**
- 对于 Parquet 文件，请参阅[步骤 4. 将 Parquet 文件导入到 TiDB Cloud](/tidb-cloud/import-parquet-files.md#步骤-4-将-parquet-文件导入到-tidb-cloud) 中的**高级设置** > **映射设置**

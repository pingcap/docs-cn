---
title: ticloud serverless export create
summary: `ticloud serverless export create` 命令的参考。
---

# ticloud serverless export create

从 TiDB Cloud Serverless 集群导出数据：

```shell
ticloud serverless export create [flags]
```

## 示例

在交互模式下从 TiDB Cloud Serverless 集群导出数据：

```shell
ticloud serverless export create
```

在非交互模式下从 TiDB Cloud Serverless 集群导出数据到本地文件：

```shell
ticloud serverless export create -c <cluster-id> --filter <database.table>
```

在非交互模式下从 TiDB Cloud Serverless 集群导出数据到 Amazon S3：

```shell
ticloud serverless export create -c <cluster-id> --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter <database.table>
```

在非交互模式下从 TiDB Cloud Serverless 集群导出数据到 Google Cloud Storage：

```shell
ticloud serverless export create -c <cluster-id> --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter <database.table>
```

在非交互模式下从 TiDB Cloud Serverless 集群导出数据到 Azure Blob Storage：

```shell
ticloud serverless export create -c <cluster-id> --azblob.uri <uri> --azblob.sas-token <sas-token> --filter <database.table>
```

在非交互模式下从 TiDB Cloud Serverless 集群导出数据到阿里云 OSS：

```shell
ticloud serverless export create -c <cluster-id> --oss.uri <uri> --oss.access-key-id <access-key-id> --oss.access-key-secret <access-key-secret> --filter <database.table>
```

在非交互模式下导出数据到 Parquet 文件并使用 `SNAPPY` 压缩：

```shell
ticloud serverless export create -c <cluster-id> --file-type parquet --parquet.compression SNAPPY --filter <database.table>
```

在非交互模式下使用 SQL 语句导出数据：

```shell
ticloud serverless export create -c <cluster-id> --sql 'select * from database.table'
```

## 参数标志

在非交互模式下，你需要手动输入必需的参数标志。在交互模式下，你可以按照 CLI 提示填写它们。

| 参数标志                         | 描述                                                                                                                                                                   | 是否必需 | 说明                                                 |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string          | 指定要从中导出数据的集群 ID。                                                                                                          | 是      | 仅在非交互模式下有效。                  |
| --file-type string               | 指定导出文件类型。可选值为 ["SQL" "CSV" "PARQUET"]。（默认为 "CSV"）                                                                                                         | 否       | 仅在非交互模式下有效。                  |
| --target-type string             | 指定导出目标。可选值为 [`"LOCAL"` `"S3"` `"GCS"` `"AZURE_BLOB"` `"OSS"`]。默认值为 `"LOCAL"`。                                                                                                | 否       | 仅在非交互模式下有效。                  |
| --s3.uri string                  | 指定 S3 URI，格式为 `s3://<bucket>/<file-path>`。当目标类型为 S3 时必需。                                                                                            | 否       | 仅在非交互模式下有效。                  |
| --s3.access-key-id string        | 指定 Amazon S3 的访问密钥 ID。你只需要设置 s3.role-arn 或 [s3.access-key-id, s3.secret-access-key] 其中之一。                                                        | 否       | 仅在非交互模式下有效。                  |
| --s3.secret-access-key string    | 指定 Amazon S3 的秘密访问密钥。你只需要设置 s3.role-arn 或 [s3.access-key-id, s3.secret-access-key] 其中之一。                                                   | 否       | 仅在非交互模式下有效。                  |
| --s3.role-arn string             | 指定 Amazon S3 的角色 ARN。你只需要设置 s3.role-arn 或 [s3.access-key-id, s3.secret-access-key] 其中之一。                                                             | 否       | 仅在非交互模式下有效。                  |
| --gcs.uri string                 | 指定 GCS URI，格式为 `gcs://<bucket>/<file-path>`。当目标类型为 GCS 时必需。                                                                                         | 否       | 仅在非交互模式下有效。                  |
| --gcs.service-account-key string | 指定 GCS 的 base64 编码服务账号密钥。                                                                                                                                | 否       | 仅在非交互模式下有效。                  |
| --azblob.uri string              | 指定 Azure Blob URI，格式为 `azure://<account>.blob.core.windows.net/<container>/<file-path>`。当目标类型为 AZURE_BLOB 时必需。                                      | 否       | 仅在非交互模式下有效。                  |
| --azblob.sas-token string        | 指定 Azure Blob 的 SAS 令牌。                                                                                                                                                  | 否       | 仅在非交互模式下有效。                  |
| --oss.uri string                 | 指定阿里云 OSS URI，格式为 `oss://<bucket>/<file-path>`。当导出 `target-type` 为 `"OSS"` 时必需。                                                                                                                                            | 否       | 仅在非交互模式下有效。                  |
| --oss.access-key-id string       | 指定访问阿里云 OSS 的 AccessKey ID。                                                                                                                                     | 否       | 仅在非交互模式下有效。                  |
| --oss.access-key-secret string   | 指定访问阿里云 OSS 的 AccessKey Secret。                                                                                                                                     | 否       | 仅在非交互模式下有效。                   |
| --csv.delimiter string           | 指定 CSV 文件中字符串类型变量的分隔符。（默认为 "\""）                                                                                                         | 否       | 仅在非交互模式下有效。                  |
| --csv.null-value string          | 指定 CSV 文件中空值的表示方式。（默认为 "\\N"）                                                                                                                   | 否       | 仅在非交互模式下有效。                  |
| --csv.separator string           | 指定 CSV 文件中每个值的分隔符。（默认为 ","）                                                                                                                           | 否       | 仅在非交互模式下有效。                  |
| --csv.skip-header                | 导出表的 CSV 文件时不包含表头。                                                                                                                                | 否       | 仅在非交互模式下有效。                  |
| --parquet.compression string     | 指定 Parquet 压缩算法。可选值为 [`"GZIP"` `"SNAPPY"` `"ZSTD"` `"NONE"`]。默认值为 `"ZSTD"`。                                                                                   | 否       | 仅在非交互模式下有效。                  |
| --filter strings                 | 使用表过滤模式指定要导出的表。不要与 --sql 一起使用。更多信息，请参见[表过滤器](/table-filter.md)。 | 否       | 仅在非交互模式下有效。                  |
| --sql string                     | 使用 `SQL SELECT` 语句过滤导出的数据。                                                                                                                           | 否       | 仅在非交互模式下有效。                  |
| --where string                   | 使用 `WHERE` 条件过滤导出的表。不要与 --sql 一起使用。                                                                                         | 否       | 仅在非交互模式下有效。                  |
| --compression string             | 指定导出文件的压缩算法。支持的算法包括 `GZIP`、`SNAPPY`、`ZSTD` 和 `NONE`。默认值为 `GZIP`。                   | 否       | 仅在非交互模式下有效。                  |
| --force                          | 无需确认即创建导出任务。当你想在非交互模式下导出整个集群时需要确认。                                                           | 否       | 仅在非交互模式下有效。                  |
| -h, --help                       | 显示此命令的帮助信息。                                                                                                                                      | 否       | 在非交互和交互模式下都可用。 |

## 继承的参数标志

| 参数标志             | 描述                                                                                          | 是否必需 | 说明                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                            | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。 |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。 | 否       | 在非交互和交互模式下都可用。                                                             |
| -D, --debug          | 启用调试模式。                                                                                   | 否       | 在非交互和交互模式下都可用。                                                             |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建一个 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。

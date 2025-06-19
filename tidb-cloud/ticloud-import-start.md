---
title: ticloud serverless import start
summary: `ticloud serverless import start` 命令的参考。
aliases: ['/tidbcloud/ticloud-import-start-local','/tidbcloud/ticloud-import-start-mysql','/tidbcloud/ticloud-import-start-s3']
---

# ticloud serverless import start

启动数据导入任务：

```shell
ticloud serverless import start [flags]
```

或使用以下别名命令：

```shell
ticloud serverless import create [flags]
```

> **注意：**
>
> 目前，每个本地导入任务只能导入一个 CSV 文件。

## 示例

在交互模式下启动导入任务：

```shell
ticloud serverless import start
```

在非交互模式下启动本地导入任务：

```shell
ticloud serverless import start --local.file-path <file-path> --cluster-id <cluster-id> --file-type <file-type> --local.target-database <target-database> --local.target-table <target-table>
```

使用自定义上传并发度启动本地导入任务：

```shell
ticloud serverless import start --local.file-path <file-path> --cluster-id <cluster-id> --file-type <file-type> --local.target-database <target-database> --local.target-table <target-table> --local.concurrency 10
```

使用自定义 CSV 格式启动本地导入任务：

```shell
ticloud serverless import start --local.file-path <file-path> --cluster-id <cluster-id> --file-type CSV --local.target-database <target-database> --local.target-table <target-table> --csv.separator \" --csv.delimiter \' --csv.backslash-escape=false --csv.trim-last-separator=true
```

在非交互模式下启动 S3 导入任务：

```shell
ticloud serverless import start --source-type S3 --s3.uri <s3-uri> --cluster-id <cluster-id> --file-type <file-type> --s3.role-arn <role-arn>
```

在非交互模式下启动 GCS 导入任务：

```shell
ticloud serverless import start --source-type GCS --gcs.uri <gcs-uri> --cluster-id <cluster-id> --file-type <file-type> --gcs.service-account-key <service-account-key>
```

在非交互模式下启动 Azure Blob 导入任务：

```shell
ticloud serverless import start --source-type AZURE_BLOB --azblob.uri <azure-blob-uri> --cluster-id <cluster-id> --file-type <file-type> --azblob.sas-token <sas-token>
```

## 标志

在非交互模式下，你需要手动输入必需的标志。在交互模式下，你只需按照 CLI 提示填写即可。

| 标志                             | 描述                                                                                                                | 是否必需 | 说明                                    |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------|
| --azblob.sas-token string        | 指定 Azure Blob 的 SAS 令牌。                                                                                       | 否       | 仅在非交互模式下生效。                  |
| --azblob.uri string              | 指定 Azure Blob URI，格式为 `azure://<account>.blob.core.windows.net/<container>/<path>`。                          | 否       | 仅在非交互模式下生效。                  |
| --gcs.service-account-key string | 指定 GCS 的 base64 编码服务账号密钥。                                                                               | 否       | 仅在非交互模式下生效。                  |
| --gcs.uri string                 | 指定 GCS URI，格式为 `gcs://<bucket>/<path>`。当源类型为 GCS 时必需。                                               | 是       | 仅在非交互模式下生效。                  |
| --s3.access-key-id string        | 指定 Amazon S3 的访问密钥 ID。你只需要设置 `s3.role-arn` 或 [`s3.access-key-id`, `s3.secret-access-key`] 其中之一。 | 否       | 仅在非交互模式下生效。                  |
| --s3.role-arn string             | 指定 Amazon S3 的角色 ARN。你只需要设置 `s3.role-arn` 或 [`s3.access-key-id`, `s3.secret-access-key`] 其中之一。    | 否       | 仅在非交互模式下生效。                  |
| --s3.secret-access-key string    | 指定 Amazon S3 的秘密访问密钥。你只需要设置 `s3.role-arn` 或 [`s3.access-key-id`, `s3.secret-access-key`] 其中之一。| 否       | 仅在非交互模式下生效。                  |
| --s3.uri string                  | 指定 S3 URI，格式为 `s3://<bucket>/<path>`。当源类型为 S3 时必需。                                                  | 是       | 仅在非交互模式下生效。                  |
| --source-type string             | 指定导入源类型，可选值为 [`"LOCAL"` `"S3"` `"GCS"` `"AZURE_BLOB"`]。默认值为 `"LOCAL"`。                           | 否       | 仅在非交互模式下生效。                  |
| -c, --cluster-id string          | 指定集群 ID。                                                                                                       | 是       | 仅在非交互模式下生效。                  |
| --local.concurrency int          | 指定上传文件的并发度。默认值为 `5`。                                                                                | 否       | 仅在非交互模式下生效。                  |
| --local.file-path string         | 指定要导入的本地文件路径。                                                                                          | 否       | 仅在非交互模式下生效。                  |
| --local.target-database string   | 指定要导入数据的目标数据库。                                                                                        | 否       | 仅在非交互模式下生效。                  |
| --local.target-table string      | 指定要导入数据的目标表。                                                                                            | 否       | 仅在非交互模式下生效。                  |
| --file-type string               | 指定导入文件类型，可选值为 ["CSV" "SQL" "AURORA_SNAPSHOT" "PARQUET"]。                                              | 是       | 仅在非交互模式下生效。                  |
| --csv.backslash-escape           | 指定是否将 CSV 文件中字段内的反斜杠解析为转义字符。默认值为 `true`。                                                | 否       | 仅在非交互模式下生效。                  |
| --csv.delimiter string           | 指定 CSV 文件中用于引用的分隔符。默认值为 `\`。                                                                     | 否       | 仅在非交互模式下生效。                  |
| --csv.separator string           | 指定 CSV 文件中的字段分隔符。默认值为 `,`。                                                                         | 否       | 仅在非交互模式下生效。                  |
| --csv.skip-header                | 指定 CSV 文件是否包含标题行。                                                                                       | 否       | 仅在非交互模式下生效。                  |
| --csv.trim-last-separator        | 指定是否将分隔符视为行终止符并修剪 CSV 文件中所有尾随分隔符。                                                       | 否       | 仅在非交互模式下生效。                  |
| --csv.not-null                   | 指定 CSV 文件是否可以包含任何 NULL 值。                                                                             | 否       | 仅在非交互模式下生效。                  |
| --csv.null-value string          | 指定 CSV 文件中 NULL 值的表示形式。（默认值为 "\\N"）                                                               | 否       | 仅在非交互模式下生效。                  |
| -h, --help                       | 显示此命令的帮助信息。                                                                                              | 否       | 在非交互模式和交互模式下都有效。        |

## 继承的标志

| 标志                  | 描述                                                                                     | 是否必需 | 说明                                                                                                |
|----------------------|------------------------------------------------------------------------------------------|----------|-----------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                        | 否       | 仅在非交互模式下生效。在交互模式下，对某些 UI 组件禁用颜色可能不起作用。                              |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。         | 否       | 在非交互模式和交互模式下都有效。                                                                      |
| -D, --debug          | 启用调试模式。                                                                            | 否       | 在非交互模式和交互模式下都有效。                                                                      |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。

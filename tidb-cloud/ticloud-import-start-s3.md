---
title: ticloud import start s3
summary: The reference of `ticloud import start s3`.
---

# ticloud import start s3

Import files from Amazon S3 into TiDB Cloud:

```shell
ticloud import start s3 [flags]
```

> **Note:**
>
> Before importing files from Amazon S3 into TiDB Cloud, you need to configure the Amazon S3 bucket access for TiDB Cloud and get the Role ARN. For more information, see [Configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).

## Examples

Start an import task in interactive mode:

```shell
ticloud import start s3
```

Start an import task in non-interactive mode:

```shell
ticloud import start s3 --project-id <project-id> --cluster-id <cluster-id> --aws-role-arn <aws-role-arn> --data-format <data-format> --source-url <source-url>
```

Start an import task with a custom CSV format:

```shell
ticloud import start s3 --project-id <project-id> --cluster-id <cluster-id> --aws-role-arn <aws-role-arn> --data-format CSV --source-url <source-url> --separator \" --delimiter \' --backslash-escape=false --trim-last-separator=true
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag | Description | Required | Note |
|---|---|---|---|
| --aws-role-arn string | Specifies the AWS role ARN that is used to access the Amazon S3 data source. | Yes | Only works in non-interactive mode. |
| --backslash-escape | Whether to parse backslashes inside fields as escape characters for CSV files. The default value is `true`. | No | Only works in non-interactive mode when `--data-format CSV` is specified. |
| -c, --cluster-id string | Specifies the cluster ID. | Yes | Only works in non-interactive mode. |
| --data-format string | Specifies the data format. Valid values are `CSV`, `SqlFile`, `Parquet`, or `AuroraSnapshot`. | Yes | Only works in non-interactive mode. |
| --delimiter string | Specifies the delimiter used for quoting for CSV files. The default value is `"`. | No | Only works in non-interactive mode when `--data-format CSV` is specified. |
| -h, --help | Displays help information for this command. | No | Works in both non-interactive and interactive modes. |
| -p, --project-id string | Specifies the project ID. | Yes | Only works in non-interactive mode. |
| --separator string | Specifies the field separator for CSV files. The default value is `,`. | No | Only works in non-interactive mode when `--data-format CSV` is specified. |
| --source-url string | The S3 path where the source data files are stored. | Yes | Only works in non-interactive mode. |
| --trim-last-separator | Whether to treat separators as line terminators and trim all trailing separators for CSV files. The default value is `false`. | No | Only works in non-interactive mode when `--data-format CSV` is specified. |

## Inherited flags

| Flag | Description | Required | Note |
|---|---|---|---|
| --no-color | Disables color in output | No | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No | Works in both non-interactive and interactive modes. |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

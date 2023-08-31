---
title: ticloud import start local
summary: The reference of `ticloud import start local`.
---

# ticloud import start local

Import a local file to a [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster:

```shell
ticloud import start local <file-path> [flags]
```

> **Note:**
>
> Currently, you can only import one CSV file for one import task.

## Examples

Start an import task in interactive mode:

```shell
ticloud import start local <file-path>
```

Start an import task in non-interactive mode:

```shell
ticloud import start local <file-path> --project-id <project-id> --cluster-id <cluster-id> --data-format <data-format> --target-database <target-database> --target-table <target-table>
```

Start an import task with a custom CSV format:

```shell
ticloud import start local <file-path> --project-id <project-id> --cluster-id <cluster-id> --data-format CSV --target-database <target-database> --target-table <target-table> --separator \" --delimiter \' --backslash-escape=false --trim-last-separator=true
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag | Description | Required | Note |
|---|---|---|---|
| --backslash-escape | Whether to parse backslashes inside fields as escape characters for CSV files. The default value is `true`. | No | Only works in non-interactive mode when `--data-format CSV` is specified. |
| -c, --cluster-id string | Specifies the cluster ID. | Yes | Only works in non-interactive mode. |
| --data-format string | Specifies the data format. Currently, only `CSV` is supported. | Yes | Only works in non-interactive mode. |
| --delimiter string | Specifies the delimiter used for quoting for CSV files. The default value is `"`. | No | Only works in non-interactive mode when `--data-format CSV` is specified. |
| -h, --help | Displays help information for this command. | No | Works in both non-interactive and interactive modes. |
| -p, --project-id string | Specifies the project ID. | Yes | Only works in non-interactive mode. |
| --separator string | Specifies the field separator for CSV files. The default value is `,`. | No | Only works in non-interactive mode when `--data-format CSV` is specified. |
| --target-database string | Specifies the target database to import data to. | Yes | Only works in non-interactive mode. |
| --target-table string | Specifies the target table to import data to. | Yes | Only works in non-interactive mode. |
| --trim-last-separator | Whether to treat separators as line terminators and trim all trailing separators for CSV files. The default value is `false`. | No | Only works in non-interactive mode when `--data-format CSV` is specified. |

## Inherited flags

| Flag | Description | Required | Note |
|---|---|---|---|
| --no-color | Disables color in output. | No | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No | Works in both non-interactive and interactive modes. |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

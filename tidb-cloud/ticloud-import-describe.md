---
title: ticloud import describe
summary: The reference of `ticloud import describe`.
---

# ticloud import describe

Get the import details of a data import task:

```shell
ticloud import describe [flags]
```

Or use the following alias command:

```shell
ticloud import get [flags]
```

## Examples

Describe an import task in interactive mode:

```shell
ticloud import describe
```

Describe an import task in non-interactive mode:

```shell
ticloud import describe --project-id <project-id> --cluster-id <cluster-id> --import-id <import-id>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description              | Required | Note                             |
|-------------------------|--------------------------|----------|-----------------------------------|
| -c, --cluster-id string | Cluster ID               | Yes      | Only works in non-interactive mode. |
| -h, --help              | Help information for this command | No       | Works in both non-interactive and interactive modes. |
| --import-id string      | The ID of the import task    | Yes      | Only works in non-interactive mode. |
| -p, --project-id string | Project ID               | Yes      | Only works in non-interactive mode. |

## Inherited flags

| Flag                 | Description                                                                               | Required | Note                                                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

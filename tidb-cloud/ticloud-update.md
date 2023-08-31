---
title: ticloud update
summary: The reference of `ticloud update`.
---

# ticloud update

Update the TiDB Cloud CLI to the latest version:

```shell
ticloud update [flags]
```

## Examples

Update the TiDB Cloud CLI to the latest version:

```shell
ticloud update
```

## Flags

| Flag       | Description              |
|------------|--------------------------|
 | -h, --help | Help information for this command |

## Inherited flags

| Flag                 | Description                                                                               | Required | Note                                                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

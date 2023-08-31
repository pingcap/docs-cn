---
title: ticloud config edit
summary: The reference of `ticloud config edit`.
---

# ticloud config edit

If you are using macOS or Linux, you can open the profile configuration file with your default text editor:

```shell
ticloud config edit [flags]
```

If you are using Windows, after you execute the preceding command, the path of the profile configuration file will be printed instead.

> **Note:**
>
> To avoid format errors and execution failures, it is NOT recommended to manually edit the configuration file. Instead, you can use [`ticloud config create`](/tidb-cloud/ticloud-config-create.md), [`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md), or [`ticloud config set`](/tidb-cloud/ticloud-config-set.md) to modify the confiturations.

## Examples

Edit the profile configuration file:

```shell
ticloud config edit
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

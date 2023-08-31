---
title: ticloud branch create
summary: The reference of `ticloud branch create`.
---

# ticloud branch create

Create a branch for a cluster:

```shell
ticloud branch create [flags]
```

> **Note:**
>
> Currently, you can only create branches for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster.

## Examples

Create a branch in interactive mode:

```shell
ticloud branch create
```

Create a branch in non-interactive mode:

```shell
ticloud branch create --cluster-id <cluster-id> --branch-name <branch-name>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                | Required | Note                                                |
|-------------------------|------------------------------------------------------------|----------|-----------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster, in which the branch will be created | Yes      | Only works in non-interactive mode.                 |
| --branch-name string    | The name of the branch to be created                           | Yes      | Only works in non-interactive mode.                 |
| -h, --help              | Get help information for this command                      | No       | Works in both non-interactive and interactive modes |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                               |
|----------------------|------------------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components.   |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                               |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

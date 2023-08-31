---
title: ticloud connect
summary: The reference of `ticloud connect`.
---

# ticloud connect

Connect to a TiDB Cloud cluster or branch:

```shell
ticloud connect [flags]
```

> **Note:**
>
> - If you are prompted about whether to use the default user, you can choose `Y` to use the default root user or choose `n` to specify another user. For [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters, the name of the default root user has a [prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix) such as `3pTAoNNegb47Uc8`.
> - The connection forces the [ANSI SQL mode](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_ansi) for the session. To exit the session, enter `\q`.

## Examples

Connect to a TiDB Cloud cluster or branch in interactive mode:

```shell
ticloud connect
```

Use the default user to connect to a TiDB Cloud cluster or branch in non-interactive mode:

```shell
ticloud connect -p <project-id> -c <cluster-id>
ticloud connect -p <project-id> -c <cluster-id> -b <branch-id>
```

Use the default user to connect to the TiDB Cloud cluster or branch with password in non-interactive mode:

```shell
ticloud connect -p <project-id> -c <cluster-id> --password <password>
ticloud connect -p <project-id> -c <cluster-id> -b <branch-id> --password <password>
```

Use a specific user to connect to the TiDB Cloud cluster or branch in non-interactive mode:

```shell
ticloud connect -p <project-id> -c <cluster-id> -u <user-name>
ticloud connect -p <project-id> -c <cluster-id> -b <branch-id> -u <user-name>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                       | Required | Note                                                 |
|-------------------------|-----------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | Cluster ID                        | Yes      | Only works in non-interactive mode.                  |
| -b, --branch-id string  | Branch ID                         | No       | Only works in non-interactive mode.                  |
| -h, --help              | Help information for this command | No       | Works in both non-interactive and interactive modes. |
| --password              | The password of the user          | No       | Only works in non-interactive mode.                  |
| -p, --project-id string | Project ID                        | Yes      | Only works in non-interactive mode.                  |
| -u, --user string       | A specific user for login         | No       | Only works in non-interactive mode.                  |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                                     |
|----------------------|------------------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                                     |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

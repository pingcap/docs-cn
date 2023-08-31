---
title: ticloud branch delete
summary: The reference of `ticloud branch delete`.
---

# ticloud branch delete

Delete a branch from your cluster:

```shell
ticloud branch delete [flags]
```

Or use the following alias command:

```shell
ticloud branch rm [flags]
```

## Examples

Delete a branch in interactive mode:

```shell
ticloud branch delete
```

Delete a branch in non-interactive mode:

```shell
ticloud branch delete --branch-id <branch-id> --cluster-id <cluster-id>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                | Required | Note                                                 |
|-------------------------|--------------------------------------------|----------|------------------------------------------------------|
| -b, --branch-id string  | The ID of the branch to be deleted         | Yes      | Only works in non-interactive mode.                  |
| --force                 | Deletes a branch without confirmation      | No       | Works in both non-interactive and interactive modes. |
| -h, --help              | Help information for this command          | No       | Works in both non-interactive and interactive modes. |
| -c, --cluster-id string | The cluster ID of the branch to be deleted | Yes      | Only works in non-interactive mode.                  |

## Inherited flags

| Flag                 | Description                                                                                | Required | Note                                                                                                              |
|----------------------|--------------------------------------------------------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components.  |
| -P, --profile string | The active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                              |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

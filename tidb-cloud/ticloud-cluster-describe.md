---
title: ticloud cluster describe
summary: The reference of `ticloud cluster describe`.
---

# ticloud cluster describe

Get information about a cluster (such as the cloud provider, cluster type, cluster configurations, and cluster status):

```shell
ticloud cluster describe [flags]
```

Or use the following alias command:

```shell
ticloud cluster get [flags]
```

## Examples

Get the cluster information in interactive mode:

```shell
ticloud cluster describe
```

Get the cluster information in non-interactive mode:

```shell
ticloud cluster describe --project-id <project-id> --cluster-id <cluster-id>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                   | Required | Note                             |
|-------------------------|-------------------------------|----------|-----------------------------------|
| -c, --cluster-id string | The ID of the cluster         | Yes      | Only works in non-interactive mode. |
| -h, --help              | Help information for this command     | No       | Works in both non-interactive and interactive modes. |
| -p, --project-id string | The project ID of the cluster | Yes      | Only works in non-interactive mode. |

## Inherited flags

| Flag                 | Description                                                                               | Required | Note                                                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

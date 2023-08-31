---
title: ticloud cluster create
summary: The reference of `ticloud cluster create`.
---

# ticloud cluster create

Create a cluster:

```shell
ticloud cluster create [flags]
```

> **Note:**
>
> Currently, you can only create a [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster using the preceding command.

## Examples

Create a cluster in interactive mode:

```shell
ticloud cluster create
```

Create a cluster in non-interactive mode:

```shell
ticloud cluster create --project-id <project-id> --cluster-name <cluster-name> --cloud-provider <cloud-provider> --region <region> --root-password <password> --cluster-type <cluster-type>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                 | Required | Note                             |
|-------------------------|-------------------------------------------------------------|----------|-----------------------------------|
| --cloud-provider string | Cloud provider (Currently, only `AWS` is supported)                                | Yes      | Only works in non-interactive mode. |
| --cluster-name string   | Name of the cluster to be created                           | Yes      | Only works in non-interactive mode. |
| --cluster-type string   | Cluster type (Currently, only `SERVERLESS` is supported)    | Yes      | Only works in non-interactive mode. |
| -h, --help              | Get help information for this command   | No       | Works in both non-interactive and interactive modes     |
| -p, --project-id string | The ID of the project, in which the cluster will be created | Yes      | Only works in non-interactive mode. |
| -r, --region string     | Cloud region                                                | Yes      | Only works in non-interactive mode. |
| --root-password string  | The root password of the cluster                            | Yes      | Only works in non-interactive mode. |

## Inherited flags

| Flag                 | Description                                                                               | Required | Note                                                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

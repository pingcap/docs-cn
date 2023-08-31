---
title: ticloud config create
summary: The reference of `ticloud config create`.
---

# ticloud config create

Create a [user profile](/tidb-cloud/cli-reference.md#user-profile) to store user profile settings:

```shell
ticloud config create [flags]
```

> **Note:**
>
> Before creating a user profile, you need to [create a TiDB Cloud API Key](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management).

## Examples

Create a user profile in interactive mode:

```shell
ticloud config create
```

Create a user profile in non-interactive mode:

```shell
ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                  | Description                                   | Required | Note                             |
|-----------------------|-----------------------------------------------|----------|-----------------------------------|
| -h, --help            | Help information for this command                     | No       | Works in both non-interactive and interactive modes. |
| --private-key string  | The private key of the TiDB Cloud API         | Yes      | Only works in non-interactive mode. |
| --profile-name string | The name of the profile, which must not contain `.` | Yes      | Only works in non-interactive mode. |
| --public-key string   | The public key of the TiDB Cloud API          | Yes      | Only works in non-interactive mode. |

## Inherited flags

| Flag                 | Description                                  | Required | Note                                                                                                                    |
|----------------------|----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                     | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

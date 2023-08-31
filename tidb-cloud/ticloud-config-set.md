---
title: ticloud config set
summary: The reference of `ticloud config set`.
---

# ticloud config set

Configure the properties for the active [user profile](/tidb-cloud/cli-reference.md#user-profile):

```shell
ticloud config set <property-name> <value> [flags]
```

The properties that can be configured include `public-key`, `private-key`, and `api-url`.

| Properties  | Description                                                        | Required |
|-------------|--------------------------------------------------------------------|----------|
| public-key  | The public key of the TiDB Cloud API                               | Yes      |
| private-key | The private key of the TiDB Cloud API                              | Yes      |
| api-url     | The base API URL of TiDB Cloud (`https://api.tidbcloud.com` by default) | No       |

> **Notes:**
>
> If you want to configure properties for a specific user profile, you can add the `-P` flag and specify the target user profile name in the command.

## Examples

Set the value of the public-key for the active profile:

```shell
ticloud config set public-key <public-key>
```

Set the value of the public-key for a specific profile `test`:

```shell
ticloud config set public-key <public-key> -P test
```

Set the API host:

```shell
ticloud config set api-url https://api.tidbcloud.com
```

> **Note:**
>
> The TiDB Cloud API URL is `https://api.tidbcloud.com` by default. Usually, you do not need to set up it.

## Flags

| Flag       | Description              |
|------------|--------------------------|
| -h, --help | Help information for this command |

## Inherited flags

| Flag                 | Description                                   | Required | Note                                                                                                                    |
|----------------------|-----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                      | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

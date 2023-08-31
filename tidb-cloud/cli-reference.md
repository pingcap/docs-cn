---
title: TiDB Cloud CLI Reference
summary: Provides an overview of TiDB Cloud CLI.
---

# TiDB Cloud CLI Reference

TiDB Cloud CLI is a command line interface, which allows you to operate TiDB Cloud from your terminal with a few lines of commands. In the TiDB Cloud CLI, you can easily manage your TiDB Cloud clusters, import data to your clusters, and perform more operations.

## Before you begin

Make sure to first [set up your TiDB Cloud CLI environment](/tidb-cloud/get-started-with-cli.md). Once you have installed the `ticloud` CLI, you can use it to manage your TiDB Cloud clusters from the command lines.

## Commands available

The following table lists the commands available for the TiDB Cloud CLI.

To use the `ticloud` CLI in your terminal, run `ticloud [command] [subcommand]`. If you are using [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview), use `tiup cloud [command] [subcommand]` instead.

| Command    | Subcommand                                                 | Description                                                                                              |
|------------|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| cluster    | create, delete, describe, list, connect-info               | Manage clusters                                                                                          |
| branch     | create, delete, describe, list, connect-info               | Manage branches                                                                                          |
| completion | bash, fish, powershell, zsh                                | Generate completion script for specified shell                                                           |
| config     | create, delete, describe, edit, list, set, use             | Configure user profiles                                                                                  |
| connect    | -                                                          | Connect to a TiDB cluster                                                                                |
| help       | cluster, completion, config, help, import, project, update | View help for any command                                                                                |
| import     | cancel, describe, list, start                              | Manage [import](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud) tasks |
| project    | list                                                       | Manage projects                                                                                          |
| update     | -                                                          | Update the CLI to the latest version                                                                     |

## Command modes

The TiDB Cloud CLI provides two modes for some commands for easy use:

- Interactive mode

    You can run a command without flags (such as `ticloud config create`), and the CLI prompts you for input.

- Non-interactive mode

    You must provide all arguments and flags that are required when running a command, such as `ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>`.

## User profile

For the TiDB Cloud CLI, a user profile is a collection of properties associated with a user, including the profile name, public key, and private key. To use TiDB Cloud CLI, you must create a user profile first.

### Create a user profile

Use [`ticloud config create`](/tidb-cloud/ticloud-config-create.md) to create a user profile.

### List all user profiles

Use [`ticloud config list`](/tidb-cloud/ticloud-config-list.md) to list all user profiles.

An example output is as follows:

```
Profile Name
default (active)
dev
staging
```

In this example output, the user profile `default` is currently active.

### Describe a user profile

Use [`ticloud config describe`](/tidb-cloud/ticloud-config-describe.md) to get the properties of a user profile.

An example output is as follows:

```json
{
  "private-key": "xxxxxxx-xxx-xxxxx-xxx-xxxxx",
  "public-key": "Uxxxxxxx"
}
```

### Set properties in a user profile

Use [`ticloud config set`](/tidb-cloud/ticloud-config-set.md) to set properties in a user profile.

### Switch to another user profile

Use [`ticloud config use`](/tidb-cloud/ticloud-config-use.md) to switch to another user profile.

An example output is as follows:

```
Current profile has been changed to default
```

### Edit the config file

Use [`ticloud config edit`](/tidb-cloud/ticloud-config-edit.md) to open the configuration file for editing.

### Delete a user profile

Use [`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md) to delete a user profile.

## Global flags

The following table lists the global flags for the TiDB Cloud CLI.

| Flag                 | Description                                   | Required | Note                                                                                                                    |
|----------------------|-----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                      | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active user profile used in this command. | No       | Works in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

---
title: tiup dm list
---

# tiup dm list

`tiup-dm` supports deploying multiple clusters using the same control machine. You can use the `tiup dm list` command to check which clusters are deployed using the control machine by the currently logged-in user.

> **Note:**
>
> By default, the data of the deployed clusters is stored in the `~/.tiup/storage/dm/clusters/` directory. The currently logged-in user cannot view the clusters deployed by other users on the same control machine.

## Syntax

```shell
tiup dm list [flags]
```

## Options

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

A table consisting of the following fields:

- `Name`: the cluster name.
- `User`: the user who deployed the cluster.
- `Version`: the cluster version.
- `Path`: the path of the cluster deployment data on the control machine.
- `PrivateKey`: the path of the private key to the cluster.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)

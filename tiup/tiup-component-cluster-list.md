---
title: tiup cluster list
---

# tiup cluster list

tiup-cluster supports deploying multiple clusters using the same control machine. The `tiup cluster list` command outputs all clusters deployed by the currently logged-in user using this control machine.

> **Note:**
>
> The deployed cluster data is stored in the `~/.tiup/storage/cluster/clusters/` directory by default, so on the same control machine, the currently logged-in user cannot view the clusters deployed by other users.

## Syntax

```shell
tiup cluster list [flags]
```

## Options

### -h, --help

- Prints help information.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Outputs

Outputs the table with the following fields:

- Name: the cluster name
- User: the deployment user
- Version: the cluster version
- Path: the path of the cluster deployment data on the control machine
- PrivateKey: the path of the private key that is used to connect the cluster

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

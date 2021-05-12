---
title: tiup dm restart
---

# tiup dm restart

The command `tiup dm restart` is used to restart all or some of the services of the specified cluster.

> **Note:**
>
> During the restart process, the related services are unavailable for a period of time.

## Syntax

```shell
tiup dm restart <cluster-name> [flags]
```

`<cluster-name>`: the name of the cluster to operate on. If you forget the cluster name, you can check it with the [cluster list](/tiup/tiup-component-cluster-list.md) command.

## Options

### -N, --node

- Specifies the nodes to be restarted. The value of this option is a comma-separated list of node IDs. You can get the node IDs from the first column of the cluster status table returned by the `[tiup dm display](/tiup/tiup-component-dm-display.md)` command.
- Data type: `STRING`
- If this option is not specified, TiUP restarts all nodes by default.

> **Note:**
>
> If the option `-R, --role` is specified at the same time, TiUP restarts service nodes that match both the requirements of `-N, --node` and `-R, --role`.

### -R, --role

- Specifies the roles of nodes to be restarted. The value of this option is a comma-separated list of the roles of the nodes. You can get the roles of the nodes from the second column of the cluster status table returned by the `[tiup dm display](/tiup/tiup-component-dm-display.md)` command.
- Data type: `STRING`
- If this option is not specified, TiUP restarts nodes of all roles by default.

> **Note:**
>
> If the option `-N, --node` is specified at the same time, TiUP restarts service nodes that match both the requirements of `-N, --node` and `-R, --role`.

### -h, --help

- Prints help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Outputs

The log of the service restart process.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)

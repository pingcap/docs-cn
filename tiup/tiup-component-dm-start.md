---
title: tiup dm start
---

# tiup dm start

The `tiup dm start` command is used to start all or part of the services of the specified cluster.

## Syntax

```shell
tiup dm start <cluster-name> [flags]
```

`<cluster-name>`: the name of the cluster to operate on. If you forget the cluster name, you can check it with the [cluster list](/tiup/tiup-component-dm-list.md) command.

## Options

### -N, --node

- Specifies the nodes to be started. If not specified, all nodes are started. The value of this option is a comma-separated list of node IDs. You can get the node IDs from the first column of the cluster status table returned by the [`tiup dm display`](/tiup/tiup-component-dm-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, all nodes are started.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are started.

### -R, --role

- Specifies the roles to be started. If not specified, all roles are started. The value of this option is a comma-separated list of node roles. You can get the roles of nodes from the second column of the cluster status table returned by the [`tiup dm display`](/tiup/tiup-component-dm-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, all roles are started.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are started.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The log of starting the service.

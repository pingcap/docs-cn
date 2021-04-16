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

- Specifies the nodes to be started. If not specified, all nodes are started. The value of this option is a comma-separated list of node IDs. The node ID is the first column of the [cluster status](/tiup/tiup-component-dm-display.md) table.
- Data type: `strings`
- Default: `[]`. If this option is not specified in the command, all nodes are started.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, then the services in their intersection are started.

### -R, --role

- Specifies the roles to be started. If not specified, all roles are started. The value of this option is a comma-separated list of node roles. The role is the second column of the [cluster status](/tiup/tiup-component-dm-display.md) table.
- Data type: `strings`
- Default: `[]`. If this option is not specified in the command, all roles are started.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the services in their intersection are started.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The log of starting the service.
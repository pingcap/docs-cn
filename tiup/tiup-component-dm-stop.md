---
title: tiup dm stop
---

# tiup dm stop

The `tiup dm stop` command is used to stop all or part of the services of the specified cluster.

> **Note:**
>
> The cluster cannot provide services after the core service is stopped.

## Syntax

```shell
tiup dm stop <cluster-name> [flags]
```

`<cluster-name>`: the name of the cluster to operate on. If you forget the cluster name, you can check it with the [cluster list](/tiup/tiup-component-dm-list.md) command.

## Options

### -N, --node

- Specifies the nodes to be stopped. If not specified, all nodes are stopped. The value of this option is a comma-separated list of node IDs. The node ID is the first column of the [cluster status](/tiup/tiup-component-dm-display.md) table.
- Data type: `strings`
- Default: `[]`, which means all nodes are selected.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, then the service status in their intersection is stopped.

### -R, --role

- Specifies the roles to be stopped. If not specified, all roles are stopped. The value of this option is a comma-separated list of node roles. The role is the second column of the [cluster status](/tiup/tiup-component-dm-display.md) table.
- Data type: `strings`
- Default: `[]`, which means all roles are selected.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the services in their intersection is stopped.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The log of stopping the service.
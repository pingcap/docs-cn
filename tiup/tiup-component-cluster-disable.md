---
title: tiup cluster disable
---

# tiup cluster disable

The `tiup cluster disable` command is used to disable the auto-enabling after restarting the machine where the cluster service is located. This command executes the `systemctl disable <service>` on the specified node to disable the auto-enabling of the service.

## Syntax

```shell
tiup cluster disable <cluster-name> [flags]
```

`<cluster-name>`: the cluster whose auto-enabling service is to be disabled.

## Options

### -N, --node

- Data type: `strings`
- Default: `[]`, which means no node is selected.
- Specifies the nodes whose auto-enabling service is to be disabled. The value of this option is a comma-separated list of node IDs. The node ID is the first column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, the auto-enabling of services in their intersection is disabled.

### -R, --role strings

- Data type: `strings`
- Default: `[]`, which means no role is selected.
- Specifies the roles whose auto-enabling service is to be disabled. The value of this option is a comma-separated list of node roles. The role is the second column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the auto-enabling of services in their intersection is disabled.

### -h, --help

- Outputs the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The execution log of the tiup-cluster.

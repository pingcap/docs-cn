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

- Specifies the nodes whose auto-enabling service is to be disabled. The value of this option is a comma-separated list of node IDs. The node ID is the first column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.
- Data type: `strings`
- Default: `[]`, which means no node is selected.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, the auto-enabling of services in their intersection is disabled.

### -R, --role

- Data type: `strings`
- Default: `[]`, which means no role is selected.
- Specifies the roles whose auto-enabling service is to be disabled. The value of this option is a comma-separated list of node roles. The role is the second column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the auto-enabling of services in their intersection is disabled.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Output

The execution log of the tiup-cluster.

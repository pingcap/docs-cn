---
title: tiup dm enable
---

# tiup dm enable

The `tiup dm enable` command is used to set the auto-enabling of the cluster service after a machine is restarted. This command enables the auto-enabling of the service by executing `systemctl enable <service>` at the specified node.

## Syntax

```shell
tiup dm enable <cluster-name> [flags]
```

`<cluster-name>` is the cluster whose service auto-enabling is to be enabled.

## Options

### -N, --node

- Specifies the nodes whose service auto-enabling is to be enabled. The value of this option is a comma-separated list of node IDs. You can get the node IDs from the first column of the cluster status table returned by the [`tiup dm display`](/tiup/tiup-component-dm-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, the auto-enabling of all nodes is enabled by default.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, the auto-enabling of services that match both the specifications of `-N, --node` and `-R, --role` is enabled.

### -R, --role

- Specifies the roles whose service auto-enabling is to be enabled. The value of this option is a comma-separated list of node roles. You can get the roles of nodes from the second column of the cluster status table returned by the [`tiup dm display`](/tiup/tiup-component-dm-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, the auto-enabling of all roles is enabled by default.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the auto-enabling of services that match both the specifications of `-N, --node` and `-R, --role` is enabled.

### -h, --help

Prints the help information.

## Output

the execution log of tiup-dm.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)

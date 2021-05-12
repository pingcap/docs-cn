---
title: tiup cluster enable
---

# tiup cluster enable

The `tiup cluster enable` command is used to set the auto-enabling of the cluster service after a machine is restarted. This command enables the auto-enabling of the service by executing `systemctl enable <service>` at the specified node.

> **Note:**
>
> When all clusters are shut down and restarted, the order of service startup is determined by the node's operating system startup order. When the restart order is incorrect, in some cases, the restarted cluster still cannot provide services. For example, if TiKV is started first but PD is not started, systemd gives up if TiKV is restarted multiple times while PD is not found).

## Syntax

```shell
tiup cluster enable <cluster-name> [flags]
```

`<cluster-name>`: the cluster whose service auto-enabling is to be enabled.

## Options

### -N, --node

- Specifies the nodes whose service auto-enabling is to be enabled. The value of this option is a comma-separated list of node IDs. You can get the node IDs from the first column of the cluster status table returned by the [`tiup cluster display`](/tiup/tiup-component-cluster-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, the auto-enabling of all nodes is enabled by default.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, the auto-enabling of services that match both the specifications of `-N, --node` and `-R, --role` is enabled.

### -R, --role

- Specifies the roles whose service auto-enabling is to be enabled. The value of this option is a comma-separated list of node roles. You can get the roles of nodes from the second column of the cluster status table returned by the [`tiup cluster display`](/tiup/tiup-component-cluster-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, the auto-enabling of all roles is enabled by default.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the auto-enabling of services that match both the specifications of `-N, --node` and `-R, --role` is enabled.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

The execution log of the tiup-cluster.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

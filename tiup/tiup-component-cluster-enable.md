---
title: tiup cluster enable
---

# tiup cluster enable

The `tiup cluster enable` command is used to set the self-enabling of the cluster service after a machine restarts. To enable the self-enabling of the service, this command executes `systemctl enable <service>` at the specified node.

> **Note:**
>
> When all clusters are shut down and restarted, the order of service startup is determined by the node's operating system startup order. When the restart order is incorrect, in some cases, the restarted cluster still cannot provide services. For example, if TiKV is started first but PD is not started, systemd gives up if TiKV is restarted multiple times while PD is not found).

## Syntax

```shell
tiup cluster enable <cluster-name> [flags]
```

`<cluster-name>`: the cluster whose auto-enabling service is to be enabled.

## Options

### -N, --node

- Specifies the nodes whose auto-enabling service is to be enabled. The value of this option is a comma-separated list of node IDs. The node ID is the first column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.
- Data type: `strings`
- Default: `[]`, which means no node is selected.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, the auto-enabling of services in their intersection is enabled.

### -R, --role

- Specifies the roles whose auto-enabling service is to be enabled. The value of this option is a comma-separated list of node roles. The role is the second column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.
- Data type: `strings`
- Default: `[]`, which means no role is selected.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the auto-enabling of services in their intersection is enabled.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The execution log of the tiup-cluster.

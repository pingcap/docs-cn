---
title: tiup dm disable
---

# tiup dm disable

After restarting the machine on which the cluster service is located, the cluster service will be automatically enabled. To disable the auto-enabling of cluster service, you can use the `tiup dm disable` command. This command executes `systemctl disable <service>` on the specified node to disable the auto-enabling of the service.

## Syntax

```shell
tiup dm disable <cluster-name> [flags]
```

`<cluster-name>` is the cluster whose service auto-enabling is to be disabled.

## Options

### -N, --node

- Specifies the nodes whose service auto-enabling is to be disabled. The value of this option is a comma-separated list of node IDs. You can get the node IDs from the first column of the cluster status table returned by the [`tiup dm display`](/tiup/tiup-component-dm-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, the auto-enabling of all nodes is disabled by default.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, the auto-enabling of services that match both the specifications of `-N, --node` and `-R, --role` is disabled.

### -R, --role

- Specifies the roles whose service auto-enabling is to be disabled. The value of this option is a comma-separated list of node roles. You can get the roles of nodes from the second column of the cluster status table returned by the [`tiup dm display`](/tiup/tiup-component-dm-display.md) command.
- Data type: `STRINGS`
- If this option is not specified in the command, the auto-enabling of all roles is disabled by default.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, the auto-enabling of services that match both the specifications of `-N, --node` and `-R, --role` is disabled.

### -h, --help

Prints the help information.

## Output

The execution log of the tiup-dm.

---
title: tiup cluster start
---

# tiup cluster start

The `tiup cluster start` command is used to start all services or some services of the specified cluster.

## Syntax

```shell
tiup cluster start <cluster-name> [flags]
```

`<cluster-name>` is the name of the cluster to operate on. If you forget the cluster name, you can check it using the [`tiup cluster list`](/tiup/tiup-component-cluster-list.md) command.

## Options

### --init

Starts the cluster in a safe way. It is recommended to use this option when the cluster is started for the first time. This method generates the password of the TiDB root user at startup and returns the password in the command line interface.

> **Note:**
>
> - After safe start of a TiDB cluster, you cannot log in to the database using the root user without a password. Therefore, you need to record the password returned by the command line for future logins.
> - The password is generated only once. If you do not record or forget the password, refer to [Forget the `root` password](/user-account-management.md#forget-the-root-password) to change the password.

### -N, --node

- Specifies the nodes to be started. The value of this option is a comma-separated list of node IDs. You can get the node IDs from the first column of the [cluster status table](/tiup/tiup-component-cluster-display.md) returned by the `tiup cluster display` command.
- Data type: `STRINGS`
- If this option is not specified in the command, all nodes are started by default.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are started.

### -R, --role

- Specifies the roles of nodes to be started. The value of this option is a comma-separated list of the roles of the nodes. You can get the roles of the nodes from the second column of the [cluster status table](/tiup/tiup-component-cluster-display.md) returned by the `tiup cluster display` command.
- Data type: `STRINGS`
- If this option is not specified in the command, all roles are started by default.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are started.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

The log of starting the service.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

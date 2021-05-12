---
title: tiup cluster display
---

# tiup cluster display

If you want to see the operation status of each component in the cluster, it is obviously inefficient to log in to each machine one by one. Therefore, tiup-cluster provides the `tiup cluster display` command to efficiently complete this task.

## Syntax

```shell
tiup cluster display <cluster-name> [flags]
```

`<cluster-name>`: the name of the cluster to operate on. If you forget the cluster name, you can check it with the [cluster list](/tiup/tiup-component-cluster-list.md) command.

## Options

### --dashboard

- By default, all node information of the entire cluster is displayed. With the `--dashboard` option, only dashboard information is displayed.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

### -N, --node

- Specifies the node to display. If this option is not specified, all nodes are displayed. The value of this option is a comma-separated list of node IDs. If you are not sure about the ID of a node, you can skip this option in the command to show the IDs and status of all nodes in the output.
- Data type: `STRINGS`
- If this option is not specified in the command, all nodes are checked by default.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are checked.

### -R, --role

- Specifies the role to display. If it is not specified, all roles are displayed. The value of this option is a comma-separated list of node roles. If you are not sure about the role deployed on a node, you can skip this option in the command to show the roles and status of all nodes in the output.
- Data type: `STRINGS`
- If this option is not specified in the command, all roles are displayed by default.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are displayed.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Outputs

- The cluster name
- The cluster version
- SSH Client Type
- Dashboard address
- The table with the following fields:
    - ID: the node ID, composed of `IP:PORT`
    - Role: the service role deployed on this node (such as TiDB, TiKV)
    - Host: the IP of the machine corresponding to the node
    - Ports: the port number occupied by the service
    - OS/Arch: the operating system and the machine architecture of this node
    - Status: the current status of the node service
    - Data Dir: the data directory of the service. `-` means no data directory.
    - Deploy Dir: the deployment directory of the service

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

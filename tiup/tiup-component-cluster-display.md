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
- Default: false

### -N, --node

- Data type: `strings`
- Default: `[]`, which means all nodes.
- Specifies the node to query. If not specified, all nodes are queried. The value of this option is a comma-separated list of node IDs. The node ID is the first column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.

> **Note:**
>
> If the `-R, --role` option is specified at the same time, then the service status in their intersection is queried.

### -R, --role strings

- Data type: `strings`
- Default: `[]`, which means all roles.
- Specifies the role to query. If not specified, all roles are queried. The value of this option is a comma-separated list of node roles. The role is the second column of the [cluster status](/tiup/tiup-component-cluster-display.md) table.

> **Note:**
>
> If the `-N, --node` option is specified at the same time, then the service status in their intersection is queried.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

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

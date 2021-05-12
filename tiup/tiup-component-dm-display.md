---
title: tiup dm display
---

# tiup dm display

If you want to check the operational status of each component in a DM cluster, it is inefficient to log in to each machine one by one. Therefore, tiup-dm provides the `tiup dm display` command to do this job efficiently.

## Syntax

```shell
tiup dm display <cluster-name> [flags]
```

`<cluster-name>` is the name of the cluster to be operated. If you forget the cluster name, you can check it using the [`tiup dm list`](/tiup/tiup-component-dm-list.md) command.

## Options

### -N, --node

- Specifies the IDs of the nodes to query, splitting by commas for multiple nodes. If you are not sure about the ID of a node, you can skip this option in the command to show the IDs and status of all nodes in the output.
- Data type: `STRING`
- This option is enabled by default with `[]` (which means all nodes) passed in.

> **Note:**
> 
> If `-R, --role` is also specified, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are queried.

### -R, --role

- Specifies the roles to query, splitting by commas for multiple roles. If you are not sure about the role deployed on a node, you can skip this option in the command to show the roles and status of all nodes in the output.
- Data type: `STRING`
- This option is enabled by default with `[]` (which means all roles) passed in.

> **Note:**
> 
> If `-N, --node` is also specified, only the service nodes that match both the specifications of `-N, --node` and `-R, --role` are queried.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

- Cluster name
- Cluster version
- SSH client type
- A table containing the following fields:
    - `ID`: the node ID, consisting of IP:PORT.
    - `Role`: the service role deployed on the node (for example, TiDB or TiKV).
    - `Host`: the IP address of the machine corresponding to the node.
    - `Ports`: the port number used by the service.
    - `OS/Arch`: the operating system and machine architecture of the node.
    - `Status`: the current status of the services on the node.
    - `Data Dir`: the data directory of the service. `-` means that there is no data directory.
    - `Deploy Dir`: the deployment directory of the service.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)

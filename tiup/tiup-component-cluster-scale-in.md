---
title: tiup cluster scale-in
---

# tiup cluster scale-in

The `tiup cluster scale-in` command is used to scale in the cluster, which takes the services of the specified nodes offline, removes the specified nodes from the cluster, and deletes the remaining files from those nodes.

Because the TiKV, TiFlash, and TiDB Binlog components are taken offline asynchronously (which requires TiUP to remove the node through API first) and the stopping process takes a long time (which requires TiUP to continuously check whether the node is successfully taken offline), the TiKV, TiFlash, and TiDB Binlog components are handled particularly as follows:

- For TiKV, TiFlash and, TiDB Binlog components:

    1. TiUP Cluster takes the node offline through API and directly exits without waiting for the process to be completed.
    2. To check the status of the nodes being scaled in, you need to execute the `tiup cluster display` command and wait for the status to become `Tombstone`.
    3. To clean up the nodes in the `Tombstone` status, you need to execute the `tiup cluster prune` command. The `tiup cluster prune` command performs the following operations:

        - Stops the services of the nodes that have been taken offline.
        - Cleans up the data files of the nodes that have been taken offline.
        - Updates the cluster topology and removes the nodes that have been taken offline.

For other components:

- When taking the PD components offline, TiUP Cluster quickly deletes the specified nodes from the cluster through API, stops the service of the specified PD nodes, and then deletes the related data files from the nodes.
- When taking other components down, TiUP Cluster directly stops the node services and deletes the related data files from the specified nodes.

## Syntax

```shell
tiup cluster scale-in <cluster-name> [flags]
```

`<cluster-name>` is the name of the cluster to scale in. If you forget the cluster name, you can check it using the [`tiup cluster list`](/tiup/tiup-component-cluster-list.md) command.

## Options

### -N, --node

- Specifies the nodes to take down. Multiple nodes are separated by commas.
- Data type: `STRING`
- There is no default value. This option is mandatory and the value must be not null.

### --force

- Controls whether to forcibly remove the specified nodes from the cluster. Sometimes, the host of the node to take offline might be down, which makes it impossible to connect to the node via SSH for operations, so you can forcibly remove the node from the cluster using the `-force` option.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

> **Note:**
>
> Because the forced removal of a TiKV node does not wait for data to be scheduled, removing more than one serving TiKV node is at the risk of data loss.

### --transfer-timeout

- When a PD or TiKV node is to be removed, the Region leader on the node will be transferred to another node first. Because the transferring process takes some time, you can set the maximum waiting time (in seconds) by configuring `--transfer-timeout`. After the timeout, the `tiup cluster scale-in` command skips waiting and starts the scaling-in directly.
- Data type: `UINT`
- The option is enabled by default with `300` seconds (the default value) passed in.

> **Note:**
>
> If a PD or TiKV node is taken offline directly without waiting for the leader transfer to be completed, the service performance might jitter.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

Shows the logs of the scaling-in process.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

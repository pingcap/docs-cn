---
title: tiup cluster destroy
---

# tiup cluster destroy

After an application goes offline, if you want to release the machines occupied by the cluster for use by other applications, you need to clean up the data on the cluster and the deployed binary files. To destroy the cluster, the `tiup cluster destroy` command performs the following operations:

- Stops the cluster.
- For each service, delete its log directory, deployment directory, and data directory.
- If the parent directory of the data directory or deployment directory of each service is created by tiup-cluster, also delete the parent directory.

## Syntax

```shell
tiup cluster destroy <cluster-name> [flags]
```

`<cluster-name>`: the name of the cluster to destroy.

## Options

### --force

- In some cases, some nodes in the cluster have been down, making it impossible to connect to the node through SSH for operation. At this time, you can use the `--force` option to ignore these errors.
- Data type: `Boolean`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

### --retain-node-data

- Specifies the nodes that need to retain data. If you need to specify more than one node, use this option multiple times: `--retain-node-data <node-A> --retain-node-data <node-B>`.
- Data type: `StringArray`
- Default: empty

### --retain-role-data

- Specifies the role that needs to retain data. If you need to specify more than one role, use this option multiple times: `--retain-role-data <role-A> --retain-role-data <role-B>`.
- Data type: `StringArray`
- Default: empty

### -h, --help

- Prints the help information.
- Data type: `Boolean`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Output

The execution log of the tiup-cluster.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

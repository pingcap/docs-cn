---
title: tiup dm scale-out
---

# tiup dm scale-out

The `tiup dm scale-out` command is used for scaling out the cluster. The internal logic of scaling out the cluster is similar to the cluster deployment. The `tiup-dm` components first establish an SSH connection to the new node, create the necessary directories on the target node, then perform the deployment and start the service.

## Syntax

```shell
tiup dm scale-out <cluster-name> <topology.yaml> [flags]
```

`<cluster-name>`: the name of the cluster to operate on. If you forget the cluster name, you can check it with the [cluster list](/tiup/tiup-component-dm-list.md) command.

`<topology.yaml>`: the prepared [topology file](/tiup/tiup-dm-topology-reference.md). This topology file should only contain the new nodes that are to be added to the current cluster.

## Options

### -u, --user

- Specifies the user name used to connect to the target machine. This user must have the secret-free sudo root permission on the target machine.
- Data type: `STRING`
- Default: the current user who executes the command.

### -i, --identity_file

- Specifies the key file used to connect to the target machine.
- Data type: `STRING`
- If this option is not specified in the command, the `~/.ssh/id_rsa` file is used to connect to the target machine by default.

### -p, --password

- Specifies the password used to connect to the target machine. Do not use this option and `-i/--identity_file` at the same time.
- Data type: `BOOLEAN`
- Default: false

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The log of scaling out.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)

---
title: tiup cluster scale-out
---

# tiup cluster scale-out

The `tiup cluster scale-out` command is used for scaling out the cluster. The internal logic of scaling out the cluster is similar to the cluster deployment. The tiup-cluster component first establishes an SSH connection to the new node, creates the necessary directories on the target node, then performs the deployment and starts the service.

When PD is scaled out, new PD nodes are added to the cluster by the join operation, and the configuration of the services associated with PD is updated; other services are directly started and added to the cluster.

## Syntax

```shell
tiup cluster scale-out <cluster-name> <topology.yaml> [flags]
```

`<cluster-name>`: the name of the cluster to operate on. If you forget the cluster name, you can check it with the [`cluster list`](/tiup/tiup-component-dm-list.md) command.

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

### --no-labels

- This option is used to skip the label check.
- When two or more TiKV nodes are deployed on the same physical machine, a risk exists: PD does not know the cluster topology, so it might schedule multiple replicas of a Region to different TiKV nodes on one physical machine, which makes this physical machine a single point of failure. To avoid this risk, you can use labels to tell PD not to schedule the same Region to the same machine. See [Schedule Replicas by Topology Labels](/schedule-replicas-by-topology-labels.md) for label configuration.
- For the test environment, this risk might not matter, and you can use `--no-labels` to skip the check.
- Data type: `BOOLEAN`
- Default: false

### --skip-create-user

- During the cluster deployment, tiup-cluster checks whether the specified user name in the topology file exists or not. If not, it creates one. To skip this check, you can use the `--skip-create-user` option.
- Data type: `BOOLEAN`
- Default: false

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The log of scaling out.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

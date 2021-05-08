---
title: TiUP Cluster
---

# TiUP Cluster

TiUP Cluster is a cluster management component of TiUP written in Golang. You can use the TiUP Cluster component to perform daily operations and maintenance, including deploying, starting, shutting down, destroying, elastic scaling, upgrading TiDB clusters, and managing TiDB cluster parameters.

## Syntax

```shell
tiup cluster [command] [flags]
```

`[command]` is the name of the command. For the supported commands, refer to the [command list](#command-list) below.

## Options

### --ssh

- Specifies the SSH client to connect to the remote end (the machine where the TiDB service is deployed) for the command execution.
- Data type: `STRING`
- Supported values:

    - `builtin`: uses the easyssh client built in tiup-cluster as the SSH client.
    - `system`: uses the default SSH client of the current operating system.
    - `none`: The SSH client is not used. The deployment is only for the current machine.

- If this option is not specified in the command, `builtin` is used as the default value.

### --ssh-timeout

- Specifies the SSH connection timeout in seconds.
- Data type: `UINT`
- If this option is not specified in the command, the default timeout is `5` seconds.

### --wait-timeout

- Specifies the maximum waiting time (in seconds) for each step in the operation process. The operation process consists of many steps, such as specifying systemctl to start or stop services, and waiting for ports to be online or offline. Each step may take several seconds. If the execution time of a step exceeds the specified timeout, the step exits with an error.
- Data type: `UINT`
- If this option is not specified in the command, the maximum waiting time for each step is `120` seconds.

### -y, --yes

- Skips the secondary confirmation of all risky operations. Using this option is not recommended, unless you are using a script to call TiUP.
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### -v, --version

- Prints the current version of TiUP Cluster.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### -h, --help

- Prints the help information of the related commands.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Command list

- [import](/tiup/tiup-component-cluster-import.md): imports a cluster deployed by Ansible
- [template](/tiup/tiup-component-cluster-template.md): outputs the topology template
- [check](/tiup/tiup-component-cluster-check.md): checks a cluster before and after the deployment
- [deploy](/tiup/tiup-component-cluster-deploy.md): deploys a cluster based on a specified topology
- [list](/tiup/tiup-component-cluster-list.md): queries the list of deployed clusters
- [display](/tiup/tiup-component-cluster-display.md): displays the status of a specified cluster
- [start](/tiup/tiup-component-cluster-start.md): starts a specified cluster
- [stop](/tiup/tiup-component-cluster-stop.md): stops a specified cluster
- [restart](/tiup/tiup-component-cluster-restart.md): restarts a specified cluster
- [scale-in](/tiup/tiup-component-cluster-scale-in.md): scales in a specified cluster
- [scale-out](/tiup/tiup-component-cluster-scale-out.md): scales out a specified cluster
- [upgrade](/tiup/tiup-component-cluster-upgrade.md): upgrades a specified cluster
- [prune](/tiup/tiup-component-cluster-prune.md): cleans up the instances in the Tombstone status for a specified cluster
- [edit-config](/tiup/tiup-component-cluster-edit-config.md): modifies the configuration of a specified cluster
- [reload](/tiup/tiup-component-cluster-reload.md): reloads the configuration of a specified cluster
- [patch](/tiup/tiup-component-cluster-patch.md): replaces a service in a deployed cluster
- [rename](/tiup/tiup-component-cluster-rename.md): renames a cluster
- [clean](/tiup/tiup-component-cluster-clean.md): deletes data from the specified cluster
- [destroy](/tiup/tiup-component-cluster-destroy.md): destroys a specified cluster
- [audit](/tiup/tiup-component-cluster-audit.md): queries the operation audit log of a specified cluster
- [replay](/tiup/tiup-component-cluster-replay.md): retries the specified command
- [enable](/tiup/tiup-component-cluster-enable.md): enables the auto-enabling of the cluster service after a machine is restarted.
- [disable](/tiup/tiup-component-cluster-disable.md): disables the auto-enabling of the cluster service after a machine is restarted.
- [help](/tiup/tiup-component-cluster-help.md): prints the help information
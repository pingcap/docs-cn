---
title: TiUP DM
---

# TiUP DM

Similar to [TiUP Cluster](/tiup/tiup-component-cluster.md) which is used to manage TiDB clusters, TiUP DM is used to manage DM clusters. You can use the TiUP DM component to perform daily operations and maintenance tasks of DM clusters, including deploying, starting, stopping, destroying, elastic scaling, upgrading DM clusters, and managing the configuration parameters of DM clusters.

## Syntax

```shell
tiup dm [command] [flags]
```

`[command]` is used to pass the name of the command. See the [command list](#list-of-commands) for supported commands.

## Options

### --ssh

- Specifies the SSH client to connect to the remote end (the machine where the TiDB service is deployed) for the command execution.
- Data type:`STRING`
- Support values:

    - `builtin`: Uses the built-in easyssh client of tiup-cluster as the SSH client.
    - `system`: Uses the default SSH client of the current operating system.
    - `none`: No SSH client is used. The deployment is only for the current machine.

- If this option is not specified in the command, `builtin` is used as the default value.

### --ssh-timeout

- Specifies the SSH connection timeout in seconds.
- Data type: `UINT`
- If this option is not specified in the command, the default timeout is `5` seconds.

### --wait-timeout

- Specifies the maximum waiting time (in seconds) for each step in the operation process. The operation process consists of many steps, such as specifying systemctl to start or stop services, and waiting for ports to be online or offline. Each step may take several seconds. If the execution time of a step exceeds the specified timeout, the step exits with an error.
- Data type:`UINT`
- If this option is not specified in the command, the maximum waiting time for each steps is `120` seconds.

### -y, --yes

- Skips the secondary confirmation of all risky operations. It is not recommended to use this option unless you use a script to call TiUP.
- Data type:`BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### -v, --version

- Prints the current version of TiUP DM.
- Data type:`BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### -h, --help

- Prints help information about the specified command.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## List of commands

- [import](/tiup/tiup-component-dm-import.md): Imports a DM v1.0 cluster deployed by DM-Ansible.
- [template](/tiup/tiup-component-dm-template.md): Outputs the topology template.
- [deploy](/tiup/tiup-component-dm-deploy.md): Deploys a cluster based on a specified topology.
- [list](/tiup/tiup-component-dm-list.md): Queries the list of deployed clusters.
- [display](/tiup/tiup-component-dm-display.md): Displays the status of a specified cluster.
- [start](/tiup/tiup-component-dm-start.md): Starts a specified cluster.
- [stop](/tiup/tiup-component-dm-stop.md): Stops a specified cluster.
- [restart](/tiup/tiup-component-dm-restart.md): Restarts a specified cluster.
- [scale-in](/tiup/tiup-component-dm-scale-in.md): Scales in a specified cluster.
- [scale-out](/tiup/tiup-component-dm-scale-out.md): Scales out a specified cluster.
- [upgrade](/tiup/tiup-component-dm-upgrade.md): Upgrades a specified cluster.
- [prune](/tiup/tiup-component-dm-prune.md): Cleans up instances in the Tombstone status for a specified cluster.
- [edit-config](/tiup/tiup-component-dm-edit-config.md): Modifies the configuration of a specified cluster.
- [reload](/tiup/tiup-component-dm-reload.md): Reloads the configuration of a specified cluster.
- [patch](/tiup/tiup-component-dm-patch.md): Replaces a specified service in a deployed cluster.
- [destroy](/tiup/tiup-component-dm-destroy.md): Destroys a specified cluster.
- [audit](/tiup/tiup-component-dm-audit.md): Queries the operation audit log of a specified cluster.
- [replay](/tiup/tiup-component-dm-replay.md): Replays the specified commands
- [enable](/tiup/tiup-component-dm-enable.md): Enables the auto-enabling of the cluster service after a machine is restarted.
- [disable](/tiup/tiup-component-dm-disable.md): Disables the auto-enabling of the cluster service after a machine is restarted.
- [help](/tiup/tiup-component-dm-help.md): Prints help information.

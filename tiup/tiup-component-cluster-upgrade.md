---
title: tiup cluster upgrade
---

# tiup cluster upgrade

The `tiup cluster upgrade` command is used to upgrade the specified cluster to a specific version.

## Syntax

```shell
tiup cluster upgrade <cluster-name> <version> [flags]
```

- `<cluster-name>`: the cluster name to operate on. If you forget the cluster name, you can check it with the [cluster list](/tiup/tiup-component-cluster-list.md) command.
- `<version>`: the target version to upgrade to, such as `v6.5.0`. Currently, it is only allowed to upgrade to a version higher than the current cluster, that is, no downgrade is allowed. It is also not allowed to upgrade to the nightly version.

## Options

### --force

- To upgrade the cluster, you need to ensure that the cluster is currently started. In some cases, you might want to upgrade when the cluster is not started. At this time, you can use `--force` to ignore the error during the upgrade, forcibly replace the binary file and start the cluster.
- Data type: `BOOLEAN`
- Default: false

> **Note:**
>
> Forcing an upgrade of the cluster that is providing services might result in service unavailability. Unstarted clusters are started automatically after a successful upgrade.

### --transfer-timeout

- When upgrading PD or TiKV, the leader of the upgraded node is migrated to other nodes first. The migration process takes some time, and you can set the maximum wait time (in seconds) by the `-transfer-timeout` option. After the timeout, the wait is skipped and the service is upgraded directly.
- Data type: `uint`
- Default: 300

> **Note:**
>
> If the wait is skipped and the service is upgraded directly, the service performance might jitter.

### --ignore-config-check

- After the binary is updated, a configuration check is performed on the TiDB, TiKV and PD components using `<binary> --config-check <config-file>`. `<binary>` is the path to the newly deployed binary and `<config-file>` is the configuration file generated based on the user configuration. To skip this check, you can use the `--ignore-config-check` option.
- Data type: `BOOLEAN`
- Default: false

### --offline

- Declares that the current cluster is not running. When this option is specified, TiUP does not evict the service leader to another node or restart the service, but only replaces the binary files of the cluster components.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The log of the upgrading progress.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

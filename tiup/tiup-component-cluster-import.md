---
title: tiup cluster import
---

# tiup cluster import

Before TiDB v4.0, TiDB clusters were mainly deployed using TiDB Ansible. For TiDB v4.0 and later releases, TiUP Cluster provides the `import` command to transfer the clusters to the tiup-cluster component for management.

> **Note:**
>
> + After importing the TiDB Ansible configuration to TiUP for management, **DO NOT** use TiDB Ansible for cluster operations anymore. Otherwise, conflicts might be caused due to inconsistent meta information.
> + If the clusters deployed using TiDB Ansible are in any of the following situations, do not use the `import` command.
> + Clusters with TLS encryption enabled
> + Pure KV clusters (clusters without TiDB instances)
> + Clusters with Kafka enabled
> + Clusters with Spark enabled
> + Clusters with TiDB Lightning/TiKV Importer enabled
> + Clusters still using the old `push` mode to collect monitoring metrics (if you keep the default mode `pull` unchanged, using the `import` command is supported)
> + Clusters in which the non-default ports (the ports configured in the `group_vars` directory are compatible) are separately configured in the `inventory.ini` configuration file using `node_exporter_port` / `blackbox_exporter_port`

## Syntax

```shell
tiup cluster import [flags]
```

## Options

### -d, --dir

- Specifies the directory where TiDB Ansible is located.
- Data type: `STRING`
- The option is enabled by default with the current directory (the default value) passed in.

### --ansible-config

- Specifies the path of the Ansible configuration file.
- Data type: `STRING`
- The option is enabled by default with `. /ansible.cfg` (the default value) passed in.

### --inventory

- Specifies the name of the Ansible inventory file.
- Data type: `STRING`
- The option is enabled by default with `inventory.ini` (the default value) passed in.

### --no-backup

- Controls whether to disable the backup of files in the directory where TiDB Ansible is located.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. After a successful import, everything in the directory specified by the `-dir` option is backed up to the `${TIUP_HOME}/.tiup/storage/cluster/clusters/{cluster-name}/ansible-backup` directory. If there are multiple inventory files (when multiple clusters are deployed) in this directory, it is recommended to enable this option. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### --rename

- Renames the imported cluster.
- Data type: `STRING`
- Default: NULL. If this option is not specified in the command, the cluster_name specified in inventory is used as the cluster name.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

Shows the logs of the import process.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

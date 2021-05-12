---
title: tiup dm import
---

# tiup dm import

In DM v1.0, the cluster is basically deployed using TiDB Ansible. TiUP DM provides the `import` command to import v1.0 clusters and redeploy the clusters in DM v2.0.

> **Note:**
>
> - The command does not support importing DM Portal components from DM v1.0 clusters.
> - Before importing the cluster, stop running the original cluster first.
> - For data migration tasks that need to be upgraded to v2.0, do not execute `stop-task` on these tasks.
> - The command only supports importing to DM v2.0.0-rc.2 and later versions.
> - The `import` command is used to import a DM v1.0 cluster to a new DM v2.0 cluster. If you need to import data migration tasks to an existing v2.0 cluster, refer to [Manually Upgrade TiDB Data Migration from v1.0.x to v2.0.x](https://docs.pingcap.com/tidb-data-migration/stable/manually-upgrade-dm-1.0-to-2.0)
> - The deployment directories of some components might be different from those in the original cluster. You can check it with the `display` command.
> - Before importing the cluster, run `tiup update --self && tiup update dm` to upgrade TiUP DM components to the latest version.
> - After the cluster is imported, there is only one DM-master node in the cluster. You can refer to [the `scale out` command](/tiup/tiup-component-dm-scale-out.md) to scale out the DM-master node.

## Syntax

```shell
tiup dm import [flags]
```

## Options

### -v, --cluster-version

- Specifies the version number for redeploying. You must use a version later than v2.0.0-rc.2 (including v2.0.0-rc.2).
- Data type: `STRING`
- This option is **required** to execute the command.

### -d, --dir

- Specifies the directory of TiDB Ansible.
- Data type: `STRING`
- If this option is not specified in the command, the current directory is the default directory.

### --inventory

- Specifies the name of the Ansible inventory file.
- Data type: `STRING`
- If this option is not specified in the command, the default file name is `"inventory.ini"`.

### --rename

- Renames the imported cluster.
- Data type: `STRING`
- If this option is not specified in the command, the default cluster name is the `cluster_name` specified in the inventory file.

### -h, --help

- Prints help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Outputs

The log of the importing process.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)

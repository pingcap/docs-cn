---
title: tiup cluster meta backup
summary: The TiUP meta file is crucial for cluster operation and maintenance. Use `tiup cluster meta backup` to regularly back up the file. Use `tiup dm list` to check the cluster name. Specify the target directory with `--file` option. Use `-h, --help` for help information. The output includes execution logs of tiup-cluster.
---

# tiup cluster meta backup

The TiUP meta file is used for cluster operation and maintenance (OM). If this file is lost, you cannot use TiUP to manage the cluster. To avoid this situation, you can use the `tiup cluster meta backup` command to back up the TiUP meta file regularly.

## Syntax

```shell
tiup cluster meta backup <cluster-name> [flags]
```

`<cluster-name>` is the name of the cluster to be operated on. If you forget the cluster name, you can check it using the [`tiup dm list`](/tiup/tiup-component-dm-list.md) command.

## Options

### --file (string, defaults to the current directory)

Specifies the target directory to store the TiUP meta backup file.

### -h, --help

- Prints the help information.
- Data type: `Boolean`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Output

The execution logs of tiup-cluster.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

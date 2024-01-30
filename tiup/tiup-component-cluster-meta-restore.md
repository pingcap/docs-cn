---
title: tiup cluster meta restore
summary: To restore the TiUP meta file, use the `tiup cluster meta restore` command with cluster name and backup file path. The restore operation overwrites the current meta file, so it should only be done when the file is lost. The `-h` or `--help` option prints help information. The output includes the execution logs of tiup-cluster.
---

# tiup cluster meta restore

To restore the TiUP meta file, you can use the `tiup cluster meta restore` command to restore from the backup file.

## Syntax

```shell
tiup cluster meta restore <cluster-name> <backup-file> [flags]
```

- `<cluster-name>` is the name of the cluster to be operated on.
- `<backup-file>` is the path to the TiUP meta backup file.

> **Note:**
>
> The restore operation overwrites the current meta file. It is recommended to restore the meta file only when it is lost.

## Options

### -h, --help

- Prints the help information.
- Data type: `Boolean`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Output

The execution logs of tiup-cluster.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

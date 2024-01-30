---
title: tiup dm prune
summary: When scaling in the cluster, a small amount of metadata in etcd may not be cleaned up, but it usually doesn't cause any problems. If needed, you can manually execute the "tiup dm prune" command to clean up the metadata. The command syntax is "tiup dm prune <cluster-name> [flags]". The option "-h, --help" prints help information and the output is the log of the cleanup process.
---

# tiup dm prune

When you scale in the cluster(/tiup/tiup-component-dm-scale-in.md), a small amount of metadata in etcd is not cleaned up, which usually causes no problem. If you need to clean up the metadata, you can manually execute the `tiup dm prune` command.

## Syntax

```shell
tiup dm prune <cluster-name> [flags]
```

## Option

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The log of the cleanup process.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)

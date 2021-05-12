---
title: tiup dm prune
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

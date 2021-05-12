---
title: tiup cluster prune
---

# tiup cluster prune

When [scaling in the cluster](/tiup/tiup-component-cluster-scale-in.md), for some components, TiUP does not immediately stop their services or delete their data. You need to wait for the data scheduling to complete and then manually execute the `tiup cluster prune` command to clean up.

## Syntax

```shell
tiup cluster prune <cluster-name> [flags]
```

## Option

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The log of the cleanup process.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

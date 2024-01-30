---
title: tiup cluster prune
summary: When scaling in the cluster, TiUP does not immediately stop services or delete data for some components. You must wait for data scheduling to complete and then manually execute the 'tiup cluster prune' command to clean up. The syntax is 'tiup cluster prune <cluster-name> [flags]'. The option '-h, --help' prints help information and the output is the log of the cleanup process.
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

---
title: tiup cluster audit cleanup
---

# tiup cluster audit cleanup

The `tiup cluster audit cleanup` command is used to clean up the logs generated in executing the `tiup cluster`command.

## Syntax

```shell
tiup cluster audit cleanup [flags]
```

## Options

### --retain-days

- Specifies the days for which logs are retained.
- Data type: `INT`
- Default value: `60`, in the unit of day.
- By default, logs generated within the last 60 days are retained, which means logs generated before 60 days are removed.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default value: `false`
- To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Output

```shell
clean audit log successfully
```

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)

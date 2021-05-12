---
title: tiup clean
---

# tiup clean

The `tiup clean` command is used to clear the data generated during component operation.

## Syntax

```shell
tiup clean [name] [flags]
```

The value of `[name]` is the `Name` field output by the [`status` command](/tiup/tiup-command-status.md). If `[name]` is omitted, you must add the `--all` option in the `tiup clean` command.

## Option

### --all

- Clears all operation records
- Data type: Boolean
- Default: false

## Output

```
Clean instance of `%s`, directory: %s
```

[<< Back to the previous page - TiUP Reference command list](/tiup/tiup-reference.md#command-list)

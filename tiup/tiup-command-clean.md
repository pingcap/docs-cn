---
title: tiup clean
---

# tiup clean

The `tiup clean` command is used to clear the data generated during component operation.

## Syntax

```sh
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

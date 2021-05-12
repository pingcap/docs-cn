---
title: tiup dm audit
---

# tiup dm audit

The `tiup dm audit` command is used to view historical commands executed on all clusters and the execution log of each command.

## Syntax

```shell
tiup dm audit [audit-id] [flags]
```

- If you do not fill in the `[audit-id]`, the table of operation records is output in reverse chronological order. The first column is the `audit-id`.
- If you fill in the `[audit-id]`, the execution log of the specified `audit-id` is checked.

## Option

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

- If `[audit-id]` is specified, the corresponding execution log is output.
- If `[audit-id]` is not specified, a table with the following fields is output:
    - ID: the `audit-id` corresponding to this record
    - Time: the execution time of the command corresponding to the record
    - Command: the command corresponding to the record

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)

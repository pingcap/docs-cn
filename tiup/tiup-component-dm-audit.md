---
title: tiup dm audit
summary: The `tiup dm audit` command is used to view historical commands executed on all clusters and the execution log of each command. If `[audit-id]` is not filled, the table of operation records is output in reverse chronological order, showing the `audit-id`, execution time, and command. If `[audit-id]` is filled, the execution log of the specified `audit-id` is checked. The `-h, --help` option prints help information. If `[audit-id]` is specified, the corresponding execution log is output. If not specified, a table with the fields ID, Time, and Command is output.
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

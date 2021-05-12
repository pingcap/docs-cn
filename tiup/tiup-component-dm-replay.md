---
title: tiup dm replay
---

# tiup dm replay

When you perform a cluster operation such as upgrade or restart, the operation might fail due to cluster environment issues. If you re-perform the operation, you need to perform all the steps from the very beginning. If the cluster is large, re-performing these steps will take a long time. In this case, you can use the `tiup dm replay` command to retry the failed commands and skip the successfully performed steps.

## Syntax

```shell
tiup dm replay <audit-id> [flags]
```

- `<audit-id>`: the `audit-id` of the command to be retried. You can view the historical commands and their `audit-id`s using the [`tiup dm audit`](/tiup/tiup-component-dm-audit.md) command.

## Option

### -h, --help

Prints the help information.

## Output

The output of the command corresponding to `<audit-id>`.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)

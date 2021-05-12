---
title: tiup env
---

# tiup env

TiUP provides users with flexible and customized interfaces, some of which are implemented using environment variables. The `tiup env` command is used to query the user-defined environment variables that TiUP supports and their values.

## Syntax

```shell
tiup env [name1...N]
```

`[name1...N]` is used to view the specified environment variables. If it is not specified, all supported environment variables are viewed by default.

## Option

None

## Output

- If `[name1...N]` is not specified, a list of "{key}"="{value}" is output.
- If `[name1...N]` is specified, the "{value}" list is output in order.

In the above output, if `value` is empty, it means that the value of the environment variable is not set. In this case, TiUP uses the default value.

[<< Back to the previous page - TiUP Reference command list](/tiup/tiup-reference.md#command-list)

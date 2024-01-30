---
title: tiup dm help
summary: The tiup-dm command-line interface provides a wealth of help information, which can be accessed using the `help` command or the `--help` option. The syntax for accessing help is `tiup dm help [command] [flags]`, where `[command]` specifies the command for which help information is needed. The `-h` or `--help` option prints the help information. The output is the help information for the specified command or `tiup-dm`.
---

# tiup dm help

tiup-dm command-line interface provides users with a wealth of help information. You can view it via the `help` command or the `--help` option. Basically, `tiup dm help <command>` is equivalent to `tiup dm <command> --help`.

## Syntax

```shell
tiup dm help [command] [flags]
```

`[command]` is used to specify the help information of which command that users need to view. If it is not specified, the help information of `tiup-dm` is viewed.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: false

## Output

The help information of `[command]` or `tiup-dm`.

[<< Back to the previous page - TiUP DM command list](/tiup/tiup-component-dm.md#command-list)

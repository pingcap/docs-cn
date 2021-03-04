---
title: tiup cluster help
---

# tiup cluster help

tiup-cluster 在命令行界面为用户提供了丰富的帮助信息，这些帮助信息可以通过 `help` 命令或者 `--help` 参数获得。`tiup cluster help <command>` 基本等价于 `tiup cluster <command> --help`。

## 语法

```sh
tiup cluster help [command] [flags]
```

`[command]` 用于指定要查看哪个命令的帮助信息，若不指定，则查看 tiup-cluster 自身的帮助信息。

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

`[command]` 或 tiup-cluster 的帮助信息。

---
title: tiup dm help
---

# tiup dm help

tiup-dm 在命令行界面为用户提供了丰富的帮助信息，这些帮助信息可以通过 `help` 命令或者 `--help` 参数获得。基本上，`tiup dm help <command>` 等价于 `tiup dm <command> --help`。

## 语法

```shell
tiup dm help [command] [flags]
```

`[command]` 用于指定要查看哪个命令的帮助信息，若不指定，则查看 tiup-dm 自身的帮助信息。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

`[command]` 或 tiup-dm 的帮助信息。
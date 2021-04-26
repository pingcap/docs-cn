---
title: tiup clean
---

# tiup clean

命令 `tiup clean` 用于清除组件运行过程中产生的数据。

## 语法

```shell
tiup clean [name] [flags]
```

`[name]` 取值为 [status 命令](/tiup/tiup-command-status.md)输出的 `Name` 字段。若省略 `[name]`，则必须配合 `--all` 使用。

## 选项

### --all

- 清除所有运行记录。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

```
Clean instance of `%s`, directory: %s
```

---
title: tiup clean
---

# tiup clean

命令 `tiup clean` 用于清除组件运行过程中产生的数据。

## 语法

```sh
tiup clean [name] [flags]
```

`[name]` 取值为 [status 命令](/tiup/tiup-command-status.md)输出的 `Name` 字段。若省略 `[name]`，则必须配合 `--all` 使用。

## 选项

### --all (boolean, 默认 false)

清除所有运行记录。

## 输出

```
Clean instance of `%s`, directory: %s
```

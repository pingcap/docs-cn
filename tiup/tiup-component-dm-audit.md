---
title: tiup dm audit
---

# tiup dm audit

命令 `tiup dm audit` 可以用于查看执行在所有集群上的历史命令，以及每个命令的执行日志。

## 语法

```sh
tiup dm audit [audit-id] [flags]
```

- 若不填写 `[audit-id]` 则按时间倒序输出操作记录的表格，第一列为 audit-id
- 若填写 `[audit-id]` 则查看指定的 audit-id 的执行日志

## 选项

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

- 若指定 `[audit-id]`，则输出对应的执行日志
- 若不指定 `[audit-id]` 则输出含有以下字段的表格：
    - ID：该条记录对应的 audit-id
    - Time：该条记录对应的命令执行时间
    - Command：该条记录对应的命令

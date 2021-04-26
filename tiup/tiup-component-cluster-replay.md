---
title: tiup cluster replay
---

# tiup cluster replay

对集群执行升级或重启等操作时，操作有可能因为环境的原因而偶然失败。这时如果重新执行操作，需要从头开始所有步骤。如果集群规模较大，会耗费较长时间。此时可以使用 `tiup cluster replay` 命令重试刚才失败的命令，并且跳过已经成功的步骤。

## 语法

```shell
tiup cluster replay <audit-id> [flags]
```

- `<audit-id>` 代表要重试的命令对应的 `audit-id`。使用 [`tiup cluster audit`](/tiup/tiup-component-cluster-audit.md) 可查看历史命令及其 `audit-id`。

## 选项

### -h, --help

输出帮助信息。

## 输出

`<audit-id>` 对应的命令的输出。

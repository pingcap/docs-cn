---
title: tiup cluster replay
---

# tiup cluster replay

在执行升级/重启集群等操作时，有可能因为环境的原因导致偶然失败，这时如果重新执行操作，会从头开始，如果集群规模较大，会比较浪费时间。使用 `tiup cluster replay` 命令，可以重试刚才失败的命令，并且跳过已经成功的步骤。

## 语法

```sh
tiup cluster replay <audit-id> [flags]
```

- `<audit-id>` 代表要重试的命令对应的 audit-id，历史命令及其 audit-id 可以通过命令 [tiup cluster audit](/tiup/tiup-component-cluster-audit.md) 查看

## 选项

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

`<audit-id>` 对应的命令的输出。
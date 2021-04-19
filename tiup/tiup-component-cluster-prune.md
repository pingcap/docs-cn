---
title: tiup cluster prune
---

# tiup cluster prune

在[缩容集群](/tiup/tiup-component-cluster-scale-in.md)时，对于某些组件，并不会立即停止服务并删除数据，而是需要等数据调度完成之后，用户手动执行 `tiup cluster prune` 命令清理。

## 语法

```sh
tiup cluster prune <cluster-name> [flags]
```

## 选项

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

清理过程的日志。

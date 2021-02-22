---
title: tiup dm prune
---

# tiup dm prune

在[缩容集群](/tiup/tiup-component-dm-scale-in.md)后，etcd 中仍然会有少量元信息不会被清理，通常不会有问题，如果确实需要清理，可以手动执行 `tiup cluster prune` 命令清理。

## 语法

```sh
tiup dm prune <cluster-name> [flags]
```

## 选项

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

清理过程的日志。

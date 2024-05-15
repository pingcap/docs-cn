---
title: tiup dm prune
summary: tiup dm prune 命令用于在缩容集群后清理 etcd 中的少量元信息。通常情况下不会有问题，但如果需要清理，可以手动执行该命令。语法为 tiup dm prune <cluster-name>，选项包括 -h, --help，输出为清理过程的日志。
---

# tiup dm prune

在[缩容集群](/tiup/tiup-component-dm-scale-in.md)后，etcd 中仍然会有少量元信息不会被清理，通常不会有问题，如果确实需要清理，可以手动执行 `tiup dm prune` 命令清理。

## 语法

```shell
tiup dm prune <cluster-name> [flags]
```

## 选项

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

清理过程的日志。

[<< 返回上一页 - TiUP DM 命令清单](/tiup/tiup-component-dm.md#命令清单)
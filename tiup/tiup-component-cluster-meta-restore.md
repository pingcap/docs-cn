---
title: tiup cluster meta restore
summary: TiUP cluster meta restore 命令用于从备份文件中恢复 TiUP meta 文件。语法为 tiup cluster meta restore <cluster-name> <backup-file>。选项包括 -h, --help，用于输出帮助信息。恢复操作会覆盖当前的 meta 文件，建议仅在 meta 文件丢失的情况下进行恢复。执行日志将作为输出。
---

# tiup cluster meta restore

当需要恢复 TiUP meta 文件时，可以通过 `tiup cluster meta restore` 命令从备份文件中恢复。

## 语法

```shell
tiup cluster meta restore <cluster-name> <backup-file> [flags]
```

- `<cluster-name>` 代表需要执行操作的集群名。
- `<backup-file>` 代表 TiUP meta 备份文件所在的文件路径。

> **注意：**
>
> 恢复操作会覆盖当前的 meta 文件，建议仅在 meta 文件丢失的情况下进行恢复。

## 选项

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-cluster 的执行日志。

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)
---
title: tiup cluster meta backup
summary: TiUP meta 文件丢失会导致无法管理集群。使用“tiup cluster meta backup”命令定期备份文件。命令语法为“tiup cluster meta backup <cluster-name>”。选项包括指定备份文件存储目录和帮助信息。输出为 tiup-cluster 的执行日志。
---

# tiup cluster meta backup

如果运维所需的 TiUP meta 文件丢失，会导致无法继续使用 TiUP 管理集群。你可以通过 `tiup cluster meta backup` 命令定期备份 TiUP meta 文件。

## 语法

```shell
tiup cluster meta backup <cluster-name> [flags]
```

`<cluster-name>` 为要操作的集群名字，如果忘记集群名字可通过[集群列表](/tiup/tiup-component-cluster-list.md)查看。

## 选项

### --file（string，默认为当前目录）

指定 TiUP meta 备份文件存储的目标目录。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-cluster 的执行日志。

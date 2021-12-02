---
title: tiup cluster clean
---

# tiup cluster clean

在测试环境中，有时候需要将集群重置回刚部署的状态，即删除所有数据，命令 `tiup cluster clean` 可以很方便的做到这一点：它会停止集群，然后删除集群上的数据。手工重启集群之后，就能得到一个全新的集群了。

> **警告：**
>
> 该命令一定会先停止集群（即使选择只清理日志也是），生产环境请勿使用。

## 语法

```shell
tiup cluster clean <cluster-name> [flags]
```

`<cluster-name>` 为要清理的集群。

## 选项

### --all

- 同时清理数据和日志，等价于同时指定 `--data` 和 `--log`，若不指定该选项，则必须至少指定以下选项之一：

    - --data：清理数据
    - --log：清理日志

- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --data

该选项开启数据清理，若不指定该选项，也不指定 `--all`，则不清理数据。

### --log

- 该选项开启日志清理，若不指定该选项，也不指定 `--all`，则不清理日志。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --ignore-node（StringArray，默认为空）

指定不需要清理的节点，如需指定多个，重复使用多次该选项：`--ignore-node <node-A> --ignore-node <node-B>`。

### --ignore-role（StringArray，默认为空）

指定不需要清理的角色，如需指定多个，重复使用多次该选项：`--ignore-role <role-A> --ignore-role <role-B>`。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-cluster 的执行日志。

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)
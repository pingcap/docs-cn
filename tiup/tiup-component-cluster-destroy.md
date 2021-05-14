---
title: tiup cluster destroy
---

# tiup cluster destroy

当业务下线之后，如果想将集群占有的机器释放出来让给其他业务使用，需要清理掉集群上的数据以及部署的二进制文件。`tiup cluster destroy` 命令会执行以下操作销毁集群：

- 停止集群
- 对于每个服务，删除其日志目录，部署目录，数据目录
- 如果各个服务的数据目录/部署目录的父目录是由 tiup-cluster 创建的，也一并删除

## 语法

```shell
tiup cluster destroy <cluster-name> [flags]
```

`<cluster-name>` 为要销毁的集群名字。

## 选项

### --force

- 在某些情况下，有可能集群中的某些节点已经宕机，导致无法通过 SSH 连接到节点进行操作，这个时候可以通过 `--force` 选项忽略这些错误。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --retain-node-data（StringArray，默认为空）

指定需要保留数据的节点，如需指定多个，重复使用多次该选项：`--retain-node-data <node-A> --retain-node-data <node-B>`。

### --retain-role-data（StringArray，默认为空）

指定需要保留数据的角色，如需指定多个，重复使用多次该选项：`--retain-role-data <role-A> --retain-role-data <role-B>`。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-cluster 的执行日志。

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)
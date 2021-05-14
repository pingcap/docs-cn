---
title: tiup cluster edit-config
---

# tiup cluster edit-config

在部署集群之后，如果需要再调整集群服务的配置，则可以使用命令 `tiup cluster edit-config`，它会启动一个编辑器（默认为 $EDITOR 环境变量指定的值，当 EDITOR 环境变量不存在时，使用 vi 打开）允许用户修改指定集群的[拓扑文件](/tiup/tiup-cluster-topology-reference.md)。

> **注意：**
> 
> + 修改配置时不能增删机器，增删机器属于[集群扩容](/tiup/tiup-component-cluster-scale-out.md)和[集群缩容](/tiup/tiup-component-cluster-scale-in.md)的功能。
> + 执行完该命令后配置只是在中控机上修改了，要应用配置需要执行 `tiup cluster relaod` 命令来重新加载。

## 语法

```shell
tiup cluster edit-config <cluster-name> [flags]
```

`<cluster-name>` 代表要操作的集群名。

## 选项

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

- 正常情况无输出
- 若修改了不能修改的字段，则保存文件时报错并提示用户重新编辑，不能修改的字段参考[拓扑文件](/tiup/tiup-cluster-topology-reference.md)中的相关描述

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)
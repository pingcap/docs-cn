---
title: tiup cluster scale-in
summary: tiup cluster scale-in 命令用于集群缩容，包括下线 TiKV 和 TiFlash 组件，以及其他组件。特殊处理包括通过 API 执行移除操作，并清理相关数据文件。命令语法为 tiup cluster scale-in <cluster-name>，必须指定要缩容的节点。其他选项包括 --force 用于强制移除宕机节点，--transfer-timeout 设置最长等待时间，-h 输出帮助信息。输出为缩容日志。
---

# tiup cluster scale-in

`tiup cluster scale-in` 命令用于集群缩容，缩容即下线服务，最终会将指定的节点从集群中移除，并删除遗留的相关文件。

## 下线特殊处理

由于 TiKV 和 TiFlash 组件的下线是异步的（需要先通过 API 执行移除操作）并且下线过程耗时较长（需要持续观察节点是否已经下线成功），所以对 TiKV 和 TiFlash 组件做了特殊处理：

- 对 TiKV 和 TiFlash 组件的操作
    - tiup-cluster 通过 API 将其下线后直接退出而不等待下线完成
    - 执行 `tiup cluster display` 查看下线节点的状态，等待其状态变为 Tombstone
    - 执行 `tiup cluster prune` 命令清理 Tombstone 节点，该命令会执行以下操作：
        - 停止已经下线掉的节点的服务
        - 清理已经下线掉的节点的相关数据文件
        - 更新集群的拓扑，移除已经下线掉的节点
- 对其他组件的操作
    - 下线 PD 组件时，会通过 API 将指定节点从集群中删除掉（这个过程很快），然后停掉指定 PD 的服务并且清除该节点的相关数据文件
    - 下线其他组件时，直接停止并且清除节点的相关数据文件

## 语法

```shell
tiup cluster scale-in <cluster-name> [flags]
```

`<cluster-name>` 为要操作的集群名字，如果忘记集群名字可通过[集群列表](/tiup/tiup-component-cluster-list.md)查看。

## 选项

### -N, --node（strings，无默认值，必须非空）

选择要缩容的节点，若缩容多个节点，以逗号分割。

### --force

- 在某些情况下，有可能被缩容的节点宿主机已经宕机，导致无法通过 SSH 连接到节点进行操作，这个时候可以通过 `--force` 选项强制将其从集群中移除。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

> **警告：**
>
> 使用该选项强制移除正在服务和下线中的 TiKV / TiFlash 节点时，这些节点会被直接删除，不等待数据调度完成，因此这个场景下，数据丢失风险非常大。不建议对未宕机的节点使用该选项。如果元数据所在的 Region 发生数据丢失，整个集群将不可用且无法恢复。

### --transfer-timeout（uint，默认 600）

在缩容 PD 或 TiKV 时，会先将被缩容节点的 leader 迁移到其他节点，迁移过程会需要一定时间，可以通过设置 `--transfer-timeout` 设置最长等待时间（单位为秒），超时之后会跳过等待直接缩容服务。

> **注意：**
>
> 若出现跳过等待直接缩容的情况，服务性能可能会出现抖动。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

缩容日志

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)

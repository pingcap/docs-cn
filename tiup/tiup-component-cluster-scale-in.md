---
title: tiup cluster scale-in
---

# tiup cluster scale-in

`tiup cluster scale-in` 命令用于集群缩容，缩容即下线服务，最终会将指定的节点从集群中移除，并删除遗留的相关文件。

由于 TiKV，TiFlash 和 TiDB Binlog 组件的下线是异步的（需要先通过 API 执行移除操作）并且下线过程耗时较长（需要持续观察节点是否已经下线成功），所以对 TiKV，TiFlash 和 TiDB Binlog 组件做了特殊处理：

- 对 TiKV，TiFlash 及 TiDB Binlog 组件的操作:
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

> **注意：**
>
> 强制移除 TiKV 节点不会等待数据调度，移除一个以上正在提供服务的 TiKV 节点会有数据丢失的风险。

### --transfer-timeout（uint，默认 300）

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

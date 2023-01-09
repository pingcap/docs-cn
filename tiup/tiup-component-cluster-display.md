---
title: tiup cluster display
---

# tiup cluster display

如果想查看集群中每个组件的运行状态，逐一登录到各个机器上查看显然很低效。因此，tiup-cluster 提供了 `tiup cluster display` 命令来高效完成这件工作。

## 语法

```shell
tiup cluster display <cluster-name> [flags]
```

`<cluster-name>` 为要操作的集群名字，如果忘记集群名字可通过[集群列表](/tiup/tiup-component-cluster-list.md)查看。

## 选项

### --dashboard

- 默认情况会展示整个集群的所有节点信息，加上该选项后仅展示 dashboard 的信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -N, --node（strings，默认为 []，表示所有节点）

指定要查询的节点，不指定则表示所有节点。该选项的值为以逗号分割的节点 ID 列表，如果不确定要查询节点的 ID，不指定此选项，输出会显示所有节点的 ID 和状态信息。

> **注意：**
>
> 若同时指定了 `-R, --role`，那么将查询它们的交集中的服务状态。

### -R, --role（strings，默认为 []，表示所有角色）

指定要查询的角色，不指定则表示所有角色。该选项的值为以逗号分割的节点角色列表，如果不确定要查询节点的角色，不指定此选项，输出会显示所有节点的角色和状态信息。

> **注意：**
>
> 若同时指定了 `-N, --node`，那么将查询它们的交集中的服务状态。

### --process

- 加上该选项后会增加展示节点的 CPU 和内存的使用信息，默认情况下不展示。
- 数据类型：`BOOLEAN`
- 默认值：`false`
- 在命令中添加该选项，并传入 `true` 或不传值，均可开启此功能。

### --uptime

- 加上该选项后会增加展示节点的 `uptime` 信息，默认情况下不展示。
- 数据类型：`BOOLEAN`
- 默认值：`false`
- 在命令中添加该选项，并传入 `true` 或不传值，均可开启此功能。

### --status-timeout

- 获取节点状态信息的超时时间。
- 数据类型：`INT`
- 默认值：`10`，单位为 `s`。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

- 集群名称
- 集群版本
- SSH 客户端类型
- Dashboard 地址
- 含有以下字段的表格：
    - ID：节点 ID，由 `IP:PORT` 构成
    - Role：该节点部署的服务角色（如 TiDB、 TiKV 等）
    - Host：该节点对应的机器 IP
    - Ports：服务占用的端口号
    - OS/Arch：该节点的操作系统和机器架构
    - Status：该节点服务当前的状态
    - Data Dir：服务的数据目录，`-` 表示没有数据目录
    - Deploy Dir：服务的部署目录

### 节点服务的状态 (Status)

节点服务可能处于如下任一状态：

- 在线 (Up)：节点服务正常运行。
- 离线 (Down) 或无法访问 (Unreachable)：节点服务未启动或对应主机存在网络问题。
- 已缩容下线 (Tombstone)：节点服务上的数据已被完整迁出并缩容完毕。仅 TiKV 或 TiFlash 存在该状态。
- 下线中 (Pending Offline)：节点服务上的数据正在被迁出并缩容。仅 TiKV 或 TiFlash 存在该状态。
- 未知 (Unknown)：未知的节点服务运行状态。

> **注意：**
>
> TiUP 显示的 `Pending Offline`、PD API 返回的 `Offline` 以及 TiDB Dashboard 显示的 `Leaving` 这三个状态的含义相同。

节点服务状态来自于 PD 的调度信息。更详细的描述请参考 [TiDB 数据库的调度 -- 信息收集](/tidb-scheduling.md#信息收集)。

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)

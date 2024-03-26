---
title: TiDB Dashboard 集群信息页面
summary: 查看整个集群中 TiDB、TiKV、PD、TiFlash 组件的运行状态及其所在主机的运行状态
---

# TiDB Dashboard 集群信息页面

该页面上允许用户查看整个集群中 TiDB、TiKV、PD、TiFlash 组件的运行状态及其所在主机的运行状态。

## 访问

可以通过以下两种方法访问集群信息页面：

* 登录 TiDB Dashboard 后，在左侧导航栏中点击**集群信息** (Cluster Info)。

* 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/cluster_info/instance>（将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）。

## 实例列表

点击**实例** (Instances) 可查看实例列表：

![实例](/media/dashboard/dashboard-cluster-info-instances-v650.png)

实例列表列出了该集群中 TiDB、TiKV、PD 和 TiFlash 组件所有实例的概况信息。

表格包含以下列：

- 地址 (Address)：实例地址
- 状态 (Status)：实例的运行状态
- 启动时间 (Up Time)：实例的启动时间
- 版本 (Version)：实例版本号
- Git 哈希值 (Git Hash)：实例二进制对应的 Git 哈希值
- 部署路径 (Deployment Directory)：实例二进制文件所在目录路径

### 实例运行状态 (Status)

实例可能处于如下任一运行状态：

- 在线 (Up)：实例正常运行。
- 离线 (Down) 或无法访问 (Unreachable)：实例未启动或对应主机存在网络问题。
- 已缩容下线 (Tombstone)：实例上的数据已被完整迁出并缩容完毕。仅 TiKV 或 TiFlash 实例存在该状态。
- 下线中 (Leaving)：实例上的数据正在被迁出并缩容。仅 TiKV 或 TiFlash 实例存在该状态。
- 未知 (Unknown)：未知的实例运行状态。

> **注意：**
>
> - TiDB Dashboard 显示的 `Leaving`、PD API 返回的 `Offline` 以及 TiUP 显示的 `Pending Offline` 这三个状态的含义相同。
> - 表格中部分列仅在实例处于在线状态 (Up) 时能显示。

实例运行状态来自于 PD 的调度信息。更详细的描述请参考 [TiDB 数据库的调度 -- 信息收集](/tidb-scheduling.md#信息收集)。

## 主机列表

点击**主机** (Hosts) 可查看主机列表：

![主机](/media/dashboard/dashboard-cluster-info-hosts-v650.png)

主机列表列出了该集群中 TiDB、TiKV、PD 和 TiFlash 组件所有实例对应主机的运行情况。

表格包含以下列：

- 主机地址 (Host Address)：主机 IP 地址
- CPU：主机 CPU 逻辑核心数
- CPU 使用率 (CPU Usage)：主机当前 1 秒的用户态和内核态 CPU 使用率
- 物理内存 (Memory)：主机总计的物理内存大小
- 内存使用率 (Memory Usage)：主机当前内存使用率

> **注意：**
>
> 主机列表信息由各个实例进程给出，因此当主机上所有实例都处于离线状态时，该主机信息将无法显示。

## 磁盘列表

点击**磁盘** (Disks) 可查看磁盘列表：

![磁盘](/media/dashboard/dashboard-cluster-info-disks-v650.png)

磁盘列表列出了该集群中 TiDB、TiKV、PD 和 TiFlash 组件所有实例对应主机磁盘的情况。

表格包含以下列：

- 主机地址 (Host Address)：主机 IP 地址
- 磁盘挂载点 (Mount Directory)：主机上运行实例所在磁盘的挂载路径
- 文件系统 (File System)：主机上运行实例所在磁盘的文件系统类型
- 磁盘容量 (Disk Capacity)：主机上运行实例所在磁盘的总空间大小
- 磁盘使用率 (Disk Usage)：主机上运行实例所在磁盘的空间使用率
- 实例 (Instance)：主机上运行的实例

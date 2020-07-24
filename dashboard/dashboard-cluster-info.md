---
title: TiDB Dashboard 集群信息页面
summary: 查看整个集群中 TiDB、TiKV、PD、TiFlash 组件的运行状态及其所在主机的运行状态
---

# TiDB Dashboard 集群信息页面

该页面上允许用户查看整个集群中 TiDB、TiKV、PD、TiFlash 组件的运行状态及其所在主机的运行状态。

## 访问

可以通过以下两种方法访问集群信息页面：

- 登录后，左侧导航条点击**集群信息**：

  ![访问](/media/dashboard/dashboard-cluster-info-access.png)

- 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/cluster_info/instance>（将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）。

## 实例列表

点击**实例**可查看实例列表：

![实例](/media/dashboard/dashboard-cluster-info-instances.png)

实例列表列出了该集群中 TiDB、TiKV、PD 和 TiFlash 组件所有实例的概况信息。

表格包含以下列：

- 地址：实例地址
- 状态：实例的运行状态
- 启动时间：实例的启动时间
- 版本：实例版本号
- 部署路径：实例二进制文件所在目录路径
- Git 哈希值：实例二进制对应的 Git 哈希值

实例的运行状态有：

- 在线 (Up)：实例正常运行。
- 离线 (Down) 或无法访问 (Unreachable)：实例未启动或对应主机存在网络问题。
- 已缩容下线 (Tombstone)：实例上的数据已被完整迁出并缩容完毕。仅 TiKV 或 TiFlash 实例存在该状态。
- 下线中 (Offline)：实例上的数据正在被迁出并缩容。仅 TiKV 或 TiFlash 实例存在该状态。
- 未知 (Unknown)：未知的实例运行状态。

> **注意：**
>
> 表格中部分列仅在实例处于在线状态时能显示。

## 主机列表

点击**主机**可查看主机列表：

![主机](/media/dashboard/dashboard-cluster-info-hosts.png)

主机列表列出了该集群中 TiDB、TiKV、PD 和 TiFlash 组件所有实例对应主机的运行情况。

表格包含以下列：

- 地址：主机 IP 地址
- CPU：主机 CPU 逻辑核心数
- CPU 使用率：主机当前 1 秒的用户态和内核态 CPU 使用率
- 物理内存：主机总计的物理内存大小
- 内存使用率：主机当前内存使用率
- 部署磁盘：主机上运行实例所在磁盘的文件系统和磁盘挂载路径
- 磁盘使用率：主机上运行实例所在磁盘的空间使用率

> **注意：**
>
> 主机列表信息由各个实例进程给出，因此当主机上所有实例都处于离线状态时，该主机信息将无法显示。

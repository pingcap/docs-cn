---
title: TiDB Dashboard 资源管控页面
summary: 在集群中搜索所有节点上的日志
---

# TiDB Dashboard 资源管控页面

为[使用资源管控 (Resource Control) 实现资源隔离](/tidb-resource-control.md)，集群管理员可以定义资源组 (Resource Group)，通过资源组限定读写的配额。在进行资源规划之前，你需要了解集群的整体容量。该页面可以帮助你查看资源管控相关信息，以便预估集群容量，更好地进行资源配置。

## 访问

可以通过以下两种方法访问资源管控页面：

* 登录 Dashboard 后，左侧导航条点击**资源管控** (**Resource Control**)：

![访问](/media/dashboard/dashboard-resource-manager-access-v710.png)

* 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/resource_manager>（将 `127.0.0.1:2379` 替换为你的实际 PD 地址和端口）。

## 资源管控页面详情

资源管控页面详情页面如下图所示：

![详情页面](/media/dashboard/dashboard-resource-manager-info.png)

整个页面分为三个部分：

- 配置：数据来自于 TiDB 的 [RESOURCE_GROUPS](/information-schema/information-schema-resource-groups#resource_groups) 表中所有资源组 (Resource Group) 的信息。参见 [RESOURCE_GROUPS](/information-schema/information-schema-resource-groups.md) 文档。

- 容量估算：在进行资源规划之前，你需要了解集群的整体容量。目前提供两种估算方式：

    - [基于硬件部署估算容量](/sql-statements/sql-statement-calibrate-resource.md#基于硬件部署估算容量)
    - [根据实际负载估算容量](/sql-statements/sql-statement-calibrate-resource.md#根据实际负载估算容量)

- 监控指标：通过观察面板上的指标，可以了解当前集群整体的资源消耗状态。

### 容量估算

在进行资源规划之前，你需要了解集群的整体容量。目前提供两种估算方式预估当前集群的 [`Request Unit (RU)`](https://docs.pingcap.com/zh/tidb/dev/tidb-resource-control#什么是-request-unit-ru) 的容量：

- [基于硬件部署估算容量](/sql-statements/sql-statement-calibrate-resource.md#基于硬件部署估算容量)

  目前提供了以下不同的负载类型供选择：TPCC、OLTP_WRITE_ONLY、OLTP_READ_WRITE、OLTP_READ_ONLY。

  ![基于硬件部署估算容量](/media/dashboard/dashboard-resource-manager-calibrate-by-hardware.png)
  
  用户资源分组总请求单元为当前除 `default` 用户外的 RU 总量，当小于容量估算值时，会进行提醒。

  系统预定义的 `default` 资源组默认拥有无限用量。当所有用户都属于 `default` 资源组时，资源分配方式与关闭资源管控时相同。

- [根据实际负载估算容量](/sql-statements/sql-statement-calibrate-resource#根据实际负载估算容量)

    ![根据实际负载估算容量](/media/dashboard/dashboard-resource-manager-calibrate-by-workload.png)
  
    可以选定时间范围：

    - 当时间窗口范围 `DURATION` 不满足 10 分钟至 24 小时的条件，会导致报错提醒：`the duration of calibration is too short/long, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s`。
  
    - 当时间窗口范围内的负载过低，会导致报错提醒：`The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead`
  
    可以通过监控指标中的 CPU Usage 来选定合适负载。

### 监控指标

可以选定时间范围，时区与前端用户所处时区相同。

- Total RU Consumed：实时统计的 [Request Unit (RU)](/tidb-resource-control#什么是-request-unit-ru) 总消耗量
- RU Consumed by Resource Groups：以 Resource Group（资源组）为单位进行实时统计的 [Request Unit (RU)](/tidb-resource-control.md#什么是-request-unit-ru) 消耗数量
- TiDB
    - CPU Quota: TiDB 最大 CPU 占用率
    - CPU Usage: 所有 TiDB 实例 CPU 占用率
- TiKV
    - CPU Quota: TiKV 最大 CPU 占用率
    - CPU Usage: 所有 TiKV 实例 CPU 占用率
    - IO MBps: 所有 TiKV 实例 MBps
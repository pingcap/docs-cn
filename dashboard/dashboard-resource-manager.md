---
title: TiDB Dashboard 资源管控页面
summary: 介绍如何使用 TiDB Dashboard 的资源管控页面查看资源管控相关信息，以便预估集群容量，更好地进行资源配置。
---

# TiDB Dashboard 资源管控页面

为使用[资源管控 (Resource Control)](/tidb-resource-control.md) 特性实现资源隔离，集群管理员可以定义资源组 (Resource Group)，通过资源组限定配额。在进行资源规划之前，你需要了解集群的整体容量。该页面可以帮助你查看资源管控相关信息，以便预估集群容量，更好地进行资源配置。

## 访问方式

可以通过以下两种方法访问资源管控页面：

* 登录 TiDB Dashboard 后，在左侧导航栏中点击**资源管控** (Resource Manager)。

* 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/resource_manager>（将 `127.0.0.1:2379` 替换为你的实际 PD 地址和端口）。

## 资源管控详情

资源管控详情页面如下图所示：

![TiDB Dashboard: Resource Manager](/media/dashboard/dashboard-resource-manager-info.png)

资源管控详情页包含以下三个部分：

- 配置 (Configuration)：数据来自于 TiDB 的 `RESOURCE_GROUPS` 表中所有资源组的信息。参见 [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md) 文档。

- 容量估算 (Estimate Capacity)：在进行资源规划之前，你需要了解集群的整体容量。目前提供两种估算方式：

    - [基于硬件部署估算容量](/sql-statements/sql-statement-calibrate-resource.md#基于硬件部署估算容量)
    - [根据实际负载估算容量](/sql-statements/sql-statement-calibrate-resource.md#根据实际负载估算容量)

- 监控指标 (Metrics)：通过观察面板上的指标，可以了解当前集群整体的资源消耗状态。

## 容量估算

在进行资源规划之前，你需要了解集群的整体容量。目前提供两种估算方式预估当前集群的 [Request Unit (RU)](/tidb-resource-control.md#什么是-request-unit-ru#什么是-request-unit-ru) 的容量：

- [基于硬件部署估算容量](/sql-statements/sql-statement-calibrate-resource.md#基于硬件部署估算容量) (Calibrate by Hardware)
    
    目前提供了以下负载类型供选择：
    
    - `tpcc`：数据写入较重的负载，根据类似 `TPC-C` 的负载模型预测。
    - `oltp_write_only`：数据写入较重的负载，根据类似 `sysbench oltp_write_only` 的负载模型预测。
    - `oltp_read_write`：数据读写平衡的负载，根据类似 `sysbench oltp_read_write` 的负载模型预测。
    - `oltp_read_only`：数据读取较重的负载，根据类似 `sysbench oltp_read_only` 的负载模型预测。

  ![基于硬件部署估算容量](/media/dashboard/dashboard-resource-manager-calibrate-by-hardware.png)

    用户资源分组总请求单元 (Total RU of user resource groups) 表示当前除 `default` 用户外的 RU 总量。当该数值小于容量估算值时，系统会发出提醒。系统预定义的 `default` 资源组默认拥有无限用量。当所有用户都属于 `default` 资源组时，资源分配方式与关闭资源管控时相同。

- [根据实际负载估算容量](/sql-statements/sql-statement-calibrate-resource.md#根据实际负载估算容量) (Calibrate by Workload)

    ![根据实际负载估算容量](/media/dashboard/dashboard-resource-manager-calibrate-by-workload.png)

    可以选择 10 分钟至 24 小时的时间范围进行预估。时区与前端用户所处时区相同。

    - 如果时间窗口范围不满足 10 分钟至 24 小时的条件，会报错 `Error 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s`。

    - [根据实际负载估算容量](/sql-statements/sql-statement-calibrate-resource.md#根据实际负载估算容量)功能的监控指标包括 `tikv_cpu_quota`、`tidb_server_maxprocs`、`resource_manager_resource_unit`、`process_cpu_usage`。如果 CPU quota 监控数据为空，会有对应监控项名称的报错，如 `Error 1105 (HY000): There is no CPU quota metrics, metrics 'tikv_cpu_quota' is empty`。
  
    - 如果时间窗口范围内的负载过低或者 `resource_manager_resource_unit` 及 `process_cpu_usage` 监控数据缺失，会报错 `Error 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead`。此外，由于 TiKV 未在 macOS 上监控 CPU 使用率，所以不支持根据实际负载估算容量功能，也会报告此错误。

  可以通过[监控指标](#监控指标)中的 **CPU Usage** 选择合适的时间范围。

> **注意：**
>
> 要使用容量估算功能，当前登录用户需要拥有 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 权限，并拥有部分系统表的访问权限。在使用此功能前，请确保当前用户已拥有这些权限，否则部分功能可能无法正常使用。详情请参考[容量预估的权限要求](/sql-statements/sql-statement-calibrate-resource.md#权限)。

## 监控指标

通过观察面板上的指标，可以了解当前集群整体的资源消耗状态。监控指标及其含义如下：

- Total RU Consumed：实时统计的 Request Unit 总消耗量
- RU Consumed by Resource Groups：以资源组为单位进行实时统计的 Request Unit 消耗数量
- TiDB
    - CPU Quota：TiDB 最大 CPU 占用率
    - CPU Usage：所有 TiDB 实例 CPU 占用率
- TiKV
    - CPU Quota：TiKV 最大 CPU 占用率
    - CPU Usage：所有 TiKV 实例 CPU 占用率
    - IO MBps：所有 TiKV 实例的 I/O 吞吐量
---
title: TiUniManager 概览
summary: 了解 TiUniManager 产品定位，总体介绍。
---

# TiUniManager 概览

TiUniManager 是为分布式数据库 TiDB 打造的管控平台软件和数据库运维管理平台，主要为 TiDB 提供数据库集群管理功能、主机管理功能和平台管理功能，涵盖了数据库运维人员 (DBA) 在 TiDB 上进行的常用运维操作，帮助 DBA 对 TiDB 进行自动化、自助化和可视化管理。

TiUniManager 可帮助 DBA 避免因人工操作失误导致的数据库故障，保障数据库安全、稳定、高效地运行，降低运维 TiDB 的难度，提升 DBA 工作效率。

自 v1.0.2 版本起，TiUniManager 正式开放源码，详见 GitHub 仓库 [tiunimanager](https://github.com/pingcap/tiunimanager)。

## 软件架构

TiUniManager 的软件架构图如下。

![TiUniManager 架构](/media/tiunimanager/tiunimanager-architecture.png)

### Web UI

TiUniManager Web UI 即用户可见的 TiUniManager 界面，展示用户输入以及服务端返回的数据。用户可与该界面进行交互，通过输入数据来获取想要看到的数据，通过界面操作完成对 TiDB 的部署运维相关工作。

### OpenAPI

TiUniManager 提供数据库管理操作的 OpenAPI，帮助用户灵活完成自动化任务或第三方集成。当前 OpenAPI 为实验特性，不建议在生产环境中使用。

### 业务逻辑

TiUniManager 平台核心功能实现层，包括一键创建 TiDB 集群、删除集群、扩容集群、恢复集群、查看集群详情、集群监控报警、错误日志、慢查询日志等。实现层负责以下方面：

- 负责后台定期备份 TiDB 数据库并保存到分布式文件系统。
- 负责管理平台中所有主机信息的导入，主机的上线，记录主机资源使用情况。
- 负责管理平台自身的配置信息，元信息的备份，性能监控等。

## 核心特性

本节介绍 TiUniManager 的核心特性。

### 易用性

TiUniManager 提供 Web UI 界面交互模式，UI 界面即开即用。用户根据规划添加主机形成统一的资源池，通过 TiUniManager 可一键创建指定规格的 TiDB 实例，数分钟内就可部署完成集群并对外提供服务。

数据库管理员 (DBA) 根据业务发展情况可随时弹性扩容 TiDB 容量及服务能力。TiUniManager 集成 DBA 常用的运维操作，所有操作都通过可视化的方式操作，极大提升 DBA 运维 TiDB 效率及易用性。

### 高可靠性

TiUniManager 支持以下特性，保障数据高可靠：

- 支持自动备份 TiDB 数据库。用户可以设置自动备份的周期和时间。
- 支持按备份文件进行数据恢复，且支持恢复到新的实例。为避免在恢复数据过程中影响业务，数据验证通过后 TiUniManager 将业务流量切换到新实例，完成数据回溯。
- 支持将数据备份文件存储在分布式文件系统，通过多副本冗余和副本分布的不同策略（不同机架等）确保数据不会丢失。
- 支持将 TiDB 部署在不同的可用区。TiDB 自身采用多副本的数据存储，TiUniManager 根据调度策略将 TiDB 的副本放在不同的可用区，实现跨机房数据可靠性功能。

### 高可用性

TiUniManager 组件均提供高可用功能，无单点故障，确保平台高可用。

TiDB 自身采用多副本的数据存储，TiUniManager 根据调度策略将 TiDB 的副本放在不同的可用区，并采用业界先进的 Raft 多数派选举算法确保数据 100% 强一致性和高可用。可将副本跨地域部署在不同的数据中心，主副本故障时自动切换，无需人工介入，自动保障业务的连续性，实现真正意义上的异地多活。

## 使用场景

本节介绍 TiUniManager 的使用场景。

### 资源管理

- 支持导入主机
- 查看主机资源列表

### 集群管理

- 支持一键创建（部署） TiDB 集群，创建过程中可选择可用区、版本、规格、节点个数等
- 支持一键接管已有 TiDB 集群
- 支持一键删除 TiDB 集群
- 支持一键弹性扩容 TiDB 集群，可分别扩展计算和存储能力
- 支持一键备份与恢复集群数据
- 支持一键查看监控报警
- 支持一键升级集群版本
- 支持日志管理，包括服务日志和慢查询日志等
- 支持通过集群 ID、名称、标签等参数搜索实例

### 数据备份与恢复

- 支持设置自动备份策略
- 支持一键手工备份
- 支持一键删除备份记录
- 支持从备份记录恢复至新集群

### 数据导入与导出

- 支持从 CSV 文件导入数据到 TiDB 集群
- 支持从 SQL 文件导入数据到 TiDB 集群
- 支持从 TiDB 集群导出数据到 CSV 文件
- 支持从 TiDB 集群导出数据库到 SQL 文件

### 数据同步

- 支持从 TiDB 集群向下游（Kafaka、MySQL、TiDB）数据库同步数据

> **注意：**
>
> 数据同步功能仅支持 TiDB 5.2.2 及以上版本的集群。

### 克隆集群

- 支持克隆一个已有的 TiDB 集群，并创建一个新的 TiDB 集群
- 支持同步克隆和快照克隆两种数据策略

> **注意：**
>
> 同步克隆功能仅支持 TiDB 5.2.2 及以上版本的集群。

### 集群参数管理

- 提供 TiDB 版本对应的参数组模板。关于支持的 TiDB 版本，参见 [TiUniManager 支持的 TiDB 版本](/tiunimanager/tiunimanager-release-notes.md#tiunimanager-支持的-tidb-版本)。
- 提供统一界面查看、修改 TiDB 集群参数

### 工作流任务管理

- 支持查看从 TiUniManager 发起的所有工作流任务记录列表
- 支持查看工作流任务详情

### 系统管理

- 支持 TiUniManager 系统监控和 TiUniManager 主机监控
- 支持查看 TiUniManager 系统日志
- 支持查看 TiUniManager 微服务 Trace 信息

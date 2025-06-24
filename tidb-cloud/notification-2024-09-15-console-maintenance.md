---
title: 2024-09-15 TiDB Cloud 控制台维护通知
summary: 了解 2024 年 9 月 15 日 TiDB Cloud 控制台维护的详细信息，如维护时间窗口、原因和影响。
---

# [2024-09-15] TiDB Cloud 控制台维护通知

本通知描述了你需要了解的 2024 年 9 月 15 日 [TiDB Cloud 控制台](https://tidbcloud.com/)维护的详细信息。

## 维护时间窗口

- 日期：2024-09-15
- 开始时间：8:00 (UTC+0)
- 结束时间：8:10 (UTC+0)
- 持续时间：约 10 分钟

> **注意：**
>
> - 目前，用户无法修改 TiDB Cloud 控制台的维护时间，因此你需要提前做好相应计划。
> - 在接下来的 3 个月内，部分用户可能会遇到额外的 20 分钟维护时间窗口。受影响的用户将提前收到电子邮件通知。

## 维护原因

我们正在升级 TiDB Cloud 控制台的元数据库服务，以提升性能和效率。这项改进旨在为所有用户提供更好的体验，这是我们持续提供高质量服务承诺的一部分。

## 影响

在维护时间窗口期间，你可能会遇到 TiDB Cloud 控制台 UI 和 API 中与创建和更新相关的功能的间歇性中断。但是，你的 TiDB 集群将保持正常的数据读写操作，确保不会对你的在线业务产生不利影响。

### 受影响的 TiDB Cloud 控制台 UI 功能

- 集群级别
    - 集群管理
        - 创建集群
        - 删除集群
        - 扩展集群
        - 暂停或恢复集群
        - 更改集群密码
        - 更改集群流量过滤器
    - 导入
        - 创建导入任务
    - 数据迁移
        - 创建迁移任务
    - Changefeed
        - 创建 changefeed 任务
    - 备份
        - 创建手动备份任务
        - 自动备份任务
    - 恢复
        - 创建恢复任务
    - 数据库审计日志
        - 测试连接性
        - 添加或删除访问记录
        - 启用或禁用数据库审计日志
        - 重启数据库审计日志
- 项目级别
    - 网络访问
        - 创建私有端点
        - 删除私有端点
        - 添加 VPC 对等连接
        - 删除 VPC 对等连接
    - 维护
        - 更改维护时间窗口
        - 延迟任务
    - 回收站
        - 删除集群
        - 删除备份
        - 恢复集群

### 受影响的 TiDB Cloud API 功能

- 集群管理
    - [CreateCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateCluster)
    - [DeleteCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/DeleteCluster)
    - [UpdateCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)
    - [CreateAwsCmek](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek)
- 备份
    - [CreateBackup](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Backup/operation/CreateBackup)
    - [DeleteBackup](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Backup/operation/DeleteBackup)
- 恢复
    - [CreateRestoreTask](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Restore/operation/CreateRestoreTask)
- 导入
    - [CreateImportTask](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import/operation/CreateImportTask)
    - [UpdateImportTask](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import/operation/UpdateImportTask)

## 完成和恢复

一旦维护成功完成，受影响的功能将恢复正常，为你提供更好的体验。

## 获取支持

如果你有任何问题或需要帮助，请联系我们的[支持团队](/tidb-cloud/tidb-cloud-support.md)。我们随时为你解答疑虑并提供必要的指导。
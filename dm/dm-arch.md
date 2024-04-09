---
title: Data Migration 架构
summary: Data Migration 架构包括三个组件：DM-master，DM-worker 和 dmctl。DM-master 负责管理和调度数据迁移任务的各项操作。DM-worker 执行具体的数据迁移任务。dmctl 是用来控制 DM 集群的命令行工具。 DM 集群的拓扑信息、数据迁移任务的运行状态和管理统一入口都由 DM-master 负责。DM-worker 负责持久化保存 binlog 数据、保存数据迁移子任务的配置信息和监控数据迁移子任务的运行状态。dmctl 用来创建、更新或删除数据迁移任务、查看数据迁移任务状态、处理数据迁移任务错误和校验数据迁移任务配置的正确性。 Data Migration 高可用机制可以进一步探索。
---

# Data Migration 架构

DM 主要包括三个组件：DM-master，DM-worker 和 dmctl。

![Data Migration architecture](/media/dm/dm-architecture-2.0.png)

## 架构组件

### DM-master

DM-master 负责管理和调度数据迁移任务的各项操作。

- 保存 DM 集群的拓扑信息
- 监控 DM-worker 进程的运行状态
- 监控数据迁移任务的运行状态
- 提供数据迁移任务管理的统一入口
- 协调分库分表场景下各个实例分表的 DDL 迁移

### DM-worker

DM-worker 负责执行具体的数据迁移任务。

- 将 binlog 数据持久化保存在本地
- 保存数据迁移子任务的配置信息
- 编排数据迁移子任务的运行
- 监控数据迁移子任务的运行状态

有关于 DM-worker 的更多介绍，详见 [DM-worker 简介](/dm/dm-worker-intro.md)。

### dmctl

dmctl 是用来控制 DM 集群的命令行工具。

- 创建、更新或删除数据迁移任务
- 查看数据迁移任务状态
- 处理数据迁移任务错误
- 校验数据迁移任务配置的正确性

有关于 dmctl 的使用介绍，详见 [dmctl 使用](/dm/dmctl-introduction.md)。

## 探索更多

- [Data Migration 高可用机制](/dm/dm-high-availability.md)
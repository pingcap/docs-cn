---
title: TiDB 8.5.5 Release Notes
summary: 了解 TiDB 8.5.5 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.5 Release Notes

发版日期：2026 年 xx 月 xx 日

TiDB 版本：8.5.5

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://pingkai.cn/download#tidb-community)

## 新功能

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 按时间点恢复 (Point-in-time recovery, PITR) 支持从压缩后的日志备份中恢复，以加快恢复速度 [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen)

    从 v9.0.0 开始，压缩日志备份功能提供了离线压缩能力，将非结构化的日志备份数据转换为结构化的 SST 文件，从而实现以下改进：

    - SST 可以被快速导入集群，从而**提升恢复性能**。
    - 压缩过程中消除重复记录，从而**减少空间消耗**。
    - 在确保 RTO (Recovery Time Objective) 的前提下，你可以设置更长的全量备份间隔，从而**降低对业务的影响**。

  更多信息，请参考[用户文档](/br/br-compact-log-backup.md)。

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据库管理

* TiKV 支持优雅关闭 (graceful shutdown) [#17221](https://github.com/tikv/tikv/issues/17221) @[hujiatao0](https://github.com/hujiatao0)

    在关闭 TiKV 服务器时，TiKV 会尽量将其上的 leader 副本转移到其他 TiKV 节点，然后再关闭。该等待期默认为 20 秒，可通过 [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入) 配置项进行调整。若达到该超时时间后仍有 leader 未完成转移，TiKV 将跳过剩余 leader 的转移，直接进入关闭流程。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入)。

* 提升进行中的日志备份与快照恢复的兼容性 [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger)

    从 v9.0.0 开始，当日志备份任务正在运行时，在满足特定条件的情况下，仍然可以执行快照恢复，并且恢复的数据可以被进行中的日志备份正常记录。这样，日志备份可以持续进行，无需在恢复数据期间中断。

    更多信息，请参考[用户文档](/br/br-pitr-manual.md#进行中的日志备份与快照恢复的兼容性)。

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

### 行为变更

### MySQL 兼容性

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
|        |                              |      |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### 系统表

### 其他

## 改进提升

## 错误修复

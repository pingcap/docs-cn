---
title: 平滑升级 TiDB
summary: 本文介绍支持无需手动取消 DDL 的平滑升级集群功能。
---

# 平滑升级 TiDB

> **警告：**
>
> 平滑升级目前为实验特性。

本文档介绍 TiDB 的平滑升级集群功能，支持无需手动取消 DDL 的操作。

从 v7.1.0 起，当将 TiDB 升级至更高的版本时，TiDB 支持平滑升级功能，取消了升级过程中的限制，提供更平滑的升级体验。此功能默认开启，且无开关控制。

## 功能简介

TiDB 引入平滑升级功能前，对于升级过程中的 DDL 操作有如下限制(可以参考[使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md#使用-tiup-升级-tidb)中警告部分)：

1. 在升级过程中，请勿执行 DDL 操作，否则可能会出现行为未定义的问题。
2. 集群中有 DDL 语句正在被执行时（通常为 `ADD INDEX` 和列类型变更等耗时较久的 DDL 语句），请勿进行升级操作。

开启平滑升级后，TiDB 升级过程不再受上述限制。

升级过程中，TiDB 会自动进行以下操作，无需用户干预：

1. 暂停用户的 DDL 操作。
2. 执行升级过程中的系统 DDL 操作。 
3. 恢复被暂停的用户的 DDL 操作。
4. 完成升级。

其中，恢复的 DDL job 仍会按升级前的顺序执行。

## 使用限制

使用平滑升级功能时，需要注意以下限制。

### 用户操作限制

* 在升级前，如果集群中存在正在处理的 canceling DDL job，即有正在被处理的 DDL job 被用户取消了，由于处于 canceling 状态的 job 无法被 `pause`，TiDB 会尝试重试。如果重试失败，会报错并退出升级。

* 在升级过程中，不允许以下操作：

  * 对系统表（`mysql.*`、`information_schema.*`、`performance_schema.*`、`metrics_schema.*`）进行 DDL 操作。

  * 执行手动取消、暂停、恢复 DDL job 操作：`ADMIN CANCEL/PAUSE/RESUME DDL JOBS job_id [, job_id] ...;`。

### 组件使用限制

* 在升级过程中，不支持以下组件操作：

  * BR、Import Data 和通过 ingest 方式导入数据等组件：由于这些操作可能会将处于 paused 状态的 DDL 拷贝到 TiDB 中，而此状态的 DDL 不能自动 resume，可能导致后续 DDL 卡住的情况。因此无法处理此类组件的操作。

  * DM、Import Data 和 TiCDC 等组件。如果在升级过程中使用这些组件向 TiDB 导入 SQL，并且其中包含 DDL 操作，则会阻塞该导入操作，并可能出现未定义错误。
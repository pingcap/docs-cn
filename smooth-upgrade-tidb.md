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

- 在升级过程中执行 DDL 操作，TiDB 可能会出现未定义的行为。
- 在 DDL 操作执行过程中升级 TiDB，TiDB 可能会出现未定义的行为。

引入平滑升级后，TiDB 升级过程不再受上述限制。

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

* 在使用 TiUP 进行升级的场景下，由于 TiUP 升级存在超时时间，如果在升级之前集群中有大量 DDL（超过 300 条）正在处理队列中等待执行，则此次升级可能会失败。

* 在升级过程中，不允许以下操作：

    * 对系统表（`mysql.*`、`information_schema.*`、`performance_schema.*`、`metrics_schema.*`）进行 DDL 操作。

    * 执行手动取消 DDL job 操作：`ADMIN CANCEL DDL JOBS job_id [, job_id] ...;`。

    * 导入数据。

### 工具使用限制

在升级过程中，不支持使用以下工具：

* BR：BR 可能会将处于 paused 状态的 DDL 拷贝到 TiDB 中，而此状态的 DDL 不能自动 resume，可能导致后续 DDL 卡住的情况。

* DM 和 TiCDC：如果在升级过程中使用 DM 和 TiCDC 向 TiDB 导入 SQL，并且其中包含 DDL 操作，则该导入操作会被阻塞，并可能出现未定义错误。

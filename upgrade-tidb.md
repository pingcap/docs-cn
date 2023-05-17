---
title: 平滑升级 TiDB
summary: 本文介绍支持无需手动取消 DDL 的平滑升级集群功能。
---

# 平滑升级 TiDB

此功能用于取消禁止用户 DDL 操作存在于升级过程的限制。本文档介绍了 TiDB 升级过程中对用户 DDL 操作的支持和约束情况。

此功能具体放开的两个限制如下(可以参考[使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md#使用-tiup-升级-tidb)中警告部分)：

1. 在升级过程中，请勿执行 DDL 操作，否则可能会出现行为未定义的问题；
2. 集群中有 DDL 语句正在被执行时（通常为 ADD INDEX 和列类型变更等耗时较久的 DDL 语句），请勿进行升级操作。

## 功能简介

在 TiDB 升级过程中会先暂停用户 DDL 操作，然后执行升级过程中的系统 DDL 操作，再恢复原先的 DDL 操作，最后完整升级。其中恢复的用户 DDL job 还是按升级前的顺序执行。此外，整个升级过程无需用户干预。

## 使用限制

### 用户操作限制

* 在升级前，有正在处理的 canceling DDL job (即有正在被处理的 DDL job 被用户取消了)时，升级会直接报错（因为 canceling 状态的 job 不能被 `pause`）并退出升级。

* 在升级过程中，不允许以下操作：

  * 禁止对系统表（mysql.*、information_schema.*、performance_schema.*、metrics_schema.*）进行 DDL 操作。

  * `ADMIN CANCEL/PAUSE/RESUME DDL JOBS job_id [, job_id] ...;`。

### 组件使用限制

* 升级过程中，不支持的一些组件操作如下：

  * BR，Lightning (Physical Import Mode) 和通过 ingest 方式导入数据等组件：升级过程中不能处理这类组件的操作，是因为这些操作中可能将 paused 状态的 DDL 拷贝到 TiDB。但是此状态的 DDL 不能自动 resume，可能导致后续 DDL 卡住的情况。

  * DM，Lightning (Logical Import Mode) 和 TiCDC 等组件。即在升级过程中，通过此类组件导入 SQL 到 TiDB，且其中有 DDL 操作，那么会导致此导入操作阻塞，此外可能存在未定义错误。

## 支持版本

此功能从 v7.1.0 版本开始引入，且当前为实验特性。

此功能支持版本：从 TiDB v7.1 版本升级至更高的版本。
---
title: Data Migration 故障诊断
category: reference
---

# Data Migration 故障诊断

本文总结了在 DM 工具使用过程中一些常见的问题，并提供了相应的解决方案。

如果你在运行 DM 工具时出现了错误，请尝试以下解决方案：

1. 执行 `query-status` 命令查看任务运行状态以及相关错误输出。

2. 查看与该错误相关的日志文件。日志文件位于 DM-master、DM-worker 部署节点上。然后查看[常见错误](#常见错误)以寻找相应的解决方案。

3. 如果该错误还没有相应的解决方案，并且你无法通过查询日志或监控指标自行解决此问题，你可以联系相关销售人员进行支持。

4. 一般情况下，错误处理完成后，只需使用 dmctl 重启任务即可。

    ```bash
    resume-task ${task name}
    ```

但在某些情况下，你还需要重置数据同步任务。有关何时需要重置以及如何重置，详见[重置数据同步任务](#重置数据同步任务)。

## 常见错误

### 执行 `query-status` 或查看日志时出现 `Access denied for user 'root'@'172.31.43.27' (using password: YES)`

在所有 DM 配置文件中，数据库相关的密码都必须使用经 dmctl 加密后的密文（若数据库密码为空，则无需加密）。有关如何使用 dmctl 加密明文密码，参见[使用 dmctl 加密上游 MySQL 用户密码](/dev/how-to/deploy/data-migration-with-ansible.md#使用-dmctl-加密上游-mysql-用户密码)。

此外，在 DM 运行过程中，上下游数据库的用户必须具备相应的读写权限。在启动同步任务过程中，DM 会自动进行相应权限的前置检查，详见[上游 MySQL 实例配置前置检查](/dev/reference/tools/data-migration/precheck.md)。

### 处理不兼容的 DDL 语句

你需要使用 dmctl 手动处理 TiDB 不兼容的 DDL 语句（包括手动跳过该 DDL 语句或使用用户指定的 DDL 语句替换原 DDL 语句，详见[跳过 (skip) 或替代执行 (replace) 异常的 SQL 语句](/dev/reference/tools/data-migration/skip-replace-sqls.md)）。

> **注意：**
>
> TiDB 目前并不兼容 MySQL 支持的所有 DDL 语句。

## 重置数据同步任务

在以下情况中，你需要重置整个数据同步任务：

- 上游数据库中人为执行了 `RESET MASTER`，造成 relay log 同步出错

- relay log 或上游 binlog event 损坏或者丢失

此时，relay 处理单元通常会发生错误而退出，且无法优雅地自动恢复，因此需要通过手动方式恢复数据同步：

1. 使用 `stop-task` 命令停止当前正在运行的所有同步任务。

2. 使用 Ansible [停止整个 DM 集群](/dev/how-to/deploy/data-migration-with-ansible.md#第-10-步关闭-dm-集群)。

3. 手动清理掉与 binlog event 被重置的 MySQL master 相对应的 DM-worker 的 relay log 目录。

    - 如果是使用 Ansible 部署，relay log 目录即 `<deploy_dir>/relay_log` 目录。
    - 如果是使用二进制文件手动部署，relay log 目录即 relay-dir 参数设置的目录。

4. 清理掉下游已同步的数据。

5. 使用 Ansible [启动整个 DM 集群](/dev/how-to/deploy/data-migration-with-ansible.md#第-9-步部署-dm-集群)。

6. 以新的任务名重启数据同步任务，或设置 `remove-meta` 为 `true` 且 `task-mode` 为 `all`。

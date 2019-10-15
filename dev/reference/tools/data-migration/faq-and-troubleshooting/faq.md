---
title: Data Migration 常见问题
category: reference
---

# Data Migration 常见问题

## DM 是否支持同步阿里 RDS 以及其他云数据库的数据？

DM 仅支持解析标准版本的 MySQL/MariaDB 的 binlog，对于阿里云 RDS 以及其他云数据库没有进行过测试，如果确认其 binlog 为标准格式，则可以支持。

## task 配置中的黑白名单的正则表达式是否支持`非获取匹配`（?!）？

目前不支持，DM 仅支持 golang 标准库的正则，可以通过 [re2-syntax](https://github.com/google/re2/wiki/Syntax) 了解 golang 支持的正则表达式。

## 如果在上游执行的一个 statement 包含多个 DDL 操作，DM 是否支持同步？

DM 会尝试将包含多个 DDL 变更操作的单条语句拆分成只包含一个 DDL 操作的多条语句，但是可能没有覆盖所有的场景。建议在上游执行的一条 statement 中只包含一个 DDL 操作，或者在测试环境中验证一下，如果不支持，可以给 DM 提 [issue](https://github.com/pingcap/dm/issues)。

## 如何处理不兼容的 DDL 语句？

你需要使用 dmctl 手动处理 TiDB 不兼容的 DDL 语句（包括手动跳过该 DDL 语句或使用用户指定的 DDL 语句替换原 DDL 语句，详见[跳过 (skip) 或替代执行 (replace) 异常的 SQL 语句](/dev/reference/tools/data-migration/skip-replace-sqls.md)）。

> **注意：**
>
> TiDB 目前并不兼容 MySQL 支持的所有 DDL 语句。

## 如何重置数据同步任务？

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
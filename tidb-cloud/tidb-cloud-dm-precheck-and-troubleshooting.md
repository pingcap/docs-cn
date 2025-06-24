---
title: 数据迁移的预检查错误、迁移错误和告警
summary: 了解如何解决使用数据迁移时的预检查错误、迁移错误和告警。
---

# 数据迁移的预检查错误、迁移错误和告警

本文档介绍如何在[使用数据迁移功能迁移数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md)时解决预检查错误、排查迁移错误和订阅告警。

## 预检查错误和解决方案

本节介绍数据迁移过程中的预检查错误和相应的解决方案。这些错误会在[使用数据迁移功能迁移数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md)时的**预检查**页面上显示。

解决方案因上游数据库而异。

### 错误消息：检查 mysql server_id 是否大于 0

- Amazon Aurora MySQL 或 Amazon RDS：默认已配置 `server_id`。你不需要配置它。确保使用 Amazon Aurora MySQL 写入实例以支持全量和增量数据迁移。
- MySQL：要为 MySQL 配置 `server_id`，请参见 [Setting the Replication Source Configuration](https://dev.mysql.com/doc/refman/8.0/en/replication-howto-masterbaseconfig.html)。

### 错误消息：检查 mysql binlog 是否已启用

- Amazon Aurora MySQL：参见 [How do I turn on binary logging for my Amazon Aurora MySQL-Compatible cluster](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)。确保使用 Amazon Aurora MySQL 写入实例以支持全量和增量数据迁移。
- Amazon RDS：参见 [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)。
- Google Cloud SQL for MySQL：Google 通过 MySQL 主数据库的时间点恢复功能启用二进制日志记录。参见 [Enable point-in-time recovery](https://cloud.google.com/sql/docs/mysql/backup-recovery/pitr#enablingpitr)。
- MySQL：参见 [Setting the Replication Source Configuration](https://dev.mysql.com/doc/refman/8.0/en/replication-howto-masterbaseconfig.html)。

### 错误消息：检查 mysql binlog_format 是否为 ROW

- Amazon Aurora MySQL：参见 [How do I turn on binary logging for my Amazon Aurora MySQL-Compatible cluster](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)。确保使用 Amazon Aurora MySQL 写入实例以支持全量和增量数据迁移。
- Amazon RDS：参见 [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)。
- MySQL：执行 `set global binlog_format=ROW;`。参见 [Setting The Binary Log Format](https://dev.mysql.com/doc/refman/8.0/en/binary-log-setting.html)。

### 错误消息：检查 mysql binlog_row_image 是否为 FULL

- Amazon Aurora MySQL：`binlog_row_image` 不可配置。此预检查项不会失败。确保使用 Amazon Aurora MySQL 写入实例以支持全量和增量数据迁移。
- Amazon RDS：过程与设置 `binlog_format` 参数类似。唯一的区别是你需要更改的参数是 `binlog_row_image` 而不是 `binlog_format`。参见 [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)。
- MySQL：执行 `set global binlog_row_image = FULL;`。参见 [Binary Logging Options and Variables](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_row_image)。

### 错误消息：检查要迁移的数据库是否在 binlog_do_db/binlog_ignore_db 中

确保已在上游数据库中启用 binlog。参见[检查 mysql binlog 是否已启用](#错误消息检查-mysql-binlog-是否已启用)。之后，根据你收到的消息解决问题：

- 如果消息类似于 `These dbs xxx are not in binlog_do_db xxx`，确保你要迁移的所有数据库都在列表中。参见 [--binlog-do-db=db_name](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#option_mysqld_binlog-do-db)。
- 如果消息类似于 `These dbs xxx are in binlog_ignore_db xxx`，确保你要迁移的所有数据库都不在忽略列表中。参见 [--binlog-ignore-db=db_name](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#option_mysqld_binlog-ignore-db)。

对于 Amazon Aurora MySQL，此预检查项不会失败。确保使用 Amazon Aurora MySQL 写入实例以支持全量和增量数据迁移。

对于 Amazon RDS，你需要更改以下参数：`replicate-do-db`、`replicate-do-table`、`replicate-ignore-db` 和 `replicate-ignore-table`。参见 [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)。

### 错误消息：检查连接并发是否超过数据库的最大连接限制

如果错误发生在上游数据库，按如下方式设置 `max_connections`：

- Amazon Aurora MySQL：过程与设置 `binlog_format` 类似。唯一的区别是你更改的参数是 `max_connections` 而不是 `binlog_format`。参见 [How do I turn on binary logging for my Amazon Aurora MySQL-Compatible cluster](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)。
- Amazon RDS：过程与设置 `binlog_format` 类似。唯一的区别是你更改的参数是 `max_connections` 而不是 `binlog_format`。参见 [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)。
- MySQL：按照文档 [max_connections](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_connections) 配置 `max_connections`。

如果错误发生在 TiDB Cloud 集群中，按照文档 [max_connections](https://docs.pingcap.com/tidb/stable/system-variables#max_connections) 配置 `max_connections`。

## 迁移错误和解决方案

本节介绍迁移过程中可能遇到的问题和解决方案。这些错误消息会显示在**迁移任务详情**页面上。

### 错误消息："迁移所需的二进制日志在源数据库上不再存在。请确保二进制日志文件保留足够长的时间以确保迁移成功。"

此错误表示要迁移的 binlog 已被清理，只能通过创建新任务来恢复。

确保增量迁移所需的 binlog 存在。建议配置 `expire_logs_days` 以延长 binlog 的保留时间。如果某些迁移任务需要 binlog，请不要使用 `purge binary log` 清理 binlog。

### 错误消息："使用给定参数连接源数据库失败。请确保源数据库已启动并可以使用给定参数连接。"

此错误表示连接源数据库失败。检查源数据库是否已启动，并且可以使用指定的参数连接。确认源数据库可用后，你可以尝试点击**重启**来恢复任务。

### 迁移任务中断并包含错误 "driver: bad connection" 或 "invalid connection"

此错误表示连接下游 TiDB 集群失败。检查下游 TiDB 集群是否处于正常状态（包括 `Available` 和 `Modifying`），并且可以使用任务指定的用户名和密码连接。确认下游 TiDB 集群可用后，你可以尝试点击**重启**来恢复任务。

### 错误消息："使用给定的用户和密码连接 TiDB 集群失败。请确保 TiDB 集群已启动并可以使用给定的用户和密码连接。"

连接 TiDB 集群失败。建议检查 TiDB 集群是否处于正常状态（包括 `Available` 和 `Modifying`）。你可以使用任务指定的用户名和密码连接。确认 TiDB 集群可用后，你可以尝试点击**重启**来恢复任务。

### 错误消息："TiDB 集群存储空间不足。请增加 TiKV 节点存储。"

TiDB 集群存储空间不足。建议[增加 TiKV 节点存储](/tidb-cloud/scale-tidb-cluster.md#change-storage)，然后点击**重启**恢复任务。

### 错误消息："连接源数据库失败。请检查数据库是否可用或是否已达到最大连接数。"

连接源数据库失败。建议检查源数据库是否已启动，数据库连接数是否未达到上限，以及是否可以使用任务指定的参数连接。确认源数据库可用后，你可以尝试点击**重启**恢复任务。

### 错误消息："Error 1273: Unsupported collation when new collation is enabled: 'utf8mb4_0900_ai_ci'"

在下游 TiDB 集群中创建架构失败。此错误表示上游 MySQL 使用的排序规则不被 TiDB 集群支持。

要解决此问题，你可以根据[支持的排序规则](/character-set-and-collation.md#character-sets-and-collations-supported-by-tidb)在 TiDB 集群中创建架构，然后点击**重启**恢复任务。

## 告警

你可以订阅 TiDB Cloud 告警邮件，以便在发生告警时及时获得通知。

以下是关于数据迁移的告警：

- "数据迁移任务在数据导出过程中遇到错误"

    建议操作：检查数据迁移页面上的错误消息，并参见[迁移错误和解决方案](#迁移错误和解决方案)获取帮助。

- "数据迁移任务在数据导入过程中遇到错误"

    建议操作：检查数据迁移页面上的错误消息，并参见[迁移错误和解决方案](#迁移错误和解决方案)获取帮助。

- "数据迁移任务在增量数据迁移过程中遇到错误"

    建议操作：检查数据迁移页面上的错误消息，并参见[迁移错误和解决方案](#迁移错误和解决方案)获取帮助。

- "数据迁移任务在增量迁移过程中已暂停超过 6 小时"

    建议操作：恢复数据迁移任务或忽略此告警。

- "复制延迟大于 10 分钟且持续增加超过 20 分钟"

    - 建议操作：联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)获取帮助。

如果你需要帮助解决这些告警，请联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)进行咨询。

有关如何订阅告警邮件的更多信息，请参见 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md)。

## 另请参阅

- [使用数据迁移功能将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)

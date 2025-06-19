---
title: SHOW [BACKUPS|RESTORES] | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW [BACKUPS|RESTORES] 的使用概览。
---

# SHOW [BACKUPS|RESTORES]

这些语句显示在 TiDB 实例上执行的所有排队、正在运行和最近完成的 [`BACKUP`](/sql-statements/sql-statement-backup.md) 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 任务的列表。

这两个语句都需要 `SUPER` 权限才能运行。

使用 `SHOW BACKUPS` 查询 `BACKUP` 任务，使用 `SHOW RESTORES` 查询 `RESTORE` 任务。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

使用 `br` 命令行工具启动的备份和恢复不会显示在结果中。

## 语法

```ebnf+diagram
ShowBRIEStmt ::=
    "SHOW" ("BACKUPS" | "RESTORES") ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

在一个连接中执行以下语句：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/backup-01';
```

在备份完成之前，在新连接中运行 `SHOW BACKUPS`：

{{< copyable "sql" >}}

```sql
SHOW BACKUPS;
```

```sql
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
| Destination                    | State   | Progress | Queue_time          | Execution_time      | Finish_time | Connection | Message |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
| s3://example-bucket/backup-01/ | Backup  | 98.38    | 2020-04-12 23:09:03 | 2020-04-12 23:09:25 |        NULL |          4 | NULL    |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
1 row in set (0.00 sec)
```

上述结果的第一行描述如下：

| 列名 | 描述 |
| :-------- | :--------- |
| `Destination` | 目标 URL（已去除所有参数以避免泄露密钥） |
| `State` | 任务状态 |
| `Progress` | 当前状态下的估计进度百分比 |
| `Queue_time` | 任务排队的时间 |
| `Execution_time` | 任务开始执行的时间；对于排队中的任务，值为 `0000-00-00 00:00:00` |
| `Finish_time` | 任务完成的时间戳；对于排队中和正在运行的任务，值为 `0000-00-00 00:00:00` |
| `Connection` | 运行此任务的连接 ID |
| `Message` | 包含详细信息的消息 |

可能的状态有：

| 状态 | 描述 |
| :-----|:------------|
| Backup | 正在进行备份 |
| Wait | 等待执行 |
| Checksum | 正在运行校验和操作 |

连接 ID 可以通过 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句用来取消备份/恢复任务。

{{< copyable "sql" >}}

```sql
KILL TIDB QUERY 4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

### 过滤

使用 `LIKE` 子句通过将目标 URL 与通配符表达式匹配来过滤任务。

{{< copyable "sql" >}}

```sql
SHOW BACKUPS LIKE 's3://%';
```

使用 `WHERE` 子句按列进行过滤。

{{< copyable "sql" >}}

```sql
SHOW BACKUPS WHERE `Progress` < 25.0;
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [RESTORE](/sql-statements/sql-statement-restore.md)

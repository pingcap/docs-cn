---
title: SHOW [BACKUPS|RESTORES]
summary: TiDB 数据库中 SHOW [BACKUPS|RESTORES] 的使用概况。
---

# SHOW [BACKUPS|RESTORES]

`SHOW [BACKUPS|RESTORES]` 语句会列出所有在 TiDB 实例上队列中的、正在执行的和近期完成的 [`BACKUP`](/sql-statements/sql-statement-backup.md) 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 任务。

查询 `BACKUP` 任务时，使用 `SHOW BACKUPS` 语句。查询 `RESTORE` 任务时，使用 `SHOW RESTORES` 语句。

执行 `SHOW BACKUPS` 需要 `SUPER` 或 `BACKUP_ADMIN` 权限。执行 `SHOW RESTORES` 需要 `SUPER` 或 `RESTORE_ADMIN`权限。

不显示用 `br` 命令行工具启动的备份和恢复。

## 语法图

```ebnf+diagram
ShowBRIEStmt ::=
    "SHOW" ("BACKUPS" | "RESTORES") ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

在一个连接中，执行以下命令备份数据库：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/backup-01/';
```

在备份完成之前，在新的连接中执行 `SHOW BACKUPS`：

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

输出结果的第一行描述如下：

| 列名 | 描述 |
| :-------- | :--------- |
| `Destination` | 目标存储的 URL（为避免泄露密钥，所有参数均不显示） |
| `State` | 任务状态 |
| `Progress` | 当前状态的进度（百分比） |
| `Queue time` | 任务开始排队的时间 |
| `Execution time` | 任务开始执行的时间；对于队列中任务，该值为 `0000-00-00 00:00:00` |
| `Finish_time` | 任务完成的时间戳；对于队列中的和运行的任务，该值为`0000-00-00 00:00:00`。 |
| `Connection` | 运行任务的连接 ID |
| `Message` | 详细信息 |

可能的状态有：

| 状态 | 说明 |
| :-----|:------------|
| Backup | 进行备份 |
| Wait | 等待执行 |
| Checksum | 运行 checksum 操作 |

连接 ID 可用于在 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句中取消备份/恢复任务：

{{< copyable "sql" >}}

```sql
KILL TIDB QUERY 4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

### 过滤

在 `LIKE` 子句中使用通配符，可以按目标存储 URL 筛选任务：

{{< copyable "sql" >}}

```sql
SHOW BACKUPS LIKE 's3://%';
```

使用 `WHERE` 子句，可以按列筛选任务：

{{< copyable "sql" >}}

```sql
SHOW BACKUPS WHERE `Progress` < 25.0;
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [RESTORE](/sql-statements/sql-statement-restore.md)

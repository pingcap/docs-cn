---
title: SHOW [BACKUPS|RESTORES]
summary: TiDB 数据库中 SHOW [BACKUPS|RESTORES] 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-backups/']
---

# SHOW [BACKUPS|RESTORES]

`SHOW [BACKUPS|RESTORES]` 语句会列出所有队列中或正在执行的 [`BACKUP`](/sql-statements/sql-statement-backup.md) 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 任务。

查询 `BACKUP` 任务时，使用 `SHOW BACKUPS` 语句。查询 `RESTORE` 任务时，使用 `SHOW RESTORES` 语句。执行两个语句均需要 `SUPER` 权限。

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
BACKUP DATABASE `test` TO 's3://example-bucket/backup-01/?region=us-west-1';
```

在备份完成之前，在新的连接中执行 `SHOW BACKUPS`：

{{< copyable "sql" >}}

```sql
SHOW BACKUPS;
```

```sql
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+
| Destination                    | State   | Progress | Queue_Time          | Execution_Time      | Finish_Time | Connection |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+
| s3://example-bucket/backup-01/ | Backup  | 98.38    | 2020-04-12 23:09:03 | 2020-04-12 23:09:25 |        NULL |          4 |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+
1 row in set (0.00 sec)
```

输出结果的第一行描述如下：

| 列名 | 描述 |
| :-------- | :--------- |
| `Destination` | 目标存储的 URL（为避免泄露密钥，所有参数均不显示） |
| `State` | 任务状态 |
| `Progress` | 当前状态的进度（百分比） |
| `Queue Time` | 任务开始排队的时间 |
| `Execution Time` | 任务开始执行的时间；对于队列中任务，该值为 `0000-00-00 00:00:00` |
| `Finish_Time` | （暂不适用） |
| `Connection` | 运行任务的连接 ID |

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

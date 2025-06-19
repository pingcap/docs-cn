---
title: RESTORE | TiDB SQL 语句参考
summary: TiDB 数据库中 RESTORE 的使用概览。
---

# RESTORE

该语句从之前由 [`BACKUP` 语句](/sql-statements/sql-statement-backup.md)生成的备份存档执行分布式恢复。

> **警告：**
>
> - 这是一个实验性功能。不建议在生产环境中使用。此功能可能会在没有事先通知的情况下更改或删除。如果发现错误，你可以在 GitHub 上报告[问题](https://github.com/pingcap/tidb/issues)。
> - 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

`RESTORE` 语句使用与 [BR 工具](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)相同的引擎，只是恢复过程由 TiDB 本身而不是单独的 BR 工具驱动。BR 的所有优点和注意事项也适用于此。特别是，**`RESTORE` 目前不符合 ACID**。在运行 `RESTORE` 之前，请确保满足以下要求：

* 集群处于"离线"状态，当前 TiDB 会话是访问所有要恢复的表的唯一活动 SQL 连接。
* 当执行完整恢复时，要恢复的表不应该已经存在，因为现有数据可能会被覆盖并导致数据和索引之间的不一致。
* 当执行增量恢复时，表应该与创建备份时的 `LAST_BACKUP` 时间戳处于完全相同的状态。

运行 `RESTORE` 需要 `RESTORE_ADMIN` 或 `SUPER` 权限。此外，执行恢复的 TiDB 节点和集群中的所有 TiKV 节点都必须具有目标的读取权限。

`RESTORE` 语句是阻塞的，只有在整个恢复任务完成、失败或取消后才会结束。运行 `RESTORE` 应准备一个长期存在的连接。可以使用 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句取消任务。

一次只能执行一个 `BACKUP` 和 `RESTORE` 任务。如果同一 TiDB 服务器上已经在运行 `BACKUP` 或 `RESTORE` 任务，新的 `RESTORE` 执行将等待所有先前的任务完成。

`RESTORE` 只能与 "tikv" 存储引擎一起使用。使用 "unistore" 引擎的 `RESTORE` 将失败。

## 语法图

```ebnf+diagram
RestoreStmt ::=
    "RESTORE" BRIETables "FROM" stringLit RestoreOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

RestoreOption ::=
    "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "CONCURRENCY" '='? LengthNum
|   "CHECKSUM" '='? Boolean
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean

Boolean ::=
    NUM | "TRUE" | "FALSE"
```

## 示例

### 从备份存档恢复

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 'local:///mnt/backup/2020/04/';
```

```sql
+------------------------------+-----------+----------+---------------------+---------------------+
| Destination                  | Size      | BackupTS | Queue Time          | Execution Time      |
+------------------------------+-----------+----------+---------------------+---------------------+
| local:///mnt/backup/2020/04/ | 248665063 | 0        | 2020-04-21 17:16:55 | 2020-04-21 17:16:55 |
+------------------------------+-----------+----------+---------------------+---------------------+
1 row in set (28.961 sec)
```

在上面的示例中，所有数据都从本地文件系统的备份存档中恢复。数据作为 SST 文件从分布在所有 TiDB 和 TiKV 节点中的 `/mnt/backup/2020/04/` 目录中读取。

上面结果的第一行描述如下：

| 列 | 描述 |
| :-------- | :--------- |
| `Destination` | 要读取的目标 URL |
| `Size` | 备份存档的总大小，以字节为单位 |
| `BackupTS` | (未使用) |
| `Queue Time` | `RESTORE` 任务排队的时间戳（当前时区） |
| `Execution Time` | `RESTORE` 任务开始运行的时间戳（当前时区） |

### 部分恢复

你可以指定要恢复的数据库或表。如果备份存档中缺少某些数据库或表，它们将被忽略，因此 `RESTORE` 将不执行任何操作就完成。

{{< copyable "sql" >}}

```sql
RESTORE DATABASE `test` FROM 'local:///mnt/backup/2020/04/';
```

{{< copyable "sql" >}}

```sql
RESTORE TABLE `test`.`sbtest01`, `test`.`sbtest02` FROM 'local:///mnt/backup/2020/04/';
```

### 外部存储

BR 支持从 S3 或 GCS 恢复数据：

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/';
```

URL 语法在[外部存储服务的 URI 格式](/external-storage-uri.md)中有进一步解释。

在不应分发凭证的云环境中运行时，将 `SEND_CREDENTIALS_TO_TIKV` 选项设置为 `FALSE`：

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### 性能调优

使用 `RATE_LIMIT` 限制每个 TiKV 节点的平均下载速度以减少网络带宽。

在恢复完成之前，`RESTORE` 会对备份文件中的数据执行校验和以验证正确性。如果你确信这种验证是不必要的，可以通过将 `CHECKSUM` 参数设置为 `FALSE` 来禁用检查。

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### 增量恢复

执行增量恢复没有特殊语法。TiDB 将识别备份存档是完整的还是增量的，并采取适当的操作。你只需要按正确的顺序应用每个增量恢复。

例如，如果按如下方式创建备份任务：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/full-backup'  SNAPSHOT = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-1' SNAPSHOT = 414971854848000 LAST_BACKUP = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-2' SNAPSHOT = 416353458585600 LAST_BACKUP = 414971854848000;
```

那么恢复时应该按相同的顺序应用：

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket/full-backup';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-1';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-2';
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [SHOW RESTORES](/sql-statements/sql-statement-show-backups.md)

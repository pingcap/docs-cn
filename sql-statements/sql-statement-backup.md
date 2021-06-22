---
title: BACKUP
summary: TiDB 数据库中 BACKUP 的使用概况。
---

# BACKUP

`BACKUP` 语句用于对 TiDB 集群执行分布式备份操作。

`BACKUP` 语句使用的引擎与 [BR](/br/backup-and-restore-use-cases.md) 相同，但备份过程是由 TiDB 本身驱动，而非单独的 BR 工具。BR 工具的优势和警告也适用于 `BACKUP` 语句。

执行 `BACKUP` 需要 `BACKUP_ADMIN` 或 `SUPER` 权限。此外，执行备份的 TiDB 节点和集群中的所有 TiKV 节点都必须有对目标存储的读或写权限。

`BACKUP` 语句开始执行后将会被阻塞，直到整个备份任务完成、失败或取消。因此，执行 `BACKUP` 时需要准备一个持久的连接。如需取消任务，可执行 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句。

一次只能执行一个 `BACKUP` 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 任务。如果 TiDB server 上已经在执行一个 `BACKUP` 或 `RESTORE` 语句，新的 `BACKUP` 将等待前面所有的任务完成后再执行。

## 语法图

```ebnf+diagram
BackupStmt ::=
    "BACKUP" BRIETables "TO" stringLit BackupOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

BackupOption ::=
    "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "CONCURRENCY" '='? LengthNum
|   "CHECKSUM" '='? Boolean
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean
|   "LAST_BACKUP" '='? BackupTSO
|   "SNAPSHOT" '='? ( BackupTSO | LengthNum TimestampUnit "AGO" )

Boolean ::=
    NUM | "TRUE" | "FALSE"

BackupTSO ::=
    LengthNum | stringLit
```

## 示例

### 备份数据库

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 'local:///mnt/backup/2020/04/';
```

```sql
+------------------------------+-----------+-----------------+---------------------+---------------------+
| Destination                  | Size      | BackupTS        | Queue Time          | Execution Time      |
+------------------------------+-----------+-----------------+---------------------+---------------------+
| local:///mnt/backup/2020/04/ | 248665063 | 416099531454472 | 2020-04-12 23:09:48 | 2020-04-12 23:09:48 |
+------------------------------+-----------+-----------------+---------------------+---------------------+
1 row in set (58.453 sec)
```

上述示例中，`test` 数据库被备份到本地，数据以 SST 文件的形式存储在分布于所有 TiDB 和 TiKV 节点的 `/mnt/backup/2020/04/` 目录中。

输出结果的第一行描述如下：

| 列名 | 描述 |
| :-------- | :--------- |
| `Destination` | 目标存储的 URL |
| `Size` |  备份文件的总大小，单位为字节 |
| `BackupTS` | 创建备份时的快照 TSO（用于[增量备份](#增量备份)） |
| `Queue Time` | `BACKUP` 任务开始排队的时间戳（当前时区） |
| `Execution Time` | `BACKUP` 任务开始执行的时间戳（当前时区） |

### 备份表

{{< copyable "sql" >}}

```sql
BACKUP TABLE `test`.`sbtest01` TO 'local:///mnt/backup/sbtest01/';
```

{{< copyable "sql" >}}

```sql
BACKUP TABLE sbtest02, sbtest03, sbtest04 TO 'local:///mnt/backup/sbtest/';
```

### 备份集群

{{< copyable "sql" >}}

```sql
BACKUP DATABASE * TO 'local:///mnt/backup/full/';
```

注意，备份中不包含系统表 (`mysql.*`、`INFORMATION_SCHEMA.*`、`PERFORMANCE_SCHEMA.*` 等)。

### 外部存储

BR 支持备份数据到 Amazon S3 或 Google Cloud Storage (GCS)：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?region=us-west-2&access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

有关详细的 URL 语法，见 [外部存储](/br/backup-and-restore-storages.md)。

当运行在云环境中时，不能分发凭证，可设置 `SEND_CREDENTIALS_TO_TIKV` 选项为 `FALSE`：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?region=us-west-2'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### 性能调优

如果你需要减少网络带宽占用，可以通过 `RATE_LIMIT` 来限制每个 TiKV 节点的平均上传速度。

默认情况下，每个 TiKV 节点上运行 4 个备份线程。可以通过 `CONCURRENCY` 选项来调整这个值。

在备份完成之前，`BACKUP` 将对集群上的数据进行校验，以验证数据的正确性。如果你确信无需进行校验，可以通过 `CHECKSUM` 选项禁用这一步骤。

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### 快照

可以指定一个时间戳、TSO 或相对时间，来备份历史数据。

{{< copyable "sql" >}}

```sql
-- 相对时间
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist01'
    SNAPSHOT = 36 HOUR AGO;
-- 时间戳（当前时区）
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    SNAPSHOT = '2020-04-01 12:00:00';
-- TSO
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    SNAPSHOT = 415685305958400;
```

对于相对时间，支持以下时间单位：

* MICROSECOND（微秒）
* SECOND（秒）
* MINUTE（分钟）
* HOUR（小时）
* DAY（天）
* WEEK（周）

注意，相对时间的单位遵循 SQL 标准，永远使用单数。

### 增量备份

提供 `LAST_BACKUP` 选项，只备份从上一次备份到当前快照之间的增量数据。

{{< copyable "sql" >}}

```sql
-- 时间戳（当前时区）
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    LAST_BACKUP = '2020-04-01 12:00:00';

-- TSO
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    LAST_BACKUP = 415685305958400;
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [RESTORE](/sql-statements/sql-statement-restore.md)
* [SHOW BACKUPS](/sql-statements/sql-statement-show-backups.md)

---
title: BACKUP | TiDB SQL 语句参考
summary: TiDB 数据库中 BACKUP 的使用概述。
---

# BACKUP

此语句用于执行 TiDB 集群的分布式备份。

> **警告：**
>
> - 此功能为实验特性。不建议在生产环境中使用。此功能可能会在没有预先通知的情况下发生变更或移除。如果发现 bug，可以在 GitHub 上提交[议题](https://github.com/pingcap/tidb/issues)。
> - 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

`BACKUP` 语句使用与 [BR 工具](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)相同的引擎，不同之处在于备份过程由 TiDB 本身驱动，而不是由独立的 BR 工具驱动。BR 的所有优点和警告也适用于此语句。

执行 `BACKUP` 需要 `BACKUP_ADMIN` 或 `SUPER` 权限。此外，执行备份的 TiDB 节点和集群中的所有 TiKV 节点都必须对目标位置具有读写权限。当启用[安全增强模式](/system-variables.md#tidb_enable_enhanced_security)时，不允许使用本地存储（以 `local://` 开头的存储路径）。

`BACKUP` 语句会阻塞直到整个备份任务完成、失败或被取消。执行 `BACKUP` 需要准备一个长期连接。可以使用 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句取消任务。

同一时间只能执行一个 `BACKUP` 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 任务。如果在同一 TiDB 服务器上已经在执行 `BACKUP` 或 `RESTORE` 语句，新的 `BACKUP` 执行将等待所有先前的任务完成。

`BACKUP` 只能与 "tikv" 存储引擎一起使用。使用 "unistore" 引擎的 `BACKUP` 将失败。

## 语法概要

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

在上面的示例中，`test` 数据库被备份到本地文件系统。数据以 SST 文件的形式保存在所有 TiDB 和 TiKV 节点的 `/mnt/backup/2020/04/` 目录中。

上面结果的第一行描述如下：

| 列 | 描述 |
| :-------- | :--------- |
| `Destination` | 目标 URL |
| `Size` | 备份存档的总大小，以字节为单位 |
| `BackupTS` | 创建备份时快照的 TSO（对[增量备份](#增量备份)有用） |
| `Queue Time` | `BACKUP` 任务排队的时间戳（当前时区） |
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

### 备份整个集群

{{< copyable "sql" >}}

```sql
BACKUP DATABASE * TO 'local:///mnt/backup/full/';
```

注意，系统表（`mysql.*`、`INFORMATION_SCHEMA.*`、`PERFORMANCE_SCHEMA.*` 等）不会包含在备份中。

### 外部存储

BR 支持将数据备份到 S3 或 GCS：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

URL 语法在[外部存储服务的 URI 格式](/external-storage-uri.md)中有进一步说明。

在不应分发凭证的云环境中运行时，将 `SEND_CREDENTIALS_TO_TIKV` 选项设置为 `FALSE`：

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### 性能调优

使用 `RATE_LIMIT` 限制每个 TiKV 节点的平均上传速度以减少网络带宽。

在备份完成之前，`BACKUP` 会对集群上的数据执行校验和以验证正确性。如果你确信这种验证是不必要的，可以通过将 `CHECKSUM` 参数设置为 `FALSE` 来禁用检查。

要指定 BR 可以执行备份表和索引的并发任务数，请使用 `CONCURRENCY` 参数。此参数控制 BR 内的线程池大小，优化备份操作的性能和效率。

一个任务代表一个表范围或一个索引范围，具体取决于备份架构。对于一个有一个索引的表，使用两个任务来备份这个表。`CONCURRENCY` 的默认值是 `4`。如果需要备份大量的表或索引，请增加其值。

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### 快照

指定时间戳、TSO 或相对时间来备份历史数据。

{{< copyable "sql" >}}

```sql
-- 相对时间
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist01'
    SNAPSHOT = 36 HOUR AGO;

-- 时间戳（当前时区）
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    SNAPSHOT = '2020-04-01 12:00:00';

-- 时间戳 oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    SNAPSHOT = 415685305958400;
```

相对时间支持的单位有：

* MICROSECOND
* SECOND
* MINUTE
* HOUR
* DAY
* WEEK

注意，按照 SQL 标准，单位始终是单数形式。

### 增量备份

提供 `LAST_BACKUP` 选项仅备份从上次备份到当前快照之间的更改。

{{< copyable "sql" >}}

```sql
-- 时间戳（当前时区）
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    LAST_BACKUP = '2020-04-01 12:00:00';

-- 时间戳 oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    LAST_BACKUP = 415685305958400;
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [RESTORE](/sql-statements/sql-statement-restore.md)
* [SHOW BACKUPS](/sql-statements/sql-statement-show-backups.md)

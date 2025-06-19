---
title: 缓存表
summary: 了解 TiDB 中的缓存表功能，该功能用于提高很少更新的小型热点表的读取性能。
---

# 缓存表

在 v6.0.0 中，TiDB 为经常访问但很少更新的小型热点表引入了缓存表功能。使用此功能时，整个表的数据会加载到 TiDB 服务器的内存中，TiDB 直接从内存获取表数据而无需访问 TiKV，从而提高读取性能。

本文档描述缓存表的使用场景、示例以及与其他 TiDB 功能的兼容性限制。

## 使用场景

缓存表功能适用于具有以下特征的表：

- 表的数据量小，例如小于 4 MiB。
- 表是只读的或很少更新，例如每分钟写入 QPS（每秒查询数）少于 10 次。
- 表经常被访问，并且你期望更好的读取性能，例如当从 TiKV 直接读取小表时遇到热点。

当表的数据量小但数据经常被访问时，数据会集中在 TiKV 的一个 Region 上并形成热点 Region，这会影响性能。因此，缓存表的典型使用场景如下：

- 配置表，应用程序从中读取配置信息。
- 金融领域的汇率表。这些表每天只更新一次，而不是实时更新。
- 银行分支机构或网络信息表，很少更新。

以配置表为例。当应用程序重启时，所有连接都会加载配置信息，这会导致较高的读取延迟。在这种情况下，你可以使用缓存表功能来解决这个问题。

## 示例

本节通过示例描述缓存表的使用方法。

### 将普通表设置为缓存表

假设有一个表 `users`：

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

要将此表设置为缓存表，使用 `ALTER TABLE` 语句：

```sql
ALTER TABLE users CACHE;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

### 验证缓存表

要验证缓存表，使用 `SHOW CREATE TABLE` 语句。如果表已缓存，返回结果会包含 `CACHED ON` 属性：

```sql
SHOW CREATE TABLE users;
```

```sql
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                               |
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| users | CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /* CACHED ON */ |
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

从缓存表读取数据后，TiDB 会将数据加载到内存中。你可以使用 [`TRACE`](/sql-statements/sql-statement-trace.md) 语句检查数据是否已加载到内存中。当缓存未加载时，返回结果包含 `regionRequest.SendReqCtx` 属性，这表示 TiDB 从 TiKV 读取数据。

```sql
TRACE SELECT * FROM users;
```

```sql
+------------------------------------------------+-----------------+------------+
| operation                                      | startTS         | duration   |
+------------------------------------------------+-----------------+------------+
| trace                                          | 17:47:39.969980 | 827.73µs   |
|   ├─session.ExecuteStmt                        | 17:47:39.969986 | 413.31µs   |
|   │ ├─executor.Compile                         | 17:47:39.969993 | 198.29µs   |
|   │ └─session.runStmt                          | 17:47:39.970221 | 157.252µs  |
|   │   └─TableReaderExecutor.Open               | 17:47:39.970294 | 47.068µs   |
|   │     └─distsql.Select                       | 17:47:39.970312 | 24.729µs   |
|   │       └─regionRequest.SendReqCtx           | 17:47:39.970454 | 189.601µs  |
|   ├─*executor.UnionScanExec.Next               | 17:47:39.970407 | 353.073µs  |
|   │ ├─*executor.TableReaderExecutor.Next       | 17:47:39.970411 | 301.106µs  |
|   │ └─*executor.TableReaderExecutor.Next       | 17:47:39.970746 | 6.57µs     |
|   └─*executor.UnionScanExec.Next               | 17:47:39.970772 | 17.589µs   |
|     └─*executor.TableReaderExecutor.Next       | 17:47:39.970776 | 6.59µs     |
+------------------------------------------------+-----------------+------------+
12 rows in set (0.01 sec)
```

再次执行 [`TRACE`](/sql-statements/sql-statement-trace.md) 后，返回结果不再包含 `regionRequest.SendReqCtx` 属性，这表示 TiDB 不再从 TiKV 读取数据，而是从内存中读取数据。

```sql
+----------------------------------------+-----------------+------------+
| operation                              | startTS         | duration   |
+----------------------------------------+-----------------+------------+
| trace                                  | 17:47:40.533888 | 453.547µs  |
|   ├─session.ExecuteStmt                | 17:47:40.533894 | 402.341µs  |
|   │ ├─executor.Compile                 | 17:47:40.533903 | 205.54µs   |
|   │ └─session.runStmt                  | 17:47:40.534141 | 132.084µs  |
|   │   └─TableReaderExecutor.Open       | 17:47:40.534202 | 14.749µs   |
|   ├─*executor.UnionScanExec.Next       | 17:47:40.534306 | 3.21µs     |
|   └─*executor.UnionScanExec.Next       | 17:47:40.534316 | 1.219µs    |
+----------------------------------------+-----------------+------------+
7 rows in set (0.00 sec)
```

注意，`UnionScan` 运算符用于读取缓存表，所以你可以通过 `explain` 在缓存表的执行计划中看到 `UnionScan`：

```sql
+-------------------------+---------+-----------+---------------+--------------------------------+
| id                      | estRows | task      | access object | operator info                  |
+-------------------------+---------+-----------+---------------+--------------------------------+
| UnionScan_5             | 1.00    | root      |               |                                |
| └─TableReader_7         | 1.00    | root      |               | data:TableFullScan_6           |
|   └─TableFullScan_6     | 1.00    | cop[tikv] | table:users   | keep order:false, stats:pseudo |
+-------------------------+---------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

### 向缓存表写入数据

缓存表支持数据写入。例如，你可以向 `users` 表插入一条记录：

```sql
INSERT INTO users(id, name) VALUES(1001, 'Davis');
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
SELECT * FROM users;
```

```sql
+------+-------+
| id   | name  |
+------+-------+
| 1001 | Davis |
+------+-------+
1 row in set (0.00 sec)
```

> **注意：**
>
> 向缓存表插入数据时，可能会出现秒级写入延迟。延迟由全局环境变量 [`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-new-in-v600) 控制。你可以根据应用程序检查延迟是否可接受来决定是否使用缓存表功能。例如，在只读场景中，你可以增加 `tidb_table_cache_lease` 的值：
>
> ```sql
> set @@global.tidb_table_cache_lease = 10;
> ```
>
> 缓存表的写入延迟较高，因为缓存表功能的实现使用了复杂的机制，需要为每个缓存设置租约。当有多个 TiDB 实例时，一个实例不知道其他实例是否已缓存数据。如果一个实例直接修改表数据，其他实例会读取旧的缓存数据。为确保正确性，缓存表实现使用租约机制确保在租约到期前数据不会被修改。这就是写入延迟较高的原因。

缓存表的元数据存储在 `mysql.table_cache_meta` 表中。此表记录了所有缓存表的 ID、当前锁定状态（`lock_type`）和锁定租约信息（`lease`）。此表仅供 TiDB 内部使用，不建议修改它。否则，可能会发生意外错误。

```sql
SHOW CREATE TABLE mysql.table_cache_meta\G
*************************** 1. row ***************************
       Table: table_cache_meta
Create Table: CREATE TABLE `table_cache_meta` (
  `tid` bigint(11) NOT NULL DEFAULT '0',
  `lock_type` enum('NONE','READ','INTEND','WRITE') NOT NULL DEFAULT 'NONE',
  `lease` bigint(20) NOT NULL DEFAULT '0',
  `oldReadLease` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`tid`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

### 将缓存表恢复为普通表

> **注意：**
>
> 在缓存表上执行 DDL 语句将会失败。在对缓存表执行 DDL 语句之前，你需要先移除缓存属性，将缓存表恢复为普通表。

```sql
TRUNCATE TABLE users;
```

```sql
ERROR 8242 (HY000): 'Truncate Table' is unsupported on cache tables.
```

```sql
mysql> ALTER TABLE users ADD INDEX k_id(id);
```

```sql
ERROR 8242 (HY000): 'Alter Table' is unsupported on cache tables.
```

要将缓存表恢复为普通表，使用 `ALTER TABLE t NOCACHE`：

```sql
ALTER TABLE users NOCACHE;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

## 缓存表的大小限制

缓存表仅适用于小表场景，因为 TiDB 会将整个表的数据加载到内存中，并且缓存的数据在修改后会失效并需要重新加载。

目前，TiDB 中缓存表的大小限制为 64 MB。如果表数据超过 64 MB，执行 `ALTER TABLE t CACHE` 将会失败。

## 与其他 TiDB 功能的兼容性限制

缓存表**不支持**以下功能：

- 不支持对分区表执行 `ALTER TABLE t ADD PARTITION` 操作。
- 不支持对临时表执行 `ALTER TABLE t CACHE` 操作。
- 不支持对视图执行 `ALTER TABLE t CACHE` 操作。
- 不支持 Stale Read。
- 不支持直接对缓存表执行 DDL 操作。在执行 DDL 操作之前，你需要先使用 `ALTER TABLE t NOCACHE` 将缓存表恢复为普通表。

缓存表**不能**在以下场景中使用：

- 设置系统变量 `tidb_snapshot` 来读取历史数据。
- 在修改期间，缓存的数据会失效，直到数据重新加载。

## 与 TiDB 迁移工具的兼容性

缓存表是 TiDB 对 MySQL 语法的扩展。只有 TiDB 能识别 `ALTER TABLE ... CACHE` 语句。TiDB 迁移工具**不支持**缓存表，包括 Backup & Restore (BR)、TiCDC 和 Dumpling。这些工具将缓存表视为普通表。

也就是说，当缓存表被备份和恢复时，它会变成普通表。如果下游集群是不同的 TiDB 集群，并且你想继续使用缓存表功能，你可以在下游集群上通过对下游表执行 `ALTER TABLE ... CACHE` 手动启用缓存表。

## 另请参阅

* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
* [系统变量](/system-variables.md)

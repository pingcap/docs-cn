---
title: 缓存表
summary: 了解 TiDB 中的缓存表功能，用于很少被修改的热点小表，提升读性能。
---

# 缓存表

TiDB 在 v6.0.0 版本中引入了缓存表功能。该功能适用于频繁被访问且很少被修改的热点小表，即把整张表的数据加载到 TiDB 服务器的内存中，直接从内存中获取表数据，避免从 TiKV 获取表数据，从而提升读性能。

本文介绍了 TiDB 缓存表的使用场景、使用示例、与其他 TiDB 功能的兼容性限制。

## 使用场景

TiDB 缓存表功能适用于以下特点的表：

- 表的数据量不大
- 只读表，或者几乎很少修改
- 表的访问很频繁，期望有更好的读性能

当表的数据量不大，访问又特别频繁的情况下，数据会集中在 TiKV 一个 Region 上，形成热点，从而影响性能。因此，TiDB 缓存表的典型使用场景如下：

- 配置表，业务通过该表读取配置信息
- 金融场景中的存储汇率的表，该表不会实时更新，每天只更新一次
- 银行分行或者网点信息表，该表很少新增记录项

以配置表为例，当业务重启的瞬间，全部连接一起加载配置，会造成较高的数据库读延迟。如果使用了缓存表，则可以解决这样的问题。

### 使用示例

#### 将普通表设为缓存表

假设已存在普通表 `users`:

{{< copyable "sql" >}}

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

通过 `ALTER TABLE` 语句，可以将这张表设置成缓存表：

{{< copyable "sql" >}}

```sql
ALTER TABLE users CACHE;
```

```
Query OK, 0 rows affected (0.01 sec)
```

#### 验证是否为缓存表

之后观察 `SHOW CREATE TABLE` 会出现 `CACHED ON` 的属性：

{{< copyable "sql" >}}

```sql
show create table users;
```

```
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

对缓存表的读取，会触发将数据加载到 TiDB 内存中，使用 `trace` 可以观察到，当缓存还未加载时，会访问 TiKV（出现了 `regionRequest.SendReqCtx`）。

{{< copyable "sql" >}}

```sql
trace  select * from users;
```


```
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

而再次执行 `trace` 时，已经不用访问 TiKV 了：

```
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

读取缓存表会使用 `UnionScan` 算子，所以通过 `explain` 查看缓存表的执行计划时，可能会在结果中看到 `UnionScan`：

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

#### 往缓存表写入数据

缓存表仍然是支持写入的，往 `users` 中插入一条记录：

{{< copyable "sql" >}}

```sql
INSERT INTO users(id, name) VALUES(1001, 'Davis');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
+------+-------+
| id   | name  |
+------+-------+
| 1001 | Davis |
+------+-------+
1 row in set (0.00 sec)
```

**注意： 缓存表的写入，有可能出现数秒级别的慢查询**，具体最长耗时受到全局环境变量 `@@tidb_table_cache_lease` 的控制。该变量的默认值是 3s，取值范围是 [1, 10]。
用户需要根据自己的业务能否承受此限制，决定是否适合使用缓存表功能。比如完全只读的场景，可以把 `@@tidb_table_cache_lease` 调大：


{{< copyable "sql" >}}

```sql
set @@global.tidb_table_cache_lease = 10;
```

```
Query OK, 0 rows affected (0.01 sec)
```


缓存表写入延时高的原因是受到实现的限制。存在多个 TiDB 实例时，一个 TiDB 实例并不知道其它的 TiDB 实例是否缓存了数据，如果它直接执行了修改操作，而其它 TiDB 依然读取旧的缓存数据，就会读到错误的结果。
为了保证正确性，缓存表的实现使用了一套复杂的基于 lease 的机制：读操作在缓存数据同时，还会对于缓存设置一个有效期，也就是 lease。在 lease 过期之前，保证修改操作无法执行。
因为修改操作必须等待 lease 过期，所以会出现写入延迟。

#### 将缓存表设为普通表

**注意： 对于缓存表执行 DDL 语句会失败，需要去掉缓存属性，将缓存表改回普通表后，才能执行。**


{{< copyable "sql" >}}

```sql
TRUNCATE TABLE users;
```

```
ERROR 8242 (HY000): 'Truncate Table' is unsupported on cache tables.
```

{{< copyable "sql" >}}

```sql
mysql> ALTER TABLE users ADD INDEX k_id(id);
```

```
ERROR 8242 (HY000): 'Alter Table' is unsupported on cache tables.
```

通过 `ALTER TABLE t NOCACHE` 语句 可以将缓存表恢复成普通表。


{{< copyable "sql" >}}

```sql
ALTER TABLE users NOCACHE
```

```
Query OK, 0 rows affected (0.00 sec)
```


## 缓存表大小限制

缓存表会将整张表的全部数据，加载到 TiDB 进程的内存中，并且执行修改操作后，缓存会失效，需要重新加载，因此只适用于表比较小的场景。

目前 TiDB 对于缓存表的大小限制为 64M。如果表的数据超过了这个大小，执行 `ALTER TABLE t CACHE` 会失败。

```
mysql> SELECT count(*) FROM t1;
+----------+
| count(*) |
+----------+
|   114688 |
+----------+
1 row in set (0.04 sec)

mysql> ALTER TABLE t1 CACHE;
ERROR 8242 (HY000): 'table too large' is unsupported on cache tables.
```

## 与其他 TiDB 功能的兼容性限制

以下是缓存表不支持的功能：

- 不支持对分区表执行 `ALTER TABLE t CACHE` 操作
- 不支持对临时表执行 `ALTER TABLE t CACHE` 操作
- 不支持对视图执行 `ALTER TABLE t CACHE` 操作
- 不支持对缓存表直接做 DDL 操作，需要先通过 `ALTER TABLE t NOCACHE` 改回普通表

以下是缓存表无法使用缓存的场景：

- 使用 Stale Read 功能
- 设置系统变量 `tidb_snapshot` 读取历史数据
- 执行修改操作期间，会使缓存失效，直到下次数据被再次加载

## TiDB 生态工具兼容性

缓存表并不是标准 MySQL 功能，而是 TiDB 扩展，并且只有 TiDB 识别 `ALTER TABLE CACHE` 语句。所有的 TiDB 生态工具，并不支持这一项功能，包括 br, cdc, dumpling 等组件，它们会将缓存表当作普通表处理。

这意味着，备份恢复一张缓存表，它会变成一张普通表。如果下游集群是另一套 TiDB 并且您希望仍然用上缓存表，可以对下游集群中的表执行 `ALTER TABLE CACHE` 手动开启。

## 另请参阅

* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
* [System Variables](/system-variables.md)

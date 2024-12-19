---
title: FLASHBACK CLUSTER
summary: TiDB 数据库中 FLASHBACK CLUSTER 的使用概况。
aliases: ['/zh/tidb/dev/sql-statement-flashback-to-timestamp']
---

# FLASHBACK CLUSTER

TiDB v6.4.0 引入了 `FLASHBACK CLUSTER TO TIMESTAMP` 语法，其功能是将集群的数据恢复到过去指定的时间点。指定时间点时，你可以使用日期时间和时间函数，日期时间的格式为：'2016-10-08 16:45:26.999'，最小时间精度范围为毫秒，通常可只写到秒，例如 '2016-10-08 16:45:26'。

TiDB v6.5.6、v7.1.3、v7.5.1、v7.6.0 开始引入了 `FLASHBACK CLUSTER TO TSO` 的语法，支持使用时间戳 [TSO](/tso.md) 更加精确地指定恢复时间点，实现更加灵活的数据恢复。

> **警告：**
>
> - 在指定恢复时间点时，请务必检查 TIMESTAMP 或 TSO 的有效性，避免指定可能超过 PD 当前分配的最大 TSO（参考 Grafana PD 面板上 `Current TSO`）的未来时间。否则，可能破坏并发处理线性一致性以及事务隔离级别，导致严重的数据正确性的问题。
> - 在 `FLASHBACK CLUSTER` 执行期间，数据清理过程不能保证事务的一致性。在 `FLASHBACK CLUSTER` 执行完成后，如需使用 TiDB 的任何历史版本读取功能（如 [Stale Read](/stale-read.md) 或 [`tidb_snapshot`](/read-historical-data.md)），请确保所选择的历史时间点不在 FLASHBACK 运行的时间范围内。如果读取的历史版本包含未 FLASHBACK 完成的数据，可能会破坏并发处理的线性一致性以及事务隔离级别，导致严重的数据正确性问题。

> **警告：**
>
> 在 TiDB v7.1.0 中使用该功能可能会出现 FLASHBACK 完成后部分 Region 仍处于 FLASHBACK 过程中的问题。请尽量避免在 v7.1.0 中使用该功能。详情可见 [#44292](https://github.com/pingcap/tidb/issues/44292)。
>
> 如果已经出现该问题，可以使用 [TiDB 快照备份与恢复](/br/br-snapshot-guide.md)功能进行数据恢复。

> **注意：**
>
> `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` 是用最新的时间戳写入特定时间点的旧数据，但不会删除当前数据，所以在使用前请确保集群有足够的存储空间来同时容纳旧数据和当前数据。

## 语法

```sql
FLASHBACK CLUSTER TO TIMESTAMP '2022-09-21 16:02:50';
FLASHBACK CLUSTER TO TSO 445494839813079041;
```

### 语法图

```ebnf+diagram
FlashbackToTimestampStmt
         ::= 'FLASHBACK' 'CLUSTER' 'TO' ('TIMESTAMP' stringLit | 'TSO' LengthNum)
```

## 注意事项

* `FLASHBACK` 指定的时间点需要在 Garbage Collection (GC) life time 时间内。你可以使用系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入) 配置数据的历史版本的保留时间（默认值是 `10m0s`）。可以使用以下 SQL 语句查询当前的 `safePoint`，即 GC 已经清理到的时间点：

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

* 执行 `FLASHBACK CLUSTER` SQL 语句的用户需要有 `SUPER` 权限。
* `FLASHBACK CLUSTER` 不支持回退修改 PD 相关信息的 DDL，如 `ALTER TABLE ATTRIBUTE`、`ALTER TABLE REPLICA`、`CREATE PLACEMENT POLICY` 等。
* `FLASHBACK CLUSTER` 指定的时间点不能存在未执行完成的 DDL 记录。若存在，TiDB 会拒绝该 DDL 操作。
* 在执行 `FLASHBACK CLUSTER` 前，TiDB 会主动断开所有相关表上的连接，并禁止对这些表进行读写操作，直到 `FLASHBACK CLUSTER` 完成。
* `FLASHBACK CLUSTER` 命令不能取消，一旦开始执行 TiDB 会一直重试，直到成功。
* 在 `FLASHBACK CLUSTER` 执行期间，若有数据备份需求，只支持使用 [BR 命令行工具进行快照备份](/br/br-snapshot-guide.md)，并需要指定早于 `FLASHBACK CLUSTER` 开始时间的 `BackupTS`。同时，在执行 `FLASHBACK CLUSTER` 期间，[开启日志备份](/br/br-pitr-guide.md)的操作会失败，请等待 `FLASHBACK CLUSTER` 结束后再尝试开启日志备份。
* 若 `FLASHBACK CLUSTER` 导致了元信息（表结构、库结构）的回滚，则相关的修改**不会**被 TiCDC 同步。因此，用户需主动暂停任务，待 `FLASHBACK CLUSTER` 完成后将上下游的 schema 定义手动同步一致，然后重新创建 TiCDC changefeed。

## 示例

闪回到指定的 TIMESTAMP 来恢复新写入的数据：

```sql
mysql> CREATE TABLE t(a INT);
Query OK, 0 rows affected (0.09 sec)

mysql> SELECT * FROM t;
Empty set (0.01 sec)

mysql> SELECT now();
+---------------------+
| now()               |
+---------------------+
| 2022-09-28 17:24:16 |
+---------------------+
1 row in set (0.02 sec)

mysql> INSERT INTO t VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)

mysql> FLASHBACK CLUSTER TO TIMESTAMP '2022-09-28 17:24:16';
Query OK, 0 rows affected (0.20 sec)

mysql> SELECT * FROM t;
Empty set (0.00 sec)
```

闪回到指定的 TSO 来精确恢复误删除的数据：

```sql
mysql> INSERT INTO t VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)


mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @@tidb_current_ts;  --  获取当前 TSO
+--------------------+
| @@tidb_current_ts  |
+--------------------+
| 446113975683252225 |
+--------------------+
1 row in set (0.00 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.00 sec)


mysql> DELETE FROM t;
Query OK, 1 rows affected (0.00 sec)


mysql> FLASHBACK CLUSTER TO TSO 446113975683252225;
Query OK, 0 rows affected (0.20 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)
```

如果 `FLASHBACK CLUSTER` 指定的时间点有未完成的 DDL 记录，那么 `FLASHBACK CLUSTER` 将执行失败：

```sql
mysql> ALTER TABLE t ADD INDEX k(a);
Query OK, 0 rows affected (0.56 sec)

mysql> ADMIN SHOW DDL JOBS 1;
+--------+---------+-----------------------+------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+---------------------+--------+
| JOB_ID | DB_NAME | TABLE_NAME            | JOB_TYPE               | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME         | START_TIME          | END_TIME            | STATE  |
+--------+---------+-----------------------+------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+---------------------+--------+
|     84 | test    | t                     | add index /* ingest */ | public       |         2 |       82 |         0 | 2023-01-29 14:33:11 | 2023-01-29 14:33:11 | 2023-01-29 14:33:12 | synced |
+--------+---------+-----------------------+------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+---------------------+--------+
1 rows in set (0.01 sec)

mysql> FLASHBACK CLUSTER TO TIMESTAMP '2023-01-29 14:33:12';
ERROR 1105 (HY000): Detected another DDL job at 2023-01-29 14:33:12 +0800 CST, can't do flashback
```

可以通过日志查看 `FLASHBACK` 执行进度，具体的日志如下所示：

```
[2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

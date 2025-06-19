---
title: FLASHBACK CLUSTER
summary: 了解在 TiDB 数据库中 FLASHBACK CLUSTER 的用法。
---

# FLASHBACK CLUSTER

TiDB v6.4.0 引入了 `FLASHBACK CLUSTER TO TIMESTAMP` 语法。你可以使用它将集群恢复到特定时间点。在指定时间戳时，你可以设置一个日期时间值或使用时间函数。日期时间的格式类似于 '2016-10-08 16:45:26.999'，最小时间单位为毫秒。但在大多数情况下，以秒为时间单位指定时间戳就足够了，例如 '2016-10-08 16:45:26'。

从 v6.5.6、v7.1.3、v7.5.1 和 v7.6.0 开始，TiDB 引入了 `FLASHBACK CLUSTER TO TSO` 语法。此语法允许你使用 [TSO](/tso.md) 来指定更精确的恢复时间点，从而提高数据恢复的灵活性。

> **警告：**
>
> `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` 语法不适用于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群。为避免意外结果，请勿在 TiDB Cloud Serverless 集群上执行此语句。

> **警告：**
>
> - 在指定恢复时间点时，请确保检查目标时间戳或 TSO 的有效性，避免指定超过 PD 当前分配的最大 TSO 的未来时间（参见 Grafana PD 面板上的 `Current TSO`）。否则，可能会违反并发处理线性一致性和事务隔离级别，导致严重的数据正确性问题。
> - 在执行 `FLASHBACK CLUSTER` 期间，数据清理过程不保证事务一致性。在 `FLASHBACK CLUSTER` 完成后，如果你打算使用 TiDB 中的任何历史版本读取功能（如 [Stale Read](/stale-read.md) 或 [`tidb_snapshot`](/read-historical-data.md)），请确保指定的历史时间戳不在 `FLASHBACK CLUSTER` 执行期间。读取包含 FLASHBACK 未完全恢复数据的历史版本可能会违反并发处理线性一致性和事务隔离级别，导致严重的数据正确性问题。

<CustomContent platform="tidb">

> **警告：**
>
> 当你在 TiDB v7.1.0 中使用此功能时，即使在 FLASHBACK 操作完成后，某些 Region 可能仍处于 FLASHBACK 过程中。建议避免在 v7.1.0 中使用此功能。更多信息，请参见 issue [#44292](https://github.com/pingcap/tidb/issues/44292)。
>
> 如果你遇到此问题，可以使用 [TiDB 快照备份和恢复](/br/br-snapshot-guide.md)功能来恢复数据。

</CustomContent>

> **注意：**
>
> `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` 的工作原理是用最新的时间戳写入特定时间点的旧数据，不会删除当前数据。因此在使用此功能之前，你需要确保有足够的存储空间来存放旧数据和当前数据。

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

* `FLASHBACK` 语句中指定的时间必须在垃圾回收（GC）生命周期内。系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)（默认值：`10m0s`）定义了行的早期版本的保留时间。可以通过以下查询获取垃圾回收已执行到的当前 `safePoint`：

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

<CustomContent platform='tidb'>

* 只有具有 `SUPER` 权限的用户才能执行 `FLASHBACK CLUSTER` SQL 语句。
* `FLASHBACK CLUSTER` 不支持回滚修改 PD 相关信息的 DDL 语句，如 `ALTER TABLE ATTRIBUTE`、`ALTER TABLE REPLICA` 和 `CREATE PLACEMENT POLICY`。
* 在 `FLASHBACK` 语句指定的时间点，不能存在未完全执行的 DDL 语句。如果存在这样的 DDL，TiDB 将拒绝执行。
* 在执行 `FLASHBACK CLUSTER` 之前，TiDB 会断开所有相关连接，并禁止对这些表进行读写操作，直到 `FLASHBACK CLUSTER` 语句完成。
* `FLASHBACK CLUSTER` 语句执行后不能取消。TiDB 将持续重试直到成功。
* 在执行 `FLASHBACK CLUSTER` 期间，如果需要备份数据，只能使用[备份与恢复](/br/br-snapshot-guide.md)并指定早于 `FLASHBACK CLUSTER` 开始时间的 `BackupTS`。此外，在执行 `FLASHBACK CLUSTER` 期间，启用[日志备份](/br/br-pitr-guide.md)将失败。因此，请在 `FLASHBACK CLUSTER` 完成后尝试启用日志备份。
* 如果 `FLASHBACK CLUSTER` 语句导致元数据（表结构、数据库结构）回滚，相关修改将**不会**被 TiCDC 复制。因此，你需要手动暂停任务，等待 `FLASHBACK CLUSTER` 完成，并手动复制上下游的架构定义以确保它们一致。之后，你需要重新创建 TiCDC changefeed。

</CustomContent>

<CustomContent platform='tidb-cloud'>

* 只有具有 `SUPER` 权限的用户才能执行 `FLASHBACK CLUSTER` SQL 语句。
* `FLASHBACK CLUSTER` 不支持回滚修改 PD 相关信息的 DDL 语句，如 `ALTER TABLE ATTRIBUTE`、`ALTER TABLE REPLICA` 和 `CREATE PLACEMENT POLICY`。
* 在 `FLASHBACK` 语句指定的时间点，不能存在未完全执行的 DDL 语句。如果存在这样的 DDL，TiDB 将拒绝执行。
* 在执行 `FLASHBACK CLUSTER` 之前，TiDB 会断开所有相关连接，并禁止对这些表进行读写操作，直到 `FLASHBACK CLUSTER` 语句完成。
* `FLASHBACK CLUSTER` 语句执行后不能取消。TiDB 将持续重试直到成功。
* 如果 `FLASHBACK CLUSTER` 语句导致元数据（表结构、数据库结构）回滚，相关修改将**不会**被 TiCDC 复制。因此，你需要手动暂停任务，等待 `FLASHBACK CLUSTER` 完成，并手动复制上下游的架构定义以确保它们一致。之后，你需要重新创建 TiCDC changefeed。

</CustomContent>

## 示例

以下示例展示如何将集群闪回到特定时间戳以恢复新插入的数据：

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

以下示例展示如何将集群闪回到特定 TSO 以精确恢复误删的数据：

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

mysql> SELECT @@tidb_current_ts;  -- 获取当前 TSO
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

如果在 `FLASHBACK` 语句指定的时间点存在未完全执行的 DDL 语句，`FLASHBACK` 语句将失败：

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

通过日志，你可以获取 `FLASHBACK` 的执行进度。以下是一个示例：

```
[2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

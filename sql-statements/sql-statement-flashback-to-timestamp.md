---
title: FLASHBACK CLUSTER TO TIMESTAMP
summary: TiDB 数据库中 FLASHBACK CLUSTER TO TIMESTAMP 的使用概况。
---

# FLASHBACK CLUSTER TO TIMESTAMP

TiDB v6.4.0 引入了 `FLASHBACK CLUSTER TO TIMESTAMP` 语法，其功能是将集群的数据恢复到特定的时间点。

> **注意：**
>
> `FLASHBACK CLUSTER TO TIMESTAMP` 是用最新的时间戳写入特定时间点的旧数据，但不会删除当前数据，所以在使用前请确保集群有足够的存储空间来同时容纳旧数据和当前数据。

## 语法

```sql
FLASHBACK CLUSTER TO TIMESTAMP '2022-09-21 16:02:50';
```

### 语法图

```ebnf+diagram
FlashbackToTimestampStmt ::=
    "FLASHBACK" "CLUSTER" "TO" "TIMESTAMP" stringLit
```

## 注意事项

* `FLASHBACK` 指定的时间点需要在 Garbage Collection (GC) life time 时间内。你可以使用系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入) 配置数据的历史版本的保留时间（默认值是 `10m0s`）。可以使用以下 SQL 语句查询当前的 `safePoint`，即 GC 已经清理到的时间点：

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

* 执行 `FLASHBACK CLUSTER` SQL 语句的用户需要有 `SUPER` 权限。
* `FLASHBACK CLUSTER` 不支持回退修改 PD 相关信息的 DDL，如 `ALTER TABLE ATTRIBUTE`、`ALTER TABLE REPLICA`、`CREATE PLACEMENT POLICY` 等。
* `FLASHBACK CLUSTER` 指定的时间点不能存在未执行完成的 DDL 记录。若存在，TiDB 会拒绝该 DDL 操作。
* 在执行 `FLASHBACK CLUSTER TO TIMESTAMP` 前，TiDB 会主动断开所有相关表上的连接，并禁止对这些表进行读写操作，直到 `FLASHBACK CLUSTER` 完成。
* `FLASHBACK CLUSTER TO TIMESTAMP` 命令不能取消，一旦开始执行 TiDB 会一直重试，直到成功。
* 在 `FLASHBACK CLUSTER` 执行期间，若有数据备份需求，只支持使用 [BR 命令行工具进行快照备份](/br/br-snapshot-guide.md)，并需要指定早于 `FLASHBACK CLUSTER` 开始时间的 `BackupTS`。同时，在执行 `FLASHBACK CLUSTER` 期间，[开启日志备份](/br/br-pitr-guide.md)的操作会失败，请等待 `FLASHBACK CLUSTER` 结束后再尝试开启日志备份。
* 若 `FLASHBACK CLUSTER` 导致了元信息（表结构、库结构）的回滚，则相关的修改**不会**被 TiCDC 同步。因此，用户需主动暂停任务，待 `FLASHBACK CLUSTER` 完成后将上下游的 schema 定义手动同步一致，然后重新创建 TiCDC changefeed。

## 示例

恢复新插入的数据：

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

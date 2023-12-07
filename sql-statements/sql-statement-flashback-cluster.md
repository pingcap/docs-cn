---
title: FLASHBACK CLUSTER
summary: TiDB 数据库中 FLASHBACK CLUSTER 的使用概况。
aliases: ['/zh/tidb/v6.5/sql-statement-flashback-to-timestamp']
---

# FLASHBACK CLUSTER

TiDB v6.4.0 引入了 `FLASHBACK CLUSTER TO TIMESTAMP` 语法，其功能是将集群的数据恢复到过去指定的时间点。指定时间点时，你可以使用日期时间和时间函数，日期时间的格式为：'2016-10-08 16:45:26.999'，最小时间精度范围为毫秒，通常可只写到秒，例如 '2016-10-08 16:45:26'。

TiDB v6.5.6 开始引入了 `FLASHBACK CLUSTER TO TSO` 的语法，支持使用时间戳 [TSO](/tso.md) 更加精确地指定恢复时间点，实现更加灵活的数据恢复。

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
         ::= 'FLASHBACK' 'CLUSTER' 'TO' 'TIMESTAMP' stringLit
           | 'FLASHBACK' 'CLUSTER' 'TO' 'TSO' LengthNum
```

## 注意事项

* `FLASHBACK` 指定的时间点需要在 Garbage Collection (GC) life time 时间内。你可以使用系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入) 配置数据的历史版本的保留时间（默认值是 `10m0s`）。可以使用以下 SQL 语句查询当前的 `safePoint`，即 GC 已经清理到的时间点：

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

* 执行 `FLASHBACK CLUSTER` SQL 语句的用户需要有 `SUPER` 权限。
* 在 `FLASHBACK` 指定的时间点到开始执行的时间段内不能存在相关表结构变更的 DDL 记录。若存在，TiDB 会拒绝该 DDL 操作。
* 在执行 `FLASHBACK CLUSTER` 前，TiDB 会主动断开所有相关表上的连接，并禁止对这些表进行读写操作，直到 `FLASHBACK` 完成。
* `FLASHBACK CLUSTER` 命令不能取消，一旦开始执行 TiDB 会一直重试，直到成功。

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

如果从 `FLASHBACK` 指定的时间点到开始执行的时间段内有改变表结构的 DDL 记录，那么将执行失败：

```sql
mysql> SELECT now();
+---------------------+
| now()               |
+---------------------+
| 2022-10-09 16:40:51 |
+---------------------+
1 row in set (0.01 sec)

mysql> CREATE TABLE t(a int);
Query OK, 0 rows affected (0.12 sec)

mysql> FLASHBACK CLUSTER TO TIMESTAMP '2022-10-09 16:40:51';
ERROR 1105 (HY000): Detected schema change due to another DDL job during [2022-10-09 16:40:51 +0800 CST, now), can't do flashback
```

可以通过 [Raft admin > Peer in Flashback State](/grafana-tikv-dashboard.md#raft-admin) 监控项和日志查看 `FLASHBACK` 执行进度，具体的日志如下所示：

```
[2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

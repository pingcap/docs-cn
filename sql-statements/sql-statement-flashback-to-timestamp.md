---
title: FLASHBACK CLUSTER TO TIMESTAMP
summary: TiDB 数据库中 FLASHBACK CLUSTER TO TIMESTAMP 的使用概况。
---

# FLASHBACK CLUSTER TO TIMESTAMP

TiDB v6.4.0 引入了 `FLASHBACK CLUSTER TO TIMESTAMP` 语法，其功能是将集群的数据恢复到特定的时间点。

> **警告：**
>
> - 当前该功能为实验特性，不建议在生产环境中使用。
> - 在执行 `FLASHBACK CLUSTER TO TIMESTAMP` 之前，需要暂停 PITR 和 TiCDC 等工具上运行的同步任务，待 `FLASHBACK` 执行完成后再启动，否则会造成同步失败等问题。

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
* 在 `FLASHBACK` 指定的时间点到开始执行的时间段内不能存在相关表结构变更的 DDL 记录。若存在，TiDB 会拒绝该 DDL 操作。
* 在执行 `FLASHBACK CLUSTER TO TIMESTAMP` 前，TiDB 会主动断开所有相关表上的连接，并禁止对这些表进行读写操作，直到 `FLASHBACK` 完成。
* `FLASHBACK CLUSTER TO TIMESTAMP` 命令不能取消，一旦开始执行 TiDB 会一直重试，直到成功。

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

可以通过日志查看 `FLASHBACK` 执行进度，具体的日志如下所示：

```
[2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

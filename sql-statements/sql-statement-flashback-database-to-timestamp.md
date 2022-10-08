---
title: FLASHBACK DATABASE TO TIMESTAMP
aliases: ['/docs-cn/dev/sql-statements/sql-statement-flashback-database-to-timestamp/', '/docs-cn/dev/reference/sql/statements/flashback-database-to-timestamp/']
---

# FLASHBACK DATABASE

在 TiDB 6.4 中，引入了 `FLASHBACK DATABASE TO TIMESTAMP` 语法，其功能是将指定 DATABASE 的数据恢复到特定的时间点。

## 语法

{{< copyable "sql" >}}

```sql
FLASHBACK DATABASE [db1], [db2] TO TIMESATMP '2022-09-21 16:02:50';
```

### 语法图

```ebnf+diagram
FlashbackDatabaseStmt ::=
    "FLASHBACK" "DATABASE" DBNameList "TO" "TIMESTAMP" stringLit
```

## 注意事项

* `FLASHBACK` 指定的时间点需要在 Garbage Collection (GC) life time 时间内，可以使用系统变量 `tidb_gc_life_time` 配置数据的历史版本的保留时间（默认值是 10m0s）。可以使用以下 SQL 语句查询当前的 safePoint，即 GC 已经清理到的时间点：

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

* 执行 `FLASHBACK DATABASE` 需要有 DATABASE 权限。
* 在 `FLASHBACK DATABASE` 指定的时间点到开始执行的时间段内不能存在相关的 DDL 执行记录。
* 在执行 `FLASHBACK DATABASE` 期间，TiDB 会主动断开所有相关的链接和正在执行的事务，直到 `FLASHBACK DATABASE` 完成。
* `FLASHBACK DATABASE` 命令不能取消，一旦开始执行会一直重试，直到成功。

## 示例

* 恢复新插入的数据

```sql
mysql> use test;
Query OK, 0 rows affected (0.00 sec)

mysql> create table t(a int);
Query OK, 0 rows affected (0.09 sec)

mysql> select * from t;
Empty set (0.01 sec)

mysql> select now();
+---------------------+
| now()               |
+---------------------+
| 2022-09-28 17:24:16 |
+---------------------+
1 row in set (0.02 sec)

mysql> insert into t values (1);
Query OK, 1 row affected (0.02 sec)

mysql> select * from t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)

mysql> flashback database test to timestamp '2022-09-28 17:24:16';
Query OK, 0 rows affected (0.20 sec)

mysql> select * from t;
Empty set (0.00 sec)
```

## 工作原理

具体工作原理可以参考[`FALSHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster-to-timestamp.md)

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

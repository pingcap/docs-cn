---
title: FLASHBACK CLUSTER TO TIMESTAMP
summary: Learn the usage of FLASHBACK CLUSTER TO TIMESTAMP in TiDB databases.
---

# FLASHBACK CLUSTER TO TIMESTAMP

TiDB v6.4.0 introduces the `FLASHBACK CLUSTER TO TIMESTAMP` syntax. You can use it to restore a cluster to a specific point in time.

> **Note:**
>
> The working principle of `FLASHBACK CLUSTER TO TIMESTAMP` is to write the old data of a specific point in time with the latest timestamp, and will not delete the current data. So before using this feature, you need to ensure that there is enough storage space for the old data and the current data.

## Syntax

```sql
FLASHBACK CLUSTER TO TIMESTAMP '2022-09-21 16:02:50';
```

### Synopsis

```ebnf+diagram
FlashbackToTimestampStmt ::=
    "FLASHBACK" "CLUSTER" "TO" "TIMESTAMP" stringLit
```

## Notes

* The time specified in the `FLASHBACK` statement must be within the Garbage Collection (GC) lifetime. The system variable [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (default: `10m0s`) defines the retention time of earlier versions of rows. The current `safePoint` of where garbage collection has been performed up to can be obtained with the following query:

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

* Only a user with the `SUPER` privilege can execute the `FLASHBACK CLUSTER` SQL statement.
* From the time specified in the `FLASHBACK` statement to the time when the `FLASHBACK` is executed, there cannot be a DDL statement that changes the related table structure. If such a DDL exists, TiDB will reject it.
* Before executing `FLASHBACK CLUSTER TO TIMESTAMP`, TiDB disconnects all related connections and prohibits read and write operations on these tables until the `FLASHBACK` statement is completed.
* The `FLASHBACK CLUSTER TO TIMESTAMP` statement cannot be canceled after being executed. TiDB will keep retrying until it succeeds.

## Example

The following example shows how to restore the newly inserted data:

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

If there is a DDL statement that changes the table structure from the time specified in the `FLASHBACK` statement to the time when the `FLASHBACK` is executed, the `FLASHBACK` statement fails:

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

Through the log, you can obtain the execution progress of `FLASHBACK`. The following is an example:

```
[2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

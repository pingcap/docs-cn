---
title: FLASHBACK CLUSTER
summary: Learn the usage of FLASHBACK CLUSTER in TiDB databases.
aliases: ['/tidb/dev/sql-statement-flashback-to-timestamp']
---

# FLASHBACK CLUSTER

TiDB v6.4.0 introduces the `FLASHBACK CLUSTER TO TIMESTAMP` syntax. You can use it to restore a cluster to a specific point in time. When specifying the timestamp, you can either set a datetime value or use a time function. The format of datetime is like '2016-10-08 16:45:26.999', with millisecond as the minimum time unit. But in most cases, specifying the timestamp with second as the time unit is sufficient, for example, '2016-10-08 16:45:26'.

Starting from v6.5.6, v7.1.3, and v7.6.0, TiDB introduces the `FLASHBACK CLUSTER TO TSO` syntax. This syntax enables you to use [TSO](/tso.md) to specify a more precise recovery point in time, thereby enhancing flexibility in data recovery.

> **Warning:**
>
> The `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` syntax is not applicable to [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters. To avoid unexpected results, do not execute this statement on TiDB Serverless clusters.

<CustomContent platform="tidb">

> **Warning:**
>
> When you use this feature in TiDB v7.1.0, some Regions might remain in the FLASHBACK process even after the completion of the FLASHBACK operation. It is recommended to avoid using this feature in v7.1.0. For more information, see issue [#44292](https://github.com/pingcap/tidb/issues/44292).
>
> If you have encountered this issue, you can use the [TiDB snapshot backup and restore](/br/br-snapshot-guide.md) feature to restore data.

</CustomContent>

> **Note:**
>
> The working principle of `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` is to write the old data of a specific point in time with the latest timestamp, and will not delete the current data. So before using this feature, you need to ensure that there is enough storage space for the old data and the current data.

## Syntax

```sql
FLASHBACK CLUSTER TO TIMESTAMP '2022-09-21 16:02:50';
FLASHBACK CLUSTER TO TSO 445494839813079041;
```

### Synopsis

```ebnf+diagram
FlashbackToTimestampStmt
         ::= 'FLASHBACK' 'CLUSTER' 'TO' 'TIMESTAMP' stringLit
           | 'FLASHBACK' 'CLUSTER' 'TO' 'TSO' LengthNum
```

## Notes

* The time specified in the `FLASHBACK` statement must be within the Garbage Collection (GC) lifetime. The system variable [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (default: `10m0s`) defines the retention time of earlier versions of rows. The current `safePoint` of where garbage collection has been performed up to can be obtained with the following query:

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

<CustomContent platform='tidb'>

* Only a user with the `SUPER` privilege can execute the `FLASHBACK CLUSTER` SQL statement.
* `FLASHBACK CLUSTER` does not support rolling back DDL statements that modify PD-related information, such as `ALTER TABLE ATTRIBUTE`, `ALTER TABLE REPLICA`, and `CREATE PLACEMENT POLICY`.
* At the time specified in the `FLASHBACK` statement, there cannot be a DDL statement that is not completely executed. If such a DDL exists, TiDB will reject it.
* Before executing `FLASHBACK CLUSTER`, TiDB disconnects all related connections and prohibits read and write operations on these tables until the `FLASHBACK CLUSTER` statement is completed.
* The `FLASHBACK CLUSTER` statement cannot be canceled after being executed. TiDB will keep retrying until it succeeds.
* During the execution of `FLASHBACK CLUSTER`, if you need to back up data, you can only use [Backup & Restore](/br/br-snapshot-guide.md) and specify a `BackupTS` that is earlier than the start time of `FLASHBACK CLUSTER`. In addition, during the execution of `FLASHBACK CLUSTER`, enabling [log backup](/br/br-pitr-guide.md) will fail. Therefore, try to enable log backup after `FLASHBACK CLUSTER` is completed.
* If the `FLASHBACK CLUSTER` statement causes the rollback of metadata (table structure, database structure), the related modifications will **not** be replicated by TiCDC. Therefore, you need to pause the task manually, wait for the completion of `FLASHBACK CLUSTER`, and manually replicate the schema definitions of the upstream and downstream to make sure that they are consistent. After that, you need to recreate the TiCDC changefeed.

</CustomContent>

<CustomContent platform='tidb-cloud'>

* Only a user with the `SUPER` privilege can execute the `FLASHBACK CLUSTER` SQL statement.
* `FLASHBACK CLUSTER` does not support rolling back DDL statements that modify PD-related information, such as `ALTER TABLE ATTRIBUTE`, `ALTER TABLE REPLICA`, and `CREATE PLACEMENT POLICY`.
* At the time specified in the `FLASHBACK` statement, there cannot be a DDL statement that is not completely executed. If such a DDL exists, TiDB will reject it.
* Before executing `FLASHBACK CLUSTER`, TiDB disconnects all related connections and prohibits read and write operations on these tables until the `FLASHBACK CLUSTER` statement is completed.
* The `FLASHBACK CLUSTER` statement cannot be canceled after being executed. TiDB will keep retrying until it succeeds.
* If the `FLASHBACK CLUSTER` statement causes the rollback of metadata (table structure, database structure), the related modifications will **not** be replicated by TiCDC. Therefore, you need to pause the task manually, wait for the completion of `FLASHBACK CLUSTER`, and manually replicate the schema definitions of the upstream and downstream to make sure that they are consistent. After that, you need to recreate the TiCDC changefeed.

</CustomContent>

## Example

The following example shows how to flashback a cluster to a specific timestamp to restore newly inserted data:

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

The following example shows how to flashback a cluster to a specific TSO to precisely restore mistakenly deleted data:

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

mysql> SELECT @@tidb_current_ts;  -- Get the current TSO
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

If there is a DDL statement that is not completely executed at the time specified in the `FLASHBACK` statement, the `FLASHBACK` statement fails:

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

Through the log, you can obtain the execution progress of `FLASHBACK`. The following is an example:

```
[2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

---
title: PROCESSLIST
summary: Learn the `PROCESSLIST` information_schema table.
---

# PROCESSLIST

`PROCESSLIST`, just like `SHOW PROCESSLIST`, is used to view the requests that are being handled.

The `PROCESSLIST` table has additional columns not present in `SHOW PROCESSLIST`:

* A `MEM` column to show memory occupied by the request being handled (in bytes)
* A `TxnStart` column to show the start time of the transaction

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC processlist;
```

```
+----------+---------------------+------+------+---------+-------+
| Field    | Type                | Null | Key  | Default | Extra |
+----------+---------------------+------+------+---------+-------+
| ID       | bigint(21) unsigned | NO   |      | 0       |       |
| USER     | varchar(16)         | NO   |      |         |       |
| HOST     | varchar(64)         | NO   |      |         |       |
| DB       | varchar(64)         | YES  |      | NULL    |       |
| COMMAND  | varchar(16)         | NO   |      |         |       |
| TIME     | int(7)              | NO   |      | 0       |       |
| STATE    | varchar(7)          | YES  |      | NULL    |       |
| INFO     | binary(512)         | YES  |      | NULL    |       |
| MEM      | bigint(21) unsigned | YES  |      | NULL    |       |
| TxnStart | varchar(64)         | NO   |      |         |       |
+----------+---------------------+------+------+---------+-------+
10 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM processlist\G
```

```
*************************** 1. row ***************************
      ID: 16
    USER: root
    HOST: 127.0.0.1
      DB: information_schema
 COMMAND: Query
    TIME: 0
   STATE: autocommit
    INFO: SELECT * FROM processlist
     MEM: 0
TxnStart:
1 row in set (0.00 sec)
```

Fields in the `PROCESSLIST` table are described as follows:

* ID: The ID of the user connection.
* USER: The name of the user who is executing `PROCESS`.
* HOST: The address that the user is connecting to.
* DB: The name of the currently connected default database.
* COMMAND: The command type that `PROCESS` is executing.
* TIME: The current execution duration of `PROCESS`, in seconds.
* STATE: The current connection state.
* INFO: The requested statement that is being processed.
* MEM: The memory used by the request that is being processed, in bytes.

## CLUSTER_PROCESSLIST

`CLUSTER_PROCESSLIST` is the cluster system table corresponding to `PROCESSLIST`. It is used to query the `PROCESSLIST` information of all TiDB nodes in the cluster. The table schema of `CLUSTER_PROCESSLIST` has one more column than `PROCESSLIST`, the `INSTANCE` column, which stores the address of the TiDB node this row of data is from.

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.cluster_processlist;
```

```sql
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
| INSTANCE        | ID  | USER | HOST     | DB   | COMMAND | TIME | STATE      | INFO                                                 | MEM | TxnStart                               |
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
| 10.0.1.22:10080 | 150 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077223) |
| 10.0.1.22:10080 | 138 | root | 10.0.1.1 | test | Query   | 0    | autocommit | SELECT * FROM information_schema.cluster_processlist | 0   | 05-28 03:54:21.230(416976223923077220) |
| 10.0.1.22:10080 | 151 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077224) |
| 10.0.1.21:10080 | 15  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077222) |
| 10.0.1.21:10080 | 14  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077225) |
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
```

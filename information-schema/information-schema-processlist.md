---
title: PROCESSLIST
summary: 了解 information_schema 表 `PROCESSLIST`。
---

# PROCESSLIST

`PROCESSLIST` 和 `SHOW PROCESSLIST` 的功能一样，都是查看当前正在处理的请求。

`PROCESSLIST` 表比 `SHOW PROCESSLIST` 的结果多出下面几列：

* `MEM` 列：`MEM` 显示正在处理的请求已使用的内存，单位是 byte。
* `TxnStart`列：显示事务的开始时间

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC processlist;
```

```sql
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

```sql
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

`PROCESSLIST` 表各列的含义如下：

* ID：客户连接 ID。
* USER：执行当前 PROCESS 的用户名。
* HOST：客户连接的地址。
* DB：当前连接的默认数据库名。
* COMMAND：当前 PROCESS 执行的命令类型。
* TIME：当前 PROCESS 的已经执行的时间，单位是秒。
* STATE：当前连接的状态。
* INFO：正在处理的请求语句。
* MEM：正在处理的请求已使用的内存，单位是 byte。
* `TxnStart`列：显示事务的开始时间

## CLUSTER_PROCESSLIST

`CLUSTER_PROCESSLIST` 是 `PROCESSLIST` 对应的集群系统表，用于查询集群中所有 TiDB 节点的 `PROCESSLIST` 信息。`CLUSTER_PROCESSLIST` 表结构上比 `PROCESSLIST` 多一列 `INSTANCE`，表示该行数据来自的 TiDB 节点地址。

{{< copyable "sql" >}}

```sql
SELECT * FROM cluster_processlist;
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

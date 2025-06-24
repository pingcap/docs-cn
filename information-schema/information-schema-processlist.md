---
title: PROCESSLIST
summary: 了解 `PROCESSLIST` information_schema 表。
---

# PROCESSLIST

`PROCESSLIST` 与 [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) 一样，用于查看正在处理的请求。

`PROCESSLIST` 表比 `SHOW PROCESSLIST` 多了以下列：

* `DIGEST` 列，用于显示 SQL 语句的摘要。
* `MEM` 列，用于显示正在处理的请求使用的内存，单位为字节。
* `DISK` 列，用于显示磁盘使用量，单位为字节。
* `TxnStart` 列，用于显示事务的开始时间。
* `RESOURCE_GROUP` 列，用于显示资源组名称。

```sql
USE information_schema;
DESC processlist;
```

```sql
+---------------------+---------------------+------+------+---------+-------+
| Field               | Type                | Null | Key  | Default | Extra |
+---------------------+---------------------+------+------+---------+-------+
| ID                  | bigint(21) unsigned | NO   |      | 0       |       |
| USER                | varchar(16)         | NO   |      |         |       |
| HOST                | varchar(64)         | NO   |      |         |       |
| DB                  | varchar(64)         | YES  |      | NULL    |       |
| COMMAND             | varchar(16)         | NO   |      |         |       |
| TIME                | int(7)              | NO   |      | 0       |       |
| STATE               | varchar(7)          | YES  |      | NULL    |       |
| INFO                | longtext            | YES  |      | NULL    |       |
| DIGEST              | varchar(64)         | YES  |      |         |       |
| MEM                 | bigint(21) unsigned | YES  |      | NULL    |       |
| DISK                | bigint(21) unsigned | YES  |      | NULL    |       |
| TxnStart            | varchar(64)         | NO   |      |         |       |
| RESOURCE_GROUP      | varchar(32)         | NO   |      |         |       |
+---------------------+---------------------+------+------+---------+-------+
13 rows in set (0.00 sec)
```

```sql
SELECT * FROM processlist\G
```

```sql
*************************** 1. row ***************************
                 ID: 2300033189772525975
               USER: root
               HOST: 127.0.0.1:51289
                 DB: NULL
            COMMAND: Query
               TIME: 0
              STATE: autocommit
               INFO: SELECT * FROM processlist
             DIGEST: dbfaa16980ec628011029f0aaf0d160f4b040885240dfc567bf760d96d374f7e
                MEM: 0
               DISK: 0
           TxnStart:
     RESOURCE_GROUP: rg1
1 row in set (0.00 sec)
```

`PROCESSLIST` 表中的字段说明如下：

* ID：用户连接的 ID。
* USER：执行 `PROCESS` 的用户名。
* HOST：用户连接的地址。
* DB：当前连接的默认数据库名称。
* COMMAND：`PROCESS` 正在执行的命令类型。
* TIME：`PROCESS` 当前执行的持续时间，单位为秒。
* STATE：当前连接状态。
* INFO：正在处理的请求语句。
* DIGEST：SQL 语句的摘要。
* MEM：正在处理的请求使用的内存，单位为字节。
* DISK：磁盘使用量，单位为字节。
* TxnStart：事务的开始时间。
* RESOURCE_GROUP：资源组名称。

## CLUSTER_PROCESSLIST

`CLUSTER_PROCESSLIST` 是对应于 `PROCESSLIST` 的集群系统表，用于查询集群中所有 TiDB 节点的 `PROCESSLIST` 信息。`CLUSTER_PROCESSLIST` 的表结构比 `PROCESSLIST` 多一列 `INSTANCE`，用于存储该行数据来自哪个 TiDB 节点的地址。

```sql
SELECT * FROM information_schema.cluster_processlist;
```

```sql
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+----------------+
| INSTANCE        | ID  | USER | HOST     | DB   | COMMAND | TIME | STATE      | INFO                                                 | MEM | TxnStart                               | RESOURCE_GROUP | 
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+----------------+

| 10.0.1.22:10080 | 150 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077223) | default        |
| 10.0.1.22:10080 | 138 | root | 10.0.1.1 | test | Query   | 0    | autocommit | SELECT * FROM information_schema.cluster_processlist | 0   | 05-28 03:54:21.230(416976223923077220) | rg1            |
| 10.0.1.22:10080 | 151 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077224) | rg2            |
| 10.0.1.21:10080 | 15  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077222) | default        |
| 10.0.1.21:10080 | 14  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077225) | default        |
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+----------------+
```

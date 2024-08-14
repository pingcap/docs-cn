---
title: PROCESSLIST
summary: 了解 information_schema 表 `PROCESSLIST`。
aliases: ['/docs-cn/dev/information-schema/information-schema-processlist/']
---

# PROCESSLIST

`PROCESSLIST` 和 [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) 的功能一样，都是查看当前正在处理的请求。

`PROCESSLIST` 表比 `SHOW PROCESSLIST` 的结果多出下面几列：

* `DIGEST` 列：显示 SQL 语句的 digest。
* `MEM` 列：显示正在处理的请求已使用的内存，单位是 byte。
* `DISK` 列：显示磁盘空间使用情况，单位是 byte。
* `TxnStart`列：显示事务的开始时间。
* `RESOURCE_GROUP`列：显示对应的资源组名称。

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

`PROCESSLIST` 表各列的含义如下：

* `ID` 列：客户连接 ID。
* `USER` 列：执行当前 PROCESS 的用户名。
* `HOST` 列：客户连接的地址。
* `DB` 列：当前连接的默认数据库名。
* `COMMAND` 列：当前 PROCESS 执行的命令类型。
* `TIME` 列：当前 PROCESS 的已经执行的时间，单位是秒。
* `STATE` 列：当前连接的状态。
* `INFO` 列：正在处理的请求语句。
* `DIGEST` 列：SQL 语句的 digest。
* `MEM` 列：正在处理的请求已使用的内存，单位是 byte。
* `DISK` 列：磁盘空间使用情况，单位是 byte。
* `TxnStart`列：显示事务的开始时间。
* `RESOURCE_GROUP`列：显示对应的资源组名称。

## CLUSTER_PROCESSLIST

`CLUSTER_PROCESSLIST` 是 `PROCESSLIST` 对应的集群系统表，用于查询集群中所有 TiDB 节点的 `PROCESSLIST` 信息。`CLUSTER_PROCESSLIST` 表结构上比 `PROCESSLIST` 多一列 `INSTANCE`，表示该行数据来自的 TiDB 节点地址。

{{< copyable "sql" >}}

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

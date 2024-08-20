---
title: TIDB_SERVERS_INFO
summary: 了解 INFORMATION_SCHEMA 表 `TIDB_SERVERS_INFO`。
---

# TIDB_SERVERS_INFO

`TIDB_SERVERS_INFO` 表提供了 TiDB 集群中 TiDB 服务器的信息（即 tidb-server 进程）。

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_SERVERS_INFO;
```

输出结果如下：

```sql
+---------------+--------------+------+------+---------+-------+
| Field         | Type         | Null | Key  | Default | Extra |
+---------------+--------------+------+------+---------+-------+
| DDL_ID        | varchar(64)  | YES  |      | NULL    |       |
| IP            | varchar(64)  | YES  |      | NULL    |       |
| PORT          | bigint(21)   | YES  |      | NULL    |       |
| STATUS_PORT   | bigint(21)   | YES  |      | NULL    |       |
| LEASE         | varchar(64)  | YES  |      | NULL    |       |
| VERSION       | varchar(64)  | YES  |      | NULL    |       |
| GIT_HASH      | varchar(64)  | YES  |      | NULL    |       |
| BINLOG_STATUS | varchar(64)  | YES  |      | NULL    |       |
| LABELS        | varchar(128) | YES  |      | NULL    |       |
+---------------+--------------+------+------+---------+-------+
9 rows in set (0.00 sec)
```

查看 `TIDB_SERVERS_INFO` 表的信息：

```sql
SELECT * FROM TIDB_SERVERS_INFO\G
```

输出结果如下：

```sql
*************************** 1. row ***************************
       DDL_ID: 771c169d-0a3a-48ea-a93c-a4d6751d3674
           IP: 0.0.0.0
         PORT: 4000
  STATUS_PORT: 10080
        LEASE: 45s
      VERSION: 8.0.11-TiDB-v8.3.0
     GIT_HASH: 635a4362235e8a3c0043542e629532e3c7bb2756
BINLOG_STATUS: Off
       LABELS:
1 row in set (0.006 sec)
```

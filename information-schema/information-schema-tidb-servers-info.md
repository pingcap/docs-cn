---
title: TIDB_SERVERS_INFO
summary: 了解 `TIDB_SERVERS_INFO` INFORMATION_SCHEMA 表。
---

# TIDB_SERVERS_INFO

`TIDB_SERVERS_INFO` 表提供了 TiDB 集群中 TiDB 服务器（即 tidb-server 进程）的信息。

> **注意：**
>
> 此表在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

```sql
USE INFORMATION_SCHEMA;
DESC tidb_servers_info;
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

查看 `TIDB_SERVERS_INFO` 表：

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
      VERSION: 8.0.11-TiDB-v8.1.2
     GIT_HASH: 827d8ff2d22ac4c93ae1b841b79d468211e1d393
BINLOG_STATUS: Off
       LABELS:
1 row in set (0.006 sec)
```

---
title: MEMORY_USAGE_OPS_HISTORY
summary: 了解 `MEMORY_USAGE_OPS_HISTORY` information_schema 系统表。
---

# MEMORY_USAGE_OPS_HISTORY

`MEMORY_USAGE_OPS_HISTORY` 表描述了当前 TiDB 实例的内存相关操作历史记录和执行依据。

```sql
USE information_schema;
DESC memory_usage_ops_history;
```

```sql
+----------------+---------------------+------+------+---------+-------+
| Field          | Type                | Null | Key  | Default | Extra |
+----------------+---------------------+------+------+---------+-------+
| TIME           | datetime            | NO   |      | NULL    |       |
| OPS            | varchar(20)         | NO   |      | NULL    |       |
| MEMORY_LIMIT   | bigint(21)          | NO   |      | NULL    |       |
| MEMORY_CURRENT | bigint(21)          | NO   |      | NULL    |       |
| PROCESSID      | bigint(21) unsigned | YES  |      | NULL    |       |
| MEM            | bigint(21) unsigned | YES  |      | NULL    |       |
| DISK           | bigint(21) unsigned | YES  |      | NULL    |       |
| CLIENT         | varchar(64)         | YES  |      | NULL    |       |
| DB             | varchar(64)         | YES  |      | NULL    |       |
| USER           | varchar(16)         | YES  |      | NULL    |       |
| SQL_DIGEST     | varchar(64)         | YES  |      | NULL    |       |
| SQL_TEXT       | varchar(256)        | YES  |      | NULL    |       |
+----------------+---------------------+------+------+---------+-------+
12 rows in set (0.000 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.memory_usage_ops_history;
```

```sql
+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
| TIME                | OPS         | MEMORY_LIMIT | MEMORY_CURRENT | PROCESSID           | MEM        | DISK | CLIENT          | DB   | USER | SQL_DIGEST                                                       | SQL_TEXT                                                             |
+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
| 2022-10-17 22:46:25 | SessionKill |  10737418240 |    10880237568 | 6718275530455515543 | 7905028235 |    0 | 127.0.0.1:34394 | test | root | 146b3d812852663a20635fbcf02be01688f52c8d433dafec0d496a14f0b59df6 | desc analyze select * from t t1 join t t2 on t1.a=t2.a order by t1.a |
+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
2 rows in set (0.002 sec)
```

`MEMORY_USAGE_OPS_HISTORY` 表中的列说明如下：

* `TIME`：会话终止的时间戳。
* `OPS`："SessionKill"
* `MEMORY_LIMIT`：终止时 TiDB 的内存使用限制，单位为字节。其值与系统变量 `tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) 的值相同。
* `MEMORY_CURRENT`：TiDB 当前的内存使用量，单位为字节。
* `PROCESSID`：被终止会话的连接 ID。
* `MEM`：被终止会话的内存使用量，单位为字节。
* `DISK`：被终止会话的磁盘使用量，单位为字节。
* `CLIENT`：被终止会话的客户端连接地址。
* `DB`：被终止会话连接的数据库名称。
* `USER`：被终止会话的用户名。
* `SQL_DIGEST`：被终止会话中正在执行的 SQL 语句的摘要。
* `SQL_TEXT`：被终止会话中正在执行的 SQL 语句。

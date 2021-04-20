---
title: CLIENT_ERRORS_SUMMARY_GLOBAL
summary: 了解 information_schema 表 `CLIENT_ERRORS_SUMMARY_GLOBAL`。
---

# CLIENT_ERRORS_SUMMARY_GLOBAL

`CLIENT_ERRORS_SUMMARY_GLOBAL` 表汇总了已返回给连接到 TiDB 服务器的客户端的 SQL 错误和警告。这些错误和警告包括：

* 格式错误的 SQL 语句。
* 除以零错误。
* 尝试插入超出范围或重复的键值。
* 权限错误。
* 表不存在。

以上错误通过 MySQL 服务器协议返回给客户端，此时应用程序应在客户端采取适当操作。`information_schema`.`CLIENT_ERRORS_SUMMARY_BY_GLOBAL` 表提供了高级概述，在应用程序无法正确处理（或记录）TiDB 服务器返回的错误的情况下很有用。

可以使用 `FLUSH CLIENT_ERRORS_SUMMARY` 语句重置汇总的计数。所汇总的是每个 TiDB 服务器的本地数据，并且只保留在内存中。如果 TiDB 服务器重新启动，会丢失汇总信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC CLIENT_ERRORS_SUMMARY_GLOBAL;
```

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| ERROR_NUMBER  | bigint(64)    | NO   |      | NULL    |       |
| ERROR_MESSAGE | varchar(1024) | NO   |      | NULL    |       |
| ERROR_COUNT   | bigint(64)    | NO   |      | NULL    |       |
| WARNING_COUNT | bigint(64)    | NO   |      | NULL    |       |
| FIRST_SEEN    | timestamp     | YES  |      | NULL    |       |
| LAST_SEEN     | timestamp     | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

字段说明如下：

* `ERROR_NUMBER`：返回的与 MySQL 兼容的错误码。
* `ERROR_MESSAGE`：与错误码匹配的错误消息（预处理语句形式）。
* `ERROR_COUNT`：返回此错误的次数。
* `WARNING_COUNT`：返回此警告的次数。
* `FIRST_SEEN`：首次返回此错误（或警告）的时间。
* `LAST_SEEN`：最近一次发送此错误（或警告）的时间。

以下示例显示了客户端连接到本地 TiDB 服务器时生成的警告。执行 `FLUSH CLIENT_ERRORS_SUMMARY` 语句后，会重置汇总。

{{< copyable "sql" >}}

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
```

```sql
+-----+
| 0/0 |
+-----+
| NULL |
+-----+
1 row in set, 1 warning (0.00 sec)

+--------------+---------------+-------------+---------------+---------------------+---------------------+
| ERROR_NUMBER | ERROR_MESSAGE | ERROR_COUNT | WARNING_COUNT | FIRST_SEEN          | LAST_SEEN           |
+--------------+---------------+-------------+---------------+---------------------+---------------------+
|         1365 | Division by 0 |           0 |             1 | 2021-03-18 13:10:51 | 2021-03-18 13:10:51 |
+--------------+---------------+-------------+---------------+---------------------+---------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Empty set (0.00 sec)
```
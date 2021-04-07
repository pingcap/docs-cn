---
title: CLIENT_ERRORS_SUMMARY_BY_HOST
summary: 了解 information_schema 表 `CLIENT_ERRORS_SUMMARY_BY_HOST`。
---

# CLIENT_ERRORS_SUMMARY_BY_HOST

`CLIENT_ERRORS_SUMMARY_BY_HOST` 表汇总了已返回给连接到 TiDB 服务器的客户端的 SQL 错误和警告。这些错误和警告包括：

* 格式错误的 SQL 语句。
* 除以零错误。
* 尝试插入超出范围或重复的键值。
* 权限错误。
* 表不存在。

以上错误通过 MySQL 服务器协议返回给客户端，此时应用程序应在客户端采取适当操作。`information_schema`.`CLIENT_ERRORS_SUMMARY_BY_HOST` 表提供了一种有效方法，能够在应用程序没有正确处理（或记录）TiDB 服务器返回的错误的情况下检查错误。

由于 `CLIENT_ERRORS_SUMMARY_BY_HOST` 会基于每个远程主机汇总错误，在诊断其中一台应用程序服务器比其他服务器生成更多错误的情况时很有用。可能的情况包括：

* 过时的 MySQL 客户端库。
* 过时的应用程序（可能是在推出新部署时遗漏了此服务器）。
* 用户权限中“主机”部分的使用不正确。
* 网络连接不可靠，导致更多超时或连接断开。

可以使用 `FLUSH CLIENT_ERRORS_SUMMARY` 语句重置汇总的计数。所汇总的是每个 TiDB 服务器的本地数据，并且只保留在内存中。如果 TiDB 服务器重新启动，会丢失汇总信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC CLIENT_ERRORS_SUMMARY_BY_HOST;
```

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| HOST          | varchar(255)  | NO   |      | NULL    |       |
| ERROR_NUMBER  | bigint(64)    | NO   |      | NULL    |       |
| ERROR_MESSAGE | varchar(1024) | NO   |      | NULL    |       |
| ERROR_COUNT   | bigint(64)    | NO   |      | NULL    |       |
| WARNING_COUNT | bigint(64)    | NO   |      | NULL    |       |
| FIRST_SEEN    | timestamp     | YES  |      | NULL    |       |
| LAST_SEEN     | timestamp     | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

字段说明如下：

* `HOST`：客户端的远程主机。
* `ERROR_NUMBER`：返回的与 MySQL 兼容的错误码。
* `ERROR_MESSAGE`：与错误码匹配的错误消息（预处理语句形式）。
* `ERROR_COUNT`：此错误返回到客户端主机的次数。
* `WARNING_COUNT`：此警告返回到客户端主机的次数。
* `FIRST_SEEN`：首次从客户端主机看到此错误（或警告）的时间。
* `LAST_SEEN`：最近一次从客户端主机看到此错误（或警告）的时间。

以下示例显示了客户端连接到本地 TiDB 服务器时生成的警告。执行 `FLUSH CLIENT_ERRORS_SUMMARY` 语句后，会重置汇总。

{{< copyable "sql" >}}

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
```

```sql
+-----+
| 0/0 |
+-----+
| NULL |
+-----+
1 row in set, 1 warning (0.00 sec)

+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| HOST      | ERROR_NUMBER | ERROR_MESSAGE | ERROR_COUNT | WARNING_COUNT | FIRST_SEEN          | LAST_SEEN           |
+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| 127.0.0.1 |         1365 | Division by 0 |           0 |             1 | 2021-03-18 12:51:54 | 2021-03-18 12:51:54 |
+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Empty set (0.00 sec)
```

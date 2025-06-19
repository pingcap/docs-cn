---
title: CLIENT_ERRORS_SUMMARY_BY_USER
summary: 了解 `CLIENT_ERRORS_SUMMARY_BY_USER` INFORMATION_SCHEMA 表。
---

# CLIENT_ERRORS_SUMMARY_BY_USER

`CLIENT_ERRORS_SUMMARY_BY_USER` 表提供了连接到 TiDB 服务器的客户端收到的 SQL 错误和警告的摘要信息。这些包括：

* 格式错误的 SQL 语句。
* 除零错误。
* 尝试插入超出范围或重复键值。
* 权限错误。
* 表不存在。

客户端错误通过 MySQL 服务器协议返回给客户端，应用程序需要采取适当的操作。在应用程序没有正确处理（或记录）TiDB 服务器返回的错误的情况下，`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_USER` 表提供了一种检查错误的有用方法。

由于 `CLIENT_ERRORS_SUMMARY_BY_USER` 按用户汇总错误，因此它可以用于诊断某个用户服务器产生的错误比其他服务器多的情况。可能的场景包括：

* 权限错误。
* 缺少表或关系对象。
* SQL 语法错误，或应用程序与 TiDB 版本之间的不兼容。

可以使用 `FLUSH CLIENT_ERRORS_SUMMARY` 语句重置汇总计数。摘要信息仅在每个 TiDB 服务器本地保存，并且只保存在内存中。如果 TiDB 服务器重启，摘要信息将会丢失。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_BY_USER;
```

输出结果如下：

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| USER          | varchar(64)   | NO   |      | NULL    |       |
| ERROR_NUMBER  | bigint(64)    | NO   |      | NULL    |       |
| ERROR_MESSAGE | varchar(1024) | NO   |      | NULL    |       |
| ERROR_COUNT   | bigint(64)    | NO   |      | NULL    |       |
| WARNING_COUNT | bigint(64)    | NO   |      | NULL    |       |
| FIRST_SEEN    | timestamp     | YES  |      | NULL    |       |
| LAST_SEEN     | timestamp     | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

字段说明：

* `USER`：已认证的用户。
* `ERROR_NUMBER`：返回的 MySQL 兼容错误号。
* `ERROR_MESSAGE`：与错误号匹配的错误消息（以预处理语句形式）。
* `ERROR_COUNT`：此错误返回给用户的次数。
* `WARNING_COUNT`：此警告返回给用户的次数。
* `FIRST_SEEN`：此错误（或警告）首次发送给用户的时间。
* `LAST_SEEN`：此错误（或警告）最近一次发送给用户的时间。

以下示例展示了客户端连接到本地 TiDB 服务器时生成的警告。执行 `FLUSH CLIENT_ERRORS_SUMMARY` 后重置摘要：

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_USER;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_USER;
```

输出结果如下：

```sql
+-----+
| 0/0 |
+-----+
| NULL |
+-----+
1 row in set, 1 warning (0.00 sec)

+------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| USER | ERROR_NUMBER | ERROR_MESSAGE | ERROR_COUNT | WARNING_COUNT | FIRST_SEEN          | LAST_SEEN           |
+------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| root |         1365 | Division by 0 |           0 |             1 | 2021-03-18 13:05:36 | 2021-03-18 13:05:36 |
+------+--------------+---------------+-------------+---------------+---------------------+---------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Empty set (0.00 sec)
```

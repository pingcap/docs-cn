---
title: CLIENT_ERRORS_SUMMARY_BY_HOST
summary: 了解 `CLIENT_ERRORS_SUMMARY_BY_HOST` INFORMATION_SCHEMA 表。
---

# CLIENT_ERRORS_SUMMARY_BY_HOST

`CLIENT_ERRORS_SUMMARY_BY_HOST` 表提供了返回给连接到 TiDB 服务器的客户端的 SQL 错误和警告的摘要。这些包括：

* 格式错误的 SQL 语句。
* 除零错误。
* 尝试插入超出范围或重复键值。
* 权限错误。
* 表不存在。

这些错误通过 MySQL 服务器协议返回给客户端，应用程序需要采取适当的操作。在应用程序没有正确处理（或记录）TiDB 服务器返回的错误的情况下，`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_HOST` 表提供了一种检查错误的有用方法。

由于 `CLIENT_ERRORS_SUMMARY_BY_HOST` 按远程主机汇总错误，因此它可以用于诊断某个应用服务器产生的错误比其他服务器多的情况。可能的场景包括：

* 过时的 MySQL 客户端库。
* 过时的应用程序（可能在部署新版本时遗漏了这台服务器）。
* 用户权限中的 "host" 部分使用不当。
* 网络连接不稳定导致更多超时或断开连接。

可以使用 `FLUSH CLIENT_ERRORS_SUMMARY` 语句重置汇总计数。摘要信息仅在每个 TiDB 服务器本地保存，并且只保存在内存中。如果 TiDB 服务器重启，摘要信息将会丢失。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_BY_HOST;
```

输出结果如下：

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

字段说明：

* `HOST`：客户端的远程主机。
* `ERROR_NUMBER`：返回的 MySQL 兼容错误号。
* `ERROR_MESSAGE`：与错误号匹配的错误消息（以预处理语句形式）。
* `ERROR_COUNT`：此错误返回给客户端主机的次数。
* `WARNING_COUNT`：此警告返回给客户端主机的次数。
* `FIRST_SEEN`：从客户端主机首次看到此错误（或警告）的时间。
* `LAST_SEEN`：从客户端主机最近一次看到此错误（或警告）的时间。

以下示例显示了客户端连接到本地 TiDB 服务器时生成的警告。执行 `FLUSH CLIENT_ERRORS_SUMMARY` 后重置摘要：

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
```

输出结果如下：

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

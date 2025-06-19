---
title: CLIENT_ERRORS_SUMMARY_GLOBAL
summary: 了解 `CLIENT_ERRORS_SUMMARY_GLOBAL` INFORMATION_SCHEMA 表。
---

# CLIENT_ERRORS_SUMMARY_GLOBAL

`CLIENT_ERRORS_SUMMARY_GLOBAL` 表提供了连接到 TiDB 服务器的客户端收到的所有 SQL 错误和警告的全局汇总。这些包括：

* 格式错误的 SQL 语句。
* 除零错误。
* 尝试插入超出范围或重复的键值。
* 权限错误。
* 表不存在。

客户端错误通过 MySQL 服务器协议返回给客户端，应用程序需要采取适当的操作。`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL` 表提供了一个高层次的概览，在应用程序没有正确处理（或记录）TiDB 服务器返回的错误的情况下特别有用。

可以使用 `FLUSH CLIENT_ERRORS_SUMMARY` 语句重置汇总计数。该汇总信息对每个 TiDB 服务器都是本地的，并且仅保存在内存中。如果 TiDB 服务器重启，汇总信息将会丢失。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_GLOBAL;
```

输出如下：

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

字段说明：

* `ERROR_NUMBER`：返回的 MySQL 兼容错误号。
* `ERROR_MESSAGE`：与错误号匹配的错误消息（以预处理语句形式）。
* `ERROR_COUNT`：此错误返回的次数。
* `WARNING_COUNT`：此警告返回的次数。
* `FIRST_SEEN`：首次发送此错误（或警告）的时间。
* `LAST_SEEN`：最近一次发送此错误（或警告）的时间。

以下示例展示了连接到本地 TiDB 服务器时生成的警告。执行 `FLUSH CLIENT_ERRORS_SUMMARY` 后重置汇总信息：

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
```

输出如下：

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

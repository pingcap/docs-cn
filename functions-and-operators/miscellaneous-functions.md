---
title: 其他函数
summary: TiDB 支持使用 MySQL 8.0 中提供的大部分其他函数。
---

# 其他函数

TiDB 支持使用 MySQL 8.0 中提供的大部分[其他函数](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html)。

## 支持的函数

| 函数名 | 功能描述  |
|:------------|:-------------------------------------------------------------------------------|
| [`ANY_VALUE()`](#any_value)              | 在 `ONLY_FULL_GROUP_BY` 模式下，防止带有 `GROUP BY` 的语句报错      |
| [`BIN_TO_UUID()`](#bin_to_uuid)          | 将通用唯一识别码 (UUID) 从二进制格式转换为文本格式    |
| [`DEFAULT()`](#default)                  | 返回表的某一列的默认值      |
| [`GROUPING()`](#grouping)                | `GROUP BY` 操作的修饰符                |
| [`INET_ATON()`](#inet_aton)              | 将 IP 地址转换为数值         |
| [`INET_NTOA()`](#inet_ntoa)              | 将数值转换为 IP 地址        |
| [`INET6_ATON()`](#inet6_aton)            | 将 IPv6 地址转换为数值       |
| [`INET6_NTOA()`](#inet6_ntoa)            | 将数值转换为 IPv6 地址      |
| [`IS_IPV4()`](#is_ipv4)                  | 判断参数是否为 IPv4 地址               |
| [`IS_IPV4_COMPAT()`](#is_ipv4_compat)    | 判断参数是否为兼容 IPv4 的地址    |
| [`IS_IPV4_MAPPED()`](#is_ipv4_mapped)    | 判断参数是否为 IPv4 映射的地址        |
| [`IS_IPV6()`](#is_ipv6)                  | 判断参数是否为 IPv6 地址               |
| [`IS_UUID()`](#is_uuid)                  | 判断参数是否为 UUID                       |
| [`NAME_CONST()`](#name_const)            | 可以用于重命名列名               |
| [`SLEEP()`](#sleep)                      | 让语句暂停执行几秒时间       |
| [`UUID()`](#uuid)                        | 返回一个通用唯一识别码 (UUID)       |
| [`UUID_TO_BIN()`](#uuid_to_bin)          | 将 UUID 从文本格式转换为二进制格式    |
| [`VALUES()`](#values)                    | 定义 `INSERT` 语句使用的值    |

### ANY_VALUE()

`ANY_VALUE()` 函数可以从一组值中返回其中任意一个值。通常，该函数用于需要在 `SELECT` 语句中包含非聚合列以及 `GROUP BY` 子句的场景中。

```sql
CREATE TABLE fruits (id INT PRIMARY KEY, name VARCHAR(255));
Query OK, 0 rows affected (0.14 sec)

INSERT INTO fruits VALUES (1,'apple'),(2,'apple'),(3,'pear'),(4,'banana'),(5, 'pineapple');
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

SELECT id,name FROM fruits GROUP BY name;
ERROR 1055 (42000): Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'test.fruits.id' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by

SELECT ANY_VALUE(id),GROUP_CONCAT(id),name FROM fruits GROUP BY name;
+---------------+------------------+-----------+
| ANY_VALUE(id) | GROUP_CONCAT(id) | name      |
+---------------+------------------+-----------+
|             1 | 1,2              | apple     |
|             3 | 3                | pear      |
|             4 | 4                | banana    |
|             5 | 5                | pineapple |
+---------------+------------------+-----------+
4 rows in set (0.00 sec)
```

在以上示例中，执行了第一条 `SELECT` 语句后，TiDB 返回了一条错误，这是因为 `id` 列是非聚合列且未包含在 `GROUP BY` 子句中。为了解决此问题，第二个 `SELECT` 查询使用了 `ANY_VALUE()` 从每个组中获取任意值，并使用了 `GROUP_CONCAT()` 将每个组中 `id` 列的所有值拼接成一个字符串。通过这种方法，你可以获取每个组中的一个值以及该组的所有值，而无需改变非聚合列的 SQL 模式。

### BIN_TO_UUID()

`BIN_TO_UUID()` 和 `UUID_TO_BIN()` 用于在文本格式 UUID 和二进制格式 UUID 之间进行转换。这两个函数都可以接受两个参数。

- 第一个参数用于指定要转换的值。
- 第二个参数（可选）用于控制二进制格式中字段的排序。

```sql
SET @a := UUID();
Query OK, 0 rows affected (0.00 sec)

SELECT @a;
+--------------------------------------+
| @a                                   |
+--------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56 |
+--------------------------------------+
1 row in set (0.00 sec)

SELECT UUID_TO_BIN(@a);
+------------------------------------+
| UUID_TO_BIN(@a)                    |
+------------------------------------+
| 0x9A17B457EB6D11EEBACF5405DB7AAD56 |
+------------------------------------+
1 row in set (0.00 sec)

SELECT BIN_TO_UUID(0x9A17B457EB6D11EEBACF5405DB7AAD56);
+-------------------------------------------------+
| BIN_TO_UUID(0x9A17B457EB6D11EEBACF5405DB7AAD56) |
+-------------------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56            |
+-------------------------------------------------+
1 row in set (0.00 sec)

SELECT UUID_TO_BIN(@a, 1);
+----------------------------------------+
| UUID_TO_BIN(@a, 1)                     |
+----------------------------------------+
| 0x11EEEB6D9A17B457BACF5405DB7AAD56     |
+----------------------------------------+
1 row in set (0.00 sec)

SELECT BIN_TO_UUID(0x11EEEB6D9A17B457BACF5405DB7AAD56, 1);
+----------------------------------------------------+
| BIN_TO_UUID(0x11EEEB6D9A17B457BACF5405DB7AAD56, 1) |
+----------------------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56               |
+----------------------------------------------------+
1 row in set (0.00 sec)
```

另请参阅 [UUID()](#uuid) 和 [UUID 最佳实践](/best-practices/uuid.md)。

### DEFAULT()

`DEFAULT()` 函数用于获取列的默认值。

```sql
CREATE TABLE t1 (id INT PRIMARY KEY, c1 INT DEFAULT 5);
Query OK, 0 rows affected (0.15 sec)

INSERT INTO t1 VALUES (1, 1);
Query OK, 1 row affected (0.01 sec)

UPDATE t1 SET c1=DEFAULT(c1)+3;
Query OK, 1 row affected (0.02 sec)
Rows matched: 1  Changed: 1  Warnings: 0

TABLE t1;
+----+------+
| id | c1   |
+----+------+
|  1 |    8 |
+----+------+
1 row in set (0.00 sec)
```

在以上示例中，`UPDATE` 语句将 `c1` 列的值设置为列的默认值（即 `5`）加 `3`，从而得到一个新值 `8`。

### GROUPING()

参见 [`GROUP BY` 修饰符](/functions-and-operators/group-by-modifier.md)。

### INET_ATON()

`INET_ATON()` 函数用于将点分十进制形式表示的 IPv4 地址转换为可有效存储的二进制形式。

```sql
SELECT INET_ATON('127.0.0.1');
```

```
+------------------------+
| INET_ATON('127.0.0.1') |
+------------------------+
|             2130706433 |
+------------------------+
1 row in set (0.00 sec)
```

### INET_NTOA()

`INET_NTOA()` 函数用于将二进制 IPv4 地址转换为点分十进制表示形式。

```sql
SELECT INET_NTOA(2130706433);
```

```
+-----------------------+
| INET_NTOA(2130706433) |
+-----------------------+
| 127.0.0.1             |
+-----------------------+
1 row in set (0.00 sec)
```

### INET6_ATON()

`INET6_ATON()` 函数的功能类似于 [`INET_ATON()`](#inet_aton)，但 `INET6_ATON()` 还可以处理 IPv6 地址。

```sql
SELECT INET6_ATON('::1');
```

```
+--------------------------------------+
| INET6_ATON('::1')                    |
+--------------------------------------+
| 0x00000000000000000000000000000001   |
+--------------------------------------+
1 row in set (0.00 sec)
```

### INET6_NTOA()

`INET6_NTOA()` 函数的功能类似于 [`INET_NTOA()`](#inet_ntoa)，但 `INET6_NTOA()` 还可以处理 IPv6 地址。

```sql
SELECT INET6_NTOA(0x00000000000000000000000000000001);
```

```
+------------------------------------------------+
| INET6_NTOA(0x00000000000000000000000000000001) |
+------------------------------------------------+
| ::1                                            |
+------------------------------------------------+
1 row in set (0.00 sec)
```

### IS_IPV4()

`IS_IPV4()` 函数用于判断输入的参数是否为 IPv4 地址。

```sql
SELECT IS_IPV4('127.0.0.1');
```

```
+----------------------+
| IS_IPV4('127.0.0.1') |
+----------------------+
|                    1 |
+----------------------+
1 row in set (0.00 sec)
```

```sql
SELECT IS_IPV4('300.0.0.1');
```

```
+----------------------+
| IS_IPV4('300.0.0.1') |
+----------------------+
|                    0 |
+----------------------+
1 row in set (0.00 sec)
```

### IS_IPV4_COMPAT()

`IS_IPV4_COMPAT()` 函数用于判断输入的参数是否为兼容 IPv4 的地址。

```sql
SELECT IS_IPV4_COMPAT(INET6_ATON('::127.0.0.1'));
```

```
+-------------------------------------------+
| IS_IPV4_COMPAT(INET6_ATON('::127.0.0.1')) |
+-------------------------------------------+
|                                         1 |
+-------------------------------------------+
1 row in set (0.00 sec)
```

### IS_IPV4_MAPPED()

`IS_IPV4_MAPPED()` 函数用于判断输入的参数是否为 IPv4 映射的地址。

```sql
SELECT IS_IPV4_MAPPED(INET6_ATON('::ffff:127.0.0.1'));
```

```
+------------------------------------------------+
| IS_IPV4_MAPPED(INET6_ATON('::ffff:127.0.0.1')) |
+------------------------------------------------+
|                                              1 |
+------------------------------------------------+
1 row in set (0.00 sec)
```

### IS_IPV6()

`IS_IPV6()` 函数用于判断输入的参数是否为 IPv6 地址。

```sql
SELECT IS_IPV6('::1');
```

```
+----------------+
| IS_IPV6('::1') |
+----------------+
|              1 |
+----------------+
1 row in set (0.00 sec)
```

### IS_UUID()

`IS_UUID()` 函数用于判断输入的参数是否为 [UUID](/best-practices/uuid.md)。

```sql
SELECT IS_UUID('eb48c08c-eb71-11ee-bacf-5405db7aad56');
```

```
+-------------------------------------------------+
| IS_UUID('eb48c08c-eb71-11ee-bacf-5405db7aad56') |
+-------------------------------------------------+
|                                               1 |
+-------------------------------------------------+
1 row in set (0.00 sec)
```

### NAME_CONST()

函数 `NAME_CONST()` 用于命名列。建议使用列别名功能代替。

```sql
SELECT NAME_CONST('column name', 'value') UNION ALL SELECT 'another value';
```

```
+---------------+
| column name   |
+---------------+
| another value |
| value         |
+---------------+
2 rows in set (0.00 sec)
```

上面这条语句使用了 `NAME_CONST()`，下面这条语句使用了列别名的方式（推荐）。

```sql
SELECT 'value' AS 'column name' UNION ALL SELECT 'another value';
```

```
+---------------+
| column name   |
+---------------+
| value         |
| another value |
+---------------+
2 rows in set (0.00 sec)
```

### SLEEP()

`SLEEP()` 函数用于将查询暂停执行几秒。

```sql
SELECT SLEEP(1.5);
```

```
+------------+
| SLEEP(1.5) |
+------------+
|          0 |
+------------+
1 row in set (1.50 sec)
```

### UUID()

`UUID()` 函数用于返回通用唯一标识符 (UUID) version 1。UUID 的定义可参考 [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122)。

```sql
SELECT UUID();
```

```
+--------------------------------------+
| UUID()                               |
+--------------------------------------+
| cb4d5ae6-eb6b-11ee-bacf-5405db7aad56 |
+--------------------------------------+
1 row in set (0.00 sec)
```

另请参阅 [UUID 最佳实践](/best-practices/uuid.md)。

### UUID_TO_BIN

参见 [BIN_TO_UUID()](#bin_to_uuid)。

### VALUES()

`VALUES(col_name)` 函数用于在 [`INSERT`](/sql-statements/sql-statement-insert.md) 语句的 `ON DUPLICATE KEY UPDATE` 子句中引用特定列的值。

```sql
CREATE TABLE t1 (id INT PRIMARY KEY, c1 INT);
Query OK, 0 rows affected (0.17 sec)

INSERT INTO t1 VALUES (1,51),(2,52),(3,53),(4,54),(5,55);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

INSERT INTO t1 VALUES(2,22),(4,44) ON DUPLICATE KEY UPDATE c1=VALUES(id)+100;
Query OK, 4 rows affected (0.01 sec)
Records: 2  Duplicates: 2  Warnings: 0

TABLE t1;
+----+------+
| id | c1   |
+----+------+
|  1 |   51 |
|  2 |  102 |
|  3 |   53 |
|  4 |  104 |
|  5 |   55 |
+----+------+
5 rows in set (0.00 sec)
```

## 不支持的函数

| 函数名 | 功能描述  |
|:------|:-----------|
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short)  | 基于特定假设提供唯一的 UUID，目前这些假设在 TiDB 中不存在，详见 [TiDB #4620](https://github.com/pingcap/tidb/issues/4620) |

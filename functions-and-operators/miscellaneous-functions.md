---
title: 其他函数
summary: 了解 TiDB 中的其他函数。
---

# 其他函数

TiDB 支持 MySQL 8.0 中提供的大多数[其他函数](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html)。

## 支持的函数

| 名称 | 描述  |
|:------------|:-----------------------------------------------------------------------------------------------|
| [`ANY_VALUE()`](#any_value)              | 抑制 `ONLY_FULL_GROUP_BY` 值拒绝     |
| [`BIN_TO_UUID()`](#bin_to_uuid)          | 将 UUID 从二进制格式转换为文本格式    |
| [`DEFAULT()`](#default)                  | 返回表列的默认值      |
| [`GROUPING()`](#grouping)                | `GROUP BY` 操作的修饰符                |
| [`INET_ATON()`](#inet_aton)              | 返回 IP 地址的数值         |
| [`INET_NTOA()`](#inet_ntoa)              | 从数值返回 IP 地址        |
| [`INET6_ATON()`](#inet6_aton)            | 返回 IPv6 地址的数值       |
| [`INET6_NTOA()`](#inet6_ntoa)            | 从数值返回 IPv6 地址      |
| [`IS_IPV4()`](#is_ipv4)                  | 判断参数是否为 IPv4 地址               |
| [`IS_IPV4_COMPAT()`](#is_ipv4_compat)    | 判断参数是否为 IPv4 兼容地址    |
| [`IS_IPV4_MAPPED()`](#is_ipv4_mapped)    | 判断参数是否为 IPv4 映射地址        |
| [`IS_IPV6()`](#is_ipv6)                  | 判断参数是否为 IPv6 地址               |
| [`IS_UUID()`](#is_uuid)                  | 判断参数是否为 UUID                       |
| [`NAME_CONST()`](#name_const)            | 可用于重命名列名               |
| [`SLEEP()`](#sleep)                      | 休眠指定的秒数。注意，对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群，`SLEEP()` 函数有一个限制，即最大休眠时间只能支持 300 秒。       |
| [`UUID()`](#uuid)                        | 返回通用唯一标识符 (UUID)       |
| [`UUID_TO_BIN()`](#uuid_to_bin)          | 将 UUID 从文本格式转换为二进制格式    |
| [`VALUES()`](#values)                    | 定义在 INSERT 期间要使用的值    |

### ANY_VALUE()

`ANY_VALUE()` 函数从一组值中返回任意一个值。通常，它用在需要在 `SELECT` 语句中包含非聚合列和 `GROUP BY` 子句的场景中。

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

在上述示例中，第一个 `SELECT` 语句返回错误，因为 `id` 列是非聚合的且未包含在 `GROUP BY` 子句中。为解决此问题，第二个 `SELECT` 查询使用 `ANY_VALUE()` 从每个组中获取任意值，并使用 `GROUP_CONCAT()` 将每个组内 `id` 列的所有值连接成单个字符串。这种方法使您能够在不更改非聚合列的 SQL 模式的情况下，获取每个组的一个值和该组的所有值。

### BIN_TO_UUID()

`BIN_TO_UUID()` 和 `UUID_TO_BIN()` 可用于在文本格式 UUID 和二进制格式之间进行转换。这两个函数都接受两个参数。

- 第一个参数指定要转换的值。
- 第二个参数（可选）控制二进制格式中字段的排序。

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

在上述示例中，`UPDATE` 语句将 `c1` 列的值设置为该列的默认值（即 `5`）加 `3`，得到新值 `8`。

### GROUPING()

参见 [`GROUP BY` 修饰符](/functions-and-operators/group-by-modifier.md)。

### INET_ATON()

`INET_ATON()` 函数将点分四段表示法的 IPv4 地址转换为可以高效存储的二进制版本。

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

`INET_NTOA()` 函数将二进制 IPv4 地址转换为点分四段表示法。

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

`INET6_ATON()` 函数类似于 [`INET_ATON()`](#inet_aton)，但 `INET6_ATON()` 也可以处理 IPv6 地址。

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

`INET6_NTOA()` 函数类似于 [`INET_NTOA()`](#inet_ntoa)，但 `INET6_NTOA()` 也可以处理 IPv6 地址。

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

`IS_IPV4()` 函数测试给定参数是否为 IPv4 地址。

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

`IS_IPV4_COMPAT()` 函数测试给定参数是否为 IPv4 兼容地址。

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

`IS_IPV4_MAPPED()` 函数测试给定参数是否为 IPv4 映射地址。

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

`IS_IPV6()` 函数测试给定参数是否为 IPv6 地址。

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

`IS_UUID()` 函数测试给定参数是否为 [UUID](/best-practices/uuid.md)。

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

`NAME_CONST()` 函数用于命名列。建议使用列别名代替。

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

上述语句使用 `NAME_CONST()`，而下面的语句使用推荐的列别名方式。

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

`SLEEP()` 函数用于暂停查询执行指定的秒数。

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

`UUID()` 函数返回一个符合 [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122) 定义的版本 1 通用唯一标识符 (UUID)。

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

| 名称 | 描述  |
|:------------|:-----------------------------------------------------------------------------------------------|
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short)            | 提供在 TiDB 中不存在的某些假设条件下唯一的 UUID [TiDB #4620](https://github.com/pingcap/tidb/issues/4620) |

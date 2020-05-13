---
title: 字符集和排序规则
category: reference
aliases: ['/docs-cn/dev/reference/sql/character-set/']
---

# 字符集和排序规则

字符集 (character set) 是符号与编码的集合。排序规则 (collation) 是在字符集中比较字符的规则。

目前 TiDB 支持以下字符集：

{{< copyable "sql" >}}

```sql
SHOW CHARACTER SET;
```

```sql
+---------|---------------|-------------------|--------+
| Charset | Description   | Default collation | Maxlen |
+---------|---------------|-------------------|--------+
| utf8    | UTF-8 Unicode | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode | utf8mb4_bin       |      4 |
| ascii   | US ASCII      | ascii_bin         |      1 |
| latin1  | Latin1        | latin1_bin        |      1 |
| binary  | binary        | binary            |      1 |
+---------|---------------|-------------------|--------+
5 rows in set (0.00 sec)
```

> **注意：**
>
> 每个字符集可能对应多个排序规则，但与之对应的**默认排序规则**有且仅有一个。

利用以下的语句可以查看字符集对应的排序规则（以下是[新的排序规则框架](#新框架下的排序规则支持)）下的结果：

{{< copyable "sql" >}}

```sql
SHOW COLLATION WHERE Charset = 'utf8mb4';
```

```sql
+--------------------+---------+------+---------+----------+---------+
| Collation          | Charset | Id   | Default | Compiled | Sortlen |
+--------------------+---------+------+---------+----------+---------+
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
2 rows in set (0.00 sec)
```

## 集群的字符集和排序规则

暂不支持

## 数据库的字符集和排序规则

每个数据库都有相应的字符集和排序规则。数据库的字符集和排序规则可以通过以下语句来设置：

```sql
CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

ALTER DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]
```

在这里 `DATABASE` 可以跟 `SCHEMA` 互换使用。

不同的数据库之间可以使用不一样的字符集和排序规则。

通过系统变量 `character_set_database` 和 `collation_database` 可以查看到当前数据库的字符集以及排序规则：

{{< copyable "sql" >}}

```sql
create schema test1 character set utf8mb4 COLLATE uft8mb4_general_ci;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
use test1;
```

```sql
Database changed
```

{{< copyable "sql" >}}

```sql
SELECT @@character_set_database, @@collation_database;
```

```sql
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| utf8mb4                  | uft8mb4_general_ci   |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
create schema test2 character set latin1 COLLATE latin1_bin;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
use test2;
```

```sql
Database changed
```

{{< copyable "sql" >}}

```sql
SELECT @@character_set_database, @@collation_database;
```

```sql
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| latin1                   | latin1_bin           |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

在 INFORMATION_SCHEMA 中也可以查看到这两个值：

{{< copyable "sql" >}}

```sql
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```

## 表的字符集和排序规则

表的字符集和排序规则可以通过以下语句来设置：

```sql
CREATE TABLE tbl_name (column_list)
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]]

ALTER TABLE tbl_name
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]
```

例如：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1(a int) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

如果表的字符集和排序规则没有设置，那么数据库的字符集和排序规则就作为其默认值。

## 列的字符集和排序规则

列的字符集和排序规则的语法如下：

```sql
col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]
```

如果列的字符集和排序规则没有设置，那么表的字符集和排序规则就作为其默认值。

## 字符串的字符集和排序规则

每一个字符串都对应一个字符集和一个排序规则，在使用字符串时指此选项可选，如下：

```sql
[_charset_name]'string' [COLLATE collation_name]
```

示例如下：

{{< copyable "sql" >}}

```sql
SELECT 'string';
SELECT _utf8mb4'string';
SELECT _utf8mb4'string' COLLATE utf8mb4_general_ci;
```

规则如下：

* 规则 1：如果指定了 `CHARACTER SET charset_name` 和 `COLLATE collation_name`，则直接使用 `charset_name`  字符集和 `collation_name` 排序规则。
* 规则 2：如果指定了 `CHARACTER SET charset_name` 且未指定 `COLLATE collation_name`，则使用 `charset_name` 字符集和 `charset_name` 对应的默认排序规则。
* 规则 3：如果 `CHARACTER SET charset_name` 和 `COLLATE collation_name` 都未指定，则使用 `character_set_connection` 和 `collation_connection` 系统变量给出的字符集和排序规则。

## 客户端连接的字符集和排序规则

* 服务器的字符集和排序规则可以通过系统变量 `character_set_server` 和 `collation_server` 获取。
* 数据库的字符集和排序规则可以通过环境变量 `character_set_database` 和 `collation_database` 获取。

对于每一个客户端的连接，也有相应的变量表示字符集和排序规则：`character_set_connection` 和 `collation_connection`。

`character_set_client` 代表客户端的字符集。在返回结果前，服务端会把结果根据 `character_set_results` 转换成对应的字符集，包括结果的元信息等。

可以用以下的语句来影响这些跟客户端相关的字符集变量：

* `SET NAMES 'charset_name' [COLLATE 'collation_name']`

    `SET NAMES` 用来设定客户端会在之后的请求中使用的字符集。`SET NAMES utf8mb4` 表示客户端会在接下来的请求中，都使用 utf8mb4 字符集。服务端也会在之后返回结果的时候使用 utf8mb4 字符集。
    `SET NAMES 'charset_name'` 语句其实等于下面语句的组合：

    {{< copyable "sql" >}}

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE` 是可选的，如果没有提供，将会用 `charset_name` 对应的默认排序规则。

* `SET CHARACTER SET 'charset_name'`

    跟 `SET NAMES` 类似，等价于下面语句的组合：

    {{< copyable "sql" >}}

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET collation_connection = @@collation_database;
    ```

## 集群、服务器、数据库、表、列、字符串的字符集和排序规则的优先级

优先级从高到低排列顺序为：

字符串 > 列 > 表 > 数据库 > 服务器 > 集群

## 字符集和排序规则的通用选择规则

* 规则 1：如果指定了 `CHARACTER SET charset_name` 和 `COLLATE collation_name`，则直接使用 `charset_name` 字符集和 `collation_name` 排序规则。
* 规则 2：如果指定了 `CHARACTER SET charset_name` 且未指定 `COLLATE collation_name`，则使用 `charset_name` 字符集和 `charset_name` 对应的默认排序规则。
* 规则 3：如果 `CHARACTER SET charset_name` 和 `COLLATE collation_name` 都未指定，则使用更高优先级的字符集和排序规则。

## 字符合法性检查

当指定的字符集为 utf8 或 utf8mb4 时，TiDB 仅支持合法的 utf8 字符。对于不合法的字符，会报错：`incorrect utf8 value`。该字符合法性检查与 MySQL 8.0 兼容，与 MySQL 5.7 及以下版本不兼容。

如果不希望报错，可以通过 `set @@tidb_skip_utf8_check=1;` 跳过字符检查。

## 排序规则支持

排序规则的语法支持和语义支持受到配置项 [`new_collations_enabled_on_first_bootstrap`](/reference/configuration/tidb-server/configuration-file.md#new_collations_enabled_on_first_bootstrap) 的影响。这里语法支持和语义支持有所区别。语法支持是指 TiDB 能够解析和设置排序规则；而语义支持是指 TiDB 能够在比较字符串时正确地使用排序规则。

在 4.0 版本之前，TiDB 只提供了旧的排序规则框架，能够在语法上支持的绝大部分 MySQL 排序规则，但语义上所有的排序规则都当成二进制排序规则。

4.0 版本中，TiDB 增加了新的排序规则框架用于在语义上支持不同的排序规则，保证字符串比较时严格遵循对应的排序规则，详情请见下文。

### 旧框架下的排序规则支持

在 4.0 版本之前，TiDB 中可以指定大部分 MySQL 中的排序规则，并把这些排序规则按照默认排序规则处理，即以编码字节序为字符定序。和 MySQL 不同的是，TiDB 在比较字符前按照排序规则的 PADDING 属性将字符末尾的空格删除，因此会造成以下的行为区别：

{{< copyable "sql" >}}

```sql
create table t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci primary key);
Query OK, 0 rows affected
insert into t values ('A');
Query OK, 1 row affected
insert into t values ('a');
Query OK, 1 row affected # MySQL 中，由于 utf8mb4_general_ci 大小写不敏感，报错 Duplicate entry 'a'。
insert into t1 values ('a ');
Query OK, 1 row affected # MySQL 中，由于补齐空格比较，报错 Duplicate entry 'a '。
```

### 新框架下的排序规则支持

TiDB 4.0 新增了完整的排序规则支持框架，从语义上支持了排序规则，并新增了配置开关 `new_collations_enabled_on_first_bootstrap`，在集群初次初始化时决定是否启用新排序规则框架。在该配置开关打开之后初始化集群，可以通过 `mysql`.`tidb` 表中的 `new_collation_enabled` 变量确认是否启用新排序规则框架：

{{< copyable "sql" >}}

```sql
select VARIABLE_VALUE from mysql.tidb where VARIABLE_NAME='new_collation_enabled';
```

```sql
+----------------+
| VARIABLE_VALUE |
+----------------+
| True           |
+----------------+
1 row in set (0.00 sec)
```

在新的排序规则框架下，TiDB 能够支持 `utf8_general_ci` 和 `utf8mb4_general_ci` 这两种排序规则，与 MySQL 兼容。

使用 `utf8_general_ci` 或者 `utf8mb4_general_ci` 时，字符串之间的比较是大小写不敏感 (case-insensitive) 和口音不敏感 (accent-insensitive) 的。同时，TiDB 还修正了排序规则的 `PADDING` 行为：

{{< copyable "sql" >}}

```sql
create table t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci primary key);
Query OK, 0 rows affected (0.00 sec)
insert into t values ('A');
Query OK, 1 row affected (0.00 sec)
insert into t values ('a');
ERROR 1062 (23000): Duplicate entry 'a' for key 'PRIMARY'
insert into t values ('a ');
ERROR 1062 (23000): Duplicate entry 'a ' for key 'PRIMARY'
```

> **注意：**
>
> TiDB 中 padding 的实现方式与 MySQL 的不同。在 MySQL 中，padding 是通过补齐空格实现的。而在 TiDB 中 padding 是通过裁剪掉末尾的空格来实现的。两种做法在绝大多数情况下是一致的，唯一的例外是字符串尾部包含小于空格 (0x20) 的字符时，例如 `'a' < 'a\t'` 在 TiDB 中的结果为 `1`，而在 MySQL 中，其等价于 `'a ' < 'a\t'`，结果为 `0`。

## 表达式中排序规则的 Coercibility 值

如果一个表达式涉及多个不同排序规则的子表达式时，需要对计算时用的排序规则进行推断，规则如下：

+ 显式 `COLLATE` 子句的 coercibility 值为 `0`。
+ 如果两个字符串的排序规则不兼容，这两个字符串 `concat` 结果的 coercibility 值为 `1`。目前所实现的排序规则都是互相兼容的。
+ 列的排序规则的 coercibility 值为 `2`。
+ 系统常量（`USER()` 或者 `VERSION()` 返回的字符串）的 coercibility 值为 `3`。
+ 常量的 coercibility 值为 `4`。
+ 数字或者中间变量的 coercibility 值为 `5`。
+ `NULL` 或者由 `NULL` 派生出的表达式的 coercibility 值为 `6`。

在推断排序规则时，TiDB 优先使用 coercibility 值较低的表达式的排序规则（与 MySQL 一致）。如果 coercibility 值相同，则按以下优先级确定排序规则：

binary > utf8mb4_bin > utf8mb4_general_ci > utf8_bin > utf8_general_ci > latin1_bin > ascii_bin

如果两个子表达式的排序规则不相同，而且表达式的 coercibility 值都为 `0` 时，TiDB 无法推断排序规则并报错。

## `COLLATE` 子句

TiDB 支持使用 `COLLATE` 子句来指定一个表达式的排序规则，该表达式的 coercibility 值为 `0`，具有最高的优先级。示例如下：

{{< copyable "sql" >}}

```sql
select 'a' = 'A' collate utf8mb4_general_ci;
```

```sql
+--------------------------------------+
| 'a' = 'A' collate utf8mb4_general_ci |
+--------------------------------------+
|                                    1 |
+--------------------------------------+
1 row in set (0.00 sec)
```

更多细节，参考 [Connection Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-connection.html)。

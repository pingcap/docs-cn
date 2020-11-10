---
title: 字符集支持
aliases: ['/docs-cn/v3.1/character-set-and-collation/','/docs-cn/v3.1/reference/sql/character-set/']
---

# 字符集支持

名词解释，下面的阐述中会交错使用中文或者英文，请互相对照：

* Character Set：字符集
* Collation：排序规则

目前 `TiDB` 支持以下字符集：

{{< copyable "sql" >}}

```sql
SHOW CHARACTER SET;
```

```
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
> - 在 `TiDB` 中 `utf8` 被当做成了 `utf8mb4` 来处理。
> - 每种字符集都对应一个默认的 Collation，当前有且仅有一个。

对于字符集来说，至少会有一个 Collation（排序规则）与之对应。而大部分字符集实际上会有多个 Collation。利用以下的语句可以查看：

{{< copyable "sql" >}}

```sql
SHOW COLLATION WHERE Charset = 'latin1';
```

```
+-------------------|---------|------|---------|----------|---------+
| Collation         | Charset | Id   | Default | Compiled | Sortlen |
+-------------------|---------|------|---------|----------|---------+
| latin1_german1_ci | latin1  |    5 |         | Yes      |       1 |
| latin1_swedish_ci | latin1  |    8 | Yes     | Yes      |       1 |
| latin1_danish_ci  | latin1  |   15 |         | Yes      |       1 |
| latin1_german2_ci | latin1  |   31 |         | Yes      |       1 |
| latin1_bin        | latin1  |   47 |         | Yes      |       1 |
| latin1_general_ci | latin1  |   48 |         | Yes      |       1 |
| latin1_general_cs | latin1  |   49 |         | Yes      |       1 |
| latin1_spanish_ci | latin1  |   94 |         | Yes      |       1 |
+-------------------|---------|------|---------|----------|---------+
8 rows in set (0.00 sec)
```

`latin1` Collation（排序规则）分别有以下含义：

| Collation         | 含义                              |
|:------------------|:----------------------------------|
| latin1_bin        | latin1 编码的二进制表示           |
| latin1_danish_ci  | 丹麦语/挪威语，不区分大小写       |
| latin1_general_ci | 多种语言的 (西欧)，不区分大小写   |
| latin1_general_cs | 多种语言的 (ISO 西欧)，区分大小写 |
| latin1_german1_ci | 德国 DIN-1 (字典序)，不区分大小写 |
| latin1_german2_ci | 德国 DIN-2，不区分大小写          |
| latin1_spanish_ci | 现代西班牙语，不区分大小写        |
| latin1_swedish_ci | 瑞典语/芬兰语，不区分大小写       |

每一个字符集，都有一个默认的 Collation，例如 `utf8` 的默认 Collation 就为 `utf8_bin`。

> **警告：**
>
> TiDB 会错误地将 `latin1` 视为 `utf8` 的子集。当用户存储不同于 `latin1` 和 `utf8` 编码的字符时，可能会导致意外情况出现。因此强烈建议使用 `utf8mb4` 字符集。详情参阅 [TiDB #18955](https://github.com/pingcap/tidb/issues/18955)。

> **注意：**
>
> `TiDB` 目前的 Collation 只支持区分大小写的比较排序规则。

## Collation 命名规则

`TiDB` 的 Collation 遵循着如下的命名规则：

* Collation 的前缀是它相应的字符集，通常之后会跟着一个或者更多的后缀来表名其他的排序规则， 例如：utf8_general_ci 和 lation1_swedish_ci 是 utf8
 和 latin1 字符集的 Collation。但是 binary 字符集只有一个 Collation，就是 binary。
* 一个语言对应的 Collation 会包含语言的名字，例如 utf8_turkish_ci 和 utf8_hungarian_ci 是依据 Turkish(土耳其语) 和 Hungarian(匈牙利语) 的排序规则来排序。
* Collation 的后缀表示了 Collation 是否区分大小写和是否区分口音。下面的表展示了这些特性：

| 后缀 | 含义                             |
|:-----|:---------------------------------|
| \_ai | 口音不敏感（Accent insensitive） |
| \_as | 口音敏感 （Accent sensitive）  |
| \_ci | 大小写不敏感                     |
| \_cs | 大小写敏感                       |

> **注意：**
>
> 目前为止 TiDB 只支持部分以上提到的 Collation。

## 集群 Character Set 和 Collation

暂不支持

## 数据库 Character Set 和 Collation

每个数据库都有相应的 Character Set 和 Collation，数据库的 Character Set 和 Collation 可以通过以下语句来设置：

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
<<<<<<< HEAD
create schema test1 character set utf8 COLLATE uft8_general_ci;
=======
CREATE SCHEMA test1 CHARACTER SET utf8mb4 COLLATE uft8mb4_general_ci;
>>>>>>> 43758a91... Capitalize sql keywords in several files (#4862)
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
USE test1;
```

```
Database changed
```

{{< copyable "sql" >}}

```sql
SELECT @@character_set_database, @@collation_database;
```

```
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| utf8                     | uft8_general_ci      |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
<<<<<<< HEAD
create schema test2 character set latin1 COLLATE latin1_general_ci;
=======
CREATE SCHEMA test2 CHARACTER SET latin1 COLLATE latin1_bin;
>>>>>>> 43758a91... Capitalize sql keywords in several files (#4862)
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
USE test2;
```

```
Database changed
```

{{< copyable "sql" >}}

```sql
SELECT @@character_set_database, @@collation_database;
```

```
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| latin1                   | latin1_general_ci    |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

在 INFORMATION_SCHEMA 中也可以查看到这两个值：

{{< copyable "sql" >}}

```sql
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```

## 表的 Character Set 和 Collation

表的 Character Set 和 Collation 可以通过以下语句来设置：

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
CREATE TABLE t1(a int) CHARACTER SET utf8 COLLATE utf8_general_ci;
```

```
Query OK, 0 rows affected (0.08 sec)
```

如果表的字符集和排序规则没有设置，那么数据库的字符集和排序规则就作为其默认值。

## 列的 Character Set 和 Collation

列的 Character Set 和 Collation 的语法如下：

```sql
col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]
```

如果列的字符集和排序规则没有设置，那么表的字符集和排序规则就作为其默认值。

## 字符串 Character Sets 和 Collation

每一字符串字符文字有一个字符集和一个比较排序规则，在使用字符串时指，此选项可选，如下：

```sql
[_charset_name]'string' [COLLATE collation_name]
```

示例，如下：

{{< copyable "sql" >}}

```sql
SELECT 'string';
SELECT _latin1'string';
SELECT _latin1'string' COLLATE latin1_danish_ci;
```

规则，如下：

* 规则1： 指定 CHARACTER SET charset_name 和 COLLATE collation_name，则直接使用 CHARACTER SET charset_name 和COLLATE collation_name。
* 规则2:    指定 CHARACTER SET charset_name 且未指定 COLLATE collation_name，则使用 CHARACTER SET charset_name 和 CHARACTER SET charset_name 默认的排序比较规则。
* 规则3:   CHARACTER SET charset_name 和 COLLATE collation_name 都未指定，则使用 character_set_connection 和 collation_connection 系统变量给出的字符集和比较排序规则。

## 客户端连接的 Character Sets 和 Collations

* 服务器的字符集和排序规则可以通过系统变量 `character_set_server` 和 `collation_server` 获取。
* 数据库的字符集和排序规则可以通过环境变量 `character_set_database` 和 `collation_database` 获取。

对于每一个客户端的连接，也有相应的变量表示字符集和排序规则：`character_set_connection` 和 `collation_connection`。

`character_set_client` 代表客户端的字符集。在返回结果前，服务端会把结果根据 `character_set_results` 转换成对应的字符集。包括结果的元信息等。

可以用以下的语句来影响这些跟客户端相关的字符集变量：

* `SET NAMES 'charset_name' [COLLATE 'collation_name']`

<<<<<<< HEAD
`SET NAMES` 用来设定客户端会在之后的请求中使用的字符集。`SET NAMES utf8` 表示客户端会在接下来的请求中，都使用 utf8 字符集。服务端也会在之后返回结果的时候使用 utf8 字符集。
`SET NAMES 'charset_name'` 语句其实等于下面语句的组合：
=======
    `SET NAMES` 用来设定客户端会在之后的请求中使用的字符集。`SET NAMES utf8mb4` 表示客户端会在接下来的请求中，都使用 utf8mb4 字符集。服务端也会在之后返回结果的时候使用 utf8mb4 字符集。
    `SET NAMES 'charset_name'` 语句其实等于下面语句的组合：

    {{< copyable "sql" >}}

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE` 是可选的，如果没有提供，将会用 `charset_name` 对应的默认排序规则设置 `collation_connection`。

* `SET CHARACTER SET 'charset_name'`

    跟 `SET NAMES` 类似，等价于下面语句的组合：

    {{< copyable "sql" >}}

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET charset_connection = @@charset_database;
    SET collation_connection = @@collation_database;
    ```

## 服务器、数据库、表、列、字符串的字符集和排序规则的优先级

优先级从高到低排列顺序为：

字符串 > 列 > 表 > 数据库 > 服务器

## 字符集和排序规则的通用选择规则

* 规则 1：如果指定了 `CHARACTER SET charset_name` 和 `COLLATE collation_name`，则直接使用 `charset_name` 字符集和 `collation_name` 排序规则。
* 规则 2：如果指定了 `CHARACTER SET charset_name` 且未指定 `COLLATE collation_name`，则使用 `charset_name` 字符集和 `charset_name` 对应的默认排序规则。
* 规则 3：如果 `CHARACTER SET charset_name` 和 `COLLATE collation_name` 都未指定，则使用更高优先级的字符集和排序规则。

## 字符合法性检查

当指定的字符集为 utf8 或 utf8mb4 时，TiDB 仅支持合法的 utf8 字符。对于不合法的字符，会报错：`incorrect utf8 value`。该字符合法性检查与 MySQL 8.0 兼容，与 MySQL 5.7 及以下版本不兼容。

如果不希望报错，可以通过 `set @@tidb_skip_utf8_check=1;` 跳过字符检查。

## 排序规则支持

排序规则的语法支持和语义支持受到配置项 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 的影响。这里语法支持和语义支持有所区别。语法支持是指 TiDB 能够解析和设置排序规则；而语义支持是指 TiDB 能够在比较字符串时正确地使用排序规则。

在 4.0 版本之前，TiDB 只提供了旧的排序规则框架，能够在语法上支持的绝大部分 MySQL 排序规则，但语义上所有的排序规则都当成二进制排序规则。

4.0 版本中，TiDB 增加了新的排序规则框架用于在语义上支持不同的排序规则，保证字符串比较时严格遵循对应的排序规则，详情请见下文。

### 旧框架下的排序规则支持

在 4.0 版本之前，TiDB 中可以指定大部分 MySQL 中的排序规则，并把这些排序规则按照默认排序规则处理，即以编码字节序为字符定序。和 MySQL 不同的是，TiDB 在比较字符前按照排序规则的 PADDING 属性将字符末尾的空格删除，因此会造成以下的行为区别：

{{< copyable "sql" >}}

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
Query OK, 0 rows affected
INSERT INTO t VALUES ('A');
Query OK, 1 row affected
INSERT INTO t VALUES ('a');
Query OK, 1 row affected # TiDB 会执行成功，而在 MySQL 中，则由于 utf8mb4_general_ci 大小写不敏感，报错 Duplicate entry 'a'。
INSERT INTO t VALUES ('a ');
Query OK, 1 row affected # TiDB 会执行成功，而在 MySQL 中，则由于补齐空格比较，报错 Duplicate entry 'a '。
```

### 新框架下的排序规则支持

TiDB 4.0 新增了完整的排序规则支持框架，从语义上支持了排序规则，并新增了配置开关 `new_collations_enabled_on_first_bootstrap`，在集群初次初始化时决定是否启用新排序规则框架。在该配置开关打开之后初始化集群，可以通过 `mysql`.`tidb` 表中的 `new_collation_enabled` 变量确认是否启用新排序规则框架：
>>>>>>> 43758a91... Capitalize sql keywords in several files (#4862)

{{< copyable "sql" >}}

```sql
<<<<<<< HEAD
SET character_set_client = charset_name;
SET character_set_results = charset_name;
SET character_set_connection = charset_name;
=======
SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME='new_collation_enabled';
>>>>>>> 43758a91... Capitalize sql keywords in several files (#4862)
```

`COLLATE` 是可选的，如果没有提供，将会用 charset_name 默认的 Collation。

* `SET CHARACTER SET 'charset_name'`

跟 `SET NAMES` 类似，等价于下面语句的组合：

{{< copyable "sql" >}}

```sql
<<<<<<< HEAD
SET character_set_client = charset_name;
SET character_set_results = charset_name;
SET collation_connection = @@collation_database;
=======
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
Query OK, 0 rows affected (0.00 sec)
INSERT INTO t VALUES ('A');
Query OK, 1 row affected (0.00 sec)
INSERT INTO t VALUES ('a');
ERROR 1062 (23000): Duplicate entry 'a' for key 'PRIMARY' # TiDB 兼容了 MySQL 的 case insensitive collation。
INSERT INTO t VALUES ('a ');
ERROR 1062 (23000): Duplicate entry 'a ' for key 'PRIMARY' # TiDB 修正了 `PADDING` 行为，与 MySQL 兼容。
>>>>>>> 43758a91... Capitalize sql keywords in several files (#4862)
```

## 集群，服务器，数据库，表，列，字符串 Character Sets 和 Collation 优化级

字符串 => 列 => 表 => 数据库 => 服务器 => 集群

## Character Sets 和 Collation 通用选择规则

* 规则1： 指定 CHARACTER SET charset_name 和 COLLATE collation_name，则直接使用 CHARACTER SET charset_name 和COLLATE collation_name。
* 规则2:    指定 CHARACTER SET charset_name 且未指定 COLLATE collation_name，则使用 CHARACTER SET charset_name 和 CHARACTER SET charset_name 默认的排序比较规则。
* 规则3:   CHARACTER SET charset_name 和 COLLATE collation_name 都未指定，则使用更高优化级给出的字符集和排序比较规则。

## 字符合法性检查

<<<<<<< HEAD
当指定的字符集为 utf8 或 utf8mb4 时，TiDB 仅支持合法的 utf8 字符。对于不合法的字符，会报错：`incorrect utf8 value`。该字符合法性检查与 MySQL 8.0 兼容，与 MySQL 5.7 及以下版本不兼容。
=======
```sql
SELECT 'a' = _utf8mb4 'A' collate utf8mb4_general_ci;
```
>>>>>>> 43758a91... Capitalize sql keywords in several files (#4862)

如果不希望报错，可以通过 `set @@tidb_skip_utf8_check=1;` 跳过字符检查。

更多细节，参考 [Connection Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-connection.html)。

---
title: 分区表
aliases: ['/docs-cn/dev/partitioned-table/','/docs-cn/dev/reference/sql/partitioning/']
---

# 分区表

本文介绍 TiDB 的分区表。

## 分区类型

本节介绍 TiDB 中的分区类型。当前支持的类型包括 [Range 分区](#range-分区)、[List 分区](#list-分区)、[List COLUMNS 分区](#list-columns-分区) 和 [Hash 分区](#hash-分区)。Range 分区，List 分区和 List COLUMNS 分区可以用于解决业务中大量删除带来的性能问题，支持快速删除分区。Hash 分区则可以用于大量写入场景下的数据打散。

### Range 分区

一个表按 Range 分区是指，对于表的每个分区中包含的所有行，按分区表达式计算的值都落在给定的范围内。Range 必须是连续的，并且不能有重叠，通过使用 `VALUES LESS THAN` 进行定义。

下列场景中，假设你要创建一个人事记录的表：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT NOT NULL,
    store_id INT NOT NULL
);
```

你可以根据需求按各种方式进行 Range 分区。其中一种方式是按 `store_id` 列进行分区：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT NOT NULL,
    store_id INT NOT NULL
)

PARTITION BY RANGE (store_id) (
    PARTITION p0 VALUES LESS THAN (6),
    PARTITION p1 VALUES LESS THAN (11),
    PARTITION p2 VALUES LESS THAN (16),
    PARTITION p3 VALUES LESS THAN (21)
);
```

在这个分区模式中，所有 `store_id` 为 1 到 5 的员工，都存储在分区 `p0` 里面，`store_id` 为 6 到 10 的员工则存储在分区 `p1` 里面。Range 分区要求，分区的定义必须是有序的，按从小到大递增。

新插入一行数据 `(72, 'Tom', 'John', '2015-06-25', NULL, 15)` 将会落到分区 `p2` 里面。但如果你插入一条 `store_id` 大于 20 的记录，则会报错，因为 TiDB 无法知晓应该将它插入到哪个分区。这种情况下，可以在建表时使用最大值：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT NOT NULL,
    store_id INT NOT NULL
)

PARTITION BY RANGE (store_id) (
    PARTITION p0 VALUES LESS THAN (6),
    PARTITION p1 VALUES LESS THAN (11),
    PARTITION p2 VALUES LESS THAN (16),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

`MAXVALUE` 表示一个比所有整数都大的整数。现在，所有 `store_id` 列大于等于 16 的记录都会存储在 `p3` 分区中。

你也可以按员工的职位编号进行分区，也就是使用 `job_code` 列的值进行分区。假设两位数字编号是用于普通员工，三位数字编号是用于办公室以及客户支持，四位数字编号是管理层职位，那么你可以这样建表：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT NOT NULL,
    store_id INT NOT NULL
)

PARTITION BY RANGE (job_code) (
    PARTITION p0 VALUES LESS THAN (100),
    PARTITION p1 VALUES LESS THAN (1000),
    PARTITION p2 VALUES LESS THAN (10000)
);
```

在这个例子中，所有普通员工存储在 `p0` 分区，办公室以及支持人员在 `p1` 分区，管理者在 `p2` 分区。

除了可以按 `store_id` 切分，你还可以按日期切分。例如，假设按员工离职的年份进行分区：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY RANGE ( YEAR(separated) ) (
    PARTITION p0 VALUES LESS THAN (1991),
    PARTITION p1 VALUES LESS THAN (1996),
    PARTITION p2 VALUES LESS THAN (2001),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

在 Range 分区中，可以基于 `timestamp` 列的值分区，并使用 `unix_timestamp()` 函数，例如：

{{< copyable "sql" >}}

```sql
CREATE TABLE quarterly_report_status (
    report_id INT NOT NULL,
    report_status VARCHAR(20) NOT NULL,
    report_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

PARTITION BY RANGE ( UNIX_TIMESTAMP(report_updated) ) (
    PARTITION p0 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-01-01 00:00:00') ),
    PARTITION p1 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-04-01 00:00:00') ),
    PARTITION p2 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-07-01 00:00:00') ),
    PARTITION p3 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-10-01 00:00:00') ),
    PARTITION p4 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-01-01 00:00:00') ),
    PARTITION p5 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-04-01 00:00:00') ),
    PARTITION p6 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-07-01 00:00:00') ),
    PARTITION p7 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-10-01 00:00:00') ),
    PARTITION p8 VALUES LESS THAN ( UNIX_TIMESTAMP('2010-01-01 00:00:00') ),
    PARTITION p9 VALUES LESS THAN (MAXVALUE)
);
```

对于 timestamp 列，使用其它的分区表达式是不允许的。

Range 分区在下列条件之一或者多个都满足时，尤其有效：

* 删除旧数据。如果你使用之前的 `employees` 表的例子，你可以简单使用 `ALTER TABLE employees DROP PARTITION p0;` 删除所有在 1991 年以前停止继续在这家公司工作的员工记录。这会比使用 `DELETE FROM employees WHERE YEAR(separated) <= 1990;` 执行快得多。
* 使用包含时间或者日期的列，或者是其它按序生成的数据。
* 频繁查询分区使用的列。例如执行这样的查询 `EXPLAIN SELECT COUNT(*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store_id;` 时，TiDB 可以迅速确定，只需要扫描 `p2` 分区的数据，因为其它的分区不满足 `where` 条件。

### List 分区

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。

在创建 List 分区表之前，需要先将 session 变量 `tidb_enable_list_partition` 的值设置为 `ON`。

{{< copyable "sql" >}}

```sql
set @@session.tidb_enable_list_partition = ON
```

此外，还需保证 `tidb_enable_table_partition` 变量已开启（默认开启）。

List 分区和 Range 分区有很多相似的地方。不同之处主要在于 List 分区中，对于表的每个分区中包含的所有行，按分区表达式计算的值属于给定的数据集合。每个分区定义的数据集合有任意个值，但不能有重复的值，可通过 `PARTITION ... VALUES IN (...)` 子句对值进行定义。

假设你要创建一张人事记录表，示例如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
);
```

假如一共有 20 个商店分布在 4 个地区，如下表所示：

```
| Region  | Store ID Numbers     |
| ------- | -------------------- |
| North   | 1, 2, 3, 4, 5        |
| East    | 6, 7, 8, 9, 10       |
| West    | 11, 12, 13, 14, 15   |
| Central | 16, 17, 18, 19, 20   |
```

如果想把同一个地区商店员工的人事数据都存储在同一个分区中，你可以根据 `store_id` 来创建 List 分区：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
);
```

这样就能方便地在表中添加或删除与特定区域相关的记录。例如，假设东部地区 (East) 所有的商店都卖给了另一家公司，所有该地区商店员工相关的行数据都可以通过 `ALTER TABLE employees TRUNCATE PARTITION pEast` 删除，这比等效的 `DELETE` 语句 `DELETE FROM employees WHERE store_id IN (6, 7, 8, 9, 10)` 执行起来更加高效。

使用 `ALTER TABLE employees DROP PARTITION pEast` 也能删除所有这些行，但同时也会从表的定义中删除分区 `pEast`。那样你还需要使用 `ALTER TABLE ... ADD PARTITION` 语句来还原表的原始分区方案。

与 Range 分区的情况不同，List 分区没有类似的 `MAXVALUE` 分区来存储所有不属于其他 partition 的值。分区表达式的所有期望值都应包含在 `PARTITION ... VALUES IN (...)` 子句中。如果 `INSERT` 语句要插入的值不匹配分区的列值，该语句将执行失败并报错，如下例所示：

```sql
test> CREATE TABLE t (
    ->   a INT,
    ->   b INT
    -> )
    -> PARTITION BY LIST (a) (
    ->   PARTITION p0 VALUES IN (1, 2, 3),
    ->   PARTITION p1 VALUES IN (4, 5, 6)
    -> );
Query OK, 0 rows affected (0.11 sec)

test> INSERT INTO t VALUES (7, 7);
ERROR 1525 (HY000): Table has no partition for value 7
```

要忽略以上类型的错误，可以通过使用 `IGNORE` 关键字。使用该关键字后，就不会插入包含不匹配分区列值的行，但是会插入任何具有匹配值的行，并且不会报错:

```sql
test> TRUNCATE t;
Query OK, 1 row affected (0.00 sec)

test> INSERT IGNORE INTO t VALUES (1, 1), (7, 7), (8, 8), (3, 3), (5, 5);
Query OK, 3 rows affected, 2 warnings (0.01 sec)
Records: 5  Duplicates: 2  Warnings: 2

test> select * from t;
+------+------+
| a    | b    |
+------+------+
|    5 |    5 |
|    1 |    1 |
|    3 |    3 |
+------+------+
3 rows in set (0.01 sec)
```

### List COLUMNS 分区

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。

List COLUMNS 分区是 List 分区的一种变体，可以将多个列用作分区键，并且可以将整数类型以外的数据类型的列用作分区列。你还可以使用字符串类型、`DATE` 和 `DATETIME` 类型的列。

假设商店员工分别来自以下 12 个城市，想要根据相关规定分成 4 个区域，如下表所示：

```
| Region | Cities                         |
| :----- | ------------------------------ |
| 1      | LosAngeles,Seattle, Houston    |
| 2      | Chicago, Columbus, Boston      |
| 3      | NewYork, LongIsland, Baltimore |
| 4      | Atlanta, Raleigh, Cincinnati   |
```

使用列表列分区，你可以为员工数据创建一张表，将每行数据存储在员工所在城市对应的分区中，如下所示：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees_1 (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT,
    city VARCHAR(15)
)
PARTITION BY LIST COLUMNS(city) (
    PARTITION pRegion_1 VALUES IN('LosAngeles', 'Seattle', 'Houston'),
    PARTITION pRegion_2 VALUES IN('Chicago', 'Columbus', 'Boston'),
    PARTITION pRegion_3 VALUES IN('NewYork', 'LongIsland', 'Baltimore'),
    PARTITION pRegion_4 VALUES IN('Atlanta', 'Raleigh', 'Cincinnati')
);
```

与 List 分区不同的是，你不需要在 `COLUMNS()` 子句中使用表达式来将列值转换为整数。

List COLUMNS 分区也可以使用 `DATE` 和 `DATETIME` 类型的列进行分区，如以下示例中所示，该示例使用与先前的 `employees_1` 表相同的名称和列，但根据 `hired` 列采用 List COLUMNS 分区：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees_2 (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT,
    city VARCHAR(15)
)
PARTITION BY LIST COLUMNS(hired) (
    PARTITION pWeek_1 VALUES IN('2020-02-01', '2020-02-02', '2020-02-03',
        '2020-02-04', '2020-02-05', '2020-02-06', '2020-02-07'),
    PARTITION pWeek_2 VALUES IN('2020-02-08', '2020-02-09', '2020-02-10',
        '2020-02-11', '2020-02-12', '2020-02-13', '2020-02-14'),
    PARTITION pWeek_3 VALUES IN('2020-02-15', '2020-02-16', '2020-02-17',
        '2020-02-18', '2020-02-19', '2020-02-20', '2020-02-21'),
    PARTITION pWeek_4 VALUES IN('2020-02-22', '2020-02-23', '2020-02-24',
        '2020-02-25', '2020-02-26', '2020-02-27', '2020-02-28')
);
```

另外，你也可以在 `COLUMNS()` 子句中添加多个列，例如：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (
    id int,
    name varchar(10)
)
PARTITION BY LIST COLUMNS(id,name) (
     partition p0 values IN ((1,'a'),(2,'b')),
     partition p1 values IN ((3,'c'),(4,'d')),
     partition p3 values IN ((5,'e'),(null,null))
);
```

### Hash 分区

Hash 分区主要用于保证数据均匀地分散到一定数量的分区里面。在 Range 分区中你必须为每个分区指定值的范围；在 Hash 分区中，你只需要指定分区的数量。

使用 Hash 分区时，需要在 `CREATE TABLE` 后面添加 `PARTITION BY HASH (expr)`，其中 `expr` 是一个返回整数的表达式。当这一列的类型是整数类型时，它可以是一个列名。此外，你很可能还需要加上 `PARTITIONS num`，其中 `num` 是一个正整数，表示将表划分多少分区。

下面的语句将创建一个 Hash 分区表，按 `store_id` 分成 4 个分区：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY HASH(store_id)
PARTITIONS 4;
```

如果不指定 `PARTITIONS num`，默认的分区数量为 1。

你也可以使用一个返回整数的 SQL 表达式。例如，你可以按入职年份分区：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY HASH( YEAR(hired) )
PARTITIONS 4;
```

最高效的 Hash 函数是作用在单列上，并且函数的单调性是跟列的值是一样递增或者递减的。

例如，`date_col` 是类型为 `DATE` 的列，表达式 `TO_DAYS(date_col)` 的值是直接随 `date_col` 的值变化的。`YEAR(date_col)` 跟 `TO_DAYS(date_col)` 就不太一样，因为不是每次 `date_col` 变化时 `YEAR(date_col)` 都会得到不同的值。

作为对比，假设我们有一个类型是 INT 的 `int_col` 的列。考虑一下表达式 `POW(5-int_col,3) + 6`，这并不是一个比较好的 Hash 函数，因为随着 `int_col` 的值的变化，表达式的结果不会成比例地变化。改变 `int_col` 的值会使表达式的结果的值变化巨大。例如，`int_col` 从 5 变到 6 表达式的结果变化是 -1，但是从 6 变到 7 的时候表达式的值的变化是 -7。

总而言之，表达式越接近 `y = cx` 的形式，它越是适合作为 Hash 函数。因为表达式越是非线性的，在各个分区上面的数据的分布越是倾向于不均匀。

理论上，Hash 分区也是可以做分区裁剪的。而实际上对于多列的情况，实现很难并且计算很耗时。因此，不推荐 Hash 分区在表达式中涉及多列。

使用 `PARTITIION BY HASH` 的时候，TiDB 通过表达式的结果做“取余”运算，决定数据落在哪个分区。换句话说，如果分区表达式是 `expr`，分区数是 `num`，则由 `MOD(expr, num)` 决定存储的分区。假设 `t1` 定义如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;
```

向 `t1` 插入一行数据，其中 `col3` 列的值是 '2005-09-15'，这条数据会被插入到分区 1 中：

```
MOD(YEAR('2005-09-01'),4)
=  MOD(2005,4)
=  1
```

### 分区对 NULL 值的处理

TiDB 允许计算结果为 NULL 的分区表达式。注意，NULL 不是一个整数类型，NULL 小于所有的整数类型值，正如 `ORDER BY` 的规则一样。

#### Range 分区对 NULL 的处理

如果插入一行到 Range 分区表，它的分区列的计算结果是 NULL，那么这一行会被插入到最小的那个分区。

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
    c1 INT,
    c2 VARCHAR(20)
)

PARTITION BY RANGE(c1) (
    PARTITION p0 VALUES LESS THAN (0),
    PARTITION p1 VALUES LESS THAN (10),
    PARTITION p2 VALUES LESS THAN MAXVALUE
);
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
select * from t1 partition(p0);
```

```
+------|--------+
| c1   | c2     |
+------|--------+
| NULL | mothra |
+------|--------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
select * from t1 partition(p1);
```

```
Empty set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
select * from t1 partition(p2);
```

```
Empty set (0.00 sec)
```

删除 `p0` 后验证：

{{< copyable "sql" >}}

```sql
alter table t1 drop partition p0;
```

```
Query OK, 0 rows affected (0.08 sec)
```

{{< copyable "sql" >}}

```sql
select * from t1;
```

```
Empty set (0.00 sec)
```

#### Hash 分区对 NULL 的处理

在 Hash 分区中 NULL 值的处理有所不同，如果分区表达式的计算结果为 NULL，它会被当作 0 值处理。

{{< copyable "sql" >}}

```sql
CREATE TABLE th (
    c1 INT,
    c2 VARCHAR(20)
)

PARTITION BY HASH(c1)
PARTITIONS 2;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO th VALUES (NULL, 'mothra'), (0, 'gigan');
```

```
Query OK, 2 rows affected (0.04 sec)
```

{{< copyable "sql" >}}

```sql
select * from th partition (p0);
```

```
+------|--------+
| c1   | c2     |
+------|--------+
| NULL | mothra |
|    0 | gigan  |
+------|--------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
select * from th partition (p1);
```

```
Empty set (0.00 sec)
```

可以看到，插入的记录 `(NULL, 'mothra')` 跟 `(0, 'gigan')` 落在了同一个分区。

> **注意：**
>
> 这里 Hash 分区对 NULL 的处理跟 [MySQL 的文档描述](https://dev.mysql.com/doc/refman/8.0/en/partitioning-handling-nulls.html)一致，但是跟 MySQL 的实际行为并不一致。也就是说，MySQL 的文档跟它的实现并不一致。
>
> TiDB 的最终行为以本文档描述为准。

## 分区管理

通过 `ALTER TABLE` 语句可以执行一些添加、删除、合并、切分、重定义分区的操作。

### Range 分区管理

创建分区表：

{{< copyable "sql" >}}

```sql
CREATE TABLE members (
    id INT,
    fname VARCHAR(25),
    lname VARCHAR(25),
    dob DATE
)

PARTITION BY RANGE( YEAR(dob) ) (
    PARTITION p0 VALUES LESS THAN (1980),
    PARTITION p1 VALUES LESS THAN (1990),
    PARTITION p2 VALUES LESS THAN (2000)
);
```

删除分区：

{{< copyable "sql" >}}

```sql
ALTER TABLE members DROP PARTITION p2;
```

```
Query OK, 0 rows affected (0.03 sec)
```

清空分区：

{{< copyable "sql" >}}

```sql
ALTER TABLE members TRUNCATE PARTITION p1;
```

```
Query OK, 0 rows affected (0.03 sec)
```

> **注意：**
>
> `ALTER TABLE ... REORGANIZE PARTITION` 在 TiDB 中暂不支持。

添加分区：

{{< copyable "sql" >}}

```sql
ALTER TABLE members ADD PARTITION (PARTITION p3 VALUES LESS THAN (2010));
```

Range 分区中，`ADD PARTITION` 只能在分区列表的最后面添加，如果是添加到已存在的分区范围则会报错：

{{< copyable "sql" >}}

```sql
ALTER TABLE members
    ADD PARTITION (
    PARTITION n VALUES LESS THAN (1970));
```

```
ERROR 1463 (HY000): VALUES LESS THAN value must be strictly »
   increasing for each partition
```

### Hash 分区管理

跟 Range 分区不同，Hash 分区不能够 `DROP PARTITION`。

目前 TiDB 的实现暂时不支持 `ALTER TABLE ... COALESCE PARTITION`。对于暂不支持的分区管理语句，TiDB 会返回错误。

{{< copyable "sql" >}}

```sql
alter table members optimize partition p0;
```

```sql
ERROR 8200 (HY000): Unsupported optimize partition
```

## 分区裁剪

有一个优化叫做[“分区裁剪”](/partition-pruning.md)，它基于一个非常简单的概念：不需要扫描那些匹配不上的分区。

假设创建一个分区表 `t1`：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    region_code TINYINT UNSIGNED NOT NULL,
    dob DATE NOT NULL
)

PARTITION BY RANGE( region_code ) (
    PARTITION p0 VALUES LESS THAN (64),
    PARTITION p1 VALUES LESS THAN (128),
    PARTITION p2 VALUES LESS THAN (192),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

如果你想获得这个 select 语句的结果：

{{< copyable "sql" >}}

```sql
SELECT fname, lname, region_code, dob
    FROM t1
    WHERE region_code > 125 AND region_code < 130;
```

很显然，结果必然是在分区 `p1` 或者 `p2` 里面，也就是说，我们只需要在 `p1` 和 `p2` 里面去搜索匹配的行。去掉不必要的分区就是所谓的裁剪。优化器如果能裁剪掉一部分的分区，则执行会快于处理整个不做分区的表的相同查询。

优化器可以通过 where 条件裁剪的两个场景：

* partition_column = constant
* partition_column IN (constant1, constant2, ..., constantN)

### 分区裁剪生效的场景

1. 分区裁剪需要使用分区表上面的查询条件，所以根据优化器的优化规则，如果查询条件不能下推到分区表，则相应的查询语句无法执行分区裁剪。

    例如：

    {{< copyable "sql" >}}

    ```sql
    create table t1 (x int) partition by range (x) (
        partition p0 values less than (5),
        partition p1 values less than (10));
    create table t2 (x int);
    ```

    {{< copyable "sql" >}}

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x where t2.x > 5;
    ```

    在这个查询中，外连接可以简化成内连接，然后由 `t1.x = t2.x` 和 `t2.x > 5` 可以推出条件 `t1.x > 5`，于是可以分区裁剪并且只使用 `p1` 分区。

    {{< copyable "sql" >}}

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x and t2.x > 5;
    ```

    这个查询中的 `t2.x > 5` 条件不能下推到 `t1` 分区表上面，因此 `t1` 无法分区裁剪。

2. 由于分区裁剪的规则优化是在查询计划的生成阶段，对于执行阶段才能获取到过滤条件的场景，无法利用分区裁剪的优化。

    例如：

    {{< copyable "sql" >}}

    ```sql
    create table t1 (x int) partition by range (x) (
        partition p0 values less than (5),
        partition p1 values less than (10));
    ```

    {{< copyable "sql" >}}

    ```sql
    explain select * from t2 where x < (select * from t1 where t2.x < t1.x and t2.x < 2);
    ```

    这个查询每从 `t2` 读取一行，都会去分区表 `t1` 上进行查询，理论上这时会满足 `t1.x > val` 的过滤条件，但实际上由于分区裁剪只作用于查询计划生成阶段，而不是执行阶段，因而不会做裁剪。

3. 由于当前实现中的一处限制，对于查询条件无法下推到 TiKV 的表达式，不支持分区裁剪。

    对于一个函数表达式 `fn(col)`，如果 TiKV 支持这个函数 `fn`，则在查询优化做谓词下推的时候，`fn(col)` 会被推到叶子节点（也就是分区），因而能够执行分区裁剪。

    如果 TiKV 不支持 `fn`，则优化阶段不会把 `fn(col)` 推到叶子节点，而是在叶子上面连接一个 Selection 节点，分区裁剪的实现没有处理这种父节点的 Selection 中的条件，因此对不能下推到 TiKV 的表达式不支持分区裁剪。

4. 对于 Hash 分区类型，只有等值比较的查询条件能够支持分区裁剪。

5. 对于 Range 分区类型，分区表达式必须是 `col` 或者 `fn(col)` 的简单形式，查询条件是 `>`、`<`、`=`、`>=`、`<=` 时才能支持分区裁剪。如果分区表达式是 `fn(col)` 形式，还要求 `fn` 必须是单调函数，才有可能分区裁剪。

    这里单调函数是指某个函数 `fn` 满足条件：对于任意 `x` `y`，如果 `x > y`，则 `fn(x) > fn(y)`。

    这种是严格递增的单调函数，非严格递增的单调函数也可以符合分区裁剪要求，只要函数 `fn` 满足：对于任意 `x` `y`，如果 `x > y`，则 `fn(x) >= fn(y)`。

    理论上所有满足单调条件（严格或者非严格）的函数都是可以支持分区裁剪。实际上，目前 TiDB 已经支持的单调函数只有：

    ```
    unix_timestamp
    to_days
    ```

    例如，分区表达式是简单列的情况：

    {{< copyable "sql" >}}

    ```sql
    create table t (id int) partition by range (id) (
        partition p0 values less than (5),
        partition p1 values less than (10));
    select * from t where t > 6;
    ```

    分区表达式是 `fn(col)` 的形式，`fn` 是我们支持的单调函数 `to_days`：

    {{< copyable "sql" >}}

    ```sql
    create table t (dt datetime) partition by range (to_days(id)) (
        partition p0 values less than (to_days('2020-04-01')),
        partition p1 values less than (to_days('2020-05-01')));
    select * from t where t > '2020-04-18';
    ```

    有一处例外是 `floor(unix_timestamp(ts))` 作为分区表达式，TiDB 针对这个场景做了特殊处理，可以支持分区裁剪。

    {{< copyable "sql" >}}

    ```sql
    create table t (ts timestamp(3) not null default current_timestamp(3))
    partition by range (floor(unix_timestamp(ts))) (
        partition p0 values less than (unix_timestamp('2020-04-01 00:00:00')),
        partition p1 values less than (unix_timestamp('2020-05-01 00:00:00')));
    select * from t where t > '2020-04-18 02:00:42.123';
    ```

## 分区选择

SELECT 语句中支持分区选择。实现通过使用一个 `PARTITION` 选项实现。

{{< copyable "sql" >}}

```sql
CREATE TABLE employees  (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(25) NOT NULL,
    lname VARCHAR(25) NOT NULL,
    store_id INT NOT NULL,
    department_id INT NOT NULL
)

PARTITION BY RANGE(id)  (
    PARTITION p0 VALUES LESS THAN (5),
    PARTITION p1 VALUES LESS THAN (10),
    PARTITION p2 VALUES LESS THAN (15),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);

INSERT INTO employees VALUES
    ('', 'Bob', 'Taylor', 3, 2), ('', 'Frank', 'Williams', 1, 2),
    ('', 'Ellen', 'Johnson', 3, 4), ('', 'Jim', 'Smith', 2, 4),
    ('', 'Mary', 'Jones', 1, 1), ('', 'Linda', 'Black', 2, 3),
    ('', 'Ed', 'Jones', 2, 1), ('', 'June', 'Wilson', 3, 1),
    ('', 'Andy', 'Smith', 1, 3), ('', 'Lou', 'Waters', 2, 4),
    ('', 'Jill', 'Stone', 1, 4), ('', 'Roger', 'White', 3, 2),
    ('', 'Howard', 'Andrews', 1, 2), ('', 'Fred', 'Goldberg', 3, 3),
    ('', 'Barbara', 'Brown', 2, 3), ('', 'Alice', 'Rogers', 2, 2),
    ('', 'Mark', 'Morgan', 3, 3), ('', 'Karen', 'Cole', 3, 2);
```

你可以查看存储在分区 `p1` 中的行：

{{< copyable "sql" >}}

```sql
SELECT * FROM employees PARTITION (p1);
```

```
+----|-------|--------|----------|---------------+
| id | fname | lname  | store_id | department_id |
+----|-------|--------|----------|---------------+
|  5 | Mary  | Jones  |        1 |             1 |
|  6 | Linda | Black  |        2 |             3 |
|  7 | Ed    | Jones  |        2 |             1 |
|  8 | June  | Wilson |        3 |             1 |
|  9 | Andy  | Smith  |        1 |             3 |
+----|-------|--------|----------|---------------+
5 rows in set (0.00 sec)
```

如果希望获得多个分区中的行，可以提供分区名的列表，用逗号隔开。例如，`SELECT * FROM employees PARTITION (p1, p2)` 返回分区 `p1` 和 `p2` 的所有行。

使用分区选择时，仍然可以使用 where 条件，以及 ORDER BY 和 LIMIT 等选项。使用 HAVING 和 GROUP BY 等聚合选项也是支持的。

{{< copyable "sql" >}}

```sql
SELECT * FROM employees PARTITION (p0, p2)
    WHERE lname LIKE 'S%';
```

```
+----|-------|-------|----------|---------------+
| id | fname | lname | store_id | department_id |
+----|-------|-------|----------|---------------+
|  4 | Jim   | Smith |        2 |             4 |
| 11 | Jill  | Stone |        1 |             4 |
+----|-------|-------|----------|---------------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT id, CONCAT(fname, ' ', lname) AS name
    FROM employees PARTITION (p0) ORDER BY lname;
```

```
+----|----------------+
| id | name           |
+----|----------------+
|  3 | Ellen Johnson  |
|  4 | Jim Smith      |
|  1 | Bob Taylor     |
|  2 | Frank Williams |
+----|----------------+
4 rows in set (0.06 sec)
```

{{< copyable "sql" >}}

```sql
SELECT store_id, COUNT(department_id) AS c
    FROM employees PARTITION (p1,p2,p3)
    GROUP BY store_id HAVING c > 4;
```

```
+---|----------+
| c | store_id |
+---|----------+
| 5 |        2 |
| 5 |        3 |
+---|----------+
2 rows in set (0.00 sec)
```

分支选择支持所有类型的分区表，无论是 Range 分区或是 Hash 分区等。对于 Hash 分区，如果没有指定分区名，会自动使用 `p0`、`p1`、`p2`、……、或 `pN-1` 作为分区名。

在 `INSERT ... SELECT` 的 `SELECT` 中也是可以使用分区选择的。

## 分区的约束和限制

本节介绍当前 TiDB 分区表的一些约束和限制。

### 分区键，主键和唯一键

本节讨论分区键，主键和唯一键之间的关系。一句话总结它们之间的关系要满足的规则：**分区表的每个唯一键，必须包含分区表达式中用到的所有列**。

> every unique key on the table must use every column in the table's partitioning expression.

这里所指的唯一也包含了主键，因为根据主键的定义，主键必须是唯一的。例如，下面这些建表语句就是无效的：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2)
)

PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1),
    UNIQUE KEY (col3)
)

PARTITION BY HASH(col1 + col3)
PARTITIONS 4;
```

它们都是有唯一键但没有包含所有分区键的。

下面是一些合法的语句的例子：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2, col3)
)

PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col3)
)

PARTITION BY HASH(col1 + col3)
PARTITIONS 4;
```

下例中会产生一个报错：

{{< copyable "sql" >}}

```sql
CREATE TABLE t3 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2),
    UNIQUE KEY (col3)
)

PARTITION BY HASH(col1 + col3)
    PARTITIONS 4;
```

```
ERROR 1491 (HY000): A PRIMARY KEY must include all columns in the table's partitioning function
```

原因是 `col1` 和 `col3` 出现在分区键中，但是几个唯一键定义并没有完全包含它们。

下面这个表就没法做分区了，因为无论如何都不可能找到满足条件的分区键：

{{< copyable "sql" >}}

```sql
CREATE TABLE t4 (
    col1 INT NOT NULL,
    col2 INT NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col3),
    UNIQUE KEY (col2, col4)
);
```

根据定义，主键也是唯一键，下面两个建表语句是无效的：

{{< copyable "sql" >}}

```sql
CREATE TABLE t5 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2)
)

PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t6 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col3),
    UNIQUE KEY(col2)
)

PARTITION BY HASH( YEAR(col2) )
PARTITIONS 4;
```

两个例子中，主键都没有包含分区表达式中的全部的列。

如果既没有主键，也没有唯一键，则不存在这个限制。

DDL 变更时，添加唯一索引也需要考虑到这个限制。比如创建了这样一个表：

{{< copyable "sql" >}}

```sql
CREATE TABLE t_no_pk (c1 INT, c2 INT)
    PARTITION BY RANGE(c1) (
        PARTITION p0 VALUES LESS THAN (10),
        PARTITION p1 VALUES LESS THAN (20),
        PARTITION p2 VALUES LESS THAN (30),
        PARTITION p3 VALUES LESS THAN (40)
    );
```

```
Query OK, 0 rows affected (0.12 sec)
```

通过 `ALTER TABLE` 添加非唯一索引是可以的。但是添加唯一索引时，唯一索引里面必须包含 `c1` 列。

使用分区表时，前缀索引是不能指定为唯一属性的：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (a varchar(20), b blob,
    UNIQUE INDEX (a(5)))
    PARTITION by range columns (a) (
    PARTITION p0 values less than ('aaaaa'),
    PARTITION p1 values less than ('bbbbb'),
    PARTITION p2 values less than ('ccccc'));
```

```sql
ERROR 1503 (HY000): A UNIQUE INDEX must include all columns in the table's partitioning function
```

### 关于函数的分区限制

只有以下函数可以用于分区表达式：

```
ABS()
CEILING()
DATEDIFF()
DAY()
DAYOFMONTH()
DAYOFWEEK()
DAYOFYEAR()
EXTRACT() (see EXTRACT() function with WEEK specifier)
FLOOR()
HOUR()
MICROSECOND()
MINUTE()
MOD()
MONTH()
QUARTER()
SECOND()
TIME_TO_SEC()
TO_DAYS()
TO_SECONDS()
UNIX_TIMESTAMP() (with TIMESTAMP columns)
WEEKDAY()
YEAR()
YEARWEEK()
```

### 兼容性

目前 TiDB 支持 Range 分区、List 分区、List COLUMNS 分区和 Hash 分区，其它的 MySQL 分区类型（例如 Key 分区）尚不支持。

对于 Range Columns 类型的分区表，目前只支持单列的场景。

分区管理方面，只要底层实现可能会涉及数据挪动的操作，目前都暂不支持。包括且不限于：调整 Hash 分区表的分区数量，修改 Range 分区表的范围，合并分区，交换分区等。

对于暂不支持的分区类型，在 TiDB 中建表时会忽略分区信息，以普通表的形式创建，并且会报 Warning。

Load Data 暂时不支持分区选择。

{{< copyable "sql" >}}

```sql
create table t (id int, val int) partition by hash(id) partitions 4;
```

普通的 Load Data 操作在 TiDB 中是支持的，如下：

{{< copyable "sql" >}}

```sql
load local data infile "xxx" into t ...
```

但 Load Data 不支持分区选择操作：

{{< copyable "sql" >}}

```sql
load local data infile "xxx" into t partition (p1)...
```

对于分区表，`select * from t` 的返回结果是分区之间无序的。这跟 MySQL 不同，MySQL 的返回结果是分区之间有序，分区内部无序。

{{< copyable "sql" >}}

```sql
create table t (id int, val int) partition by range (id) (
    partition p0 values less than (3),
    partition p1 values less than (7),
    partition p2 values less than (11));
```

```
Query OK, 0 rows affected (0.10 sec)
```

{{< copyable "sql" >}}

```sql
insert into t values (1, 2), (3, 4),(5, 6),(7,8),(9,10);
```

```
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

TiDB 每次返回结果会不同，例如：

{{< copyable "sql" >}}

```
select * from t;
```

```
+------|------+
| id   | val  |
+------|------+
|    7 |    8 |
|    9 |   10 |
|    1 |    2 |
|    3 |    4 |
|    5 |    6 |
+------|------+
5 rows in set (0.00 sec)
```

MySQL 的返回结果：

{{< copyable "sql" >}}

```
select * from t;
```

```
+------|------+
| id   | val  |
+------|------+
|    1 |    2 |
|    3 |    4 |
|    5 |    6 |
|    7 |    8 |
|    9 |   10 |
+------|------+
5 rows in set (0.00 sec)
```

环境变量 `tidb_enable_list_partition` 可以控制是否启用分区表功能。如果该变量设置为 `OFF`，则建表时会忽略分区信息，以普通表的方式建表。

该变量仅作用于建表，已经建表之后再修改该变量无效。详见[系统变量和语法](/system-variables.md#tidb_enable_list_partition-从-v50-版本开始引入)。

### 动态模式

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。

TiDB 访问分区表有两种模式，`dynamic` 和 `static`，目前默认使用 `static` 模式。如果想开启 `dynamic` 模式，需要手动将 `tidb_partition_prune_mode` 设置为 `dynamic`。

{{< copyable "sql" >}}

```sql
set @@session.tidb_partition_prune_mode = 'dynamic'
```

在 `static` 模式下，TiDB 用多个算子单独访问每个分区，然后通过 Union 将结果合并起来。下面例子进行了一个简单的读取操作，可以发现 TiDB 用 Union 合并了对应两个分区的结果：

{{< copyable "sql" >}}

```sql
mysql> create table t1(id int, age int, key(id)) partition by range(id) (
    ->     partition p0 values less than (100),
    ->     partition p1 values less than (200),
    ->     partition p2 values less than (300),
    ->     partition p3 values less than (400));
Query OK, 0 rows affected (0.01 sec)

mysql> explain select * from t1 where id < 150;
+------------------------------+----------+-----------+------------------------+--------------------------------+
| id                           | estRows  | task      | access object          | operator info                  |
+------------------------------+----------+-----------+------------------------+--------------------------------+
| PartitionUnion_9             | 6646.67  | root      |                        |                                |
| ├─TableReader_12             | 3323.33  | root      |                        | data:Selection_11              |
| │ └─Selection_11             | 3323.33  | cop[tikv] |                        | lt(test.t1.id, 150)            |
| │   └─TableFullScan_10       | 10000.00 | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo |
| └─TableReader_18             | 3323.33  | root      |                        | data:Selection_17              |
|   └─Selection_17             | 3323.33  | cop[tikv] |                        | lt(test.t1.id, 150)            |
|     └─TableFullScan_16       | 10000.00 | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo |
+------------------------------+----------+-----------+------------------------+--------------------------------+
7 rows in set (0.00 sec)
```

在 `dynamic` 模式下，每个算子都支持直接访问多个分区，所以 TiDB 不再使用 Union。

{{< copyable "sql" >}}

```sql
mysql> set @@session.tidb_partition_prune_mode = 'dynamic';
Query OK, 0 rows affected (0.00 sec)

mysql> explain select * from t1 where id < 150;
+-------------------------+----------+-----------+-----------------+--------------------------------+
| id                      | estRows  | task      | access object   | operator info                  |
+-------------------------+----------+-----------+-----------------+--------------------------------+
| TableReader_7           | 3323.33  | root      | partition:p0,p1 | data:Selection_6               |
| └─Selection_6           | 3323.33  | cop[tikv] |                 | lt(test.t1.id, 150)            |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1        | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+-----------------+--------------------------------+
3 rows in set (0.00 sec)
```

从以上查询结果可知，执行计划中的 Union 消失了，分区裁剪依然生效，且执行计划只访问了 `p0` 和 `p1` 两个分区。

`dynamic` 模式让执行计划更简单清晰，省略 Union 操作可提高执行效率，还可避免 Union 并发管理的问题。此外 `dynamic` 模式还解决了两个 `static` 模式无法解决的问题：

+ 不能使用 Plan Cache（见以下示例一和示例二）
+ 不能使用 IndexJoin 的执行方式（见以下示例三和示例四）

**示例一**：以下示例在配置文件中开启 Plan Cache 功能，并在 `static` 模式下执行同一个查询两次：

{{< copyable "sql" >}}

```sql
mysql> set @a=150;
Query OK, 0 rows affected (0.00 sec)

mysql> set @@tidb_partition_prune_mode = 'static';
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t1 where id < ?';
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt using @a;
Empty set (0.00 sec)

mysql> execute stmt using @a;
Empty set (0.00 sec)

-- static 模式下执行两次相同的查询，第二次无法命中缓存
mysql> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      0 |
+------------------------+
1 row in set (0.00 sec)
```

`last_plan_from_cache` 变量可以显示上一次查询是否命中 Plan Cache。从以上示例一可知，在 `static` 模式下，即使在分区表上执行同一个查询多次，也不会命中 Plan Cache。

**示例二**：以下示例在 `dynamic` 模式下执行与示例一相同的操作：

{{< copyable "sql" >}}

```sql
mysql> set @@tidb_partition_prune_mode = 'dynamic';
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t1 where id < ?';
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt using @a;
Empty set (0.00 sec)

mysql> execute stmt using @a;
Empty set (0.00 sec)

-- dynamic 模式下第二次执行命中缓存
mysql> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)
```

由示例二结果可知，开启 `dynamic` 模式后，分区表查询能命中 Plan Cache 。

**示例三**：以下示例在 `static` 模式下尝试执行计划带 IndexJoin 的查询：

{{< copyable "sql" >}}

```sql
mysql> create table t2(id int, code int);
Query OK, 0 rows affected (0.01 sec)

mysql> set @@tidb_partition_prune_mode = 'static';
Query OK, 0 rows affected (0.00 sec)

mysql> explain select /*+ TIDB_INLJ(t1, t2) */ t1.* from t1, t2 where t2.code = 0 and t2.id = t1.id;
+--------------------------------+----------+-----------+------------------------+------------------------------------------------+
| id                             | estRows  | task      | access object          | operator info                                  |
+--------------------------------+----------+-----------+------------------------+------------------------------------------------+
| HashJoin_13                    | 12.49    | root      |                        | inner join, equal:[eq(test.t1.id, test.t2.id)] |
| ├─TableReader_42(Build)        | 9.99     | root      |                        | data:Selection_41                              |
| │ └─Selection_41               | 9.99     | cop[tikv] |                        | eq(test.t2.code, 0), not(isnull(test.t2.id))   |
| │   └─TableFullScan_40         | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                 |
| └─PartitionUnion_15(Probe)     | 39960.00 | root      |                        |                                                |
|   ├─TableReader_18             | 9990.00  | root      |                        | data:Selection_17                              |
|   │ └─Selection_17             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|   │   └─TableFullScan_16       | 10000.00 | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo                 |
|   ├─TableReader_24             | 9990.00  | root      |                        | data:Selection_23                              |
|   │ └─Selection_23             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|   │   └─TableFullScan_22       | 10000.00 | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo                 |
|   ├─TableReader_30             | 9990.00  | root      |                        | data:Selection_29                              |
|   │ └─Selection_29             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|   │   └─TableFullScan_28       | 10000.00 | cop[tikv] | table:t1, partition:p2 | keep order:false, stats:pseudo                 |
|   └─TableReader_36             | 9990.00  | root      |                        | data:Selection_35                              |
|     └─Selection_35             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|       └─TableFullScan_34       | 10000.00 | cop[tikv] | table:t1, partition:p3 | keep order:false, stats:pseudo                 |
+--------------------------------+----------+-----------+------------------------+------------------------------------------------+
17 rows in set, 1 warning (0.00 sec)
```

从以上示例三结果可知，即使使用了 `TIDB_INLJ` 的 hint，也无法使得带分区表的查询选上带 IndexJoin 的执行计划。

**示例四**：以下示例在 `dynamic` 模式下尝试执行计划带 IndexJoin 的查询：

{{< copyable "sql" >}}

```sql
mysql> set @@tidb_partition_prune_mode = 'dynamic';
Query OK, 0 rows affected (0.00 sec)

mysql> explain select /*+ TIDB_INLJ(t1, t2) */ t1.* from t1, t2 where t2.code = 0 and t2.id = t1.id;
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
| id                              | estRows  | task      | access object          | operator info                                                                                                       |
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
| IndexJoin_11                    | 12.49    | root      |                        | inner join, inner:IndexLookUp_10, outer key:test.t2.id, inner key:test.t1.id, equal cond:eq(test.t2.id, test.t1.id) |
| ├─TableReader_16(Build)         | 9.99     | root      |                        | data:Selection_15                                                                                                   |
| │ └─Selection_15                | 9.99     | cop[tikv] |                        | eq(test.t2.code, 0), not(isnull(test.t2.id))                                                                        |
| │   └─TableFullScan_14          | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                                                      |
| └─IndexLookUp_10(Probe)         | 1.25     | root      | partition:all          |                                                                                                                     |
|   ├─Selection_9(Build)          | 1.25     | cop[tikv] |                        | not(isnull(test.t1.id))                                                                                             |
|   │ └─IndexRangeScan_7          | 1.25     | cop[tikv] | table:t1, index:id(id) | range: decided by [eq(test.t1.id, test.t2.id)], keep order:false, stats:pseudo                                      |
|   └─TableRowIDScan_8(Probe)     | 1.25     | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                                                      |
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
8 rows in set (0.00 sec)
```

从示例四结果可知，开启 `dynamic` 模式后，带 IndexJoin 的计划在执行查询时被选上。

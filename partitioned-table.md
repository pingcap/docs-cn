---
title: Partitioning
summary: Learn how to use partitioning in TiDB.
aliases: ['/docs/dev/partitioned-table/','/docs/dev/reference/sql/partitioning/']
---

# Partitioning

This document introduces TiDB's implementation of partitioning.

## Partitioning types

This section introduces the types of partitioning in TiDB. Currently, TiDB supports [Range partitioning](#range-partitioning), [Range COLUMNS partitioning](#range-columns-partitioning), [List partitioning](#list-partitioning), [List COLUMNS partitioning](#list-columns-partitioning), and [Hash partitioning](#hash-partitioning).

Range partitioning, Range COLUMNS partitioning, List partitioning and List COLUMNS partitioning are used to resolve the performance issues caused by a large amount of deletions in the application, and support fast drop partition operations. Hash partitioning is used to scatter the data when there are a large amount of writes.

### Range partitioning

When a table is partitioned by Range, each partition contains rows for which the partitioning expression value lies within a given Range. Ranges have to be contiguous but not overlapping. You can define it by using `VALUES LESS THAN`.

Assume you need to create a table that contains personnel records as follows:

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
);
```

You can partition a table by Range in various ways as needed. For example, you can partition it by using the `store_id` column:

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
)

PARTITION BY RANGE (store_id) (
    PARTITION p0 VALUES LESS THAN (6),
    PARTITION p1 VALUES LESS THAN (11),
    PARTITION p2 VALUES LESS THAN (16),
    PARTITION p3 VALUES LESS THAN (21)
);
```

In this partition scheme, all rows corresponding to employees whose `store_id` is 1 through 5 are stored in the `p0` partition while all employees whose `store_id` is 6 through 10 are stored in `p1`. Range partitioning requires the partitions to be ordered, from lowest to highest.

If you insert a row of data `(72, 'Tom', 'John', '2015-06-25', NULL, NULL, 15)`, it falls in the `p2` partition. But if you insert a record whose `store_id` is larger than 20, an error is reported because TiDB cannot know which partition this record should be inserted into. In this case, you can use `MAXVALUE` when creating a table:

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
)

PARTITION BY RANGE (store_id) (
    PARTITION p0 VALUES LESS THAN (6),
    PARTITION p1 VALUES LESS THAN (11),
    PARTITION p2 VALUES LESS THAN (16),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

`MAXVALUE` represents an integer value that is larger than all other integer values. Now, all records whose `store_id` is equal to or larger than 16 (the highest value defined) are stored in the `p3` partition.

You can also partition a table by employees' job codes, which are the values of the `job_code` column. Assume that two-digit job codes stand for regular employees, three-digit codes stand for office and customer support personnel, and four-digit codes stand for managerial personnel. Then you can create a partitioned table like this:

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
)

PARTITION BY RANGE (job_code) (
    PARTITION p0 VALUES LESS THAN (100),
    PARTITION p1 VALUES LESS THAN (1000),
    PARTITION p2 VALUES LESS THAN (10000)
);
```

In this example, all rows relating to regular employees are stored in the `p0` partition, all office and customer support personnel in the `p1` partition, and all managerial personnel in the `p2` partition.

Besides splitting up the table by `store_id`, you can also partition a table by dates. For example, you can partition by employees' separation year:

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
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

In Range partitioning, you can partition based on the values of the `timestamp` column and use the `unix_timestamp()` function, for example:

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

It is not allowed to use any other partitioning expression that contains the timestamp column.

Range partitioning is particularly useful when one or more of the following conditions are satisfied:

* You want to delete the old data. If you use the `employees` table in the previous example, you can delete all records of employees who left this company before the year 1991 by simply using `ALTER TABLE employees DROP PARTITION p0;`. It is faster than executing the `DELETE FROM employees WHERE YEAR(separated) <= 1990;` operation.
* You want to use a column that contains time or date values, or containing values arising from some other series.
* You need to frequently run queries on the columns used for partitioning. For example, when executing a query like `EXPLAIN SELECT COUNT(*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store_id;`, TiDB can quickly know that only the data in the `p2` partition needs to be scanned, because the other partitions do not match the `WHERE` condition.

### Range COLUMNS partitioning

Range COLUMNS partitioning is a variant of Range partitioning. You can use one or more columns as partitioning keys. The data types of partition columns can be integer, string (`CHAR` or `VARCHAR`), `DATE`, and `DATETIME`. Any expressions, such as non-COLUMNS partitioning, are not supported.

Suppose that you want to partition by name, and drop old and invalid data, then you can create a table as follows:

```sql
CREATE TABLE t (
  valid_until datetime,
  name varchar(255) CHARACTER SET ascii,
  notes text
)
PARTITION BY RANGE COLUMNS(name,valid_until)
(PARTITION `p2022-g` VALUES LESS THAN ('G','2023-01-01 00:00:00'),
 PARTITION `p2023-g` VALUES LESS THAN ('G','2024-01-01 00:00:00'),
 PARTITION `p2024-g` VALUES LESS THAN ('G','2025-01-01 00:00:00'),
 PARTITION `p2022-m` VALUES LESS THAN ('M','2023-01-01 00:00:00'),
 PARTITION `p2023-m` VALUES LESS THAN ('M','2024-01-01 00:00:00'),
 PARTITION `p2024-m` VALUES LESS THAN ('M','2025-01-01 00:00:00'),
 PARTITION `p2022-s` VALUES LESS THAN ('S','2023-01-01 00:00:00'),
 PARTITION `p2023-s` VALUES LESS THAN ('S','2024-01-01 00:00:00'),
 PARTITION `p2024-s` VALUES LESS THAN ('S','2025-01-01 00:00:00'),
 PARTITION `p2022-` VALUES LESS THAN (0x7f,'2023-01-01 00:00:00'),
 PARTITION `p2023-` VALUES LESS THAN (0x7f,'2024-01-01 00:00:00'),
 PARTITION `p2024-` VALUES LESS THAN (0x7f,'2025-01-01 00:00:00'))
```

It will partition the data by year and by name in the ranges ['', 'G'), ['G', 'M'), ['M', 'S') and ['S',). It allows you to easily drop invalid data while still benefit from partition pruning on both `name` and `valid_until` columns. In this example, `[,)` indicates a left-closed, right-open range. For example, ['G', 'M') indicates a range containing `G` and from `G` to `M`, but excluding `M`.

### Range INTERVAL partitioning

Range INTERVAL partitioning is an extension of Range partitioning, which allows you to create partitions of a specified interval easily. Starting from v6.3.0, INTERVAL partitioning is introduced in TiDB as syntactic sugar.

> **Warning:**
>
> This is an experimental feature, which might be changed or removed without prior notice. The syntax and implementation may change before GA. If you find a bug, please open an issue in the [TiDB repository](https://github.com/pingcap/tidb/issues). 

The sytax is as follows:

```sql
PARTITION BY RANGE [COLUMNS] (<partitioning expression>)
INTERVAL (<interval expression>)
FIRST PARTITION LESS THAN (<expression>)
LAST PARTITION LESS THAN (<expression>)
[NULL PARTITION]
[MAXVALUE PARTITION]
```

For example:

```sql
CREATE TABLE employees (
    id int unsigned NOT NULL,
    fname varchar(30),
    lname varchar(30),
    hired date NOT NULL DEFAULT '1970-01-01',
    separated date DEFAULT '9999-12-31',
    job_code int,
    store_id int NOT NULL
) PARTITION BY RANGE (id)
INTERVAL (100) FIRST PARTITION LESS THAN (100) LAST PARTITION LESS THAN (10000) MAXVALUE PARTITION
```

It creates the following table:

```sql
CREATE TABLE `employees` (
  `id` int unsigned NOT NULL,
  `fname` varchar(30) DEFAULT NULL,
  `lname` varchar(30) DEFAULT NULL,
  `hired` date NOT NULL DEFAULT '1970-01-01',
  `separated` date DEFAULT '9999-12-31',
  `job_code` int DEFAULT NULL,
  `store_id` int NOT NULL
)
PARTITION BY RANGE (`id`)
(PARTITION `P_LT_100` VALUES LESS THAN (100),
 PARTITION `P_LT_200` VALUES LESS THAN (200),
...
 PARTITION `P_LT_9900` VALUES LESS THAN (9900),
 PARTITION `P_LT_10000` VALUES LESS THAN (10000),
 PARTITION `P_MAXVALUE` VALUES LESS THAN (MAXVALUE))
```

Range INTERVAL partitioning also works with [Range COLUMNS](#range-columns-partitioning) partitioning.

For example:

```sql
CREATE TABLE monthly_report_status (
    report_id int NOT NULL,
    report_status varchar(20) NOT NULL,
    report_date date NOT NULL
)
PARTITION BY RANGE COLUMNS (report_date)
INTERVAL (1 MONTH) FIRST PARTITION LESS THAN ('2000-01-01') LAST PARTITION LESS THAN ('2025-01-01')
```

It creates this table:

```
CREATE TABLE `monthly_report_status` (
  `report_id` int(11) NOT NULL,
  `report_status` varchar(20) NOT NULL,
  `report_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE COLUMNS(`report_date`)
(PARTITION `P_LT_2000-01-01` VALUES LESS THAN ('2000-01-01'),
 PARTITION `P_LT_2000-02-01` VALUES LESS THAN ('2000-02-01'),
...
 PARTITION `P_LT_2024-11-01` VALUES LESS THAN ('2024-11-01'),
 PARTITION `P_LT_2024-12-01` VALUES LESS THAN ('2024-12-01'),
 PARTITION `P_LT_2025-01-01` VALUES LESS THAN ('2025-01-01'))
```

The optional parameter `NULL PARTITION` creates a partition with the definition as `PARTITION P_NULL VALUES LESS THAN (<minimum value of the column type>)`, only matching when the partitioning expression evaluates to `NULL`. See [Handling of NULL with Range partitioning](#handling-of-null-with-range-partitioning), which explains that `NULL` is considered to be less than any other value. 

The optional parameter `MAXVALUE PARTITION` creates the last partition as `PARTITION P_MAXVALUE VALUES LESS THAN (MAXVALUE)`.

#### ALTER INTERVAL partitioned tables

INTERVAL partitioning also adds simpler syntaxes for adding and dropping partitions.

The following statement changes the first partition. It drops all partitions whose values are less than the given expression, and makes the matched partition the new first partition. It does not affect a NULL PARTITION.

```
ALTER TABLE table_name FIRST PARTITION LESS THAN (<expression>)
```

The following statement changes the last partition, meaning adding more partitions with higher ranges and room for new data. It will add new partitions with the current INTERVAL up to and including the given expression. It does not work if a `MAXVALUE PARTITION` exists, because it needs data reorganization.

```
ALTER TABLE table_name LAST PARTITION LESS THAN (<expression>)
```

#### INTERVAL partitioning details and limitations

- The INTERVAL partitioning feature only involves the `CREATE/ALTER TABLE` syntax. There is no change in metadata, so tables created or altered with the new syntax are still MySQL-compatible.
- There is no change in the output format of `SHOW CREATE TABLE` to keep MySQL compatibility.
- The new `ALTER` syntax applies to existing tables conforming to INTERVAL. You do not need to create these tables with the `INTERVAL` syntax.
- For `RANGE COLUMNS`, only integer, date, and datetime column types are supported.

### List partitioning

Before creating a List partitioned table, you need to set the value of the session variable `tidb_enable_list_partition` to `ON`.

{{< copyable "sql" >}}

```sql
set @@session.tidb_enable_list_partition = ON
```

Also, make sure that `tidb_enable_table_partition` is set to `ON`, which is the default setting.

List partitioning is similar to Range partitioning. Unlike Range partitioning, in List partitioning, the partitioning expression values for all rows in each partition are in a given value set. This value set defined for each partition can have any number of values but cannot have duplicate values. You can use the `PARTITION ... VALUES IN (...)` clause to define a value set.

Suppose that you want to create a personnel record table. You can create a table as follows:

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
);
```

Suppose that there are 20 stores distributed in 4 districts, as shown in the table below:

```
| Region  | Store ID Numbers     |
| ------- | -------------------- |
| North   | 1, 2, 3, 4, 5        |
| East    | 6, 7, 8, 9, 10       |
| West    | 11, 12, 13, 14, 15   |
| Central | 16, 17, 18, 19, 20   |
```

If you want to store the personnel data of employees of the same region in the same partition, you can create a List partitioned table based on `store_id`:

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

After creating the partitions as above, you can easily add or delete records related to a specific region in the table. For example, suppose that all stores in the East region (East) are sold to another company. Then all the row data related to the store employees of this region can be deleted by executing `ALTER TABLE employees TRUNCATE PARTITION pEast`, which is much more efficient than the equivalent statement `DELETE FROM employees WHERE store_id IN (6, 7, 8, 9, 10)`.

You can also execute `ALTER TABLE employees DROP PARTITION pEast` to delete all related rows, but this statement also deletes the `pEast` partition from the table definition. In this situation, you must execute the `ALTER TABLE ... ADD PARTITION` statement to recover the original partitioning scheme of the table.

Unlike Range partitioning, List partitioning does not have a similar `MAXVALUE` partition to store all values that do not belong to other partitions. Instead, all expected values of the partition expression must be included in the `PARTITION ... VALUES IN (...)` clause. If the value to be inserted in an `INSERT` statement does not match the column value set of any partition, the statement fails to execute and an error is reported. See the following example:

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

To ignore the error type above, you can use the `IGNORE` keyword. After using this keyword, if a row contains values that do not match the column value set of any partition, this row will not be inserted. Instead, any row with matched values is inserted, and no error is reported:

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

### List COLUMNS partitioning

List COLUMNS partitioning is a variant of List partitioning. You can use multiple columns as partition keys. Besides the integer data type, you can also use the columns in the string, `DATE`, and `DATETIME` data types as partition columns.

Suppose that you want to divide the store employees from the following 12 cities into 4 regions, as shown in the following table:

```
| Region | Cities                         |
| :----- | ------------------------------ |
| 1      | LosAngeles,Seattle, Houston    |
| 2      | Chicago, Columbus, Boston      |
| 3      | NewYork, LongIsland, Baltimore |
| 4      | Atlanta, Raleigh, Cincinnati   |
```

You can use List COLUMNS partitioning to create a table and store each row in the partition that corresponds to the employee's city, as shown below:

{{< copyable "sql" >}}

```sql
CREATE TABLE employees_1 (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
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

Unlike List partitioning, in List COLUMNS partitioning, you do not need to use the expression in the `COLUMNS()` clause to convert column values to integers.

List COLUMNS partitioning can also be implemented using columns of the `DATE` and `DATETIME` types, as shown in the following example. This example uses the same names and columns as the previous `employees_1` table, but uses List COLUMNS partitioning based on the `hired` column:

{{< copyable "sql" >}}

```sql
CREATE TABLE employees_2 (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
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

In addition, you can also add multiple columns in the `COLUMNS()` clause. For example:

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

### Hash partitioning

Hash partitioning is used to make sure that data is evenly scattered into a certain number of partitions. With Range partitioning, you must specify the range of the column values for each partition when you use Range partitioning, while you just need to specify the number of partitions when you use Hash partitioning.

Partitioning by Hash requires you to append a `PARTITION BY HASH (expr)` clause to the `CREATE TABLE` statement. `expr` is an expression that returns an integer. It can be a column name if the type of this column is integer. In addition, you might also need to append `PARTITIONS num`, where `num` is a positive integer indicating how many partitions a table is divided into.

The following operation creates a Hash partitioned table, which is divided into 4 partitions by `store_id`:

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY HASH(store_id)
PARTITIONS 4;
```

If `PARTITIONS num` is not specified, the default number of partitions is 1.

You can also use an SQL expression that returns an integer for `expr`. For example, you can partition a table by the hire year:

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY HASH( YEAR(hired) )
PARTITIONS 4;
```

The most efficient Hash function is one which operates upon a single table column, and whose value increases or decreases consistently with the column value.

For example, `date_col` is a column whose type is `DATE`, and the value of the `TO_DAYS(date_col)` expression varies with the value of `date_col`. `YEAR(date_col)` is different from `TO_DAYS(date_col)`, because not every possible change in `date_col` produces an equivalent change in `YEAR(date_col)`.

In contrast, assume that you have an `int_col` column whose type is `INT`. Now consider about the expression `POW(5-int_col,3) + 6`. It is not a good Hash function though, because as the value of `int_col` changes, the result of the expression does not change proportionally. A value change in `int_col` might result in a huge change in the expression result. For example, when `int_col` changes from 5 to 6, the change of the expression result is -1. But the result change might be -7 when `int_col` changes from 6 to 7.

In conclusion, when the expression has a form that is closer to `y = cx`, it is more suitable to be a Hash function. Because the more non-linear an expression is, the more unevenly scattered the data among the partitions tends to be.

In theory, pruning is also possible for expressions involving more than one column value, but determining which of such expressions are suitable can be quite difficult and time-consuming. For this reason, the use of hashing expressions involving multiple columns is not particularly recommended.

When using `PARTITION BY HASH`, TiDB decides which partition the data should fall into based on the modulus of the result of the expression. In other words, if a partitioning expression is `expr` and the number of partitions is `num`, `MOD(expr, num)` decides the partition in which the data is stored. Assume that `t1` is defined as follows:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;
```

When you insert a row of data into `t1` and the value of `col3` is '2005-09-15', then this row is inserted into partition 1:

```
MOD(YEAR('2005-09-01'),4)
=  MOD(2005,4)
=  1
```

#### How TiDB handles Linear Hash partitions

Before v6.4.0, if you execute DDL statements of [MySQL Linear Hash](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html) partitions in TiDB, TiDB can only create non-partitioned tables. In this case, if you still want to use partitioned tables in TiDB, you need to modify the DDL statements.

Since v6.4.0, TiDB supports parsing the MySQL `PARTITION BY LINEAR HASH` syntax but ignores the `LINEAR` keyword in it. If you have some existing DDL and DML statements of MySQL Linear Hash partitions, you can execute them in TiDB without modification:

- For a `CREATE` statement of MySQL Linear Hash partitions, TiDB will create a non-linear Hash partitioned table (note that there is no Linear Hash partitioned table in TiDB). If the number of partitions is a power of 2, the rows in the TiDB Hash partitioned table are distributed the same as that in the MySQL Linear Hash partitioned table. Otherwise, the distribution of these rows in TiDB is different from MySQL. This is because non-linear partitioned tables use a simple "modulus number of partition", while linear partitioned tables use "modulus next power of 2 and fold the values between the number of partitions and the next power of 2". For details, see [#38450](https://github.com/pingcap/tidb/issues/38450).

- For all other statements of MySQL Linear Hash partitions, they work in TiDB the same as that in MySQL, except that the rows are distributed differently if the number of partitions is not a power of 2, which will give different results for [partition selection](#partition-selection), `TRUNCATE PARTITION`, and `EXCHANGE PARTITION`.

### How TiDB partitioning handles NULL

It is allowed in TiDB to use `NULL` as the calculation result of a partitioning expression.

> **Note:**
>
> `NULL` is not an integer. TiDB's partitioning implementation treats `NULL` as being less than any other integer values, just as `ORDER BY` does.

#### Handling of NULL with Range partitioning

When you insert a row into a table partitioned by Range, and the column value used to determine the partition is `NULL`, then this row is inserted into the lowest partition.

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

Drop the `p0` partition and verify the result:

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

#### Handling of NULL with Hash partitioning

When partitioning tables by Hash, there is a different way of handling `NULL` value - if the calculation result of the partitioning expression is `NULL`, it is considered as `0`.

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

You can see that the inserted record `(NULL, 'mothra')` falls into the same partition as `(0, 'gigan')`.

> **Note:**
>
> `NULL` values by Hash partitions in TiDB are handled in the same way as described in [How MySQL Partitioning Handles NULL](https://dev.mysql.com/doc/refman/8.0/en/partitioning-handling-nulls.html), which, however, is not consistent with the actual behavior of MySQL. In other words, MySQL's implementation in this case is not consistent with its documentation.
>
> In this case, the actual behavior of TiDB is in line with the description of this document.

## Partition management

For `LIST` and `RANGE` partitioned tables, you can add and drop partitions using the `ALTER TABLE <table name> ADD PARTITION (<partition specification>)` or `ALTER TABLE <table name> DROP PARTITION <list of partitions>` statement.

For `LIST` and `RANGE` partitioned tables, `REORGANIZE PARTITION` is not yet supported.

For `HASH` partitioned tables, `COALESCE PARTITION` and `ADD PARTITION` are not yet supported.

`EXCHANGE PARTITION` works by swapping a partition and a non-partitioned table, similar to how renaming a table like `RENAME TABLE t1 TO t1_tmp, t2 TO t1, t1_tmp TO t2` works.

For example, `ALTER TABLE partitioned_table EXCHANGE PARTITION p1 WITH TABLE non_partitioned_table` swaps the `partitioned_table` table `p1` partition with the `non_partitioned_table` table.

Ensure that all rows that you are exchanging into the partition match the partition definition; otherwise, the statement will fail.

Note that TiDB has some specific features that might affect `EXCHANGE PARTITION`. When the table structure contains such features, you need to ensure that `EXCHANGE PARTITION` meets the [MySQL's EXCHANGE PARTITION condition](https://dev.mysql.com/doc/refman/8.0/en/partitioning-management-exchange.html). Meanwhile, ensure that these specific features are defined the same for both partitioned and non-partitioned tables. These specific features include the following:

<CustomContent platform="tidb">

* [Placement Rules in SQL](/placement-rules-in-sql.md): placement policies are the same.

</CustomContent>

* [TiFlash](/tikv-overview.md): the numbers of TiFlash replicas are the same.
* [Clustered Indexes](/clustered-indexes.md): partitioned and non-partitioned tables are both `CLUSTERED`, or both `NONCLUSTERED`.

In addition, there are limitations on the compatibility of `EXCHANGE PARTITION` with other components. Both partitioned and non-partitioned tables must have the same definition.

- TiFlash: when the TiFlash replica definitions in partitioned and non-partitioned tables are different, the `EXCHANGE PARTITION` operation cannot be performed.
- TiCDC: TiCDC replicates the `EXCHANGE PARTITION` operation when both partitioned and non-partitioned tables have primary keys or unique keys. Otherwise, TiCDC will not replicate the operation.
- TiDB Lightning and BR: do not perform the `EXCHANGE PARTITION` operation during import using TiDB Lightning or during restore using BR.

### Range partition management

Create a partitioned table:

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

Drop a partition:

{{< copyable "sql" >}}

```sql
ALTER TABLE members DROP PARTITION p2;
```

```
Query OK, 0 rows affected (0.03 sec)
```

Empty a partition:

{{< copyable "sql" >}}

```sql
ALTER TABLE members TRUNCATE PARTITION p1;
```

```
Query OK, 0 rows affected (0.03 sec)
```

> **Note:**
>
> `ALTER TABLE ... REORGANIZE PARTITION` is currently unsupported in TiDB.

Add a partition:

{{< copyable "sql" >}}

```sql
ALTER TABLE members ADD PARTITION (PARTITION p3 VALUES LESS THAN (2010));
```

When partitioning tables by Range, `ADD PARTITION` can be only appended to the very end of a partition list. If it is appended to an existing Range partition, an error is reported:

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

### Hash partition management

Unlike Range partitioning, `DROP PARTITION` is not supported in Hash partitioning.

Currently, `ALTER TABLE ... COALESCE PARTITION` is not supported in TiDB as well. For partition management statements that are not currently supported, TiDB returns an error.

{{< copyable "sql" >}}

```sql
alter table members optimize partition p0;
```

```sql
ERROR 8200 (HY000): Unsupported optimize partition
```

## Partition pruning

[Partition pruning](/partition-pruning.md) is an optimization which is based on a very simple idea - do not scan the partitions that do not match.

Assume that you create a partitioned table `t1`:

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

If you want to get the result of this `SELECT` statement:

{{< copyable "sql" >}}

```sql
SELECT fname, lname, region_code, dob
    FROM t1
    WHERE region_code > 125 AND region_code < 130;
```

It is evident that the result falls in either the `p1` or the `p2` partition, that is, you just need to search for the matching rows in `p1` and `p2`. Excluding the unneeded partitions is so-called "pruning". If the optimizer is able to prune a part of partitions, the execution of the query in the partitioned table will be much faster than that in a non-partitioned table.

The optimizer can prune partitions through `WHERE` conditions in the following two scenarios:

* partition_column = constant
* partition_column IN (constant1, constant2, ..., constantN)

Currently, partition pruning does not work with `LIKE` conditions.

### Some cases for partition pruning to take effect

1. Partition pruning uses the query conditions on the partitioned table, so if the query conditions cannot be pushed down to the partitioned table according to the planner's optimization rules, partition pruning does not apply for this query.

    For example:

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

    In this query, the left out join is converted to the inner join, and then `t1.x > 5` is derived from `t1.x = t2.x` and `t2.x > 5`, so it could be used in partition pruning and only the partition `p1` remains.

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x and t2.x > 5;
    ```

    In this query, `t2.x > 5` cannot be pushed down to the `t1` partitioned table, so partition pruning would not take effect for this query.

2. Since partition pruning is done during the plan optimizing phase, it does not apply for those cases that filter conditions are unknown until the execution phase.

    For example:

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

    This query reads a row from `t2` and uses the result for the subquery on `t1`. Theoretically, partition pruning could benefit from `t1.x > val` expression in the subquery, but it does not take effect there as that happens in the execution phase.

3. As a result of a limitation from current implementation, if a query condition cannot be pushed down to TiKV, it cannot be used by the partition pruning.

    Take the `fn(col)` expression as an example. If the TiKV coprocessor supports this `fn` function, `fn(col)` may be pushed down to the the leaf node (that is, partitioned table) according to the predicate push-down rule during the plan optimizing phase, and partition pruning can use it.

    If the TiKV coprocessor does not support this `fn` function, `fn(col)` would not be pushed down to the leaf node. Instead, it becomes a `Selection` node above the leaf node. The current partition pruning implementation does not support this kind of plan tree.

4. For Hash partition, the only query supported by partition pruning is the equal condition.

5. For Range partition, for partition pruning to take effect, the partition expression must be in those forms: `col` or `fn(col)`, and the query condition must be one of `>`, `<`, `=`, `>=`, and `<=`. If the partition expression is in the form of `fn(col)`, the `fn` function must be monotonous.

    If the `fn` function is monotonous, for any `x` and `y`, if `x > y`, then `fn(x) > fn(y)`. Then this `fn` function can be called strictly monotonous. For any `x` and `y`, if `x > y`, then `fn(x) >= fn(y)`. In this case, `fn` could also be called "monotonous". In theory, all monotonous functions are supported by partition pruning.

    Currently, partition pruning in TiDB only support those monotonous functions:

    * [`UNIX_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)
    * [`TO_DAYS()`](/functions-and-operators/date-and-time-functions.md)

    For example, the partition expression is a simple column:

    {{< copyable "sql" >}}

    ```sql
    create table t (id int) partition by range (id) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    select * from t where id > 6;
    ```

    Or the partition expression is in the form of `fn(col)` where `fn` is `to_days`:

    {{< copyable "sql" >}}

    ```sql
    create table t (dt datetime) partition by range (to_days(id)) (
            partition p0 values less than (to_days('2020-04-01')),
            partition p1 values less than (to_days('2020-05-01')));
    select * from t where dt > '2020-04-18';
    ```

    An exception is `floor(unix_timestamp())` as the partition expression. TiDB does some optimization for that case by case, so it is supported by partition pruning.

    {{< copyable "sql" >}}

    ```sql
    create table t (ts timestamp(3) not null default current_timestamp(3))
    partition by range (floor(unix_timestamp(ts))) (
            partition p0 values less than (unix_timestamp('2020-04-01 00:00:00')),
            partition p1 values less than (unix_timestamp('2020-05-01 00:00:00')));
    select * from t where ts > '2020-04-18 02:00:42.123';
    ```

## Partition selection

`SELECT` statements support partition selection, which is implemented by using a `PARTITION` option.

{{< copyable "sql" >}}

```sql
SET @@sql_mode = '';

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

You can view the rows stored in the `p1` partition:

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

If you want to get the rows in multiple partitions, you can use a list of partition names which are separated by commas. For example, `SELECT * FROM employees PARTITION (p1, p2)` returns all rows in the `p1` and `p2` partitions.

When you use partition selection, you can still use `WHERE` conditions and options such as `ORDER BY` and `LIMIT`. It is also supported to use aggregation options such as `HAVING` and `GROUP BY`.

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

Partition selection is supported for all types of table partitioning, including Range partitioning and Hash partitioning. For Hash partitions, if partition names are not specified, `p0`, `p1`, `p2`,..., or `pN-1` is automatically used as the partition name.

`SELECT` in `INSERT ... SELECT` can also use partition selection.

## Restrictions and limitations on partitions

This section introduces some restrictions and limitations on partitioned tables in TiDB.

### Partitioning keys, primary keys and unique keys

This section discusses the relationship of partitioning keys with primary keys and unique keys. The rule governing this relationship can be expressed as follows: **Every unique key on the table must use every column in the table's partitioning expression**. This also includes the table's primary key, because it is by definition a unique key.

For example, the following table creation statements are invalid:

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

In each case, the proposed table has at least one unique key that does not include all columns used in the partitioning expression.

The valid statements are as follows:

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

The following example displays an error:

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

The `CREATE TABLE` statement fails because both `col1` and `col3` are included in the proposed partitioning key, but neither of these columns is part of both of unique keys on the table. After the following modifications, the `CREATE TABLE` statement becomes valid:

{{< copyable "sql" >}}

```sql
CREATE TABLE t3 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2, col3),
    UNIQUE KEY (col1, col3)
)
PARTITION BY HASH(col1 + col3)
    PARTITIONS 4;
```

The following table cannot be partitioned at all, because there is no way to include in a partitioning key any columns that belong to both unique keys:

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

Because every primary key is by definition a unique key, so the next two statements are invalid:

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

In the above examples, the primary key does not include all columns referenced in the partitioning expression. After adding the missing column in the primary key, the `CREATE TABLE` statement becomes valid:

{{< copyable "sql" >}}

```sql
CREATE TABLE t5 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2, col3)
)
PARTITION BY HASH(col3)
PARTITIONS 4;
CREATE TABLE t6 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2, col3),
    UNIQUE KEY(col2)
)
PARTITION BY HASH( YEAR(col2) )
PARTITIONS 4;
```

If a table has neither unique keys nor primary keys, then this restriction does not apply.

When you change tables using DDL statements, you also need to consider this restriction when adding a unique index. For example, when you create a partitioned table as shown below:

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

You can add a non-unique index by using `ALTER TABLE` statements. But if you want to add a unique index, the `c1` column must be included in the unique index.

When using a partitioned table, you cannot specify the prefix index as a unique attribute:

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

### Partitioning limitations relating to functions

Only the functions shown in the following list are allowed in partitioning expressions:

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

### Compatibility with MySQL

Currently, TiDB supports Range partitioning, Range COLUMNS partitioning, List partitioning, List COLUMNS partitioning, and Hash partitioning. Other partitioning types that are available in MySQL such as key partitioning are not supported yet in TiDB.

With regard to partition management, any operation that requires moving data in the bottom implementation is not supported currently, including but not limited to: adjust the number of partitions in a Hash partitioned table, modify the Range of a Range partitioned table, merge partitions and exchange partitions.

For the unsupported partitioning types, when you create a table in TiDB, the partitioning information is ignored and the table is created in the regular form with a warning reported.

The `LOAD DATA` syntax does not support partition selection currently in TiDB.

{{< copyable "sql" >}}

```sql
create table t (id int, val int) partition by hash(id) partitions 4;
```

The regular `LOAD DATA` operation is supported:

{{< copyable "sql" >}}

```sql
load local data infile "xxx" into t ...
```

But `Load Data` does not support partition selection:

{{< copyable "sql" >}}

```sql
load local data infile "xxx" into t partition (p1)...
```

For a partitioned table, the result returned by `select * from t` is unordered between the partitions. This is different from the result in MySQL, which is ordered between the partitions but unordered inside the partitions.

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

TiDB returns a different result every time, for example:

{{< copyable "sql" >}}

```sql
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

The result returned in MySQL:

{{< copyable "sql" >}}

```sql
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

The `tidb_enable_list_partition` environment variable controls whether to enable the partitioned table feature. If this variable is set to `OFF`, the partition information will be ignored when a table is created, and this table will be created as a normal table.

This variable is only used in table creation. After the table is created, modify this variable value takes no effect. For details, see [system variables](/system-variables.md#tidb_enable_list_partition-new-in-v50).

### Dynamic pruning mode

TiDB accesses partitioned tables in either `dynamic` or `static` mode. `dynamic` mode is used by default since v6.3.0. However, dynamic partitioning is effective only after the full table-level statistics, or GlobalStats, are collected. Before GlobalStats are collected, TiDB will use the `static` mode instead. For detailed information about GlobalStats, see [Collect statistics of partitioned tables in dynamic pruning mode](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode).

{{< copyable "sql" >}}

```sql
set @@session.tidb_partition_prune_mode = 'dynamic'
```

Manual ANALYZE and normal queries use the session-level `tidb_partition_prune_mode` setting. The `auto-analyze` operation in the background uses the global `tidb_partition_prune_mode` setting.

In `static` mode, partitioned tables use partition-level statistics. In `dynamic` mode, partitioned tables use table-level GlobalStats.

When switching from `static` mode to `dynamic` mode, you need to check and collect statistics manually. This is because after the switch to `dynamic` mode, partitioned tables have only partition-level statistics but no table-level statistics. GlobalStats are collected only upon the next `auto-analyze` operation.

{{< copyable "sql" >}}

```sql
set session tidb_partition_prune_mode = 'dynamic';
show stats_meta where table_name like "t";
```

```
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          | p0             | 2022-05-27 20:23:34 |            1 |         2 |
| test    | t          | p1             | 2022-05-27 20:23:34 |            2 |         4 |
| test    | t          | p2             | 2022-05-27 20:23:34 |            2 |         4 |
+---------+------------+----------------+---------------------+--------------+-----------+
3 rows in set (0.01 sec)
```

To make sure that the statistics used by SQL statements are correct after you enable global `dynamic` pruning mode, you need to manually trigger `analyze` on the tables or on a partition of the table to obtain GlobalStats.

{{< copyable "sql" >}}

```sql
analyze table t partition p1;
show stats_meta where table_name like "t";
```

```
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          | global         | 2022-05-27 20:50:53 |            0 |         5 |
| test    | t          | p0             | 2022-05-27 20:23:34 |            1 |         2 |
| test    | t          | p1             | 2022-05-27 20:50:52 |            0 |         2 |
| test    | t          | p2             | 2022-05-27 20:50:08 |            0 |         2 |
+---------+------------+----------------+---------------------+--------------+-----------+
4 rows in set (0.00 sec)
```

If the following warning is displayed during the `analyze` process, partition statistics are inconsistent, and you need to collect statistics of these partitions or the entire table again.

```
| Warning | 8244 | Build table: `t` column: `a` global-level stats failed due to missing partition-level column stats, please run analyze table to refresh columns of all partitions
```

You can also use scripts to update statistics of all partitioned tables. For details, see [Update statistics of partitioned tables in dynamic pruning mode](#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode).

After table-level statistics are ready, you can enable the global dynamic pruning mode, which is effective to all SQL statements and `auto-analyze` operations.

{{< copyable "sql" >}}

```sql
set global tidb_partition_prune_mode = dynamic
```

In `static` mode, TiDB accesses each partition separately using multiple operators, and then merges the results using `Union`. The following example is a simple read operation where TiDB merges the results of two corresponding partitions using `Union`:

{{< copyable "sql" >}}

```sql
mysql> create table t1(id int, age int, key(id)) partition by range(id) (
    ->     partition p0 values less than (100),
    ->     partition p1 values less than (200),
    ->     partition p2 values less than (300),
    ->     partition p3 values less than (400));
Query OK, 0 rows affected (0.01 sec)

mysql> explain select * from t1 where id < 150;
```

```
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

In `dynamic` mode, each operator supports direct access to multiple partitions, so TiDB no longer uses `Union`.

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

From the above query results, you can see that the `Union` operator in the execution plan disappears while the partition pruning still takes effect and the execution plan only accesses `p0` and `p1`.

`dynamic` mode makes execution plans simpler and clearer. Omitting the Union operation can improve the execution efficiency and avoid the problem of Union concurrent execution. In addition, `dynamic` mode also allows execution plans with IndexJoin which cannot be used in `static` mode. (See examples below)

**Example 1**: In the following example, a query is performed in `static` mode using the execution plan with IndexJoin:

{{< copyable "sql" >}}

```sql
mysql> create table t1 (id int, age int, key(id)) partition by range(id)
    -> (partition p0 values less than (100),
    ->  partition p1 values less than (200),
    ->  partition p2 values less than (300),
    ->  partition p3 values less than (400));
Query OK, 0 rows affected (0,08 sec)

mysql> create table t2 (id int, code int);
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

mysql> show warnings;
+---------+------+------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                            |
+---------+------+------------------------------------------------------------------------------------+
| Warning | 1815 | Optimizer Hint /*+ INL_JOIN(t1, t2) */ or /*+ TIDB_INLJ(t1, t2) */ is inapplicable |
+---------+------+------------------------------------------------------------------------------------+
1 row in set (0,00 sec)
```

From example 1, you can see that even if the `TIDB_INLJ` hint is used, the query on the partitioned table cannot select the execution plan with IndexJoin.

**Example 2**: In the following example, the query is performed in `dynamic` mode using the execution plan with IndexJoin:

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
| └─IndexLookUp_10(Probe)         | 12.49    | root      | partition:all          |                                                                                                                     |
|   ├─Selection_9(Build)          | 12.49    | cop[tikv] |                        | not(isnull(test.t1.id))                                                                                             |
|   │ └─IndexRangeScan_7          | 12.50    | cop[tikv] | table:t1, index:id(id) | range: decided by [eq(test.t1.id, test.t2.id)], keep order:false, stats:pseudo                                      |
|   └─TableRowIDScan_8(Probe)     | 12.49    | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                                                      |
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
8 rows in set (0.00 sec)
```

From example 2, you can see that in `dynamic` mode, the execution plan with IndexJoin is selected when you execute the query.

Currently, neither `static` nor `dynamic` pruning mode supports prepared statements plan cache.

#### Update statistics of partitioned tables in dynamic pruning mode

1. Locate all partitioned tables:

    {{< copyable "sql" >}}

    ```sql
    select distinct concat(TABLE_SCHEMA,'.',TABLE_NAME)
        from information_schema.PARTITIONS
        where TABLE_SCHEMA not in('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');
    ```

    ```
    +-------------------------------------+
    | concat(TABLE_SCHEMA,'.',TABLE_NAME) |
    +-------------------------------------+
    | test.t                              |
    +-------------------------------------+
    1 row in set (0.02 sec)
    ```

2. Generate the statements for updating the statistics of all partitioned tables:

    {{< copyable "sql" >}}

    ```sql
    select distinct concat('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;')
        from information_schema.PARTITIONS
        where TABLE_SCHEMA not in ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');
    +----------------------------------------------------------------------+
    | concat('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') |
    +----------------------------------------------------------------------+
    | ANALYZE TABLE test.t ALL COLUMNS;                                    |
    +----------------------------------------------------------------------+
    1 row in set (0.01 sec)
    ```

    You can change `ALL COLUMNS` to the columns you need.

3. Export the batch update statements to a file:

    {{< copyable "sql" >}}

    ```sql
    mysql --host xxxx --port xxxx -u root -p -e "select distinct concat('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') \
        from information_schema.PARTITIONS \
        where TABLE_SCHEMA not in ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');" | tee gatherGlobalStats.sql
    ```

4. Execute a batch update:

    Process SQL statements before executing the `source` command:

    ```
    sed -i "" '1d' gatherGlobalStats.sql --- mac
    sed -i '1d' gatherGlobalStats.sql --- linux
    ```

    {{< copyable "sql" >}}

    ```sql
    SET session tidb_partition_prune_mode = dynamic;
    source gatherGlobalStats.sql
    ```

---
title: 分区表
summary: 了解如何在 TiDB 中使用分区表。
---

# 分区表

本文档介绍 TiDB 的分区表实现。

## 分区类型

本节介绍 TiDB 中的分区类型。目前，TiDB 支持[范围分区](#范围分区)、[范围列分区](#范围列分区)、[列表分区](#列表分区)、[列表列分区](#列表列分区)、[哈希分区](#哈希分区)和[键分区](#键分区)。

- 范围分区、范围列分区、列表分区和列表列分区用于解决应用程序中大量删除操作导致的性能问题，并支持快速删除分区。
- 哈希分区和键分区用于在大量写入的场景中分布数据。与哈希分区相比，键分区支持分布多个列的数据，并支持对非整数列进行分区。

### 范围分区

当表按范围分区时，每个分区包含分区表达式值在给定范围内的行。范围必须是连续的但不能重叠。你可以使用 `VALUES LESS THAN` 来定义它。

假设你需要创建一个包含人事记录的表，如下所示：

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

你可以根据需要以各种方式按范围分区表。例如，你可以使用 `store_id` 列进行分区：

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

在此分区方案中，所有 `store_id` 为 1 到 5 的员工对应的行存储在 `p0` 分区中，而所有 `store_id` 为 6 到 10 的员工存储在 `p1` 分区中。范围分区要求分区按从低到高的顺序排列。

如果你插入一行数据 `(72, 'Tom', 'John', '2015-06-25', NULL, NULL, 15)`，它会落在 `p2` 分区中。但如果你插入一条 `store_id` 大于 20 的记录，则会报错，因为 TiDB 不知道该记录应该插入到哪个分区。在这种情况下，你可以在创建表时使用 `MAXVALUE`：

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

`MAXVALUE` 表示一个大于所有其他整数值的整数值。现在，所有 `store_id` 大于或等于 16（定义的最高值）的记录都存储在 `p3` 分区中。

你也可以按员工的工作代码（即 `job_code` 列的值）对表进行分区。假设两位数的工作代码代表普通员工，三位数代码代表办公室和客户支持人员，四位数代码代表管理人员。那么你可以创建一个分区表，如下所示：

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

在此示例中，所有与普通员工相关的行存储在 `p0` 分区中，所有办公室和客户支持人员存储在 `p1` 分区中，所有管理人员存储在 `p2` 分区中。

除了按 `store_id` 拆分表外，你还可以按日期对表进行分区。例如，你可以按员工的离职年份进行分区：

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

在范围分区中，你可以基于 `timestamp` 列的值进行分区，并使用 `unix_timestamp()` 函数，例如：

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

不允许使用包含 timestamp 列的任何其他分区表达式。

在以下情况下，范围分区特别有用：

* 你想要删除旧数据。如果使用前面示例中的 `employees` 表，你可以通过简单使用 `ALTER TABLE employees DROP PARTITION p0;` 来删除 1991 年之前离职的所有员工的记录。这比执行 `DELETE FROM employees WHERE YEAR(separated) <= 1990;` 操作要快得多。
* 你想使用包含时间或日期值的列，或包含来自其他系列的值的列。
* 你需要经常在用于分区的列上运行查询。例如，当执行像 `EXPLAIN SELECT COUNT(*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store_id;` 这样的查询时，TiDB 可以快速知道只需要扫描 `p2` 分区中的数据，因为其他分区不符合 `WHERE` 条件。

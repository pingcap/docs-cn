---
title: 生成列
---

# 生成列

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

本文介绍生成列的概念以及用法。

## 生成列的基本概念

与一般的列不同，生成列的值由列定义中表达式计算得到。对生成列进行插入或更新操作时，并不能对之赋值，只能使用 `DEFAULT`。

生成列包括存储生成列和虚拟生成列。存储生成列会将计算得到的值存储起来，在读取时不需要重新计算。虚拟生成列不会存储其值，在读取时会重新计算。存储生成列和虚拟生成列相比，前者在读取时性能更好，但是要占用更多的磁盘空间。

无论是存储生成列还是虚拟列，都可以在其上面建立索引。

## 生成列的应用

生成列的主要的作用之一：从 JSON 数据类型中解出数据，并为该数据建立索引。

MySQL 5.7 及 TiDB 都不能直接为 JSON 类型的列添加索引，即不支持在如下表结构中的 `address_info` 上建立索引：

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

如果要为 JSON 列某个字段添加索引，可以抽取该字段为生成列。

以 `city` 这一 `address_info` 中的字段为例，可以为其建立一个虚拟生成列并添加索引：

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))),
    KEY (city)
);
```

该表中，`city` 列是一个虚拟生成列。并且在该列上建立了索引。以下语句能够利用索引加速语句的执行速度：

{{< copyable "sql" >}}

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT name, id FROM person WHERE city = 'Beijing';
```

```
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
| id                              | estRows | task      | access object                  | operator info                                               |
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
| Projection_4                    | 10.00   | root      |                                | test.person.name, test.person.id                            |
| └─IndexLookUp_10                | 10.00   | root      |                                |                                                             |
|   ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:person, index:city(city) | range:["Beijing","Beijing"], keep order:false, stats:pseudo |
|   └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:person                   | keep order:false, stats:pseudo                              |
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
```

从执行计划中，可以看出使用了 `city` 这个索引来读取满足 `city = 'Beijing'` 这个条件的行的 `HANDLE`，再用这个 `HANDLE` 来读取该行的数据。

如果 `$.city` 路径中无数据，则 `JSON_EXTRACT` 返回 `NULL`。如果想增加约束，`city` 列必须是 `NOT NULL`，则可按照以下方式定义虚拟生成列：

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) NOT NULL,
    KEY (city)
);
```

## 生成列在 INSERT 和 UPDATE 语句中的行为

`INSERT` 和 `UPDATE` 语句都会检查生成列计算得到的值是否满足生成列的定义。未通过有效性检测的行会返回错误：

{{< copyable "sql" >}}

```sql
INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
```

```
ERROR 1048 (23000): Column 'city' cannot be null
```

## 索引生成列替换

当查询中出现的某个表达式与一个含索引的生成列同等时，TiDB 会将这个表达式替换为对应的生成列，这样就可以在生成查询计划时考虑使用这个索引。

例如，下面的例子为 `a+1` 这个表达式创建生成列并添加索引，从而加速了查询。

{{< copyable "sql" >}}

```sql
create table t(a int);
desc select a+1 from t where a+1=3;
+---------------------------+----------+-----------+---------------+--------------------------------+
| id                        | estRows  | task      | access object | operator info                  |
+---------------------------+----------+-----------+---------------+--------------------------------+
| Projection_4              | 8000.00  | root      |               | plus(test.t.a, 1)->Column#3    |
| └─TableReader_7           | 8000.00  | root      |               | data:Selection_6               |
|   └─Selection_6           | 8000.00  | cop[tikv] |               | eq(plus(test.t.a, 1), 3)       |
|     └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+---------------------------+----------+-----------+---------------+--------------------------------+
4 rows in set (0.00 sec)

alter table t add column b bigint as (a+1) virtual;
alter table t add index idx_b(b);
desc select a+1 from t where a+1=3;
+------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                     | estRows | task      | access object           | operator info                               |
+------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                         | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t, index:idx_b(b) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+-------------------------+---------------------------------------------+
2 rows in set (0.01 sec)
```

> **注意：**
>
> 只有当待替换的表达式类型和生成列类型严格相等时，才会进行转换。
>
> 上例中，`a` 的类型是 int，而 `a+1` 的列类型是 bigint，如果将生成列的类型定为 int，就不会发生替换。
>
> 关于类型转换规则，可以参见[表达式求值的类型转换](/functions-and-operators/type-conversion-in-expression-evaluation.md)。

## 生成列的局限性

目前生成列有以下局限性：

- 不能通过 `ALTER TABLE` 增加存储生成列；
- 不能通过 `ALTER TABLE` 将存储生成列转换为普通列，也不能将普通列转换成存储生成列；
- 不能通过 `ALTER TABLE` 修改存储生成列的生成列表达式；
- 并未支持所有的 [JSON 函数](/functions-and-operators/json-functions.md)；
- 目前仅当生成列是虚拟生成列时索引生成列替换规则有效，暂不支持将表达式替换为存储生成列，但仍然可以通过直接使用该生成列本身来使用索引。

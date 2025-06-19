---
title: 生成列
summary: 了解如何使用生成列。
---

# 生成列

本文介绍生成列的概念和用法。

## 基本概念

与普通列不同，生成列的值是由列定义中的表达式计算得出的。在插入或更新生成列时，你不能为其赋值，只能使用 `DEFAULT`。

生成列有两种类型：虚拟生成列和存储生成列。虚拟生成列不占用存储空间，在读取时计算。存储生成列在写入（插入或更新）时计算，并占用存储空间。与虚拟生成列相比，存储生成列具有更好的读取性能，但会占用更多磁盘空间。

无论是虚拟生成列还是存储生成列，你都可以在其上创建索引。

## 用法

生成列的主要用途之一是从 JSON 数据类型中提取数据并为其建立索引。

在 MySQL 8.0 和 TiDB 中，JSON 类型的列不能直接创建索引。也就是说，以下表结构是**不支持的**：

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

要为 JSON 列创建索引，你必须先将其提取为生成列。

以 `address_info` 中的 `city` 字段为例，你可以创建一个虚拟生成列并为其添加索引：

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))), -- 虚拟生成列
    -- city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) VIRTUAL, -- 虚拟生成列
    -- city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) STORED, -- 存储生成列
    KEY (city)
);
```

在这个表中，`city` 列是一个**虚拟生成列**并且有一个索引。以下查询可以使用该索引来加速执行：

{{< copyable "sql" >}}

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT name, id FROM person WHERE city = 'Beijing';
```

```sql
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
| id                              | estRows | task      | access object                  | operator info                                               |
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
| Projection_4                    | 10.00   | root      |                                | test.person.name, test.person.id                            |
| └─IndexLookUp_10                | 10.00   | root      |                                |                                                             |
|   ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:person, index:city(city) | range:["Beijing","Beijing"], keep order:false, stats:pseudo |
|   └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:person                   | keep order:false, stats:pseudo                              |
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
```

从查询执行计划可以看出，使用了 `city` 索引来读取满足条件 `city ='Beijing'` 的行的 `HANDLE`，然后使用这个 `HANDLE` 来读取行的数据。

如果路径 `$.city` 处不存在数据，`JSON_EXTRACT` 返回 `NULL`。如果你想强制约束 `city` 必须为 `NOT NULL`，可以按如下方式定义虚拟生成列：

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

## 生成列的验证

`INSERT` 和 `UPDATE` 语句都会检查虚拟列定义。不通过验证的行会返回错误：

{{< copyable "sql" >}}

```sql
mysql> INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
ERROR 1048 (23000): Column 'city' cannot be null
```

## 生成列索引替换规则

当查询中的表达式与带有索引的生成列严格等价时，TiDB 会用相应的生成列替换该表达式，这样优化器在构建执行计划时就可以考虑使用该索引。

以下示例为表达式 `a+1` 创建生成列并添加索引。列 `a` 的类型为 int，`a+1` 的列类型为 bigint。如果将生成列的类型设置为 int，则不会发生替换。关于类型转换规则，请参见[表达式求值的类型转换](/functions-and-operators/type-conversion-in-expression-evaluation.md)。

```sql
create table t(a int);
desc select a+1 from t where a+1=3;
```

```sql
+---------------------------+----------+-----------+---------------+--------------------------------+
| id                        | estRows  | task      | access object | operator info                  |
+---------------------------+----------+-----------+---------------+--------------------------------+
| Projection_4              | 8000.00  | root      |               | plus(test.t.a, 1)->Column#3    |
| └─TableReader_7           | 8000.00  | root      |               | data:Selection_6               |
|   └─Selection_6           | 8000.00  | cop[tikv] |               | eq(plus(test.t.a, 1), 3)       |
|     └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+---------------------------+----------+-----------+---------------+--------------------------------+
4 rows in set (0.00 sec)
```

```sql
alter table t add column b bigint as (a+1) virtual;
alter table t add index idx_b(b);
desc select a+1 from t where a+1=3;
```

```sql
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
> 如果要替换的表达式和生成列都是字符串类型但长度不同，你可以通过将系统变量 [`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630) 设置为 `ON` 来实现替换。在配置此系统变量时，请确保生成列计算的值严格满足生成列的定义。否则，由于长度差异可能导致数据被截断，从而导致结果不正确。详见 GitHub issue [#35490](https://github.com/pingcap/tidb/issues/35490#issuecomment-1211658886)。

## 限制

JSON 和生成列当前的限制如下：

- 不能通过 `ALTER TABLE` 添加存储生成列。
- 不能通过 `ALTER TABLE` 语句将存储生成列转换为普通列，也不能将普通列转换为存储生成列。
- 不能通过 `ALTER TABLE` 语句修改存储生成列的表达式。
- 不是所有的 [JSON 函数](/functions-and-operators/json-functions.md)都支持。
- 不支持 [`NULLIF()` 函数](/functions-and-operators/control-flow-functions.md#nullif)。你可以使用 [`CASE` 函数](/functions-and-operators/control-flow-functions.md#case)代替。
- 目前，生成列索引替换规则仅在生成列是虚拟生成列时有效。对于存储生成列不生效，但可以通过直接使用生成列本身来使用索引。

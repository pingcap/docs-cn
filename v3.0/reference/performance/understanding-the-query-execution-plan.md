---
title: 理解 TiDB 执行计划
category: reference
aliases: ['/docs-cn/sql/understanding-the-query-execution-plan/']
---

# 理解 TiDB 执行计划

TiDB 优化器会根据当前数据表的实际情况来选择最优的执行计划，执行计划由一系列的算子构成。本文将详细解释 TiDB 中 `EXPLAIN` 语句返回的执行计划信息。

## 使用 `EXPLAIN` 来优化 SQL 语句

`EXPLAIN` 语句的返回结果提供了 TiDB 执行 SQL 查询的详细信息：

- `EXPLAIN` 可以和 `SELECT`，`DELETE` 语句一起使用；
- 执行 `EXPLAIN`，TiDB 会返回被 `EXPLAIN` 的 SQL 语句经过优化器后的最终物理执行计划。也就是说，`EXPLAIN` 展示了 TiDB 执行该 SQL 语句的完整信息，比如以什么样的顺序，什么方式 JOIN 两个表，表达式树长什么样等等。详见 [`EXPLAIN` 输出格式](#explain-输出格式)；
- TiDB 支持 `EXPLAIN [options] FOR CONNECTION connection_id`，但与 MySQL 的 `EXPLAIN FOR` 有一些区别，请参见 [`EXPLAIN FOR CONNECTION`](#explain-for-connection)。

通过观察 `EXPLAIN` 的结果，你可以知道如何给数据表添加索引使得执行计划使用索引从而加速 SQL 语句的执行速度；你也可以使用 `EXPLAIN` 来检查优化器是否选择了最优的顺序来 JOIN 数据表。

## `EXPLAIN` 输出格式

目前 TiDB 的 `EXPLAIN` 会输出 4 列，分别是：id，count，task，operator info。执行计划中每个算子都由这 4 列属性来描述，`EXPLAIN` 结果中每一行描述一个算子。每个属性的具体含义如下：

| 属性名          | 含义                                                                                                                                        |
|:----------------|:--------------------------------------------------------------------------------------------------------------------------------------------|
| id            | 算子的 ID，在整个执行计划中唯一的标识一个算子。在 TiDB 2.1 中，id 会格式化显示算子的树状结构。数据从 child 流向 parent，每个 算子的 parent 有且仅有一个。                                                                                       |
| count         | 预计当前算子将会输出的数据条数，基于统计信息以及算子的执行逻辑估算而来。                                                            |
| task          | 当前这个算子属于什么 task。目前的执行计划分成为两种 task，一种叫 **root** task，在 tidb-server 上执行，一种叫 **cop** task，并行的在 TiKV 上执行。当前的执行计划在 task 级别的拓扑关系是一个 root task 后面可以跟许多 cop task，root task 使用 cop task 的输出结果作为输入。cop task 中执行的也即是 TiDB 下推到 TiKV 上的任务，每个 cop task 分散在 TiKV 集群中，由多个进程共同执行。 |
| operator info | 每个算子的详细信息。各个算子的 operator info 各有不同，详见 [Operator Info](#operator-info)。                   |

## `EXPLAIN ANALYZE` 输出格式

作为 `EXPLAIN` 语句的扩展，`EXPLAIN ANALYZE` 语句执行查询并在 `execution info` 列中提供额外的执行统计信息。具体如下：

* `time` 显示从进入算子到离开算子的全部 wall time，包括所有子算子操作的全部执行时间。如果该算子被父算子多次调用 (`loops`)，这个时间就是累积的时间。
* `loops` 是当前算子被父算子的调用次数。
* `rows` 是当前算子返回的行的总数。例如，可以将 `count` 列的精度和 `execution_info` 列中的 `rows`/`loops` 值进行对比，据此评定查询优化器估算的精确度。

### 用例

使用 [bikeshare example database](https://github.com/pingcap/docs/blob/master/dev/how-to/get-started/import-example-database.md):

```
mysql> EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
+--------------------------+-------------+------+------------------------------------------------------------------------------------------------------------------------+
| id                       | count       | task | operator info                                                                                                          |
+--------------------------+-------------+------+------------------------------------------------------------------------------------------------------------------------+
| StreamAgg_20             | 1.00        | root | funcs:count(col_0)                                                                                                     |
| └─TableReader_21         | 1.00        | root | data:StreamAgg_9                                                                                                       |
|   └─StreamAgg_9          | 1.00        | cop  | funcs:count(1)                                                                                                         |
|     └─Selection_19       | 8166.73     | cop  | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) |
|       └─TableScan_18     | 19117643.00 | cop  | table:trips, range:[-inf,+inf], keep order:false                                                                       |
+--------------------------+-------------+------+------------------------------------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

在上面的例子中，coprocessor 上读取 `trips` 表上的数据（`TableScan_18`），寻找满足 `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` 条件的数据（`Selection_19`），然后计算满足条件的数据行数（`StreamAgg_9`），最后把结果返回给 TiDB。TiDB 汇总各个 coprocessor 返回的结果（`TableReader_21`），并进一步计算所有数据的行数（`StreamAgg_20`），最终把结果返回给客户端。在上面这个查询中，TiDB 根据 `trips` 表的统计信息估算出 `TableScan_18` 的输出结果行数为 19117643.00，满足条件 `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` 的有 `8166.73` 条，经过聚合运算后，只有 1 条结果。

上述查询中，虽然大部分计算逻辑都下推到了 TiKV 的 coprocessor 上，但是其执行效率还是不够高，可以添加适当的索引来消除 `TableScan_18` 对 `trips` 的全表扫，进一步加速查询的执行：

```sql
mysql> ALTER TABLE trips ADD INDEX (start_date);
..
mysql> EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
+------------------------+---------+------+--------------------------------------------------------------------------------------------------+
| id                     | count   | task | operator info                                                                                    |
+------------------------+---------+------+--------------------------------------------------------------------------------------------------+
| StreamAgg_25           | 1.00    | root | funcs:count(col_0)                                                                               |
| └─IndexReader_26       | 1.00    | root | index:StreamAgg_9                                                                                |
|   └─StreamAgg_9        | 1.00    | cop  | funcs:count(1)                                                                                   |
|     └─IndexScan_24     | 8166.73 | cop  | table:trips, index:start_date, range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false |
+------------------------+---------+------+--------------------------------------------------------------------------------------------------+
4 rows in set (0.01 sec)
```

在添加完索引后的新执行计划中，使用 `IndexScan_24` 直接读取满足条件 `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` 的数据，可以看到，估算的要扫描的数据行数从之前的 `19117643.00` 降到了现在的 `8166.73`。在测试环境中显示，这个查询的执行时间从 50.41 秒降到了 0.00 秒！

## `EXPLAIN FOR CONNECTION`

`EXPLAIN FOR CONNECTION` 用于获得一个连接中最后执行的查询的执行计划，其输出格式与 `EXPLAIN` 完全一致。但 TiDB 中的实现与 MySQL 不同，除了输出格式之外，还有以下区别：

- MySQL 返回的是**正在执行**的查询计划，而 TiDB 返回的是**最后执行**的查询计划。
- MySQL 的文档中指出，MySQL 要求登录用户与被查询的连接相同，或者拥有 `PROCESS` 权限，而 TiDB 则要求登录用户与被查询的连接相同，或者拥有 `SUPER` 权限。

## 概述

### Task 简介

目前 TiDB 的计算任务隶属于两种不同的 task：cop task 和 root task。cop task 是指使用 TiKV 中的 coprocessor 执行的计算任务，root task 是指在 TiDB 中执行的计算任务。

SQL 优化的目标之一是将计算尽可能地下推到 TiKV 中执行。TiKV 中的 coprocessor 能支持大部分 SQL 内建函数（包括聚合函数和标量函数）、SQL `LIMIT` 操作、索引扫描和表扫描。但是，所有的 Join 操作都只能作为 root task 在 TiDB 上执行。

### 表数据和索引数据

TiDB 的表数据是指一张表的原始数据，存放在 TiKV 中。对于每行表数据，它的 key 是一个 64 位整数，称为 Handle ID。如果一张表存在 int 类型的主键，TiDB 会把主键的值当作表数据的 Handle ID，否则由系统自动生成 Handle ID。表数据的 value 由这一行的所有数据编码而成。在读取表数据的时候，可以按照 Handle ID 递增的顺序返回。

TiDB 的索引数据和表数据一样，也存放在 TiKV 中。它的 key 是由索引列编码的有序 bytes，value 是这一行索引数据对应的 Handle ID，通过 Handle ID 可以读取这一行的非索引列。在读取索引数据的时候，TiKV 会按照索引列递增的顺序返回，如果有多个索引列，首先保证第 1 列递增，并且在第 i 列相等的情况下，保证第 i + 1 列递增。

### 范围查询

在 WHERE/HAVING/ON 条件中，TiDB 优化器会分析主键或索引键的查询返回。如数字、日期类型的比较符，如大于、小于、等于以及大于等于、小于等于，字符类型的 LIKE 符号等。

值得注意的是，TiDB 目前只支持比较符一端是列，另一端是常量，或可以计算成某一常量的情况，类似 `year(birth_day) < 1992` 的查询条件是不能利用索引的。还要注意应尽可能使用同一类型进行比较，以避免引入额外的 cast 操作而导致不能利用索引，如 `user_id = 123456`，如果 `user_id` 是字符串，需要将 `123456` 也写成字符串常量的形式。

针对同一列的范围查询条件使用 `AND` 和 `OR` 组合后，等于对范围求交集或者并集。对于多维组合索引，可以写多个列的条件。例如对组合索引`(a, b, c)`，当 a 为等值查询时，可以继续求 b 的查询范围，当 b 也为等值查询时，可以继续求 c 的查询范围，反之如果 a 为非等值查询，则只能求 a 的范围。

## Operator Info

### TableReader 和 TableScan

TableScan 表示在 KV 端对表数据进行扫描，TableReader 表示在 TiDB 端从 TiKV 端读取，属于同一功能的两个算子。table 表示 SQL 语句中的表名，如果表名被重命名，则显示重命名。range 表示扫描的数据范围，如果在查询中不指定 WHERE/HAVING/ON 条件，则会选择全表扫描，如果在 int 类型的主键上有范围查询条件，会选择范围查询。keep order 表示 table scan 是否按顺序返回。

### IndexReader 和 IndexLookUp

Index 在 TiDB 端的读取方式有两种：IndexReader 表示直接从索引中读取索引列，适用于 SQL 语句中仅引用了该索引相关的列或主键；IndexLookUp 表示从索引中过滤部分数据，仅返回这些数据的 Handle ID，通过 Handle ID 再次查找表数据，这种方式需要两次从 TiKV 获取数据。Index 的读取方式是由优化器自动选择的。

IndexScan 是 KV 端读取索引数据的算子，和 TableScan 功能类似。table 表示 SQL 语句中的表名，如果表名被重命名，则显示重命名。index 表示索引名。range 表示扫描的数据范围。out of order 表示 index scan 是否按照顺序返回。注意在 TiDB 中，多列或者非 int 列构成的主键是当作唯一索引处理的。

### Selection

Selection 表示 SQL 语句中的选择条件，通常出现在 WHERE/HAVING/ON 子句中。

### Projection

Projection 对应 SQL 语句中的 SELECT 列表，功能是将每一条输入数据映射成新的输出数据。

### Aggregation

Aggregation 对应 SQL 语句中的 Group By 语句或者没有 Group By 语句但是存在聚合函数，例如 count 或 sum 函数等。TiDB 支持两种聚合算法：Hash Aggregation 以及 Stream Aggregation（待补充）。Hash Aggregation 是基于哈希的聚合算法，如果 Hash Aggregation 紧邻 Table 或者 Index 的读取算子，则聚合算子会在 TiKV 端进行预聚合，以提高计算的并行度和减少网络开销。

### Join

TiDB 支持 Inner Join 以及 Left/Right Outer Join，并会自动将可以化简的外连接转换为 Inner Join。

TiDB 支持三种 Join 算法：Hash Join，Sort Merge Join 和 Index Look up Join。Hash Join 的原理是将参与连接的小表预先装载到内存中，读取大表的所有数据进行连接。Sort Merge Join 会利用输入数据的有序信息，同时读取两张表的数据并依次进行比较。Index Look Up Join 会读取外表的数据，并对内表进行主键或索引键查询。

### Apply

Apply 是 TiDB 用来描述子查询的一种算子，行为类似于 Nested Loop，即每次从外表中取一条数据，带入到内表的关联列中，并执行，最后根据 Apply 内联的 Join 算法进行连接计算。

值得注意的是，Apply 一般会被查询优化器自动转换为 Join 操作。用户在编写 SQL 的过程中应尽量避免 Apply 算子的出现。

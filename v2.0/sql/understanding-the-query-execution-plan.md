---
title: 理解 TiDB 执行计划
category: user guide
---

# 理解 TiDB 执行计划

TiDB 优化器会根据当前数据表的实际情况来选择最优的执行计划，执行计划由一系列的 operator 构成，这里我们详细解释一下 TiDB 中 `EXPLAIN` 语句返回的执行计划信息。

## 使用 `EXPLAIN` 来优化 SQL 语句

`EXPLAIN` 语句的返回结果提供了 TiDB 执行 SQL 查询的详细信息：

- `EXPLAIN` 可以和 `SELECT`, `DELETE`, `INSERT`, `REPLACE`, 以及 `UPDATE` 语句一起使用；
- 执行 `EXPLAIN`，TiDB 会返回被 `EXPLAIN` 的 SQL 语句经过优化器后的最终物理执行计划。也就是说，`EXPLAIN` 展示了 TiDB 执行该 SQL 语句的完整信息，比如以什么样的顺序，什么方式 JOIN 两个表，表达式树长什么样等等。详细请看 [`EXPLAIN` 输出格式](#explain-output-format)；
- TiDB 目前还不支持 `EXPLAIN [options] FOR CONNECTION connection_id`，我们将在未来支持它，详细请看：[#4351](https://github.com/pingcap/tidb/issues/4351)；

通过观察 `EXPLAIN` 的结果，你可以知道如何给数据表添加索引使得执行计划使用索引从而加速 SQL 语句的执行速度；你也可以使用 `EXPLAIN` 来检查优化器是否选择了最优的顺序来 JOIN 数据表。

## <span id="explain-output-format">`EXPLAIN` 输出格式</span>

目前 TiDB 的 `EXPLAIN` 会输出 6 列，分别是：id，parents，children，task，operator info 和 count，执行计划中每个 operator 都由这 6 列属性来描述，`EXPLAIN` 结果中每一行描述一个 operator。下面详细解释每个属性的含义：

| 属性名          | 含义                                                                                                                                        |
|:----------------|:--------------------------------------------------------------------------------------------------------------------------------------------|
| id            | operator 的 id，在整个执行计划中唯一的标识一个 operator                                                                                       |
| parents       | 这个 operator 的 parent。目前的执行计划可以看做是一个 operator 构成的树状结构，数据从 child 流向 parent，每个 operator 的 parent 有且仅有一个 |
| children      | 这个 operator 的 children，也即是这个 operator 的数据来源                                                                                     |
| task          | 当前这个 operator 属于什么 task。目前的执行计划分成为两种 task，一种叫 **root** task，在 tidb-server 上执行，一种叫 **cop** task，并行的在 tikv 上执行。当前的执行计划在 task 级别的拓扑关系是一个 root task 后面可以跟许多 cop task，root task 使用 cop task 的输出结果作为输入。cop task 中执行的也即是 tidb 下推到 tikv 上的任务，每个 cop task 分散在 tikv 集群中，由多个进程共同执行 |
| operator info | 每个 operator 的详细信息。各个 operator 的 operator info 各有不同，我们将在 [Operator Info](#operator-info) 中详细介绍                   |
| count         | 预计当前 operator 将会输出的数据条数，基于统计信息以及 operator 的执行逻辑估算而来                                                            |

## 概述

### Task 简介

目前 TiDB 的计算任务隶属于两种不同的 task：cop task 和 root task。cop task 是指使用 TiKV 中的 coprocessor 执行的计算任务，root task 是指在 TiDB 中执行的计算任务。

SQL 优化的目标之一是将计算尽可能地下推到 TiKV 中执行。TiKV 中的 coprocessor 能支持大部分 SQL 内建函数（包括聚合函数和标量函数）、SQL `LIMIT` 操作、索引扫描和表扫描。但是，所有的 Join 操作都只能作为 root task 在 TiDB 上执行。

### 表数据和索引数据

TiDB 的表数据是指一张表的原始数据，存放在 TiKV 中。对于每行表数据，它的 key 是一个 64 位整数，称为 Handle ID。如果一张表存在 int 类型的主键，我们会把主键的值当作表数据的 Handle ID，否则由系统自动生成 Handle ID。表数据的 value 由这一行的所有数据编码而成。在读取表数据的时候，我们可以按照 Handle ID 递增的顺序返回。

TiDB 的索引数据和表数据一样，也存放在 TiKV 中。它的 key 是由索引列编码的有序 bytes，value 是这一行索引数据对应的 Handle ID，通过 Handle ID 我们可以读取这一行的非索引列。在读取索引数据的时候，我们按照索引列递增的顺序返回，如果有多个索引列，我们首先保证第 1 列递增，并且在第 i 列相等的情况下，保证第 i + 1 列递增。

### 范围查询

在 WHERE/HAVING/ON 条件中，我们会分析主键或索引键的查询返回。如数字、日期类型的比较符，如大于、小于、等于以及大于等于、小于等于，字符类型的 LIKE 符号等。
值得注意的是，我们只支持比较符一端是列，另一端是常量，或可以计算成某一常量的情况，类似 `year(birth_day) < 1992` 的查询条件是不能利用索引的。还要注意应尽可能使用同一类型进行比较，以避免引入额外的 cast 操作而导致不能利用索引，如 `user_id = 123456`，如果 `user_id` 是字符串，需要将 `123456` 也写成字符串常量的形式。
针对同一列的范围查询条件使用 `AND` 和 `OR` 组合后，等于对范围求交集或者并集。对于多维组合索引，我们可以写多个列的条件。例如对组合索引`(a, b, c)`，当 a 为等值查询时，可以继续求 b 的查询范围，当 b 也为等值查询时，可以继续求 c 的查询范围，反之如果 a 为非等值查询，则只能求 a 的范围。

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

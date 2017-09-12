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

## <span id="operator-info">概述</span>

### Task 简介

目前 TiDB 的计算任务隶属于两种不同的 task: cop task 和 root task。cop task 是指被下推到 KV 端分布式执行的计算任务，root task 是指在 TiDB 端单点执行的计算任务。SQL 优化的目标之一是将计算尽可能的下推到 KV 端执行。

### 表数据和索引数据

TiDB 的表数据是指一张表的原始数据，存放在 TiKV 中。对于每行表数据，它的 key 是一个64位整数，称为 handle id。如果一张表存在 int 类型的主键，我们会把主键的值当作表数据的 handle id，否则由系统自动生成 handle id。表数据的 value 由这一行的所有数据编码而成。在读取表数据的时候，我们可以按照 handle id 递增的顺序返回。

TiDB 的索引数据和表数据一样，也存放在 TiKV 中。它的 key 是由索引列编码的有序 bytes，value 是这一行索引数据对应的 handle id，通过 handle id 我们可以读取这一行的非索引列。在读取索引数据的时候，我们按照索引列递增的顺序返回，如果有多个索引列，我们首先保证第 1 列递增，并且在第 i 列相等的情况下，保证第 i + 1 列递增。

### 范围查询

在 WHERE/HAVING/ON 条件中，我们会分析主键或索引键的查询返回。如数字、日期类型的比较符，如大于、小于、等于以及大于等于、小于等于，字符类型的 Like 符号等。
值得注意的是，我们只支持比较符一端是列，另一端是常量，或可以计算成某一常量的情况，类似 `year(birth_day) < 1992` 的查询条件是不能利用索引的。还要注意应尽可能使用同一类型进行比较，以避免引入额外的 cast 操作而导致不能利用索引，如 `user_id = 123456`，如果 `user_id` 是字符串，需要将 `123456` 也写成字符串常量的形式。
针对同一列的范围查询条件使用 `AND` 和 `OR` 组合后，等于对范围求交集或者并集。对于多维组合索引，我们可以写多个列的条件。例如对组合索引`(a, b, c)`，当 a 为等值查询时，可以继续求 b 的查询范围，当 b 也为等值查询时，可以继续求 c 的查询范围，反之如果 a 为非等值查询，则只能求 a 的范围。

## <span id="operator-info">Operator Info</span>

### TableScan

TableScan 表示在 KV 端对表数据进行扫描。table 表示它在 SQL 语句中的表名，如果表名被重命名，则显示重命名。range 表示扫描的数据范围，如果在查询中不指定 WHERE/HAVING/ON 条件，则会选择全表扫描，如果在 int 类型的主键上有范围查询条件，会选择范围查询。keep order 表示 table scan 是否按顺序返回。

### IndexReader 和 IndexLookUp

### Selection

### Projection

### TableDual

### Union

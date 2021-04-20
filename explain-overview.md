---
title: EXPLAIN 概览
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划。
---

# `EXPLAIN` 概览

> **注意：**
>
> 使用 MySQL 客户端连接到 TiDB 时，为避免输出结果在终端中换行，可先执行 `pager less -S` 命令。执行命令后，新的 `EXPLAIN` 的输出结果不再换行，可按右箭头 <kbd>→</kbd> 键水平滚动阅读输出结果。

TiDB 优化器会根据当前数据表的最新的统计信息来选择最优的执行计划，执行计划由一系列的算子构成。本文将详细解释 TiDB 中的执行计划。

## `EXPLAIN` 简介

TiDB 中可以使用 `EXPLAIN` 命令来查看执行计划，`EXPLAIN` 语句的返回结果提供了 TiDB 执行 SQL 查询的详细信息：

- `EXPLAIN` 可以和 `SELECT`，`DELETE` 等语句一起使用；
- 执行 `EXPLAIN`，TiDB 会返回被 `EXPLAIN` 的 SQL 语句经过优化器后的最终物理执行计划。也就是说，`EXPLAIN` 展示了 TiDB 执行该 SQL 语句的完整信息，比如以什么样的顺序，什么方式 JOIN 两个表，表达式树长什么样等等。
- 关于 `EXPLAIN` 每列的简述，可以参见 [EXPLAIN 输出格式](/sql-statements/sql-statement-explain.md)。

通过观察 `EXPLAIN` 的结果，你可以知道如何给数据表添加索引使得执行计划使用索引从而加速 SQL 语句的执行速度；你也可以使用 `EXPLAIN` 来检查优化器是否选择了最优的顺序来 JOIN 数据表。

### 算子的执行顺序

TiDB 的执行计划是一个树形结构，树中每个节点即是算子。考虑到每个算子内多线程并发执行的情况，在一条 SQL 执行的过程中，如果能够有一个手术刀把这棵树切开看看，大家可能会发现所有的算子都正在消耗 CPU 和内存处理数据，从这个角度来看，算子是没有执行顺序的。

但是如果从一行数据先后被哪些算子处理的角度来看，一条数据在算子上的执行是有顺序的。这个顺序可以通过下面这个规则简单总结出来：

**Build 总是先于 Probe 执行，并且 Build 总是出现在 Probe 前面。**

这个原则的前半句是说：如果一个算子有多个孩子节点，孩子节点 ID 后面有 Build 关键字的算子总是先于有 Probe 关键字的算子执行。后半句是说：TiDB 在展现执行计划的时候，Build 端总是第一个出现，接着才是 Probe 端。

一些例子：

```
TiDB(root@127.0.0.1:test) > explain select * from t use index(idx_a) where a = 1;
+-------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                            | estRows | task      | access object           | operator info                               |
+-------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexLookUp_7                 | 10.00   | root      |                         |                                             |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t, index:idx_a(a) | range:[1,1], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 10.00   | cop[tikv] | table:t                 | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+-------------------------+---------------------------------------------+
3 rows in set (0.00 sec)
```

这里 `IndexLookUp_7` 算子有两个孩子节点：`IndexRangeScan_5(Build)` 和 `TableRowIDScan_6(Probe)`。可以看到，`IndexRangeScan_5(Build)` 是第一个出现的，并且基于上面这条规则，要得到一条数据，需要先执行 `IndexRangeScan_5(Build)` 得到一个 RowID 以后，再由 `TableRowIDScan_6(Probe)` 根据前者读上来的 RowID 去获取完整的一行数据。

这种规则隐含的另一个信息是：在同一层级的节点中，出现在最前面的算子可能是最先被执行的，而出现在最末尾的算子可能是最后被执行的。比如下面这个例子：

```
TiDB(root@127.0.0.1:test) > explain select * from t t1 use index(idx_a) join t t2 use index() where t1.a = t2.a;
+----------------------------------+----------+-----------+--------------------------+------------------------------------------------------------------+
| id                               | estRows  | task      | access object            | operator info                                                    |
+----------------------------------+----------+-----------+--------------------------+------------------------------------------------------------------+
| HashJoin_22                      | 12487.50 | root      |                          | inner join, inner:TableReader_26, equal:[eq(test.t.a, test.t.a)] |
| ├─TableReader_26(Build)          | 9990.00  | root      |                          | data:Selection_25                                                |
| │ └─Selection_25                 | 9990.00  | cop[tikv] |                          | not(isnull(test.t.a))                                            |
| │   └─TableFullScan_24           | 10000.00 | cop[tikv] | table:t2                 | keep order:false, stats:pseudo                                   |
| └─IndexLookUp_29(Probe)          | 9990.00  | root      |                          |                                                                  |
|   ├─IndexFullScan_27(Build)      | 9990.00  | cop[tikv] | table:t1, index:idx_a(a) | keep order:false, stats:pseudo                                   |
|   └─TableRowIDScan_28(Probe)     | 9990.00  | cop[tikv] | table:t1                 | keep order:false, stats:pseudo                                   |
+----------------------------------+----------+-----------+--------------------------+------------------------------------------------------------------+
7 rows in set (0.00 sec)
```

要完成 `HashJoin_22`，需要先执行 `TableReader_26(Build)` 再执行 `IndexLookUp_29(Probe)`。而在执行 `IndexLookUp_29(Probe)` 的时候，又需要先执行 `IndexFullScan_27(Build)` 再执行 `TableRowIDScan_28(Probe)`。所以从整条执行链路来看，`TableRowIDScan_28(Probe)` 是最后被唤起执行的。

### Task 简介

目前 TiDB 的计算任务隶属于两种不同的 task：cop task 和 root task。cop task 是指使用 TiKV 中的 coprocessor 执行的计算任务，root task 是指在 TiDB 中执行的计算任务。

SQL 优化的目标之一是将计算尽可能地下推到 TiKV 中执行。TiKV 中的 coprocessor 能支持大部分 SQL 内建函数（包括聚合函数和标量函数）、SQL `LIMIT` 操作、索引扫描和表扫描。但是，所有的 Join 操作都只能作为 root task 在 TiDB 上执行。

### Access Object 简介

算子所访问的数据项信息。包括表 `table`，表分区 `partition` 以及使用的索引 `index`（如果有）。只有直接访问数据的算子才拥有这些信息。

### 范围查询

在 WHERE/HAVING/ON 条件中，TiDB 优化器会分析主键或索引键的查询返回。如数字、日期类型的比较符，如大于、小于、等于以及大于等于、小于等于，字符类型的 LIKE 符号等。

值得注意的是，TiDB 目前只支持比较符一端是列，另一端是常量，或可以计算成某一常量的情况，类似 `year(birth_day) < 1992` 的查询条件是不能利用索引的。还要注意应尽可能使用同一类型进行比较，以避免引入额外的 cast 操作而导致不能利用索引，如 `user_id = 123456`，如果 user_id 是字符串，需要将 123456 也写成字符串常量的形式。

针对同一列的范围查询条件使用 AND 和 OR 组合后，等于对范围求交集或者并集。对于多维组合索引，可以写多个列的条件。例如对组合索引 (a, b, c)，当 a 为等值查询时，可以继续求 b 的查询范围，当 b 也为等值查询时，可以继续求 c 的查询范围；反之，如果 a 为非等值查询，则只能求 a 的范围。

## 算子信息

不同的算子在 explain 时输出的信息各有不同，接下来这部分将会讲述如何阅读各种扫表、聚合、连接算子的执行计划。

可以使用优化器提示来控制优化器的行为，以此控制物理算子的选择，如使用 `/*+ HASH_JOIN(t1, t2) */` 来提示优化器使用 Hash Join 算法，详见[优化器提示](/optimizer-hints.md)。

如果读者想要详细了解各算子的内部实现，可以参见[源码阅读系列](https://pingcap.com/blog-cn/#TiDB-源码阅读)。

### 如何阅读扫表的执行计划

真正执行扫表（读盘或者读 TiKV Block Cache）操作的算子有如下几类：

- **TableFullScan**：这是大家所熟知的 “全表扫” 操作
- **TableRangeScan**：带有范围的表数据扫描操作
- **TableRowIDScan**：根据上层传递下来的 RowID 精确地扫描表数据
- **IndexFullScan**：另一种“全表扫”，只不过这里扫的是索引数据，不是表数据
- **IndexRangeScan**：带有范围的索引数据扫描操作

TiDB 会汇聚 TiKV/TiFlash 上扫描的数据或者计算结果，这种“数据汇聚”算子目前有如下几类：

- **TableReader**：将 TiKV 上底层扫表算子 TableFullScan 或 TableRangeScan 得到的数据进行汇总。
- **IndexReader**：将 TiKV 上底层扫表算子 IndexFullScan 或 IndexRangeScan 得到的数据进行汇总。
- **IndexLookUp**：先汇总 Build 端 TiKV 扫描上来的 RowID，再去 Probe 端上根据这些 RowID 精确地读取 TiKV 上的数据。Build 端是 IndexFullScan 或 IndexRangeScan 类型的算子，Probe 端是 TableRowIDScan 类型的算子。
- **IndexMerge**：和 IndexLookupReader 类似，可以看做是它的扩展，可以同时读取多个索引的数据，有多个 Build 端，一个 Probe 端。执行过程也很类似，先汇总所有 Build 端 TiKV 扫描上来的 RowID，再去 Probe 端上根据这些 RowID 精确地读取 TiKV 上的数据。Build 端是 IndexFullScan 或 IndexRangeScan 类型的算子，Probe 端是 TableRowIDScan 类型的算子。

#### 表数据和索引数据

TiDB 的表数据是指一张表的原始数据，存放在 TiKV 中。对于每行表数据，它的 key 是一个 64 位整数，称为 RowID。如果一张表存在 int 类型的主键，TiDB 会把主键的值当作表数据的 RowID，否则由系统自动生成 RowID。表数据的 value 由这一行的所有数据编码而成。在读取表数据的时候，可以按照 RowID 递增的顺序返回。

TiDB 的索引数据和表数据一样，也存放在 TiKV 中。它的 key 是由索引列编码的有序 bytes，value 是这一行索引数据对应的 RowID，通过 RowID 可以读取这一行的非索引列。在读取索引数据的时候，TiKV 会按照索引列递增的顺序返回，如果有多个索引列，首先保证第 1 列递增，并且在第 i 列相等的情况下，保证第 i + 1 列递增。

#### IndexLookUp 示例

```
mysql> explain select * from t use index(idx_a);
+-------------------------------+----------+-----------+-------------------------+--------------------------------+
| id                            | estRows  | task      | access object           | operator info                  |
+-------------------------------+----------+-----------+-------------------------+--------------------------------+
| IndexLookUp_6                 | 10000.00 | root      |                         |                                |
| ├─IndexFullScan_4(Build)      | 10000.00 | cop[tikv] | table:t, index:idx_a(a) | keep order:false, stats:pseudo |
| └─TableRowIDScan_5(Probe)     | 10000.00 | cop[tikv] | table:t                 | keep order:false, stats:pseudo |
+-------------------------------+----------+-----------+-------------------------+--------------------------------+
3 rows in set (0.00 sec)
```

这里 `IndexLookUp_6` 算子有两个孩子节点：`IndexFullScan_4(Build)` 和 `TableRowIDScan_5(Probe)`。可以看到，`IndexFullScan_4(Build)` 执行索引全表扫，扫描索引 a 的所有数据，因为是全范围扫，这个操作将获得表中所有数据的 RowID，之后再由 `TableRowIDScan_5(Probe)` 根据这些 RowID 去扫描所有的表数据。可以预见的是，这个执行计划不如直接使用 TableReader 进行全表扫，因为同样都是全表扫，这里的 IndexLookUp 多扫了一次索引，带来了额外的开销。

其中对于扫表操作来说，explain 表中的 operator info 列记录了读到的数据是否是有序的，如上面例子 `IndexFullScan` 算子中的 `keep order:false` 表示读到的数据是无序的。而 operator info 中的 `stats:pseudo` 表示可能因为没有统计信息，或者统计信息过旧，不会用统计信息来进行估算。对于其他扫表操作来说，operator info 所含有的信息类似。

#### TableReader 示例

```
mysql> explain select * from t where a > 1 or b >100;
+-------------------------+----------+-----------+---------------+----------------------------------------+
| id                      | estRows  | task      | access object | operator info                          |
+-------------------------+----------+-----------+---------------+----------------------------------------+
| TableReader_7           | 8000.00  | root      |               | data:Selection_6                       |
| └─Selection_6           | 8000.00  | cop[tikv] |               | or(gt(test.t.a, 1), gt(test.t.b, 100)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo         |
+-------------------------+----------+-----------+---------------+----------------------------------------+
3 rows in set (0.00 sec)
```

在上面例子中 `TableReader_7` 算子的孩子节点是 `Selection_6`。以这个孩子节点为根的子树被当做了一个 `Cop Task` 下发给了相应的 TiKV，这个 Cop Task 使用 `TableFullScan_5` 算子执行扫表操作。`Selection` 表示 SQL 语句中的选择条件，可能来自 SQL 语句中的 `WHERE`/`HAVING`/`ON` 子句。由 `TableFullScan_5` 可以看到，这个执行计划使用了一个全表扫描的操作，集群的负载将因此而上升，可能会影响到集群中正在运行的其他查询。这时候如果能够建立合适的索引，并且使用 IndexMerge 算子，将能够极大的提升查询的性能，降低集群的负载。

#### IndexMerge 示例

`IndexMerge` 是 TiDB v4.0 中引入的一种对表的新访问方式。在这种访问方式下，TiDB 优化器可以选择对一张表使用多个索引，并将每个索引的返回结果进行合并。在某些场景下，这种访问方式能够减少大量不必要的数据扫描，提升查询的执行效率。

```
mysql> explain select * from t where a = 1 or b = 1;
+-------------------------+----------+-----------+---------------+--------------------------------------+
| id                      | estRows  | task      | access object | operator info                        |
+-------------------------+----------+-----------+---------------+--------------------------------------+
| TableReader_7           | 8000.00  | root      |               | data:Selection_6                     |
| └─Selection_6           | 8000.00  | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+----------+-----------+---------------+--------------------------------------+
mysql> set @@tidb_enable_index_merge = 1;
mysql> explain select * from t use index(idx_a, idx_b) where a > 1 or b > 1;
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                             | estRows | task      | access object           | operator info                                  |
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_16                  | 6666.67 | root      |                         |                                                |
| ├─IndexRangeScan_13(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_14(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_15(Probe)     | 6666.67 | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

例如，在上述示例中，过滤条件是使用 `OR` 条件连接的 `WHERE` 子句。在启用 `IndexMerge` 前，每个表只能使用一个索引，不能将 `a = 1` 下推到索引 `a`，也不能将 `b = 1` 下推到索引 `b`。当 `t` 中存在大量数据时，全表扫描的效率会很低。针对这类场景，TiDB 引入了对表的新访问方式 `IndexMerge`。

在 `IndexMerge` 访问方式下，优化器可以选择对一张表使用多个索引，并将每个索引的返回结果进行合并，生成以上示例中后一个 `IndexMerge` 的执行计划。此时的 `IndexMerge_16` 算子有三个子节点，其中 `IndexRangeScan_13` 和 `IndexRangeScan_14` 根据范围扫描得到符合条件的所有 `RowID`，再由 `TableRowIDScan_15` 算子根据这些 `RowID` 精确地读取所有满足条件的数据。

其中对于 `IndexRangeScan`/`TableRangeScan` 一类按范围进行的扫表操作，`EXPLAIN` 表中 `operator info` 列相比于其他扫表操作，多了被扫描数据的范围这一信息。比如上面的例子中，`IndexRangeScan_13` 算子中的 `range:(1,+inf]` 这一信息表示该算子扫描了从 `1` 到正无穷这个范围的数据。

> **注意：**
>
> 目前，TiDB 的 `IndexMerge` 特性在 TiDB 4.0.0-rc.1 版本中默认关闭。同时 4.0 版本中的 `IndexMerge` 目前支持的场景仅限于析取范式（`or` 连接的表达式），暂不支持合取范式（`and` 连接的表达式）。开启 `IndexMerge` 特性有以下方法：
>
> - 设置系统变量 `tidb_enable_index_merge` 为 1
> - 在查询中使用 SQL Hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)
>
> SQL Hint 的优先级高于系统变量。

### 如何阅读聚合的执行计划

TiDB 的聚合算法包括如下两类：

- Hash Aggregate
- Stream Aggregate

#### Hash Aggregate 示例

TiDB 上的 Hash Aggregation 算子采用多线程并发优化，执行速度快，但会消耗较多内存。下面是一个 Hash Aggregate 的例子：

```
TiDB(root@127.0.0.1:test) > explain select /*+ HASH_AGG() */ count(*) from t;
+---------------------------+----------+-----------+---------------+---------------------------------+
| id                        | estRows  | task      | access object | operator info                   |
+---------------------------+----------+-----------+---------------+---------------------------------+
| HashAgg_11                | 1.00     | root      |               | funcs:count(Column#7)->Column#4 |
| └─TableReader_12          | 1.00     | root      |               | data:HashAgg_5                  |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | funcs:count(1)->Column#7        |
|     └─TableFullScan_8     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo  |
+---------------------------+----------+-----------+---------------+---------------------------------+
4 rows in set (0.00 sec)
```

一般而言 TiDB 的 Hash Aggregate 会分成两个阶段执行，一个在 TiKV/TiFlash 的 Coprocessor 上，在扫表算子读取数据时计算聚合函数的中间结果。另一个在 TiDB 层，汇总所有 Coprocessor Task 的中间结果后，得到最终结果。其中 explain 表中的 operator info 列还记录了 Hash Aggregation 的其他信息，我们需要关注的信息是 Aggregation 所使用的聚合函数是什么。如在上面的例子中，Hash Aggregation 算子的 operator info 中的内容为 `funcs:count(Column#7)->Column#4`，我们可以得到 Hash Aggregation 使用了聚合函数 `count` 进行计算。下面例子中 Stream Aggregation 算子中 operator info 所表示的信息和此处相同。

#### Stream Aggregate 示例

TiDB Stream Aggregation 算子通常会比 Hash Aggregate 占用更少的内存，有些场景中也会比 Hash Aggregate 执行得更快。当数据量太大或者系统内存不足时，可以试试 Stream Aggregate 算子。一个 Stream Aggregate 的例子如下：

```
TiDB(root@127.0.0.1:test) > explain select /*+ STREAM_AGG() */ count(*) from t;
+----------------------------+----------+-----------+---------------+---------------------------------+
| id                         | estRows  | task      | access object | operator info                   |
+----------------------------+----------+-----------+---------------+---------------------------------+
| StreamAgg_16               | 1.00     | root      |               | funcs:count(Column#7)->Column#4 |
| └─TableReader_17           | 1.00     | root      |               | data:StreamAgg_8                |
|   └─StreamAgg_8            | 1.00     | cop[tikv] |               | funcs:count(1)->Column#7        |
|     └─TableFullScan_13     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo  |
+----------------------------+----------+-----------+---------------+---------------------------------+
4 rows in set (0.00 sec)
```

和 Hash Aggregate 类似，一般而言 TiDB 的 Stream Aggregate 也会分成两个阶段执行，一个在 TiKV/TiFlash 的 Coprocessor 上，在扫表算子读取数据时计算聚合函数的中间结果。另一个在 TiDB 层，汇总所有 Coprocessor Task 的中间结果后，得到最终结果。

### 如何阅读 Join 的执行计划

TiDB 的 Join 算法包括如下几类：

- Hash Join
- Merge Join
- Index Join (Index Nested Loop Join)
- Index Hash Join (Index Nested Loop Hash Join)

下面分别通过一些例子来解释这些 Join 算法的执行过程。

#### Hash Join 示例

TiDB 的 Hash Join 算子采用了多线程优化，执行速度较快，但会消耗较多内存。一个 Hash Join 的例子如下：

```
mysql> EXPLAIN SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
+-----------------------------+----------+-----------+------------------------+------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                  |
+-----------------------------+----------+-----------+------------------------+------------------------------------------------+
| HashJoin_30                 | 12487.50 | root      |                        | inner join, equal:[eq(test.t1.id, test.t2.id)] |
| ├─IndexReader_35(Build)     | 9990.00  | root      |                        | index:IndexFullScan_34                         |
| │ └─IndexFullScan_34        | 9990.00  | cop[tikv] | table:t2, index:id(id) | keep order:false, stats:pseudo                 |
| └─IndexReader_33(Probe)     | 9990.00  | root      |                        | index:IndexFullScan_32                         |
|   └─IndexFullScan_32        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                 |
+-----------------------------+----------+-----------+------------------------+------------------------------------------------+
5 rows in set (0.01 sec)
```

Hash Join 会将 Build 端的数据缓存在内存中，根据这些数据构造出一个 Hash Table，然后读取 Probe 端的数据，用 Probe 端的数据去探测 Build 端构造出来的 Hash Table，将符合条件的数据返回给用户。其中 explain 表中的 operator info 列还记录了 Hash Join 的其他信息，包括查询是 Inner Join 还是 Outer Join，Join 的条件是什么。如在上面的例子中，该查询是一个 Inner Join，其中 Join 的条件 `equal:[eq(test.t1.id, test.t2.id)]` 和查询语句中 `where t1.id = t2.id` 部分对应。下面例子中其他几个 Join 算子的 operator info 和此处类似。

#### Merge Join 示例

TiDB 的 Merge Join 算子相比于 Hash Join 通常会占用更少的内存，但可能执行时间会更久。当数据量太大，或系统内存不足时，建议尝试使用。下面是一个 Merge Join 的例子：

```
mysql> EXPLAIN SELECT /*+ MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                         |
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------+
| MergeJoin_7                 | 12487.50 | root      |                        | inner join, left key:test.t1.id, right key:test.t2.id |
| ├─IndexReader_12(Build)     | 9990.00  | root      |                        | index:IndexFullScan_11                                |
| │ └─IndexFullScan_11        | 9990.00  | cop[tikv] | table:t2, index:id(id) | keep order:true, stats:pseudo                         |
| └─IndexReader_10(Probe)     | 9990.00  | root      |                        | index:IndexFullScan_9                                 |
|   └─IndexFullScan_9         | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:true, stats:pseudo                         |
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------+
5 rows in set (0.01 sec)
```

Merge Join 算子在执行时，会从 Build 端把一个 Join Group 的数据全部读取到内存中，接着再去读 Probe 端的数据，用 Probe 端的每行数据去和 Build 端的一个完整 Join Group 比较，依次查看是否匹配（除了满足等值条件以外，还有其他非等值条件，这里的 “匹配” 主要是指查看是否满足非等值条件）。Join Group 指的是所有 Join Key 上值相同的数据。

#### Index Join 示例

对于外表经过 WHERE 条件过滤后结果集较小（小于 1 万行）的场景，可以尝试使用这个算法。

```
mysql> EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                                                  |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| IndexJoin_11                | 12487.50 | root      |                        | inner join, inner:IndexReader_10, outer key:test.t1.id, inner key:test.t2.id   |
| ├─IndexReader_31(Build)     | 9990.00  | root      |                        | index:IndexFullScan_30                                                         |
| │ └─IndexFullScan_30        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                                                 |
| └─IndexReader_10(Probe)     | 1.00     | root      |                        | index:Selection_9                                                              |
|   └─Selection_9             | 1.00     | cop[tikv] |                        | not(isnull(test.t2.id))                                                        |
|     └─IndexRangeScan_8      | 1.00     | cop[tikv] | table:t2, index:id(id) | range: decided by [eq(test.t2.id, test.t1.id)], keep order:false, stats:pseudo |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

#### Index Hash Join 示例

该算法与 Index Join 使用条件完全一样，但在某些场景下会更为节省内存资源。

```
mysql> EXPLAIN SELECT /*+ INL_HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                                                  |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| IndexHashJoin_18            | 12487.50 | root      |                        | inner join, inner:IndexReader_10, outer key:test.t1.id, inner key:test.t2.id   |
| ├─IndexReader_31(Build)     | 9990.00  | root      |                        | index:IndexFullScan_30                                                         |
| │ └─IndexFullScan_30        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                                                 |
| └─IndexReader_10(Probe)     | 1.00     | root      |                        | index:Selection_9                                                              |
|   └─Selection_9             | 1.00     | cop[tikv] |                        | not(isnull(test.t2.id))                                                        |
|     └─IndexRangeScan_8      | 1.00     | cop[tikv] | table:t2, index:id(id) | range: decided by [eq(test.t2.id, test.t1.id)], keep order:false, stats:pseudo |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

## 优化实例

使用 [bikeshare example database](https://github.com/pingcap/docs/blob/master/import-example-data.md):

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows  | task      | access object | operator info                                                                                                          |
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| StreamAgg_20                 | 1.00        | root      |               | funcs:count(Column#13)->Column#11                                                                                      |
| └─TableReader_21             | 1.00        | root      |               | data:StreamAgg_9                                                                                                       |
|   └─StreamAgg_9              | 1.00        | cop[tikv] |               | funcs:count(1)->Column#13                                                                                              |
|     └─Selection_19           | 8166.73     | cop[tikv] |               | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) |
|       └─TableFullScan_18     | 19117643.00 | cop[tikv] | table:trips   | keep order:false, stats:pseudo                                                                                         |
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
```

在上面的例子中，coprocessor 上读取 trips 表上的数据 (`TableScan_18`)，寻找满足 `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` 条件的数据 (`Selection_19`)，然后计算满足条件的数据行数 (`StreamAgg_9`)，最后把结果返回给 TiDB。TiDB 汇总各个 coprocessor 返回的结果 (`TableReader_21`)，并进一步计算所有数据的行数 (`StreamAgg_20`)，最终把结果返回给客户端。在上面这个查询中，TiDB 根据 `trips` 表的统计信息估算出 `TableScan_18` 的输出结果行数为 19117643.00，满足条件 `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` 的有 8166.73 条，经过聚合运算后，只有 1 条结果。

上述查询中，虽然大部分计算逻辑都下推到了 TiKV 的 coprocessor 上，但是其执行效率还是不够高，可以添加适当的索引来消除 `TableScan_18` 对 trips 的全表扫，进一步加速查询的执行：

{{< copyable "sql" >}}

```sql
ALTER TABLE trips ADD INDEX (start_date);
```

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```
+-----------------------------+---------+-----------+-------------------------------------------+---------------------------------------------------------------------------------+
| id                          | estRows | task      | access object                             | operator info                                                                   |
+-----------------------------+---------+-----------+-------------------------------------------+---------------------------------------------------------------------------------+
| StreamAgg_17                | 1.00    | root      |                                           | funcs:count(Column#13)->Column#11                                               |
| └─IndexReader_18            | 1.00    | root      |                                           | index:StreamAgg_9                                                               |
|   └─StreamAgg_9             | 1.00    | cop[tikv] |                                           | funcs:count(1)->Column#13                                                       |
|     └─IndexRangeScan_16     | 8166.73 | cop[tikv] | table:trips, index:start_date(start_date) | range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false, stats:pseudo |
+-----------------------------+---------+-----------+-------------------------------------------+---------------------------------------------------------------------------------+
4 rows in set (0.00 sec)
```

在添加完索引后的新执行计划中，使用 `IndexScan_24` 直接读取满足条件 `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` 的数据，可以看到，估算的要扫描的数据行数从之前的 19117643.00 降到了现在的 8166.73。在测试环境中显示，这个查询的执行时间从 50.41 秒降到了 0.01 秒！

## 算子相关的系统变量

TiDB 在 MySQL 的基础上，定义了一些专用的系统变量和语法用来优化性能。其中一些系统变量和具体的算子相关，比如算子的并发度，算子的内存使用上限，是否允许使用分区表等。这些都可以通过系统变量进行控制，从而影响各个算子执行的效率。

如果读者想要详细了解所有的系统变量及其使用规则，可以参见[系统变量和语法](/system-variables.md)。

## 另请参阅

* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
* [TiDB in Action](https://book.tidb.io/session3/chapter1/sql-execution-plan.html)
* [System Variables](/system-variables.md)

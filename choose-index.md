---
title: 索引的选择
aliases: ['/docs-cn/dev/choose-index/']
---

# 索引的选择

从存储层读取数据是 SQL 计算过程中最为耗时的部分之一，TiDB 目前支持从不同的存储和不同的索引中读取数据，索引选择得是否合理将很大程度上决定一个查询的运行速度。

本章节将介绍 TiDB 如何选择索引去读入数据，以及相关的一些控制索引选择的方式。

## 读表

在介绍索引的选择之前，首先要了解 TiDB 有哪些读表的方式，这些方式的触发条件是什么，不同方式有什么区别，各有什么优劣。

### 读表算子

| 读表算子 | 触发条件 | 适用场景 | 说明 |
| :------- | :------- | :------- | :---- |
| PointGet/BatchPointGet | 读表的范围是一个或多个单点范围 | 任何场景 | 如果能被触发，通常被认为是最快的算子，因为其直接调用 kvget 的接口进行计算，不走 coprocessor  |
| TableReader | 无 | 任何场景 | 该 TableReader 算子用于 TiKV。从 TiKV 端直接扫描表数据，一般被认为是效率最低的算子，除非在 `_tidb_rowid` 这一列上存在范围查询，或者无其他可以选择的读表算子时，才会选择这个算子  |
| TableReader | 表在 TiFlash 节点上存在副本 | 需要读取的列比较少，但是需要计算的行很多 | 该 TableReader 算子用于 TiFlash。TiFlash 是列式存储，如果需要对少量的列和大量的行进行计算，一般会选择这个算子 |
| IndexReader | 表有一个或多个索引，且计算所需的列被包含在索引里 | 存在较小的索引上的范围查询，或者对索引列有顺序需求的时候 | 当存在多个索引的时候，会根据估算代价选择合理的索引 |
| IndexLookupReader | 表有一个或多个索引，且计算所需的列**不完全**被包含在索引里 | 同 IndexReader | 因为计算列不完全被包含在索引里，所以读完索引后需要回表，这里会比 IndexReader 多一些开销 |
| IndexMerge | 表有多个索引或多值索引 | 使用多值索引或同时使用多个索引的时候 | 可以通过 [optimizer hints](/optimizer-hints.md) 指定使用该算子，或让优化器根据代价估算自动选择该算子，参见[用 EXPLAIN 查看索引合并的 SQL 执行计划](/explain-index-merge.md) |

> **注意：**
> 
> TableReader 是基于 `_tidb_rowid` 的索引，TiFlash 是列存索引，所以索引的选择即是读表算子的选择。

## 索引的选择

TiDB 基于规则或基于代价来选择索引。基于的规则包括前置规则和 Skyline-Pruning。在选择索引时，TiDB 会先尝试前置规则。如果存在索引满足某一条前置规则，则直接选择该索引。否则，TiDB 会采用 Skyline-Pruning 来排除不合适的索引，然后基于每个读表算子的代价估算，选择代价最小的索引。

### 基于规则选择

#### 前置规则

TiDB 采用如下的启发式前置规则来选择索引：

+ 规则 1：如果存在索引满足“唯一性索引全匹配 + 不需要回表（即该索引生成的计划是 IndexReader）”时，直接选择该索引。

+ 规则 2：如果存在索引满足“唯一性索引全匹配 + 需要回表（即该索引生成的计划是 IndexLookupReader）”时，选择满足该条件且回表行数最小的索引作为候选索引。

+ 规则 3：如果存在索引满足“普通索引不需要回表 + 读取行数小于一定阈值”时，选择满足该条件且读取行数最小的索引作为候选索引。

+ 规则 4：如果规则 2 和 3 之中仅选出一条候选索引，则选择该候选索引。如果规则 2 和 3 均选出候选索引，则选择读取行数（读索引行数 + 回表行数）较小的索引。

上述规则中的“索引全匹配”指每个索引列上均存在等值条件。在执行 `EXPLAIN FORMAT = 'verbose' ...` 语句时，如果前置规则匹配了某一索引，TiDB 会输出一条 NOTE 级别的 warning 提示该索引匹配了前置规则。

在以下示例中，因为索引 `idx_b` 满足规则 2 中“唯一性索引全匹配 + 需要回表”的条件，TiDB 选择索引 `idx_b` 作为访问路径，`SHOW WARNING` 返回了索引 `idx_b` 命中前置规则的提示。

```sql
mysql> CREATE TABLE t(a INT PRIMARY KEY, b INT, c INT, UNIQUE INDEX idx_b(b));
Query OK, 0 rows affected (0.01 sec)

mysql> EXPLAIN FORMAT = 'verbose' SELECT b, c FROM t WHERE b = 3 OR b = 6;
+-------------------+---------+---------+------+-------------------------+------------------------------+
| id                | estRows | estCost | task | access object           | operator info                |
+-------------------+---------+---------+------+-------------------------+------------------------------+
| Batch_Point_Get_5 | 2.00    | 8.80    | root | table:t, index:idx_b(b) | keep order:false, desc:false |
+-------------------+---------+---------+------+-------------------------+------------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;
+-------+------+-------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                   |
+-------+------+-------------------------------------------------------------------------------------------+
| Note  | 1105 | unique index idx_b of t is selected since the path only has point ranges with double scan |
+-------+------+-------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

#### Skyline-Pruning

Skyline-Pruning 是一个针对索引的启发式过滤规则，能降低错误估算导致选错索引的概率。Skyline-Pruning 从以下三个维度衡量一个索引的优劣：

- 索引的列涵盖了多少访问条件。“访问条件”指的是可以转化为某列范围的 `where` 条件，如果某个索引的列集合涵盖的访问条件越多，那么它在这个维度上更优。

- 选择该索引读表时，是否需要回表（即该索引生成的计划是 IndexReader 还是 IndexLookupReader）。不用回表的索引在这个维度上优于需要回表的索引。如果均需要回表，则比较索引的列涵盖了多少过滤条件。过滤条件指的是可以根据索引判断的 `where` 条件。如果某个索引的列集合涵盖的访问条件越多，则回表数量越少，那么它在这个维度上越优。

+ 选择该索引是否能满足一定的顺序。因为索引的读取可以保证某些列集合的顺序，所以满足查询要求顺序的索引在这个维度上优于不满足的索引。

对于以上三种维度，如果索引 `idx_a` 在这三个维度上都不比 `idx_b` 差，且有一个维度比 `idx_b` 好，那么 TiDB 会优先选择 `idx_a`。在执行 `EXPLAIN FORMAT = 'verbose' ...` 语句时，如果 Skyline-Pruning 排除了某些索引，TiDB 会输出一条 NOTE 级别的 warning 提示哪些索引在 Skyline-Pruning 排除之后保留下来。

在以下示例中，索引 `idx_b` 和 `idx_e` 均劣于 `idx_b_c`，因而被 Skyline-Pruning 排除，`SHOW WARNING` 的返回结果显示了经过 Skyline-Pruning 后剩余的索引。

```sql
mysql> CREATE TABLE t(a INT PRIMARY KEY, b INT, c INT, d INT, e INT, INDEX idx_b(b), INDEX idx_b_c(b, c), INDEX idx_e(e));
Query OK, 0 rows affected (0.01 sec)

mysql> EXPLAIN FORMAT = 'verbose' SELECT * FROM t WHERE b = 2 AND c > 4;
+-------------------------------+---------+---------+-----------+------------------------------+----------------------------------------------------+
| id                            | estRows | estCost | task      | access object                | operator info                                      |
+-------------------------------+---------+---------+-----------+------------------------------+----------------------------------------------------+
| IndexLookUp_10                | 33.33   | 738.29  | root      |                              |                                                    |
| ├─IndexRangeScan_8(Build)     | 33.33   | 2370.00 | cop[tikv] | table:t, index:idx_b_c(b, c) | range:(2 4,2 +inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_9(Probe)     | 33.33   | 2370.00 | cop[tikv] | table:t                      | keep order:false, stats:pseudo                     |
+-------------------------------+---------+---------+-----------+------------------------------+----------------------------------------------------+
3 rows in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;
+-------+------+------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                  |
+-------+------+------------------------------------------------------------------------------------------+
| Note  | 1105 | [t,idx_b_c] remain after pruning paths for t given Prop{SortItems: [], TaskTp: rootTask} |
+-------+------+------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### 基于代价选择

在使用 Skyline-Pruning 规则排除了不合适的索引之后，索引的选择完全基于代价估算，读表的代价估算需要考虑以下几个方面：

- 索引的每行数据在存储层的平均长度。
- 索引生成的查询范围的行数量。
- 索引的回表代价。
- 索引查询时的范围数量。

根据这些因子和代价模型，优化器会选择一个代价最低的索引进行读表。

#### 代价选择调优的常见问题

1. 估算的行数量不准确？

    一般是统计信息过期或者准确度不够造成的，可以重新执行 `analyze table` 或者修改 `analyze table` 的参数。

2. 统计信息准确，为什么读 TiFlash 更快，而优化器选择了 TiKV？

    目前区别 TiFlash 和 TiKV 的代价模型还比较粗糙，可以调小 `tidb_opt_seek_factor` 的值，让优化器倾向于选择 TiFlash。
    
3. 统计信息准确，某个索引要回表，但是它比另一个不用回表的索引实际执行更快，为什么选择了不用回表的索引？

    碰到这种情况，可能是代价估算时对于回表的代价计算得过大，可以调小 `tidb_opt_network_factor`，降低回表的代价。

## 控制索引的选择

通过 [Optimizer Hints](/optimizer-hints.md) 可以实现单条查询对索引选择的控制。

- `USE_INDEX`/`IGNORE_INDEX` 可以强制优化器使用/不使用某些索引。`FORCE_INDEX` 和 `USE_INDEX` 的作用相同。

- `READ_FROM_STORAGE` 可以强制优化器对于某些表选择 TiKV/TiFlash 的存储引擎进行查询。

## 使用多值索引

[多值索引](/sql-statements/sql-statement-create-index.md#多值索引)和普通索引有所不同，TiDB 目前只会使用 [IndexMerge](/explain-index-merge.md) 来访问多值索引。因此要想使用多值索引进行数据访问，请确保`tidb_enable_index_merge` 被设置为 `ON`。

多值索引的使用限制请参考 [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md#特性与限制)。

### 支持多值索引的场景

目前 TiDB 支持将 `json_member_of`、`json_contains` 和 `json_overlaps` 条件自动转换成 IndexMerge 来访问多值索引。既可以依赖优化器根据代价自动选择，也可通过 [`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) optimizer hint 或 [`use_index`](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-) 指定选择多值索引，见下面例子：

```sql
mysql> CREATE TABLE t1 (j JSON, INDEX idx((CAST(j->'$.path' AS SIGNED ARRAY)))); -- 使用 '$.path' 作为路径创建多值索引
Query OK, 0 rows affected (0.04 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t1, idx) */ * FROM t1 WHERE (1 MEMBER OF (j->'$.path'));
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                               | operator info                                                          |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------+
| Selection_5                     | 8000.00 | root      |                                                                             | json_memberof(cast(1, json BINARY), json_extract(test.t1.j, "$.path")) |
| └─IndexMerge_8                  | 10.00   | root      |                                                                             | type: union                                                            |
|   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo                            |
|   └─TableRowIDScan_7(Probe)     | 10.00   | cop[tikv] | table:t1                                                                    | keep order:false, stats:pseudo                                         |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t1, idx) */ * FROM t1 WHERE JSON_CONTAINS((j->'$.path'), '[1, 2, 3]');
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| id                            | estRows | task      | access object                                                               | operator info                               |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| IndexMerge_9                  | 10.00   | root      |                                                                             | type: intersection                          |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[2,2], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[3,3], keep order:false, stats:pseudo |
| └─TableRowIDScan_8(Probe)     | 10.00   | cop[tikv] | table:t1                                                                    | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
5 rows in set (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t1, idx) */ * FROM t1 WHERE JSON_OVERLAPS((j->'$.path'), '[1, 2, 3]');
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                               | operator info                                                                    |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| Selection_5                     | 8000.00 | root      |                                                                             | json_overlaps(json_extract(test.t1.j, "$.path"), cast("[1, 2, 3]", json BINARY)) |
| └─IndexMerge_10                 | 10.00   | root      |                                                                             | type: union                                                                      |
|   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo                                      |
|   ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[2,2], keep order:false, stats:pseudo                                      |
|   ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[3,3], keep order:false, stats:pseudo                                      |
|   └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:t1                                                                    | keep order:false, stats:pseudo                                                   |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------+
6 rows in set, 1 warning (0.00 sec)
```

复合的多值索引，也一样可以使用 IndexMerge 进行访问：

```sql
mysql> CREATE TABLE t2 (a INT, j JSON, b INT, INDEX idx(a, (CAST(j->'$.path' AS SIGNED ARRAY)), b));
Query OK, 0 rows affected (0.04 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND (1 MEMBER OF (j->'$.path')) AND b=2;
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                                     | operator info                                                          |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+------------------------------------------------------------------------+
| Selection_5                     | 0.01    | root      |                                                                                   | json_memberof(cast(1, json BINARY), json_extract(test.t2.j, "$.path")) |
| └─IndexMerge_8                  | 0.00    | root      |                                                                                   | type: union                                                            |
|   ├─IndexRangeScan_6(Build)     | 0.00    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1 2,1 1 2], keep order:false, stats:pseudo                    |
|   └─TableRowIDScan_7(Probe)     | 0.00    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                                         |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+------------------------------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_CONTAINS((j->'$.path'), '[1, 2, 3]');
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+
| id                            | estRows | task      | access object                                                                     | operator info                                   |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+
| IndexMerge_9                  | 0.10    | root      |                                                                                   | type: intersection                              |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1,1 1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 3,1 3], keep order:false, stats:pseudo |
| └─TableRowIDScan_8(Probe)     | 0.10    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                  |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+
5 rows in set (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_OVERLAPS((j->'$.path'), '[1, 2, 3]');
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                                     | operator info                                                                    |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| Selection_5                     | 8.00    | root      |                                                                                   | json_overlaps(json_extract(test.t2.j, "$.path"), cast("[1, 2, 3]", json BINARY)) |
| └─IndexMerge_10                 | 0.10    | root      |                                                                                   | type: union                                                                      |
|   ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1,1 1], keep order:false, stats:pseudo                                  |
|   ├─IndexRangeScan_7(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo                                  |
|   ├─IndexRangeScan_8(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 3,1 3], keep order:false, stats:pseudo                                  |
|   └─TableRowIDScan_9(Probe)     | 0.10    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                                                   |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
6 rows in set, 1 warning (0.00 sec)
```

对于由多个 `member of` 组成的 `OR`/`AND` 条件，且这些条件可以被作用在同一个或者多个多值索引上，由于 `member of` 的单路性质，也可以使用 IndexMerge `UNION` 或者 `INTERSECTION` 进行访问：

```sql
mysql> CREATE TABLE t3 (a INT, j JSON, b INT, k JSON, INDEX idx(a, (CAST(j AS SIGNED ARRAY))), INDEX idx2(b,(CAST(k as SIGNED ARRAY))));
Query OK, 0 rows affected (0.04 sec)
```

使用 `UNION` 进行访问：

```sql
mysql> EXPLAIN SELECT /*+ use_index_merge(t3, idx) */ * FROM t3 WHERE ((a=1 AND (1 member of (j)))) OR ((a=2 AND (2 member of (j))));
+---------------------------------+---------+-----------+---------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                     | operator info                                                                                                                                    |
+---------------------------------+---------+-----------+---------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5                     | 0.08    | root      |                                                   | or(and(eq(test.t3.a, 1), json_memberof(cast(1, json BINARY), test.t3.j)), and(eq(test.t3.a, 2), json_memberof(cast(2, json BINARY), test.t3.j))) |
| └─IndexMerge_9                  | 0.10    | root      |                                                   | type: union                                                                                                                                      |
|   ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t3, index:idx(a, cast(`j` as signed array)) | range:[1 1,1 1], keep order:false, stats:pseudo                                                                                                  |
|   ├─IndexRangeScan_7(Build)     | 0.10    | cop[tikv] | table:t3, index:idx(a, cast(`j` as signed array)) | range:[2 2,2 2], keep order:false, stats:pseudo                                                                                                  |
|   └─TableRowIDScan_8(Probe)     | 0.10    | cop[tikv] | table:t3                                          | keep order:false, stats:pseudo                                                                                                                   |
+---------------------------------+---------+-----------+---------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
```

使用 `INTERSECTION` 进行访问：

```sql
tidb> EXPLAIN SELECT /*+ use_index_merge(t3, idx, idx2) */ * FROM t3 WHERE ((a=1 AND (1 member of (j)))) AND ((b=1 AND (2 member of (k))));
+-------------------------------+---------+-----------+----------------------------------------------------+-------------------------------------------------+
| id                            | estRows | task      | access object                                      | operator info                                   |
+-------------------------------+---------+-----------+----------------------------------------------------+-------------------------------------------------+
| IndexMerge_8                  | 0.10    | root      |                                                    | type: intersection                              |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t3, index:idx(a, cast(`j` as signed array))  | range:[1 1,1 1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t3, index:idx2(b, cast(`k` as signed array)) | range:[1 2,1 2], keep order:false, stats:pseudo |
| └─TableRowIDScan_7(Probe)     | 0.10    | cop[tikv] | table:t3                                           | keep order:false, stats:pseudo                  |
+-------------------------------+---------+-----------+----------------------------------------------------+-------------------------------------------------+
4 rows in set (0.01 sec)
```

### 部分支持多值索引的场景

如果多个条件通过 `AND`/`OR` 进行组合，每个 `item` 条件对应多个不同的索引，则有以下情况：

* 如果单个 item 的路径也是 index merge，则只要其和外部的 `AND`/`OR` 的逻辑一致，就可以和外部 index merge 融合。
* 如果单个 item 的路径也是 index merge，且其 index partial path 只有一条，那么无论其自身 index merge 的逻辑是 `AND`/`OR`，都可以和外部 index merge 融合。

```sql
mysql> CREATE TABLE t(j1 JSON, j2 JSON, a INT, INDEX k1((CAST(j1->'$.path' AS SIGNED ARRAY))), INDEX k2((CAST(j2->'$.path' AS SIGNED ARRAY))), INDEX ka(a));
Query OK, 0 rows affected (0.02 sec)
```

```sql
tidb> EXPLAIN SELECT /*+ use_index_merge(t, k1, k2, ka) */ * FROM t WHERE (1 member of (j1->'$.path')) AND (2 member of (j2->'$.path')) AND (a = 3);
+-------------------------------+---------+-----------+----------------------------------------------------------------------------+---------------------------------------------+
| id                            | estRows | task      | access object                                                              | operator info                               |
+-------------------------------+---------+-----------+----------------------------------------------------------------------------+---------------------------------------------+
| IndexMerge_9                  | 10.00   | root      |                                                                            | type: intersection                          |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t, index:ka(a)                                                       | range:[3,3], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t, index:k1(cast(json_extract(`j1`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t, index:k2(cast(json_extract(`j2`, _utf8'$.path') as signed array)) | range:[2,2], keep order:false, stats:pseudo |
| └─TableRowIDScan_8(Probe)     | 10.00   | cop[tikv] | table:t                                                                    | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+----------------------------------------------------------------------------+---------------------------------------------+
5 rows in set (0.00 sec)
```

目前只能使用 1 个索引进行访问，而无法产生如下面这样同时使用多个索引的计划：

```
Selection
└─IndexMerge
  ├─IndexRangeScan(k1)
  ├─IndexRangeScan(k2)
  ├─IndexRangeScan(ka)
  └─Selection
    └─TableRowIDScan
```

### 不支持多值索引的场景

如果多个条件通过 `OR` 进行组合，且这些条件对应多个不同的索引，则无法使用多值索引，如：

```sql
mysql> create table t(j1 json, j2 json, a int, INDEX k1((CAST(j1->'$.path' AS SIGNED ARRAY))), INDEX k2((CAST(j2->'$.path' AS SIGNED ARRAY))), INDEX ka(a));
Query OK, 0 rows affected (0.03 sec)

mysql> explain select /*+ use_index_merge(t, k1, k2, ka) */ * from t where (1 member of (j1->'$.path')) or (2 member of (j2->'$.path'));
+-------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                                                      |
+-------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | or(json_memberof(cast(1, json BINARY), json_extract(test.t.j1, "$.path")), json_memberof(cast(2, json BINARY), json_extract(test.t.j2, "$.path"))) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                                                                                                                               |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                                                                     |
+-------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set, 3 warnings (0.00 sec)

mysql> explain select /*+ use_index_merge(t, k1, k2, ka) */ * from t where (1 member of (j1->'$.path')) or (a = 3);
+-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                               |
+-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | or(json_memberof(cast(1, json BINARY), json_extract(test.t.j1, "$.path")), eq(test.t.a, 3)) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                                                                        |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                              |
+-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
3 rows in set, 3 warnings (0.00 sec)
```

对于上述场景，你可以使用 `Union All` 改写查询以使用多值索引。

下面是一些更加复杂且暂时无法使用 IndexMerge 来访问多值索引的场景：

```sql
mysql> CREATE TABLE t4 (j JSON, INDEX idx((CAST(j AS SIGNED ARRAY))));
Query OK, 0 rows affected (0.04 sec)

-- 如果查询包含多个 json_contains 通过 OR 组成的条件，则无法通过 IndexMerge 访问索引
mysql> EXPLAIN SELECT /*+ use_index_merge(t3, idx) */ * FROM t3 WHERE (json_contains(j, '[1, 2]')) OR (json_contains(j, '[3, 4]'));
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                    |
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
| TableReader_7           | 9600.00  | root      |               | data:Selection_6                                                                                                 |
| └─Selection_6           | 9600.00  | cop[tikv] |               | or(json_contains(test.t3.j, cast("[1, 2]", json BINARY)), json_contains(test.t3.j, cast("[3, 4]", json BINARY))) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                   |
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
3 rows in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;
+---------+------+----------------------------+
| Level   | Code | Message                    |
+---------+------+----------------------------+
| Warning | 1105 | IndexMerge is inapplicable |
+---------+------+----------------------------+
1 row in set (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t3, idx) */ * FROM t3 WHERE (json_contains(j, '[1, 2]')) OR (json_contains(j, '[3, 4]'));
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                    |
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
| TableReader_7           | 9600.00  | root      |               | data:Selection_6                                                                                                 |
| └─Selection_6           | 9600.00  | cop[tikv] |               | or(json_contains(test.t3.j, cast("[1, 2]", json BINARY)), json_contains(test.t3.j, cast("[3, 4]", json BINARY))) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                   |
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
3 rows in set, 1 warning (0.01 sec)

-- 如果查询中包含较为复杂的多层 OR / AND 嵌套形成的表达式，则无法通过 IndexMerge 访问索引
mysql> EXPLAIN SELECT /*+ use_index_merge(t3, idx) */ * FROM t3 WHERE ((1 member of (j)) AND (2 member of (j))) OR ((3 member of (j)) AND (4 member of (j)));
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                                                                                                                |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | or(and(json_memberof(cast(1, json BINARY), test.t3.j), json_memberof(cast(2, json BINARY), test.t3.j)), and(json_memberof(cast(3, json BINARY), test.t3.j), json_memberof(cast(4, json BINARY), test.t3.j))) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                                                                                                                                                                                         |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                                                                                                               |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set, 2 warnings (0.00 sec)
```

受限于多值索引的特性，当多值索引无法生效时，使用 [`use_index`](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-) 可能会返回 `Can't find a proper physical plan for this query` 的错误，而使用 [`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) 不会，因此建议使用 `use_index_merge`：

```sql
mysql> EXPLAIN SELECT /*+ use_index(t3, idx) */ * FROM t3 WHERE ((1 member of (j)) AND (2 member of (j))) OR ((3 member of (j)) AND (4 member of (j)));
ERROR 1815 (HY000): Internal : Cant find a proper physical plan for this query

mysql> EXPLAIN SELECT /*+ use_index_merge(t3, idx) */ * FROM t3 WHERE ((1 member of (j)) AND (2 member of (j))) OR ((3 member of (j)) AND (4 member of (j)));
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                                                                                                                |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | or(and(json_memberof(cast(1, json BINARY), test.t3.j), json_memberof(cast(2, json BINARY), test.t3.j)), and(json_memberof(cast(3, json BINARY), test.t3.j), json_memberof(cast(4, json BINARY), test.t3.j))) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                                                                                                                                                                                         |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                                                                                                               |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set, 2 warnings (0.00 sec)
```
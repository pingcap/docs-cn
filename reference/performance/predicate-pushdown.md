---
title: 谓词下推规则简介
category: reference
---

# 谓词下推规则简介

这里的谓词，可以简单理解为 `WHERE`、`HAVING` 或者 `JOIN` 的 `ON` 子句中的 “筛选条件”。所谓谓词下推，也就是让这些筛选条件在处理过程中尽可能早的执行。

谓词下推规则会把每个算子上能推的条件尽量往下推，如果某些谓词到某个算子时无法下推了，那么就会在这个算子上面新加一个 Selection 算子，形成新的查询计划。

谓词下推是非常重要的一个优化。

## 例子

对于

{{< copyable "sql" >}}

```sql
select * from t1, t2 where t1.a > 3 and t2.b > 5;
```

假设 t1 和 t2 都是 100 条数据。如果把 t1 和 t2 两个表做笛卡尔积了再过滤，我们要处理 10000 条数据，而如果能先做过滤条件，那么数据量就会大量减少。谓词下推会尽量把过滤条件推到靠近叶子节点，从而减少数据的处理量，节省计算开销。这就是谓词下推的作用。

```sql
explain select * from t1, t2 where t1.a > 3 and t2.b > 5;
+------------------------------+----------+-----------+---------------+--------------------------------+
| id                           | estRows  | task      | access object | operator info                  |
+------------------------------+----------+-----------+---------------+--------------------------------+
| HashJoin_9                   | 1111.11  | root      |               | CARTESIAN inner join           |
| ├─TableReader_12(Build)      | 0.33     | root      |               | data:Selection_11              |
| │ └─Selection_11             | 0.33     | cop[tikv] |               | gt(test.t1.a, 3)               |
| │   └─TableFullScan_10       | 1.00     | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
| └─TableReader_15(Probe)      | 3333.33  | root      |               | data:Selection_14              |
|   └─Selection_14             | 3333.33  | cop[tikv] |               | gt(test.t2.b, 5)               |
|     └─TableFullScan_13       | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo |
+------------------------------+----------+-----------+---------------+--------------------------------+
7 rows in set (0.00 sec)
```

上面的例子将原本在 join 上的谓词，下推到了扫表算子中，最后通过 coprocessor 推给 TiKV 去做。

## 谓词下推与 join

谓词下推可以推过很多算子，这里讨论一下 join 算子的谓词下推规则。

对于 inner join，如果某个谓词中含有的列仅来自于左表或者右表中的一个，可以直接将其下推。

而对于 outer join，一种可能出现的情况是即使内表已经过滤了 NULL，在 join 之后还是会产生 NULL，所以不能简单下推，需要做更多的判断。

在对 join 进行谓词下推时，会首先尝试将 outer join 转换为 inner join.

什么情况下 outer join 可以转 inner join? outer join 的结果集包括外表的所有行，而不仅仅是连接列所匹配的行。如果外表的某行在内表中没有匹配的行，则结果集中内表对应的行补 NULL。

如果我们知道连接后的谓词条件一定会把内表包含 NULL 的行全部都过滤掉，那么做 outer join 就没有意义了，可以直接改写成 inner join.

## 不能推过的算子节点

谓词下推不能推过 Limit 和 MaxOneRow 算子。

因为先 Limit N 行，然后再做 Selection 操作，跟先做 Selection 操作，再 Limit N 行得到的结果是不一样的。

比如数据是 1 到 100，先 Limit 10 再 Select 大于 5，得到的是 5 到 10，而先做 Selection 再做 Limit 得到的是 5 到 15。

MaxOneRow 也是同理，它跟 Limit 1 效果一样。

## 另请参阅

* [理解 EXPLAIN 执行计划](/reference/performance/understanding-the-query-execution-plan.md)
* [TiDB 源码阅读系列文章（七）基于规则的优化](https://pingcap.com/blog-cn/tidb-source-code-reading-7/#谓词下推)
* [TiDB rule_predicate_push_down.go](https://github.com/pingcap/tidb/blob/master/planner/core/rule_predicate_push_down.go)

---
title: 错误索引的解决方案
summary: 了解如何处理错误索引问题。
---

# 错误索引的解决方案

在观察到某个查询的执行速度达不到预期时，可能是它的索引使用有误，这时就需要通过一些手段来解决。通常可以先使用[表的健康度信息](/statistics.md#表的健康度信息)来查看统计信息的健康度。根据健康度可以分为以下两种情况处理。

## 健康度较低

这意味着距离 TiDB 上次 `ANALYZE` 很久了。这时可以先使用 `ANALYZE` 命令对统计信息进行更新。更新之后如果索引的使用上还是错误的，可以查看下一小节。

## 健康度接近 100%

这时意味着刚刚结束 `ANALYZE` 命令或者结束后不久。这时可能和 TiDB 对行数的估算逻辑有关。

对于等值查询，错误索引可能是由 [Count-Min Sketch](/statistics.md#count-min-sketch) 引起的。这时可以先检查是不是这种特殊情况，然后进行对应的处理。

如果经过检查发现不是上面的可能情况，可以使用 [Optimizer Hints](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-) 中提到的 `USE_INDEX` 或者 `use index` 来强制选择索引。同时也可以使用[执行计划管理](/sql-plan-management.md)中提到的方式来非侵入地更改查询的行为。

## 其他情况

除去上述情况外，也存在因为数据的更新导致现有所有索引都不再适合的情况。这时就需要对条件和数据分布进行分析，查看是否有新的索引可以加快查询速度，然后使用 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 命令增加新的索引。

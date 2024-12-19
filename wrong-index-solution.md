---
title: 错误索引的解决方案
summary: 了解如何处理错误索引问题。
---

# 错误索引的解决方案

在观察到某个查询的执行速度达不到预期时，可能是它的索引使用有误。

可能造成 TiDB 优化器选择非预期索引的原因包括：

- **统计信息过时**：优化器依赖统计信息来估算查询成本。如果统计信息过时，可能导致优化器作出次优选择。
- **统计信息不匹配**：即使统计信息是最新的，也可能无法准确反映数据分布情况，导致成本估算偏差。
- **成本计算不准确**：当查询的结构复杂或数据分布不均时，优化器有可能会错误地估算使用某个索引的成本。
- **存储引擎选择不当**：在某些场景下，优化器选择的存储引擎可能不适合当前查询。
- **函数下推限制**：部分函数或操作无法下推到存储引擎执行，可能会影响查询性能。

## 统计信息健康度

可以先使用[表的健康度信息](/statistics.md#表的健康度信息)来查看统计信息的健康度。根据健康度可以分为以下两种情况处理。

### 健康度较低

这意味着距离 TiDB 上次执行 `ANALYZE` 已经很久了。这时可以先使用 `ANALYZE` 命令对统计信息进行更新。更新之后如果仍在使用错误的索引，可以参考下一小节。

### 健康度接近 100%

这时意味着刚刚结束 `ANALYZE` 命令或者结束后不久。这时可能和 TiDB 对行数的估算逻辑有关。

对于等值查询，错误索引可能是由 [Count-Min Sketch](/statistics.md#count-min-sketch) 引起的。这时可以先检查是不是这种特殊情况，然后进行对应的处理。

如果经过检查发现不是上面的可能情况，可以使用 [Optimizer Hints](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-) 中提到的 `USE_INDEX` 或者 `use index` 来强制选择索引。同时也可以使用[执行计划管理](/sql-plan-management.md)中提到的方式来非侵入地更改查询的行为。

### 其他情况

除去上述情况外，也存在因为数据的更新导致现有所有索引都不再适合的情况。这时就需要对条件和数据分布进行分析，查看是否有新的索引可以加快查询速度，然后使用 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 命令增加新的索引。

## 统计信息不匹配

当数据分布特别不均衡时，统计信息可能无法准确反映实际数据分布。此时，可以尝试配置 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 语句的不同选项来提高统计信息的准确性，以更准确地匹配索引。

例如，假设你有一个 `orders` 表，其中 `customer_id` 列上有一个索引，但超过 50% 的订单都具有相同的 `customer_id`。对于该表，统计信息可能无法很好地反映数据分布，从而影响查询性能。

## 成本信息

如需查看执行成本的详细信息，可以在执行 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 和 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句时带上 `FORMAT=verbose` 选项。通过这些信息，可以了解不同执行路径之间的成本差异。

## 引擎选择

默认情况下，TiDB 会基于成本估算选择使用 TiKV 或 TiFlash 访问数据表。你可以通过配置 Engine 隔离的方式，尝试使用不同的存储引擎执行同一查询。

更多信息，请参考 [Engine 隔离](/tiflash/use-tidb-to-read-tiflash.md#engine-隔离)。

## 函数下推

为了提升查询性能，TiDB 会将某些函数下推到 TiKV 或 TiFlash 存储引擎中执行。然而，部分函数不支持下推，这可能会限制可用的执行计划，进而影响查询性能。

关于支持下推的表达式，请参考 [TiKV 支持的下推计算](/functions-and-operators/expressions-pushed-down.md) 和 [TiFlash 支持的下推计算](/tiflash/tiflash-supported-pushdown-calculations.md)。

需要注意的是，你也可以禁用特定表达式的下推。更多信息，请参考[优化规则和表达式下推的黑名单](/blocklist-control-plan.md)。

## 另请参阅

- [常规统计信息](/statistics.md)
- [索引选择](/choose-index.md)
- [Optimizer Hints](/optimizer-hints.md)
- [执行计划管理 (SPM)](/sql-plan-management.md)
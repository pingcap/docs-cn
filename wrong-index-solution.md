---
title: 错误索引解决方案
summary: 了解如何解决错误索引问题。
---

# 错误索引解决方案

如果你发现某些查询的执行速度未达到预期，可能是优化器选择了错误的索引来执行查询。

优化器可能选择意外索引的原因有多个：

- **统计信息过期**：优化器依赖统计信息来估算查询成本。如果统计信息过期，优化器可能会做出次优选择。
- **统计信息不匹配**：即使统计信息是最新的，它们可能无法准确反映数据分布，导致成本估算不准确。
- **成本计算不正确**：由于查询结构复杂或数据分布的原因，优化器可能会错误计算使用索引的成本。
- **存储引擎选择不当**：在某些情况下，优化器可能会选择对查询不是最优的存储引擎。
- **函数下推限制**：某些函数或操作可能无法下推到存储引擎，这可能会影响查询性能。

## 统计信息健康度

你可以首先查看统计信息中的[表的健康状态](/statistics.md#health-state-of-tables)，然后根据不同的健康状态来解决这个问题。

### 低健康状态

低健康状态意味着 TiDB 长时间未执行 `ANALYZE` 语句。你可以通过运行 `ANALYZE` 命令来更新统计信息。更新后，如果优化器仍然使用错误的索引，请参考下一节。

### 接近 100% 的健康状态

接近 100% 的健康状态表明 `ANALYZE` 语句刚刚完成或在不久前完成。在这种情况下，错误索引问题可能与 TiDB 的行数估算逻辑有关。

对于等值查询，原因可能是 [Count-Min Sketch](/statistics.md#count-min-sketch)。你可以检查 Count-Min Sketch 是否是导致问题的原因并采取相应的解决方案。

如果上述原因不适用于你的问题，你可以使用 `USE_INDEX` 或 `use index` 优化器提示来强制选择索引（详见 [USE_INDEX](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)）。此外，你还可以通过使用[SQL 计划管理](/sql-plan-management.md)以非侵入式的方式改变查询行为。

### 其他情况

除了上述情况外，错误索引问题也可能是由数据更新导致所有索引不再适用。在这种情况下，你需要对条件和数据分布进行分析，看看是否可以通过新索引来加速查询。如果可以，你可以通过运行 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 命令来添加新索引。

## 统计信息不匹配

当数据分布高度倾斜时，统计信息可能无法准确反映实际数据。在这种情况下，可以尝试配置 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 语句的选项。这可能有助于提高统计信息的准确性并更好地匹配索引。

例如，假设你有一个 `orders` 表，其中有一个 `customer_id` 列的索引，而超过 50% 的订单共享相同的 `customer_id`。在这种情况下，统计信息可能无法很好地表示数据分布，从而影响查询性能。

## 成本信息

要查看执行成本的详细信息，你可以使用 `FORMAT=verbose` 选项执行 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 和 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句。根据这些信息，你可以看到不同执行路径之间的成本差异。

## 引擎选择

默认情况下，TiDB 根据成本估算选择 TiKV 或 TiFlash 进行表访问。你可以通过应用引擎隔离来尝试对同一查询使用不同的引擎。

更多信息，请参见[引擎隔离](/tiflash/use-tidb-to-read-tiflash.md#engine-isolation)。

## 函数下推

为了提高查询性能，TiDB 可以将某些函数下推到 TiKV 或 TiFlash 存储引擎执行。但是，某些函数不支持下推，这可能会限制可用的执行计划，并可能影响查询性能。

关于支持下推的表达式，请参见 [TiKV 支持的下推计算](/functions-and-operators/expressions-pushed-down.md)和 [TiFlash 支持的下推计算](/tiflash/tiflash-supported-pushdown-calculations.md)。

请注意，你也可以禁用特定表达式的下推。更多信息，请参见[优化规则和表达式下推的黑名单](/blocklist-control-plan.md)。

## 另请参阅

- [统计信息](/statistics.md)
- [索引选择](/choose-index.md)
- [优化器提示](/optimizer-hints.md)
- [SQL 计划管理](/sql-plan-management.md)

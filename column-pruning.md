---
title: 列裁剪
category: performance
---

# 列裁剪

列裁剪的基本思想在于：对于算子中实际用不上的列，优化器在优化的过程中没有必要保留它们。 对这些列的删除会减少 I/O 资源占用，并为后续的优化带来便利。下面给出一个列重复的例子：

假设表 t 里面有 a b c d 四列，执行如下语句：

```sql
select a from t where b > 5
```

在该查询的过程中，t 表实际上只有 a, b 两列会被用到，而 c, d 的数据则显得多余。对应到该语句的查询计划，Selection 算子会用到 b 列，下面接着的 DataSource 算子会用到 a, b 两列，而剩下 c, d 两列则都可以裁剪掉，DataSource 算子在读数据时不需要将它们读进来。

出于上述考量，TiDB 会在逻辑优化阶段进行自上而下的扫描，裁剪不需要的列，减少资源浪费。该扫描过程称作 “列裁剪”，对应逻辑优化规则中的 `columnPruner`。

## 算法实现

对于逻辑计划中的一个算子而言，它所需要的列分为两种：上层算子计算时所需要的列，本层算子计算时所需要的列。从这个原则出发，优化器可以自顶向下地计算每个算子所需要的列，在遍历的过程中，维护逻辑计划树中的祖先节点给当前算子带来的“列需求”。

相关代码实现于 `planner/core/` 目录下的 `plan.go` 与 `rule_column_pruning.go` 中，实现接口如下。

```goland
PruneColumns([]*expression.Column) error
```

函数输入即为施加给当前算子的“列需求”集合。 在普通优化器中，列裁剪会发生在逻辑优化的开始和结尾，[相关代码](https://github.com/pingcap/tidb/blob/902231076d56fee9074e4c7bcd03a0d0f0d88524/planner/core/optimizer.go#L61)。 在 cascades 优化器中，列裁剪会发生在 Preprocessing 阶段，[相关代码](https://github.com/pingcap/tidb/blob/ded862fbebc555de98e230ef57310f9162725a9e/planner/cascades/optimize.go#L118)。

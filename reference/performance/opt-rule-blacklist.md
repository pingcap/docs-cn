---
title: 优化规则黑名单
category: reference
---

# 优化规则黑名单

在[join reorder 算法简介](/reference/performance/join-reorder.md)中，介绍了一种较为复杂的优化规则，TiDB 对于某条查询，会智能地选择一些优化规则对查询进行智能优化。

同时 TiDB 提供了一些可以自定义优化的功能，方便用户针对查询进行调优，比如[优化器 Hints](/reference/performance/optimizer-hints.md)。

**优化规则黑名单**是针对优化规则的调优手段之一，主要用于手动禁用一些优化规则。

## 重要的优化规则<div id="rules"></div>

- 列裁剪（column_prune）：对于上层算子不需要的列，在下层算子不输出该列，减少计算。

- 子查询去关联（decorrelate）：会尝试对相关子查询进行改写，将其转换为普通 join 或 aggression 计算。

- 聚合消除（aggregation_eliminate）：尝试消除执行计划中的某些不必要的聚合算子。

- 投影消除（projection_eliminate）：对于执行计划中不必要的投影算子，对其消除。

- 最大最小消除（max_min_eliminate）：改写聚合中的 max, min 计算，转化为 order by + limit 1。

- 谓词下推（predicate_push_down）：尝试将执行计划中过滤条件下推到离数据源更近的算子上。

- 外连接消除（outer_join_eliminate）：尝试消除执行计划中不必要的 left join 或者 right join。

- 分区表查询改写（partition_processor）：将分区表查询改成为用 union all 算子代替。

- 聚合下推（aggregation_push_down）：尝试将执行计划中的聚合算子下推到更底层的计算节点。

- topN 下推（topn_push_down）：尝试将执行计划中的 topN 算子下推到更底层的计算节点。

- join 重排序（join_reorder）：尝试对多个 join 算子进行重新排序。

## 如何禁用优化规则

当某些优化规则对于一些比较特殊的查询，出现了不理想的优化结果时，用户可以使用**优化规则黑名单**对一些优化规则进行禁用。

### 使用方法

每个优化规则都有自己的名字，比如列裁剪的名字是 "column_prune"，所有优化规则的名字皆可以在[重要的优化规则](/reference/performance/opt-rule-blacklist.md#rules)的括号中查到。

当用户想禁用某些规则时，可以往 `mysql.opt_rule_blacklist` 的表中写入规则的名字，比如：

{{< copyable "sql" >}}

```sql
insert into mysql.opt_rule_blacklist values("join_reorder"),("topn_push_down");
```

> **注意：**
> TiDB 不会实时地将这个表读入到内存中，所以即便是写入了禁用规则也不会立马生效。

然后用户需要执行以下 SQL，让 TiDB 把禁用规则写到内存中，才能真正做到禁用的效果：

{{< copyable "sql" >}}

```sql
admin reload opt_rule_blacklist
```

同理，需要解除某些规则的禁用时，需要执行删除表中数据并执行 `admin reload`:

{{< copyable "sql" >}}

```sql
delete from mysql.opt_rule_blacklist where name in ("join_reoder", "topn_push_down")
admin reload opt_rule_blacklist
```

> **注意：**
> 所以以上操作需要使用 root 权限的用户进行操作。

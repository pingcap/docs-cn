---
title: 优化规则黑名单
category: reference
---

# 优化规则黑名单

**优化规则黑名单**是针对优化规则的调优手段之一，主要用于手动禁用一些优化规则。

## 重要的优化规则<div id="rules"></div>

|**优化规则**|**规则名称**|**简介**|
| :--- | :--- | :--- |
| 列裁剪 | column_prune | 对于上层算子不需要的列，不在下层算子输出该列，减少计算 |
| 子查询去关联 | decorrelate | 尝试对相关子查询进行改写，将其转换为普通 join 或 aggression 计算 |
| 聚合消除 | aggregation_eliminate | 尝试消除执行计划中的某些不必要的聚合算子 |
| 投影消除 | projection_eliminate |  消除执行计划中不必要的投影算子 |
| 最大最小消除 | max_min_eliminate | 改写聚合中的 max/min 计算，转化为 `order by` + `limit 1` |
| 谓词下推 | predicate_push_down | 尝试将执行计划中过滤条件下推到离数据源更近的算子上 |
| 外连接消除 | outer_join_eliminate | 尝试消除执行计划中不必要的 left join 或者 right join |
| 分区裁剪 | partition_processor | 将分区表查询改成为用 union all，并裁剪掉不满足过滤条件的分区 |
| 聚合下推 | aggregation_push_down | 尝试将执行计划中的聚合算子下推到更底层的计算节点 |
| TopN 下推 | topn_push_down | 尝试将执行计划中的 TopN 算子下推到离数据源更近的算子上 |
| Join 重排序 | join_reorder | 对多表 join 确定连接顺序 |

## 如何禁用优化规则

当某些优化规则对于一些比较特殊的查询，出现了不理想的优化结果时，用户可以使用**优化规则黑名单**对一些优化规则进行禁用。

### 使用方法

> **注意：**
> 以下操作都需要数据库的 root 权限。

每个优化规则都有自己的名字，比如列裁剪的名字是 "column_prune"，所有优化规则的名字皆可以在[重要的优化规则](/reference/performance/opt-rule-blacklist.md#rules)表格中第二列查到。

当用户想禁用某些规则时，可以往 `mysql.opt_rule_blacklist` 的表中写入规则的名字，比如：

{{< copyable "sql" >}}

```sql
insert into mysql.opt_rule_blacklist values("join_reorder"),("topn_push_down");
```

执行以下 SQL 让禁用规则立即生效：

{{< copyable "sql" >}}

```sql
admin reload opt_rule_blacklist
```

同理，需要解除某些规则的禁用时，需要删除表中数据再执行 `admin reload`:

{{< copyable "sql" >}}

```sql
delete from mysql.opt_rule_blacklist where name in ("join_reoder", "topn_push_down")
admin reload opt_rule_blacklist
```

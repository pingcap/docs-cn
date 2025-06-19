---
title: TopN 和 Limit 算子下推
summary: 了解 TopN 和 Limit 算子下推的实现。
---

# TopN 和 Limit 算子下推

本文档描述了 TopN 和 Limit 算子下推的实现。

在 TiDB 执行计划树中，SQL 中的 `LIMIT` 子句对应 Limit 算子节点，`ORDER BY` 子句对应 Sort 算子节点。相邻的 Limit 算子和 Sort 算子会被合并为 TopN 算子节点，表示按照某种排序规则返回前 N 条记录。也就是说，Limit 算子等价于一个没有排序规则的 TopN 算子节点。

类似于谓词下推，TopN 和 Limit 在执行计划树中被下推到尽可能靠近数据源的位置，以便在早期阶段过滤所需数据。通过这种方式，下推显著减少了数据传输和计算的开销。

要禁用此规则，请参考[表达式下推的优化规则和黑名单](/blocklist-control-plan.md)。

## 示例

本节通过一些示例说明 TopN 下推。

### 示例 1：下推到存储层的 Coprocessor

{{< copyable "sql" >}}

```sql
create table t(id int primary key, a int not null);
explain select * from t order by a limit 10;
```

```
+----------------------------+----------+-----------+---------------+--------------------------------+
| id                         | estRows  | task      | access object | operator info                  |
+----------------------------+----------+-----------+---------------+--------------------------------+
| TopN_7                     | 10.00    | root      |               | test.t.a, offset:0, count:10   |
| └─TableReader_15           | 10.00    | root      |               | data:TopN_14                   |
|   └─TopN_14                | 10.00    | cop[tikv] |               | test.t.a, offset:0, count:10   |
|     └─TableFullScan_13     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+----------------------------+----------+-----------+---------------+--------------------------------+
4 rows in set (0.00 sec)
```

在这个查询中，TopN 算子节点被下推到 TiKV 进行数据过滤，每个 Coprocessor 只向 TiDB 返回 10 条记录。TiDB 聚合数据后，执行最终的过滤。

### 示例 2：TopN 可以下推到 Join 中（排序规则仅依赖外表的列）

{{< copyable "sql" >}}

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t left join s on t.a = s.a order by t.a limit 10;
```

```
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                   |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| TopN_12                          | 10.00    | root      |               | test.t.a, offset:0, count:10                    |
| └─HashJoin_17                    | 12.50    | root      |               | left outer join, equal:[eq(test.t.a, test.s.a)] |
|   ├─TopN_18(Build)               | 10.00    | root      |               | test.t.a, offset:0, count:10                    |
|   │ └─TableReader_26             | 10.00    | root      |               | data:TopN_25                                    |
|   │   └─TopN_25                  | 10.00    | cop[tikv] |               | test.t.a, offset:0, count:10                    |
|   │     └─TableFullScan_24       | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                  |
|   └─TableReader_30(Probe)        | 10000.00 | root      |               | data:TableFullScan_29                           |
|     └─TableFullScan_29           | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                  |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
8 rows in set (0.01 sec)
```

在这个查询中，TopN 算子的排序规则仅依赖外表 `t` 的列，因此可以在下推 TopN 到 Join 之前进行计算，以减少 Join 操作的计算成本。此外，TiDB 还将 TopN 下推到存储层。

### 示例 3：TopN 不能下推到 Join 之前

{{< copyable "sql" >}}

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t join s on t.a = s.a order by t.id limit 10;
```

```
+-------------------------------+----------+-----------+---------------+--------------------------------------------+
| id                            | estRows  | task      | access object | operator info                              |
+-------------------------------+----------+-----------+---------------+--------------------------------------------+
| TopN_12                       | 10.00    | root      |               | test.t.id, offset:0, count:10              |
| └─HashJoin_16                 | 12500.00 | root      |               | inner join, equal:[eq(test.t.a, test.s.a)] |
|   ├─TableReader_21(Build)     | 10000.00 | root      |               | data:TableFullScan_20                      |
|   │ └─TableFullScan_20        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo             |
|   └─TableReader_19(Probe)     | 10000.00 | root      |               | data:TableFullScan_18                      |
|     └─TableFullScan_18        | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo             |
+-------------------------------+----------+-----------+---------------+--------------------------------------------+
6 rows in set (0.00 sec)
```

TopN 不能下推到 `Inner Join` 之前。以上面的查询为例，如果 Join 后得到 100 条记录，然后经过 TopN 后剩下 10 条记录。但如果先执行 TopN 得到 10 条记录，Join 后可能只剩下 5 条记录。在这种情况下，下推会导致不同的结果。

同样，TopN 既不能下推到 Outer Join 的内表，也不能在其排序规则涉及多个表的列时下推，比如 `t.a+s.a`。只有当 TopN 的排序规则完全依赖于外表的列时，才能进行下推。

### 示例 4：将 TopN 转换为 Limit

{{< copyable "sql" >}}

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t left join s on t.a = s.a order by t.id limit 10;
```

```
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                   |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| TopN_12                          | 10.00    | root      |               | test.t.id, offset:0, count:10                   |
| └─HashJoin_17                    | 12.50    | root      |               | left outer join, equal:[eq(test.t.a, test.s.a)] |
|   ├─Limit_21(Build)              | 10.00    | root      |               | offset:0, count:10                              |
|   │ └─TableReader_31             | 10.00    | root      |               | data:Limit_30                                   |
|   │   └─Limit_30                 | 10.00    | cop[tikv] |               | offset:0, count:10                              |
|   │     └─TableFullScan_29       | 10.00    | cop[tikv] | table:t       | keep order:true, stats:pseudo                   |
|   └─TableReader_35(Probe)        | 10000.00 | root      |               | data:TableFullScan_34                           |
|     └─TableFullScan_34           | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                  |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
8 rows in set (0.00 sec)
```

在上面的查询中，TopN 首先被下推到外表 `t`。TopN 需要按 `t.id` 排序，而这是主键并且可以直接按顺序读取（`keep order: true`），无需在 TopN 中额外排序。因此，TopN 被简化为 Limit。

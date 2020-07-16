---
title: TopN and Limit Operator Push Down
summary: Learn the implementation of TopN and Limit operator pushdown.
---

# TopN and Limit Operator Push Down

This document describes the implementation of TopN and Limit operator pushdown.

In the TiDB execution plan tree, the `LIMIT` clause in SQL corresponds to the Limit operator node, and the `ORDER BY` clause corresponds to the Sort operator node. The adjacent Limit operator and Sort operator are combined as the TopN operator node, which means that the top N records are returned according to a certain sorting rule. That is to say, a Limit operator is equivalent to a TopN operator node with a null sorting rule.

Similar to predicate pushdown, TopN and Limit are pushed down in the execution plan tree to a position as close to the data source as possible so that the required data is filtered at an early stage. In this way, the pushdown significantly reduces the overhead of data transmission and calculation.

To disable this rule, refer to [Optimization Rules and Blocklist for Expression Pushdown](/blocklist-control-plan.md).

## Examples

This section illustrates TopN pushdown through some examples.

### Example 1: Push down to the Coprocessors in the storage layer

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

In this query, the TopN operator node is pushed down to TiKV for data filtering, and each Coprocessor returns only 10 records to TiDB. After TiDB aggregates the data, the final filtering is performed.

### Example 2: TopN can be pushed down into Join (the sorting rule only depends on the columns in the outer table)

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

In this query, the sorting rule of the TopN operator only depends on the columns in the outer table `t`, so a calculation can be performed before pushing down TopN to Join, to reduce the calculation cost of the Join operation. Besides, TiDB also pushes TopN down to the storage layer.

### Example 3: TopN cannot be pushed down before Join

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

TopN cannot be pushed down before `Inner Join`. Taking the query above as an example, if you get 100 records after Join, then you can have 10 records left after TopN. However, if TopN is performed first to get 10 records, only 5 records are left after Join. In such cases, the pushdown results in different results. 

Similarly, TopN can neither be pushed down to the inner table of Outer Join, nor can it be pushed down when its sorting rule is related to columns on multiple tables, such as `t.a+s.a`. Only when the sorting rule of TopN exclusively depends on columns on the outer table, can TopN be pushed down. 

### Example 4: Convert TopN to Limit

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

In the query above, TopN is first pushed to the outer table `t`. TopN needs to sort by `t.id`, which is the primary key and can be directly read in order  (`keep order: true`) without extra sorting in TopN. Therefore, TopN is simplified as Limit.

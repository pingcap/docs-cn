---
title: The Blocklist of Optimization Rules and Expression Pushdown
summary: Learn about the blocklist to control the optimization rules and the behavior of expression pushdown.
---

# The Blocklist of Optimization Rules and Expression Pushdown

This document introduces how to use the blocklist of optimization rules and the blocklist of expression pushdown to control the behavior of TiDB.

## The blocklist of optimization rules

The blocklist of optimization rules is one way to tune optimization rules, mainly used to manually disable some optimization rules.

### Important optimization rules

|**Optimization Rule**|**Rule Name**|**Description**|
| :--- | :--- | :--- |
| Column pruning | column_prune | One operator will prune the column if it is not needed by the upper executor. |
| Decorrelate subquery | decorrelate | Tries to rewrite the correlated subquery to non-correlated join or aggregation. |
| Aggregation elimination | aggregation_eliminate | Tries to remove unnecessary aggregation operators from the execution plan. |
| Projection elimination | projection_eliminate | Removes unnecessary projection operators from the execution plan. |
| Max/Min elimination | max_min_eliminate | Rewrites some max/min functions in aggregation to the `order by` + `limit 1` form. |
| Predicate pushdown | predicate_push_down | Tries to push predicates down to the operator that is closer to the data source. |
| Outer join elimination | outer_join_eliminate | Tries to remove the unnecessary left join or right join from the execution plan. |
| Partition pruning | partition_processor | Prunes partitions which are rejected by the predicates and rewrite partitioned table query to the `UnionAll + Partition Datasource` form. |
| Aggregation pushdown | aggregation_push_down | Tries to push aggregations down to their children. |
| TopN pushdown | topn_push_down | Tries to push the TopN operator to the place closer to the data source. |
| Join reorder | join_reorder | Decides the order of multi-table joins. |

### Disable optimization rules

You can use the blocklist of optimization rules to disable some of them if some rules lead to a sub-optimal execution plan for special queries.

#### Usage

> **Note:**
>
> All the following operations need the `super privilege` privilege of the database. Each optimization rule has a name. For example, the name of column pruning is `column_prune`. The names of all optimization rules can be found in the second column of the table [Important Optimization Rules](#important-optimization-rules).

- If you want to disable some rules, write its name to the `mysql.opt_rule_blacklist` table. For example:

    {{< copyable "sql" >}}

    ```sql
    insert into mysql.opt_rule_blacklist values("join_reorder"), ("topn_push_down");
    ```

    Executing the following SQL statement can make the above operation take effect immediately. The effective range includes all old connections of the corresponding TiDB server:

    {{< copyable "sql" >}}

    ```sql
    admin reload opt_rule_blacklist;
    ```

    > **Note:**
    >
    > `admin reload opt_rule_blacklist` only takes effect on the TiDB server where the above statement has been run. If you want all TiDB servers of the cluster to take effect, run this command on each TiDB server.

- If you want to re-enable a rule, delete the corresponding data in the table, and then run the `admin reload` statement:

    {{< copyable "sql" >}}

    ```sql
    delete from mysql.opt_rule_blacklist where name in ("join_reorder", "topn_push_down");
    ```

    {{< copyable "sql" >}}

    ```sql
    admin reload opt_rule_blacklist;
    ```

## The blocklist of expression pushdown

The blocklist of expression pushdown is one way to tune the expression pushdown, mainly used to manually disable some expressions of some specific data types.

### Expressions which are supported to be pushed down

| Expression Classification | Concrete Operations |
| :-------------- | :------------------------------------- |
| [Logical operations](/functions-and-operators/operators.md#logical-operators) | AND (&&), OR (&#124;&#124;), NOT (!) |
| [Comparison functions and operators](/functions-and-operators/operators.md#comparison-functions-and-operators) | <, <=, =, != (`<>`), >, >=, [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to), [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in), IS NULL, LIKE, IS TRUE, IS FALSE, [`COALESCE()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) |
| [Numeric functions and operators](/functions-and-operators/numeric-functions-and-operators.md) | +, -, *, /, [`ABS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs), [`CEIL()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil), [`CEILING()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling), [`FLOOR()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor) |
| [Control flow functions](/functions-and-operators/control-flow-functions.md) | [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case), [`IF()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_if), [`IFNULL()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_ifnull) |
| [JSON functions](/functions-and-operators/json-functions.md) | [JSON_TYPE(json_val)](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type),<br/> [JSON_EXTRACT(json_doc, path[, path] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract),<br/> [JSON_UNQUOTE(json_val)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote),<br/> [JSON_OBJECT(key, val[, key, val] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object),<br/> [JSON_ARRAY([val[, val] ...])](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array),<br/> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge),<br/> [JSON_SET(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set),<br/> [JSON_INSERT(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert),<br/> [JSON_REPLACE(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace),<br/> [JSON_REMOVE(json_doc, path[, path] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove) |
| [Date and time functions](/functions-and-operators/date-and-time-functions.md) | [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format)  |

### Disable the pushdown of specific expressions

When you get wrong results due to the expression pushdown, you can use the blocklist to make a quick recovery for the application. More specifically, you can add some of the supported functions or operators to the `mysql.expr_pushdown_blacklist` table to disable the pushdown of specific expressions.

The schema of `mysql.expr_pushdown_blacklist` is shown as follows:

{{< copyable "sql" >}}

```sql
desc mysql.expr_pushdown_blacklist;
```

```sql
+------------+--------------+------+------+-------------------+-------+
| Field      | Type         | Null | Key  | Default           | Extra |
+------------+--------------+------+------+-------------------+-------+
| name       | char(100)    | NO   |      | NULL              |       |
| store_type | char(100)    | NO   |      | tikv,tiflash,tidb |       |
| reason     | varchar(200) | YES  |      | NULL              |       |
+------------+--------------+------+------+-------------------+-------+
3 rows in set (0.00 sec)
```

Here is the description of each field above:

+ `name`: The name of the function that is disabled to be pushed down.
+ `store_type`: To specify the component that you want to prevent the function from being pushed down to for computing. Available components are `tidb`, `tikv`, and `tiflash`. The `store_type` is case-insensitive. If you need to specify multiple components, use a comma to separate each component.
    - When `store_type` is `tidb`, it indicates whether the function can be executed in other TiDB servers while the TiDB memory table is being read.
    - When `store_type` is `tikv`, it indicates whether the function can be executed in TiKV server's Coprocessor component.
    - When `store_type` is `tiflash`, it indicates whether the function can be executed in TiFlash Server's Coprocessor component.
+ `reason`: To record the reason why this function is added to the blocklist.

### Usage

This section describes how to use the blocklist of expression pushdown.

#### Add to the blocklist

To add one or more expressions (functions or operators) to the blocklist, perform the following steps:

1. Insert the corresponding function name or operator name, and the set of components you want to disable the pushdown, to the `mysql.expr_pushdown_blacklist` table.

2. Execute `admin reload expr_pushdown_blacklist`.

### Remove from the blocklist

To remove one or more expressions from the blocklist, perform the following steps:

1. Delete the corresponding function name or operator name, and the set of components you want to disable the pushdown, from the `mysql.expr_pushdown_blacklist` table.

2. Execute `admin reload expr_pushdown_blacklist`.

> **Note:**
>
> `admin reload expr_pushdown_blacklist` only takes effect on the TiDB server where this statement is run. If you want all TiDB servers of the cluster to take effect, run this command on each TiDB server.

## Expression blocklist usage example

In the following example, the `<` and `>` operators are added to the blocklist, and then the `>` operator is removed from the blocklist.

To judge whether the blocklist takes effect, observe the results of `EXPLAIN` (See [Optimize SQL statements using `EXPLAIN`](/explain-overview.md)).

1. The predicates `a < 2` and `a > 2` in the `WHERE` clause of the following SQL statement can be pushed down to TiKV.

    {{< copyable "sql" >}}

    ```sql
    explain select * from t where a < 2 and a > 2;
    ```

    ```sql
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | id                      | estRows  | task      | access object | operator info                      |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | TableReader_7           | 0.00     | root      |               | data:Selection_6                   |
    | └─Selection_6           | 0.00     | cop[tikv] |               | gt(ssb_1.t.a, 2), lt(ssb_1.t.a, 2) |
    |   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo     |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    3 rows in set (0.00 sec)
    ```

2. Insert the expression to the `mysql.expr_pushdown_blacklist` table and execute `admin reload expr_pushdown_blacklist`.

    {{< copyable "sql" >}}

    ```sql
    insert into mysql.expr_pushdown_blacklist values('<','tikv',''), ('>','tikv','');
    ```

    ```sql
    Query OK, 2 rows affected (0.01 sec)
    Records: 2  Duplicates: 0  Warnings: 0
    ```

    {{< copyable "sql" >}}

    ```sql
    admin reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

3. Observe the execution plan again and you will find that both the `<` and `>` operators are not pushed down to TiKV Coprocessor.

    {{< copyable "sql" >}}

    ```sql
    explain select * from t where a < 2 and a > 2;
    ```

    ```sql
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | id                      | estRows  | task      | access object | operator info                      |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | Selection_7             | 10000.00 | root      |               | gt(ssb_1.t.a, 2), lt(ssb_1.t.a, 2) |
    | └─TableReader_6         | 10000.00 | root      |               | data:TableFullScan_5               |
    |   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo     |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    3 rows in set (0.00 sec)
    ```

4. Remove one expression (here is `>`) from the blocklist and execute `admin reload expr_pushdown_blacklist`.

    {{< copyable "sql" >}}

    ```sql
    delete from mysql.expr_pushdown_blacklist where name = '>';
    ```

    ```sql
    Query OK, 1 row affected (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    admin reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

5. Observe the execution plan again and you will find that `<` is not pushed down while `>` is pushed down to TiKV Coprocessor.

    {{< copyable "sql" >}}

    ```sql
    explain select * from t where a < 2 and a > 2;
    ```

    ```sql
    +---------------------------+----------+-----------+---------------+--------------------------------+
    | id                        | estRows  | task      | access object | operator info                  |
    +---------------------------+----------+-----------+---------------+--------------------------------+
    | Selection_8               | 0.00     | root      |               | lt(ssb_1.t.a, 2)               |
    | └─TableReader_7           | 0.00     | root      |               | data:Selection_6               |
    |   └─Selection_6           | 0.00     | cop[tikv] |               | gt(ssb_1.t.a, 2)               |
    |     └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
    +---------------------------+----------+-----------+---------------+--------------------------------+
    4 rows in set (0.00 sec)
    ```

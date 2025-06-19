---
title: 优化规则和表达式下推的黑名单
summary: 了解如何使用黑名单来控制优化规则和表达式下推的行为。
---

# 优化规则和表达式下推的黑名单

本文档介绍如何使用优化规则黑名单和表达式下推黑名单来控制 TiDB 的行为。

## 优化规则黑名单

优化规则黑名单是调整优化规则的一种方式，主要用于手动禁用某些优化规则。

### 重要的优化规则

|**优化规则**|**规则名称**|**描述**|
| :--- | :--- | :--- |
| 列剪裁 | column_prune | 如果上层执行器不需要某列，则该操作符会将其剪裁掉。 |
| 子查询去相关 | decorrelate | 尝试将相关子查询重写为非相关连接或聚合。 |
| 聚合消除 | aggregation_eliminate | 尝试从执行计划中移除不必要的聚合操作符。 |
| 投影消除 | projection_eliminate | 从执行计划中移除不必要的投影操作符。 |
| 最大/最小值消除 | max_min_eliminate | 将聚合中的某些 max/min 函数重写为 `order by` + `limit 1` 形式。 |
| 谓词下推 | predicate_push_down | 尝试将谓词下推到更接近数据源的操作符。 |
| 外连接消除 | outer_join_eliminate | 尝试从执行计划中移除不必要的左连接或右连接。 |
| 分区裁剪 | partition_processor | 裁剪被谓词拒绝的分区，并将分区表查询重写为 `UnionAll + Partition Datasource` 形式。 |
| 聚合下推 | aggregation_push_down | 尝试将聚合下推到其子节点。 |
| TopN 下推 | topn_push_down | 尝试将 TopN 操作符下推到更接近数据源的位置。 |
| 连接重排序 | join_reorder | 决定多表连接的顺序。 |
| 从窗口函数推导 TopN 或 Limit | derive_topn_from_window | 从窗口函数推导出 TopN 或 Limit 操作符。 |

### 禁用优化规则

如果某些规则导致特定查询的执行计划不够优化，你可以使用优化规则黑名单来禁用这些规则。

#### 使用方法

> **注意：**
>
> 以下所有操作都需要数据库的 `super privilege` 权限。每个优化规则都有一个名称。例如，列剪裁的名称是 `column_prune`。所有优化规则的名称可以在[重要的优化规则](#重要的优化规则)表的第二列中找到。

- 如果你想禁用某些规则，将其名称写入 `mysql.opt_rule_blacklist` 表。例如：

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO mysql.opt_rule_blacklist VALUES("join_reorder"), ("topn_push_down");
    ```

    执行以下 SQL 语句可以使上述操作立即生效。生效范围包括相应 TiDB 服务器的所有旧连接：

    {{< copyable "sql" >}}

    ```sql
    admin reload opt_rule_blacklist;
    ```

    > **注意：**
    >
    > `admin reload opt_rule_blacklist` 只对运行该语句的 TiDB 服务器生效。如果你想让集群中的所有 TiDB 服务器都生效，需要在每个 TiDB 服务器上运行此命令。

- 如果你想重新启用某个规则，删除表中相应的数据，然后运行 `admin reload` 语句：

    {{< copyable "sql" >}}

    ```sql
    DELETE FROM mysql.opt_rule_blacklist WHERE name IN ("join_reorder", "topn_push_down");
    ```

    {{< copyable "sql" >}}

    ```sql
    admin reload opt_rule_blacklist;
    ```

## 表达式下推黑名单

表达式下推黑名单是调整表达式下推的一种方式，主要用于手动禁用某些特定数据类型的表达式。

### 支持下推的表达式

关于支持下推的表达式的更多信息，请参见[支持下推到 TiKV 的表达式](/functions-and-operators/expressions-pushed-down.md#支持下推到-tikv-的表达式)。

### 禁用特定表达式的下推

当由于表达式下推导致结果错误时，你可以使用黑名单来快速恢复应用程序。具体来说，你可以将一些支持的函数或运算符添加到 `mysql.expr_pushdown_blacklist` 表中，以禁用特定表达式的下推。

`mysql.expr_pushdown_blacklist` 的表结构如下：

{{< copyable "sql" >}}

```sql
DESC mysql.expr_pushdown_blacklist;
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

以下是每个字段的说明：

+ `name`：禁止下推的函数名称。
+ `store_type`：指定要阻止函数下推到哪个组件进行计算。可用的组件有 `tidb`、`tikv` 和 `tiflash`。`store_type` 不区分大小写。如果需要指定多个组件，使用逗号分隔每个组件。
    - 当 `store_type` 为 `tidb` 时，表示在读取 TiDB 内存表时该函数是否可以在其他 TiDB 服务器中执行。
    - 当 `store_type` 为 `tikv` 时，表示该函数是否可以在 TiKV 服务器的 Coprocessor 组件中执行。
    - 当 `store_type` 为 `tiflash` 时，表示该函数是否可以在 TiFlash 服务器的 Coprocessor 组件中执行。
+ `reason`：记录将此函数添加到黑名单的原因。

### 使用方法

本节描述如何使用表达式下推黑名单。

#### 添加到黑名单

要将一个或多个表达式（函数或运算符）添加到黑名单，请执行以下步骤：

1. 将相应的函数名称或运算符名称，以及你想禁用下推的组件集合，插入到 `mysql.expr_pushdown_blacklist` 表中。

2. 执行 `admin reload expr_pushdown_blacklist`。

### 从黑名单中移除

要从黑名单中移除一个或多个表达式，请执行以下步骤：

1. 从 `mysql.expr_pushdown_blacklist` 表中删除相应的函数名称或运算符名称，以及你想禁用下推的组件集合。

2. 执行 `admin reload expr_pushdown_blacklist`。

> **注意：**
>
> `admin reload expr_pushdown_blacklist` 只对运行该语句的 TiDB 服务器生效。如果你想让集群中的所有 TiDB 服务器都生效，需要在每个 TiDB 服务器上运行此命令。

## 表达式黑名单使用示例

在以下示例中，将 `<` 和 `>` 运算符添加到黑名单，然后将 `>` 运算符从黑名单中移除。

要判断黑名单是否生效，请观察 `EXPLAIN` 的结果（参见 [TiDB 执行计划概览](/explain-overview.md)）。

1. 以下 SQL 语句中 `WHERE` 子句中的谓词 `a < 2` 和 `a > 2` 可以下推到 TiKV。

    {{< copyable "sql" >}}

    ```sql
    EXPLAIN SELECT * FROM t WHERE a < 2 AND a > 2;
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

2. 将表达式插入到 `mysql.expr_pushdown_blacklist` 表并执行 `admin reload expr_pushdown_blacklist`。

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO mysql.expr_pushdown_blacklist VALUES('<','tikv',''), ('>','tikv','');
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

3. 再次观察执行计划，你会发现 `<` 和 `>` 运算符都没有下推到 TiKV Coprocessor。

    {{< copyable "sql" >}}

    ```sql
    EXPLAIN SELECT * FROM t WHERE a < 2 and a > 2;
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

4. 从黑名单中移除一个表达式（这里是 `>`）并执行 `admin reload expr_pushdown_blacklist`。

    {{< copyable "sql" >}}

    ```sql
    DELETE FROM mysql.expr_pushdown_blacklist WHERE name = '>';
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

5. 再次观察执行计划，你会发现 `<` 没有下推，而 `>` 下推到了 TiKV Coprocessor。

    {{< copyable "sql" >}}

    ```sql
    EXPLAIN SELECT * FROM t WHERE a < 2 AND a > 2;
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

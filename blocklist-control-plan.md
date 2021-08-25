---
title: 优化规则与表达式下推的黑名单
summary: 了解优化规则与表达式下推的黑名单。
---

# 优化规则与表达式下推的黑名单

本文主要介绍优化规则的黑名单与表达式下推的黑名单。

## 优化规则黑名单

**优化规则黑名单**是针对优化规则的调优手段之一，主要用于手动禁用一些优化规则。

### 重要的优化规则

|**优化规则**|**规则名称**|**简介**|
| :--- | :--- | :--- |
| 列裁剪 | column_prune | 对于上层算子不需要的列，不在下层算子输出该列，减少计算 |
| 子查询去关联 | decorrelate | 尝试对相关子查询进行改写，将其转换为普通 join 或 aggregation 计算 |
| 聚合消除 | aggregation_eliminate | 尝试消除执行计划中的某些不必要的聚合算子 |
| 投影消除 | projection_eliminate |  消除执行计划中不必要的投影算子 |
| 最大最小消除 | max_min_eliminate | 改写聚合中的 max/min 计算，转化为 `order by` + `limit 1` |
| 谓词下推 | predicate_push_down | 尝试将执行计划中过滤条件下推到离数据源更近的算子上 |
| 外连接消除 | outer_join_eliminate | 尝试消除执行计划中不必要的 left join 或者 right join |
| 分区裁剪 | partition_processor | 将分区表查询改成为用 union all，并裁剪掉不满足过滤条件的分区 |
| 聚合下推 | aggregation_push_down | 尝试将执行计划中的聚合算子下推到更底层的计算节点 |
| TopN 下推 | topn_push_down | 尝试将执行计划中的 TopN 算子下推到离数据源更近的算子上 |
| Join 重排序 | join_reorder | 对多表 join 确定连接顺序 |

### 禁用优化规则

当某些优化规则在一些特殊查询中的优化结果不理想时，可以使用**优化规则黑名单**禁用一些优化规则。

#### 使用方法

> **注意：**
>
> 以下操作都需要数据库的 super privilege 权限。每个优化规则都有各自的名字，比如列裁剪的名字是 "column_prune"。所有优化规则的名字都可以在[重要的优化规则](#重要的优化规则)表格中第二列查到。

- 如果你想禁用某些规则，可以在 `mysql.opt_rule_blacklist` 表中写入规则的名字，例如：

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO mysql.opt_rule_blacklist VALUES("join_reorder"), ("topn_push_down");
    ```

    执行以下 SQL 语句可让禁用规则立即生效，包括相应 TiDB Server 的所有旧链接：

    {{< copyable "sql" >}}

    ```sql
    ADMIN reload opt_rule_blacklist;
    ```

    > **注意：**
    >
    > `admin reload opt_rule_blacklist` 只对执行该 SQL 语句的 TiDB server 生效。若需要集群中所有 TiDB server 生效，需要在每台 TiDB server 上执行该 SQL 语句。

- 需要解除一条规则的禁用时，需要删除表中禁用该条规则的相应数据，再执行 `admin reload`：

    {{< copyable "sql" >}}

    ```sql
    DELETE FROM mysql.opt_rule_blacklist WHERE name IN ("join_reorder", "topn_push_down");
    admin reload opt_rule_blacklist;
    ```

## 表达式下推黑名单

**表达式下推黑名单**是针对表达式下推的调优手段之一，主要用于对于某些存储类型手动禁用一些表达式。

### 已支持下推的表达式

| 表达式分类 | 具体操作 |
| :-------------- | :------------------------------------- |
| [逻辑运算](/functions-and-operators/operators.md#逻辑操作符) | AND (&&), OR (&#124;&#124;), NOT (!) |
| [比较运算](/functions-and-operators/operators.md#比较方法和操作符) | <, <=, =, != (`<>`), >, >=, [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to), [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in), IS NULL, LIKE, IS TRUE, IS FALSE, [`COALESCE()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) |
| [数值运算](/functions-and-operators/numeric-functions-and-operators.md) | +, -, *, /, [`ABS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs), [`CEIL()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil), [`CEILING()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling), [`FLOOR()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor) |
| [控制流运算](/functions-and-operators/control-flow-functions.md) | [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case), [`IF()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_if), [`IFNULL()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_ifnull) |
| [JSON 运算](/functions-and-operators/json-functions.md) | [JSON_TYPE(json_val)](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type),<br/> [JSON_EXTRACT(json_doc, path[, path] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract),<br/> [JSON_UNQUOTE(json_val)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote),<br/> [JSON_OBJECT(key, val[, key, val] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object),<br/> [JSON_ARRAY([val[, val] ...])](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array),<br/> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge),<br/> [JSON_SET(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set),<br/> [JSON_INSERT(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert),<br/> [JSON_REPLACE(json_doc, path, val[, path, val] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace),<br/> [JSON_REMOVE(json_doc, path[, path] ...)](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove) |
| [日期运算](/functions-and-operators/date-and-time-functions.md) | [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format)  |

### 禁止特定表达式下推

当函数的计算过程由于下推而出现异常时，可通过黑名单功能禁止其下推来快速恢复业务。具体而言，你可以将上述支持的函数或运算符名加入黑名单 `mysql.expr_pushdown_blacklist` 中，以禁止特定表达式下推。

`mysql.expr_pushdown_blacklist` 的 schema 如下：

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

以上结果字段解释如下：

+ `name`：禁止下推的函数名。
+ `store_type`：用于指明希望禁止该函数下推到哪些组件进行计算。组件可选 `tidb`、`tikv` 和 `tiflash`。`store_type` 不区分大小写，如果需要禁止向多个存储引擎下推，各个存储之间需用逗号隔开。
    - `store_type` 为 `tidb` 时表示在读取 TiDB 内存表时，是否允许该函数在其他 TiDB Server 上执行。
    - `store_type` 为 `tikv` 时表示是否允许该函数在 TiKV Server 的 Coprocessor 模块中执行。
    - `store_type` 为 `tiflash` 时表示是否允许该函数在 TiFlash Server 的 Coprocessor 模块中执行。
+ `reason`：用于记录该函数被加入黑名单的原因。

### 使用方法

#### 加入黑名单

如果要将一个或多个函数或运算符加入黑名单，执行以下步骤：

1. 向 `mysql.expr_pushdown_blacklist` 插入对应的函数名或运算符名以及希望禁止下推的存储引擎集合。

2. 执行 `admin reload expr_pushdown_blacklist;`。

#### 移出黑名单

如果要将一个或多个函数及运算符移出黑名单，执行以下步骤：

1. 从 `mysql.expr_pushdown_blacklist` 表中删除对应的函数名或运算符名。

2. 执行 `admin reload expr_pushdown_blacklist;`。

> **注意：**
>
> `admin reload expr_pushdown_blacklist` 只对执行该 SQL 语句的 TiDB server 生效。若需要集群中所有 TiDB server 生效，需要在每台 TiDB server 上执行该 SQL 语句。

### 表达式黑名单用法示例

以下示例首先将运算符 `<` 及 `>` 加入黑名单，然后将运算符 `>` 从黑名单中移出。

黑名单是否生效可以从 `explain` 结果中进行观察（参见 [`EXPLAIN` 简介](/explain-overview.md#explain-简介)）。

1. 对于以下 SQL 语句，`where` 条件中的 `a < 2` 和 `a > 2` 可以下推到 TiKV 进行计算。

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

2. 往 `mysql.expr_pushdown_blacklist` 表中插入禁用表达式，并且执行 `admin reload expr_pushdown_blacklist`。

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
    ADMIN reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

3. 重新观察执行计划，发现表达式下推黑名单生效，`where` 条件中的 `<` 和 `>` 没有被下推到 TiKV Coprocessor 上。

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

4. 将某一表达式（`>` 大于）禁用规则从黑名单表中删除，并且执行 `admin reload expr_pushdown_blacklist`。

    {{< copyable "sql" >}}

    ```sql
    DELETE FROM mysql.expr_pushdown_blacklist WHERE name = '>';
    ```

    ```sql
    Query OK, 1 row affected (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    ADMIN reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

5. 重新观察执行计划，可以看到只有 `>` 表达式被重新下推到 TiKV Coprocessor，`<` 表达式仍然被禁用下推。

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

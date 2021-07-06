---
title: 下推到 TiKV 的表达式列表
summary: TiDB 中下推到 TiKV 的表达式列表及相关设置。
aliases: ['/docs-cn/dev/functions-and-operators/expressions-pushed-down/','/docs-cn/dev/reference/sql/functions-and-operators/expressions-pushed-down/']
---

# 下推到 TiKV 的表达式列表

当 TiDB 从 TiKV 中读取数据的时候，TiDB 会尽量下推一些表达式运算到 TiKV 中，从而减少数据传输量以及 TiDB 单一节点的计算压力。本文将介绍 TiDB 已支持下推的表达式，以及如何禁止下推特定表达式。

## 已支持下推的表达式列表

| 表达式分类 | 具体操作 |
| :-------------- | :------------------------------------- |
| [逻辑运算](/functions-and-operators/operators.md#逻辑操作符) | AND (&&), OR (&#124;&#124;), NOT (!) |
| [比较运算](/functions-and-operators/operators.md#比较方法和操作符) | <, <=, =, != (`<>`), >, >=, [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to), [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in), IS NULL, LIKE, IS TRUE, IS FALSE, [`COALESCE()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) |
| [数值运算](/functions-and-operators/numeric-functions-and-operators.md) | +, -, *, /, [`ABS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs), [`CEIL()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil), [`CEILING()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling), [`FLOOR()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor) |
| [控制流运算](/functions-and-operators/control-flow-functions.md) | [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case), [`IF()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_if), [`IFNULL()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_ifnull) |
| [JSON运算](/functions-and-operators/json-functions.md) | [JSON_TYPE(json_val)][json_type],<br/> [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract],<br/> [JSON_OBJECT(key, val[, key, val] ...)][json_object],<br/> [JSON_ARRAY([val[, val] ...])][json_array],<br/> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge],<br/> [JSON_SET(json_doc, path, val[, path, val] ...)][json_set],<br/> [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert],<br/> [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace],<br/> [JSON_REMOVE(json_doc, path[, path] ...)][json_remove] |
| [日期运算](/functions-and-operators/date-and-time-functions.md) | [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format)  |

## 禁止特定表达式下推

当函数的计算过程由于下推而出现异常时，可通过黑名单功能禁止其下推来快速恢复业务。具体而言，你可以将上述支持的函数或运算符名加入黑名单 `mysql.expr_pushdown_blacklist` 中，以禁止特定表达式下推。

`mysql.expr_pushdown_blacklist` 的 schema 如下：

```sql
tidb> desc mysql.expr_pushdown_blacklist;
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

> **注意：**：
>
> `tidb` 是一种特殊的 store_type，其含义是 TiDB 内存表，比如：`PERFORMANCE_SCHEMA.events_statements_summary_by_digest`，属于系统表的一种，非特殊情况不用考虑这种存储引擎。

### 加入黑名单

执行以下步骤，可将一个或多个函数或运算符加入黑名单：

1. 向 `mysql.expr_pushdown_blacklist` 插入对应的函数名或运算符名以及希望禁止下推的存储类型集合。
2. 执行 `admin reload expr_pushdown_blacklist;`。

### 移出黑名单

执行以下步骤，可将一个或多个函数及运算符移出黑名单：

1. 从 `mysql.expr_pushdown_blacklist` 表中删除对应的函数名或运算符名。
2. 执行 `admin reload expr_pushdown_blacklist;`。

### 黑名单用法示例

以下示例首先将运算符 `<` 及 `>` 加入黑名单，然后将运算符 `>` 从黑名单中移出。

黑名单是否生效可以从 `explain` 结果中进行观察（参见[如何理解 `explain` 结果](/explain-overview.md)）。

```sql
tidb> create table t(a int);
Query OK, 0 rows affected (0.06 sec)

tidb> explain select * from t where a < 2 and a > 2;
+-------------------------+----------+-----------+---------------+------------------------------------+
| id                      | estRows  | task      | access object | operator info                      |
+-------------------------+----------+-----------+---------------+------------------------------------+
| TableReader_7           | 0.00     | root      |               | data:Selection_6                   |
| └─Selection_6           | 0.00     | cop[tikv] |               | gt(ssb_1.t.a, 2), lt(ssb_1.t.a, 2) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo     |
+-------------------------+----------+-----------+---------------+------------------------------------+
3 rows in set (0.00 sec)

tidb> insert into mysql.expr_pushdown_blacklist values('<', 'tikv',''), ('>','tikv','');
Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0

tidb> admin reload expr_pushdown_blacklist;
Query OK, 0 rows affected (0.00 sec)

tidb> explain select * from t where a < 2 and a > 2;
+-------------------------+----------+-----------+---------------+------------------------------------+
| id                      | estRows  | task      | access object | operator info                      |
+-------------------------+----------+-----------+---------------+------------------------------------+
| Selection_7             | 10000.00 | root      |               | gt(ssb_1.t.a, 2), lt(ssb_1.t.a, 2) |
| └─TableReader_6         | 10000.00 | root      |               | data:TableFullScan_5               |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo     |
+-------------------------+----------+-----------+---------------+------------------------------------+
3 rows in set (0.00 sec)

tidb> delete from mysql.expr_pushdown_blacklist where name = '>';
Query OK, 1 row affected (0.01 sec)

tidb> admin reload expr_pushdown_blacklist;
Query OK, 0 rows affected (0.00 sec)

tidb> explain select * from t where a < 2 and a > 2;
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

> **注意：**
>
> - `admin reload expr_pushdown_blacklist` 只对执行该 SQL 语句的 TiDB server 生效。若需要集群中所有 TiDB server 生效，需要在每台 TiDB server 上执行该 SQL 语句。
> - 表达式黑名单功能在 v3.0.0 及以上版本中支持。
> - 在 v3.0.3 及以下版本中，不支持将某些运算符的原始名称文本（如 ">"、"+" 和 "is null"）加入黑名单中，部分运算符在黑名单中需使用别名。已支持下推的表达式中，别名与原始名不同的运算符见下表（区分大小写）。

| 运算符原始名称 | 运算符别名 |
| :-------- | :---------- |
| < | lt |
| > | gt |
| <= | le |
| >= | ge |
| = | eq |
| != | ne |
| `<>` | ne |
| `<=>` | nulleq |
| &#124; | bitor |
| && | bitand|
| &#124;&#124; | or |
| ! | not |
| in | in |
| + | plus|
| - | minus |
| * | mul |
| / | div |
| DIV | intdiv|
| IS NULL | isnull |
| IS TRUE | istrue |
| IS FALSE | isfalse |

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_short_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path
[json_short_extract_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path
[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_merge_preserve]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge-preserve
[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
[json_keys]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-keys
[json_length]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length
[json_valid]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-valid
[json_quote]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-quote
[json_contains]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains
[json_contains_path]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path
[json_arrayagg]:https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-arrayagg
[json_depth]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-depth

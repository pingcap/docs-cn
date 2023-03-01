---
title: List of Expressions for Pushdown
summary: Learn a list of expressions that can be pushed down to TiKV and the related operations.
aliases: ['/docs/dev/functions-and-operators/expressions-pushed-down/','/docs/dev/reference/sql/functions-and-operators/expressions-pushed-down/']
---

# List of Expressions for Pushdown

When TiDB reads data from TiKV, TiDB tries to push down some expressions (including calculations of functions or operators) to be processed to TiKV. This reduces the amount of transferred data and offloads processing from a single TiDB node. This document introduces the expressions that TiDB already supports pushing down and how to prohibit specific expressions from being pushed down using blocklist.

Tiflash also supports pushdown for the functions and operators [listed on this page](/tiflash/tiflash-supported-pushdown-calculations.md).

## Supported expressions for pushdown to TiKV

| Expression Type | Operations |
| :-------------- | :------------------------------------- |
| [Logical operators](/functions-and-operators/operators.md#logical-operators) | AND (&&), OR (&#124;&#124;), NOT (!) |
| [Comparison functions and operators](/functions-and-operators/operators.md#comparison-functions-and-operators) | <, <=, =, != (`<>`), >, >=, [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to), [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in), IS NULL, LIKE, IS TRUE, IS FALSE, [`COALESCE()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) |
| [Numeric functions and operators](/functions-and-operators/numeric-functions-and-operators.md) | +, -, *, /, [`ABS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs), [`CEIL()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil), [`CEILING()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling), [`FLOOR()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor), [`MOD()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_mod) |
| [Control flow functions](/functions-and-operators/control-flow-functions.md) | [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#operator_case), [`IF()`](https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#function_if), [`IFNULL()`](https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#function_ifnull) |
| [JSON functions](/functions-and-operators/json-functions.md) | [JSON_TYPE(json_val)][json_type],<br/> [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract],<br/> [JSON_OBJECT(key, val[, key, val] ...)][json_object],<br/> [JSON_ARRAY([val[, val] ...])][json_array],<br/> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge],<br/> [JSON_SET(json_doc, path, val[, path, val] ...)][json_set],<br/> [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert],<br/> [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace],<br/> [JSON_REMOVE(json_doc, path[, path] ...)][json_remove] |
| [Date and time functions](/functions-and-operators/date-and-time-functions.md) | [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format), [`SYSDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_sysdate) |
| [String functions](/functions-and-operators/string-functions.md) | [`RIGHT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_right) |

## Blocklist specific expressions

If unexpected behavior occurs in the calculation process when pushing down the [supported expressions](#supported-expressions-for-pushdown-to-tikv) or specific data types (**only** the [`ENUM` type](/data-type-string.md#enum-type) and the [`BIT` type](/data-type-numeric.md#bit-type)), you can restore the application quickly by prohibiting the pushdown of the corresponding functions, operators, or data types. Specifically, you can prohibit the functions, operators, or data types from being pushed down by adding them to the blocklist `mysql.expr_pushdown_blacklist`. For details, refer to [Add to the blocklist](#add-to-the-blocklist).

The schema of `mysql.expr_pushdown_blacklist` is as follows:

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

Field description:

+ `name`: the name of the function, operator, or data type that is prohibited from being pushed down.
+ `store_type`: specifies to which storage engine the function, operator, or data type is prohibited from being pushed down. Currently, TiDB supports the three storage engines: `tikv`, `tidb`, and `tiflash`. `store_type` is case-insensitive. If a function is prohibited from being pushed down to multiple storage engines, use a comma to separate each engine.
+ `reason` : The reason why the function is blocklisted.

### Add to the blocklist

To add one or more [functions, operators](#supported-expressions-for-pushdown-to-tikv), or data types (**only** the [`ENUM` type](/data-type-string.md#enum-type) and the [`BIT` type](/data-type-numeric.md#bit-type)) to the blocklist, perform the following steps:

1. Insert the followings to `mysql.expr_pushdown_blacklist`:

    - the name of the function, operator, or data type to be prohibited from being pushed down
    - the storage engine to be prohibited from being pushed down

2. Execute the `admin reload expr_pushdown_blacklist;` command.

### Remove from the blocklist

To remove one or more functions, operators, or data types from the blocklist, perform the following steps:

1. Delete the name of the function, operator, or data type in `mysql.expr_pushdown_blacklist`.

2. Execute the `admin reload expr_pushdown_blacklist;` command.

### Blocklist usage examples

The following example demonstrates how to add the `DATE_FORMAT()` function, `>` operator, and `BIT` data type to the blocklist, then remove `>` from the blocklist.

You can see whether the blocklist takes effect by checking the results returned by `EXPLAIN` statement (See [Understanding `EXPLAIN` results](/explain-overview.md)).

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

tidb> insert into mysql.expr_pushdown_blacklist values('date_format()', 'tikv',''), ('>','tikv',''), ('bit','tikv','');
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

> **Note:**
>
> - `admin reload expr_pushdown_blacklist` only takes effect on the TiDB server that executes this SQL statement. To make it apply to all TiDB servers, execute the SQL statement on each TiDB server.
> - The feature of blocklisting specific expressions is supported in TiDB 3.0.0 or later versions.
> - TiDB 3.0.3 or earlier versions does not support adding some of the operators (such as ">", "+", "is null") to the blocklist by using their original names. You need to use their aliases (case-sensitive) instead, as shown in the following table:

| Operator Name | Aliases |
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

[json_arrayagg]: https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_json-arrayagg

[json_depth]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-depth

---
title: Cast 函数和操作符
aliases: ['/docs-cn/dev/functions-and-operators/cast-functions-and-operators/','/docs-cn/dev/reference/sql/functions-and-operators/cast-functions-and-operators/']
summary: Cast 函数和操作符用于将某种数据类型的值转换为另一种数据类型。TiDB 支持使用 MySQL 8.0 中提供的所有 Cast 函数和操作符。
---

# Cast 函数和操作符

Cast 函数和操作符用于将某种数据类型的值转换为另一种数据类型。TiDB 支持使用 MySQL 8.0 中提供的所有 [Cast 函数和操作符](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html)。

## Cast 函数和操作符表

| 函数和操作符名 | 功能描述 |
| --------------- | ----------------------------------- |
| [`BINARY`](#binary) | 将一个字符串转换成一个二进制字符串 |
| [`CAST()`](#cast) | 将一个值转换成一个确定类型 |
| [`CONVERT()`](#convert) | 将一个值转换成一个确定类型 |

> **注意：**
>
> TiDB 和 MySQL 对于 `SELECT CAST(MeN AS CHAR)`（或者等价的 `SELECT CONVERT(MeM, CHAR)`）的结果显示不一致，其中 `MeN` 是用科学计数法表示的双精度浮点数。MySQL 在 `-15 <= N <= 14` 时显示完整数值，在 `N < -15` 或 `N > 14` 时显示科学计数法。而 TiDB 始终显示完整数值。例如，MySQL 对于 `SELECT CAST(3.1415e15 AS CHAR)` 的显示结果为 `3.1415e15`，而 TiDB 的显示结果为 `3141500000000000`。

## BINARY

[`BINARY`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#operator_binary) 运算符从 MySQL 8.0.27 版本起已被废弃。建议在 TiDB 和 MySQL 中都改用 `CAST(... AS BINARY)`。

## CAST

[`CAST(<expression> AS <type> [ARRAY])`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast) 函数用于将一个表达式的值转换为指定的数据类型。

此外，你还可以将该函数用于创建[多值索引](/sql-statements/sql-statement-create-index.md#多值索引)。

支持的数据类型包括：

| 类型                 | 描述             | 是否可用于多值索引                        |
|----------------------|------------------|------------------------------------------------|
| `BINARY(n)`          | 二进制字符串     | 否                                             |
| `CHAR(n)`            | 字符串           | 是，但仅当指定了长度时才有效                       |
| `DATE`               | 日期             | 是                                             |
| `DATETIME(fsp)`      | 日期/时间，其中 `fsp` 是可选的 | 是                            |
| `DECIMAL(n, m)`      | 十进制数，其中 `n` 和 `m` 是可选的，如果未指定，则默认为 `10` 和 `0` | 否 |
| `DOUBLE`             | 双精度浮点数     | 否                                             |
| `FLOAT(n)`           | 浮点数，其中 `n` 是可选的，应介于 `0` 和 `53` 之间 | 否                  |
| `JSON`               | JSON             | 否                                             |
| `REAL`               | 浮点数           | 是                                             |
| `SIGNED [INTEGER]`   | 有符号整数       | 是                                             |
| `TIME(fsp)`          | 时间             | 是                                             |
| `UNSIGNED [INTEGER]` | 无符号整数       | 是                                             |
| `VECTOR`             | 向量            | 否                                             |
| `YEAR`               | 年               | 否                                             |

示例：

以下语句将二进制字符串从十六进制文字转换为 `CHAR`。

```sql
SELECT CAST(0x54694442 AS CHAR);
```

```sql
+--------------------------+
| CAST(0x54694442 AS CHAR) |
+--------------------------+
| TiDB                     |
+--------------------------+
1 row in set (0.0002 sec)
```

以下语句将从 JSON 列中提取的 `a` 属性的值转换为无符号数组。需要注意的是，该函数只有作为多值索引定义的一部分时，才支持将数据转换为数组。

```sql
CREATE TABLE t (
    id INT PRIMARY KEY,
    j JSON,
    INDEX idx_a ((CAST(j->'$.a' AS UNSIGNED ARRAY)))
);
INSERT INTO t VALUES (1, JSON_OBJECT('a',JSON_ARRAY(1,2,3)));
INSERT INTO t VALUES (2, JSON_OBJECT('a',JSON_ARRAY(4,5,6)));
INSERT INTO t VALUES (3, JSON_OBJECT('a',JSON_ARRAY(7,8,9)));
ANALYZE TABLE t;
```

```sql
 EXPLAIN SELECT * FROM t WHERE 1 MEMBER OF(j->'$.a')\G
*************************** 1. row ***************************
           id: IndexMerge_10
      estRows: 2.00
         task: root
access object: 
operator info: type: union
*************************** 2. row ***************************
           id: ├─IndexRangeScan_8(Build)
      estRows: 2.00
         task: cop[tikv]
access object: table:t, index:idx_a(cast(json_extract(`j`, _utf8mb4'$.a') as unsigned array))
operator info: range:[1,1], keep order:false, stats:partial[j:unInitialized]
*************************** 3. row ***************************
           id: └─TableRowIDScan_9(Probe)
      estRows: 2.00
         task: cop[tikv]
access object: table:t
operator info: keep order:false, stats:partial[j:unInitialized]
3 rows in set (0.00 sec)
```

## CONVERT

[`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) 函数用于在[字符集](/character-set-and-collation.md)之间进行转换。

示例：

```sql
SELECT CONVERT(0x616263 USING utf8mb4);
```

```sql
+---------------------------------+
| CONVERT(0x616263 USING utf8mb4) |
+---------------------------------+
| abc                             |
+---------------------------------+
1 row in set (0.0004 sec)
```

## MySQL 兼容性

- TiDB 不支持对空间类型 (`SPATIAL`) 进行转换操作。更多信息，请参考 [#6347](https://github.com/pingcap/tidb/issues/6347)。
- TiDB 不支持在 `CAST()` 中使用 `AT TIME ZONE`。更多信息，请参考 [#51742](https://github.com/pingcap/tidb/issues/51742)。
- `CAST(24 AS YEAR)` 在 TiDB 中返回的结果为两位数字，而在 MySQL 中返回的结果为四位数字。更多信息，请参考 [#29629](https://github.com/pingcap/tidb/issues/29629)。
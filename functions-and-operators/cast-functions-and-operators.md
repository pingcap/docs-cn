---
title: 类型转换函数和运算符
summary: 了解类型转换函数和运算符。
---

# 类型转换函数和运算符

类型转换函数和运算符允许将值从一种数据类型转换为另一种数据类型。TiDB 支持 MySQL 8.0 中提供的所有[类型转换函数和运算符](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html)。

| 名称 | 描述 |
| ---------------------------------------- | -------------------------------- |
| [`BINARY`](#binary) | 将字符串转换为二进制字符串 |
| [`CAST()`](#cast) | 将值转换为指定类型 |
| [`CONVERT()`](#convert) | 将值转换为指定类型 |

> **注意：**
>
> TiDB 和 MySQL 对于 `SELECT CAST(MeN AS CHAR)`（或其等效形式 `SELECT CONVERT(MeM, CHAR)`）显示不一致的结果，其中 `MeN` 表示科学记数法中的双精度浮点数。当 `-15 <= N <= 14` 时，MySQL 显示完整的数值，当 `N < -15` 或 `N > 14` 时显示科学记数法。但是，TiDB 始终显示完整的数值。例如，MySQL 显示 `SELECT CAST(3.1415e15 AS CHAR)` 的结果为 `3.1415e15`，而 TiDB 显示结果为 `3141500000000000`。

## BINARY

[`BINARY`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#operator_binary) 运算符自 MySQL 8.0.27 起已被弃用。建议在 TiDB 和 MySQL 中都使用 `CAST(... AS BINARY)` 代替。

## CAST

[`CAST(<expression> AS <type> [ARRAY])`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast) 函数用于将表达式转换为指定类型。

此函数也用于创建[多值索引](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)。

支持以下类型：

| 类型 | 描述 | 是否可用于多值索引 |
|----------------------|------------------|------------------------------------------------------------|
| `BINARY(n)` | 二进制字符串 | 否 |
| `CHAR(n)` | 字符串 | 是，但仅当指定长度时 |
| `DATE` | 日期 | 是 |
| `DATETIME(fsp)` | 日期/时间，其中 `fsp` 是可选的 | 是 |
| `DECIMAL(n, m)` | 十进制数，其中 `n` 和 `m` 是可选的，如果未指定则分别为 `10` 和 `0` | 否 |
| `DOUBLE` | 双精度浮点数 | 否 |
| `FLOAT(n)` | 浮点数，其中 `n` 是可选的，应在 `0` 到 `53` 之间 | 否 |
| `JSON` | JSON | 否 |
| `REAL` | 浮点数 | 是 |
| `SIGNED [INTEGER]` | 有符号整数 | 是 |
| `TIME(fsp)` | 时间 | 是 |
| `UNSIGNED [INTEGER]` | 无符号整数 | 是 |
| `YEAR` | 年份 | 否 |

示例：

以下语句将十六进制字面量的二进制字符串转换为 `CHAR`。

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

以下语句将从 JSON 列中提取的 `a` 属性的值转换为无符号数组。注意，转换为数组仅支持作为多值索引定义的一部分。

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

- TiDB 不支持对 `SPATIAL` 类型进行类型转换操作。更多信息，请参见 [#6347](https://github.com/pingcap/tidb/issues/6347)。
- TiDB 不支持 `CAST()` 的 `AT TIME ZONE`。更多信息，请参见 [#51742](https://github.com/pingcap/tidb/issues/51742)。
- `CAST(24 AS YEAR)` 在 TiDB 中返回 2 位数字，在 MySQL 中返回 4 位数字。更多信息，请参见 [#29629](https://github.com/pingcap/tidb/issues/29629)。

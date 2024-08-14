---
title: JSON 数据类型
aliases: ['/docs-cn/dev/data-type-json/','/docs-cn/dev/reference/sql/data-types/json/']
summary: JSON 类型存储半结构化数据，使用 Binary 格式序列化，加快查询和解析速度。JSON 字段不能创建索引，但可以对 JSON 文档中的子字段创建索引。TiDB 仅支持下推部分 JSON 函数到 TiFlash，不建议使用 BR 恢复包含 JSON 列的数据到 v6.3.0 之前的 TiDB 集群。请勿同步非标准 JSON 类型的数据。MySQL 误标记二进制类型数据为 STRING 类型，TiDB 保持正确的二进制类型。ENUM 或 SET 数据类型转换为 JSON 时，TiDB 会检查格式正确性。TiDB 支持使用 ORDER BY 对 JSON Array 或 JSON Object 进行排序。在 INSERT JSON 列时，TiDB 会将值隐式转换为 JSON。
---

# JSON 数据类型

JSON 类型可以存储 JSON 这种半结构化的数据，相比于直接将 JSON 存储为字符串，它的好处在于：

1. 使用 Binary 格式进行序列化，对 JSON 的内部字段的查询、解析加快；
2. 多了 JSON 合法性验证的步骤，只有合法的 JSON 文档才可以放入这个字段中；

JSON 字段本身上，并不能创建索引，但是可以对 JSON 文档中的某个子字段创建索引。例如：

```sql
CREATE TABLE city (
    id INT PRIMARY KEY,
    detail JSON,
    population INT AS (JSON_EXTRACT(detail, '$.population')),
    index index_name (population)
);
INSERT INTO city (id,detail) VALUES (1, '{"name": "Beijing", "population": 100}');
SELECT id FROM city WHERE population >= 100;
```

更多信息，请参考 [JSON 函数](/functions-and-operators/json-functions.md)和[生成列](/generated-columns.md)。

## JSON 值的类型

JSON 文档中的每个值都属于一种特定的数据类型。可以通过 [`JSON_TYPE`()](/functions-and-operators/json-functions/json-functions-return.md#json_type) 的输出结果查看。

| 类型             | 示例                        |
|------------------|--------------------------------|
| ARRAY            | `[]`                           |
| BIT              |                                |
| BLOB             | `0x616263`                          |
| BOOLEAN          | `true`                         |
| DATE             | `"2025-06-14"`                 |
| DATETIME         | `"2025-06-14 09:05:10.000000"` |
| DOUBLE           | `1.14`                         |
| INTEGER          | `5`                            |
| NULL             | `null`                         |
| OBJECT           | `{}`                           |
| OPAQUE           |                                |
| STRING           | `"foobar"`                     |
| TIME             | `"09:10:00.000000"`            |
| UNSIGNED INTEGER | `9223372036854776000`          |

## 使用限制

- 目前 TiDB 仅支持下推部分 JSON 函数到 TiFlash。详情请参考 [TiFlash 支持下推的表达式](/tiflash/tiflash-supported-pushdown-calculations.md#支持下推的表达式)。
- TiDB Backup & Restore（BR）在 v6.3.0 版本对 JSON 列的数据的编码进行了修改。因此不建议使用 BR 恢复包含 JSON 列的数据到 v6.3.0 之前的 TiDB 集群。
- 请勿使用任何同步工具同步非标准 JSON 类型（例如 DATE、DATETIME、TIME 等）的数据。

## MySQL 兼容性

- 当使用二进制类型数据创建 JSON 时，目前 MySQL 会将其误标记为 STRING 类型，而 TiDB 会保持正确的二进制类型。

    ```sql
    CREATE TABLE test(a json);
    INSERT INTO test SELECT json_objectagg('a', b'01010101');

    -- 在 TiDB 中，执行以下 SQL 语句返回结果如下所示。在 MySQL 中，执行以下 SQL 语句的结果为 `0, 1`。
    mysql> SELECT JSON_EXTRACT(JSON_OBJECT('a', b'01010101'), '$.a') = "base64:type15:VQ==" AS r1, JSON_EXTRACT(a, '$.a') = "base64:type15:VQ==" AS r2 FROM test;
    +------+------+
    | r1   | r2   |
    +------+------+
    |    0 |    0 |
    +------+------+
    1 row in set (0.01 sec)
    ```

    详情可见此 [issue](https://github.com/pingcap/tidb/issues/37443)。

- 当将 ENUM 或 SET 数据类型转换为 JSON 时，TiDB 会检查其格式正确性。例如，当执行下面的 SQL 语句时，TiDB 中会报错：

    ```sql
    CREATE TABLE t(e ENUM('a'));
    INSERT INTO t VALUES ('a');
    mysql> SELECT CAST(e AS JSON) FROM t;
    ERROR 3140 (22032): Invalid JSON text: The document root must not be followed by other values.
    ```

    详情可见此 [issue](https://github.com/pingcap/tidb/issues/9999)。

- TiDB 支持使用 `ORDER BY` 对 JSON Array 或 JSON Object 进行排序。

    当使用 `ORDER BY` 对 JSON Array 或 JSON Object 进行排序时，MySQL 会返回一个警告，且排序结果与比较运算结果不一致：

    ```sql
    CREATE TABLE t(j JSON);
    INSERT INTO t VALUES ('[1,2,3,4]');
    INSERT INTO t VALUES ('[5]');

    mysql> SELECT j FROM t WHERE j < JSON_ARRAY(5);
    +--------------+
    | j            |
    +--------------+
    | [1, 2, 3, 4] |
    +--------------+
    1 row in set (0.00 sec)

    -- 在 TiDB 中，执行以下 SQL 语句返回结果如下所示。在 MySQL 中，执行以下 SQL 语句会返回警告 “This version of MySQL doesn't yet support 'sorting of non-scalar JSON values'. ”，且排序结果与 `<` 比较结果不一致。
    mysql> SELECT j FROM t ORDER BY j;
    +--------------+
    | j            |
    +--------------+
    | [1, 2, 3, 4] |
    | [5]          |
    +--------------+
    2 rows in set (0.00 sec)
    ```

    详情可见此 [issue](https://github.com/pingcap/tidb/issues/37506)。

- 在 INSERT JSON 列时，TiDB 会将值隐式转换为 JSON：

    ```sql
    CREATE TABLE t(col JSON);

    -- 在 TiDB 中，执行以下 INSERT 语句成功。在 MySQL 中，执行以下 INSERT 语句将返回 Invalid JSON text 错误。
    INSERT INTO t VALUES (3);
    ```

有关 JSON 的更多信息，可以参考 [JSON 函数](/functions-and-operators/json-functions.md)和[生成列](/generated-columns.md)。

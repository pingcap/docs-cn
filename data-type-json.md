---
title: JSON 类型
aliases: ['/docs-cn/dev/data-type-json/','/docs-cn/dev/reference/sql/data-types/json/']
---

# JSON 类型

JSON 类型可以存储 JSON 这种半结构化的数据，相比于直接将 JSON 存储为字符串，它的好处在于：

1. 使用 Binary 格式进行序列化，对 JSON 的内部字段的查询、解析加快；
2. 多了 JSON 合法性验证的步骤，只有合法的 JSON 文档才可以放入这个字段中；

JSON 字段本身上，并不能创建索引，但是可以对 JSON 文档中的某个子字段创建索引。例如：

{{< copyable "sql" >}}

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

# 使用限制

- 暂不支持 JSON PATH 中范围选取的语法，以下 SQL 会在 TiDB 中报错:

    ```sql
    SELECT j->'$[1 to 2]' FROM t;
    SELECT j->'$[last]' FROM t;
    ```

- 请勿使用 BR 工具将备份的 `>=6.3` 版本包含 JSON 列的数据恢复至 `<6.3` 版本的集群中，否则有几率出现无法查询 JSON 的问题。

# MySQL 兼容性

- 当使用二进制类型数据创建 JSON 时，目前 MySQL 会将其误标记为 STRING 类型。

    ```sql
    CREATE TABLE test(a json);
    INSERT INTO test SELECT json_objectagg('a', b'01010101');

    -- TiDB 结果如下所示, 在 MySQL 中下面 SQL 结果为 `0, 1`.
    mysql> SELECT JSON_EXTRACT(JSON_OBJECT('a', b'01010101'), '$.a') = "base64:type15:VQ==" AS r1, JSON_EXTRACT(a, '$.a') = "base64:type15:VQ==" AS r2 FROM test;
    +------+------+
    | r1   | r2   |
    +------+------+
    |    0 |    0 |
    +------+------+
    1 row in set (0.01 sec)
    ```
    详情可见此 [issue](https://github.com/pingcap/tidb/issues/37443)

- 当 `enum/set` 转换为 JSON 时，TiDB 会检查其格式正确性。下面 SQL 在 TiDB 中会报错:

    ```sql
    CREATE TABLE t(e ENUM('a'));
    INSERT INTO t VALUES ('a');
    mysql> SELECT CAST(e AS JSON) FROM t;
    ERROR 3140 (22032): Invalid JSON text: The document root must not be followed by other values.
    ```
    详情可见此 [issue](https://github.com/pingcap/tidb/issues/9999)

- TiDB 支持对 JSON ARRAY/OBJECT 的 `order by`

    当使用 `ORDER BY` 对 JSON Array 或 JSON Object 进行排序时，MySQL 会返回一个警告，且排序结果与比较运算结果不一致:

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

    -- 在 MySQL 中下面 SQL 会抛出 warning: This version of MySQL doesn't yet support 'sorting of non-scalar JSON values'. 且结果与 `<` 比较结果不一致
    mysql> SELECT j FROM t ORDER BY j;
    +--------------+
    | j            |
    +--------------+
    | [1, 2, 3, 4] |
    | [5]          |
    +--------------+
    2 rows in set (0.00 sec)
    ```
    详情可见此 [issue](https://github.com/pingcap/tidb/issues/37506)

- 在 INSERT JSON 列时，TiDB 会将值隐式转换为 JSON

    ```sql
    CREATE TABLE t(col JSON);
    -- TiDB INSERT 成功，MySQL 会报错: Invalid JSON text
    INSERT INTO t VALUES (3);
    ```

有关 JSON 的更多信息，可以参考 [JSON 函数](/functions-and-operators/json-functions.md)和[生成列](/generated-columns.md)。

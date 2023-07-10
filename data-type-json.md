---
title: TiDB Data Type
summary: Learn about the JSON data type in TiDB.
aliases: ['/docs/dev/data-type-json/','/docs/dev/reference/sql/data-types/json/']
---

# JSON Type

TiDB supports the `JSON` (JavaScript Object Notation) data type, which is useful for storing semi-structured data. The `JSON` data type provides the following advantages over storing `JSON`-format strings in a string column:

- Use the Binary format for serialization. The internal format permits quick read access to `JSON` document elements.
- Automatic validation of the JSON documents stored in `JSON` columns. Only valid documents can be stored.

`JSON` columns, like columns of other binary types, are not indexed directly, but you can index the fields in the `JSON` document in the form of generated column:

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

For more information, see [JSON Functions](/functions-and-operators/json-functions.md) and [Generated Columns](/generated-columns.md).

## Restrictions

- Currently, TiDB only supports pushing down limited `JSON` functions to TiFlash. For more information, see [Push-down expressions](/tiflash/tiflash-supported-pushdown-calculations.md#push-down-expressions).
- TiDB Backup & Restore (BR) versions earlier than v6.3.0 do not support recovering data containing JSON columns. No version of BR supports recovering data containing JSON columns to TiDB clusters earlier than v6.3.0.
- Do not use any replication tool to replicate data containing non-standard `JSON` data types, such as `DATE`, `DATETIME`, and `TIME`.

## MySQL compatibility

- When you create JSON columns with data in the `BINARY` type, MySQL mislabels the data as the `STRING` type currently, while TiDB processes it as the `BINARY` type correctly.

    ```sql
    CREATE TABLE test(a json);
    INSERT INTO test SELECT json_objectagg('a', b'01010101');

    -- In TiDB, executing the following SQL statement returns `0, 0`. In MySQL, executing the following SQL statement returns `0, 1`.
    mysql> SELECT JSON_EXTRACT(JSON_OBJECT('a', b'01010101'), '$.a') = "base64:type15:VQ==" AS r1, JSON_EXTRACT(a, '$.a') = "base64:type15:VQ==" AS r2 FROM test;
    +------+------+
    | r1   | r2   |
    +------+------+
    |    0 |    0 |
    +------+------+
    1 row in set (0.01 sec)
    ```

    For more information, see issue [#37443](https://github.com/pingcap/tidb/issues/37443).

- When converting the data type from `ENUM` or `SET` to `JSON`, TiDB checks the correctness of data format. For example, executing the following SQL statements in TiDB will return an error.

    ```sql
    CREATE TABLE t(e ENUM('a'));
    INSERT INTO t VALUES ('a');
    mysql> SELECT CAST(e AS JSON) FROM t;
    ERROR 3140 (22032): Invalid JSON text: The document root must not be followed by other values.
    ```

    For more information, see issue [#9999](https://github.com/pingcap/tidb/issues/9999).

- In TiDB, you can use `ORDER BY` to sort JSON arrays or JSON objects.

    In MySQL, if you use `ORDER BY` to sort JSON arrays or JSON objects, MySQL returns a warning and the sorting result does not match the result of the comparison operation:

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

    -- In TiDB, executing the following SQL statement returns the correct sorting result. In MySQL, executing the following SQL statement returns the "This version of MySQL doesn't yet support 'sorting of non-scalar JSON values'." warning and the sorting result is inconsistent with the comparison result of `<`.
    mysql> SELECT j FROM t ORDER BY j;
    +--------------+
    | j            |
    +--------------+
    | [1, 2, 3, 4] |
    | [5]          |
    +--------------+
    2 rows in set (0.00 sec)
    ```

    For more information, see issue [#37506](https://github.com/pingcap/tidb/issues/37506).

- When you insert data to a JSON column, TiDB implicitly converts the value of the data to the `JSON` type.

    ```sql
    CREATE TABLE t(col JSON);

    -- In TiDB, the following INSERT statement is executed successfully. In MySQL, executing the following INSERT statement returns the "Invalid JSON text" error.
    INSERT INTO t VALUES (3);
    ```

For more information about the `JSON` data type, see [JSON functions](/functions-and-operators/json-functions.md) and [Generated Columns](/generated-columns.md).
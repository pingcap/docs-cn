---
title: 聚合 JSON 值的 JSON 函数
summary: 了解用于聚合 JSON 值的 JSON 函数。
---

# 聚合 JSON 值的 JSON 函数

本页列出的函数是 TiDB 支持的[聚合函数](/functions-and-operators/aggregate-group-by-functions.md)的一部分，专门用于处理 JSON。

## [JSON_ARRAYAGG()](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-arrayagg)

`JSON_ARRAYAGG(key)` 函数根据给定的 `key` 将键的值聚合成一个 JSON 数组。`key` 通常是一个表达式或列名。

示例：

以下示例中，表中一列的两行数据被聚合成一个 JSON 数组。

```sql
SELECT JSON_ARRAYAGG(v) FROM (SELECT 1 'v' UNION SELECT 2);
```

```
+------------------+
| JSON_ARRAYAGG(v) |
+------------------+
| [2, 1]           |
+------------------+
1 row in set (0.00 sec)
```

## [JSON_OBJECTAGG()](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-objectagg)

`JSON_OBJECTAGG(key,value)` 函数根据给定的 `key` 和 `value` 将键和值聚合成一个 JSON 对象。`key` 和 `value` 通常都是表达式或列名。

示例：

首先，创建两个表并添加一些行数据。

```sql
CREATE TABLE plants (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE plant_attributes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plant_id INT, attribute VARCHAR(255),
    value VARCHAR(255),
    FOREIGN KEY (plant_id) REFERENCES plants(id)
);

INSERT INTO plants
VALUES
(1,"rose"),
(2,"tulip"),
(3,"orchid");

INSERT INTO plant_attributes(plant_id,attribute,value)
VALUES
(1,"color","red"),
(1,"thorns","yes"),
(2,"color","orange"),
(2,"thorns","no"),
(2,"grows_from","bulb"),
(3,"color","white"),
(3, "thorns","no");
```

现在可以查看创建的表的内容。

```sql
TABLE plants;
```

```
+----+--------+
| id | name   |
+----+--------+
|  1 | rose   |
|  2 | tulip  |
|  3 | orchid |
+----+--------+
3 rows in set (0.00 sec)
```

```sql
TABLE plant_attributes;
```

```
+----+----------+------------+--------+
| id | plant_id | attribute  | value  |
+----+----------+------------+--------+
|  1 |        1 | color      | red    |
|  2 |        1 | thorns     | yes    |
|  3 |        2 | color      | orange |
|  4 |        2 | thorns     | no     |
|  5 |        2 | grows_from | bulb   |
|  6 |        3 | color      | white  |
|  7 |        3 | thorns     | no     |
+----+----------+------------+--------+
7 rows in set (0.00 sec)
```

你可以使用 `JSON_OBJECTAGG()` 函数处理这些数据。在下面的示例中，你可以看到对于每个分组，多个键值对被聚合成一个 JSON 对象。

```sql
SELECT
    p.name,
    JSON_OBJECTAGG(attribute,value)
FROM
    plant_attributes pa
    LEFT JOIN plants p ON pa.plant_id=p.id
GROUP BY
    plant_id;
```

```
+--------+-----------------------------------------------------------+
| name   | JSON_OBJECTAGG(attribute,value)                           |
+--------+-----------------------------------------------------------+
| rose   | {"color": "red", "thorns": "yes"}                         |
| orchid | {"color": "white", "thorns": "no"}                        |
| tulip  | {"color": "orange", "grows_from": "bulb", "thorns": "no"} |
+--------+-----------------------------------------------------------+
3 rows in set (0.00 sec)
```

## 另请参阅

- [JSON 函数概览](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)

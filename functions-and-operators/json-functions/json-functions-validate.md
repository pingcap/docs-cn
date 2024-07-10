---
title: 验证 JSON 文档的函数
summary: 了解验证 JSON 文档的函数。
---

# 验证 JSON 文档的函数

本文档介绍用于验证 JSON 文档的函数。

## [JSON_SCHEMA_VALID()](https://dev.mysql.com/doc/refman/8.0/en/json-validation-functions.html#function_json-schema-valid)

`JSON_SCHEMA_VALID(schema, json_doc)` 函数根据 schema 验证 JSON 文档，确保数据的完整性和一致性。该函数可以与 [CHECK](/constraints.md#check-约束) 约束一起使用，以便在修改表时自动进行 schema 验证。该函数遵循 [JSON Schema specification](https://json-schema.org/specification)。

验证关键词如下：

| 验证关键词 | 适用于 | 描述 |
|---|---|---|
| `type`                 | Any | 测试类型，如 `array`、`string` |
| `enum`                 | Any | 测试某个值是否在指定的值数组中 |
| `const`                | Any | 与 `enum` 相似，但只适用于单个值 |
| `allOf`                | Any | 匹配所有指定的 schema |
| `anyOf`                | Any | 匹配任意指定的 schema |
| `multipleOf`           | `number`/`integer` | 测试值是否是指定值的倍数 |
| `maximum`              | `number`/`integer` | 测试数值是否小于最大值（包括最大值在内）|
| `exclusiveMaximum`     | `number`/`integer` | 测试数值是否小于最大值（不包括最大值）  |
| `minimum`              | `number`/`integer` | 测试数值是否大于最小值（包括最小值在内）|
| `exclusiveMinimum`     | `number`/`integer` | 测试值是否大于最小值（不包括最小值）    |
| `maxlength`            | `string` | 测试值的长度是否不超过指定值 |
| `minLength`            | `string` | 测试值的长度是否不低于指定值 |
| `format`               | `string` | 测试字符串是否符合指定格式 |
| `pattern`              | `string` | 测试字符串是否与模式匹配  |
| `items`                | `array` | 适用于数组项的 schema |
| `prefixItems`          | `array` | 适用于数组的位置项的 schema |
| `maxItems`             | `array` | 测试数组中的元素数量是否不超过指定值 |
| `minItems`             | `array` | 测试数组中的元素数量是否不低于指定值 |
| `uniqueItems`          | `array` | 测试数组中的元素是否唯一，`true`/`false`|
| `contains`             | `array` | 为数组中的元素设置 schema |
| `maxContains`          | `array` | 与 `contains` 一起使用时，用于测试某些元素出现的最多次数 |
| `minContains`          | `array` | 与 `contains` 一起使用时，用于测试某些元素出现的最少次数 |
| `properties`           | `object` | 适用于对象属性的 schema |
| `patternProperties`    | `object` | 根据属性名称的模式匹配，应用于某些属性的 schema  |
| `additionalProperties` | `object` | 是否允许额外的属性，`true`/`false` |
| `minProperties`        | `object` | 测试对象的最小属性数量 |
| `maxProperties`        | `object` | 测试对象的最大属性数量 |
| `required`             | `object` | 必须填写的属性名称     |

示例：

下面一些示例使用了如下 JSON 文档：

```json
{
    "fruits": [
        "orange",
        "apple",
        "pear"
    ],
    "vegetables": [
        "carrot",
        "pepper",
        "kale"]
}
```

使用[用户自定义的变量](/user-defined-variables.md)存放 JSON 文档。

```sql
SET @j := '{"fruits": ["orange", "apple", "pear"], "vegetables": ["carrot", "pepper", "kale"]}';
```

先测试类型：

```sql
SELECT JSON_SCHEMA_VALID('{"type": "object"}',@j);
```

```
+--------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "object"}',@j) |
+--------------------------------------------+
|                                          1 |
+--------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"type": "array"}',@j);
```

```
+-------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "array"}',@j) |
+-------------------------------------------+
|                                         0 |
+-------------------------------------------+
1 row in set (0.00 sec)
```

```sql
mysql> SELECT JSON_TYPE(@j);
```

```
+---------------+
| JSON_TYPE(@j) |
+---------------+
| OBJECT        |
+---------------+
1 row in set (0.00 sec)
```

从上面的输出中可以看到，`@j` 的类型是 `object`，与 [`JSON_TYPE()`](/functions-and-operators/json-functions/json-functions-return.md#json_type) 的输出结果一致。

现在验证某些属性是否存在。

```sql
SELECT JSON_SCHEMA_VALID('{"required": ["fruits","vegetables"]}',@j);
```

```
+---------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"required": ["fruits","vegetables"]}',@j) |
+---------------------------------------------------------------+
|                                                             1 |
+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

在前面的输出中可以看到，`fruits` 和 `vegetables` 的属性是存在的，验证成功。

```sql
SELECT JSON_SCHEMA_VALID('{"required": ["fruits","vegetables","grains"]}',@j);
```

```
+------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"required": ["fruits","vegetables","grains"]}',@j) |
+------------------------------------------------------------------------+
|                                                                      0 |
+------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

在前面的输出中可以看到，验证 `fruits`、`vegetables` 和 `grains` 属性是否存在失败了，因为 `grains` 不存在。

现在验证 `fruits` 是否为数组。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array"}}}',@j);
```

```
+-----------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array"}}}',@j) |
+-----------------------------------------------------------------------+
|                                                                     1 |
+-----------------------------------------------------------------------+
1 row in set (0.01 sec)
```

从上面的输出结果，可以确认 `fruits` 是数组。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "string"}}}',@j);
```

```
+------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "string"}}}',@j) |
+------------------------------------------------------------------------+
|                                                                      0 |
+------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

上面的输出结果显示 `fruits` **不是**字符串。

现在验证数组中的元素数量。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 3}}}',@j);
```

```
+--------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 3}}}',@j) |
+--------------------------------------------------------------------------------------+
|                                                                                    1 |
+--------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

前面的输出结果显示，`fruits` 是一个至少包含 3 个元素的数组。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 4}}}',@j);
```

```
+--------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 4}}}',@j) |
+--------------------------------------------------------------------------------------+
|                                                                                    0 |
+--------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

前面的输出结果显示，`fruits` **不是**一个至少包含 4 个元素的数组，它没有达到元素数量的最低要求。

对于整数值，可以检查它们是否在某个范围内。

```sql
SELECT JSON_SCHEMA_VALID('{"type": "integer", "minimum": 40, "maximum": 45}', '42');
+------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "integer", "minimum": 40, "maximum": 45}', '42') |
+------------------------------------------------------------------------------+
|                                                                            1 |
+------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"type": "integer", "minimum": 40, "maximum": 45}', '123');
```

```
+-------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "integer", "minimum": 40, "maximum": 45}', '123') |
+-------------------------------------------------------------------------------+
|                                                                             0 |
+-------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

对于字符串，可以验证是否匹配指定的模式。

```sql
SELECT JSON_SCHEMA_VALID('{"type": "string", "pattern": "^Ti"}', '"TiDB"');
```

```
+---------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "string", "pattern": "^Ti"}', '"TiDB"') |
+---------------------------------------------------------------------+
|                                                                   1 |
+---------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"type": "string", "pattern": "^Ti"}', '"PingCAP"');
```

```
+------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "string", "pattern": "^Ti"}', '"PingCAP"') |
+------------------------------------------------------------------------+
|                                                                      0 |
+------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

你可以检查一个值是否符合指定的命名格式。可验证的格式包括：`ipv4`、`ipv6`、`time`、`date`、`duration`、`email`、`hostname`、`uuid` 和 `uri`。

```sql
SELECT JSON_SCHEMA_VALID('{"format": "ipv4"}', '"127.0.0.1"');
```

```
+--------------------------------------------------------+
| JSON_SCHEMA_VALID('{"format": "ipv4"}', '"127.0.0.1"') |
+--------------------------------------------------------+
|                                                      1 |
+--------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"format": "ipv4"}', '"327.0.0.1"');
```

```
+--------------------------------------------------------+
| JSON_SCHEMA_VALID('{"format": "ipv4"}', '"327.0.0.1"') |
+--------------------------------------------------------+
|                                                      0 |
+--------------------------------------------------------+
1 row in set (0.00 sec)
```

你还可以使用 `enum` 来检查一个字符串是否在一个数组中。

```sql
SELECT JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"TiDB"');
```

```
+------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"TiDB"') |
+------------------------------------------------------------+
|                                                          1 |
+------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"MySQL"');
```

```
+-------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"MySQL"') |
+-------------------------------------------------------------+
|                                                           1 |
+-------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"SQLite"');
```

```
+--------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"SQLite"') |
+--------------------------------------------------------------+
|                                                            0 |
+--------------------------------------------------------------+
1 row in set (0.00 sec)
```

你可以使用 `anyOf` 将某些要求组合起来，验证是否满足其中任意一个要求。

```sql
SELECT JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '"TiDB"');
```

```
+------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '"TiDB"') |
+------------------------------------------------------------------------------------+
|                                                                                  1 |
+------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '["TiDB", "MySQL"]');
```

```
+-----------------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '["TiDB", "MySQL"]') |
+-----------------------------------------------------------------------------------------------+
|                                                                                             0 |
+-----------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '5');
```

```
+-------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '5') |
+-------------------------------------------------------------------------------+
|                                                                             1 |
+-------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

- 如果 `JSON_SCHEMA_VALID()` 中待验证的 schema 无效（如 `{"type"： "sting"}`），MySQL 可能会接受该 schema ，但 TiDB 会返回错误。注意这里的 `"sting"` 存在拼写错误，应为 `"string"`。
- MySQL 使用的是较早 draft 版本的 JSON Schema standard。

## 另请参阅

- [JSON Schema Reference](https://json-schema.org/understanding-json-schema/reference)
- [JSON 函数](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)
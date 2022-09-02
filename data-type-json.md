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

# MySQL 兼容性

- 修复了 MySQL 使用二进制类型数据创建 JSON 时错误的将其标记为 STRING TYPE 的 bug：

{{< copyable "sql" >}}

```sql
create table test (a json);
insert into test select json_objectagg('a', b'01010101');

mysql> select json_extract(json_object('a', b'01010101'), '$.a') = "base64:type15:VQ==" as result;
+--------+
| result |
+--------+
|      0 |
+--------+
1 row in set (0.02 sec)

-- 在 MySQL 中下面 SQL 结果为 1.
mysql> select json_extract(a, '$.a') = "base64:type15:VQ==" as result from test;
+--------+
| result |
+--------+
|      0 |
+--------+
1 row in set (0.02 sec)
```
详情可见此 [issue](https://github.com/pingcap/tidb/issues/37443)

- 修复了 MySQL 错误的将 `enum/set` 转换为 `json` 的 bug:

{{< copyable "sql" >}}

```sql
create table t(e enum('a'));
insert into t values ('a');
mysql> select cast(e as json) from t;
ERROR 3140 (22032): Invalid JSON text: The document root must not be followed by other values.
```
详情可见此 [issue](https://github.com/pingcap/tidb/issues/9999)

- 支持对 JSON ARRAY/OBJECT 的 `order by`

如果在 MySQL 中对 JSON ARRAY/OBJECT 使用 order by 会得到一个 warning，且结果与比较运算不一致:

{{< copyable "sql" >}}

```sql
create table t(j JSON);
insert into t values ('[1,2,3,4]');
insert into t values ('[5]');

mysql> select j from t where j < json_array(5);
+--------------+
| j            |
+--------------+
| [1, 2, 3, 4] |
+--------------+
1 row in set (0.00 sec)

-- 在 MySQL 中下面 SQL 会抛出 warning: This version of MySQL doesn't yet support 'sorting of non-scalar JSON values'. 且结果与 `<` 比较结果不一致
mysql> select j from t order by j;
+--------------+
| j            |
+--------------+
| [1, 2, 3, 4] |
| [5]          |
+--------------+
2 rows in set (0.00 sec)
```
详情可见此 [issue](https://github.com/pingcap/tidb/issues/37506)

- 暂不支持 JSON PATH 中范围选取的语法，以下 SQL 会在 TiDB 中报错:

{{< copyable "sql" >}}

```sql
select j->'$[1 to 2]' from t;
select j->'$[last]' from t;
```

有关 JSON 的更多信息，可以参考 [JSON 函数](/functions-and-operators/json-functions.md)和[生成列](/generated-columns.md)。

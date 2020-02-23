---
title: JSON 函数及 Generated Column
category: compatibility
---

# JSON 函数及 Generated Column

## 概述

为了在功能上兼容 MySQL 5.7 及以上，同时更好地支持文档类型存储，我们在最新版本的 TiDB 中加入了 JSON 的支持。TiDB 所支持的文档是指以 JSON 为编码类型的键值对的组合。用户可以在 TiDB 的表中使用 JSON 类型的字段，同时以生成列（generated column）的方式为 JSON 文档内部的字段建立索引。基于此，用户可以很灵活地处理那些 schema 不确定的业务，同时不必受限于传统文档数据库糟糕的读性能及匮乏的事务支持。

## JSON功能介绍

TiDB 的 JSON 主要参考了 MySQL 5.7 的用户接口。例如，可以创建一个表，包含一个 JSON 字段来存储那些复杂的信息：

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON
);
```

当我们向表中插入数据时，便可以这样处理那些模式不确定的数据了：

```sql
INSERT INTO person (name, address_info) VALUES ("John", '{"city": "Beijing"}');
```

就这么简单！直接在 JSON 字段对应的位置上，放一个合法的 JSON 字符串，就可以向表中插入 JSON 了。TiDB 会解析这个文本，然后以一种更加紧凑、易于访问的二进制形式来保存。

当然，你也可以将其他类型的数据用 CAST 转换为 JSON：

```sql
INSERT INTO person (name, address_info) VALUES ("John", CAST('{"city": "Beijing"}' AS JSON));
INSERT INTO person (name, address_info) VALUES ("John", CAST('123' AS JSON));
INSERT INTO person (name, address_info) VALUES ("John", CAST(123 AS JSON));
```

现在，如果我们想查询表中所有居住在北京的用户，该怎么做呢？需要把数据全拉回来，然后在业务层进行过滤吗？不需要，和 MongoDB 等文档数据库相同，我们有在服务端支持用户各种复杂组合查询条件的能力。你可以这样写 SQL：

```sql
SELECT id, name FROM person WHERE JSON_EXTRACT(address_info, '$.city') = 'Beijing';
```

TiDB 支持 `JSON_EXTRACT` 函数，该函数与 MySQL 5.7 中 `JSON_EXTRACT` 的用法完全相同。这个函数的意思就是，从 `address_info` 这个文档中取出名为 `city` 这个字段。它的第二个参数是一个“路径表达式”，我们由此可以指定到底要取出哪个字段。关于路径表达式的完整语法描述比较复杂，我们还是通过几个简单的例子来了解其用法：

```sql
SET @person = '{"name":"John","friends":[{"name":"Forest","age":16},{"name":"Zhang San","gender":"male"}]}';

SELECT JSON_EXTRACT(@person,  '$.name'); -- gets "John"
SELECT JSON_EXTRACT(@person,  '$.friends[0].age'); -- gets 16
SELECT JSON_EXTRACT(@person,  '$.friends[1].gender'); -- gets "male"
SELECT JSON_EXTRACT(@person,  '$.friends[2].name'); -- gets NULL
```

除了插入、查询外，对 JSON 的修改也是支持的。总的来说，目前我们支持的 MySQL 5.7 的 JSON 函数如下表所示：

* [JSON_EXTRACT](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract)
* [JSON_ARRAY](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array)
* [JSON_OBJECT](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object)
* [JSON_SET](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set)
* [JSON_REPLACE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace)
* [JSON_INSERT](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert)
* [JSON_REMOVE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove)
* [JSON_TYPE](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type)
* [JSON_UNQUOTE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote)

直接从名字上，我们便能得出这些函数的大致用途，而且它们的语义也与 MySQL 5.7 完全一致，因此，想要查询它们具体的用法，我们可以直接查阅 MySQL 5.7 的[相关文档](https://dev.mysql.com/doc/refman/5.7/en/json-functions.html)。MySQL 5.7 的用户可以无缝迁移至 TiDB。

熟悉 MySQL 5.7 的用户会发现，TiDB 尚未完全支持所有 MySQL 5.7 中的 JSON 函数。这是因为我们的一期目标是能够提供完备的 **MySQL X Plugin** 支持即可，而这已经涵盖大部分常用的 JSON 增删改查的功能了。如有需要，我们会继续完善对其他函数的支持。

## 使用生成列对 JSON 建索引

在有了上述的知识铺垫后，您可能会发现我们在查询 JSON 中的一个字段时，走的是全表扫描。使用 TiDB 的 `EXPLAIN` 语句时，一个比 MySQL 完备得多的结果会告诉我们，的确是全表扫描。那么，我们能否对 JSON 字段进行索引呢？

首先，这种索引是错误的：

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

这并非是因为技术上无法支持，而是因为对 JSON 的直接比较，本身就是没有意义的 —— 尽管我们可以人为地约定一些比较规则，比如 ARRAY 比所有的 OBJECT 都大 —— 但是这并没有什么用处。因此，正如 MySQL 5.7 所做的那样，我们禁止了直接在 JSON 字段上创建索引，而是通过生成列的方式，支持了对 JSON 文档内的某一字段建立索引：

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64)  AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) VIRTUAL,
    KEY (city)
);
```

这个表中，`city` 列就是一个 **生成列**。顾名思义，该列由表中其他的列生成，而不能显式地在插入或更新时为它赋一个值。对于生成列，用户还可以指定其为 ``VIRTUAL`` 来避免它被显式地保存在记录中，而是在需要地时候再由其他列来生成，这对于列比较宽且需要节约存储空间地情况尤为有用。有了这个生成列，我们就可以在它上面建立索引了，在用户看来与常规的列便没什么两样，是不是很简单呢？而查询的时候，我们可以：

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

这样，便可以走索引了！

另外，需要注意的是，如果 JSON 文档中指定路径下的字段不存在，那么 JSON_EXTRACT 的结果会是 NULL ，这时，带有索引的生成列的值也就为 NULL 了。因此，如果这是用户不希望看到的，那也可以在生成列上增加 NOT NULL 约束，这样，当插入新的纪录算出来的 city 字段为 NULL 时，便可以检查出来了。

## 目前的一些限制

目前 JSON 及生成列仍然有一些限制：

* 不能 ALTER TABLE 增加 STORED 存储方式的生成列；
* 不能 ALTER TABLE 在生成列上增加索引；

这些功能，包括其他一些 JSON 函数的实现尚在开发过程中。

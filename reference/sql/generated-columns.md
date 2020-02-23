---
title: 生成列
category: reference
---

# 生成列

为了在功能上兼容 MySQL 5.7，TiDB 支持生成列 (generated column)。生成列的主要的作用之一：从 JSON 数据类型中解出数据，并为该数据建立索引。

## 使用 generated column 对 JSON 建索引

MySQL 5.7 及 TiDB 都不能直接为 JSON 类型的列添加索引，即**不支持**如下表结构：

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

为 JSON 列添加索引之前，首先必须抽取该列为 generated column。

以 `city` generated stored column 为例，你可以添加索引：

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) STORED,
    KEY (city)
);
```

该表中，`city` 列是一个 **generated stored column**。顾名思义，此列由该表的其他列生成，对此列进行插入或更新操作时，并不能对之赋值。此列按其定义的表达式生成，并存储在数据库中，这样在读取此列时，就可以直接读取，不用再读取其依赖的 `address_info` 列后再计算得到。`city` 列的索引**存储在数据库中**，并使用和 `varchar(64)` 类的其他索引相同的结构。

可使用 generated stored column 的索引，以提高如下语句的执行速度：

{{< copyable "sql" >}}

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

如果 `$.city` 路径中无数据，则 `JSON_EXTRACT` 返回 `NULL`。如果想增加约束，`city` 列必须是 `NOT NULL`，则可按照以下方式定义 virtual column：

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) STORED NOT NULL,
    KEY (city)
);
```

`INSERT` 和 `UPDATE` 语句都会检查 virtual column 的定义。未通过有效性检测的行会返回错误：

{{< copyable "sql" >}}

```sql
INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
```

```
ERROR 1048 (23000): Column 'city' cannot be null
```

## 使用 generated virtual column

TiDB 也支持 generated virtual column，和 generated store column 不同的是，此列按需生成，并不存储在数据库中，也不占用内存空间，因而是**虚拟的**。

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) VIRTUAL
);
```

## 局限性

目前 JSON and generated column 有以下局限性：

- 不能通过 `ALTER TABLE` 增加 `STORED` 存储方式的 generated column；
- 不能通过 `ALTER TABLE` 将 generated stored column 转换为普通列，也不能将普通列转换成 generated stored column；
- 不能通过 `ALTER TABLE` 修改 generated stored column 的**生成列表达式**；
- 并未支持所有的 [JSON 函数](/reference/sql/functions-and-operators/json-functions.md)。
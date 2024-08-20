---
title: 使用 TiDB 的增删改查 SQL
summary: 简单介绍 TiDB 的增删改查 SQL。
---

# 使用 TiDB 的增删改查 SQL

本章将简单介绍 TiDB 的增删改查 SQL 的使用方法。

## 在开始之前

请确保你已经连接到 TiDB 集群，若未连接，请参考[使用 TiDB Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)来创建一个 TiDB Serverless 集群。

## 基本 SQL 操作

> **注意：**
>
> 此处文档引用并简化自 TiDB 文档中的 [SQL 基本操作](/basic-sql-operations.md)，你可直接前往此文档获取更全面、深入的 SQL 基本操作信息。

成功部署 TiDB 集群之后，便可以在 TiDB 中执行 SQL 语句了。因为 TiDB 兼容 MySQL，你可以使用 MySQL 客户端连接 TiDB，并且[大多数情况下](/mysql-compatibility.md)可以直接执行 MySQL 语句。

SQL 是一门声明性语言，它是数据库用户与数据库交互的方式。它更像是一种自然语言，好像在用英语与数据库进行对话。本文档介绍基本的 SQL 操作。完整的 SQL 语句列表，参见 [SQL 语句概览](/sql-statements/sql-statement-overview.md)。

## 分类

SQL 语言通常按照功能划分成以下的 4 个部分：

- **DDL (Data Definition Language)**：数据定义语言，用来定义数据库对象，包括库、表、视图和索引等。
- **DML (Data Manipulation Language)**：数据操作语言，用来操作和业务相关的记录。
- **DQL (Data Query Language)**：数据查询语言，用来查询经过条件筛选的记录。
- **DCL (Data Control Language)**：数据控制语言，用来定义访问权限和安全级别。

此文档中，主要介绍 DML 和 DQL，即数据操作语言和数据查询语言。其余部分可查看 [SQL 基本操作](/basic-sql-operations.md)或 [SQL 语句概览](/sql-statements/sql-statement-overview.md)获得更多信息。

## DML 数据操作语言

数据操作语言可完成数据的增删改。

使用 `INSERT` 语句向表内插入表记录。例如：

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

使用 `INSERT` 语句向表内插入包含部分字段数据的表记录。例如：

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

使用 `UPDATE` 语句向表内修改表记录的部分字段数据。例如：

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

使用 `DELETE` 语句向表内删除部分表记录。例如：

```sql
DELETE FROM person WHERE id=2;
```

> **注意：**
>
> `UPDATE` 和 `DELETE` 操作如果不带 `WHERE` 过滤条件是对全表进行操作。

## DQL 数据查询语言

数据查询语言是从一个表或多个表中检索出想要的数据行，通常是业务开发的核心内容。

使用 `SELECT` 语句检索单表内数据。例如：

```sql
SELECT * FROM person;
```

在 `SELECT` 后面加上要查询的列名。例如：

```sql
SELECT name FROM person;
```

运行结果为：

```
+------+
| name |
+------+
| tom  |
+------+
1 rows in set (0.00 sec)
```

使用 `WHERE` 子句，对所有记录进行是否符合条件的筛选后再返回。例如：

```sql
SELECT * FROM person WHERE id < 5;
```

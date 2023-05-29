---
title: 概述
summary: TiDB 数据库模式设计的概述。
---

# 概述

本页概述了 TiDB 中的数据库模式。将从本页开始围绕 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 这个应用程序来对 TiDB 的设计数据库部分展开介绍。并使用此数据库做后续数据的写入、读取示例。

## 术语歧义

此处术语会有歧义，为消除歧义，在此作出数据库模式设计文档部分中的术语简要约定：

为避免和通用术语[数据库 (Database)](https://en.wikipedia.org/wiki/Database) 混淆，因此将逻辑对象称为**数据库 (Database)**，TiDB 仍使用原名称，并将 TiDB 的部署实例称为**集群 (Cluster)**。

因为 TiDB 使用与 MySQL 兼容的语法，在此语法下，**模式 (Schema)** 仅代表[通用术语定义](https://en.wiktionary.org/wiki/schema)，并无逻辑对象定义，可参考此[官方文档](https://dev.mysql.com/doc/refman/8.0/en/create-database.html)。若你从其他拥有 **Schema** 逻辑对象的数据库（如：[PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html)、[Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html)、[Microsoft SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15) 等）迁移而来，请注意此区别。

## 数据库 Database

TiDB 语境中的 Database 或者说数据库，可以认为是表和索引等对象的集合。

TiDB 集群包含一个名为 `test` 的数据库。但建议你自行创建数据库，而不是使用 `test` 数据库。

## 表 Table

TiDB 语境中的 Table 或者说表，从属于某个[数据库](#数据库-database)。

表包含数据**行**。每行数据中的每个值都属于一个特定的**列**。每列都只允许单一数据类型的数据值。列可添加[约束](/constraints.md)来进一步限定。你还可以添加[生成列](/generated-columns.md)用于计算。

## 索引 Index

索引是单个表中行的副本，按列或列集排序。TiDB 查询使用索引来更有效的查找表内的数据，同时可以给出特定列的值。每个索引都是从属于某个[表](#表-table)的。

索引有两种常见的类型，分别为：

- **Primary Key**: 即主键索引，即标识在主键列上的索引。
- **Secondary Index**: 即二级索引，即在非主键上标识的索引。

> **注意：**
>
> TiDB 中，关于 **Primary Key** 的默认定义与 MySQL 常用存储引擎 [InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html) 不一致。**InnoDB** 中，**Primary Key** 的语义为：唯一，不为空，**且为聚簇索引**。
>
> 而在 TiDB 中，**Primary Key** 的定义为：唯一，不为空。但主键不保证为**聚簇索引**。而是由另一组关键字 `CLUSTERED`、`NONCLUSTERED` 额外控制 **Primary Key** 是否为聚簇索引，若不指定，则由系统变量 `@@global.tidb_enable_clustered_index` 影响，具体说明请看[聚簇索引](/clustered-indexes.md)。

### 专用索引

TiDB 支持一些特殊场景专用的索引，用以提高特定用例中的查询性能。具体请参考[索引和约束](/basic-features.md#索引和约束)。

## 其他对象

TiDB 支持一些和**表**同级的对象：

- [视图](/views.md): 视图是一张虚拟表，该虚拟表的结构由创建视图时的 `SELECT` 语句定义，TiDB 目前不支持物化视图。
- [序列](/sql-statements/sql-statement-create-sequence.md): 创建和存储顺序数据。
- [临时表](/temporary-tables.md): 临时表是数据不持久化的表。

## 访问控制

TiDB 支持基于用户或角色的访问控制。你可以通过[角色](/role-based-access-control.md)或直接指向[用户](/user-account-management.md)，从而授予**用户**查看、修改或删除数据对象和数据模式的[权限](/privilege-management.md)。

## 执行数据库模式更改

不推荐使用客户端的 Driver 或 ORM 来执行数据库模式的更改。以经验来看，作为最佳实践，建议使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)或使用任意你喜欢的 GUI 客户端来进行数据库模式的更改。本文档中，将在大多数场景下，使用 **MySQL 客户端** 传入 SQL 文件来执行数据库模式的更改。

## 对象大小限制

具体限制请参考 [TiDB 使用限制](/tidb-limitations.md)。

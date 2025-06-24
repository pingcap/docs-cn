---
title: TiDB 数据库架构设计概述
summary: 了解 TiDB 数据库架构设计的基础知识。
---

# TiDB 数据库架构设计概述

本文档提供了 TiDB 数据库架构设计的基础知识，包括 TiDB 中的对象、访问控制、数据库架构变更和对象限制。

在后续文档中，将以[书店](/develop/dev-guide-bookshop-schema-design.md)为例，向你展示如何设计数据库并在数据库中执行数据读写操作。

## TiDB 中的对象

为了区分一些通用术语，以下是 TiDB 中使用的术语约定：

- 为避免与通用术语[数据库](https://en.wikipedia.org/wiki/Database)混淆，本文档中的**数据库**指的是一个逻辑对象，**TiDB** 指的是 TiDB 本身，而**集群**指的是已部署的 TiDB 实例。

- TiDB 使用与 MySQL 兼容的语法，其中 **schema** 表示通用术语 [schema](https://en.wiktionary.org/wiki/schema)，而不是数据库中的逻辑对象。更多信息，请参见 [MySQL 文档](https://dev.mysql.com/doc/refman/8.0/en/create-database.html)。如果你要从将 schema 作为逻辑对象的数据库（例如 [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html)、[Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html) 和 [Microsoft SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15)）迁移，请注意这一区别。

### 数据库

TiDB 中的数据库是表和索引等对象的集合。

TiDB 自带一个名为 `test` 的默认数据库。但是，建议你创建自己的数据库，而不是使用 `test` 数据库。

### 表

表是[数据库](#数据库)中相关数据的集合。

每个表由**行**和**列**组成。行中的每个值都属于特定的**列**。每列只允许单一数据类型。为了进一步限定列，你可以添加一些[约束](/constraints.md)。为了加速计算，你可以添加[生成列](/generated-columns.md)。

### 索引

索引是表中选定列的副本。你可以使用[表](#表)的一列或多列创建索引。通过索引，TiDB 可以快速定位数据，而无需每次都搜索表中的每一行，这大大提高了查询性能。

有两种常见的索引类型：

- **主键**：主键列上的索引。
- **二级索引**：非主键列上的索引。

> **注意：**
>
> 在 TiDB 中，**主键**的默认定义与 [InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html)（MySQL 的常用存储引擎）中的定义不同。
>
> - 在 InnoDB 中，**主键**的定义是唯一的、非空的，并且是**聚簇索引**。
> - 在 TiDB 中，**主键**的定义是唯一的和非空的。但主键不一定是**聚簇索引**。要指定主键是否为聚簇索引，你可以在 `CREATE TABLE` 语句中的 `PRIMARY KEY` 后添加非保留关键字 `CLUSTERED` 或 `NONCLUSTERED`。如果语句没有明确指定这些关键字，默认行为由系统变量 `@@global.tidb_enable_clustered_index` 控制。更多信息，请参见[聚簇索引](/clustered-indexes.md)。

#### 专用索引

<CustomContent platform="tidb">

为了提高各种用户场景的查询性能，TiDB 为你提供了一些专用类型的索引。有关每种类型的详细信息，请参见[索引和约束](/basic-features.md#索引和约束)。

</CustomContent>

<CustomContent platform="tidb-cloud">

为了提高各种用户场景的查询性能，TiDB 为你提供了一些专用类型的索引。有关每种类型的详细信息，请参见[索引和约束](https://docs.pingcap.com/tidb/stable/basic-features#indexing-and-constraints)。

</CustomContent>

### 其他支持的逻辑对象

TiDB 支持以下与**表**处于同一级别的逻辑对象：

- [视图](/views.md)：视图充当虚拟表，其架构由创建视图的 `SELECT` 语句定义。
- [序列](/sql-statements/sql-statement-create-sequence.md)：序列用于生成和存储顺序数据。
- [临时表](/temporary-tables.md)：数据不持久的表。

## 访问控制

<CustomContent platform="tidb">

TiDB 支持基于用户和基于角色的访问控制。要允许用户查看、修改或删除数据对象和数据架构，你可以直接向[用户](/user-account-management.md)授予[权限](/privilege-management.md)，或通过[角色](/role-based-access-control.md)向用户授予[权限](/privilege-management.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB 支持基于用户和基于角色的访问控制。要允许用户查看、修改或删除数据对象和数据架构，你可以直接向[用户](https://docs.pingcap.com/tidb/stable/user-account-management)授予[权限](https://docs.pingcap.com/tidb/stable/privilege-management)，或通过[角色](https://docs.pingcap.com/tidb/stable/role-based-access-control)向用户授予[权限](https://docs.pingcap.com/tidb/stable/privilege-management)。

</CustomContent>

## 数据库架构变更

作为最佳实践，建议你使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)或 GUI 客户端而不是驱动程序或 ORM 来执行数据库架构变更。

## 对象限制

更多信息，请参见 [TiDB 限制](/tidb-limitations.md)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>

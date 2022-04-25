---
title: 概述
---

# 概述

本页概述了 TiDB 中的数据库模式，我们将从本页开始，设计一个数据库，并使用此数据库做后续数据的写入、读取示例。

> Note:
>
> 此处将术语会有歧义，为消除歧义，在此作出数据库模式设计文档部分中的术语简要约定：
>
> 1. 为避免和通用术语[数据库 (Database)](https://en.wikipedia.org/wiki/Database)混淆，我们将逻辑对象称为`数据库 (Database)`，TiDB 仍使用原名称，并将 TiDB 的部署实例称为`集群 (Cluster)`。
> 2. 因为 TiDB 使用与 MySQL 兼容的语法，在此语法下，`模式 (Schema)` 仅代表[通用术语定义](https://en.wiktionary.org/wiki/schema)，并无逻辑对象定义，可参考此[官方文档](https://dev.mysql.com/doc/refman/8.0/en/create-database.html)。若您从其他拥有 `Schema` 逻辑对象的数据库（如：[PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html)、[Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html)、[Microsoft SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15) 等）迁移而来，请注意此区别。

## 数据库 Database

TiDB 语境中的 Database 或者说数据库，可以认为是表和索引等对象的集合。

TiDB 集群包含一个名为 `test` 的数据库。但我们建议您自行创建数据库，而不是使用 `test` 数据库。

## 表 Table

TiDB 语境中的 Table 或者说表，从属于某个[数据库](#数据库-database)。

表包含数据`行`。每行数据中的每个值都属于一个特定的`列`。每列都只允许单一数据类型的数据值。列可添加[约束](https://docs.pingcap.com/zh/tidb/stable/constraints)来进一步限定。你还可以添加[生成列（实验特性）](https://docs.pingcap.com/zh/tidb/stable/generated-columns)用于计算。

## 索引 Index

索引是单个表中行的副本，按列或列集排序。TiDB 查询使用索引来更有效的查找表内的数据，同时可以给出特定列的值。每个索引都是从属于某个[表](#表-table)的。

索引有两种常见的类型，分别为：

1. `Primary Key`: 即主键索引，即标识在主键列上的索引
2. `Secondary Index`: 即二级索引，即在非主键上标识的索引

> Note:
>
> TiDB 中，关于 `Primary Key` 的默认定义与 MySQL 常用存储引擎 [InnoDB](https://mariadb.com/kb/en/innodb/) 不一致。`InnoDB` 中，`Primary Key` 的语义为：唯一，不为空，**且为聚簇索引**。
>
> 而在 TiDB 中，`Primary Key` 的定义为：唯一，不为空。但主键不保证为**聚簇索引**。而是由另一组关键字 `CLUSTERED` / `NONCLUSTERED` 额外控制 `Primary Key` 是否为聚簇索引，若不指定，则由系统变量 `@@global.tidb_enable_clustered_index` 影响，具体说明请看[此文档](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes)。

### 专用索引

TiDB 支持一些特殊场景专用的索引，用以提高特定用例中的查询性能。有关这些专用索引的指导，请参阅以下页面：

|                                                           索引和约束                                                           |   5.4    |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| :----------------------------------------------------------------------------------------------------------------------------: | :------: | :------: | :------: | :------: | :------: | :------: |
| [表达式索引](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-index#%E8%A1%A8%E8%BE%BE%E5%BC%8F%E7%B4%A2%E5%BC%95) | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
|                         [列式存储 (TiFlash)](https://docs.pingcap.com/zh/tidb/stable/tiflash-overview)                         |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|                            [RocksDB 引擎](https://docs.pingcap.com/zh/tidb/stable/rocksdb-overview)                            |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|                              [Titan 插件](https://docs.pingcap.com/zh/tidb/stable/titan-overview)                              |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|                         [不可见索引](https://docs.pingcap.com/zh/tidb/stable/sql-statement-add-index)                          |    Y     |    Y     |    Y     |    Y     |    Y     |    N     |
|              [复合主键](https://docs.pingcap.com/zh/tidb/stable/constraints#%E4%B8%BB%E9%94%AE%E7%BA%A6%E6%9D%9F)              |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|              [唯一约束](https://docs.pingcap.com/zh/tidb/stable/constraints#%E5%94%AF%E4%B8%80%E7%BA%A6%E6%9D%9F)              |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|                          [整型主键上的聚簇索引](https://docs.pingcap.com/zh/tidb/stable/constraints)                           |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|                      [复合或非整型主键上的聚簇索引](https://docs.pingcap.com/zh/tidb/stable/constraints)                       |    Y     |    Y     |    Y     |    Y     |    Y     |    N     |

## 其他对象

TiDB 支持一些和`表`同级的对象：

1. [视图](https://docs.pingcap.com/zh/tidb/stable/views): 视图是一张虚拟表，该虚拟表的结构由创建视图时的 `SELECT` 语句定义，TiDB 目前不支持物化视图。
2. [序列](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-sequence): 创建和存储顺序数据。
3. [临时表](https://docs.pingcap.com/zh/tidb/stable/temporary-tables): 临时表是数据不持久化的表。

## 访问控制

TiDB 支持基于用户或角色的访问控制。你可以通过[角色](https://docs.pingcap.com/zh/tidb/stable/role-based-access-control)或直接指向[用户](https://docs.pingcap.com/zh/tidb/stable/user-account-management)，从而授予`用户`查看、修改或删除 数据对象和数据模式的[权限](https://docs.pingcap.com/zh/tidb/stable/privilege-management)。

## 执行数据库模式更改

我们不推荐使用客户端的 Driver 或 ORM 来执行数据库模式的更改。以经验来看，作为最佳实践，我们建议使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)或使用任意你喜欢的 GUI 客户端来进行数据库模式的更改。本文档中，我们将在大多数场景下，使用 `MySQL 客户端` 传入 SQL 文件来执行数据库模式的更改。

## 对象大小限制

此处摘录一些常见的对象大小限制，详细使用限制请查阅[此文档](https://docs.pingcap.com/zh/tidb/stable/tidb-limitations)。

### 标识符长度限制

|    对象    |  限制   |
| :--------: | :-----: |
| 数据库名称 | 64 字符 |
|   表名称   | 64 字符 |
|   列名称   | 64 字符 |
|  索引名称  | 64 字符 |
|  视图名称  | 64 字符 |
|  序列名称  | 64 字符 |

### 单个表内限制

|      对象      |                                                                                                                   限制                                                                                                                    |
| :------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|      列数      |                                                                                                       默认为 1017，最大可调至 4096                                                                                                        |
|     索引数     |                                                                                                         默认为 64，最大可调至 512                                                                                                         |
|     分区数     |                                                                                                                   8192                                                                                                                    |
|    单行大小    | 默认为 6MB，可通过 [txn-entry-size-limit](https://docs.pingcap.com/zh/tidb/stable/tidb-configuration-file#txn-entry-size-limit-span-classversion-mark%E4%BB%8E-v50-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5span) 配置项调整 |
| 单行内单列大小 |                                                                                                                    6MB                                                                                                                    |

### 字符串类型限制

|   对象    |    限制    |
| :-------: | :--------: |
|   CHAR    |  256 字符  |
|  BINARY   |  256 字节  |
| VARBINARY | 65535 字节 |
|  VARCHAR  | 16383 字符 |
|   TEXT    |    6MB     |
|   BLOB    |    6MB     |

### 行数

TiDB 可通过增加集群的节点数来支持任意数量的行，原理可阅读[此文档](https://docs.pingcap.com/zh/tidb/stable/tidb-best-practices)

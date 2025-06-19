---
title: 数据库模式
summary: 了解 TiDB Cloud 的数据库模式概念。
---

# 数据库模式

数据库模式定义了数据库、表、列、索引和其他对象中数据的结构和组织方式。

本文档介绍了数据库模式的关键概念，如数据库、表、列、数据类型、约束和索引。同时还介绍了高级功能，如用于无缝管理中间数据的临时表、用于高效近似最近邻（ANN）搜索的向量索引，以及用于提高读取性能的缓存表。

## 数据库

TiDB 中的数据库是表和索引等对象的集合。

### 系统数据库

系统数据库是 TiDB 创建的用于存储系统表的默认数据库。TiDB 提供以下系统数据库：

- [`INFORMATION_SCHEMA`](/information-schema/information-schema.md)

- [`mysql`](/mysql-schema/mysql-schema.md)

- [`performance_schema`](/performance-schema/performance-schema.md)

- [`sys`](/sys-schema/sys-schema.md)

### `test` 数据库

TiDB 自带一个名为 `test` 的默认数据库。但是，建议您创建自己的数据库，而不是使用 `test` 数据库。

## 表

表是[数据库](/develop/dev-guide-schema-design-overview.md#database)中相关数据的集合。

每个表由行和列组成。行中的每个值都属于特定的列。每列只允许单一数据类型。为了进一步限定列，您可以添加一些[约束](/constraints.md)。为了加速计算，您可以添加[生成列](/generated-columns.md)。

### 系统表

- `mysql` 模式包含 TiDB 系统表。其设计类似于 MySQL 中的 `mysql` 模式，其中像 `mysql.user` 这样的表可以直接编辑。它还包含一些 MySQL 的扩展表。

- Information Schema 提供了一种查看系统元数据的 ANSI 标准方式。除了为 MySQL 兼容性包含的表外，TiDB 还提供了许多自定义的 `INFORMATION_SCHEMA` 表。许多 `INFORMATION_SCHEMA` 表都有相应的 `SHOW` 命令。查询 `INFORMATION_SCHEMA` 的好处是可以在表之间进行连接。

- Performance Schema。TiDB 实现了性能模式表以实现 MySQL 兼容性。

### 缓存表

TiDB 为经常访问但很少更新的小型热点表引入了[缓存表](/cached-tables.md)功能。使用此功能时，整个表的数据会加载到 TiDB 服务器的内存中，TiDB 直接从内存中获取表数据而无需访问 TiKV，从而提高读取性能。

### 临时表

临时表功能解决了应用程序临时存储中间结果的问题，使您无需频繁创建和删除表。您可以将中间计算数据存储在临时表中。当不再需要中间数据时，TiDB 会自动清理和回收临时表。这避免了用户应用程序过于复杂，减少了表管理开销，并提高了性能。

### 分区表

在 TiDB 中，[分区](/partitioned-table.md)使您能够将一个大表划分为一个或多个称为分区的可管理部分。每个分区都是独立的，可以单独管理。

## 列

列从属于表。每个表至少有一列。列通过将每行中的值划分为单一数据类型的小单元，为表提供结构。

更多信息，请参见[定义列](/develop/dev-guide-create-table.md#define-columns)。

## 生成列

TiDB 允许您将 JSON 数据类型中的数据提取为[生成列](/generated-columns.md)。

与普通列不同，生成列的值是由列定义中的表达式计算得出的。在插入或更新生成列时，您不能分配值，只能使用 `DEFAULT`。

生成列有两种类型：虚拟列和存储列。虚拟生成列不占用存储空间，在读取时计算。存储生成列在写入（插入或更新）时计算，并占用存储空间。与虚拟生成列相比，存储生成列具有更好的读取性能，但占用更多磁盘空间。

## 数据类型

TiDB 支持除 `SPATIAL` 类型外的所有 MySQL 数据类型。这包括所有[数值类型](/data-type-numeric.md)、[字符串类型](/data-type-string.md)、[日期和时间类型](/data-type-date-and-time.md)以及 [JSON 类型](/data-type-json.md)。

## 索引

索引是表中选定列的副本。您可以使用[表](/develop/dev-guide-schema-design-overview.md#table)的一个或多个列创建索引。通过索引，TiDB 可以快速定位数据，而无需每次都搜索表中的每一行，这大大提高了查询性能。

有两种常见的索引类型：

- 主键：主键列上的索引。

- 二级索引：非主键列上的索引

### 唯一索引

TiDB 中的唯一索引在一个或多个列上强制实施唯一性，确保表中没有两行在索引列中具有相同的值。这种约束提供了一种维护数据完整性的方法，防止重复值，使唯一索引非常适合那些自然应该是唯一的字段，如电子邮件地址、用户名或产品代码。

### 主键索引

主键索引是表中一个或多个列上的唯一索引，作为每行的主要标识符。在 TiDB 中，每个表必须有一个主键，可以由用户显式定义，如果未指定主键，则由 TiDB 隐式定义。

### 复合索引

复合索引是在表的两个或多个列上构建的索引，对于按多个字段过滤或排序数据的查询特别有用。例如，在人员表中创建一个包含 `last_name` 和 `first_name` 的复合索引，允许 TiDB 基于两个名字快速定位记录。

### 不可见索引

不可见索引是存在于数据库中但对查询优化器隐藏的索引，这意味着它们在查询计划中被忽略。在 TiDB 中，不可见索引对于测试和调试很有用，允许您评估索引对性能的影响而无需完全删除它。

从 TiDB v8.0.0 开始，您可以通过修改 [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800) 系统变量使优化器选择不可见索引。

### 聚簇索引

在聚簇索引中，"聚簇"指的是数据存储的组织方式，而不是一组数据库服务器的协同工作。一些数据库管理系统将聚簇索引称为索引组织表（IOT）。

此功能控制包含主键的表中数据的存储方式。它使 TiDB 能够以一种可以提高某些查询性能的方式组织表。

更多信息，请参见[聚簇索引](/clustered-indexes.md)。

### 二级索引

二级索引是 TiDB 集群中的一个逻辑对象。您可以简单地将其视为 TiDB 用来提高查询性能的一种数据排序方式。在 TiDB 中，创建二级索引是一个在线操作，不会阻塞表上的任何数据读写操作。对于每个索引，TiDB 为表中的每一行创建引用，并按选定的列对引用进行排序，而不是直接对数据进行排序。

有关二级索引的更多信息，请参见[二级索引](https://docs.pingcap.com/tidb/stable/tidb-best-practices#secondary-index)。

在 TiDB 中，您可以[向现有表添加二级索引](/develop/dev-guide-create-secondary-indexes.md#add-a-secondary-index-to-an-existing-table)或[在创建新表时创建二级索引](/develop/dev-guide-create-secondary-indexes.md#create-a-secondary-index-when-creating-a-new-table)。

### 向量索引

对于以下 TiDB 部署选项，TiDB 支持向量数据类型和向量搜索索引。

- TiDB Cloud Serverless

- TiDB Self-Managed v8.4.0 或更高版本

在 TiDB 中，向量索引是一种专门设计的索引，用于在包含向量数据的列上进行高效的近似最近邻（ANN）搜索。向量索引，特别是 HNSW（分层可导航小世界）算法，允许 K-最近邻（KNN）搜索快速识别向量空间中最接近的数据点。这显著提高了查询性能，使结果能够在毫秒级内返回，相比暴力搜索方法有很大提升。

向量索引依赖 TiFlash 副本进行数据存储和搜索功能。在创建和使用向量索引之前，请确保集群中有可用的 TiFlash 节点。

## 约束

TiDB 支持几乎与 MySQL 相同的约束。

### NOT NULL 约束

`NOT NULL` 约束确保列不能包含 `NULL` 值。

当列被定义为 `NOT NULL` 约束时，TiDB 确保任何尝试在该列中插入或更新 `NULL` 值的行都会导致错误。这种行为与 MySQL 的 `NOT NULL` 约束实现一致。

### CHECK 约束

`CHECK` 约束限制表中列的值必须满足您指定的条件。当向表中添加 `CHECK` 约束时，TiDB 在插入或更新数据时检查是否满足约束。如果不满足约束，则返回错误。

### 主键约束

与 MySQL 一样，TiDB 中的主键约束包含唯一约束，即创建主键约束等同于具有唯一约束。此外，TiDB 的其他主键约束也与 MySQL 类似。

### 唯一键约束

唯一约束意味着唯一索引和主键列中的所有非空值都是唯一的。

### FOREIGN KEY 约束

外键是一个数据库约束，通过将一个表（子表）中的列链接到另一个表（父表）中的列来强制两个表之间的引用完整性。这确保子表中外键列的值与父表中主键或唯一键列的值匹配。例如，`orders` 表中的记录可能有一个链接到 `customers` 表中客户的外键，这确保每个订单都与有效的客户关联。

从 v6.6.0 开始，TiDB 支持外键约束作为实验性功能。此功能允许相关数据的跨表引用，并通过强制引用完整性帮助维护数据一致性。但是，需要注意的是，由于可能存在性能问题，特别是在大数据量的情况下，此功能是实验性的，不建议在生产环境中使用。

更多信息，请参见[外键约束](/foreign-key.md)。

## 视图

视图作为一个虚拟表，其模式由创建视图的 `SELECT` 语句定义。使用视图有以下好处：

- 仅向用户公开安全的字段和数据，以确保底层表中存储的敏感字段和数据的安全性。

- 将经常出现的复杂查询定义为视图，使复杂查询更简单和方便。

更多信息，请参见[视图](/views.md)。

## 序列

序列是一个数据库对象，设计用于根据指定的规则集生成一系列数字。此功能在需要唯一标识符的场景中特别有用，例如在创建数据库表的主键时。

更多信息，请参见[序列](/sql-statements/sql-statement-create-sequence.md)。

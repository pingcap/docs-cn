---
title: 创建表
summary: 了解表创建中的定义、规则和指南。
---

# 创建表

本文介绍如何使用 SQL 语句创建表以及相关的最佳实践。文档提供了基于 TiDB 的 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用程序示例来说明这些最佳实践。

## 开始之前

在阅读本文之前，请确保完成以下任务：

- [构建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)
- 阅读[数据库设计概述](/develop/dev-guide-schema-design-overview.md)
- [创建数据库](/develop/dev-guide-create-database.md)

## 什么是表

[表](/develop/dev-guide-schema-design-overview.md#table)是 TiDB 集群中从属于[数据库](/develop/dev-guide-schema-design-overview.md#database)的逻辑对象。它用于存储从 SQL 语句发送的数据。表以行和列的形式保存数据记录。一个表至少有一列。如果你定义了 `n` 列，每行数据都具有与这 `n` 列完全相同的字段。

## 命名表

创建表的第一步是为表命名。不要使用会给自己或同事带来困扰的无意义名称。建议你遵循公司或组织的表命名约定。

`CREATE TABLE` 语句通常采用以下形式：

```sql
CREATE TABLE {table_name} ( {elements} );
```

**参数说明**

- `{table_name}`：要创建的表的名称。
- `{elements}`：以逗号分隔的表元素列表，如列定义和主键定义。

假设你需要在 `bookshop` 数据库中创建一个表来存储用户信息。

注意，你还不能执行以下 SQL 语句，因为还没有添加任何列。

```sql
CREATE TABLE `bookshop`.`users` (
);
```

## 定义列

**列**从属于表。每个表至少有一列。列通过将每行中的值划分为单一数据类型的小单元，为表提供结构。

列定义通常采用以下形式：

```
{column_name} {data_type} {column_qualification}
```

**参数说明**

- `{column_name}`：列名。
- `{data_type}`：列的[数据类型](/data-type-overview.md)。
- `{column_qualification}`：列限定符，如**列级约束**或[生成列](/generated-columns.md)子句。

你可以向 `users` 表添加一些列，如唯一标识符 `id`、`balance` 和 `nickname`。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

在上述语句中，定义了一个名为 `id` 且类型为 [bigint](/data-type-numeric.md#bigint-type) 的字段。这用于表示唯一的用户标识符。这意味着所有用户标识符都应该是 `bigint` 类型。

然后，定义了一个名为 `nickname` 的字段，它是 [varchar](/data-type-string.md#varchar-type) 类型，长度限制为 100 个字符。这意味着用户的 `nicknames` 使用 `varchar` 类型，且不超过 100 个字符。

最后，添加了一个名为 `balance` 的字段，它是 [decimal](/data-type-numeric.md#decimal-type) 类型，具有 `15` 的**精度**和 `2` 的**小数位数**。**精度**表示字段中的总位数，**小数位数**表示小数点后的位数。例如，`decimal(5,2)` 表示精度为 `5`，小数位数为 `2`，范围从 `-999.99` 到 `999.99`。`decimal(6,1)` 表示精度为 `6`，小数位数为 `1`，范围从 `-99999.9` 到 `99999.9`。**decimal** 是一种[定点类型](/data-type-numeric.md#fixed-point-types)，可以用来精确存储数字。在需要精确数字的场景（例如，与用户资产相关的场景）中，请确保使用 **decimal** 类型。

TiDB 支持许多其他列数据类型，包括[整数类型](/data-type-numeric.md#integer-types)、[浮点类型](/data-type-numeric.md#floating-point-types)、[定点类型](/data-type-numeric.md#fixed-point-types)、[日期和时间类型](/data-type-date-and-time.md)以及[枚举类型](/data-type-string.md#enum-type)。你可以参考支持的列[数据类型](/data-type-overview.md)，并使用与你想要在数据库中保存的数据相匹配的**数据类型**。

让我们再复杂一点，你可以定义一个 `books` 表，这将是 `bookshop` 数据的核心。`books` 表包含书籍的 ID、标题、类型（例如，杂志、小说、生活、艺术）、库存、价格和出版日期等字段。

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint NOT NULL,
  `title` varchar(100),
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports'),
  `published_at` datetime,
  `stock` int,
  `price` decimal(15,2)
);
```

这个表包含的数据类型比 `users` 表更多。

- [int](/data-type-numeric.md#integer-types)：建议使用合适大小的类型，以避免使用过多磁盘空间甚至影响性能（类型范围过大）或数据溢出（数据类型范围过小）。
- [datetime](/data-type-date-and-time.md)：**datetime** 类型可用于存储时间值。
- [enum](/data-type-string.md#enum-type)：枚举类型可用于存储有限的选择值。

## 选择主键

[主键](/constraints.md#primary-key)是表中的一列或一组列，其值唯一标识表中的一行。

> **注意：**
>
> TiDB 中**主键**的默认定义与 [InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html)（MySQL 的常用存储引擎）中的不同。
>
> - 在 **InnoDB** 中：**主键**是唯一的、非空的，并且是**聚簇索引**。
>
> - 在 TiDB 中：**主键**是唯一的且非空的。但主键不保证是**聚簇索引**。相反，另一组关键字 `CLUSTERED` / `NONCLUSTERED` 额外控制**主键**是否为**聚簇索引**。如果未指定关键字，则由系统变量 `@@global.tidb_enable_clustered_index` 控制，如[聚簇索引](https://docs.pingcap.com/tidb/stable/clustered-indexes)中所述。

**主键**在 `CREATE TABLE` 语句中定义。[主键约束](/constraints.md#primary-key)要求所有受约束的列只包含非空值。

可以创建没有**主键**或具有非整数**主键**的表。在这种情况下，TiDB 会创建一个 `_tidb_rowid` 作为**隐式主键**。隐式主键 `_tidb_rowid` 由于其单调递增的特性，可能会在写入密集的场景中造成写入热点。因此，如果你的应用程序是写入密集型的，请考虑使用 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 和 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 参数对数据进行分片。但是，这可能会导致读放大，所以你需要权衡取舍。

当表的**主键**是[整数类型](/data-type-numeric.md#integer-types)并且使用 `AUTO_INCREMENT` 时，无法通过使用 `SHARD_ROW_ID_BITS` 来避免热点。如果你需要避免热点并且不需要连续递增的主键，可以使用 [`AUTO_RANDOM`](/auto-random.md) 代替 `AUTO_INCREMENT` 来消除行 ID 的连续性。

<CustomContent platform="tidb">

有关如何处理热点问题的更多信息，请参考[热点问题处理](/troubleshoot-hot-spot-issues.md)。

</CustomContent>

按照[选择主键的指南](#选择主键时需要遵循的指南)，以下示例展示了如何在 `users` 表中定义 `AUTO_RANDOM` 主键。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

## 聚簇或非聚簇

TiDB 从 v5.0 开始支持[聚簇索引](/clustered-indexes.md)功能。此功能控制包含主键的表中数据的存储方式。它使 TiDB 能够以可以提高某些查询性能的方式组织表。

此上下文中的聚簇指的是数据存储的组织方式，而不是一组数据库服务器的协同工作。一些数据库管理系统将聚簇索引表称为索引组织表（IOT）。

目前，TiDB 中**包含主键**的表分为以下两类：

- `NONCLUSTERED`：表的主键是非聚簇索引。在具有非聚簇索引的表中，行数据的键由 TiDB 隐式分配的内部 `_tidb_rowid` 组成。由于主键本质上是唯一索引，具有非聚簇索引的表需要至少两个键值对来存储一行，即：
    - `_tidb_rowid`（键）- 行数据（值）
    - 主键数据（键）- `_tidb_rowid`（值）
- `CLUSTERED`：表的主键是聚簇索引。在具有聚簇索引的表中，行数据的键由用户给定的主键数据组成。因此，具有聚簇索引的表只需要一个键值对来存储一行，即：
    - 主键数据（键）- 行数据（值）

如[选择主键](#选择主键)中所述，TiDB 使用关键字 `CLUSTERED` 和 `NONCLUSTERED` 来控制**聚簇索引**。

> **注意：**
>
> TiDB 仅支持通过表的 `PRIMARY KEY` 进行聚簇。启用聚簇索引后，术语 `PRIMARY KEY` 和聚簇索引可能会互换使用。`PRIMARY KEY` 指的是约束（逻辑属性），而聚簇索引描述了数据存储的物理实现方式。

按照[选择聚簇索引的指南](#选择聚簇索引时需要遵循的指南)，以下示例创建了一个 `books` 和 `users` 之间的关联表，表示用户对书籍的 `ratings`。该示例创建表并使用 `book_id` 和 `user_id` 构造复合主键，并在该**主键**上创建**聚簇索引**。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime,
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```
## 添加列约束

除了[主键约束](#选择主键)外，TiDB 还支持其他**列约束**，如 [NOT NULL](/constraints.md#not-null) 约束、[UNIQUE KEY](/constraints.md#unique-key) 约束和 `DEFAULT`。有关完整约束，请参考 [TiDB 约束](/constraints.md)文档。

### 设置默认值

要在列上设置默认值，请使用 `DEFAULT` 约束。默认值允许你在不为每列指定值的情况下插入数据。

你可以将 `DEFAULT` 与[支持的 SQL 函数](/functions-and-operators/functions-and-operators-overview.md)一起使用，将默认值的计算从应用层移出，从而节省应用层的资源。计算消耗的资源并没有消失，而是移到了 TiDB 集群。通常，你可以使用默认时间插入数据。以下示例展示了在 `ratings` 表中设置默认值：

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

此外，如果在更新数据时也需要默认填充当前时间，可以使用以下语句（但在 `ON UPDATE` 后只能填写与当前时间相关的表达式）：

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

有关不同数据类型的默认值的更多信息，请参见[默认值](/data-type-default-values.md)。

### 防止重复值

如果你需要防止列中出现重复值，可以使用 `UNIQUE` 约束。

例如，要确保用户昵称是唯一的，你可以这样重写 `users` 表的创建 SQL 语句：

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

如果你尝试在 `users` 表中插入相同的 `nickname`，将返回错误。

### 防止空值

如果你需要防止列中出现空值，可以使用 `NOT NULL` 约束。

以用户昵称为例。要确保昵称不仅唯一而且不为空，你可以这样重写创建 `users` 表的 SQL 语句：

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

## 使用 HTAP 功能

<CustomContent platform="tidb">

> **注意：**
>
> 本指南中提供的步骤**仅**适用于测试环境的快速入门。对于生产环境，请参考[探索 HTAP](/explore-htap.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本指南中提供的步骤**仅**适用于快速入门。有关更多说明，请参考[使用带有 TiFlash 的 HTAP 集群](/tiflash/tiflash-overview.md)。

</CustomContent>

假设你想对 `bookshop` 应用程序中的 `ratings` 表进行 OLAP 分析，例如，查询**书籍评分是否与评分时间有显著相关性**，这是为了分析用户对书籍的评分是否客观。那么你需要查询整个 `ratings` 表的 `score` 和 `rated_at` 字段。这个操作对于仅支持 OLTP 的数据库来说是资源密集型的。或者你可以使用一些 ETL 或其他数据同步工具将数据从 OLTP 数据库导出到专用的 OLAP 数据库进行分析。

在这种场景下，TiDB 作为一个支持 OLTP 和 OLAP 场景的 **HTAP（混合事务和分析处理）**数据库，是一个理想的一站式数据库解决方案。

### 复制列式数据

<CustomContent platform="tidb">

目前，TiDB 支持两个数据分析引擎，**TiFlash** 和 **TiSpark**。对于大数据场景（100 T），推荐使用 **TiFlash MPP** 作为 HTAP 的主要解决方案，**TiSpark** 作为补充解决方案。

要了解更多关于 TiDB HTAP 功能的信息，请参考以下文档：[TiDB HTAP 快速入门指南](/quick-start-with-htap.md)和[探索 HTAP](/explore-htap.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

要了解更多关于 TiDB HTAP 功能的信息，请参见 [TiDB Cloud HTAP 快速入门](/tidb-cloud/tidb-cloud-htap-quickstart.md)和[使用带有 TiFlash 的 HTAP 集群](/tiflash/tiflash-overview.md)。

</CustomContent>

在本例中，选择了 [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) 作为 `bookshop` 数据库的数据分析引擎。

TiFlash 在部署后不会自动复制数据。因此，你需要手动指定要复制的表：

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

**参数说明**

- `{table_name}`：表名。
- `{count}`：复制副本的数量。如果为 0，则删除复制副本。

**TiFlash** 随后将复制该表。当执行查询时，TiDB 会根据成本优化自动选择使用 TiKV（行式）或 TiFlash（列式）进行查询。或者，你可以手动指定查询是否使用 **TiFlash** 副本。要了解如何指定，请参考[使用 TiDB 读取 TiFlash 副本](/tiflash/use-tidb-to-read-tiflash.md)。

### HTAP 功能使用示例

为 `ratings` 表开启 `1` 个 TiFlash 副本：

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **注意：**
>
> 如果你的集群不包含 **TiFlash** 节点，这条 SQL 语句会报错：`1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0`。你可以使用[构建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-cloud-serverless-cluster)来创建一个包含 **TiFlash** 的 TiDB Cloud Serverless 集群。

然后你可以执行以下查询：

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

你还可以执行 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句来查看此语句是否使用了 **TiFlash**：

```sql
EXPLAIN ANALYZE SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

运行结果：

```sql
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| id                          | estRows   | actRows | task         | access object | execution info                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                  | memory   | disk |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| Projection_4                | 299821.99 | 24      | root         |               | time:60.8ms, loops:6, Concurrency:5                                                                                                                                                                                                                                                                                                                                  | hour(cast(bookshop.ratings.rated_at, time))->Column#6, Column#5                                                                                | 17.7 KB  | N/A  |
| └─HashAgg_5                 | 299821.99 | 24      | root         |               | time:60.7ms, loops:6, partial_worker:{wall_time:60.660079ms, concurrency:5, task_num:293, tot_wait:262.536669ms, tot_exec:40.171833ms, tot_time:302.827753ms, max:60.636886ms, p95:60.636886ms}, final_worker:{wall_time:60.701437ms, concurrency:5, task_num:25, tot_wait:303.114278ms, tot_exec:176.564µs, tot_time:303.297475ms, max:60.69326ms, p95:60.69326ms}  | group by:Column#10, funcs:avg(Column#8)->Column#5, funcs:firstrow(Column#9)->bookshop.ratings.rated_at                                         | 714.0 KB | N/A  |
|   └─Projection_15           | 300000.00 | 300000  | root         |               | time:58.5ms, loops:294, Concurrency:5                                                                                                                                                                                                                                                                                                                                | cast(bookshop.ratings.score, decimal(8,4) BINARY)->Column#8, bookshop.ratings.rated_at, hour(cast(bookshop.ratings.rated_at, time))->Column#10 | 366.2 KB | N/A  |
|     └─TableReader_10        | 300000.00 | 300000  | root         |               | time:43.5ms, loops:294, cop_task: {num: 1, max: 43.1ms, proc_keys: 0, rpc_num: 1, rpc_time: 43ms, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                        | data:TableFullScan_9                                                                                                                           | 4.58 MB  | N/A  |
|       └─TableFullScan_9     | 300000.00 | 300000  | cop[tiflash] | table:ratings | tiflash_task:{time:5.98ms, loops:8, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:45, total_skipped_packs:1, total_scanned_rows:368640, total_skipped_rows:8192, total_rs_index_load_time: 1ms, total_read_time: 1ms},total_create_snapshot_time:1ms}                                                                                                        | keep order:false                                                                                                                               | N/A      | N/A  |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
```

当出现字段 `cop[tiflash]` 时，表示任务被发送到 **TiFlash** 进行处理。
## 执行 `CREATE TABLE` 语句

按照上述规则创建所有表后，我们的[数据库初始化](/develop/dev-guide-bookshop-schema-design.md#database-initialization-script-dbinitsql)脚本应该是这样的。如果你需要查看详细的表信息，请参考[表的描述](/develop/dev-guide-bookshop-schema-design.md#description-of-the-tables)。

将数据库初始化脚本命名为 `init.sql` 并保存，你可以执行以下语句来初始化数据库。

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < init.sql
```

要查看 `bookshop` 数据库下的所有表，使用 [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md#show-full-tables) 语句。

```sql
SHOW TABLES IN `bookshop`;
```

运行结果：

```
+--------------------+
| Tables_in_bookshop |
+--------------------+
| authors            |
| book_authors       |
| books              |
| orders             |
| ratings            |
| users              |
+--------------------+
```

## 创建表时需要遵循的指南

本节提供了创建表时需要遵循的指南。

### 命名表时需要遵循的指南

- 使用**完全限定**的表名（例如，`CREATE TABLE {database_name}. {table_name}`）。如果不指定数据库名称，TiDB 将使用你的 **SQL 会话**中的当前数据库。如果你没有使用 `USE {databasename};` 在 SQL 会话中指定数据库，TiDB 将返回错误。
- 使用有意义的表名。例如，如果你需要创建一个用户表，你可以使用以下名称：`user`、`t_user`、`users`，或遵循你公司或组织的命名约定。如果你的公司或组织没有命名约定，你可以参考[表命名约定](/develop/dev-guide-object-naming-guidelines.md#table-naming-convention)。不要使用这样的表名：`t1`、`table1`。
- 多个单词用下划线分隔，建议名称不超过 32 个字符。
- 为不同业务模块的表创建单独的 `DATABASE`，并添加相应的注释。

### 定义列时需要遵循的指南

- 检查列支持的[数据类型](/data-type-overview.md)，并根据数据类型限制组织数据。为计划存储在列中的数据选择适当的类型。
- 检查[选择主键的指南](#选择主键时需要遵循的指南)，并决定是否使用主键列。
- 检查[选择聚簇索引的指南](#选择聚簇索引时需要遵循的指南)，并决定是否指定**聚簇索引**。
- 检查[添加列约束](#添加列约束)，并决定是否向列添加约束。
- 使用有意义的列名。建议遵循你公司或组织的表命名约定。如果你的公司或组织没有相应的命名约定，请参考[列命名约定](/develop/dev-guide-object-naming-guidelines.md#column-naming-convention)。

### 选择主键时需要遵循的指南

- 在表中定义**主键**或**唯一索引**。
- 尽量选择有意义的**列**作为**主键**。
- 出于性能考虑，尽量避免存储过宽的表。不建议表字段数超过 `60` 个，单行数据总大小超过 `64K`。建议将数据长度过大的字段拆分到另一个表。
- 不建议使用复杂的数据类型。
- 对于要进行连接的字段，确保数据类型一致，避免隐式转换。
- 避免在单个单调数据列上定义**主键**。如果你使用单个单调数据列（例如，具有 `AUTO_INCREMENT` 属性的列）来定义**主键**，可能会影响写入性能。如果可能，使用 `AUTO_RANDOM` 代替 `AUTO_INCREMENT`，这样可以放弃主键的连续和递增属性。
- 如果你确实需要在写入密集的场景下在单个单调数据列上创建索引，不要将这个单调数据列定义为**主键**，你可以使用 `AUTO_RANDOM` 为该表创建**主键**，或使用 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 和 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 对 `_tidb_rowid` 进行分片。

### 选择聚簇索引时需要遵循的指南

- 遵循[选择主键的指南](#选择主键时需要遵循的指南)来构建**聚簇索引**。
- 与具有非聚簇索引的表相比，具有聚簇索引的表在以下场景中提供更大的性能和吞吐量优势：
    - 插入数据时，聚簇索引减少了一次网络中索引数据的写入。
    - 当查询只涉及主键的等值条件时，聚簇索引减少了一次网络中索引数据的读取。
    - 当查询只涉及主键的范围条件时，聚簇索引减少了多次网络中索引数据的读取。
    - 当查询只涉及主键前缀的等值或范围条件时，聚簇索引减少了多次网络中索引数据的读取。
- 另一方面，具有聚簇索引的表可能会有以下问题：
    - 当你插入大量值接近的主键时，可能会出现写入热点问题。遵循[选择主键时需要遵循的指南](#选择主键时需要遵循的指南)。
    - 如果主键的数据类型大于 64 位，特别是当有多个二级索引时，表数据会占用更多存储空间。

- 要控制[是否使用聚簇索引的默认行为](/clustered-indexes.md#create-a-table-with-clustered-indexes)，你可以显式指定是否使用聚簇索引，而不是使用系统变量 `@@global.tidb_enable_clustered_index` 和配置 `alter-primary-key`。

### 执行 `CREATE TABLE` 语句时需要遵循的指南

- 不建议使用客户端 Driver 或 ORM 进行数据库架构更改。建议使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)或使用 GUI 客户端进行数据库架构更改。在本文档中，大多数场景下使用 **MySQL 客户端**传入 SQL 文件来执行数据库架构更改。
- 遵循[创建和删除表的 SQL 开发规范](/develop/dev-guide-sql-development-specification.md#create-and-delete-tables)。建议在业务应用程序内部包装构建和删除语句，添加判断逻辑。

## 下一步

请注意，本文档中创建的所有表都不包含二级索引。有关添加二级索引的指南，请参考[创建二级索引](/develop/dev-guide-create-secondary-indexes.md)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>

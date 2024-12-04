---
title: 创建表
summary: 创建表的方法、规范及例子。
---

# 创建表

本文档介绍如何使用 SQL 语句来创建表以及创建表的最佳实践。本文档提供了一个基于 TiDB 的 [bookshop](/develop/dev-guide-bookshop-schema-design.md) 数据库的示例加以说明。

> **注意：**
>
> 此处仅对 `CREATE TABLE` 语句进行简单描述，详细参考文档（包含其他示例），可参阅 [CREATE TABLE](/sql-statements/sql-statement-create-table.md) 文档。

## 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读[数据库模式概览](/develop/dev-guide-schema-design-overview.md)。
- [创建一个数据库](/develop/dev-guide-create-database.md)。

## 什么是表

[表](/develop/dev-guide-schema-design-overview.md#表-table)是集群中的一种逻辑对象，它从属于[数据库](/develop/dev-guide-schema-design-overview.md#数据库-database)，用于保存从 SQL 中发送的数据。表以行和列的形式组织数据记录,一张表至少有一列。若在表中定义了 n 个列，那么每一行数据都将拥有与这 n 个列中完全一致的字段。

## 命名表

创建表的第一步，就是给你的表起个名字。请不要使用无意义的表名，将给未来的你或者你的同事带来极大的困扰。推荐你遵循公司或组织的表命名规范。

`CREATE TABLE` 语句通常采用以下形式：

```sql
CREATE TABLE {table_name} ( {elements} );
```

**参数描述**

- `{table_name}`: 表名。
- `{elements}`: 以逗号分隔的表元素列表，比如列定义，主键定义等。

假设你需要创建一个表来存储 `bookshop` 库中的用户信息。

注意，此时因为一个列都没被添加，所以下方这条 SQL 暂时还不能被运行：

```sql
CREATE TABLE `bookshop`.`users` (
);
```

## 定义列

**列**从属于表，每张表都至少有一**列**。**列**通过将每行中的值分成一个个单一数据类型的小单元来为表提供结构。

列定义通常使用以下形式：

```
{column_name} {data_type} {column_qualification}
```

**参数描述**

- `{column_name}`：列名。
- `{data_type}`：列的[数据类型](/basic-features.md#数据类型函数和操作符)。
- `{column_qualification}`：列的限定条件，如**列级约束**或[生成列](/generated-columns.md)子句。

可以为 `users` 表添加一些列，如他们的唯一标识 `id`，余额 `balance` 及昵称 `nickname`。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

其中，定义了一个字段名为 `id`，类型为 [bigint](/data-type-numeric.md#bigint-类型) 的字段。用以表示用户唯一标识。这意味着，所有的用户标识都应该是 `bigint` 类型的。

而在其后，又定义了一个字段名为 `nickname`，类型为 [varchar](/data-type-string.md#varchar-类型)，且长度不得超过 100 字符的字段。用以表示用户的昵称。这意味着，所用用户的昵称都是 `varchar` 类型，且不超过 100 字符的。

最后，又加入了一个字段名为 `balance` 用以表示用户的余额，类型为 [decimal](/data-type-numeric.md#decimal-类型)，且其精度为 15，比例为 2。简单的说明一下精度和比例代表的含义，精度代表字段数值的总位数，而比例代表小数点后有多少位。例如: `decimal(5,2)`，即精度为 5，比例为 2 时，其取值范围为 `-999.99` 到 `999.99`。`decimal(6,1)`，即精度为 6，比例为 1 时，其取值范围为 `-99999.9` 到 `99999.9`。`decimal` 类型为定点数，可精确保存数字，在需要精确数字的场景（如用户财产相关）中，请确保使用[定点数](/data-type-numeric.md#定点类型)类型。

TiDB 支持许多其他的列数据类型，包含[整数](/data-type-numeric.md#整数类型)、[浮点数](/data-type-numeric.md#浮点类型)、[定点数](/data-type-numeric.md#定点类型)、[时间](/data-type-date-and-time.md#datetime-类型)、[枚举](/data-type-string.md#enum-类型) 等，可参考支持的列的[数据类型](/basic-features.md#数据类型函数和操作符)，并使用与你准备保存在数据库内的数据匹配的**数据类型**。

稍微提升一下复杂度，例如选择定义一张 `books` 表，这张表将是 `bookshop` 数据的核心。它包含书的唯一标识、名称、书籍类型（如：杂志、动漫、教辅等）、库存、价格、出版时间等字段。

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

这张表比 `users` 表包含更多的数据类型：

- [int](/data-type-numeric.md#integer-类型): 推荐使用合适大小的类型，防止使用过量的硬盘甚至影响性能(类型范围过大)或数据溢出(类型范围过小)。
- [datetime](/basic-features.md#数据类型函数和操作符): 可以使用 **datetime** 类型保存时间值。
- [enum](/data-type-string.md#enum-类型): 可以使用 **enum** 类型的枚举来保存有限选择的值。

## 选择主键

[主键](/constraints.md#主键约束)是一个或一组列，这个由所有主键列组合起来的值是数据行的唯一标识。

> **注意：**
>
> TiDB 中，关于 **Primary Key** 的默认定义与 MySQL 常用存储引擎 [InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html) 不一致。**InnoDB** 中，**Primary Key** 的语义为：唯一，不为空，**且为聚簇索引**。
>
> 而在 TiDB 中，**Primary Key** 的定义为：唯一，不为空。但主键不保证为**聚簇索引**。而是由另一组关键字 `CLUSTERED`、`NONCLUSTERED` 额外控制 **Primary Key** 是否为聚簇索引，若不指定，则由系统变量 `@@global.tidb_enable_clustered_index` 影响，具体说明请看[此文档](/clustered-indexes.md)。

主键在 `CREATE TABLE` 语句中定义。[主键约束](/constraints.md#主键约束)要求所有受约束的列仅包含非 `NULL` 值。

一个表可以没有主键，主键也可以是非整数类型。但此时 TiDB 就会创建一个 `_tidb_rowid` 作为隐式主键。隐式主键 `_tidb_rowid` 因为其单调递增的特性，可能在大批量写入场景下会导致写入热点，如果你写入量密集，可考虑通过 [SHARD_ROW_ID_BITS](/shard-row-id-bits.md) 和 [PRE_SPLIT_REGIONS](/sql-statements/sql-statement-split-region.md#pre_split_regions) 两参数控制打散。但这可能导致读放大，请自行取舍。

表的主键为[整数类型](/data-type-numeric.md#整数类型)且使用了 `AUTO_INCREMENT` 时，无法使用 `SHARD_ROW_ID_BITS` 消除热点。需解决此热点问题，且无需使用主键的连续和递增时，可使用 [AUTO_RANDOM](/auto-random.md) 替换 `AUTO_INCREMENT` 属性来消除行 ID 的连续性。

更多有关热点问题的处理办法，请参考[TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)。

需遵循[选择主键时应遵守的规则](#选择主键时应遵守的规则)，举一个 `users` 表中定义 `AUTO_RANDOM` 主键的例子：

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

## 选择聚簇索引

[聚簇索引](/clustered-indexes.md) (clustered index) 是 TiDB 从 v5.0 开始支持的特性，用于控制含有主键的表数据的存储方式。通过使用聚簇索引，TiDB 可以更好地组织数据表，从而提高某些查询的性能。有些数据库管理系统也将聚簇索引称为“索引组织表” (index-organized tables)。

目前 TiDB 中 **_含有主键_** 的表分为以下两类：

- `NONCLUSTERED`，表示该表的主键为非聚簇索引。在非聚簇索引表中，行数据的键由 TiDB 内部隐式分配的 `_tidb_rowid` 构成，而主键本质上是唯一索引，因此非聚簇索引表存储一行至少需要两个键值对，分别为：
    - `_tidb_rowid`（键）- 行数据（值）
    - 主键列数据（键） - `_tidb_rowid`（值）
- `CLUSTERED`，表示该表的主键为聚簇索引。在聚簇索引表中，行数据的键由用户给定的主键列数据构成，因此聚簇索引表存储一行至少只要一个键值对，即：
    - 主键列数据（键） - 行数据（值）

如[主键](#选择主键)中所述，聚簇索引在 TiDB 中，使用关键字 `CLUSTERED`、`NONCLUSTERED` 进行控制。

> **注意：**
>
> TiDB 仅支持根据表的主键来进行聚簇操作。聚簇索引启用时，“主键”和“聚簇索引”两个术语在一些情况下可互换使用。主键指的是约束（一种逻辑属性），而聚簇索引描述的是数据存储的物理实现。

需遵循[选择聚簇索引时应遵守的规则](#选择聚簇索引时应遵守的规则)，假设需要建立一张 `books` 和 `users` 之间关联的表，代表用户对某书籍的评分。使用表名 `ratings` 来创建该表，并使用 `book_id` 和 `user_id` 构建[复合主键](/constraints.md#主键约束)，并在该主键上建立聚簇索引：

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

除[主键约束](#选择主键)外，TiDB 还支持其他的列约束，如：[非空约束 `NOT NULL`](/constraints.md#非空约束)、[唯一约束 `UNIQUE KEY`](/constraints.md#唯一约束)、默认值 `DEFAULT` 等。完整约束，请查看 [TiDB 约束](/constraints.md)文档。

### 填充默认值

如需在列上设置默认值，请使用 `DEFAULT` 约束。默认值将可以使你无需指定每一列的值，就可以插入数据。

你可以将 `DEFAULT` 与[支持的 SQL 函数](/basic-features.md#数据类型函数和操作符)结合使用，将默认值的计算移出应用层，从而节省应用层的资源（当然，计算所消耗的资源并不会凭空消失，只是被转移到了 TiDB 集群中）。常见的，希望实现数据插入时，可默认填充默认的时间。还是使用 `ratings` 作为示例，可使用以下语句：

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

此外，如需在数据更新时也默认填入当前时间，可使用以下语句（但 `ON UPDATE` 后仅可填入与当前时间相关的表达式）：

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

关于不同数据类型默认值的更多信息，请参阅[数据类型的默认值](/data-type-default-values.md)。

### 防止重复

如果你需要防止列中出现重复值，那你可以使用 `UNIQUE` 约束。

例如，你需要确保用户的昵称唯一，可以这样改写 `users` 表的创建 SQL：

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

如果你在 `users` 表中尝试插入相同的 `nickname`，将返回错误。

### 防止空值

如果你需要防止列中出现空值，那就可以使用 `NOT NULL` 约束。

还是使用用户昵称来举例子，除了昵称唯一，还希望昵称不可为空，于是此处可以这样改写 `users` 表的创建 SQL：

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

## 使用 HTAP 能力

> **注意：**
>
> 本指南中有关 HTAP 的步骤仅适用于快速上手体验，不适用于生产环境。如需探索 HTAP 更多功能，请参考[深入探索 HTAP](/explore-htap.md)。

假设 `bookshop` 应用程序，有对用户评价的 `ratings` 表进行 OLAP 分析查询的需求，例如需查询: **书籍的评分，是否和评价的时间具有显著的相关性** 的需求，用以分析用户的书籍评分是否客观。那么会要求查询整个 `ratings` 表中的 `score` 和 `rated_at` 字段。这对普通仅支持的 OLTP 的数据库来说，是一个非常消耗资源的操作。或者使用一些 ETL 或其他数据同步工具，将 OLTP 数据库中的数据，导出到专用的 OLAP 数据库，再进行分析。

这种场景下，TiDB 就是一个比较理想的一站式数据库解决方案，TiDB 是一个 **HTAP (Hybrid Transactional and Analytical Processing)** 数据库，同时支持 OLTP 和 OLAP 场景。

### 同步列存数据

当前，TiDB 支持两种数据分析引擎：**TiFlash** 和 **TiSpark**。大数据场景 (100 T) 下，推荐使用 TiFlash MPP 作为 HTAP 的主要方案，TiSpark 作为补充方案。希望了解更多关于 TiDB 的 HTAP 能力，可参考以下文章：[快速上手 HTAP](/quick-start-with-htap.md) 和[深入探索 HTAP](/explore-htap.md)。

此处选用 [TiFlash](/tiflash/tiflash-overview.md) 为 `bookshop` 数据库的数据分析引擎。

TiFlash 部署完成后并不会自动同步数据，而需要手动指定需要同步的表，开启同步副本仅需一行 SQL，如下所示：

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

**参数描述**

- `{table_name}`: 表名。
- `{count}`: 同步副本数，若为 0，则表示删除同步副本。

随后，TiFlash 将同步该表，查询时，TiDB 将会自动基于成本优化，考虑使用 **TiKV (行存)** 或 **TiFlash (列存)** 进行数据查询。当然，除了自动的方法，你也可以直接指定查询是否使用 TiFlash 副本，使用方法可查看[使用 TiDB 读取 TiFlash](/tiflash/use-tidb-to-read-tiflash.md) 文档。

### 使用 HTAP 的示例

`ratings` 表开启 1 个 TiFlash 副本：

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **注意：**
>
> 如果你的集群，不包含 TiFlash 节点，此 SQL 语句将会报错：`1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0` 你可以[使用 TiDB Cloud Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-cloud-serverless-集群) 来创建一个含有 TiFlash 的集群。

随后正常进行查询即可：

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

也可使用 [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md) 语句查看此语句是否使用了 TiFlash 引擎：

```sql
EXPLAIN ANALYZE SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

运行结果为：

```
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

在出现 `cop[tiflash]` 字样时，表示该任务发送至 TiFlash 进行处理。

## 执行 `CREATE TABLE` 语句

按以上步骤创建所有表后，[数据库初始化](/develop/dev-guide-bookshop-schema-design.md#数据库初始化-dbinitsql-脚本)脚本应该如此所示。若需查看表信息详解，请参阅[数据表详解](/develop/dev-guide-bookshop-schema-design.md#数据表详解)。

如果将数据库初始化脚本命名为 `init.sql` 并保存，可使用以下语句来执行数据库初始化：

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < init.sql
```

需查看 `bookshop` 数据库下的所有表，可使用 [SHOW TABLES](/sql-statements/sql-statement-show-tables.md#show-full-tables) 语句：

```sql
SHOW TABLES IN `bookshop`;
```

运行结果为：

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

## 创建表时应遵守的规则

本小节给出了一些在创建表时应遵守的规则。

### 命名表时应遵守的规则

- 使用**完全限定**的表名称（例如：`CREATE TABLE {database_name}.{table_name}`）。这是因为你在不指定数据库名称时，TiDB 将使用你 **SQL 会话**中的[当前数据库](/sql-statements/sql-statement-use.md)。若你未在 SQL 会话中使用 `USE {databasename};` 来指定数据库，TiDB 将会返回错误。
- 请使用有意义的表名，例如，若你需要创建一个用户表，你可以使用名称：`user`, `t_user`, `users` 等，或遵循你公司或组织的命名规范。如果你的公司或组织没有相应的命名规范，可参考[表命名规范](/develop/dev-guide-object-naming-guidelines.md#表命名规范)。请勿使用这样的表名，如：`t1`, `table1` 等。
- 多个单词以下划线分隔，不推荐超过 32 个字符。
- 不同业务模块的表单独建立 `DATABASE`，并增加相应注释。

### 定义列时应遵守的规则

- 查看支持的列的[数据类型](/basic-features.md#数据类型函数和操作符)，并按照数据类型的限制来组织你的数据。为你计划被存在列中的数据选择合适的类型。
- 查看[选择主键时应遵守的规则](#选择主键时应遵守的规则)，决定是否使用主键列。
- 查看[选择聚簇索引时应遵守的规则](#选择聚簇索引时应遵守的规则)，决定是否指定聚簇索引。
- 查看[添加列约束](#添加列约束)，决定是否添加约束到列中。
- 请使用有意义的列名，推荐你遵循公司或组织的表命名规范。如果你的公司或组织没有相应的命名规范，可参考[列命名规范](/develop/dev-guide-object-naming-guidelines.md#字段命名规范)。

### 选择主键时应遵守的规则

- 在表内定义一个主键或唯一索引。
- 尽量选择有意义的列作为主键。
- 出于为性能考虑，尽量避免存储超宽表，表字段数不建议超过 60 个，建议单行的总数据大小不要超过 64K，数据长度过大字段最好拆到另外的表。
- 不推荐使用复杂的数据类型。
- 需要 JOIN 的字段，数据类型保障绝对一致，避免隐式转换。
- 避免在单个单调数据列上定义主键。如果你使用单个单调数据列（例如：`AUTO_INCREMENT` 的列）来定义主键，有可能会对写性能产生负面影响。可能的话，使用 `AUTO_RANDOM` 替换 `AUTO_INCREMENT`（这会失去主键的连续和递增特性）。
- 如果你 **_必须_** 在单个单调数据列上创建索引，且有大量写入的话。请不要将这个单调数据列定义为主键，而是使用 `AUTO_RANDOM` 创建该表的主键，或使用 [SHARD_ROW_ID_BITS](/shard-row-id-bits.md) 和 [PRE_SPLIT_REGIONS](/sql-statements/sql-statement-split-region.md#pre_split_regions) 打散 `_tidb_rowid`。

### 选择聚簇索引时应遵守的规则

- 遵循[选择主键时应遵守的规则](#选择主键时应遵守的规则)：

    聚簇索引将基于主键建立，请遵循选择主键时应遵守的规则，此为选择聚簇索引时应遵守规则的基础。

- 在以下场景中，尽量使用聚簇索引，将带来性能和吞吐量的优势：

    - 插入数据时会减少一次从网络写入索引数据。
    - 等值条件查询仅涉及主键时会减少一次从网络读取数据。
    - 范围条件查询仅涉及主键时会减少多次从网络读取数据。
    - 等值或范围条件查询仅涉及主键的前缀时会减少多次从网络读取数据。

- 在以下场景中，尽量避免使用聚簇索引，将带来性能劣势：

    - 批量插入大量取值相邻的主键时，可能会产生较大的写热点问题，请遵循[选择主键时应遵守的规则](#选择主键时应遵守的规则)。
    - 当使用大于 64 位的数据类型作为主键时，可能导致表数据需要占用更多的存储空间。该现象在存在多个二级索引时尤为明显。

- 显式指定是否使用聚簇索引，而非使用系统变量 `@@global.tidb_enable_clustered_index` 及配置项 `alter-primary-key` 控制是否使用[聚簇索引的默认行为](/clustered-indexes.md#创建聚簇索引表)。

### `CREATE TABLE` 执行时应遵守的规则

- 不推荐使用客户端的 Driver 或 ORM 来执行数据库模式的更改。基于过往经验，建议使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)或使用任意你喜欢的 GUI 客户端来进行数据库模式的更改。本文档中，将在大多数场景下，使用 **MySQL 客户端** 传入 SQL 文件来执行数据库模式的更改。
- 遵循 SQL 开发规范中的[建表删表规范](/develop/dev-guide-sql-development-specification.md#建表删表规范)，建议业务应用内部封装建表删表语句增加判断逻辑。

## 更进一步

请注意，到目前为止，创建的所有表都不包含二级索引。添加二级索引的指南，请参考[创建二级索引](/develop/dev-guide-create-secondary-indexes.md)。

---
title: 创建表
---

# 创建表

此页面提供了一个创建表的最佳实践指南，并提供了一个基于 TiDB 的 [bookshop](bookshop-schema-design.md) 数据库的示例。

> Note:
>
> 有关该 `CREATE TABLE` 语句的详细参考文档，包含其他示例，可参阅 [CREATE TABLE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-table) 文档

## 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud(DevTier) 构建 TiDB 集群](build-cluster-in-cloud.md)
- 阅读[数据库模式概览](schema-design-overview.md)
- [创建一个数据库](create-database.md)

## 创建表

[表](schema-design-overview.md#表-table)是集群中的一种逻辑对象，用于存储从应用程序的持久层或其他 SQL 中发送的数据。表以行和列的形式组织数据记录。

要创建表，请使用 [CREATE TABLE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-table) 语句，并遵循我们在下方列出的最佳实践：

- [命名表](#命名表)
- [定义列](#定义列)
- [选择主键](#选择主键)
- [选择是否聚簇](#选择是否聚簇)
- [添加额外的约束](#添加额外的约束)
- [使用 HTAP 能力](#使用-htap-能力)
- [执行 `CREATE TABLE` 语句](#执行-create-table-语句)

对每个最佳实践查看完毕后，你可以看看本章提供的示例。

### 命名表

给你的表起个名字，这是创建表的第一步。我们推荐你遵循公司或组织的表命名规范。

`CREATE TABLE` 语句通常采用以下形式：

```sql
CREATE TABLE {table_name} ( {elements} );
```

|      参数      |                      描述                      |
| :------------: | :--------------------------------------------: |
| `{table_name}` |                      表名                      |
|  `{elements}`  | 以逗号分隔的表元素列表，比如列定义，主键定义等 |

#### 表命名的最佳实践

以下是命名表时需要遵循的一些最佳实践：

- 使用 `完全限定` 的表名称（例如：`CREATE TABLE {database_name}.{table_name}`）。这是因为您在不指定数据库名称时，TiDB 将使用您 `SQL 会话` 中的[当前数据库](https://docs.pingcap.com/zh/tidb/stable/sql-statement-use)。若您未在 SQL 会话中使用 `USE {databasename};` 来指定数据库，TiDB 将会返回错误。
- 请使用有意义的表名，例如，若您需要创建一个用户表，您可以使用名称：`user`, `t_user`, `users` 等，或遵循您公司或组织的命名规范。如果您的公司或组织没有相应的命名规范，可参考[表命名规范](object-naming-guidelines.md#3-表命名规范)。请勿使用这样的表名，如：`t1`, `table1` 等。
- 多个单词以下划线分隔，不推荐超过 32 个字符。
- 不同业务模块的表单独建立 `DATABASE`，并增加相应注释

#### 表命名示例

假设您需要创建一个表来存储 `bookshop` 库中的用户信息。

注意，此时因为一个列都没被添加，所以下方这条 SQL 暂时还不能被运行：

```sql
CREATE TABLE `bookshop`.`users` (
);
```

### 定义列

`列` 通过将每行中的值分成一个个单一数据类型的小单元来为表提供结构。

列定义通常使用以下形式：

```
{column_name} {data_type} {column_qualification}
```

|           参数           |                                                                               描述                                                                                |
| :----------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|     `{column_name}`      |                                                                               列名                                                                                |
|      `{data_type}`       | 列的[数据类型](https://docs.pingcap.com/zh/tidb/stable/basic-features#%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%E5%87%BD%E6%95%B0%E5%92%8C%E6%93%8D%E4%BD%9C%E7%AC%A6) |
| `{column_qualification}` |                        列的限定条件，如 `列级约束` 或 [生成列（实验功能）](https://docs.pingcap.com/zh/tidb/stable/generated-columns)子句                         |

#### 列定义的最佳实践

以下是定义列时需要遵循的一些最佳实践：

- 查看支持的列的[数据类型](https://docs.pingcap.com/zh/tidb/stable/basic-features#%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%E5%87%BD%E6%95%B0%E5%92%8C%E6%93%8D%E4%BD%9C%E7%AC%A6)，并按照数据类型的限制来组织你的数据。为你计划被存在列中的数据选择合适的类型。
- 查看选择主键的[最佳实践](#主键选择的最佳实践)与[示例](#主键选择的示例)，决定是否使用主键列
- 查看选择聚簇索引的[最佳实践](#聚簇索引选择的最佳实践)与[示例](#聚簇索引选择的示例)，决定是否指定聚簇索引
- 查看[添加列约束](#添加列约束)，决定是否添加约束到列中
- 请使用有意义的列名，我们推荐你遵循公司或组织的表命名规范。如果您的公司或组织没有相应的命名规范，可参考[列命名规范](object-naming-guidelines.md#4-字段命名规范)。

#### 列定义示例

我们可以为 `users` 表添加一些列，如他们的唯一标识 `id`，余额 `balance` 及昵称 `nickname`。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

其中，我们定义了一个字段名为 `id`，类型为 [bigint](https://docs.pingcap.com/zh/tidb/stable/data-type-numeric#bigint-%E7%B1%BB%E5%9E%8B) 的字段。用以表示用户唯一标识。这意味着，所有的用户标识都应该是 `bigint` 类型的。

而我们在其后，又定义了一个字段名为 `nickname`，类型为 [varchar](https://docs.pingcap.com/zh/tidb/stable/data-type-string#varchar-%E7%B1%BB%E5%9E%8B)，且长度不得超过 100 字符的字段。用以表示用户的昵称。这意味着，所用用户的昵称都是 `varchar` 类型，且不超过 100 字符的。

最后，我们又加入了一个字段名为 `balance` 用以表示用户的余额，类型为 [decimal](https://docs.pingcap.com/zh/tidb/stable/data-type-numeric#%E5%AE%9A%E7%82%B9%E7%B1%BB%E5%9E%8B)，且其精度为 15，比例为 2。简单的说明一下精度和比例代表的含义，精度代表字段数值的总位数，而比例代表小数点后有多少位。例如: `decimal(5,2)`，即精度为 5，比例为 2 时，其取值范围为 `-999.99` 到 `999.99`。`decimal(6,1)` ，即精度为 6，比例为 1 时，其取值范围为 `-99999.9` 到 `99999.9`。`decimal` 类型为定点数，可精确保存数字，在需要精确数字的场景（如用户财产相关）中，请确保使用[定点数](https://docs.pingcap.com/zh/tidb/stable/data-type-numeric#%E5%AE%9A%E7%82%B9%E7%B1%BB%E5%9E%8B)类型。

TiDB 支持许多其他的列数据类型，包含 [整数](https://docs.pingcap.com/zh/tidb/stable/data-type-numeric#%E6%95%B4%E6%95%B0%E7%B1%BB%E5%9E%8B)、[浮点数](https://docs.pingcap.com/zh/tidb/stable/data-type-numeric#%E6%B5%AE%E7%82%B9%E7%B1%BB%E5%9E%8B)、[定点数](https://docs.pingcap.com/zh/tidb/stable/data-type-numeric#%E5%AE%9A%E7%82%B9%E7%B1%BB%E5%9E%8B)、
[时间](https://docs.pingcap.com/zh/tidb/stable/data-type-date-and-time#datetime-%E7%B1%BB%E5%9E%8B)、[枚举](https://docs.pingcap.com/zh/tidb/stable/data-type-string#enum-%E7%B1%BB%E5%9E%8B) 等，可参考支持的列的[数据类型](https://docs.pingcap.com/zh/tidb/stable/basic-features#%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%E5%87%BD%E6%95%B0%E5%92%8C%E6%93%8D%E4%BD%9C%E7%AC%A6)，并使用与您准备保存在数据库内的数据匹配的`数据类型`。

让我们稍微提升一下复杂度，例如我们会选择定义一张 `books` 表，这张表将是 `bookshop` 数据的核心。它包含书的 唯一标识、名称、书籍类型（如：杂志 / 动漫 / 教辅 等）、库存、价格、出版时间 字段。

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

- [int](https://docs.pingcap.com/zh/tidb/stable/data-type-numeric#integer-%E7%B1%BB%E5%9E%8B): 我们推荐使用合适大小的类型，防止使用过量的硬盘甚至影响性能(类型范围过大)或数据溢出(类型范围过小)
- [datetime](https://docs.pingcap.com/zh/tidb/stable/basic-features#%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%E5%87%BD%E6%95%B0%E5%92%8C%E6%93%8D%E4%BD%9C%E7%AC%A6): 可以使用 `datetime` 类型保存时间值
- [enum](https://docs.pingcap.com/zh/tidb/stable/data-type-string#enum-%E7%B1%BB%E5%9E%8B): 可以使用 `enum` 类型的枚举来保存有限选择的值

### 选择主键

[主键](https://docs.pingcap.com/zh/tidb/stable/constraints#%E4%B8%BB%E9%94%AE%E7%BA%A6%E6%9D%9F)是一个或一组列，这个由所有主键列组合起来的值是数据行的唯一标识。

> Note:
>
> TiDB 中，关于 `Primary Key` 的默认定义与 MySQL 常用存储引擎 [InnoDB](https://mariadb.com/kb/en/innodb/) 不一致。`InnoDB` 中，`Primary Key` 的语义为：唯一，不为空，**且为聚簇索引**。
>
> 而在 TiDB 中，`Primary Key` 的定义为：唯一，不为空。但主键不保证为**聚簇索引**。而是由另一组关键字 `CLUSTERED` / `NONCLUSTERED` 额外控制 `Primary Key` 是否为聚簇索引，若不指定，则由系统变量 `@@global.tidb_enable_clustered_index` 影响，具体说明请看[此文档](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes)。

主键在 `CREATE TABLE` 语句中定义。[主键约束](https://docs.pingcap.com/zh/tidb/stable/constraints#%E4%B8%BB%E9%94%AE%E7%BA%A6%E6%9D%9F)要求所有受约束的列仅包含非 `NULL` 值。

一个表可以没有主键，主键也可以是非整数类型。但此时 TiDB 就会创建一个 `_tidb_rowid` 作为隐式主键。隐式主键 `_tidb_rowid` 因为其单调递增的特性，可能在大批量写入场景下会导致写入热点，如果你写入量密集，可考虑通过 [SHARD_ROW_ID_BITS](https://docs.pingcap.com/zh/tidb/stable/shard-row-id-bits) 和 [PRE_SPLIT_REGIONS](https://docs.pingcap.com/zh/tidb/stable/sql-statement-split-region#pre_split_regions) 两参数控制打散。但这可能导致读放大，请自行取舍。

表的主键为 [整数类型](https://docs.pingcap.com/zh/tidb/stable/data-type-numeric#%E6%95%B4%E6%95%B0%E7%B1%BB%E5%9E%8B) 且使用了 `AUTO_INCREMENT` 时，无法使用 `SHARD_ROW_ID_BITS` 消除热点。需解决此热点问题，且无需使用主键的连续和递增时，可使用 [AUTO_RANDOM](https://docs.pingcap.com/zh/tidb/stable/auto-random) 替换 `AUTO_INCREMENT` 属性来消除行 ID 的连续性。

更多有关热点问题的处理办法，请参考[此处](https://docs.pingcap.com/zh/tidb/stable/troubleshoot-hot-spot-issues)。

#### 主键选择的最佳实践

以下是在 TiDB 中选择主键列时需要遵循的一些最佳实践：

- 在表内定义一个主键或唯一索引。
- 尽量选择有意义的列作为主键。
- 出于为性能考虑，尽量避免存储超宽表，表字段数不建议超过 60 个，建议单行的总数据大小不要超过 64K，数据长度过大字段最好拆到另外的表。
- 不推荐使用复杂的数据类型。
- 需要 JOIN 的字段，数据类型保障绝对一致，避免隐式转换。
- 避免在单个单调数据列上定义主键。如果你使用单个单调数据列（例如：`AUTO_INCREMENT` 的列）来定义主键，有可能会对写性能产生负面影响。可能的话，使用 `AUTO_RANDOM` 替换 `AUTO_INCREMENT`（这会失去主键的连续和递增特性）。
- 如果你 **_必须_** 在单个单调数据列上创建索引，且有大量写入的话。请不要将这个单调数据列定义为主键，而是使用 `AUTO_RANDOM` 创建该表的主键，或使用 [SHARD_ROW_ID_BITS](https://docs.pingcap.com/zh/tidb/stable/shard-row-id-bits) 和 [PRE_SPLIT_REGIONS](https://docs.pingcap.com/zh/tidb/stable/sql-statement-split-region#pre_split_regions) 打散 `_tidb_rowid`。

#### 主键选择的示例

需遵循[主键选择的最佳实践](#主键选择的最佳实践)，我们展示在 `users` 表中定义 `AUTO_RANDOM` 主键的场景：

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

### 选择聚簇索引

[聚簇索引](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes) (clustered index) 是 TiDB 从 v5.0 开始支持的特性，用于控制含有主键的表数据的存储方式。通过使用聚簇索引，TiDB 可以更好地组织数据表，从而提高某些查询的性能。有些数据库管理系统也将聚簇索引称为“索引组织表” (index-organized tables)。

目前 TiDB 中 **_含有主键_** 的表分为以下两类：

- `NONCLUSTERED`，表示该表的主键为非聚簇索引。在非聚簇索引表中，行数据的键由 TiDB 内部隐式分配的 `_tidb_rowid` 构成，而主键本质上是唯一索引，因此非聚簇索引表存储一行至少需要两个键值对，分别为
  - `_tidb_rowid`（键）- 行数据（值）
  - 主键列数据（键） - `_tidb_rowid`（值）
- `CLUSTERED`，表示该表的主键为聚簇索引。在聚簇索引表中，行数据的键由用户给定的主键列数据构成，因此聚簇索引表存储一行至少只要一个键值对，即
  - 主键列数据（键） - 行数据（值）

如[主键](#选择主键)中所述，聚簇索引在 TiDB 中，使用关键字 `CLUSTERED` / `NONCLUSTERED` 进行控制。

> 注意
>
> TiDB 仅支持根据表的主键来进行聚簇操作。聚簇索引启用时，“主键”和“聚簇索引”两个术语在一些情况下可互换使用。主键指的是约束（一种逻辑属性），而聚簇索引描述的是数据存储的物理实现。

#### 聚簇索引选择的最佳实践

以下是在 TiDB 中选择聚簇索引时需要遵循的一些最佳实践：

- 遵循 [主键选择的最佳实践](#主键选择的最佳实践)

  聚簇索引将基于主键建立，请遵循主键选择的最佳实践，以完成聚簇索引最佳实践的基础。

- 在以下场景中，尽量使用聚簇索引，将带来性能和吞吐量的优势：

  - 插入数据时会减少一次从网络写入索引数据。
  - 等值条件查询仅涉及主键时会减少一次从网络读取数据。
  - 范围条件查询仅涉及主键时会减少多次从网络读取数据。
  - 等值或范围条件查询仅涉及主键的前缀时会减少多次从网络读取数据。

- 在以下场景中，尽量避免使用聚簇索引，将带来性能劣势：

  - 批量插入大量取值相邻的主键时，可能会产生较大的写热点问题，请遵循[主键选择的最佳实践](#主键选择的最佳实践)。
  - 当使用大于 64 位的数据类型作为主键时，可能导致表数据需要占用更多的存储空间。该现象在存在多个二级索引时尤为明显。

- 显式指定是否使用聚簇索引，而非使用系统变量 `@@global.tidb_enable_clustered_index` 及配置项 `alter-primary-key` 控制是否使用[聚簇索引的默认行为](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes#%E5%88%9B%E5%BB%BA%E8%81%9A%E7%B0%87%E7%B4%A2%E5%BC%95%E8%A1%A8)。

#### 聚簇索引选择的示例

需遵循[聚簇索引选择的最佳实践](#聚簇索引选择的最佳实践)，假设我们将需要建立一张 `books` 和 `users` 之间关联的表，代表用户对某书籍的评分。我们使用表名 `ratings` 来创建该表，并使用 `book_id` 和 `user_id` 构建[复合主键](https://docs.pingcap.com/zh/tidb/stable/constraints#%E4%B8%BB%E9%94%AE%E7%BA%A6%E6%9D%9F)，并在该主键上建立聚簇索引：

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime,
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

### 添加列约束

除[主键约束](#选择主键)外，TiDB 还支持其他的列约束，如：[非空约束 `NOT NULL`](https://docs.pingcap.com/zh/tidb/stable/constraints#%E9%9D%9E%E7%A9%BA%E7%BA%A6%E6%9D%9F)、[唯一约束 `UNIQUE KEY`](https://docs.pingcap.com/zh/tidb/stable/constraints#%E5%94%AF%E4%B8%80%E7%BA%A6%E6%9D%9F)、默认值 `DEFAULT` 等。完整约束，请查看[此处](https://docs.pingcap.com/zh/tidb/stable/constraints)。

#### 填充默认值

如需在列上设置默认值，请使用 `DEFAULT` 约束。默认值将可以使你无需指定每一列的值，就可以插入数据。

你可以将 `DEFAULT` 与[支持的 SQL 函数](https://docs.pingcap.com/zh/tidb/stable/basic-features#%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%E5%87%BD%E6%95%B0%E5%92%8C%E6%93%8D%E4%BD%9C%E7%AC%A6)结合使用，将默认值的计算移出应用层，从而节省应用层的资源（当然，计算所消耗的资源并不会凭空消失，只是被转移到了 TiDB 集群中）。常见的，我们想实现数据插入时，可默认填充默认的时间。还是使用 `rating` 作为示例，可使用以下语句：

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

额外的，如果需更新时也默认填入当前时间，可使用以下语句（但 `ON UPDATE` 后仅可填入[当前时间相关语句](https://pingcap.github.io/sqlgram/#NowSymOptionFraction)，`DEFAULT` 后支持[更多选择](https://pingcap.github.io/sqlgram/#DefaultValueExpr)）：

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

#### 防止重复

如果你需要防止列中出现重复值，那你可以使用 `UNIQUE` 约束。

例如，你需要确保用户的昵称唯一，我们可以这样改写 `user` 表的创建 SQL：

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

如果你在 `user` 表中尝试插入相同的 `nickname`，将返回错误。

#### 防止空值

如果你需要防止列中出现空值，那就可以使用 `NOT NULL` 约束。

还是使用用户昵称来举例子，除了昵称唯一，我们还希望昵称不可为空，于是此处可以这样改写 `user` 表的创建 SQL：

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

### 使用 HTAP 能力

> Note:
>
> 本指南中有关 HTAP 的步骤仅适用于快速上手体验，不适用于生产环境。如需探索 HTAP 更多功能，请参考[深入探索 HTAP](https://docs.pingcap.com/zh/tidb/stable/explore-htap)。

假设我们的 `bookshop` 应用程序，有对用户评价的 `ratings` 表进行 OLAP 分析查询的需求，例如需查询: `书籍的评分，是否和评价的时间具有显著的相关性` 的需求，用以分析用户的书籍评分是否客观。那么会要求我们查询整个 `ratings` 表中的 `score` 和 `rated_at` 字段。这对普通仅支持的 OLTP 的数据库来说，是一个非常消耗资源的操作。或者使用一些 ETL 或其他数据同步工具，将 OLTP 数据库中的数据，导出到专用的 OLAP 数据库，再进行分析。

这种场景下，TiDB 就是一个比较理想的一站式数据库解决方案，TiDB 是一个 `HTAP (Hybrid Transactional and Analytical Processing)` 数据库，同时支持 OLTP 和 OLAP 场景。

#### 同步列存数据

当前，TiDB 支持两种数据分析引擎：`TiFlash` 和 `TiSpark`。大数据场景 (100 T) 下，推荐使用 TiFlash MPP 作为 HTAP 的主要方案，TiSpark 作为补充方案。希望了解更多关于 TiDB 的 HTAP 能力，可参考以下文章：[快速上手 HTAP](https://docs.pingcap.com/zh/tidb/stable/quick-start-with-htap) 和 [深入探索 HTAP](https://docs.pingcap.com/zh/tidb/stable/explore-htap)。

我们此处选用 [TiFlash](https://docs.pingcap.com/zh/tidb/stable/tiflash-overview) 为 `bookshop` 数据库的数据分析引擎。

TiFlash 部署完成后并不会自动同步数据，而需要手动指定需要同步的表，开启同步副本仅需一行 SQL，如下所示：

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

|      参数      |                  描述                  |
| :------------: | :------------------------------------: |
| `{table_name}` |                  表名                  |
|   `{count}`    | 同步副本数，若为 0，则表示删除同步副本 |

随后，TiFlash 将同步该表，查询时，TiDB 将会自动基于成本优化，考虑使用 `TiKV (行存)` 或 `TiFlash (列存)` 进行数据查询。当然，除了自动的方法，你也可以直接指定查询是否使用 TiFlash 副本，使用方法可查看[此处](https://docs.pingcap.com/zh/tidb/stable/use-tiflash#%E4%BD%BF%E7%94%A8-tidb-%E8%AF%BB%E5%8F%96-tiflash)。

#### 使用 HTAP 的示例

`ratings` 表开启 1 个 TiFlash 副本：

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> Note:
>
> 如果您的集群，不包含 TiFlash 节点，此 SQL 语句将会报错：`1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0` 你可以[使用 TiDB Cloud(DevTier) 构建 TiDB 集群](build-cluster-in-cloud.md#步骤1-创建免费集群) 来创建一个含有 TiFlash 的免费集群。

随后正常进行查询即可：

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

我们也可使用 [EXPLAIN ANALYZE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-explain-analyze) 语句查看此语句是否使用了 TiFlash 引擎：

```sql
EXPLAIN ANALYZE SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

```
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| id                          | estRows   | actRows | task         | access object | execution info                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                  | memory   | disk |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| Projection_4                | 299821.99 | 24      | root         |               | time:60.8ms, loops:6, Concurrency:5                                                                                                                                                                                                                                                                                                                                  | hour(cast(bookshop.ratings.rated_at, time))->Column#6, Column#5                                                                                | 17.7 KB  | N/A  |
| └─HashAgg_5                 | 299821.99 | 24      | root         |               | time:60.7ms, loops:6, partial_worker:{wall_time:60.660079ms, concurrency:5, task_num:293, tot_wait:262.536669ms, tot_exec:40.171833ms, tot_time:302.827753ms, max:60.636886ms, p95:60.636886ms}, final_worker:{wall_time:60.701437ms, concurrency:5, task_num:25, tot_wait:303.114278ms, tot_exec:176.564µs, tot_time:303.297475ms, max:60.69326ms, p95:60.69326ms}  | group by:Column#10, funcs:avg(Column#8)->Column#5, funcs:firstrow(Column#9)->bookshop.ratings.rated_at                                         | 714.0 KB | N/A  |
|   └─Projection_15           | 300000.00 | 300000  | root         |               | time:58.5ms, loops:294, Concurrency:5                                                                                                                                                                                                                                                                                                                                | cast(bookshop.ratings.score, decimal(8,4) BINARY)->Column#8, bookshop.ratings.rated_at, hour(cast(bookshop.ratings.rated_at, time))->Column#10 | 366.2 KB | N/A  |
|     └─TableReader_10        | 300000.00 | 300000  | root         |               | time:43.5ms, loops:294, cop_task: {num: 1, max: 43.1ms, proc_keys: 0, rpc_num: 1, rpc_time: 43ms, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                        | data:TableFullScan_9                                                                                                                           | 4.58 MB  | N/A  |
|       └─TableFullScan_9     | 300000.00 | 300000  | cop[tiflash] | table:ratings | tiflash_task:{time:5.98ms, loops:8, threads:1}                                                                                                                                                                                                                                                                                                                       | keep order:false                                                                                                                               | N/A      | N/A  |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
```

在出现 `cop[tiflash]` 字样时，表示该任务发送至 TiFlash 进行处理。

### 执行 `CREATE TABLE` 语句

我们定义完毕 `CREATE TABLE` 后，可以进行执行。

#### `CREATE TABLE` 执行的最佳实践

执行 `CREATE TABLE` 时需要遵循的一些最佳实践：

- 我们不推荐使用客户端的 Driver 或 ORM 来执行数据库模式的更改。以经验来看，作为最佳实践，我们建议使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)或使用任意你喜欢的 GUI 客户端来进行数据库模式的更改。本文档中，我们将在大多数场景下，使用 `MySQL 客户端` 传入 SQL 文件来执行数据库模式的更改。
- 遵循 SQL 开发规范中的[建表删表规范](sql-development-specification.md#1-建表删表规范)，建议业务应用内部封装建表删表语句增加判断逻辑。

#### `CREATE TABLE` 执行的示例

按以上步骤创建所有表后，我们的 `dbinit.sql` 文件应该类似于[此处](bookshop-schema-design.md#数据库初始化-dbinitsql-脚本)所示。若需查看表信息详解，请参阅[此处](bookshop-schema-design.md#数据表详解)。

我们可使用以下语句来执行 `dbinit.sql` 文件：

```sh
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < dbinit.sql
```

需查看 `bookshop` 数据库下的所有表，可使用 [SHOW TABLES](https://docs.pingcap.com/zh/tidb/stable/sql-statement-show-tables#show-full-tables) 语句：

```sql
SHOW TABLES IN `bookshop`;
```

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

请注意，到目前为止，我们所创建的所有表都不包含二级索引。添加二级索引的指南，请参考[创建二级索引](create-secondary-indexes.md)。

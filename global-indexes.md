---
title: 全局索引
summary: 介绍 TiDB 全局索引的适用场景、优势、使用方法、实现原理及其限制。全局索引突破了分区表唯一键必须包含分区列的限制，显著提升跨分区查询性能，简化数据迁移和应用开发。详细对比了全局索引与本地索引的适用场景，说明了全局索引的创建、管理方式及其对分区操作的影响，并通过性能测试数据展示了其在高并发和大规模分区场景下的性能优势。同时，介绍了全局索引的底层编码方式及与聚簇索引的关系，帮助你更好地理解和应用全局索引以优化分区表的查询和维护效率。
---

# 全局索引

在引入全局索引 (Global Index) 之前，TiDB 会为每个分区创建一个局部索引 (Local Index)，即一个分区对应一个局部索引。这种索引方式存在一个[使用限制](/partitioned-table.md#分区键主键和唯一键)：主键和唯一键必须包含所有的分区键，以确保数据的全局唯一性。此外，当查询的数据跨越多个分区时，TiDB 需要扫描各个分区的数据才能返回结果。

为解决这些问题，TiDB 从 v8.3.0 开始引入全局索引。全局索引能覆盖整个表的数据，使得主键和唯一键在不包含分区键的情况下仍能保持全局唯一性。此外，全局索引可以在一次操作中访问多个分区的索引数据，而无需对每个分区的局部索引逐一查找，显著提升了针对非分区键的查询性能。<!--从 v9.0.0 开始，非唯一索引也可以创建为全局索引。-->

## 全局索引和本地索引的适用场景

下图展示了本地索引和全局索引的区别。

<img src="https://github.com/hfxsd/docs-cn/blob/global-index-best-practices/media/global-index-vs-local-index.png" alt="Global Index vs. Local Index" width="60%" height="60%"/>

**全局索引的适用场景**：

- **数据归档不频繁**：例如，医疗行业的部分业务数据需要保存 30 年，通常按月分区，然后一次性创建 360 个分区，且很少进行 `DROP` 或 `TRUNCATE` 操作。在这种情况下，使用全局索引更为合适，能够提供跨分区的一致性和查询性能。
- **查询需要跨分区的数据**：当查询需要访问多个分区的数据时，全局索引可以避免跨分区扫描，提高查询效率。

**本地索引的适用场景**：

- **数据归档需求**：如果数据归档操作很频繁，且主要查询集中在单个分区内，本地索引可以提供更好的性能。
- **需要使用分区交换功能**：在银行等行业，可能会将处理后的数据先写入普通表，确认无误后再交换到分区表，以减少对分区表性能的影响。此时，本地索引更为适用，因为在使用了全局索引之后，分区表将不再支持分区交换功能。

## 全局索引的优势

### 提升查询性能

全局索引能够有效提高检索非分区列的效率。当查询涉及非分区列时，全局索引可以快速定位相关数据，避免了对所有分区的全表扫描，可以显著降低协处理任务 ( Coprocessor Task) 的数量，这对于分区数量庞大的场景尤为有效。

经过测试，在分区数量为 100 的情况下，sysbench `select_random_points` 场景的性能提升了 53 倍。

### 增强应用灵活性

全局索引的引入，消除了分区表上唯一键必须包含所有分区列的限制。这使得用户在设计索引时更加灵活，可以根据实际的查询需求和业务逻辑来创建索引，而不再受限于表的分区方案。这种灵活性有助于更好地优化查询性能，满足多样化的业务需求。

### 减少应用修改工作量

在数据迁移和应用修改过程中，全局索引可以减少对应用的修改工作量。如果没有全局索引，在迁移数据或修改应用时，可能需要调整分区方案，或者重写查询语句以适应索引的限制。有了全局索引之后，可以避免这些修改，从而降低开发和维护成本。

如在将 Oracle 数据库中的某张表迁移到 TiDB 时，因为 Oracle 支持全局索引，可能在某些表上存在一些不包含分区列的唯一索引，在迁移过程需要对表结构进行调整，以适应 TiDB 的分区表限制。然而，随着 TiDB 对全局索引的支持，你只需简单地修改索引定义，将其设置为全局索引，即可与 Oracle 保持一致，从而显著降低迁移成本。

## 全局索引的限制

- 如果索引定义中未显式指定 `GLOBAL` 关键字，TiDB 将默认创建局部索引 (Local Index)。
- `GLOBAL` 和 `LOCAL` 关键字仅适用于分区表，对非分区表没有影响。即在非分区表中，全局索引和局部索引之间没有区别。
- 以下 DDL 操作会触发全局索引的更新：`DROP PARTITION`、`TRUNCATE PARTITION` 和 `REORGANIZE PARTITION`。这些 DDL 需等待全局索引更新完成后才会返回结果，耗时会相应增加。尤其是在数据归档场景下，如 `DROP PARTITION` 和 `TRUNCATE PARTITION`，若没有全局索引，通常可以立即完成；但使用全局索引后，耗时会随着所需更新的索引数量的增加而增加。
- 包含全局索引的表不支持 `EXCHANGE PARTITION`。
- 默认情况下，分区表的主键为聚簇索引，且必须包含分区键。如果要求主键不包含分区建，可以在建表时显式指定主键为非聚簇的全局索引，例如：`PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL`。
- 如果在表达式列上添加了全局索引，或者一个全局索引同时也是前缀索引（如 `UNIQUE KEY idx_id_prefix (id(10)) GLOBAL`），你需要为该全局索引手动收集统计信息。

## 全局索引的发展历程

- **v7.6.0 版本之前**：TiDB 仅支持分区表的本地索引。这意味着，对于分区表上的唯一键，必须包含表分区表达式中的所有列。如果查询条件中没有使用分区键，那么查询将不得不扫描所有分区，这会导致查询性能下降。
- **v7.6.0 版本**：引入了系统变量 [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-从-v760-版本开始引入)，用于开启全局索引功能。然而，当时该功能仍在开发中，不推荐启用。
- **v8.3.0 版本**：全局索引功能作为实验性特性发布。你可以在创建索引时使用 `GLOBAL` 关键字来显式创建全局索引。
- **v8.4.0 版本**：全局索引功能正式成为一般可用（GA）特性。你可以直接使用 `GLOBAL` 关键字创建全局索引，而无需再设置系统变量 `tidb_enable_global_index`。从该版本开始，该系统变量被弃用，并且始终为 `ON`。
- **v8.5.0 版本**：全局索引功能支持包含分区表达式中的所有列。<!-- - **v9.0.0 版本**：全局索引功能支持非唯一索引的情况。在分区表中，除聚簇索引外都可以被创建为全局索引。-->

## 使用方法

如果你需要创建全局索引，可以通过在索引定义中添加 `GLOBAL` 关键字来实现。

> **注意：**
>
> 全局索引对分区管理有影响，执行 `DROP`、`TRUNCATE` 和 `REORGANIZE PARTITION` 操作也会触发表级别全局索引的更新，这意味着这些 DDL 操作只有在对应表的全局索引完全更新后才会返回结果。

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY uidx12(col1, col2) GLOBAL,
    UNIQUE KEY uidx3(col3),
    KEY idx1(col1) GLOBAL
)
PARTITION BY HASH(col3)
PARTITIONS 4;
```

在上面示例中，唯一索引 `uidx12` 和非唯一索引 `idx1` 将成为全局索引，但 `uidx3` 仍是常规的唯一索引。

请注意，**聚簇索引**不能成为全局索引，如下例所示：

```sql
CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    PRIMARY KEY (col2) CLUSTERED GLOBAL
) PARTITION BY HASH(col1) PARTITIONS 5;
```

```
ERROR 1503 (HY000): A CLUSTERED INDEX must include all columns in the table's partitioning function
```

聚簇索引不能成为全局索引，是因为如果聚簇索引是全局索引，则表将不再分区。这是因为聚簇索引的键是分区级别的行数据的键，但全局索引是表级别的，这就造成了冲突。如果需要将主键设置为全局索引，则需要显式设置该主键为非聚簇索引，如 `PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL`。

你可以通过 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 输出中的 `GLOBAL` 索引选项来识别全局索引。

```sql
SHOW CREATE TABLE t1\G
```

```
       Table: t1
Create Table: CREATE TABLE `t1` (
  `col1` int NOT NULL,
  `col2` date NOT NULL,
  `col3` int NOT NULL,
  `col4` int NOT NULL,
  UNIQUE KEY `uidx12` (`col1`,`col2`) /*T![global_index] GLOBAL */,
  UNIQUE KEY `uidx3` (`col3`),
  KEY `idx1` (`col1`) /*T![global_index] GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY HASH (`col3`) PARTITIONS 4
1 row in set (0.00 sec)
```

或查询 [`INFORMATION_SCHEMA.TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md) 表并查看输出中的 `IS_GLOBAL` 列来识别全局索引。

```sql
SELECT * FROM information_schema.tidb_indexes WHERE table_name='t1';
```

```
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
| TABLE_SCHEMA | TABLE_NAME | NON_UNIQUE | KEY_NAME | SEQ_IN_INDEX | COLUMN_NAME | SUB_PART | INDEX_COMMENT | Expression | INDEX_ID | IS_VISIBLE | CLUSTERED | IS_GLOBAL |
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
| test         | t1         |          0 | uidx12   |            1 | col1        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
| test         | t1         |          0 | uidx12   |            2 | col2        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
| test         | t1         |          0 | uidx3    |            1 | col3        |     NULL |               | NULL       |        2 | YES        | NO        |         0 |
| test         | t1         |          1 | idx1     |            1 | col1        |     NULL |               | NULL       |        3 | YES        | NO        |         1 |
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
3 rows in set (0.00 sec)
```

在对普通表进行分区或者对分区表进行重新分区时，可以根据需要将索引更新为全局索引或局部索引。

例如，下面的 SQL 语句会基于 `col1` 列对表 `t1` 进行重新分区，并将该表中的全局索引 `uidx12` 和 `idx1` 更新为局部索引，将局部索引 `uidx3` 更新为全局索引。`uidx3` 是基于 `col3` 列的唯一索引，为了保证 `col3` 在所有分区中的唯一性，`uidx3` 必须为全局索引；`uidx12` 和 `idx1` 是基于 `col1` 列的索引，因此可以是全局索引或局部索引。

```sql
ALTER TABLE t1 PARTITION BY HASH (col1) PARTITIONS 3 UPDATE INDEXES (uidx12 LOCAL, uidx3 GLOBAL, idx1 LOCAL);
```

## 全局索引的工作原理

### 基本思想

在 TiDB 的分区表中，本地索引的键值前缀是分区表的 ID，而全局索引的前缀是表的 ID。这样的改进能够确保全局索引的数据在 TiKV 上分布是连续的，降低了查询索引时 RPC 的数量。

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  KEY idx(k),
  KEY global_idx(k) GLOBAL
) partition by hash(id) partitions 5;
```

以上面的表结构为例，`idx` 为普通索引，`global_idx` 为全局索引。索引 `idx` 的数据会分布在 5 个不同的 Range 中，如 `PartitionID1_i_xxx`、`PartitionID2_i_xxx` 等，而索引 `global_idx` 的数据则会集中在一个 Range (`TableID_i_xxx`) 内。

当进行与 `k` 相关的查询时，如 `SELECT * FROM sbtest WHERE k > 1`，通过索引 `idx` 会构造 5 个不同的 Range，而通过全局索引 `global_idx` 则只会构造 1 个 Range，每个 Range 在 TiDB 中对应一个或多个 RPC 请求，这样使用全局索引可以降低数倍的 RPC 请求数，从而提升查询索引的性能。

下图直观地展示了在使用 `idx` 和 `global_idx` 两个不同索引执行 `SELECT * FROM sbtest WHERE k > 1` 查询语句在 RPC 请求和数据流转过程中的差异。

![Mechanism of Global Indexes](/media/global-index-mechanism.png)

### 编码方式

在 TiDB 中，索引项被编码为键值对。对于分区表，每个分区在 TiKV 层被视为一个独立的物理表，拥有自己的 `partitionID`。因此，分区表的索引项也被编码为：

```
唯一键
Key:
- PartitionID_indexID_ColumnValues

Value:
- IntHandle
 - TailLen_IntHandle

- CommonHandle
 - TailLen_IndexVersion_CommonHandle

非唯一键
Key:
- PartitionID_indexID_ColumnValues_Handle

Value:
- IntHandle
 - TailLen_Padding

- CommonHandle
 - TailLen_IndexVersion
```

在全局索引中，索引项的编码方式有所不同。为了使全局索引的键布局与当前索引键编码保持兼容，新的索引编码布局为：

```
唯一键
Key:
- TableID_indexID_ColumnValues

Value:
- IntHandle
 - TailLen_PartitionID_IntHandle

- CommonHandle
 - TailLen_IndexVersion_CommonHandle_PartitionID

非唯一键
Key:
- TableID_indexID_ColumnValues_Handle

Value:
- IntHandle
 - TailLen_PartitionID

- CommonHandle
 - TailLen_IndexVersion_PartitionID
```

这种编码方式使得全局索引的键以 `TableID` 开头，而 `PartitionID` 被放置在 Value 中。这样设计的优点是，它与现有的索引键编码方式兼容，但同时也带来了一些挑战，例如，在执行 `DROP PARTITION`、`TRUNCATE PARTITION` 等 DDL 操作时，由于索引项不连续，需要进行额外的处理。

## 性能测试数据

以下测试基于 sysbench 的 `select_random_points` 场景，主要用于对比不同分区策略与索引方式下的查询性能。测试表结构和配置如下：

示例表结构如下：

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  KEY `k_1` (`k`)
  /* Key `k_1` (`k`, `c`) GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
/* Partition by hash(`id`) partitions 100 */
/* Partition by range(`id`) xxxx */
```

负载 SQL 如下：

```sql
SELECT id, k, c, pad
FROM sbtest1
WHERE k IN (xx, xx, xx)
```

Range Partition (100 partitions)

| Table type                                                            | Concurrency 1 | Concurrency 32 | Concurrency 64 | Average RU |
| --------------------------------------------------------------------- | ------------- | -------------- | -------------- | ---------- |
| Clustered non-partitioned table                                       | 225           | 19,999         | 30,293         | 7.92       |
| Clustered table range partitioned by PK                               | 68            | 480            | 511            | 114.87     |
| Clustered table range partitioned by PK, with Global Index on `k`,`c` | 207           | 17,798         | 27,707         | 11.73      |

Hash Partition (100 partitions)

| Table type                                                           | Concurrency 1 | Concurrency 32 | Concurrency 64 | Average RU |
| -------------------------------------------------------------------- | ------------- | -------------- | -------------- | ---------- |
| Clustered non-partitioned table                                      | 166           | 20,361         | 28,922         | 7.86       |
| Clustered table hash partitioned by PK                               | 60            | 244            | 283            | 119.73     |
| Clustered table hash partitioned by PK, with Global Index on `k`,`c` | 156           | 18,233         | 15,581         | 10.77      |

通过上述测试可以看出，在高并发环境下，全局索引能够显著提升分区表查询性能，提升幅度可达 50 倍。同时，全局索引还能够显著降低资源（RU）消耗。随着分区数量的增加，这种性能提升的效果将愈加明显。

## 全局索引和聚簇索引

由于聚簇索引和全局索引的原理限制，一个索引不能同时作为聚簇索引和全局索引。然而，这两种索引在不同查询场景中能提供不同的性能优化。在遇到需要同时兼顾两者的需求时，你可以将分区列添加到聚簇索引中，同时创建一个不包含分区列的全局索引。

假设有如下表结构：

```sql
CREATE TABLE `t` (
  `id` int DEFAULT NULL,
  `ts` timestamp NULL DEFAULT NULL,
  `data` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (UNIX_TIMESTAMP(`ts`))
(PARTITION `p0` VALUES LESS THAN (1735660800)
 PARTITION `p1` VALUES LESS THAN (1738339200)
 ...)
```

在上面的 `t` 表中，`id` 列的值是唯一的。为了优化点查和范围查询的性能，可以选择在建表语句中定义一个聚簇索引 `PRIMARY KEY(id, ts)` 和一个不包含分区列的全局索引 `UNIQUE KEY id(id)`。这样在进行基于 `id` 的点查询时，会采用全局索引 `id`，选择 `PointGet` 的执行计划；而在进行范围查询时，聚簇索引则会被选中，因为聚簇索引相比全局索引少了一次回表操作，从而提升查询效率。

修改后的表结构如下所示：

```sql
CREATE TABLE `t` (
  `id` int NOT NULL,
  `ts` timestamp NOT NULL,
  `data` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`, `ts`) /*T![clustered_index] CLUSTERED */,
  UNIQUE KEY `id` (`id`) /*T![global_index] GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (UNIX_TIMESTAMP(`ts`))
(PARTITION `p0` VALUES LESS THAN (1735660800),
 PARTITION `p1` VALUES LESS THAN (1738339200)
 ...)
```

这种方式既能优化基于 `id` 的点查询，又能提升范围查询的性能，同时确保表的分区列在基于时间戳的查询中能得到有效的利用。

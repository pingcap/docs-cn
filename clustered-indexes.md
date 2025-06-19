---
title: 聚簇索引
summary: 了解聚簇索引的概念、使用场景、用法、限制和兼容性。
---

# 聚簇索引

TiDB 从 v5.0 开始支持聚簇索引功能。此功能控制包含主键的表中数据的存储方式。它使 TiDB 能够以一种可以提高某些查询性能的方式组织表。

这里的 _聚簇_ 指的是 _数据存储的组织方式_，而不是 _一组协同工作的数据库服务器_。某些数据库管理系统将聚簇索引表称为 _索引组织表_ (IOT)。

目前，TiDB 中包含主键的表分为以下两类：

- `NONCLUSTERED`：表的主键是非聚簇索引。在具有非聚簇索引的表中，行数据的键由 TiDB 隐式分配的内部 `_tidb_rowid` 组成。由于主键本质上是唯一索引，具有非聚簇索引的表需要至少两个键值对来存储一行数据，即：
    - `_tidb_rowid`（键）- 行数据（值）
    - 主键数据（键）- `_tidb_rowid`（值）
- `CLUSTERED`：表的主键是聚簇索引。在具有聚簇索引的表中，行数据的键由用户提供的主键数据组成。因此，具有聚簇索引的表只需要一个键值对来存储一行数据，即：
    - 主键数据（键）- 行数据（值）

> **注意：**
>
> TiDB 仅支持通过表的 `PRIMARY KEY` 进行聚簇。启用聚簇索引后，_`PRIMARY KEY`_ 和 _聚簇索引_ 这两个术语可能会互换使用。`PRIMARY KEY` 指的是约束（逻辑属性），而聚簇索引描述了数据存储的物理实现方式。

## 使用场景

与具有非聚簇索引的表相比，具有聚簇索引的表在以下场景中具有更大的性能和吞吐量优势：

+ 当插入数据时，聚簇索引减少了一次网络写入索引数据的操作。
+ 当查询只涉及主键的等值条件时，聚簇索引减少了一次网络读取索引数据的操作。
+ 当查询只涉及主键的范围条件时，聚簇索引减少了多次网络读取索引数据的操作。
+ 当查询只涉及主键前缀的等值或范围条件时，聚簇索引减少了多次网络读取索引数据的操作。

另一方面，具有聚簇索引的表也有一些缺点。请参见以下内容：

- 当插入大量值相近的主键时，可能会出现写入热点问题。
- 如果主键的数据类型大于 64 位，表数据会占用更多存储空间，特别是当存在多个二级索引时。

## 用法

### 创建具有聚簇索引的表

从 TiDB v5.0 开始，你可以在 `CREATE TABLE` 语句中的 `PRIMARY KEY` 后添加非保留关键字 `CLUSTERED` 或 `NONCLUSTERED` 来指定表的主键是否为聚簇索引。例如：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) CLUSTERED);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) NONCLUSTERED);
```

注意，在列定义中，关键字 `KEY` 和 `PRIMARY KEY` 具有相同的含义。

你也可以使用 TiDB 中的[注释语法](/comment-syntax.md)来指定主键的类型。例如：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] CLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] NONCLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] CLUSTERED */);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] NONCLUSTERED */);
```

对于未明确指定关键字 `CLUSTERED`/`NONCLUSTERED` 的语句，默认行为由系统变量 [`@@global.tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50) 控制。该变量支持的值如下：

- `OFF` 表示默认将主键创建为非聚簇索引。
- `ON` 表示默认将主键创建为聚簇索引。
- `INT_ONLY` 表示行为由配置项 `alter-primary-key` 控制。如果 `alter-primary-key` 设置为 `true`，则默认将主键创建为非聚簇索引。如果设置为 `false`，则仅将由整数列组成的主键创建为聚簇索引。

`@@global.tidb_enable_clustered_index` 的默认值为 `ON`。

### 添加或删除聚簇索引

TiDB 不支持在表创建后添加或删除聚簇索引。也不支持聚簇索引和非聚簇索引之间的相互转换。例如：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) CLUSTERED; -- 当前不支持。
ALTER TABLE t DROP PRIMARY KEY;     -- 如果主键是聚簇索引，则不支持。
ALTER TABLE t DROP INDEX `PRIMARY`; -- 如果主键是聚簇索引，则不支持。
```

### 添加或删除非聚簇索引

TiDB 支持在表创建后添加或删除非聚簇索引。你可以显式指定关键字 `NONCLUSTERED` 或省略它。例如：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) NONCLUSTERED;
ALTER TABLE t ADD PRIMARY KEY(b, a); -- 如果省略关键字，主键默认为非聚簇索引。
ALTER TABLE t DROP PRIMARY KEY;
ALTER TABLE t DROP INDEX `PRIMARY`;
```

### 检查主键是否为聚簇索引

你可以使用以下方法之一来检查表的主键是否为聚簇索引：

- 执行 `SHOW CREATE TABLE` 命令。
- 执行 `SHOW INDEX FROM` 命令。
- 查询系统表 `information_schema.tables` 中的 `TIDB_PK_TYPE` 列。

通过运行 `SHOW CREATE TABLE` 命令，你可以看到 `PRIMARY KEY` 的属性是 `CLUSTERED` 还是 `NONCLUSTERED`。例如：

```sql
mysql> SHOW CREATE TABLE t;
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                      |
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` bigint(20) NOT NULL,
  `b` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

通过运行 `SHOW INDEX FROM` 命令，你可以检查结果中 `Clustered` 列是否显示 `YES` 或 `NO`。例如：

```sql
mysql> SHOW INDEX FROM t;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| t     |          0 | PRIMARY  |            1 | a           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
1 row in set (0.01 sec)
```

你也可以查询系统表 `information_schema.tables` 中的 `TIDB_PK_TYPE` 列，看结果是 `CLUSTERED` 还是 `NONCLUSTERED`。例如：

```sql
mysql> SELECT TIDB_PK_TYPE FROM information_schema.tables WHERE table_schema = 'test' AND table_name = 't';
+--------------+
| TIDB_PK_TYPE |
+--------------+
| CLUSTERED    |
+--------------+
1 row in set (0.03 sec)
```

## 限制

目前，聚簇索引功能有几种不同类型的限制。请参见以下内容：

- 不支持且不在支持计划中的情况：
    - 不支持将聚簇索引与属性 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 一起使用。此外，属性 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 对非 [`AUTO_RANDOM`](/auto-random.md) 的聚簇索引表不生效。
    - 不支持降级具有聚簇索引的表。如果需要降级此类表，请使用逻辑备份工具迁移数据。
- 目前不支持但在支持计划中的情况：
    - 不支持使用 `ALTER TABLE` 语句添加、删除和修改聚簇索引。
- 特定版本的限制：    
    - 在 v5.0 中，不支持将聚簇索引功能与 TiDB Binlog 一起使用。启用 TiDB Binlog 后，TiDB 仅允许创建单个整数列作为主键的聚簇索引。TiDB Binlog 不会将现有聚簇索引表上的数据变更（如插入、删除和更新）复制到下游。如果需要将具有聚簇索引的表复制到下游，请将集群升级到 v5.1 或使用 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) 进行复制。

启用 TiDB Binlog 后，如果创建的聚簇索引不是单个整数主键，TiDB 会返回以下错误：

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED);
ERROR 8200 (HY000): Cannot create clustered index table when the binlog is ON
```

如果将聚簇索引与属性 `SHARD_ROW_ID_BITS` 一起使用，TiDB 会报告以下错误：

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED) SHARD_ROW_ID_BITS = 3;
ERROR 8200 (HY000): Unsupported shard_row_id_bits for table with primary key as row id
```

## 兼容性

### 与早期和后期 TiDB 版本的兼容性

TiDB 支持升级具有聚簇索引的表，但不支持降级此类表，这意味着后期 TiDB 版本中具有聚簇索引的表中的数据在早期版本中不可用。

TiDB v3.0 和 v4.0 部分支持聚簇索引功能。当完全满足以下要求时，该功能默认启用：

- 表包含 `PRIMARY KEY`。
- `PRIMARY KEY` 仅由一个列组成。
- `PRIMARY KEY` 是 `INTEGER` 类型。

从 TiDB v5.0 开始，聚簇索引功能完全支持所有类型的主键，但默认行为与 TiDB v3.0 和 v4.0 一致。要更改默认行为，你可以将系统变量 `@@tidb_enable_clustered_index` 配置为 `ON` 或 `OFF`。更多详情，请参见[创建具有聚簇索引的表](#创建具有聚簇索引的表)。

### 与 MySQL 的兼容性

TiDB 特定的注释语法支持将关键字 `CLUSTERED` 和 `NONCLUSTERED` 包装在注释中。`SHOW CREATE TABLE` 的结果也包含 TiDB 特定的 SQL 注释。MySQL 数据库和早期版本的 TiDB 数据库会忽略这些注释。

### 与 TiDB 迁移工具的兼容性

聚簇索引功能仅与 v5.0 及更高版本的以下迁移工具兼容：

- 备份和恢复工具：BR、Dumpling 和 TiDB Lightning。
- 数据迁移和复制工具：DM 和 TiCDC。

但是，你不能通过使用 v5.0 BR 工具备份和恢复表来将具有非聚簇索引的表转换为具有聚簇索引的表，反之亦然。

### 与其他 TiDB 功能的兼容性

对于具有组合主键或单个非整数主键的表，如果将主键从非聚簇索引更改为聚簇索引，其行数据的键也会改变。因此，在 TiDB v5.0 之前版本中可执行的 `SPLIT TABLE BY/BETWEEN` 语句在 v5.0 及更高版本的 TiDB 中不再适用。如果要使用 `SPLIT TABLE BY/BETWEEN` 拆分具有聚簇索引的表，需要提供主键列的值，而不是指定整数值。请参见以下示例：

```sql
mysql> create table t (a int, b varchar(255), primary key(a, b) clustered);
Query OK, 0 rows affected (0.01 sec)
mysql> split table t between (0) and (1000000) regions 5;
ERROR 1105 (HY000): Split table region lower value count should be 2
mysql> split table t by (0), (50000), (100000);
ERROR 1136 (21S01): Column count doesn't match value count at row 0
mysql> split table t between (0, 'aaa') and (1000000, 'zzz') regions 5;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
|                  4 |                    1 |
+--------------------+----------------------+
1 row in set (0.00 sec)
mysql> split table t by (0, ''), (50000, ''), (100000, '');
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
|                  3 |                    1 |
+--------------------+----------------------+
1 row in set (0.01 sec)
```

属性 [`AUTO_RANDOM`](/auto-random.md) 只能用于聚簇索引。否则，TiDB 会返回以下错误：

```sql
mysql> create table t (a bigint primary key nonclustered auto_random);
ERROR 8216 (HY000): Invalid auto random: column a is not the integer primary key, or the primary key is nonclustered
```

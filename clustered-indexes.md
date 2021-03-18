---
title: 聚簇索引
summary: 本文档介绍了聚簇索引的概念、使用场景、使用方法、限制和兼容性。
---

# 聚簇索引

聚簇索引是 TiDB 从 v5.0-rc 开始支持的特性，用于控制含有主键的表数据的存储方式。通过使用聚簇索引，TiDB 可以更好地组织数据表，从而提高某些查询的性能。有些数据库管理系统也将聚簇索引称为“索引组织表” (index-organized tables)。

目前 TiDB 所有含有主键的表分为两类，分别是：

- `NONCLUSTERED`，表示该表的主键为非聚簇索引。在非聚簇索引表中，行数据的键由 TiDB 内部隐式分配的 `_tidb_rowid` 构成，而主键本质上是唯一索引，因此非聚簇索引表存储一行至少需要两个键值对，分别为
    - `_tidb_rowid` -> row data
    - primary key columns data -> `_tidb_rowid`
- `CLUSTERED`，表示该表的主键为聚簇索引。在聚簇索引表中，行数据的键由用户给定的主键列数据构成，不存在唯一索引，因此聚簇索引表存储一行至少只要一个键值对，即
    - primary key columns data -> row data

请再次注意，TiDB 仅支持根据表的主键来进行聚簇操作。聚簇索引启用时，主键和聚簇索引两个术语在一些情况下可互换使用。主键指的是约束（一种逻辑属性），而聚簇索引描述的是数据存储的物理实现。

## 使用场景

相较于非聚簇索引表，聚簇索引表在以下几个场景中，性能和吞吐量都有较大优势：

- 插入数据时会减少一次从网络写入索引数据。
- 等值条件查询仅涉及主键时会减少一次从网络读取数据。
- 范围条件查询仅涉及主键时会减少多次从网络读取数据。
- 等值或范围条件查询仅涉及主键的前缀时会减少多次从网络读取数据。

另一方面，聚簇索引表也存在一定的劣势：

- 批量插入大量取值相邻的主键时，可能会产生较大的写热点问题。
- 当使用大于 64 位的数据类型作为主键时，可能导致表本身需要占用更多的存储空间。该现象在存在多个二级索引时尤为明显。

## 使用方法

### 创建聚簇索引表

从 TiDB 版本 5.0 开始，要指定一个表的主键是否使用聚簇索引，可以在 `CREATE TABLE` 语句中将 `CLUSTERED` 或者 `NONCLUSTERED` 非保留关键字标注在 `PRIMARY KEY` 后面，例如：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) CLUSTERED);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) NONCLUSTERED);
```

注意在列定义中的 `KEY` 和 `PRIMARY KEY` 含义相同。

此外，TiDB 支持[可执行的注释语法](/comment-syntax.md)：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] CLUSTERED */, b VARCHAR(255)); 
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] NONCLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] CLUSTERED */,);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] NONCLUSTERED */); 
```

### 添加、删除聚簇索引

目前 TiDB 不支持在建表之后添加或删除聚簇索引，也不支持聚簇索引和非聚簇索引的互相转换。例如：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) CLUSTERED; -- 暂不支持
ALTER TABLE t DROP PRIMARY KEY;     -- 如果主键为聚簇索引，则不支持
ALTER TABLE t DROP INDEX `PRIMARY`; -- 如果主键为聚簇索引，则不支持
```

### 添加、删除非聚簇索引

TiDB 支持在建表之后添加或删除非聚簇索引。此时可以选择显式指定 `NONCLUSTERED` 关键字或省略关键字：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) NONCLUSTERED;
ALTER TABLE t ADD PRIMARY KEY(b, a); -- 不指定关键字，则为非聚簇索引
ALTER TABLE t DROP PRIMARY KEY;
ALTER TABLE t DROP INDEX `PRIMARY`;
```

### 查询主键是否为聚簇索引

要确定一张表的主键是否使用了聚簇索引，TiDB 提供了三种方式：

- `SHOW CREATE TABLE`
- `SHOW INDEX FROM`
- `information_schema.tables`

通过 `SHOW CREATE TABLE` 查看，`PRIMARY KEY` 的属性可能为 `CLUSTERED` 或 `NONCLUSTERED`：

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

通过 `SHOW INDEX FROM` 查看，`Clustered` 一列可能的结果为 `Yes` 或 `No`：

```sql
mysql> SHOW INDEX FROM t;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| t     |          0 | PRIMARY  |            1 | a           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
1 row in set (0.01 sec)
```

查询 `information_schema.tables` 系统表中的 `TIDB_PK_TYPE` 列，可能的结果为 `CLUSTERED` 或 `NONCLUSTERED`：

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

目前 TiDB 的聚簇索引具有两类限制。一类是明确不支持且没有支持计划的使用限制: 

- 不支持与 TiDB Binlog 一起使用。开启 Binlog 后 TiDB 不允许创建非单个整数列作为主键的聚簇索引；已创建的聚簇索引表的数据插入、删除和更新动作不会通过 Binlog 同步到下游。如需同步聚簇索引表，请使用 [TiCDC](/ticdc/ticdc-overview.md)。
- 不支持与 `SHARD_ROW_ID_BITS` 一起使用。
- 不支持对聚簇索引表进行降级。如需降级，请使用逻辑备份工具迁移数据。

开启 Binlog 之后，创建非单个整数列作为主键的聚簇索引会报以下错误：

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED);
ERROR 8200 (HY000): Cannot create clustered index table when the binlog is ON
```

与 `SHARD_ROW_ID_BITS` 一起使用时会报以下错误：

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED) SHARD_ROW_ID_BITS = 3;
ERROR 8200 (HY000): Unsupported shard_row_id_bits for table with primary key as row id
```

另一类是尚未支持，但未来有计划支持的使用限制：

- 尚未支持通过 `ALTER TABLE` 语句增加、删除、修改聚簇索引。
- 在 v5.0-rc 中，如果 `alter-primary-key = true`，无法新建聚簇索引表。从 v5.0 开始，`alter-primary-key` 选项被移除，该限制已被解除。

## 兼容性

### 升降级兼容性

TiDB 支持对聚簇索引表的升级兼容，但不支持降级兼容，即高版本 TiDB 聚簇索引表的数据在低版本 TiDB 上不可用。

聚簇索引在 TiDB v3.0 和 v4.0 中已完成部分支持，当表中存在单个整数列作为主键时默认启用，即：

- 表设置了主键
- 主键只有一列
- 主键的数据类型为整数类型

在 TiDB v5.0-rc 中，支持非整数列主键以及任意类型复合主键的聚簇索引，默认行为通过全局变量和 session 变量 `@@tidb_enable_clustered_index` 来控制。而单整数列主键仍然为默认启用聚簇索引。

而从 TiDB v5.0 开始，不论是单整数列主键还是其他类型主键，默认均为非聚簇索引。该行为变更可能导致默认配置下的 TiDB 在某些场景中出现性能回退，此时可以考虑显式启用聚簇索引。

### MySQL 兼容性

TiDB 支持使用可执行注释的语法来包裹 `CLUSTERED` 或 `NONCLUSTERED` 关键字，且 `SHOW CREATE TABLE` 的结果均包含 TiDB 特有的可执行注释，因此这部分 DDL 语句能被 MySQL 或低版本的 TiDB 识别并执行。

### TiDB 生态工具兼容性

聚簇索引仅与 v5.0 及以后版本的以下生态工具兼容：

- 备份与恢复工具 BR、Dumpling、Lightning。
- 数据迁移和同步工具 DM、TiCDC。

v5.0 的 BR 不能通过备份恢复将非聚簇索引表转换成聚簇索引表，反之亦然。

### 与 TiDB 其他特性的兼容性

在非单整数列作为主键的表中，从非聚簇索引变为聚簇索引之后，在 v5.0-rc 之前版本的 TiDB 能够执行的 `SPLIT TABLE BY/BETWEEN` 语句在 v5.0-rc 及以后版本的 TiDB 上不再可用，原因是行数据键的构成发生了变化。在聚簇索引表上执行 `SPLIT TABLE BY/BETWEEN` 时需要依据主键列指定值，而不是指定一个整数值。例如：

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

---
title: 使用 FastScan 功能
summary: 介绍通过使用 FastScan 来加速 OLAP 场景的查询的方法。
aliases: ['/zh/tidb/dev/sql-statement-set-tiflash-mode/','/zh/tidb/dev/dev-guide-use-fastscan/']
---

# 使用 FastScan 功能

本文档介绍通过使用 FastScan 来加速 Online Analytical Processing (OLAP) 场景中查询的方法。

默认情况下，TiFlash 能够保证查询结果精度以及数据一致性。如果使用 FastScan，TiFlash 可以实现更高效的查询性能，但不保证查询结果精度和数据一致性。

某些 OLAP 对查询结果精度可以容忍一定误差。如果对查询性能有更高要求，可以在 session 级别或 global 级别开启 FastScan 功能，你可以通过修改变量 [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-从-v630-版本开始引入) 的值来选择是否启用 FastScan 功能。

## 使用限制

当开启 FastScan 功能时，查询结果可能会包含表中的旧数据，即相同主键的多个历史版本的数据或者已经删除的数据。如下所示：

```sql
CREATE TABLE t1 (a INT PRIMARY KEY, b INT);
ALTER TABLE t1 SET TIFLASH REPLICA 1;
INSERT INTO t1 VALUES(1,2);
INSERT INTO t1 VALUES(10,20);
UPDATE t1 SET b = 4 WHERE a = 1;
DELETE FROM t1 WHERE a = 10;
SET SESSION tidb_isolation_read_engines='tiflash';

SELECT * FROM t1;
+------+------+
| a    | b    |
+------+------+
|    1 |    4 |
+------+------+

SET SESSION tiflash_fastscan=ON;
SELECT * FROM t1;
+------+------+
| a    | b    |
+------+------+
|    1 |    2 |
|    1 |    4 |
|   10 |   20 |
+------+------+
```

对于这些旧数据，TiFlash 在后台会自动发起数据整理（Compaction）。当这些旧数据已经被后台整理且它们的数据版本小于 GC safe point 之后，才会被物理清理。此后在 FastScan 模式下将不再返回这些数据。旧数据被整理的时机受多种因素的自动触发，你也可以通过 [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) 手动触发数据整理。 

## 启用和禁用 FastScan

默认情况下，session 和 global 级别的变量 `tiflash_fastscan=OFF`，即没有开启 FastScan 功能。你可以通过以下语句来查看对应的变量信息。

```
show variables like 'tiflash_fastscan';
```

```
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

```
show global variables like 'tiflash_fastscan';
```

```
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

变量 `tiflash_fastscan` 支持 session 级别和 global 级别的修改。如果需要在当前 session 中启用 FastScan 功能，可以通过以下语句设置:

```
set session tiflash_fastscan=ON;
```

如果对 global 级别的 `tiflash_fastscan` 进行设置，设置后新建的会话中默认 session 和 global 变量 `tiflash_fastscan` 启用新值。设置方式如下：

```
set global tiflash_fastscan=ON;
```

可以用下面语句禁用 FastScan：

```sql
set session tiflash_fastscan=OFF;
set global tiflash_fastscan=OFF;
```

## 实现机制

TiFlash 存储层的数据主要存放在 Delta 层和 Stable 层。

在默认状态下（即未开启 FastScan 功能），TableScan 算子过程整体包括了以下步骤：

1. Read data：在 Delta 层和 Stable 层分别建立数据流，进行各自数据的读取。
2. Sort Merge：将步骤 1 中建立的数据流进行合并，并且将数据按照 (主键列，时间戳列) 顺序排列返回。
3. Range Filter：根据读取范围限制，对步骤 2 中的数据进行过滤筛选并返回。
4. MVCC + Column Filter：对步骤 3 中的数据进行 MVCC 过滤（即依照查询需要的数据版本，根据主键列以及时间戳列筛选出正确的数据版本），同时进行 Column 过滤（即过滤掉查询请求中不需要的列）并返回。

FastScan 通过损失一定的数据一致性来获取更快的查询性能。FastScan 中的 TableScan 流程省略了上述过程中的第 2 步和第 4 步中 MVCC 的部分，从而提高查询性能。

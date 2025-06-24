---
title: 使用 FastScan
summary: 介绍如何使用 FastScan 在 OLAP 场景下加速查询。
---

# 使用 FastScan

本文档介绍如何使用 FastScan 在在线分析处理（OLAP）场景中加速查询。

默认情况下，TiFlash 保证查询结果的精确性和数据一致性。通过 FastScan 功能，TiFlash 可以提供更高效的查询性能，但不保证查询结果的准确性和数据一致性。

某些 OLAP 场景允许查询结果有一定的容错性。在这些情况下，如果你需要更高的查询性能，可以在会话级别或全局级别启用 FastScan 功能。你可以通过配置变量 `tiflash_fastscan` 来选择是否启用 FastScan 功能。

## 限制

当启用 FastScan 功能时，你的查询结果可能包含表的旧数据。这意味着你可能会获得具有相同主键的多个历史版本数据或已被删除的数据。

例如：

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

虽然 TiFlash 可以在后台自动触发旧数据的压缩，但在数据被压缩且其数据版本早于 GC 安全点之前，旧数据不会被物理清理。在物理清理之后，被清理的旧数据将不再在 FastScan 模式下返回。数据压缩的时机由各种因素自动触发。你也可以使用 [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) 语句手动触发数据压缩。

## 启用和禁用 FastScan

默认情况下，变量 `tiflash_fastscan=OFF` 在会话级别和全局级别都是关闭的，即 FastScan 功能未启用。你可以使用以下语句查看变量信息。

```
show variables like 'tiflash_fastscan';

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

```
show global variables like 'tiflash_fastscan';

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

你可以在会话级别和全局级别配置变量 `tiflash_fastscan`。如果你需要在当前会话中启用 FastScan，可以使用以下语句：

```
set session tiflash_fastscan=ON;
```

你也可以在全局级别设置 `tiflash_fastscan`。新设置将在新会话中生效，但不会在当前和之前的会话中生效。此外，在新会话中，会话级别和全局级别的 `tiflash_fastscan` 都将采用新值。

```
set global tiflash_fastscan=ON;
```

你可以使用以下语句禁用 FastScan。

```
set session tiflash_fastscan=OFF;
set global tiflash_fastscan=OFF;
```

## FastScan 的工作机制

TiFlash 存储层的数据存储在两个层次：Delta 层和 Stable 层。

默认情况下，FastScan 未启用，TableScan 算子按以下步骤处理数据：

1. 读取数据：在 Delta 层和 Stable 层分别创建数据流来读取各自的数据。
2. 排序合并：合并步骤 1 中创建的数据流。然后按照（主键列，时间戳列）的顺序排序后返回数据。
3. 范围过滤：根据数据范围，过滤步骤 2 生成的数据，然后返回数据。
4. MVCC + 列过滤：通过 MVCC（即根据主键列和时间戳列过滤数据版本）和列过滤（即过滤掉不需要的列）对步骤 3 生成的数据进行过滤，然后返回数据。

FastScan 通过牺牲一些数据一致性来获得更快的查询速度。在 FastScan 中，正常扫描过程中的步骤 2 和步骤 4 中的 MVCC 部分被省略，从而提高查询性能。

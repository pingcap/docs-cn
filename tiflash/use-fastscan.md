---
title: 使用 FastScan 功能
summary: 介绍通过使用 FastScan 来加速 OLAP 场景的查询的方法。
aliases: ['/zh/tidb/dev/sql-statement-set-tiflash-mode/','/zh/tidb/dev/dev-guide-use-fastscan/']
---

# 使用 FastScan 功能

本文档介绍通过使用 FastScan 来加速 Online Analytical Processing (OLAP) 场景中查询的方法。

默认情况下，TiFlash 能够保证查询结果精度以及数据一致性。如果使用 FastScan，TiFlash 可以实现更高效的查询性能，但不保证查询结果精度和数据一致性。

某些 OLAP 对查询结果精度可以容忍一定误差。如果对查询性能有更高要求，可以在 session 级别或 global 级别开启 FastScan 功能，你可以通过修改变量 `tiflash_fastscan` 的值来选择是否启用 FastScan 功能。

> **警告：**
> 当开启 FastScan 功能时，查询结果会包含相同主键的多个版本的数据，或者已经被删除的数据。如下所示：

> 
```
create table t1 (a int primary key, b int);
alter table t1 set tiflash replica 1;
insert into t1 values(1,2);
insert into t1 values(10,20);
update t1 set b = 4 where a = 1;
delete from t1 where a = 10;
set session tidb_isolation_read_engines='tiflash';

select * from t1;
+------+------+
| a    | b    |
+------+------+
|    1 |    4 |
+------+------+

set session tiflash_fastscan=ON;
select * from t1;
+------+------+
| a    | b    |
+------+------+
|    1 |    2 |
|    1 |    4 |
|   10 |   20 |
+------+------+
```

> 在这些旧数据（相同主键的多版本旧数据和已经被 delete 语句删除的数据）被进行了 compact 整理，并且它们的数据版本小于 GC safe point 之后，才会被真正物理清理。此后在 FastScan 模式下不再返回这些数据 。数据被 compact 的时机受多种因素的自动触发，用户也可以通过 [`Alter Table ... Compact`](/sql-statements/sql-statement-alter-table-compact.md) 手动触发数据 compact 整理。 

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
2. Sort Merge：将步骤 1 中建立的数据流进行合并，并且将数据按照 (handle, version) 顺序排列返回。
3. Range Filter：根据读取范围限制，对步骤 2 中的数据进行过滤筛选并返回。
4. MVCC + Column Filter：对步骤 3 中的数据进行 MVCC 过滤，同时过滤掉不需要的列并返回。

FastScan 通过损失一定的数据一致性来获取更快的查询性能。FastScan 中的 TableScan 流程省略了上述过程中的第 2 步和第 4 步中 MVCC 的部分，从而提高查询性能。
---
title: Fast Mode 
summary: 介绍通过使用 fast mode 来加速 AP 场景的查询方法。
aliases: ['/zh/tidb/dev/use-fast-mode']
---
# Fast Mode

本章将介绍通过使用 fast mode 来加速 AP 场景的查询方法。

## 概述：

TiFlash 中的表默认属于 Normal Mode，在 Normal Mode 下，对应表的查询结果提供了数据一致性的保证，来提供了精准的查询结果。

而针对 AP 中对查询结果精度可以容忍一定误差，而对查询性能有更高的要求的场景，我们可以将对应的表切换成 TiFlash 的 Fast Mode 模式后，再进行查询。

我们可以根据对不同表的不同查询结果需求，来回切换对应表的模式。

## 切换成 fast mode 模式

所有表我们默认都是 Normal Mode。我们可以通过以下的语句将对应的表切换成 Fast Mode。

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name SET TIFALSH MODE FAST
```

我们可以通过以下语句来查看目前表的模式。

```sql
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'table_name' AND table_schema = 'database_name'
```

切换完成后，后续在 TiFlash 中的查询，都会在 Fast Mode 下进行，直到用下方的语句重新切换回 Normal Mode。

```sql
ALTER TABLE table_name SET TIFALSH MODE NORMAL
```

模式的切换会在全局生效。我们对于 TiFlash 模式的切换，只有在有 TiFlash Replica 的表中才能生效。并且对于临时表、内存表、系统表、以及列名中含有非 utf-8 字符的表，目前都不支持 TiFlash 相关的操作，因此也不支持对其修改 TiFlash table mode。

你可以通过 [ALTER TABLE SET TIFLASH MODE](/sql-statements/sql-statement-set-tiflash-mode.md)了解更多的细节。

## 实现机制：
TiFlash 中的存储层中，数据主要存放在 Delta 部分和 Stable 部分。

Normal Mode 中 TableScan 算子过程整体包括了以下步骤：
1. Read data : 在 Delta 层 和 Stable 层分别建立数据流，进行各自数据的读取。
2. Sort Merge : 将步骤1中建立的数据流进行合并，并且将数据按照 (handle,version) 顺序排列返回。
3. Range Filter : 对步骤2中的数据进行数据范围的过滤筛选并返回。
4. MVCC + Column Filter：对步骤三中的数据进行 MVCC 的过滤，并过滤掉不需要的列进行数据的返回。

而 Fast Mode 下通过损失一定的数据一致性来获取更快的查询性能，我们简化 Fast Mode 中的 TableScan 流程为
1. Read data :  在 Delta 层 和 Stable 层分别建立数据流，进行各自数据的读取。
2. Range Filter：对步骤1中的数据进行数据范围的过滤筛选并返回。
3. Delete Filter : 过滤掉删除操作所在行的数据, 并且过滤掉不需要的列进行数据的返回。
4. Merge : 将上述的数据流直接合并返回（不进行排序操作）

Fast Mode 下通过减少 MVCC 的过滤以及相关的操作，来提高查询的性能。
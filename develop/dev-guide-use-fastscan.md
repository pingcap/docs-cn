---
title: FastScan
summary: 介绍通过使用 FastScan 来加速 OLAP 场景的查询的方法。
---

# FastScan

> **警告：**
>
> 该功能目前是实验性功能，其形式和使用方法可能会在未来版本中发生变化。

本文档介绍通过使用 FastScan 来加速 Online Analytical Processing (OLAP) 场景中查询的方法。

默认情况下，TiFlash 能够保证查询结果精度以及数据一致性。如果使用 FastScan，TiFlash 可以实现更高效的查询性能，但不保证查询结果精度和数据一致性。

某些 OLAP 对查询结果精度可以容忍一定误差。如果对查询性能有更高要求，可以将对应的 TiFlash 表开启 FastScan 功能。

对于通过 [ALTER TABLE SET TIFLASH MODE](/sql-statements/sql-statement-set-tiflash-mode.md) 启用了 FastScan 的表，FastScan 会全局生效。对于临时表、内存表、系统表、以及列名中含有非 UTF-8 字符的表，都不支持 TiFlash 相关的操作。

了解更多信息，请参考 [ALTER TABLE SET TIFLASH MODE](/sql-statements/sql-statement-set-tiflash-mode.md)。

## 启用 FastScan

默认情况下，所有表都不启用 FastScan。你通过以下语句来查看 FastScan 状态。

```sql
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'table_name' AND table_schema = 'database_name'
```

通过以下语句将对应的表启用 FastScan。

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name SET TIFLASH MODE FAST
```

启用完成后，后续对应的表在 TiFlash 中的查询，都会使用 FastScan 功能。

可以用下面语句禁用 FastScan。

```sql
ALTER TABLE table_name SET TIFLASH MODE NORMAL
```

## 实现机制

TiFlash 存储层的数据主要存放在 Delta 层和 Stable 层。

Normal Mode 中 TableScan 算子过程整体包括了以下步骤:

1. Read data：在 Delta 层 和 Stable 层分别建立数据流，进行各自数据的读取。
2. Sort Merge：将步骤 1 中建立的数据流进行合并，并且将数据按照 (handle, version) 顺序排列返回。
3. Range Filter：根据读取范围限制，对步骤 2 中的数据进行过滤筛选并返回。
4. MVCC + Column Filter：对步骤 3 中的数据进行 MVCC 过滤，同时过滤掉不需要的列并返回。

FastScan 通过损失一定的数据一致性来获取更快的查询性能。FastScan 中的 TableScan 流程省略了上述过程中的第 2 步和第 4 步中 MVCC 的部分，从而提高查询性能。
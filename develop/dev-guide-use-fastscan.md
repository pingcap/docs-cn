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

某些 OLAP 对查询结果精度可以容忍一定误差。如果对查询性能有更高要求，可以在 session 级别或 global 级别开启 FastScan 功能，你可以通过修改变量 `tiflash_fastscan` 的值来选择是否启用 FastScan 功能。

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
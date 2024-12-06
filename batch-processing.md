---
title: 批量处理概览
summary: 介绍了 TiDB 为批量处理场景提供的功能，包括 Pipelined DML、非事务性 DML、IMPORT INTO 语句、被废弃的 batch dml 等
---

# 批量处理概览

批量处理场景对 TiDB 的主要挑战在于 TiDB 内存限制了事务的大小，以及对更快的处理速度的要求。

随着版本演进，TiDB 提供了多种批量数据处理功能，但它们之间的区别和适用场景容易混淆。本文将详细对比：
- Pipelined DML
- 非事务性 DML
- IMPORT INTO 语句
- 已废弃 batch dml

通过明确每个功能的特点，帮助在批量处理场景下做出正确选择。

## Pipelined DML

Pipelined DML 在 TiDB v8.1 LTS 作为实验性特性发布，在 v8.5 LTS 内核部分功能得到完善，性能大幅提升。

它的主要特点是:
1. 适合通用的批量数据处理场景，支持 INSERT、REPLACE、UPDATE、DELETE 操作。
2. 事务大小不再受到 TiDB 内存限制，支持处理超大规模数据。
3. 速度比标准 DML 更快。
4. 通过系统变量启用，无需修改 SQL 语句。

它的主要限制是：
1. 只适用于自动提交的语句。

它的适用场景是：通用的批量数据处理场景，例如大量数据的插入、更新、删除等。

更多信息见[Pipelined DML](/pipelined-dml.md)。

## 非事务 DML 语句

非事务 DML 语句是在 TiDB v6.1 LTS 首次引入的功能，支持 DELETE。在 v6.5 中开始支持 INSERT、REPLACE、UPDATE。

它的主要特点是：
- 通过将一条语句拆为多条语句执行，使得每个语句的事务更小，绕开内存限制。
- 处理速度比标准 DML 稍快或相当。

它的主要限制是：
- 只适用于自动提交的语句。
- 需要修改 SQL 语句。
- 对 SQL 语句本身限制较多，不符合条件的语句可能需要改写。
- 因为拆分执行，不具有完整的事务 ACID 性质，在失败时语句可能部分完成。

它的适用场景是：大量数据的插入、更新、删除等场景。由于限制较多，建议在 Pipelined DML 不适用的场景下考虑使用。

更多信息见[非事务 DML 语句](/non-transactional-dml.md)。

## IMPORT INTO 语句

IMPORT INTO 语句是在 TiDB v7.5 LTS 首次引入的功能，专为数据导入设计，以替代 TiDB Lightning。

它的主要特点是：
- 导入速度非常快。
- 易用性比 TiDB Lightning 更高。

它的主要限制是：
- 只适合数据导入场景。
- 不满足事务 ACID 性质。
- 使用限制较多。

它的适用场景是：数据导入场景，例如数据迁移、数据恢复等。建议在合适的场景下，使用 IMPORT INTO 代替 TiDB Lightning。

更多信息见[IMPORT INTO](/sql-statements/sql-statement-import-into.md)。

## 已被废弃的 batch dml

在 TiDB v4.0 以前用于批量处理的 batch dml 功能已被废弃，不再推荐使用。这个功能是由以下这组系统变量控制的:

- `tidb_batch_insert`
- `tidb_batch_delete`
- `tidb_batch_commit`
- `tidb_enable_batch_dml`
- `tidb_dml_batch_size`

这组功能因为容易引起数据索引不一致，导致数据损坏或丢失，已被废弃。相关变量将被逐渐移除。

不建议在任何场景下使用已被废弃的 batch dml 功能。建议迁移到上面描述的其它方案。
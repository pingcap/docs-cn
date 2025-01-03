---
title: 数据批量处理
summary: 介绍了 TiDB 为数据批量处理场景提供的功能，包括 Pipelined DML、非事务性 DML、IMPORT INTO 语句以及已被废弃的 batch-dml。
---

# 数据批量处理

批量数据处理是实际业务中常见且重要的操作，它涉及到对大量数据进行高效操作，如数据迁移、批量导入、归档操作或大规模更新等。

为了提升批量处理性能，TiDB 随着版本的演进提供了多种数据批量处理功能：

- 数据导入
    - `IMPORT INTO` 语句（从 TiDB v7.2.0 开始引入，在 v7.5.0 成为正式功能）
- 数据增删改
    - Pipelined DML（从 TiDB v8.0.0 开始引入，实验特性）
    - 非事务性 DML（从 TiDB v6.1.0 开始引入）
    - 已废弃的 batch-dml 功能

本文分别介绍这些功能的主要优势、限制和使用场景，帮助你根据实际需求选择合适的方案，从而更高效地完成批量数据处理任务。

## 数据导入

`IMPORT INTO` 语句专为数据导入设计，使你无需单独部署 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)，即可将 CSV、SQL 或 PARQUET 等格式的数据快速导入到 TiDB 的一张空表中。

主要优势：

- 导入速度非常快。
- 比 TiDB Lightning 更易用。

主要限制：

- 不满足事务 [ACID](/glossary.md#acid) 性质。
- 使用限制较多。

适用场景：

- 数据导入场景，例如数据迁移、数据恢复等。建议在合适的场景下，使用 IMPORT INTO 代替 TiDB Lightning。

更多信息，请参考 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)。

## 数据增删改

### Pipelined DML

Pipelined DML 是从 TiDB v8.0.0 开始引入的实验特性。在 v8.5.0 中，TiDB 对该功能进行了完善，其性能得到大幅提升。

主要优势：

- 在事务执行过程中，通过将数据持续写入存储层，而不是全部缓存在内存中，使得事务大小不再受到 TiDB 内存限制，支持处理超大规模数据。
- 速度比标准 DML 更快。
- 通过系统变量启用，无需修改 SQL 语句。

主要限制：

- 只适用于[自动提交](/transaction-overview.md#自动提交)的 `INSERT`、`REPLACE`、`UPDATE`、`DELETE` 语句。

适用场景：

- 通用的批量数据处理场景，例如大量数据的插入、更新、删除等。

更多信息，请参考 [Pipelined DML](/pipelined-dml.md)。

### 非事务 DML 语句

非事务 DML 语句是从 TiDB v6.1.0 开始引入的功能。在 v6.1.0 中，该功能仅支持 `DELETE` 语句。从 v6.5.0 起，该功能新增支持 `INSERT`、`REPLACE`、`UPDATE` 语句。

主要优势：

- 通过将一条 SQL 语句拆为多条语句执行，使得每个语句的事务更小，绕开内存限制。
- 处理速度比标准 DML 稍快或相当。

主要限制：

- 只适用于[自动提交](/transaction-overview.md#自动提交)的语句。
- 需要修改 SQL 语句。
- 对 SQL 语句本身限制较多，不符合条件的语句可能需要改写。
- 因为 SQL 语句被拆分执行，不具有完整的事务 ACID 性质，在失败时语句可能部分完成。

适用场景：

- 大量数据的插入、更新、删除等场景。由于限制较多，建议在 Pipelined DML 不适用的场景下考虑使用。

更多信息，请参考[非事务 DML 语句](/non-transactional-dml.md)。

### 已被废弃的 batch-dml

TiDB 在 v4.0 之前提供了 batch-dml 功能，用于批量数据处理。该功能已被废弃，不再推荐使用。batch-dml 功能由以下这些系统变量控制：

- `tidb_batch_insert`
- `tidb_batch_delete`
- `tidb_batch_commit`
- `tidb_enable_batch_dml`
- `tidb_dml_batch_size`

因为该功能可能引起数据索引不一致，导致数据损坏或丢失，以上变量已被废弃，并计划将在未来的版本中逐渐移除。

不建议在任何场景下使用已被废弃的 batch-dml 功能。建议选择上面描述的其它方案。
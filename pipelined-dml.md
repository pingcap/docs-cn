---
title: Pipelined DML
summary: 介绍 Pipelined DML 的使用场景、使用方法、使用限制和使用该功能的常见问题。Pipelined DML 增强了 TiDB 批量处理的能力，使得事务大小不再受到 TiDB 内存限制。
---

# Pipelined DML

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。语法和实现可能会在 GA 前发生变化。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

本文介绍 Pipelined DML 的使用场景、使用方法、使用限制和使用该功能的常见问题。

## 功能概述

Pipelined DML 是 TiDB 从 v8.0.0 开始引入的实验特性，用于优化大规模数据写入场景的性能。启用 Pipelined DML 后，当执行 DML 操作时，TiDB 会将相应的数据持续写入存储层，而不是全部缓存在内存中。这种方式就像流水线 (Pipeline) 一样，数据一边被读取（输入），一边被写入到存储层（输出），从而解决了大规模 DML 操作的以下常见问题：

- 内存限制：传统 DML 在处理大量数据时容易导致 OOM
- 性能瓶颈：大事务执行效率低，容易引起系统负载波动

启用此功能后，你可以：

- 执行不受 TiDB 内存限制的大规模数据操作
- 获得更平稳的系统负载和更低的操作延迟
- 将事务内存使用控制在可预测范围内（在 1 GiB 以内）

在以下场景中，建议考虑启用 Pipelined DML：

- 需要处理数百万行或更多数据的写入
- 执行 DML 操作时遇到内存不足错误
- 大规模数据操作导致系统负载波动明显

需要注意的是，虽然 Pipelined DML 能显著降低事务处理的内存需求，但执行大规模数据操作时，仍需要[设置合理的内存阈值](/system-variables.md#tidb_mem_quota_query)（建议至少 2 GiB），以确保除事务以外其他模块（如执行器）的正常运行。

## 使用限制

目前，Pipelined DML 存在以下使用限制：

- 与 TiCDC、TiFlash 或 BR 尚不兼容，请勿在与这些组件有关的表上使用 Pipelined DML。强行使用可能会引发阻塞以及这些组件的 OOM 等问题。
- 不适用于存在写入冲突的场景。在这种场景下，Pipelined DML 性能可能大幅下降，或失败回滚。
- 在使用 Pipelined DML 执行 DML 语句的过程中，需要确保[元数据锁](/metadata-lock.md)保持开启。
- 启用 Pipelined DML 后，TiDB 在执行 DML 语句时会自动检测以下条件是否全部符合。如果其中任一条件不符合，TiDB 会拒绝使用 Pipelined DML 执行该语句，自动回退到普通 DML 执行，并生成对应的 warning 信息：
    - 仅支持[自动提交](/transaction-overview.md#自动提交)的语句。
    - 仅支持 `INSERT`、`UPDATE`、`REPLACE` 和 `DELETE` 语句。
    - 操作的表不包含[临时表](/temporary-tables.md)或[缓存表](/cached-tables.md)。
    - 当[外键约束](/foreign-key.md)检查开启 (`foreign_key_checks = ON`) 时，操作的表不包含外键关系。
- 当使用 Pipelined DML 执行 `INSERT IGNORE ... ON DUPLICATE KEY UPDATE` 语句时，如果更新操作发生冲突，可能会返回 `Duplicate entry` 错误。

## 使用方法

本小节介绍如何启用 Pipelined DML 并验证其是否生效。

### 启用 Pipelined DML

根据需要，你可以选择以下方式之一启用 Pipelined DML：

- 如需在会话级别启用 Pipelined DML，请将 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-从-v800-版本开始引入) 变量设置为 `"bulk"`：

    ```sql
    SET tidb_dml_type = "bulk";
    ```

- 如需为某一条 DML 语句启用 Pipelined DML，请在该语句中添加 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) hint。

    - 数据归档示例：

        ```sql
        INSERT /*+ SET_VAR(tidb_dml_type='bulk') */ INTO target_table SELECT * FROM source_table;
        ```

    - 批量数据更新示例：

        ```sql
        UPDATE /*+ SET_VAR(tidb_dml_type='bulk') */ products
        SET price = price * 1.1
        WHERE category = 'electronics';
        ```

    - 批量删除示例：

        ```sql
        DELETE /*+ SET_VAR(tidb_dml_type='bulk') */ FROM logs WHERE log_time < '2023-01-01';
        ```

### 验证是否生效

执行 DML 语句后，可以查看 [`tidb_last_txn_info`](/system-variables.md#tidb_last_txn_info-从-v409-版本开始引入) 变量来确认该语句的执行是否使用了 Pipelined DML：

```sql
SELECT @@tidb_last_txn_info;
```

如果返回结果中 `pipelined` 字段为 `true`，则表示成功使用了 Pipelined DML。

## 最佳实践

- 将 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 略微调大，以确保执行器等部分的内存使用不会超过限制。建议至少设置为 2 GiB。对于 TiDB 内存充足的情况，可以适当调大。
- 在向新表插入数据的场景，Pipelined DML 性能易受到热点影响。为实现最佳性能，建议尽可能先打散热点。可以参考 [TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)。

## 相关配置

- 系统变量 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-从-v800-版本开始引入) 用于控制是否在会话级别启用 Pipelined DML。
- 当 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-从-v800-版本开始引入) 设置为 `"bulk"` 时，配置项 [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit) 的效果等同于设置为 `false`。
- 以 Pipelined DML 方式执行事务时，事务的大小不受 TiDB 配置项 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 的限制。
- 以 Pipelined DML 方式执行超大事务时，事务耗时可能较长。对于这种模式的事务，其事务锁的最大 TTL 为 [`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl) 与 24 小时中的较大值。
- 当事务执行时间超过 [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-从-v610-版本开始引入) 设定值后，GC 可能会强制回滚事务，导致事务失败。

## 观测 Pipelined DML

你可以通过以下方式观测 Pipelined DML 的执行过程：

- 查看系统变量 [`tidb_last_txn_info`](/system-variables.md#tidb_last_txn_info-从-v409-版本开始引入)，获取当前会话上一个事务的执行信息，包括是否使用了 Pipelined DML。
- 查看 TiDB 日志中包含 `"[pipelined dml]"` 字样的行，了解 Pipelined DML 的执行过程和进度，包括当前阶段、已经写入的数据量等。
- 查看 TiDB 日志中的 [`expensive query` 日志](/identify-expensive-queries.md#expensive-query-日志示例)的 `affected rows` 字段，获取耗时较长语句的当前进度。
- 查看 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表，了解事务的执行进度。Pipelined DML 通常用于大事务，执行耗时较长，可以通过该表查看事务的执行进度。

## 常见问题

### 为什么我的查询没有使用 Pipelined DML？

当 TiDB 拒绝以 Pipelined DML 模式执行语句时，会生成对应的警告信息，可以通过检查警告信息 (`SHOW WARNINGS;`) 确定原因。

常见的原因：

- DML 语句不是自动提交的
- 使用了不支持的表类型，例如[临时表](/temporary-tables.md)或[缓存表](/cached-tables.md)
- 涉及外键且外键检查开启

### Pipelined DML 会影响事务的隔离级别吗？

不会。Pipelined DML 仅改变了事务写入的实现机制，不影响 TiDB 的事务隔离保证。

### 为什么使用了 Pipelined DML 还是会出现内存不足？

即使开启了 Pipelined DML，仍然有可能碰到内存 quota 不足导致语句被 kill 的情况：

```
The query has been canceled due to exceeding the memory limit allowed for a single SQL query. Please try to narrow the query scope or increase the tidb_mem_quota_query limit, and then try again.
```

这是因为 Pipelined DML 功能仅能控制事务执行过程中数据使用的内存，但语句执行时使用的总内存还包括执行器等部分的内存。如果语句执行时所需的总内存超过了 TiDB 的内存限制，仍然可能会出现内存不足的错误。

通常情况下，将系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 设置为更大的值可以解决该问题。推荐设置为 2 GiB。对于算子复杂或涉及数据量大的 SQL 语句，可能需要将该变量设置为更大的值。

## 探索更多

- [批量处理概览](/batch-processing.md)
- [TiDB 内存控制](/configure-memory-usage.md)
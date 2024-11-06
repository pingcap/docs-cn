---
title: Pipelined DML
summary: Pipelined DML 增强了 TiDB 批量处理的能力，使得事务大小不再受到 TiDB 内存限制。batch processing, bulk, non-transactional DML
---

# Pipelined DML

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。语法和实现可能会在 GA 前发生变化。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

本文档介绍 Pipelined DML 的使用场景、使用方法、使用限制和使用该功能的常见问题。

Pipelined DML 是 TiDB 的一项实验特性，用于优化大规模数据写入场景。通过持续将事务数据写入存储层而不是完全缓存在内存中，该特性可以显著降低内存占用，提升大规模数据写入性能。使用 Pipelined DML，你可以执行超大规模的 DML 操作而不必担心内存溢出问题。

## 使用场景和作用

Pipelined DML 在以下场景中具有明显优势：

- 需要执行大规模数据迁移或归档操作
- 进行批量数据导入或更新
- ETL (Extract, Transform, Load) 处理涉及大量数据写入
- 需要降低大规模写入时的内存占用

Pipelined DML 在这些场景主要有 3 点优势
- 事务使用内存可控，事务大小不受 TiDB 内存总量限制。事务部分内存使用限制在 1 GiB 以内。
- 延迟更低。
- CPU 和 IO 负载更平滑。

### 数据归档场景

当需要将历史数据从活跃表归档到归档表时，通常涉及大量数据迁移。例如：

```sql
INSERT INTO sales_archive SELECT * FROM sales WHERE sale_date < '2023-01-01';
```

使用 Pipelined DML 可以有效处理数百万行数据的迁移，避免 OOM 问题。

### 批量数据更新场景

当需要对大量数据进行更新操作时，例如批量调整商品价格或更新用户状态，Pipelined DML 可以高效完成操作：

```sql
UPDATE /*+ SET_VAR(tidb_dml_type='bulk') */ products 
SET price = price * 1.1 
WHERE category = 'electronics';
```

### 批量删除场景

当需要删除大量数据时，例如删除历史数据或清理过期数据，Pipelined DML 可以高效完成操作：

```sql
DELETE /*+ SET_VAR(tidb_dml_type='bulk') */ FROM logs WHERE log_time < '2023-01-01';
```

## 使用方法

### 启用 Pipelined DML

要使用 Pipelined DML，你需要将 `tidb_dml_type` 会话变量设置为 `"bulk"`：

```sql
SET tidb_dml_type = "bulk";
```

或者使用 SET_VAR hint，如：

```sql
INSERT /*+ SET_VAR(tidb_dml_type='bulk') */ INTO target_table SELECT * FROM source_table;
```

### 验证是否生效

执行语句后，可以通过检查 [`tidb_last_txn_info`](#tidb_last_txn_info-从-v409-版本开始引入) 变量来确认是否使用了 Pipelined DML：

```sql
SELECT @@tidb_last_txn_info;
```

如果返回结果中 `pipelined` 字段为 `true`，则表示成功使用了 Pipelined DML。

## 使用条件

1. 操作包含涉及 TiCDC、TiFlash 或 BR 的表时不可以使用。
> **警告：**
>
> 目前 Pipelined DML 尚不兼容，强行使用可能会引发阻塞和相关组件 OOM 等问题。未来版本会逐渐支持。

2. Pipelined DML 不适合在有写写冲突的场景使用。在这种场景下，Pipelined DML 性能可能大幅下降，或失败回滚。
3. 需要确保在语句执行过程中保持[元数据锁](/metadata-lock.md)处于开启状态。 
4. 使用 Pipelined DML 时，TiDB 会检测以下条件是否符合，不符合时 TiDB 会拒绝使用 Pipelined DML 执行，并自动回退到普通 DML 执行，同时生成对应的 Warning 信息：
    - 仅适用于自动提交的语句
    - 仅适用于 `INSERT`、`UPDATE`、`REPLACE` 和 `DELETE` 语句
    - 不可用于[临时表](/temporary-tables.md)和[缓存表](/cached-tables.md)
    - 开启外键约束检查时 (`foreign_key_checks = ON`) ，不可包含外键相关表操作

特殊行为：
  - `INSERT IGNORE ... ON DUPLICATE UPDATE` 语句可能会在更新造成冲突时报出 `Duplicate entry` 的错误。

## 最佳实践

- 将 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 略微调大，以确保执行器等部分的内存使用不会超过限制。建议值为至少 2 GiB。对于 TiDB 内存充足的情况，可以适当调大。
- 在向新表进行插入的场景，Pipelined DML 易于受到热点影响。为实现最佳性能，建议尽可能先打散热点。可以参考[TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md#tidb-热点问题处理)。

## 相关配置

- 系统变量 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-从-v800-版本开始引入)：用于控制是否启用 Pipelined DML。
- 配置项[`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit)：当使用 Pipelined DML 时，该配置项的效果等同于设置为 `false`。
- 以 Pipelined DML 方式执行超大事务时，事务耗时可能较长。对于这种模式的事务，其事务锁的最大 TTL 为 [`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl) 与 24 小时中的较大值。
- 当事务执行时间超过 [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-从-v610-版本开始引入) 设定值后，GC 可能会强制回滚事务，导致事务失败。
- 以 `"bulk"` 方式执行事务时，事务的大小不受 TiDB 配置项 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 的限制。

## 观测 Pipelined DML

Pipelined DML 的执行过程可以通过以下方式进行观测：
- 系统变量[`tidb_last_txn_info`](#tidb_last_txn_info-从-v409-版本开始引入)，它可以查看上一个事务的执行信息，包括是否使用了 Pipelined DML。
- TiDB 日志中包含 "[pipelined dml]" 字样的日志行表示展示了 Pipelined DML 的执行过程和进度，包括当前阶段、已经写入的数据量等。
- TiDB 日志中的 ["expensive query" 日志](/identify-expensive-queries.md#expensive-query-日志示例) 包含的 affected rows 字段，可以查看耗时较长语句的当前进度。
- [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)表，会展示事务的执行进度。Pipelined DML 通常用于大事务，执行耗时较长，可以通过该表查看事务的执行进度。

## 常见问题

### 为什么我的查询没有使用 Pipelined DML？

当 TiDB 拒绝以 Pipelined DML 模式执行语句时，会生成对应的 warning，可以通过检查 warning 信息得知原因。

常见的原因：

1. 语句不是自动提交的
2. 使用了不支持的表类型
3. 涉及外键且外键检查开启

### Pipelined DML 会影响事务的隔离级别吗？

不会。Pipelined DML 仅改变了事务写入的实现机制，不影响 TiDB 的事务隔离保证。

### 为什么使用了 Pipelined DML 还是会内存不足？

即时开启了 Pipelined DML，仍然有可能碰到内存 quota 不足导致语句被 kill 的情况：
```
The query has been canceled due to exceeding the memory limit allowed for a single SQL query. Please try to narrow the query scope or increase the tidb_mem_quota_query limit, and then try again.
```

这是因为 Pipelined DML 功能仅控制了事务部分使用的内存，但语句使用的总内存还需要包括执行器等部分的内存。如果语句需要的总内存空间超过了 TiDB 的内存限制，仍然会出现内存不足的情况。
通常将 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 设置为更大的值可以解决这个问题。推荐设置为 2 GiB。对于算子复杂或数据量大的 SQL，可能需要更大的值。

## 探索更多

- [批量处理概览](/batch-processing.md)
- [TiDB 内存控制](/configure-memory-usage.md)
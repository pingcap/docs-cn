---
title: 非事务 DML 
summary: 以事务的原子性和隔离性为代价，将 DML 拆成多个批次执行，用以提升批量数据处理场景的性能和易用性。
---

# 非事务 DML

本文档介绍非事务 DML 的使用场景、使用方法、使用限制和使用该功能的常见问题。

非事务 DML 是将一个普通 DML 拆成多个 SQL 执行，以牺牲事务的原子性和隔离性为代价，增强批量数据处理场景下的性能和易用性。

目前，

> **注意：**
>
> 非事务 DML 不保证该语句的原子性和隔离性，不能认为它和原始 DML 等价。

## 使用场景

在大批量的数据处理场景，经常需要对一大批数据执行相同的操作。如果直接使用一个 SQL 语句，很可能导致事务大小超过限制，且大事务的性能影响比较明显。

批量数据处理操作往往和在线业务操作不具有时间或数据上的交集，没有并发操作时，隔离性是不必要的。
如果将批量数据操作设计成幂等的，或者易于重试的，那么原子性可以是不必要的。业务满足了这两个条件，那么可以考虑使用非事务 DML。

例如一个期删除过期数据的需求，在确保没有任何业务会访问过期数据时，适合使用非事务 DML 来提升删除性能。

## 前提条件

要使用非事务 DML，必须满足以下条件：

- 确认该语句不需要原子性。即执行结果可能是一部分行被修改，一部分没有。该语句需要是幂等的，或是做好了根据错误信息对部分数据重试的准备。**如果开启了 `tidb_redact_log = 1` 且 `tidb_nontransactional_ignore_error = 1`，则该语句必须是幂等的**。否则语句部分失败时无法准确定位失败的部分。
- 确认该语句将要操作的数据没有其它并发的写入。
- 确认该语句不会修改它自己会读取的内容，否则后续的 batch 读到之前 batch 写入的内容，容易引起非预期的现象。
- 确认该语句满足[使用限制](#使用限制)。
- 不建议同时在该 DML 将要读写的表上进行并发的 DDL 操作。

> **警告：**
>
> 如果同时开启了 redact log 和 tidb_nontransactional_ignore_error，用户可能无法完整得知每个 batch 的错误信息，无法只对失败的 batch 进行重试。因此这个非事务 DML 必须是幂等的。

## 使用方法

TiDB 目前支持的非事务 DML 只有 DELETE 语句。其语法见 [BATCH](/sql-statements/sql-statement-batch.md)。

最佳实践：

1. （可选）DRY RUN QUERY，手动执行该查询，确认 DML 影响的数据范围是否大体正确。
2. （可选）DRY RUN，检查拆分后的语句和执行计划。关注索引选择效率。
3. 执行非事务 DML
4. 如果报错，从报错信息或日志中获取具体失败的数据范围，进行重试或手动处理。

非事务 DML 执行过程中，可以通过 `show processlist` 查看执行进度。日志、慢日志等也会记录每个拆分后的语句在整个非事务 DML 中的进度。

通过 `KILL TIDB` kill 一个非事务语句时，会取消当前正在执行的 batch 之后的所有 batch。执行结果信息需要从日志里获得。

## 参数说明

| 参数 | 说明 | 默认值 | 是否必填 | 建议值 |
| :-- | :-- | :-- | :-- | :-- |
| 划分列 | 用于划分 batch 的列 | TiDB 尝试自动选择 | 否 | 选择可以最高效地满足 where 条件的列 |
| batch size | 用于控制每个 batch 的大小 | N/A | 是 | 1K - 1M。过小和过大都会导致性能下降 |

### 划分列的选择

非事务语句需要用一个列作为数据分批的标准。为效率考虑，这一列必须能够利用索引。不同的索引和划分列所导致的执行效率可能有数十倍的差别。可以参考以下两条建议。

- 索引选择率高的索引中的列。不同索引选择率可能导致数十倍的性能差异。
- 有聚簇索引时，用主键作为划分列效率更高（包括 int handle 和 _tidb_rowid）

用户可以不指定划分列，TiDB 默认会使用 handle 的第一列。但是如果聚簇索引主键的第一列是不支持的数据类型，TiDB 会报错。需要用户自己选择合适的划分列。

### batch size 的选择

batch size 越大，拆分出来的 SQL 越少，每个 SQL 越慢。最优的 batch size 依据 workload 而定，根据经验值推荐从 50000 开始尝试。
过小和过大的 batch size 执行效率都会下降。

每个 batch 的信息需要存在内存里，因此 batch 数量过多会显著增加消耗的内存。这也是 batch size 不能过小的原因之一。

## 使用限制

非事务 DML 的硬性限制，不满足这些条件将会报错。

- 只可对单表进行操作。
- DML 不可以包含 ORDER BY 或 LIMIT 字句。
- 用于拆分的列必须被索引。该索引可以是单列的索引，或是一个联合索引的第一列。
- 必须在 [`autocommit`](/system-variables.md#autocommit) 模式中使用。
- 不可以在开启旧的 batch-dml feature 时使用
- 不可以设置了 [tidb_snapshot](/read-historical-data.md#操作流程) 时使用。
- 不可以用在 prepare 语句。
- 划分列不支持 ENUM，SET，JSON，DURATION，TIME 等类型。
- 不可以用在[临时表](/temporary-tables.md)上。
- 不支持[公共表表达式](/develop/use-common-table-expression.md）。

## 原理

非事务 DML 的实现原理，是将原本需要在用户侧手动执行的拆分工作内置为 TiDB 的一个功能，降低用户负担。要理解非事务 DML 的行为，可以将其想象成一个用户脚本做了如下事情：

对于非事务 DML："BATCH ON $C$ LIMIT $N$ DELETE FROM ... WHERE $P$"

1. 根据原始语句的筛选条件 $P$，和指定的用于拆分的列 $C$，查询出所有满足 $P$ 的 $C$。对这些 $C$ 排序后按 $N$ 分成多个分组 $B_1 \dots B_k$。对所有 $B_i$，保留它的第一个和最后一个 $C$，记为 $S_i$ 和 $E_i$。这一步所执行的查询语句，可以通过 [DRY RUN QUERY](/sql-statements/sql-statement-batch.md#示例) 查看。
2. 那么 $B_i$ 所涉及的数据就是满足 $P_i$:`C BETWEEN <S_i> AND <E_i>` 的一个子集。可以通过 $P_i$ 来缩小每个 batch 需要处理的数据范围。
3. 对 $B_i$，将上面这个条件嵌入原始语句的 WHERE 条件，使其变为`WHERE ($P_i$) AND ($P$)`。这一步的执行结果，可以通过 [DRY RUN](/sql-statements/sql-statement-batch.md#示例) 查看。
4. 对所有 batch，依次执行新的语句。收集每个分组的错误并合并，在所有分组结束后作为整个非事务 DML 的结果返回。

## 部分失败

非事务 DML 不满足原子性，可能存在一些 batch 成功，一些 batch 失败的情况。系统变量 `tidb_nontransactional_ignore_error` 控制了非事务 DML 处理错误的行为。

当 `tidb_nontransactional_ignore_error=0`，在碰到第一个报错的 batch 时，非事务 DML 即中止，取消其后的所有 batch，返回错误。

当 `tidb_nontransactional_ignore_error=1`，当某个 batch 执行报错时，其后的 batch 会继续执行，直到所有 batch 执行完毕，返回结果时把这些错误合并后返回。
但一个例外是，如果第一个 batch 就执行失败，有很大概率是语句本身有错，此时整个非事务语句会直接返回一个错误。

## 与旧版本 batch-dml 的对比

非事务 DML 尚不能替代所有的 batch-dml 使用场景。
它们的主要区别有

### 性能

在索引选择率较高的情况下，非事务 DML 和 batch-dml 性能接近。在索引选择率差的情况下，非事务 DML 可能会明显慢于 batch-dml。

### 稳定性

batch-dml 极易因为使用不当导致数据索引不一致问题。

非事务 DML 不会导致数据索引不一致问题。但使用不当时，非事务 DML 与原始语句不等价，应用可能观察到和预期不符的现象。详见[常见问题](#常见问题)。

## 常见问题

### 报错：Failed to restore the delete statement, probably because of unsupported type of the shard column

划分列的类型暂时不支持 ENUM，SET，JSON，DURATION，TIME 等类型，请尝试重新指定一个划分列。推荐使用整数或字符串类型。

### 和普通的 Delete 不等价的“异常”行为

非事务 DML 和这个 DML 的原始形式并不等价，这可能是由以下原因导致的

- 有并发的其它写入
- 非事务 DML 修改了它自己会读取的值。Read your own write！
- 在每个 batch 上实际执行的 SQL 由于改变了 where 条件，可能会导致执行计划不一样、表达式计算顺序不一样等，由此导致了执行结果不一样。
- DML 中含有非确定性的操作。

## 兼容信息

非事务语句是 TiDB 独有的功能，与 MySQL 不兼容。

## 探索更多

* [BATCH](/sql-statements/sql-statement-batch.md) 语法
* [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-从-v61-版本开始引入)

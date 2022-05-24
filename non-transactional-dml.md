---
title: 非事务 DML 语句
summary: 以事务的原子性和隔离性为代价，将 DML 语句拆成多个语句依次执行，用以提升批量数据处理场景的稳定性和易用性。
---

# 非事务 DML 语句

本文档介绍非事务 DML 语句的使用场景、使用方法、使用限制和使用该功能的常见问题。

非事务 DML 语句是将一个普通 DML 语句拆成多个 SQL 语句（即多个 batch）执行，以牺牲事务的原子性和隔离性为代价，增强批量数据处理场景下的性能和易用性。

非事务 DML 语句包括 `INSERT`、`UPDATE` 和 `DELETE`，TiDB 目前只支持非事务 `DELETE` 语句，详细的语法介绍见 [`BATCH`](/sql-statements/sql-statement-batch.md)。

> **注意：**
>
> 非事务 DML 语句不保证该语句的原子性和隔离性，不能认为它和原始 DML 语句等价。

## 使用场景

在大批量的数据处理场景，用户经常需要对一大批数据执行相同的操作。如果直接使用一个 SQL 语句执行操作，很可能导致事务大小超过限制，而大事务会明显影响执行性能。

批量数据处理操作往往和在线业务操作不具有时间或数据上的交集。没有并发操作时，隔离性是不必要的。如果将批量数据操作设计成幂等的，或者易于重试的，那么原子性也是不必要的。如果你的业务满足这两个条件，那么可以考虑使用非事务 DML 语句。

非事务 DML 语句用于在特定场景下绕过大事务的事务大小限制，用一条语句完成原本需要拆分成多个事务完成的任务，且执行效率更高，占用资源更少。

例如，对于一个删除过期数据的需求，在确保没有任何业务会访问过期数据时，适合使用非事务 DML 语句来提升删除性能。

## 前提条件

要使用非事务 DML 语句，必须满足以下条件：

- 确保该语句不需要原子性，即允许执行结果中，一部分行被修改，而一部分行没有被修改。
- 确保该语句具有幂等性，或是做好准备根据错误信息对部分数据重试。如果系统变量 `tidb_redact_log = 1` 且 `tidb_nontransactional_ignore_error = 1`，则该语句必须是幂等的。否则语句部分失败时，无法准确定位失败的部分。
- 确保该语句将要操作的数据没有其它并发的写入，即不被其它语句同时更新。否则可能出现漏删、多删等非预期的现象。
- 确保该语句不会修改语句自身会读取的内容，否则后续的 batch 读到之前 batch 写入的内容，容易引起非预期的情况。
- 确认该语句满足[使用限制](#使用限制)。
- 不建议在该 DML 语句将要读写的表上同时进行并发的 DDL 操作。

> **警告：**
>
> 如果同时开启了 `tidb_redact_log` 和 `tidb_nontransactional_ignore_error`，你可能无法完整得知每个 batch 的错误信息，无法只对失败的 batch 进行重试。因此，如果同时开启了这两个系统变量，该非事务 DML 语句必须是幂等的。

## 使用示例

### 使用非事务 DML 语句

以下部分通过示例说明非事务 DML 语句的使用方法：

创建一张表 `t`，表结构如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE t(id int, v int, key(id));
```

```sql
Query OK, 0 rows affected
```

向表 `t` 中插入一些数据。

{{< copyable "sql" >}}

```sql
INSERT INTO t VALUES (1,2),(2,3),(3,4),(4,5),(5,6);
```

```sql
Query OK, 5 rows affected
```

以下操作使用非事务 DML 语句，删除表 `t` 的 `v` 列上小于整数 6 的行。该语句将以 2 为 batch size，以 `id` 列为划分列，拆分为两个 SQL 语句执行。

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DELETE FROM t where v < 6;
```

```sql
+----------------+---------------+
| number of jobs | job status    |
+----------------+---------------+
| 2              | all succeeded |
+----------------+---------------+
1 row in set
```

查看非事务 DML 语句的删除结果。

{{< copyable "sql" >}}

```sql
SELECT * FROM t;
```

```sql
+----+---+
| id | v |
+----+---+
| 5  | 6 |
+----+---+
1 row in set
```

### 查看非事务 DML 语句的执行进度

非事务 DML 语句执行过程中，可以通过 `SHOW PROCESSLIST` 查看执行进度，返回结果中的 `Time` 表示当前 batch 执行的耗时。日志、慢日志等也会记录每个拆分后的语句在整个非事务 DML 语句中的进度。例如：

{{< copyable "sql" >}}

```sql
show processlist;
```

```sql
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
| Id   | User | Host               | db     | Command | Time | State      | Info                                                                                               |
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
| 1203 | root | 100.64.10.62:52711 | test   | Query   | 0    | autocommit | /* job 506/500000 */ DELETE FROM `test`.`t1` WHERE `test`.`t1`.`_tidb_rowid` BETWEEN 2271 AND 2273 |
| 1209 | root | 100.64.10.62:52735 | <null> | Query   | 0    | autocommit | show full processlist                                                                              |
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
```

### 终止一个非事务 DML 语句

通过 `KILL TIDB` 终止一个非事务语句时，TiDB 会取消当前正在执行的 batch 之后的所有 batch。执行结果信息需要从日志里获得。

### 查询非事务 DML 语句中划分 batch 的语句

要查询非事务 DML 语句中用于划分 batch 的语句，你可在非事务 DML 语句中添加 `DRY RUN QUERY`。添加后，TiDB 不实际执行这个查询和后续的 DML 操作。

下面这条语句查询 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 这条非事务 DML 语句内用于划分 batch 的查询语句。

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DRY RUN QUERY DELETE FROM t WHERE v < 6;
```

```sql
+--------------------------------------------------------------------------------+
| query statement                                                                |
+--------------------------------------------------------------------------------+
| SELECT `id` FROM `test`.`t` WHERE (`v` < 6) ORDER BY IF(ISNULL(`id`),0,1),`id` |
+--------------------------------------------------------------------------------+
1 row in set
```

### 查询非事务 DML 语句中首末 batch 对应的语句

要查询非事务 DML 语句中第一个和最后一个 batch 对应的实际 DML 语句，你可在语句中添加 `DRY RUN`。添加后，TiDB 只划分 batch，不执行这些 SQL 语句。因为 batch 数量可能很多，不显示全部 batch，只显示第一个和最后一个 batch。

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DRY RUN DELETE FROM t where v < 6;
```

```sql
+-------------------------------------------------------------------+
| split statement examples                                          |
+-------------------------------------------------------------------+
| DELETE FROM `test`.`t` WHERE (`id` BETWEEN 1 AND 2 AND (`v` < 6)) |
| DELETE FROM `test`.`t` WHERE (`id` BETWEEN 3 AND 4 AND (`v` < 6)) |
+-------------------------------------------------------------------+
2 rows in set
```

### 在非事务 DML 语句中使用 Optimizer Hint

对于 `DELETE` 语句原本支持的 Optimizer Hint，非事务 `DELETE` 语句也同样支持，hint 位置与普通 `DELETE` 语句中的位置相同：

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DELETE /*+ USE_INDEX(t)*/ FROM t where v < 6;
```

## 最佳实践

建议按照以下步骤执行非事务 DML 语句：

1. 选择合适的[划分列](#参数说明)。建议使用整数或字符串类型。
2. （可选）在非事务 DML 语句中添加 `DRY RUN QUERY`，手动执行查询，确认 DML 语句影响的数据范围是否大体正确。
3. （可选）在非事务 DML 语句中添加 `DRY RUN`，手动执行查询，检查拆分后的语句和执行计划。需要关注索引选择效率。
4. 执行非事务 DML 语句。
5. 如果报错，从报错信息或日志中获取具体失败的数据范围，进行重试或手动处理。

## 参数说明

| 参数 | 说明 | 默认值 | 是否必填 | 建议值 |
| :-- | :-- | :-- | :-- | :-- |
| 划分列 | 用于划分 batch 的列，例如以上非事务 DML 语句 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 中的 `id` 列  | TiDB 尝试自动选择 | 否 | 选择可以最高效地满足 `WHERE` 条件的列 |
| Batch size | 用于控制每个 batch 的大小，batch 即 DML 操作拆分成的 SQL 语句个数，例如以上非事务 DML 语句 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 中的 `LIMIT 2`。batch 数量越多，batch size 越小 | N/A | 是 | 1000～1000000，过小和过大都会导致性能下降 |

### 划分列的选择

非事务 DML 语句需要用一个列作为数据分批的标准，该列即为划分列。为获得更高的执行效率，划分列必须能够利用索引。不同的索引和划分列所导致的执行效率可能有数十倍的差别。选择划分列时，可以考虑以下建议：

- 当你对业务数据分布有一定了解时，根据 `WHERE` 条件，选择划分 batch 后，划分范围较小的列。
    - 在理想情况下，`WHERE` 条件可以利用划分列的索引，降低每个 batch 需要扫描的数据量。例如有一个交易表，记录了每一笔交易的开始和结束时间，你希望删除结束时间在一个月之前的所有交易记录。如果在交易的开始时间有索引，且已知交易的开始和结束时间通常相差不大，那么可以选择开始时间作为划分列。
    - 在不太理想的情况下：划分列的数据分布与 `WHERE` 条件完全无关，无法利用划分列的索引来减少数据扫描的范围。
- 有聚簇索引时，建议用主键作为划分列，这样语句执行效率更高（包括 `INT` 主键和 `_tidb_rowid`）。

你可以不指定划分列，TiDB 默认会使用 handle 的第一列作为划分列。但如果聚簇索引主键的第一列是非事务 DML 语句不支持的数据类型（即 `ENUM`，`BIT`，`SET`，`JSON`），TiDB 会报错。你可根据业务需要选择合适的划分列。

### Batch size 的选择

非事务 DML 语句中，batch size 越大，拆分出来的 SQL 语句越少，每个 SQL 语句执行起来越慢。最优的 batch size 依据 workload 而定。根据经验值，推荐从 50000 开始尝试。过小和过大的 batch size 都会导致执行效率下降。

每个 batch 的信息存储在内存里，因此 batch 数量过多会显著增加内存消耗。这也是 batch size 不能过小的原因之一。非事务语句用于存储 batch 信息消耗的内存上限与 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 相同，超出这个限制时触发的操作由 [`oom-action`](/tidb-configuration-file.md#oom-action) 配置项控制。

## 使用限制

非事务 DML 语句的硬性限制，不满足这些条件时 TiDB 会报错。

- 只可对单表进行操作，暂不支持多表连接。
- DML 语句不能包含 `ORDER BY` 或 `LIMIT` 字句。
- 用于拆分的列必须被索引。该索引可以是单列的索引，或是一个联合索引的第一列。
- 必须在 [`autocommit`](/system-variables.md#autocommit) 模式中使用。
- 不能在开启了 batch-dml 时使用。
- 不能在设置了 [`tidb_snapshot`](/read-historical-data.md#操作流程) 时使用。
- 不能与 `prepare` 语句一起使用。
- 划分列不支持 `ENUM`，`BIT`，`SET`，`JSON` 类型。
- 不支持用在[临时表](/temporary-tables.md)上。
- 不支持[公共表表达式](/develop/use-common-table-expression.md）。

## 控制 batch 执行失败

非事务 DML 语句不满足原子性，可能存在一些 batch 成功，一些 batch 失败的情况。系统变量 [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-从-v610-版本开始引入) 控制非事务 DML 语句处理错误的行为。

一个例外是，如果第一个 batch 就执行失败，有很大概率是语句本身有错，此时整个非事务语句会直接返回一个错误。

## 实现原理

非事务 DML 语句的实现原理，是将原本需要在用户侧手动执行的 SQL 语句拆分工作内置为 TiDB 的一个功能，简化用户操作。要理解非事务 DML 语句的行为，可以将其想象成一个用户脚本进行了如下操作：

对于非事务 DML `BATCH ON $C$ LIMIT $N$ DELETE FROM ... WHERE $P$`，其中 $C$ 为用于拆分的列，$N$ 为 batch size，$P$ 为筛选条件。

1. TiDB 根据原始语句的筛选条件 $P$，和指定的用于拆分的列 $C$，查询出所有满足 $P$ 的 $C$。对这些 $C$ 排序后按 $N$ 分成多个分组 $B_1 \dots B_k$。对所有 $B_i$，保留它的第一个和最后一个 $C$，记为 $S_i$ 和 $E_i$。这一步所执行的查询语句，可以通过 [`DRY RUN QUERY`](/non-transactional-dml.md#查询非事务-dml-语句中划分-batch-的语句) 查看。
2. $B_i$ 所涉及的数据就是满足 $P_i$: $C$ BETWEEN $S_i$ AND $E_i$ 的一个子集。可以通过 $P_i$ 来缩小每个 batch 需要处理的数据范围。
3. 对 $B_i$，将上面这个条件嵌入原始语句的 WHERE 条件，使其变为 WHERE ($P_i$) AND ($P$)。这一步的执行结果，可以通过 [`DRY RUN`](/non-transactional-dml.md#查询非事务-dml-语句中首末-batch-对应的语句) 查看。
4. 对所有 batch，依次执行新的语句。收集每个分组的错误并合并，在所有分组结束后作为整个非事务 DML 语句的结果返回。

## 与 batch-dml 的异同

batch-dml 是一种在 DML 语句执行期间将一个事务拆成多个事务提交的机制。

> **注意：**
>
> batch-dml 功能使用不当时，存在数据索引不一致风险。该功能将在 TiDB 后续版本中被废弃，因此不建议使用。

非事务 DML 语句尚不能替代所有的 batch-dml 使用场景。它们的主要区别有：

- 性能：在[划分效率](#划分列的选择)较高的情况下，非事务 DML 语句和 batch-dml 性能接近。在划分效率较低的情况下，非事务 DML 语句可能会明显慢于 batch-dml。

- 稳定性：batch-dml 极易因为使用不当导致数据索引不一致问题。而非事务 DML 语句不会导致数据索引不一致问题。但使用不当时，非事务 DML 语句与原始语句不等价，应用可能观察到和预期不符的现象。详见[常见问题](#常见问题)。

## 常见问题

### 执行时出现报错 `Failed to restore the delete statement, probably because of unsupported type of the shard column`

划分列的类型暂时不支持 `ENUM`、`BIT`、`SET`、`JSON` 类型，请尝试重新指定一个划分列。推荐使用整数或字符串类型的列。如果划分列不是这些类型，请联系 PingCAP 技术支持。

### 非事务 `DELETE` 出现和普通的 `DELETE` 不等价的“异常”行为

非事务 DML 语句和这个 DML 语句的原始形式并不等价，这可能是由以下原因导致的：

- 有并发的其它写入。
- 非事务 DML 语句修改了语句自身会读取的值。
- 在每个 batch 上实际执行的 SQL 语句由于改变了 `WHERE` 条件，可能会导致执行计划以及表达式计算顺序不同，由此导致了执行结果不一样。
- DML 语句中含有非确定性的操作。

## 兼容信息

非事务语句是 TiDB 独有的功能，与 MySQL 不兼容。

## 探索更多

* [BATCH](/sql-statements/sql-statement-batch.md) 语法
* [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-从-v610-版本开始引入)

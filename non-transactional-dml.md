---
title: 非事务 DML 语句
summary: 了解 TiDB 中的非事务 DML 语句。通过牺牲原子性和隔离性，将一个 DML 语句拆分为多个语句按顺序执行，从而提高批量数据处理场景下的稳定性和易用性。
---

# 非事务 DML 语句

本文档介绍 TiDB 中非事务 DML 语句的使用场景、使用方法和限制。此外，还说明了实现原理和常见问题。

非事务 DML 语句是将一个 DML 语句拆分成多个 SQL 语句（即多个批次）按顺序执行。它以牺牲事务的原子性和隔离性为代价，提高了批量数据处理的性能和易用性。

通常，内存消耗较大的事务需要拆分成多个 SQL 语句以绕过事务大小限制。非事务 DML 语句将这个过程集成到 TiDB 内核中以实现相同的效果。通过拆分 SQL 语句来理解非事务 DML 语句的效果会很有帮助。可以使用 `DRY RUN` 语法来预览拆分后的语句。

非事务 DML 语句包括：

- `INSERT INTO ... SELECT`
- `REPLACE INTO .. SELECT`
- `UPDATE`
- `DELETE`

详细语法请参见 [`BATCH`](/sql-statements/sql-statement-batch.md)。

> **注意：**
>
> - 非事务 DML 语句不保证语句的原子性和隔离性，且与原始 DML 语句不等价。
> - 将 DML 语句重写为非事务 DML 语句后，不能假设其行为与原始语句一致。
> - 在使用非事务 DML 之前，需要分析拆分后的语句是否会相互影响。

## 使用场景

在大数据处理场景中，你可能经常需要对大批量数据执行相同的操作。如果直接使用单个 SQL 语句执行操作，事务大小可能会超出限制并影响执行性能。

批量数据处理通常与在线应用操作在时间或数据上没有重叠。当不存在并发操作时，隔离性（ACID 中的 I）是不必要的。如果批量数据操作是幂等的或容易重试，原子性也是不必要的。如果你的应用程序既不需要数据隔离也不需要原子性，可以考虑使用非事务 DML 语句。

非事务 DML 语句用于在某些场景下绕过大事务的大小限制。使用一条语句完成原本需要手动拆分事务的任务，具有更高的执行效率和更少的资源消耗。

例如，要删除过期数据，如果你确保没有应用程序会访问过期数据，可以使用非事务 DML 语句来提高 `DELETE` 性能。

## 前提条件

在使用非事务 DML 语句之前，请确保满足以下条件：

- 语句不需要原子性，允许在执行结果中有些行被修改而有些行保持不变。
- 语句是幂等的，或者你准备根据错误消息对部分数据进行重试。如果系统变量设置为 `tidb_redact_log = 1` 和 `tidb_nontransactional_ignore_error = 1`，则此语句必须是幂等的。否则，当语句部分失败时，无法准确定位失败的部分。
- 要操作的数据没有其他并发写入，即同时不会被其他语句更新。否则，可能会出现漏写、错写、多次修改同一行等意外结果。
- 语句不修改语句本身要读取的数据。否则，后续批次将读取到前一批次写入的数据，容易造成意外结果。

    - 在非事务 `INSERT INTO ... SELECT` 语句中从同一个表中选择并修改时，避免修改分片列。否则，多个批次可能会读取同一行并多次插入数据：
        - 不建议使用 `BATCH ON test.t.id LIMIT 10000 INSERT INTO t SELECT id+1, value FROM t;`
        - 建议使用 `BATCH ON test.t.id LIMIT 10000 INSERT INTO t SELECT id, value FROM t;`
        - 如果分片列 `id` 具有 `AUTO_INCREMENT` 属性，建议使用 `BATCH ON test.t.id LIMIT 10000 INSERT INTO t(value) SELECT value FROM t;`
    - 避免在非事务 `UPDATE`、`INSERT ... ON DUPLICATE KEY UPDATE` 或 `REPLACE INTO` 语句中更新分片列：
        - 例如，对于非事务 `UPDATE` 语句，拆分的 SQL 语句按顺序执行。前一批次的修改在提交后被下一批次读取，导致同一行数据被多次修改。
        - 这些语句不支持 `BATCH ON test.t.id LIMIT 10000 UPDATE t SET test.t.id = test.t.id-1;`
        - 不建议使用 `BATCH ON test.t.id LIMIT 1 INSERT INTO t SELECT id+1, value FROM t ON DUPLICATE KEY UPDATE id = id + 1;`
    - 分片列不应该用作 Join 键。例如，以下示例使用分片列 `test.t.id` 作为 Join 键，导致非事务 `UPDATE` 语句多次修改同一行：

        ```sql
        CREATE TABLE t(id int, v int, key(id));
        CREATE TABLE t2(id int, v int, key(id));
        INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
        INSERT INTO t2 VALUES (1, 1), (2, 2), (4, 4);
        BATCH ON test.t.id LIMIT 1 UPDATE t JOIN t2 ON t.id = t2.id SET t2.id = t2.id+1;
        SELECT * FROM t2; -- (4, 1) (4, 2) (4, 4)
        ```

- 语句满足[限制条件](#限制条件)。
- 不建议对该 DML 语句要读取或写入的表执行并发 DDL 操作。

> **警告：**
>
> 如果同时启用 `tidb_redact_log` 和 `tidb_nontransactional_ignore_error`，你可能无法获得每个批次的完整错误信息，也无法仅重试失败的批次。因此，如果这两个系统变量都打开，非事务 DML 语句必须是幂等的。

## 使用示例

### 使用非事务 DML 语句

以下各节通过示例说明非事务 DML 语句的使用：

创建一个具有以下模式的表 `t`：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (id INT, v INT, KEY(id));
```

```sql
Query OK, 0 rows affected
```

向表 `t` 中插入一些数据。

{{< copyable "sql" >}}

```sql
INSERT INTO t VALUES (1, 2), (2, 3), (3, 4), (4, 5), (5, 6);
```

```sql
Query OK, 5 rows affected
```

以下操作使用非事务 DML 语句删除表 `t` 的列 `v` 上小于整数 6 的行。此语句被拆分为两个 SQL 语句，批次大小为 2，按 `id` 列分片并执行。

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6;
```

```sql
+----------------+---------------+
| number of jobs | job status    |
+----------------+---------------+
| 2              | all succeeded |
+----------------+---------------+
1 row in set
```

检查上述非事务 DML 语句的删除结果。

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

以下示例说明如何使用多表连接。首先，创建表 `t2` 并插入数据：

```sql
CREATE TABLE t2(id int, v int, key(id));
INSERT INTO t2 VALUES (1,1), (3,3), (5,5);
```

然后，通过连接表 `t` 和 `t2` 更新表 `t2` 的数据。注意需要指定分片列的完整数据库名、表名和列名（`test.t.id`）：

```sql
BATCH ON test.t._tidb_rowid LIMIT 1 UPDATE t JOIN t2 ON t.id = t2.id SET t2.id = t2.id+1;
```

查询结果：

```sql
SELECT * FROM t2;
```

```sql
+----+---+
| id | v |
+----+---+
| 1  | 1 |
| 3  | 3 |
| 6  | 5 |
+----+---+
```

### 查看执行进度

在非事务 DML 语句执行期间，可以使用 `SHOW PROCESSLIST` 查看进度。返回结果中的 `Time` 字段表示当前批次执行的时间消耗。日志和慢日志也会记录非事务 DML 执行过程中每个拆分语句的进度。例如：

{{< copyable "sql" >}}

```sql
SHOW PROCESSLIST;
```

```sql
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
| Id   | User | Host               | db     | Command | Time | State      | Info                                                                                               |
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
| 1203 | root | 100.64.10.62:52711 | test   | Query   | 0    | autocommit | /* job 506/500000 */ DELETE FROM `test`.`t1` WHERE `test`.`t1`.`_tidb_rowid` BETWEEN 2271 AND 2273 |
| 1209 | root | 100.64.10.62:52735 | <null> | Query   | 0    | autocommit | show full processlist                                                                              |
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
```

### 终止非事务 DML 语句

要终止非事务 DML 语句，可以使用 `KILL TIDB <processlist_id>`。然后 TiDB 将取消当前正在执行的批次之后的所有批次。你可以从日志中获取执行结果。

有关 `KILL TIDB` 的更多信息，请参见参考 [`KILL`](/sql-statements/sql-statement-kill.md)。

### 查询批次划分语句

在非事务 DML 语句执行期间，内部使用一个语句将 DML 语句划分为多个批次。要查询此批次划分语句，可以在此非事务 DML 语句中添加 `DRY RUN QUERY`。然后 TiDB 将不执行此查询和后续的 DML 操作。

以下语句查询执行 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 期间的批次划分语句：

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

### 查询第一个和最后一个批次对应的语句

要查询非事务 DML 语句中第一个和最后一个批次对应的实际 DML 语句，可以在此非事务 DML 语句中添加 `DRY RUN`。然后，TiDB 只划分批次而不执行这些 SQL 语句。由于可能有很多批次，不显示所有批次，只显示第一个和最后一个。

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DRY RUN DELETE FROM t WHERE v < 6;
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

### 使用优化器提示

如果 `DELETE` 语句中原本支持优化器提示，则非事务 `DELETE` 语句中也支持优化器提示。提示的位置与普通 `DELETE` 语句中的位置相同：

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DELETE /*+ USE_INDEX(t)*/ FROM t WHERE v < 6;
```

## 最佳实践

要使用非事务 DML 语句，建议按以下步骤操作：

1. 选择合适的[分片列](#参数说明)。建议使用整数或字符串类型。
2. 在非事务 DML 语句中添加 `DRY RUN QUERY`，手动执行查询，并确认 DML 语句影响的数据范围大致正确。
3. 在非事务 DML 语句中添加 `DRY RUN`，手动执行查询，并检查拆分语句和执行计划。需要注意以下几点：

    - 拆分语句是否能读取前一条语句写入的结果，这可能会导致异常。
    - 索引选择性。
    - TiDB 自动选择的分片列是否会被修改。

4. 执行非事务 DML 语句。
5. 如果报错，从错误消息或日志中获取具体失败的数据范围，重试或手动处理。

## 参数说明

| 参数 | 说明 | 默认值 | 是否必需 | 建议值 |
| :-- | :-- | :-- | :-- | :-- |
| 分片列 | 用于分片批次的列，例如上述非事务 DML 语句 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 中的 `id` 列。 | TiDB 尝试自动选择分片列（不推荐）。 | 否 | 选择能以最高效方式满足 `WHERE` 条件的列。 |
| 批次大小 | 用于控制每个批次的大小。批次数是 DML 操作被拆分成的 SQL 语句数，例如上述非事务 DML 语句 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 中的 `LIMIT 2`。批次越多，批次大小越小。 | 不适用 | 是 | 1000-1000000。批次太小或太大都会导致性能下降。 |

### 如何选择分片列

非事务 DML 语句使用一列作为数据分批的依据，即分片列。为了提高执行效率，分片列需要使用索引。不同索引和分片列带来的执行效率可能相差几十倍。选择分片列时，请考虑以下建议：

- 如果你了解应用程序的数据分布，根据 `WHERE` 条件，选择分批后数据范围较小的列。
    - 理想情况下，`WHERE` 条件可以利用分片列的索引来减少每个批次需要扫描的数据量。例如，有一个记录每个事务开始和结束时间的事务表，你想删除所有结束时间在一个月之前的事务记录。如果事务的开始时间有索引，并且事务的开始和结束时间相对接近，那么可以选择开始时间列作为分片列。
    - 不太理想的情况是，分片列的数据分布与 `WHERE` 条件完全独立，分片列的索引不能用于减少数据扫描范围。
- 当存在聚簇索引时，建议使用主键（包括 `INT` 主键和 `_tidb_rowid`）作为分片列，这样执行效率更高。
- 选择重复值较少的列。

你也可以选择不指定分片列。然后，TiDB 将默认使用 `handle` 的第一列作为分片列。但如果聚簇索引的第一列是非事务 DML 语句不支持的数据类型（即 `ENUM`、`BIT`、`SET`、`JSON`），TiDB 将报错。你可以根据应用程序需求选择合适的分片列。

### 如何设置批次大小

在非事务 DML 语句中，批次大小越大，拆分的 SQL 语句越少，每个 SQL 语句的执行速度越慢。最佳批次大小取决于工作负载。建议从 50000 开始。批次大小太小或太大都会导致执行效率降低。

每个批次的信息存储在内存中，因此太多批次会显著增加内存消耗。这就解释了为什么批次大小不能太小。非事务语句存储批次信息消耗的内存上限与 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 相同，超过此限制时触发的操作由配置项 [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610) 决定。

## 限制条件

以下是非事务 DML 语句的硬性限制。如果不满足这些限制，TiDB 将报错。

- DML 语句不能包含 `ORDER BY` 或 `LIMIT` 子句。
- 不支持子查询或集合操作。
- 分片列必须有索引。索引可以是单列索引，也可以是联合索引的第一列。
- 必须在 [`autocommit`](/system-variables.md#autocommit) 模式下使用。
- 启用 batch-dml 时不能使用。
- 设置 [`tidb_snapshot`](/read-historical-data.md) 时不能使用。
- 不能与 `prepare` 语句一起使用。
- 不支持将 `ENUM`、`BIT`、`SET`、`JSON` 类型作为分片列。
- 不支持[临时表](/temporary-tables.md)。
- 不支持[公用表表达式](/develop/dev-guide-use-common-table-expression.md)。

## 控制批次执行失败

非事务 DML 语句不满足原子性。有些批次可能成功，有些可能失败。系统变量 [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610) 控制非事务 DML 语句如何处理错误。

一个例外是，如果第一个批次失败，很可能是语句本身有错误。在这种情况下，整个非事务语句将直接返回错误。

## 工作原理

非事务 DML 语句的工作原理是将 SQL 语句的自动拆分构建到 TiDB 中。如果没有非事务 DML 语句，你需要手动拆分 SQL 语句。要理解非事务 DML 语句的行为，可以将其视为执行以下任务的用户脚本：

对于非事务 DML `BATCH ON $C$ LIMIT $N$ DELETE FROM ... WHERE $P$`，$C$ 是用于划分的列，$N$ 是批次大小，$P$ 是过滤条件。

1. 根据原始语句的过滤条件 $P$ 和指定的划分列 $C$，TiDB 查询所有满足 $P$ 的 $C$。TiDB 根据 $N$ 将这些 $C$ 分组为 $B_1 \dots B_k$。对于所有 $B_i$，TiDB 保留其第一个和最后一个 $C$ 作为 $S_i$ 和 $E_i$。可以通过 [`DRY RUN QUERY`](/non-transactional-dml.md#查询批次划分语句) 查看此步骤执行的查询语句。
2. $B_i$ 涉及的数据是满足 $P_i$ 的子集：$C$ BETWEEN $S_i$ AND $E_i$。你可以使用 $P_i$ 缩小每个批次需要处理的数据范围。
3. 对于 $B_i$，TiDB 将上述条件嵌入原始语句的 `WHERE` 条件中，使其成为 WHERE ($P_i$) AND ($P$)。可以通过 [`DRY RUN`](/non-transactional-dml.md#查询第一个和最后一个批次对应的语句) 查看此步骤的执行结果。
4. 对于所有批次，按顺序执行新语句。收集并组合每个分组的错误，在所有分组完成后作为整个非事务 DML 语句的结果返回。

## 与 batch-dml 的比较

batch-dml 是在执行 DML 语句期间将事务拆分为多个事务提交的机制。

> **注意：**
>
> 不建议使用已弃用的 batch-dml。当 batch-dml 功能使用不当时，存在数据索引不一致的风险。

非事务 DML 语句尚未替代所有 batch-dml 使用场景。它们的主要区别如下：

- 性能：当[分片列](#如何选择分片列)高效时，非事务 DML 语句的性能接近 batch-dml。当分片列效率较低时，非事务 DML 语句的性能显著低于 batch-dml。

- 稳定性：batch-dml 由于使用不当容易导致数据索引不一致。非事务 DML 语句不会导致数据索引不一致。但是，当使用不当时，非事务 DML 语句与原始语句不等价，应用程序可能会观察到意外行为。详见[常见问题部分](#非事务-delete-有不等价于普通-delete-的异常行为)。

## 常见问题

### 执行多表连接语句时出现 `Unknown column xxx in 'where clause'` 错误

当 `WHERE` 子句中连接的查询涉及除[分片列](#参数说明)定义表之外的其他表时，会出现此错误。例如，在以下 SQL 语句中，分片列是 `t2.id` 并在表 `t2` 中定义，但 `WHERE` 子句涉及表 `t2` 和 `t3`。

```sql
BATCH ON test.t2.id LIMIT 1 
INSERT INTO t 
SELECT t2.id, t2.v, t3.id FROM t2, t3 WHERE t2.id = t3.id
```

```sql
(1054, "Unknown column 't3.id' in 'where clause'")
```

如果出现错误，可以使用 `DRY RUN QUERY` 打印查询语句进行确认。例如：

```sql
BATCH ON test.t2.id LIMIT 1 
DRY RUN QUERY INSERT INTO t 
SELECT t2.id, t2.v, t3.id FROM t2, t3 WHERE t2.id = t3.id
```

要避免错误，可以将 `WHERE` 子句中与其他表相关的条件移到 `JOIN` 子句的 `ON` 条件中。例如：

```sql
BATCH ON test.t2.id LIMIT 1 
INSERT INTO t 
SELECT t2.id, t2.v, t3.id FROM t2 JOIN t3 ON t2.id = t3.id
```

```
+----------------+---------------+
| number of jobs | job status    |
+----------------+---------------+
| 0              | all succeeded |
+----------------+---------------+
```

### 实际批次大小与指定的批次大小不同

在非事务 DML 语句执行期间，最后一个批次要处理的数据大小可能小于指定的批次大小。

当**分片列中存在重复值**时，每个批次将包含该批次中分片列最后一个元素的所有重复值。因此，此批次中的行数可能大于指定的批次大小。

此外，当发生其他并发写入时，每个批次处理的行数可能与指定的批次大小不同。

### 执行时出现 `Failed to restore the delete statement, probably because of unsupported type of the shard column` 错误

分片列不支持 `ENUM`、`BIT`、`SET`、`JSON` 类型。尝试指定新的分片列。建议使用整数或字符串类型列。

<CustomContent platform="tidb">

如果在选择的分片列不是这些不支持的类型时出现错误，请从 PingCAP 或社区[获取支持](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果在选择的分片列不是这些不支持的类型时出现错误，请[联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

### 非事务 `DELETE` 有不等价于普通 `DELETE` 的异常行为

非事务 DML 语句与此 DML 语句的原始形式不等价，可能有以下原因：

- 存在其他并发写入。
- 非事务 DML 语句修改了语句本身将要读取的值。
- 每个批次执行的 SQL 语句可能因为 `WHERE` 条件改变而导致不同的执行计划和表达式计算顺序。因此，执行结果可能与原始语句不同。
- DML 语句包含非确定性操作。

## MySQL 兼容性

非事务语句是 TiDB 特有的，与 MySQL 不兼容。

## 另请参阅

* [`BATCH`](/sql-statements/sql-statement-batch.md) 语法
* [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610)

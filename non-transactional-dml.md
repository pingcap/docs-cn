---
title: Non-Transactional DML Statements
summary: Learn the non-transactional DML statements in TiDB. At the expense of atomicity and isolation, a DML statement is split into multiple statements to be executed in sequence, which improves the stability and ease of use in batch data processing scenarios.
---

# Non-Transactional DML Statements

This document describes the usage scenarios, usage methods, and restrictions of non-transactional DML statements in TiDB. In addition, the implementation principle and common issues are also explained.

A non-transactional DML statement is a DML statement split into multiple SQL statements (which is, multiple batches) to be executed in sequence. It enhances the performance and ease of use in batch data processing at the expense of transactional atomicity and isolation.

Usually, memory-consuming transactions need to be split into multiple SQL statements to bypass the transaction size limit. Non-transactional DML statements integrate this process into the TiDB kernel to achieve the same effect. It is helpful to understand the effect of non-transactional DML statements by splitting SQL statements. The `DRY RUN` syntax can be used to preview the split statements.

Non-transactional DML statements include:

- `INSERT INTO ... SELECT`
- `REPLACE INTO .. SELECT`
- `UPDATE`
- `DELETE`

For detailed syntax, see [`BATCH`](/sql-statements/sql-statement-batch.md).

> **Note:**
>
> - A non-transactional DML statement does not guarantee the atomicity and isolation of the statement, and is not equivalent to the original DML statement.
> - After a DML statement is rewritten into a non-transactional DML statement, you cannot assume that its behavior is consistent with that of the original statement.
> - Before using a non-transactional DML, you need to analyze whether the split statements will affect each other.

## Usage scenarios

In the scenarios of large data processing, you might often need to perform same operations on a large batch of data. If the operation is performed directly using a single SQL statement, the transaction size might exceed the limit and affect the execution performance.

Batch data processing often has no overlap of time or data with the online application operations. Isolation (I in ACID) is unnecessary when no concurrent operations exist. Atomicity is also unnecessary if bulk data operations are idempotent or easily retryable. If your application needs neither data isolation nor atomicity, you can consider using non-transactional DML statements.

Non-transactional DML statements are used to bypass the size limit on large transactions in certain scenarios. One statement is used to complete tasks that would otherwise require manually splitting of transactions, with higher execution efficiency and less resource consumption.

For example, to delete expired data, if you ensure that no application will access the expired data, you can use a non-transactional DML statement to improve the `DELETE` performance.

## Prerequisites

Before using non-transactional DML statements, make sure that the following conditions are met:

- The statement does not require atomicity, which permits some rows to be modified and some rows to remain unmodified in the execution result.
- The statement is idempotent, or you are prepared to retry on a part of the data according to the error message. If the system variables are set to `tidb_redact_log = 1` and `tidb_nontransactional_ignore_error = 1`, this statement must be idempotent. Otherwise, when the statement partially fails, the failed part cannot be accurately located.
- The data to be operated on has no other concurrent writes, which means it is not updated by other statements at the same time. Otherwise, unexpected results such as missing writes, wrong writes, and modifying the same line multiple times might occur.
- The statement does not modify the data to be read by the statement itself. Otherwise, the following batch will read the data written by the previous batch and easily causes unexpected results.

    - Avoid modifying the shard column when you select from and modify the same table within a non-transactional `INSERT INTO ... SELECT` statement. Otherwise, multiple batches might read the same row and insert data multiple times:
        - It is not recommended to use `BATCH ON test.t.id LIMIT 10000 INSERT INTO t SELECT id+1, value FROM t;`.
        - It is recommended to use `BATCH ON test.t.id LIMIT 10000 INSERT INTO t SELECT id, value FROM t;`.
        - If the shard column `id` has the `AUTO_INCREMENT` attribute, it is recommended to use `BATCH ON test.t.id LIMIT 10000 INSERT INTO t(value) SELECT value FROM t;`.
    - Avoid updating the shard column in the non-transactional `UPDATE`, `INSERT ... ON DUPLICATE KEY UPDATE`, or `REPLACE INTO` statement:
        - For example, for a non-transactional `UPDATE` statement, the split SQL statements are executed in sequence. The modification of the previous batch is read by the next batch after the previous batch is committed, which causes the same line of data to be modified multiple times.
        - These statements do not support `BATCH ON test.t.id LIMIT 10000 UPDATE t SET test.t.id = test.t.id-1;`.
        - It is not recommended to use `BATCH ON test.t.id LIMIT 1 INSERT INTO t SELECT id+1, value FROM t ON DUPLICATE KEY UPDATE id = id + 1;`.
    - The shard column should not be used as a Join key. For example, the following example uses the shard column `test.t.id` as a Join key, which causes a non-transactional `UPDATE` statement to modify the same line multiple times:

        ```sql
        CREATE TABLE t(id int, v int, key(id));
        CREATE TABLE t2(id int, v int, key(id));
        INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
        INSERT INTO t2 VALUES (1, 1), (2, 2), (4, 4);
        BATCH ON test.t.id LIMIT 1 UPDATE t JOIN t2 ON t.id = t2.id SET t2.id = t2.id+1;
        SELECT * FROM t2; -- (4, 1) (4, 2) (4, 4)
        ```

- The statement meets the [restrictions](#restrictions).
- It is not recommended to perform concurrent DDL operations on the table to be read or written by this DML statement.

> **Warning:**
>
> If `tidb_redact_log` and `tidb_nontransactional_ignore_error` are enabled at the same time, you might not get the complete error information of each batch, and you cannot retry the failed batch only. Therefore, if both of the system variables are turned on, the non-transactional DML statement must be idempotent.

## Usage examples

### Use a non-transactional DML statement

The following sections describe the use of non-transactional DML statements with examples:

Create a table `t` with the following schema:

{{< copyable "sql" >}}

```sql
CREATE TABLE t (id INT, v INT, KEY(id));
```

```sql
Query OK, 0 rows affected
```

Insert some data into table `t`.

{{< copyable "sql" >}}

```sql
INSERT INTO t VALUES (1, 2), (2, 3), (3, 4), (4, 5), (5, 6);
```

```sql
Query OK, 5 rows affected
```

The following operation uses a non-transactional DML statement to delete rows with values less than the integer 6 on column `v` of table `t`. This statement is split into two SQL statements, with a batch size of 2, sharded by the `id` column and executed.

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

Check the deletion results of the above non-transactional DML statement.

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

The following example describes how to use multiple table joins. First, create table `t2` and insert data:

```sql
CREATE TABLE t2(id int, v int, key(id));
INSERT INTO t2 VALUES (1,1), (3,3), (5,5);
```

Then, update the data of table `t2` by joining table `t` and `t2`. Note that you need to specify the shard column along with the complete database name, table name, and column name (`test.t.id`):

```sql
BATCH ON test.t._tidb_rowid LIMIT 1 UPDATE t JOIN t2 ON t.id = t2.id SET t2.id = t2.id+1;
```

Query the results:

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

### Check the execution progress

During the execution of a non-transactional DML statement, you can view the progress using `SHOW PROCESSLIST`. The `Time` field in the returned result indicates the time consumption of the current batch execution. Logs and slow logs also record the progress of each split statement throughout the non-transactional DML execution. For example:

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

### Terminate a non-transactional DML statement

To terminate a non-transactional DML statement, you can use `KILL TIDB <processlist_id>`. Then TiDB will cancel all batches after the batch that is currently being executed. You can get the execution result from the log.

For more information about `KILL TIDB`, see the reference [`KILL`](/sql-statements/sql-statement-kill.md).

### Query the batch-dividing statement

During the execution of a non-transactional DML statement, a statement is internally used to divide the DML statement into multiple batches. To query this batch-dividing statement, you can add `DRY RUN QUERY` to this non-transactional DML statement. Then TiDB will not execute this query and the subsequent DML operations.

The following statement queries the batch-dividing statement during the execution of `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6`:

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

### Query the statements corresponding to the first and the last batches

To query the actual DML statements corresponding to the first and the last batches in a non-transactional DML statement, you can add `DRY RUN` to this non-transactional DML statement. Then, TiDB only divides batches and does not execute these SQL statements. Because there might be many batches, not all batches are displayed, and only the first one and the last one are displayed.

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

### Use the optimizer hint

If an optimizer hint is originally supported in the `DELETE` statement, the optimizer hint is also supported in the non-transactional `DELETE` statement. The position of the hint is the same as that in the ordinary `DELETE` statement:

{{< copyable "sql" >}}

```sql
BATCH ON id LIMIT 2 DELETE /*+ USE_INDEX(t)*/ FROM t WHERE v < 6;
```

## Best practices

To use a non-transactional DML statement, the following steps are recommended:

1. Select an appropriate [shard column](#parameter-description). Integer or string types are recommended.
2. Add `DRY RUN QUERY` to the non-transactional DML statement, execute the query manually, and confirm whether the data range affected by the DML statement is roughly correct.
3. Add `DRY RUN` to the non-transactional DML statement, execute the query manually, and check the split statements and the execution plans. You need to pay attention to the following points:

    - Whether the split statement can read the result written by the previous statement, which might cause an anomaly.
    - The index selectivity.
    - Whether the shard column automatically selected by TiDB will be modified.

4. Execute the non-transactional DML statement.
5. If an error is reported, get the specific failed data range from the error message or log, and retry or handle it manually.

## Parameter description

| Parameter | Description | Default value | Required or not | Recommended value |
| :-- | :-- | :-- | :-- | :-- |
| Shard column | The column used to shard batches, such as the `id` column in the above non-transactional DML statement `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6`. | TiDB tries to automatically select a shard column (not recommended). | No | Select a column that can meet the `WHERE` condition in the most efficient way. |
| Batch size | Used to control the size of each batch. The number of batches is the number of SQL statements into which DML operations are split, such as `LIMIT 2` in the above non-transactional DML statement `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6`. The more batches, the smaller the batch size. | N/A | Yes | 1000-1000000. Too small or too large a batch will lead to performance degradation. |

### How to select a shard column

A non-transactional DML statement uses a column as the basis for data batching, which is the shard column. For higher execution efficiency, a shard column is required to use index. The execution efficiency brought by different indexes and shard columns might vary by dozens of times. When choosing the shard column, consider the following suggestions:

- If you know the application data distribution, according to the `WHERE` condition, choose the column that divides data with smaller ranges after the batching.
    - Ideally, the `WHERE` condition can take advantage of the index of the shard column to reduce the amount of data to be scanned per batch. For example, there is a transaction table that records the start and end time of each transaction, and you want to delete all transaction records whose end time is before one month. If there is an index on the start time of the transaction, and the start and end times of the transaction are relatively close, then you can choose the start time column as the shard column.
    - In a less-than-ideal case, the data distribution of the shard column is completely independent of the `WHERE` condition, and the index of the shard column cannot be used to reduce the scope of the data scan.
- When a clustered index exists, it is recommended to use the primary key (including an `INT` primary key and `_tidb_rowid`) as the shard column, so that the execution efficiency is higher.
- Choose the column with fewer duplicate values.

You can also choose not to specify a shard column. Then, TiDB will use the first column of `handle` as the shard column by default. But if the first column of the primary key of the clustered index is of a data type not supported by non-transactional DML statements (which is `ENUM`, `BIT`, `SET`, `JSON`), TiDB will report an error. You can choose an appropriate shard column according to your application needs.

### How to set batch size

In non-transactional DML statements, the larger the batch size, the fewer SQL statements are split and the slower each SQL statement is executed. The optimal batch size depends on the workload. It is recommended to start from 50000. Either too small or too large batch sizes will cause decreased execution efficiency.

The information of each batch is stored in memory, so too many batches can significantly increase memory consumption. This explains why the batch size cannot be too small. The upper limit of memory consumed by non-transactional statements for storing batch information is the same as [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), and the action triggered when this limit is exceeded is determined by the configuration item [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610).

## Restrictions

The following are hard restrictions on non-transactional DML statements. If these restrictions are not met, TiDB will report an error.

- The DML statements cannot contain `ORDER BY` or `LIMIT` clauses.
- Subqueries or set operations are not supported.
- The shard column must be indexed. The index can be a single-column index, or the first column of a joint index.
- Must be used in the [`autocommit`](/system-variables.md#autocommit) mode.
- Cannot be used when batch-dml is enabled.
- Cannot be used when [`tidb_snapshot`](/read-historical-data.md#operation flow) is set.
- Cannot be used with the `prepare` statement.
- `ENUM`, `BIT`, `SET`, `JSON` types are not supported as the shard columns.
- Not supported for [temporary tables](/temporary-tables.md).
- [Common Table Expression](/develop/dev-guide-use-common-table-expression.md) is not supported.

## Control batch execution failure

Non-transactional DML statements do not satisfy atomicity. Some batches might succeed and some might fail. The system variable [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610) controls how the non-transactional DML statements handle errors.

An exception is that if the first batch fails, there is a high probability that the statement itself is wrong. In this case, the entire non-transactional statement will directly return an error.

## How it works

The working principle of non-transactional DML statements is to build into TiDB the automatic splitting of SQL statements. Without non-transactional DML statements, you will need to manually split the SQL statements. To understand the behavior of a non-transactional DML statement, think of it as a user script doing the following tasks:

For the non-transactional DML `BATCH ON $C$ LIMIT $N$ DELETE FROM ... WHERE $P$`, $C$ is the column used for dividing, $N$ is the batch size, and $P$ is the filter condition.

1. According to the filter condition $P$ of the original statement and the specified column $C$ for dividing, TiDB queries all $C$ that satisfy $P$. TiDB sorts these $C$ into groups $B_1 \dots B_k$ according to $N$. For each of all $B_i$, TiDB keeps its first and last $C$ as $S_i$ and $E_i$. The query statement executed in this step can be viewed through [`DRY RUN QUERY`](/non-transactional-dml.md#query-the-batch-dividing-statement).
2. The data involved in $B_i$ is a subset that satisfies $P_i$: $C$ BETWEEN $S_i$ AND $E_i$. You can use $P_i$ to narrow down the range of data that each batch needs to process.
3. For $B_i$, TiDB embeds the above condition into the `WHERE` condition of the original statement, which makes it WHERE ($P_i$) AND ($P$). The execution result of this step can be viewed through [`DRY RUN`](/non-transactional-dml.md#query-the-statements-corresponding-to-the-first-and-the-last-batches).
4. For all batches, execute new statements in sequence. The errors for each grouping are collected and combined, and returned as the result of the entire non-transactional DML statement after all groupings are complete.

## Comparison with batch-dml

batch-dml is a mechanism for splitting a transaction into multiple transaction commits during the execution of a DML statement.

> **Note:**
>
> It is not recommended to use batch-dml which has been deprecated. When the batch-dml feature is not properly used, there is a risk of data index inconsistency.

Non-transactional DML statements are not yet a replacement for all batch-dml usage scenarios. Their main differences are as follows:

- Performance: When the [shard column](#how-to-select-a-shard-column) is efficient, the performance of non-transactional DML statements is close to that of batch-dml. When the shard column is less efficient, the performance of non-transactional DML statements is significantly lower than that of batch-dml.

- Stability: batch-dml is prone to data index inconsistencies due to improper use. Non-transactional DML statements do not cause data index inconsistencies. However, when used improperly, non-transactional DML statements are not equivalent to the original statements, and the applications might observe unexpected behavior. See the [common issues section](#non-transactional-delete-has-exceptional-behavior-that-is-not-equivalent-to-ordinary-delete) for details.

## Common issues

### The actual batch size is not the same as the specified batch size

During the execution of a non-transactional DML statement, the size of data to be processed in the last batch might be smaller than the specified batch size.

When **duplicated values exist in the shard column**, each batch will contain all the duplicated values of the last element of the shard column in this batch. Therefore, the number of rows in this batch might be greater than the specified batch size.

In addition, when other concurrent writes occur, the number of rows processed in each batch might be different from the specified batch size.

### The `Failed to restore the delete statement, probably because of unsupported type of the shard column` error occurs during execution

The shard column does not support `ENUM`, `BIT`, `SET`, `JSON` types. Try to specify a new shard column. It is recommended to use an integer or string type column.

<CustomContent platform="tidb">

If the error occurs when the selected shard column is not one of these unsupported types, [get support](/support.md) from PingCAP or the community.

</CustomContent>

<CustomContent platform="tidb-cloud">

If the error occurs when the selected shard column is not one of these unsupported types, [contact TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

</CustomContent>

### Non-transactional `DELETE` has "exceptional" behavior that is not equivalent to ordinary `DELETE`

A non-transactional DML statement is not equivalent to the original form of this DML statement, which might have the following reasons:

- There are other concurrent writes.
- The non-transactional DML statement modifies a value that the statement itself will read.
- The SQL statement executed in each batch might cause a different execution plan and expression calculation order because the `WHERE` condition is changed. Therefore, the execution result might be different from the original statement.
- The DML statements contain non-deterministic operations.

## MySQL compatibility

Non-transactional statements are TiDB-specific and are not compatible with MySQL.

## See also

* The [`BATCH`](/sql-statements/sql-statement-batch.md) syntax
* [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610)

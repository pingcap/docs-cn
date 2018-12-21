---
title: The Proprietary System Variables and Syntaxes in TiDB
category: user guide
---

# The Proprietary System Variables and Syntaxes in TiDB

On the basis of MySQL variables and syntaxes, TiDB has defined some specific system variables and syntaxes to optimize performance.

## System variable

Variables can be set with the `SET` statement, for example:

```sql
set @@tidb_distsql_scan_concurrency = 10
```

If you need to set the global variable, run:

```sql
set @@global.tidb_distsql_scan_concurrency = 10
```

### tidb_distsql_scan_concurrency

Scope: SESSION | GLOBAL
Default value: 10
This variable is used to set the concurrency of the `scan` operation. Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios. For OLAP scenarios, the maximum value cannot exceed the number of CPU cores of all the TiKV nodes.

### tidb_index_lookup_size

Scope: SESSION | GLOBAL
Default value: 20000
This variable is used to set the batch size of index lookup operation. Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_lookup_concurrency

Scope: SESSION | GLOBAL
Default value: 4
This variable is used to set the concurrency of the `index lookup` operation. Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_serial_scan_concurrency

Scope: SESSION | GLOBAL
Default value: 1
This variable is used to set the concurrency of the `serial scan` operation. Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

## Optimizer hint

On the basis of MySQL’s `Optimizer Hint` Syntax, TiDB adds some proprietary `Hint` syntaxes. When using the `Hint` syntax, the TiDB optimizer will try to use the specific algorithm, which performs better than the default algorithm in some scenarios.

The `Hint` syntax is included in comments like `/*+ xxx */`, and in MySQL client versions earlier than 5.7.7, the comment is removed by default. If you want to use the `Hint` syntax in these earlier versions, add the `--comments` option when starting the client. For example: `mysql -h 127.0.0.1 -P 4000 -uroot --comments`.

### TIDB_SMJ(t1, t2)

```sql
SELECT /*+ TIDB_SMJ(t1, t2) */ * from t1，t2 where t1.id = t2.id
```

This variable is used to remind the optimizer to use the `Sort Merge Join` algorithm. This algorithm takes up less memory, but takes longer to execute. It is recommended if the data size is too large, or there’s insufficient system memory.

### TIDB_INLJ(t1, t2)

```sql
SELECT /*+ TIDB_INLJ(t1, t2) */ * from t1，t2 where t1.id = t2.id
```

This variable is used to remind the optimizer to use the `Index Nested Loop Join` algorithm. In some scenarios, this algorithm runs faster and takes up fewer system resources, but may be slower and takes up more system resources in some other scenarios. You can try to use this algorithm in scenarios where the result-set is less than 10,000 rows after the outer table is filtered by the WHERE condition. The parameter in `TIDB_INLJ()` is the candidate table for the driving table (external table) when generating the query plan. That means, `TIDB_INLJ (t1)` will only consider using t1 as the driving table to create a query plan.

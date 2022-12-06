---
title: BATCH
summary: An overview of the usage of BATCH for the TiDB database.
---

# BATCH

The `BATCH` syntax splits a DML statement into multiple statements in TiDB for execution. This means that there are **no guarantees** of transactional atomicity and isolation. Therefore, it is a "non-transactional" statement.

Currently, `INSERT`, `REPLACE`, `UPDATE`, and `DELETE` are supported in `BATCH`.

Based on a column, the `BATCH` syntax divides a DML statement into multiple ranges of scope for execution. In each range, a single SQL statement is executed.

For details about the usage and restrictions, see [Non-transactional DML statements](/non-transactional-dml.md).

When you use multi-table join in a `BATCH` statement, you need to specify the full path of the column to avoid ambiguity:

```sql
BATCH ON test.t2.id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;
```

The preceding statement specifies the column to be split as `test.t2.id`, which is unambiguous. If you use the `id` as follows, an error is reported:

```sql
BATCH ON id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;

Non-transactional DML, shard column must be fully specified
```

## Synopsis

```ebnf+diagram
NonTransactionalDMLStmt ::=
    'BATCH' ( 'ON' ColumnName )? 'LIMIT' NUM DryRunOptions? ShardableStmt

DryRunOptions ::=
    'DRY' 'RUN' 'QUERY'?

ShardableStmt ::=
    DeleteFromStmt
|   UpdateStmt
|   InsertIntoStmt
|   ReplaceIntoStmt
```

## MySQL compatibility

The `BATCH` syntax is TiDB-specific and not compatible with MySQL.

## See also

* [Non-transactional DML statements](/non-transactional-dml.md)

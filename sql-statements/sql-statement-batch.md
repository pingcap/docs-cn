---
title: BATCH
summary: An overview of the usage of BATCH for the TiDB database.
---

# BATCH

The `BATCH` syntax splits a DML statement into multiple statements in TiDB for execution. This means that there are **no guarantees** of transactional atomicity and isolation. Therefore, it is a "non-transactional" statement.

Currently, only `DELETE` is supported in `BATCH`.

Based on a column, the `BATCH` syntax divides a DML statement into multiple ranges of scope for execution. In each range, a single SQL statement is executed.

For details about the usage and restrictions, see [Non-transactional DML statements](/non-transactional-dml.md).

## Synopsis

```ebnf+diagram
NonTransactionalDeleteStmt ::=
    'BATCH' ( 'ON' ColumnName )? 'LIMIT' NUM DryRunOptions? DeleteFromStmt

DryRunOptions ::=
    'DRY' 'RUN' 'QUERY'?
```

## MySQL compatibility

The `BATCH` syntax is TiDB-specific and not compatible with MySQL.

## See also

* [Non-transactional DML statements](/non-transactional-dml.md)

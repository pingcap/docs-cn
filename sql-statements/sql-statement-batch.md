---
title: BATCH
summary: TiDB 数据库中 BATCH 的使用概述。
---

# BATCH

`BATCH` 语法在 TiDB 中将一个 DML 语句拆分为多个语句执行。这意味着**不保证**事务的原子性和隔离性。因此，它是一个"非事务性"语句。

目前，`BATCH` 支持 `INSERT`、`REPLACE`、`UPDATE` 和 `DELETE` 操作。

基于一个列，`BATCH` 语法将 DML 语句划分为多个范围作用域来执行。在每个范围内，执行一个单独的 SQL 语句。

有关使用方法和限制的详细信息，请参见[非事务性 DML 语句](/non-transactional-dml.md)。

当你在 `BATCH` 语句中使用多表连接时，需要指定列的完整路径以避免歧义：

```sql
BATCH ON test.t2.id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;
```

上述语句将要拆分的列指定为 `test.t2.id`，这是没有歧义的。如果你像下面这样使用 `id`，将会报错：

```sql
BATCH ON id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;

Non-transactional DML, shard column must be fully specified
```

## 语法

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

## MySQL 兼容性

`BATCH` 语法是 TiDB 特有的，与 MySQL 不兼容。

## 另请参阅

* [非事务性 DML 语句](/non-transactional-dml.md)

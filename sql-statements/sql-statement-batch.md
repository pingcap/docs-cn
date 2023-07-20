---
title: BATCH
summary: TiDB 数据库中 BATCH 的使用概况。
---

# BATCH

BATCH 语句将一个 DML 语句拆成多个语句在内部执行，因此**不保证**事务的原子性和隔离性，是一个“非事务”语句。

目前 BATCH 语句支持 `INSERT`、`REPLACE`、`UPDATE`、`DELETE`。

BATCH 语句在某一列将 DML 语句涉及的范围划分为多个区间，在每个区间执行一条 SQL。

详细的说明和使用限制见[非事务语句](/non-transactional-dml.md)。

在涉及多表 join 时，`BATCH` 语法中指定拆分列时需要指明完整的路径以避免歧义，如：

```sql
BATCH ON test.t2.id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;
```

上面这条语句的拆分列用 `test.t2.id` 指明，不具有歧义。如果写成如下 `id` 的形式，则会报错：

```sql
BATCH ON id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;

Non-transactional DML, shard column must be fully specified
```

## 语法图

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

BATCH 语句是 TiDB 独有的语句，与 MySQL 不兼容。

## 另请参阅

* [非事务语句](/non-transactional-dml.md)

---
title: BATCH
summary: TiDB 数据库中 BATCH 的使用概况。
---

# BATCH

BATCH 语句将一个 DML 语句拆成多个语句在内部执行，因此**不保证**事务的原子性和隔离性，是一个“非事务”语句。

目前 BATCH 语句仅支持 `DELETE`。

BATCH 语句在某一列将 DML 语句涉及的范围划分为多个区间，在每个区间执行一条 SQL。

详细的说明和使用限制见[非事务语句](/non-transactional-dml.md)。

## 语法图

```ebnf+diagram
NonTransactionalDeleteStmt ::=
    'BATCH' ( 'ON' ColumnName )? 'LIMIT' NUM DryRunOptions? DeleteFromStmt

DryRunOptions ::=
    'DRY' 'RUN' 'QUERY'?
```

## MySQL 兼容性

BATCH 语句是 TiDB 独有的语句，与 MySQL 不兼容。

## 另请参阅

* [非事务语句](/non-transactional-dml.md)

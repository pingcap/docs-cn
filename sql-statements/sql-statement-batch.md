---
title: BATCH 
summary: TiDB 数据库中 BATCH 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-batch/']
---

# BATCH 

BATCH 语句将一个 DML 语句拆成多个在内部执行，因此**不保证事务的 atomicity 和 isolation 特性**，是一个“非事务”语句。

目前 BATCH 语句仅支持 DELETE。

BATCH 语句在某一列将 DML 语句涉及的范围划分为多个区间，在每个区间执行一条 SQL。

详细的说明和使用限制见 [非事务语句](/non-transactional-DML.md)。

## 语法图

```ebnf+diagram
NonTransactionalDeleteStmt ::= 
    "BATCH" ["ON" ColumnName] "LIMIT" NUM ["DRY" "RUN" ["QUERY"]] DeleteFromStmt
```

## MySQL 兼容性

BATCH 语句是 TiDB 独有的语句，与 MySQL 不兼容。

## 另请参阅

* [非事务语句](/non-transactional-DML.md)

---
title: 事务语句
category: user guide
---

# TiDB 事务语句

TiDB 支持分布式事务。涉及到事务的语句包括 `Autocommit` 变量、 `START TRANSACTION`/`BEGIN`、 `COMMIT` 以及 `ROLLBACK`。

## 自动提交
语法：
```sql
SET autocommit = {0 | 1}
```
通过设置 autocommit 的值为 1，可以将当前 Session 设置为自动提交状态，0 则表示当前 Session 为非自动提交状态。默认情况下， autocommit 的值为 1。

在自动提交状态，每条语句运行后，会将其修改自动提交到数据库中。否则，会等到运行 `COMMIT` 语句或者是 `BEGIN` 语句的时候，才会将之前的修改提交到数据库。

另外 autocommit 也是一个 System Variable，所以可以通过变量赋值语句修改当前 Session 或者是 Global 的值。
```sql
SET @@SESSION.autocommit = {0 | 1};
SET @@GLOBAL.autocommit = {0 | 1};
```


## START TRANSACTION, Begin
语法:
```sql
BEGIN;

START TRANSACTION;

START TRANSACTION WITH CONSISTENT SNAPSHOT;
```
上述三条语句都是事务开始语句，效果相同。通过事务开始语句可以显式地开始一个新的事务，如果这个时候当前 Session 正在一个事务中间过程中，会将当前事务提交后，开启一个新的事务。


## COMMIT
语法：
```sql
COMMIT;
```
提交当前事务，包括从 `BEGIN` 到 `COMMIT` 之间的所有修改。


## ROLLBACK
语法：
```sql
ROLLBACK;
```
回滚当前事务，撤销从 `BEGIN` 到 `ROLLBACK` 之间的所有修改。


## 显式事务和隐式事务
TiDB 可以显式地使用事务（`BEGIN/COMMIT`） 或者隐式的使用事务 （`SET autocommit = 1`）。

如果在 autocmmit = 1 的状态下，通过 `BEGIN` 语句开启一个新的事务，那么在 `COMMIT`/`ROLLBACK` 之前，会禁用 autocommit，也就是变成显式事务。

对于 DDL 语句，会自动提交并且不能回滚。如果运行 DDL 的时候，正在一个事务的中间过程中，会先将当前的事务提交，再运行 DDL。


## 事务隔离级别
TiDB 默认使用 `SNAPSHOT ISOLATION`，可以通过下面的语句将当前 Session 的隔离级别设置为 `READ COMMITTED`。
```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

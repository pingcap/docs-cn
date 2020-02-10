---
title: TiDB 事务概览
category: reference
---

# TiDB 事务概览

TiDB 支持完整的分布式事务。本文主要介绍涉及到事务的语句、显式/隐式事务以及事务的隔离级别和惰性检查。

常用的变量包括 `autocommit`、[`tidb_disable_txn_auto_retry`](/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_disable_txn_auto_retry) 以及 [`tidb_retry_limit`](/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_retry_limit)。

## 事务常用语句

### `BEGIN` 和 `START TRANSACTION`

语法：

{{< copyable "sql" >}}

```sql
BEGIN;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION WITH CONSISTENT SNAPSHOT;
```

以上三条语句都用于开启事务，效果相同。执行开启事务语句可以显式地开启一个新的事务。如果执行以上语句时，当前 Session 正处于一个事务的中间过程，那么系统会先自动提交当前事务，再开启一个新的事务。

### `COMMIT`

语法：

{{< copyable "sql" >}}

```sql
COMMIT;
```

该语句用于提交当前的事务，包括从 `[BEGIN|START TRANSACTION]` 到 `COMMIT` 之间的所有修改。

### `ROLLBACK`

语法：

{{< copyable "sql" >}}

```sql
ROLLBACK;
```

该语句用于回滚当前事务，撤销从 `[BEGIN|START TRANSACTION]` 到 `ROLLBACK` 之间的所有修改。

## 自动提交

语法：

{{< copyable "sql" >}}

```sql
SET autocommit = {0 | 1}
```

当 `autocommit = 1` 时（默认），当前的 Session 为自动提交状态。设置 `autocommit = 0` 时将更改当前 Session 为非自动提交状态。

自动提交状态下，每条语句运行后，TiDB 会自动将修改提交到数据库中。非自动提交状态下，通过执行 `COMMIT` 语句来手动提交事务。

> **注意：**
>
> 某些语句执行后会导致隐式提交。例如，执行 `[BEGIN|START TRANCATION]` 语句的时候，TiDB 会试图提交上一个事务，并开启一个新的事务。详情参见 [implicit commit](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)。

另外，`autocommit` 也是一个系统变量，你可以通过变量赋值语句修改当前 Session 或 Global 的值。

{{< copyable "sql" >}}

```sql
SET @@SESSION.autocommit = {0 | 1};
```

{{< copyable "sql" >}}

```sql
SET @@GLOBAL.autocommit = {0 | 1};
```

## 显式事务和隐式事务

TiDB 可以显式地使用事务 (`[BEGIN|START TRANSACTION]`/`COMMIT`) 或者隐式地使用事务 (`SET autocommit = 1`)。

在自动提交状态下，使用 `[BEGIN|START TRANSACTION]` 语句会显式地开启一个事务，同时也会禁用自动提交，使隐式事务变成显式事务。直到执行 `COMMIT` 或 `ROLLBACK` 语句时才会恢复到此前默认的自动提交状态。

对于 DDL 语句，会自动提交并且不能回滚。如果运行 DDL 的时候，正在一个事务的中间过程中，会先自动提交当前事务，再执行 DDL。

## 事务隔离级别

TiDB **只支持** `SNAPSHOT ISOLATION`，可以通过下面的语句将当前 Session 的隔离级别设置为 `READ COMMITTED`，这只是语法上的兼容，事务依旧是以 `SNAPSHOT ISOLATION` 来执行。

{{< copyable "sql" >}}

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## 事务的惰性检查

TiDB 中，对于普通的 `INSERT` 语句写入的值，会进行惰性检查。惰性检查的含义是，不在 `INSERT` 语句执行时进行唯一约束的检查，而在事务提交时进行唯一约束的检查。

举例：

{{< copyable "sql" >}}

```sql
CREATE TABLE T (I INT KEY);
INSERT INTO T VALUES (1);
BEGIN;
INSERT INTO T VALUES (1); -- MySQL 返回错误；TiDB 返回成功
INSERT INTO T VALUES (2);
COMMIT; -- MySQL 提交成功；TiDB 返回错误，事务回滚
SELECT * FROM T; -- MySQL 返回 1 2；TiDB 返回 1
```

惰性检查的意义在于，如果对事务中每个 `INSERT` 语句都立刻进行唯一性约束检查，将造成很高的网络开销。而在提交时进行一次批量检查，将会大幅提升性能。

> **注意：**
>
> 本优化仅对普通的 `INSERT` 语句生效，对 `INSERT IGNORE` 和 `INSERT ON DUPLICATE KEY UPDATE` 不会生效。

## 语句回滚

TiDB 支持语句执行的原子性回滚。在事务内部执行一个语句，遇到错误时，该语句整体不会生效。

{{< copyable "sql" >}}

```sql
begin;
insert into test values (1);
insert into tset values (2);  -- tset 拼写错误，使该语句执行出错。
insert into test values (3);
commit;
```

上面的例子里面，第二条语句执行失败，但第一和第三条语句仍然能正常提交。

{{< copyable "sql" >}}

```sql
begin;
insert into test values (1);
insert into tset values (2);  -- tset 拼写错误，使该语句执行出错。
insert into test values (3);
rollback;
```

以上例子中，第二条语句执行失败。由于调用了 `rollback`，因此事务不会将任何数据写入数据库。

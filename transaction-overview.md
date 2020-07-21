---
title: TiDB 事务概览
summary: 了解 TiDB 中的事务。
aliases: ['/docs-cn/dev/reference/transactions/overview/']
---

# TiDB 事务概览

TiDB 支持完整的分布式事务，提供[乐观事务](/optimistic-transaction.md)与[悲观事务](/pessimistic-transaction.md)（TiDB 3.0 中引入）两种事务模型。本文主要介绍涉及到常用事务的语句、显式/隐式事务、事务的隔离级别和惰性检查，以及事务大小的限制。

常用的变量包括 [`autocommit`](#自动提交)、[`tidb_disable_txn_auto_retry`](/tidb-specific-system-variables.md#tidb_disable_txn_auto_retry)、[`tidb_retry_limit`](/tidb-specific-system-variables.md#tidb_retry_limit) 以及 [`tidb_txn_mode`](/tidb-specific-system-variables.md#tidb_txn_mode)。

## 常用事务语句

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

> **注意：**
>
> 与 MySQL 不同的是，TiDB 在执行完上述语句后即会获取当前数据库快照，而 MySQL 的 `BEGIN` 和 `START TRANSACTION` 是在开启事务后的第一个从 InnoDB 读数据的 `SELECT` 语句（非 `SELECT FOR UPDATE`）后获取快照，`START TRANSACTION WITH CONSISTENT SNAPSHOT` 是语句执行时获取快照。因此，TiDB 中的 `BEGIN`、`START TRANSACTION` 和 `START TRANSACTION WITH CONSISTENT SNAPSHOT` 都等效为 MySQL 中的 `START TRANSACTION WITH CONSISTENT SNAPSHOT`。

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

当 `autocommit = 1` 时（默认），当前的 Session 为自动提交状态，即每条语句运行后，TiDB 会自动将修改提交到数据库中。设置 `autocommit = 0` 时更改当前 Session 更改为非自动提交状态，通过执行 `COMMIT` 语句来手动提交事务。

> **注意：**
>
> 某些语句执行后会导致隐式提交。例如，执行 `[BEGIN|START TRANCATION]` 语句时，TiDB 会试图提交上一个事务，并开启一个新的事务。详情参见 [implicit commit](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)。

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

TiDB 可以显式地使用事务（通过 `[BEGIN|START TRANSACTION]`/`COMMIT` 语句定义事务的开始和结束) 或者隐式地使用事务 (`SET autocommit = 1`)。

在自动提交状态下，使用 `[BEGIN|START TRANSACTION]` 语句会显式地开启一个事务，同时也会禁用自动提交，使隐式事务变成显式事务。直到执行 `COMMIT` 或 `ROLLBACK` 语句时才会恢复到此前默认的自动提交状态。

对于 DDL 语句，会自动提交并且不能回滚。如果运行 DDL 的时候，正在一个事务的中间过程中，会先自动提交当前事务，再执行 DDL。

## 惰性检查

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
> + 本优化仅在乐观事务中生效。
> + 本优化仅对普通的 `INSERT` 语句生效，对 `INSERT IGNORE` 和 `INSERT ON DUPLICATE KEY UPDATE` 不会生效。

## 语句回滚

TiDB 支持语句执行失败后的原子性回滚。在事务内部执行一个语句，遇到错误时，该语句整体不会生效。

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

以上例子中，第二条语句执行失败。由于调用了 `ROLLBACK`，因此事务不会将任何数据写入数据库。

## 事务限制

由于底层存储引擎的限制，TiDB 要求单行不超过 6 MB。可以将一行的所有列根据类型转换为字节数并加和来估算单行大小。

TiDB 同时支持乐观事务与悲观事务，其中乐观事务是悲观事务的基础。由于乐观事务是先将修改缓存在私有内存中，因此，TiDB 对于单个事务的容量做了限制。

TiDB 默认设置了单个事务的容量的总大小不超过 100 MB，这个默认值可以通过配置文件中的配置项 `txn-total-size-limit` 进行修改，最大支持到 10 GB。实际的单个事务大小限制还取决于服务器剩余可用内存大小，执行事务时 TiDB 进程的内存消耗大约是事务大小 6 倍以上。

在 4.0 以前的版本，TiDB 限制了单个事务的键值对的总数量不超过 30 万条，从 4.0 版本起 TiDB 取消了这项限制。

> **注意：**
> 
> 通常，用户会开启 TiDB Binlog 将数据向下游进行同步。某些场景下，用户会使用消息中间件来消费同步到下游的 binlog，例如 Kafka。
>
> 以 Kafka 为例，Kafka 的单条消息处理能力的上限是 1 GB。因此，当把 `txn-total-size-limit` 设置为 1 GB 以上时，可能出现事务在 TiDB 中执行成功，但下游 Kafka 报错的情况。为避免这种情况出现，请用户根据最终消费者的限制来决定 `txn-total-size-limit` 的实际大小。例如：下游使用了 Kafka，则 `txn-total-size-limit` 不应超过 1 GB。

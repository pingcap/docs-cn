---
title: TiDB 事务隔离级别
category: reference
aliases: ['/docs-cn/sql/transaction-isolation/']
---

# TiDB 事务隔离级别

事务隔离级别是数据库事务处理的基础，ACID 中 I，即 Isolation，指的就是事务的隔离性。

SQL 92 标准定义了 4 种隔离级别：读未提交、读已提交、可重复读、串行化。详见下表：

| Isolation Level  | Dirty Write  | Dirty Read   | Fuzzy Read   | Phantom      |
| ---------------- | ------------ | ------------ | ------------ | ------------ |
| READ UNCOMMITTED | Not Possible | Possible     | Possible     | Possible     |
| READ COMMITTED   | Not Possible | Not possible | Possible     | Possible     |
| REPEATABLE READ  | Not Possible | Not possible | Not possible | Possible     |
| SERIALIZABLE     | Not Possible | Not possible | Not possible | Not possible |

TiDB 实现了快照隔离 (Snapshot Isolation) 级别的一致性。为与 MySQL 保持一致，又称其为“可重复读”。该隔离级别不同于 [ANSI 可重复读隔离级别](#与-ansi-可重复读隔离级别的区别)和 [MySQL 可重复读隔离级别](#与-mysql-可重复读隔离级别的区别)。

> **注意：**
>
> 在 3.0 默认设置中，事务的自动重试已经默认关闭。关于该项功能的补充信息和应如何开启该项功能，请参考[自动重试导致的事务异常](#自动重试导致的事务异常)和[事务重试](#事务重试)。

TiDB 使用 [Percolator 事务模型](https://research.google.com/pubs/pub36726.html)，当事务启动时会获取全局读时间戳，事务提交时也会获取全局提交时间戳，并以此确定事务的执行顺序，如果想了解 TiDB 事务模型的实现可以详细阅读以下两篇文章：[TiKV 的 MVCC (Multi-Version Concurrency Control) 机制](https://pingcap.com/blog-cn/mvcc-in-tikv/)，[Percolator 和 TiDB 事务算法](https://pingcap.com/blog-cn/percolator-and-txn/)。

## 可重复读

当事务隔离级别为可重复读时，只能读到该事务启动时已经提交的其他事务修改的数据，未提交的数据或在事务启动后其他事务提交的数据是不可见的。对于本事务而言，事务语句可以看到之前的语句做出的修改。

对于运行于不同节点的事务而言，不同事务启动和提交的顺序取决于从 PD 获取时间戳的顺序。

处于可重复读隔离级别的事务不能并发的更新同一行，当时事务提交时发现该行在该事务启动后，已经被另一个已提交的事务更新过，那么该事务会回滚并启动自动重试。示例如下：

```sql
create table t1(id int);
insert into t1 values(0);

start transaction;              |               start transaction;
select * from t1;               |               select * from t1;
update t1 set id=id+1;          |               update t1 set id=id+1;
commit;                         |
                                |               commit; -- 事务提交失败，回滚
```

### 与 ANSI 可重复读隔离级别的区别

尽管名称是可重复读隔离级别，但是 TiDB 中可重复读隔离级别和 ANSI 可重复隔离级别是不同的。按照 [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf) 论文中的标准，TiDB 实现的是论文中的 Snapshot 隔离级别 (SI)。该隔离级别不会出现狭义上的幻读 (A3)，但不会阻止广义上的幻读 (P3)，同时，SI 还会出现写偏斜，而 ANSI 可重复读隔离级别不会出现写偏斜，会出现幻读。

### 与 MySQL 可重复读隔离级别的区别

MySQL 可重复读隔离级别在更新时并不检验当前版本是否可见，也就是说，即使该行在事务启动后被更新过，同样可以继续更新。这种情况在 TiDB 会导致事务回滚，导致事务最终失败，而 MySQL 是可以更新成功的。MySQL 的可重复读隔离级别并非 Snapshot 隔离级别，MySQL 可重复读隔离级别的一致性要弱于 Snapshot 隔离级别，也弱于 TiDB 的可重复读隔离级别。

## 事务重试

TiDB 默认不会进行事务重试，因为重试事务将会导致丢失更新异常。如果应用程序可以容忍事务重试带来的异常，或者说并不关注事务是否以 SI 隔离级别来执行，可以开启自动重试。通过设置 `tidb_disable_txn_auto_retry = 0` 可开启该项功能，同时要注意 `tidb_retry_limit` 的值不能为 0，否则，也会禁用自动重试。开启自动重试以后，事务遇到提交出错的可能性会降低。

## 自动重试导致的事务异常

因为 TiDB 不会[默认](#事务重试)自动重试事务，如果开启自动重试，显式的事务在遇到冲突后，可能会导致最终结果不符合预期。

比如下面这两个例子:

| Session1 | Session2   |
| ---------------- | ------------ |
| `begin;` | `begin;` |
| `select balance from t where id = 1;` | `update t set balance = balance -100 where id = 1;` |
|  | `update t set balance = balance -100 where id = 2;` |
| // 使用 select 的结果决定后续的逻辑 | `commit;` |
| `if balance > 100 {` | |
| `update t set balance = balance + 100 where id = 2;` | |
| `}` | |
| `commit;` // 自动重试 | |

| Session1 | Session2   |
| ---------------- | ------------ |
| `begin;` | `begin;` |
| `update t set balance = balance - 100  where id = 1;` | `delete from t where id = 1;` |
|  | `commit;` |
| // 使用 affected_rows 的结果决定后续的逻辑 | |
| `if affected_rows > 0 {` | |
| `update t set balance = balance + 100 where id = 2;` | |
| `}` | |
| `commit;` // 自动重试 | |

因为 TiDB 自动重试机制会把事务第一次执行的所有语句重新执行一遍，当一个事务里的后续语句是否执行取决于前面语句执行结果的时候，自动重试会违反快照隔离，导致更新丢失。这种情况下，需要在应用层重试整个事务。

通过配置 `tidb_disable_txn_auto_retry = 1` 变量可以关掉显示事务的重试。

```sql
SET GLOBAL tidb_disable_txn_auto_retry = 1;
```

改变 `tidb_disable_txn_auto_retry` 变量不会影响 `auto_commit = 1` 的单语句的隐式事务，因为该语句的自动重试，不会造成丢失更新等异常，即不会破坏事务的隔离性。

关掉显式事务重试后，如果出现事务冲突，commit 语句会返回错误，错误信息会包含 `try again later` 这个字符串，应用层可以用来判断遇到的错误是否是可以重试的。

如果事务执行过程中包含了应用层的逻辑，建议在应用层添加显式事务的重试，并关闭自动重试。

`tidb_retry_limit` 变量决定了事务重试的最大次数，默认值为 10，当它被设置为 0 时，所有事务都不会自动重试，包括自动提交的单语句隐式事务。这是彻底禁用 TiDB 中自动重试机制的方法。当用户相比于事务隔离性，更关心事务执行的延迟时，可以将它设置为 0，所有冲突的事务都会以最快的方式上报失败给应用层。

## 语句回滚

在事务内部执行一个语句，遇到错误时，该语句不会生效。

```sql
begin;
insert into test values (1);
insert into tset values (2);  // tset 拼写错了，这条语句出错。
insert into test values (3);
commit;
```

上面的例子里面，第二个语句失败，其它插入 1 和 3 仍然能正常提交。

```sql
begin;
insert into test values (1);
insert into tset values (2);  // tset 拼写错了，这条语句出错。
insert into test values (3);
rollback;
```

这个例子中，第二个语句失败，最后由于调用了 rollback，事务不会将任何数据写入数据库。

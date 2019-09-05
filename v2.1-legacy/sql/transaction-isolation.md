---
title: TiDB 事务隔离级别
category: user guide
---

# TiDB 事务隔离级别

事务隔离级别是数据库事务处理的基础，ACID 中 I，即 Isolation，指的就是事务的隔离性。

sql 92标准定义了4种隔离级别，读未提交、读已提交、可重复读、串行化，见下表。

| Isolation Level  | Dirty Read   | Nonrepeatable Read | Phantom Read          | Serialization Anomaly |
| ---------------- | ------------ | ------------------ | --------------------- | --------------------- |
| Read uncommitted | Possible     | Possible           | Possible              | Possible              |
| Read committed   | Not possible | Possible           | Possible              | Possible              |
| Repeatable read  | Not possible | Not possible       | Not possible in  TiDB | Possible              |
| Serializable     | Not possible | Not possible       | Not possible          | Not possible          |

TiDB 实现了其中的可重复读。

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
                                |               commit; --回滚并自动重试
```

### 与 ANSI 可重复读隔离级别的区别

尽管名称是可重复读隔离级别，但是 TiDB 中可重复读隔离级别和 ANSI 可重复隔离级别是不同的，按照 [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf) 论文中的标准，TiDB 实现的是论文中的 snapshot 隔离级别，该隔离级别不会出现幻读，但是会出现写偏斜，而 ANSI 可重复读隔离级别不会出现写偏斜，会出现幻读。

### 与MySQL可重复读隔离级别的区别

MySQL 可重复读隔离级别在更新时并不检验当前版本是否可见，也就是说，即使该行在事务启动后被更新过，同样可以继续更新。这种情况在 TiDB 会导致事务回滚并后台重试，重试最终可能会失败，导致事务最终失败，而 MySQL 是可以更新成功的。
MySQL 的可重复读隔离级别并非 snapshot 隔离级别，MySQL 可重复读隔离级别的一致性要弱于 snapshot 隔离级别，也弱于 TiDB 的可重复读隔离级别。

## 事务重试

对于 insert/delete/update 操作，如果事务执行失败，并且系统判断该错误为可重试，会在系统内部自动重试事务。

通过配置参数 `retry-limit` 可控制自动重试的次数：

```
[performance]
...
# The maximum number of retries when commit a transaction.
retry-limit = 10
```

## 乐观事务注意事项

因为 TiDB 使用乐观锁机制，通过显式的 `BEGIN` 语句创建的事务，在遇到冲突后自动重试可能会导致最终结果不符合预期。

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
| `if affected_rows > 100 {` | |
| `update t set balance = balance + 100 where id = 2;` | |
| `}` | |
| `commit;` // 自动重试 | |

因为 TiDB 自动重试机制会把事务第一次执行的所有语句重新执行一遍，当一个事务里的后续语句是否执行取决于前面语句执行结果的时候，自动重试无法保证最终结果符合预期。这种情况下，需要在应用层重试整个事务。

通过配置全局变量 `tidb_disable_txn_auto_retry` 可以关掉显式事务的重试。

```
set @@global.tidb_disable_txn_auto_retry = on;
```

这个变量不会影响 `auto_commit = 1` 的单语句的隐式事务，仍然会自动重试。

关掉显式事务重试后，如果出现事务冲突，commit 语句会返回错误，错误信息会包含 `try again later` 这个字符串，应用层可以用来判断遇到的错误是否是可以重试的。

如果事务执行过程中包含了应用层的逻辑，建议在应用层添加显式事务的重试，并关闭自动重试。

## 语句回滚

在事务内部执行一个语句，遇到错误时，该语句不会生效。

```
begin;
insert into test values (1);
insert into tset values (2);  // tset 拼写错了，这条语句出错。
insert into test values (3);
commit;
```

上面的例子里面，第二个语句失败，其它插入 1 和 3 仍然能正常提交。

```
begin;
insert into test values (1);
insert into tset values (2);  // tset 拼写错了，这条语句出错。
insert into test values (3);
rollback;
```

这个例子中，第二个语句失败，最后由于调用了 rollback，事务不会将任何数据写入数据库。

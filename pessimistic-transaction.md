---
title: TiDB 悲观事务模型
summary: 了解 TiDB 的悲观事务模型。
aliases: ['/docs-cn/v3.0/pessimistic-transaction/','/docs-cn/v3.0/reference/transactions/transaction-pessimistic/']
---

# TiDB 悲观事务模型

在 v3.0.8 之前，TiDB 默认使用的乐观事务模式会导致事务提交时因为冲突而失败。为了保证事务的成功率，需要修改应用程序，加上重试的逻辑。悲观事务模式可以避免这个问题，应用程序无需添加重试逻辑，就可以正常执行。

## 悲观事务的使用方法

进入悲观事务模式有以下三种方式:

- 执行 `BEGIN PESSIMISTIC;` 语句开启的事务，会进入悲观事务模式。
可以通过写成注释的形式 `BEGIN /*!90000 PESSIMISTIC */;` 来兼容 MySQL 语法。

- 执行 `set @@tidb_txn_mode = 'pessimistic';`，使这个 session 执行的所有显式事务（即非 autocommit 的事务）都会进入悲观事务模式。

- 执行 `set @@global.tidb_txn_mode = 'pessimistic';`，使之后整个集群所有新创建 session 执行的所有显示事务（即非 autocommit 的事务）都会进入悲观事务模式。

在配置了 `global.tidb_txn_mode` 为 `pessimistic` 之后，默认进入悲观事务模式，但是可以用以下三种方式使事务进入乐观事务模式：

- 执行 `BEGIN OPTIMISTIC;` 语句开启的事务，会进入乐观事务模式。
可以通过写成注释的形式 `BEGIN /*!90000 OPTIMISTIC */;` 来兼容 MySQL 语法。

- 执行 `set @@tidb_txn_mode = 'optimistic';` 或 `set @@tidb_txn_mode = '';`，使当前的 session 执行的事务进入乐观事务模式。

- 执行 `set @@global.tidb_txn_mode = 'optimistic;'` 或 `set @@global.tidb_txn_mode = '';`，使之后整个集群所有新创建 session 执行的事务都进入乐观事务模式。

`BEGIN PESSIMISTIC;` 和 `BEGIN OPTIMISTIC;` 语句的优先级高于 `tidb_txn_mode` 系统变量。使用这两个语句开启的事务，会忽略系统变量，从而支持悲观、乐观事务混合使用。

如果想要禁用悲观事务特性，可以修改 TiDB 配置文件，在 `[pessimistic-txn]` 类别下添加 `enable = false`。

## 悲观事务模式的行为

悲观事务的行为和 MySQL 基本一致（不一致之处详见[和 MySQL InnoDB 的差异](#和-mysql-innodb-的差异)）：

- `SELECT FOR UPDATE` 会读取已提交的最新数据，并对读取到的数据加悲观锁。

- `UPDATE`、`DELETE` 和 `INSERT` 语句都会读取已提交的最新的数据来执行，并对修改的数据加悲观锁。

- 当一行数据被加了悲观锁以后，其他尝试修改这一行的写事务会被阻塞，等待悲观锁的释放。

- 当一行数据被加了悲观锁以后，其他尝试读取这一行的事务不会被阻塞，可以读到已提交的数据。

- 事务提交或回滚的时候，会释放所有的锁。

- 当有多个事务同时等待同一个锁释放时，会尽可能按照事务 start ts 顺序获取锁，但不能严格保证。

- 如果并发事务出现死锁，会被死锁检测器检测到，随机终止掉其中一个事务并返回兼容 MySQL 的错误码 `1213`。

- 乐观事务和悲观事务可以共存，事务可以任意指定使用乐观模式或悲观模式来执行。

- 通过设置 `innodb_lock_wait_timeout` 变量，设置等锁超时时间，等锁超时后返回兼容 MySQL 的错误码 `1205`。

## 和 MySQL InnoDB 的差异

1. TiDB 使用 range 作为 WHERE 条件，执行 DML 和 `SELECT FOR UPDATE` 语句时不会阻塞范围内并发的 `INSERT` 语句的执行。

    InnoDB 通过实现 gap lock，支持阻塞 range 内并发的 `INSERT` 语句的执行，其主要目的是为了支持 statement based binlog，因此有些业务会通过将隔离级别降低至 READ COMMITTED 来避免 gap lock 导致的并发性能问题。TiDB 不支持 gap lock，也就不需要付出相应的并发性能的代价。

2. TiDB 不支持 `SELECT LOCK IN SHARE MODE`。

    使用这个语句执行的时候，效果和没有加锁是一样的，不会阻塞其他事务的读写。

3. DDL 可能会导致悲观事务提交失败。

    MySQL 在执行 DDL 时会被正在执行的事务阻塞住，而在 TiDB 中 DDL 操作会成功，造成悲观事务提交失败：`ERROR 1105 (HY000): Information schema is changed. [try again later]`。

4. `START TRANSACTION WITH CONSISTENT SNAPSHOT` 之后，MySQL 仍然可以读取到之后在其他事务创建的表，而 TiDB 不能。

5. autocommit 事务不支持悲观锁

    所有自动提交的语句都不会加悲观锁，该类语句在用户侧感知不到区别，因为悲观事务的本质是把整个事务的重试变成了单个 DML 的重试，autocommit 事务即使在 TiDB 关闭重试时也会自动重试，效果和悲观事务相同。

    自动提交的 select for update 语句也不会等锁。

## 常见问题

1. TiDB 日志出现 `pessimistic write conflict, retry statement`。

    当发生 write conflict 时，乐观事务会直接终止，而悲观事务会尝试用最新数据重试该语句直到没有 write conflict，每次重试都会打印该 log，不用特别关注。

2. 执行 DML 时报错 `pessimistic lock retry limit reached`。

    悲观事务每个语句有重试次数限制，当因 write conflict 重试超过该限制时会报该错误，默认为 256 次，可通过 TiDB 配置文件 `[pessimistic-txn]` 类别下的 `max-retry-limit` 修改。

3. 悲观事务执行时间限制。

    除了有事务执行时间不能超出 `tikv_gc_life_time` 的限制外，悲观事务的 TTL 有 10 分钟上限，所以执行时间超过 10 分钟的悲观事务有可能提交失败。

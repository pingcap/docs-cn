---
title: TiDB 悲观事务模式
category: reference
---

# TiDB 悲观事务模式

TiDB 默认使用乐观事务模式，存在事务提交时因为冲突而失败的问题。为了保证事务的成功率，需要修改应用程序，加上重试的逻辑。
悲观事务模式可以避免这个问题，应用程序无需添加重试逻辑，就可以正常执行。

## 悲观事务模式的行为

悲观事务的行为和 MySQL 基本一致（不一致之处详见[和 MySQL InnoDB 的差异](#和-mysql-innodb-的差异)）：

- `SELECT FOR UPDATE` 会读取已提交的最新数据，并对读取到的数据加悲观锁。

- `UPDATE`、`DELETE` 和 `INSERT` 语句都会读取已提交的最新的数据来执行，并对修改的数据加悲观锁。

- 当一行数据被加了悲观锁以后，其他尝试修改这一行的写事务会被阻塞，等待悲观锁的释放。

- 当一行数据被加了悲观锁以后，其他尝试读取这一行的事务不会被阻塞，可以读到已提交的数据。

- 事务提交或回滚的时候，会释放所有的锁。

- 如果并发事务出现死锁，会被死锁检测器检测到，并返回兼容 MySQL 的错误码 `1213`。

- 乐观事务和悲观事务可以共存，事务可以任意指定使用乐观模式或悲观模式来执行。

- 通过设置 `innodb_wait_timeout` 变量 <span class="version-mark">从 v3.0.6 开始引入</span>，设置等锁超时时间，等锁超时后返回兼容 MySQL 的错误码 `1205`。

## 悲观事务的使用方法

进入悲观事务模式有以下三种方式:

- 执行 `BEGIN PESSIMISTIC;` 语句开启的事务，会进入悲观事务模式。
可以通过写成注释的形式 `BEGIN /*!90000 PESSIMISTIC */;` 来兼容 MySQL 语法。

- 执行 `set @@tidb_txn_mode = 'pessimistic';`，使这个 session 执行的所有显式事务（即非 autocommit 的事务）都会进入悲观事务模式。

- 执行 `set @@global.tidb_txn_mode = 'pessimistic';`，使之后整个集群所有新创建的 session 都会进入悲观事务模式执行显式事务。

在配置了 `global.tidb_txn_mode` 为 `pessimistic` 之后，默认进入悲观事务模式，但是可以用以下两种方式使事务进入乐观事务模式：

- 执行 `BEGIN OPTIMISTIC;` 语句开启的事务，会进入乐观事务模式。
可以通过写成注释的形式 `BEGIN /*!90000 OPTIMISTIC */;` 来兼容 MySQL 语法。

- 执行 `set @@tidb_txn_mode = 'optimistic';`，使当前的 session 执行的事务进入乐观事务模式。

`BEGIN PESSIMISTIC;` 和 `BEGIN OPTIMISTIC;` 语句的优先级高于 `tidb_txn_mode` 系统变量。使用这两个语句开启的事务，会忽略系统变量。

如果想要禁用悲观事务特性，可以修改配置文件，在 `[pessimistic-txn]` 类别下添加 `enable = false`.

## 和 MySQL InnoDB 的差异

1. TiDB 使用 range 作为 WHERE 条件，执行 DML 和 `SELECT FOR UPDATE` 语句时不会阻塞范围内并发的 `INSERT` 语句的执行。

    InnoDB 通过实现 gap lock，支持阻塞 range 内并发的 `INSERT` 语句的执行，其主要目的是为了支持 statement based binlog，因此有些业务会通过将隔离级别降低至 READ COMMITTED 来避免 gap lock 导致的并发性能问题。TiDB 不支持 gap lock，也就不需要付出相应的并发性能的代价。

2. TiDB 不支持 `SELECT LOCK IN SHARE MODE`。

    使用这个语句执行的时候，效果和没有加锁是一样的，不会阻塞其他事务的读写。

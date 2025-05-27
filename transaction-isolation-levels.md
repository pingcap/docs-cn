---
title: TiDB 事务隔离级别
summary: 了解 TiDB 事务的隔离级别。
aliases: ['/docs-cn/dev/transaction-isolation-levels/','/docs-cn/dev/reference/transactions/transaction-isolation/']
---

# TiDB 事务隔离级别

事务隔离级别是数据库事务处理的基础，[ACID](/glossary.md#acid) 中的 "I"，即 Isolation，指的就是事务的隔离性。

SQL-92 标准定义了 4 种隔离级别：读未提交 (READ UNCOMMITTED)、读已提交 (READ COMMITTED)、可重复读 (REPEATABLE READ)、串行化 (SERIALIZABLE)。详见下表：

| Isolation Level  | Dirty Write  | Dirty Read   | Fuzzy Read   | Phantom      |
| ---------------- | ------------ | ------------ | ------------ | ------------ |
| READ UNCOMMITTED | Not Possible | Possible     | Possible     | Possible     |
| READ COMMITTED   | Not Possible | Not possible | Possible     | Possible     |
| REPEATABLE READ  | Not Possible | Not possible | Not possible | Possible     |
| SERIALIZABLE     | Not Possible | Not possible | Not possible | Not possible |

TiDB 实现了快照隔离 (Snapshot Isolation, SI) 级别的一致性。为与 MySQL 保持一致，又称其为“可重复读” (REPEATABLE READ)。该隔离级别不同于 [ANSI 可重复读隔离级别](#与-ansi-可重复读隔离级别的区别)和 [MySQL 可重复读隔离级别](#与-mysql-可重复读隔离级别的区别)。

> **注意：**
>
> 在 TiDB v3.0 中，事务的自动重试功能默认为禁用状态。不建议开启自动重试功能，因为可能导致**事务隔离级别遭到破坏**。更多关于事务自动重试的文档说明，请参考[事务重试](/optimistic-transaction.md#重试机制)。
>
> 从 TiDB [v3.0.8](/releases/release-3.0.8.md#tidb) 版本开始，新创建的 TiDB 集群会默认使用[悲观事务模式](/pessimistic-transaction.md)，悲观事务中的当前读（for update 读）为**不可重复读**，关于悲观事务使用注意事项，请参考[悲观事务模式](/pessimistic-transaction.md)

## 可重复读隔离级别 (Repeatable Read)

TiDB 的可重复读隔离级别基于快照隔离 (Snapshot Isolation, SI) 实现，行为会根据事务模式（乐观事务或悲观事务）有所不同。

### 乐观事务中的可重复读

在乐观事务模式下，TiDB 的可重复读隔离级别提供以下特性：

#### 读取特性

- **快照一致性**：事务只能读到该事务启动时已经提交的其他事务修改的数据
- **事务内一致性**：事务语句可以看到之前的语句在本事务内做出的修改
- **时间戳确定性**：事务的 `start_ts` 在事务开始时确定，所有读操作都使用这个时间戳

#### 写冲突检测

- **提交时检测**：当事务提交时，会检查是否存在写冲突
- **回滚重试**：如果发现该行在事务启动后被其他已提交事务更新过，当前事务会回滚
- **重试机制**：在满足条件时，事务可能会自动重试（不推荐开启）

#### 示例行为

```sql
-- 乐观事务示例
create table t1(id int);
insert into t1 values(0);

-- 事务 A                           -- 事务 B
start transaction;                 start transaction;
select * from t1;                  select * from t1;
update t1 set id=id+1;             update t1 set id=id+1;
commit;                            commit; -- 会失败并回滚
```

### 悲观事务中的可重复读

在悲观事务模式下，TiDB 的可重复读隔离级别行为更接近 MySQL：

#### 读取特性

- **快照读一致性**：普通的 `SELECT` 语句读取事务开始时的快照
- **当前读更新**：`SELECT FOR UPDATE`、`UPDATE`、`DELETE` 等 DML 操作会读取最新已提交的数据
- **ForUpdate 时间戳**：DML 操作使用单独的 `for_update_ts` 时间戳，确保读取最新数据

#### 锁机制

- **即时加锁**：写操作会立即对相关行加悲观锁
- **锁等待**：当多个事务并发更新同一行时，后执行的事务会等待锁释放
- **避免回滚**：通过预先加锁，大大减少了事务提交时的冲突

#### 示例行为

```sql
-- 悲观事务示例
create table t1(id int);
insert into t1 values(0);

-- 事务 A                           -- 事务 B
start transaction;                 start transaction;
select * from t1;                  select * from t1;
update t1 set id=id+1;             update t1 set id=id+1; -- 会等待事务 A 的锁
commit;                            commit; -- 可以成功提交

### 事务启动和时间戳机制

对于运行于不同节点的事务而言，不同事务启动和提交的顺序取决于从 PD 获取时间戳的顺序。

#### 乐观事务

- 事务开始时获取 `start_ts`
- 所有读操作使用 `start_ts`
- 提交时获取 `commit_ts` 并检查冲突

#### 悲观事务

- 事务开始时获取 `start_ts`
- 普通读操作使用 `start_ts`
- DML 操作获取新的 `for_update_ts` 并使用该时间戳读取最新数据
- 提交时使用两阶段提交协议

### 并发更新处理

两种事务模式在处理并发更新冲突时有着不同的机制：

#### 乐观事务的并发更新行为

乐观事务使用延迟冲突检测机制，在事务执行期间不会获取任何锁。具体行为如下：

- **执行阶段**：允许多个事务并发执行 DML 操作，彼此不受干扰
- **冲突检测**：冲突检测发生在提交阶段（prewrite 阶段）
- **冲突处理**：当事务提交时发现该行在该事务启动后已经被另一个已提交的事务更新过（`data.commit_ts > txn.start_ts`），当前事务会自动回滚
- **重试机制**：如果开启了自动重试，事务会在限定次数内重试（不推荐开启）

这种机制在代码中体现为使用固定的 `start_ts` 进行读取，并在提交时进行写写冲突检测。

#### 悲观事务的并发更新行为

悲观事务使用即时加锁机制，在执行 DML 操作时立即获取锁。具体行为如下：

- **即时加锁**：DML 操作（`UPDATE`、`DELETE`、`SELECT FOR UPDATE` 等）执行时立即对相关行加悲观锁
- **锁等待机制**：处于可重复读隔离级别的悲观事务在更新同一行时，后执行的事务会等待获取锁，直到持有锁的事务提交或回滚释放行锁后才能继续执行
- **超时控制**：事务等待锁的时间由 `innodb_lock_wait_timeout` 参数控制（默认 50 秒），超时后返回错误码 `1205`
- **避免冲突**：通过预先加锁，避免了提交时的冲突检测和回滚

这种机制确保了在可重复读隔离级别下，同一行数据不会被多个事务同时修改，提供了更好的并发控制。

### 与 ANSI 可重复读隔离级别的区别

尽管名称是可重复读隔离级别，但是 TiDB 中可重复读隔离级别和 ANSI 可重复隔离级别是不同的。按照 [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf) 论文中的标准，TiDB 实现的是论文中的快照隔离级别。该隔离级别不会出现狭义上的幻读 (A3)，但不会阻止广义上的幻读 (P3)，同时，快照隔离还会出现写偏斜，而 ANSI 可重复读隔离级别不会出现写偏斜，会出现幻读。

### 与 MySQL 可重复读隔离级别的区别

#### 乐观事务与 MySQL 的区别

MySQL 可重复读隔离级别在更新时并不检验当前版本是否可见，也就是说，即使该行在事务启动后被更新过，同样可以继续更新。这种情况在 TiDB 使用乐观事务时会导致事务回滚，可能导致事务最终失败。

#### 悲观事务与 MySQL 的相似性

TiDB 默认的悲观事务和 MySQL 行为基本一致，都可以在行被其他事务更新后继续更新成功。主要区别在于：

- **读取行为**：TiDB 悲观事务中，DML 操作基于最新已提交数据执行，与 MySQL 行为相同，但与 TiDB 乐观事务模式不同
- **锁等待**：两者都支持锁等待机制
- **事务重试**：TiDB 支持更灵活的事务重试机制

## 读已提交隔离级别 (Read Committed)

从 TiDB [v4.0.0-beta](/releases/release-4.0.0-beta.md#tidb) 版本开始，TiDB 支持使用 Read Committed 隔离级别。由于历史原因，当前主流数据库的 Read Committed 隔离级别本质上都是 Oracle 定义的[一致性读隔离级别](https://docs.oracle.com/cd/B19306_01/server.102/b14220/consist.htm)。TiDB 为了适应这一历史原因，悲观事务中的 Read Committed 隔离级别的实质行为也是一致性读。

> **注意：**
>
> Read Committed 隔离级别仅在[悲观事务模式](/pessimistic-transaction.md)下生效。在[乐观事务模式](/optimistic-transaction.md)下设置事务隔离级别为 Read Committed 将不会生效，事务将仍旧使用可重复读隔离级别。

从 v6.0.0 版本开始，TiDB 支持使用系统变量 [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-从-v600-版本开始引入) 对读写冲突较少情况下优化时间戳的获取。开启此变量后，`SELECT` 语句会尝试使用前一个有效的时间戳进行数据读取，初始值为事务的 `start_ts`。

- 如果整个读取过程没有遇到更新的数据版本，则返回结果给客户端且 `SELECT` 语句执行成功。
- 如果读取过程中遇到更新的数据版本：
    - 如果当前 TiDB 尚未向客户端回复数据，则尝试重新获取一个新的时间戳重试此语句。
    - 如果 TiDB 已经向客户端返回部分数据，则 TiDB 会向客户端报错。每次向客户端回复的数据量受 `tidb_init_chunk_size` 和 `tidb_max_chunk_size` 控制。

在使用 `READ-COMMITTED` 隔离级别且单个事务中 `SELECT` 语句较多、读写冲突较少的场景，可通过开启此变量来避免获取全局 timestamp 带来的延迟和开销。

从 v6.3.0 版本开始，TiDB 支持通过开启系统变量 [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-从-v630-版本开始引入) 对点写冲突较少情况下优化时间戳的获取。开启此变量后，点写语句会尝试使用当前事务有效的时间戳进行数据读取和加锁操作，且在读取数据时按照开启 [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-从-v600-版本开始引入) 的方式读取数据。目前该变量适用的点写语句包括 `UPDATE`、`DELETE`、`SELECT ...... FOR UPDATE` 三种类型。点写语句是指将主键或者唯一键作为过滤条件且最终执行算子包含 `POINT-GET` 的写语句。目前这三种点写语句的共同点是会先根据 key 值做点查，如果 key 存在再加锁，如果不存在则直接返回空集。

- 如果点写语句的整个读取过程中没有遇到更新的数据版本，则继续使用当前事务的时间戳进行加锁。
    - 如果加锁过程中遇到因时间戳旧而导致写冲突，则重新获取最新的全局时间戳进行加锁。
    - 如果加锁过程中没有遇到写冲突或其他错误，则加锁成功。
- 如果读取过程中遇到更新的数据版本，则尝试重新获取一个新的时间戳重试此语句。

在使用 `READ-COMMITTED` 隔离级别且单个事务中点写语句较多、点写冲突较少的场景，可通过开启此变量来避免获取全局时间戳带来的延迟和开销。

### 与 MySQL Read Committed 隔离级别的区别

MySQL 的 Read Committed 隔离级别大部分符合一致性读特性，但其中存在某些特例，如半一致性读 ([semi-consistent read](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html))，TiDB 没有兼容这个特殊行为。

## 查看和修改事务隔离级别

你可以通过以下方式查看和修改事务隔离级别。

查看当前会话的事务隔离级别：

```sql
SHOW VARIABLES LIKE 'transaction_isolation';
```

修改当前会话的事务隔离级别：

```sql
SET SESSION transaction_isolation = 'READ-COMMITTED';
```

关于事务隔离级别的配置和使用说明，请参考：

- [系统变量 `transaction_isolation`](/system-variables.md#transaction_isolation)
- [事务模式](/pessimistic-transaction.md#隔离级别)
- [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md)

## 更多阅读

- [TiDB 的乐观事务模型](https://pingcap.com/blog-cn/best-practice-optimistic-transaction/)
- [TiDB 新特性漫谈-悲观事务](https://pingcap.com/blog-cn/pessimistic-transaction-the-new-features-of-tidb/)
- [TiDB 新特性-白话悲观锁](https://pingcap.com/blog-cn/tidb-4.0-pessimistic-lock/)
- [TiKV 的 MVCC (Multi-Version Concurrency Control) 机制](https://pingcap.com/blog-cn/mvcc-in-tikv/)

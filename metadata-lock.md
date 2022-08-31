---
title: 元数据锁
---

# 元数据锁

本文介绍了 TiDB 中的元数据锁。

## 元数据锁的概念

在 TiDB 中，对元数据对象的更改采用的是 F1 论文中的在线异步变更算法。事务在执行时会获取开始时对应的元数据快照。如果事务执行过程中相关表上发生了元数据的更改，为了保证数据的一致性，TiDB 会返回 Information schema is changed 的错误。
为了解决这个问题，在 6.3 版本中，TiDB 引入元数据锁这一特性，对 DML 语句和 DDL 语句的执行进行协调，最大程度上避免了 DML 语句报错的问题。

## 元数据锁的原理

一个 DDL 语句在执行过程中需要进行多次状态变更，而在元数据线异步变更的算法要求集群中事务提交所采用的元数据版本最多相差一个版本。
以加索引为例，其状态会经历 None-> Delete Only, Delete Only -> Write Only, Write Only -> Write Reorg, Write Reorg -> Public 这四个变化。

那么以下的提交流程将违反这一约束：

txn1: None

txn2: DeleteOnly

txn3: WriteOnly

txn4: None

txn5: Write Reorg

txn6: WriteOnly

txn7: Public

其中 `txn4` 提交时采用的元数据版本与 `txn3` 提交时采用的元数据版本相差了两个版本，会导致正确性问题。

在引入元数据锁后，会保证整个 TiDB 集群中的所有事务所用的元数据版本最多相差一个版本。为此：

执行 DML 语句时，TiDB 会在事务上下文中记录下该 DML 语句访问的元数据对象，例如表、视图，以及对应的元数据版本。事务提交时会清空这些记录。

执行 DDL 语句进行状态变更时，会往所有的 TiDB 节点推送新版本的元数据。如果一个 TiDB 节点上所有的与这次状态变更相关的旧事务都以及提交，我们称这个 TiDB 获得了该元数据对象的元数据锁。
当集群中的所有 TiDB 节点都获取了该元数据对象的元数据锁后，才能进行下一次状态变更。

## 元数据锁的影响

对于 DML 语句来说，元数据锁不会导致 DML 语句被阻塞，因此也不会存在死锁的问题。

开启元数据锁后，在事务中某个元数据对象的元数据信息在第一次访问时确定，之后不再变化。

对于 DDL 语句来说，在进行元数据状态变更时，会被涉及相关元数据的旧事务所阻塞。

例如以下的执行流程：

| session 1                                                 | session 2                                       |
|:----------------------------------------------------------|:------------------------------------------------|
| CREATE TABLE t (a INT);                                   |                                                 |
| INSERT INTO T VALUES(1);                                  |                                                 | 
| BEGIN;                                                    |                                                 |  
|                                                           | ALTER TABLE t ADD COLUMN b INT                  |           
| SELECT * FROM t;  采用 t 表当前的元数据版本，返回(a=1，b=NULL)，同时给表 t 上锁 |                                                 |
 |                                                           | ALTER TABLE t ADD COLUMN c INT (被 session 1 阻塞) |

在可重复读隔离级别下，如果事务开始到确定一个表的元数据过程中，执行了加索引或者列类型变更这类需要更改数据的 DDL。则有以下表现：
 
| session 1                                           | session 2                                       |
|:----------------------------------------------------|:------------------------------------------------|
| CREATE TABLE t (a INT);                             |                                                 |
| INSERT INTO T VALUES(1);                            |                                                 |
| BEGIN;                                              |                                                 |
|                                                     | ALTER TABLE t ADD INDEX idx(a)                  |
| SELECT * FROM t; (索引 idx 不可用)                       |                                                 |
| COMMIT;                                             |                                                 |
| BEGIN;                                              |                                                 | 
|                                                     | ALTER TABLE t MODIFY COLUMN a CHAR(10)          |
| SELECT * FROM t; (报错 Information schema is changed) |                                                 |

## 不需要加元数据锁的场景

并不是所有的 DML 语句都需要加元数据锁，例如：

+ Autocommit 的查询语句
+ 开启了 Stale Read
+ 访问临时表

## DDL 阻塞的排查

TiDB 在 6.3 版本中引入了一个视图 `mysql.tidb_ddl_lock`, 可以用于查看当前阻塞的 DDL 的相关信息。

以元数据锁的影响小节中 session2 的语句 `ALTER TABLE t ADD COLUMN c INT` 为例。

```sql
select * from mysql.tidb_ddl_lock\G
*************************** 1. row ***************************
    JOB_ID: 141
   DB_NAME: test
TABLE_NAME: t
     QUERY: ALTER TABLE t ADD COLUMN c INT
SESSION ID: 2199023255957
  TxnStart: 08-30 16:35:41.313(435643624013955072)
1 row in set (0.02 sec)
```

从以上的结果中，我们可以知道这个 DDL 是被 ID 为 2199023255957 的 session
 给阻塞了。我们可以通过 Global Kill 命令将其杀死，然后 DDL 便能继续执行下去：

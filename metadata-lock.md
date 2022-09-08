---
title: 元数据锁
---

# 元数据锁

本文介绍了 TiDB 中的元数据锁。

## 元数据锁的概念

在 TiDB 中，对元数据对象的更改采用的是 F1 论文中的在线异步变更算法。事务在执行时会获取开始时对应的元数据快照。如果事务执行过程中相关表上发生了元数据的更改，为了保证数据的一致性，TiDB 会返回 Information schema is changed 的错误，导致用户事务提交失败。
为了解决这个问题，在 v6.3 版本中，TiDB 在 Online DDL 算法中引入了元数据锁特性，通过协调表元数据变更过程中  DML 语句和 DDL 语句的优先级，让执行中的 DDL 语句等待持有旧版本元数据的 DML 语句提交，尽可能避免 DML 语句报错。

## 元数据锁的原理

### 背景

TiDB 中实现的是 Online DDL 的模式，一个 DDL 语句在执行过程中需要修改定义的对象元数据版本需要进行多次小版本变更，而元数据在线异步变更的算法只论证了相邻的两个小版本之间是兼容的（即用户在相邻的两个版本间做操作，对于DDL 变更对象所存储的数据一致性是不会产生破坏的）。
以针对 t1 表加索引 idx1 为例，其状态会经历 None-> Delete Only, Delete Only -> Write Only, Write Only -> Write Reorg, Write Reorg -> Public 这四个变化。

那么以下的提交流程将违反这一约束：

| 事务   | 所用的版本      | 集群最新版本     | 版本差 |
|:-----|:-----------|:-----------|:----|
| txn1 | None       | None       | 0   |
| txn2 | DeleteOnly | DeleteOnly | 0   |
| txn3 | WriteOnly  | WriteOnly  | 0   |
| txn4 | None       | WriteOnly  | 2   |
| txn5 | WriteReorg | WriteReorg | 0   |
| txn6 | WriteOnly  | WriteReorg | 1   |
| txn7 | Public     | Public     | 0   |

其中 `txn4` 提交时采用的元数据版本与集群中最新的元数据版本相差了两个版本，会导致正确性问题。

### 元数据锁的实现

在引入元数据锁后，会保证整个 TiDB 集群中的所有事务所用的元数据版本最多相差一个版本。为此：

执行 DML 语句时，TiDB 会在事务上下文中记录下该 DML 语句访问的元数据对象，例如表、视图，以及对应的元数据版本。事务提交时会清空这些记录。

执行 DDL 语句进行状态变更时，会往所有的 TiDB 节点推送新版本的元数据。如果一个 TiDB 节点上所有的与这次状态变更所有事务使用的状态与当前状态版本之差 < 2，我们称这个 TiDB 获得了该元数据对象的元数据锁。当集群中的所有 TiDB 节点都获取了该元数据对象的元数据锁后，才能进行下一次状态变更。

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
| SELECT * FROM t;  
|#采用 t 表当前的元数据版本，返回(a=1，b=NULL)，同时给表 t 上锁  |                                                                                   
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

## TiDB MDL 优化
因为增加了 MDL 锁机制，会给 TiDB DDL 任务的执行带来一定的性能影响，为了降低 MDL 对于 DDL 任务的影响，在分析完成 DML 事务的特征之后，梳理出来一些不需要添加 MDL 锁的场景
### 不需要加元数据锁的场景

并不是所有的 DML 语句都需要加元数据锁，例如：

+ Autocommit 的查询语句
+ 开启了 Stale Read
+ 访问临时表

## 启用元数据锁

使用系统变量 [`tidb_enable_mdl`](/system-variables.md#tidb_enable_mdl-从-v630-版本开始引入) 启动或者关闭元数据锁特性。

## DDL 阻塞的排查

TiDB 在 v6.3 版本中引入了 `mysql.tidb_ddl_lock` 视图，可以用于查看当前阻塞的 DDL 的相关信息。

以给表 `t` 添加索引为例，假设有 DDL 语句 `ALTER TABLE t ADD INDEX idx(a)`：

```sql
SELECT * FROM mysql.tidb_ddl_lock\G
*************************** 1. row ***************************
    JOB_ID: 141
   DB_NAME: test
TABLE_NAME: t
     QUERY: ALTER TABLE t ADD INDEX idx(a)
SESSION ID: 2199023255957
  TxnStart: 08-30 16:35:41.313(435643624013955072)
SQL_DIGESTS: ["begin","select * from `t`"]
1 row in set (0.02 sec)
```

> **注意：**
>
> 查询这个视图需要有 `PROCESS` 权限。

这时我们可以从结果了解到有一个 SESSION ID 为 2199023255957 的连接的事务阻塞了该 DDL 的执行，并且其事务执行的 SQL 语句如 SQL_DIGESTS 中所示。
如果想要中止该事务的执行以使得该 DDL 能够继续执行，我们可以通过 Global Kill 命令将其杀死，然后 DDL 便能继续执行下去：

```sql
mysql> KILL 2199023255957;
Query OK, 0 rows affected (0.00 sec)
```

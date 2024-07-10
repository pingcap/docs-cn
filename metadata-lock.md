---
title: 元数据锁
summary: 介绍 TiDB 中元数据锁的概念、原理、实现和影响。
---

# 元数据锁

本文介绍了 TiDB 中的元数据锁。

## 元数据锁的概念

在 TiDB 中，对元数据对象的更改采用的是在线异步变更算法。事务在执行时会获取开始时对应的元数据快照。如果事务执行过程中相关表上发生了元数据的更改，为了保证数据的一致性，TiDB 会返回 `Information schema is changed` 的错误，导致用户事务提交失败。

为了解决这个问题，在 TiDB v6.3.0 中，online DDL 算法中引入了元数据锁特性。通过协调表元数据变更过程中 DML 语句和 DDL 语句的优先级，让执行中的 DDL 语句等待持有旧版本元数据的 DML 语句提交，尽可能避免 DML 语句报错。

## 适用场景

元数据锁适用于所有的 DDL 语句，包括但不限于：

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
- [`ADD COLUMN`](/sql-statements/sql-statement-add-column.md)
- [`DROP COLUMN`](/sql-statements/sql-statement-drop-column.md)
- [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md)
- [`DROP PARTITION`](/partitioned-table.md#分区管理)
- [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)
- [`EXCHANGE PARTITION`](/partitioned-table.md#分区管理)
- [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)
- [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)

使用元数据锁机制会给 TiDB DDL 任务的执行带来一定的性能影响。为了降低元数据锁对 DDL 任务的影响，下列场景不需要加元数据锁：

- 开启了 auto-commit 的查询语句
- 开启了 Stale Read 功能
- 访问临时表

## 使用元数据锁

在 v6.5.0 及之后的版本中，TiDB 默认开启元数据锁特性。当集群从 v6.5.0 之前的版本升级到 v6.5.0 及之后的版本时，TiDB 会自动开启元数据锁功能。如果需要关闭元数据锁，你可以将系统变量 [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-从-v630-版本开始引入) 设置为 `OFF`。

## 元数据锁的影响

- 对于 DML 语句来说，元数据锁不会导致 DML 语句被阻塞，因此也不会存在死锁的问题。
- 开启元数据锁后，事务中某个元数据对象的元数据信息在第一次访问时确定，之后不再变化。
- 对于 DDL 语句来说，在进行元数据状态变更时，会被涉及相关元数据的旧事务所阻塞。例如以下的执行流程：

    | Session 1 | Session 2 |
    |:---------------------------|:----------|
    | `CREATE TABLE t (a INT);`  |           |
    | `INSERT INTO t VALUES(1);` |           |
    | `BEGIN;`                   |           |
    |                            | `ALTER TABLE t ADD COLUMN b INT;` |
    | `SELECT * FROM t;`<br/>（采用 `t` 表当前的元数据版本，返回 `(a=1，b=NULL)`，同时给表 `t` 加锁）|           |
    |                            | `ALTER TABLE t ADD COLUMN c INT;`（被 Session 1 阻塞）|

    在可重复读隔离级别下，如果从事务开始到确定一个表的元数据过程中，执行了加索引或者变更列类型等需要更改数据的 DDL，则有以下表现：

    | Session 1                  | Session 2                                 |
    |:---------------------------|:------------------------------------------|
    | `CREATE TABLE t (a INT);`  |                                           |
    | `INSERT INTO t VALUES(1);` |                                           |
    | `BEGIN;`                   |                                           |
    |                            | `ALTER TABLE t ADD INDEX idx(a);`         |
    | `SELECT * FROM t;`（索引 `idx` 不可用）|                                 |
    | `COMMIT;`                  |                                           |
    | `BEGIN;`                   |                                           |
    |                            | `ALTER TABLE t MODIFY COLUMN a CHAR(10);` |
    | `SELECT * FROM t;`（报错 `ERROR 8028 (HY000): public column a has changed`） |             |

## 元数据锁的可观测性

TiDB v6.3.0 引入了 `mysql.tidb_mdl_view` 视图，可以用于查看当前阻塞的 DDL 的相关信息。

> **注意：**
>
> 查询 `mysql.tidb_mdl_view` 视图需要有 [`PROCESS` 权限](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)。

下面以给表 `t` 添加索引为例，假设有 DDL 语句 `ALTER TABLE t ADD INDEX idx(a)`：

```sql
SELECT * FROM mysql.tidb_mdl_view\G
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

可以从上面的输出结果中了解到，有一个 `SESSION ID` 为 `2199023255957` 的事务阻塞了该添加索引 DDL 的执行。该事务执行的 SQL 语句如 `SQL_DIGESTS` 中所示，即 ``["begin","select * from `t`"]``。如果想要使被阻塞的 DDL 能够继续执行，可以通过如下 Global `KILL` 命令中止 `SESSION ID` 为 `2199023255957` 的事务：

```sql
mysql> KILL 2199023255957;
Query OK, 0 rows affected (0.00 sec)
```

中止该事务后，再次查询 `mysql.tidb_mdl_view` 视图。此时，查询结果不再显示上面的事务信息，说明 DDL 不再被阻塞：

```sql
SELECT * FROM mysql.tidb_mdl_view\G
Empty set (0.01 sec)
```

## 元数据锁的原理

### 问题描述

TiDB 中 DDL 操作使用的是 online DDL 模式。一个 DDL 语句在执行过程中，需要修改定义的对象元数据版本可能会进行多次小版本变更，而元数据在线异步变更的算法只论证了相邻的两个小版本之间是兼容的，即在相邻的两个元数据版本间操作，不会破坏 DDL 变更对象所存储的数据一致性。

以添加索引为例，DDL 语句的状态会经历 None -> Delete Only，Delete Only -> Write Only，Write Only -> Write Reorg，Write Reorg -> Public 这四个变化。

以下的提交流程将违反“相邻的两个小版本之间是兼容的”约束：

| 事务  | 所用的版本  | 集群最新版本 | 版本差 |
|:-----|:-----------|:-----------|:----|
| txn1 | None       | None       | 0   |
| txn2 | DeleteOnly | DeleteOnly | 0   |
| txn3 | WriteOnly  | WriteOnly  | 0   |
| txn4 | None       | WriteOnly  | 2   |
| txn5 | WriteReorg | WriteReorg | 0   |
| txn6 | WriteOnly  | WriteReorg | 1   |
| txn7 | Public     | Public     | 0   |

其中 `txn4` 提交时采用的元数据版本与集群最新的元数据版本相差了两个版本，会影响数据正确性。

### 实现

引入元数据锁会保证整个 TiDB 集群中的所有事务所用的元数据版本最多相差一个版本。为此：

- 执行 DML 语句时，TiDB 会在事务上下文中记录该 DML 语句访问的元数据对象，例如表、视图，以及对应的元数据版本。事务提交时会清空这些记录。
- DDL 语句进行状态变更时，会向所有的 TiDB 节点推送最新版本的元数据。如果一个 TiDB 节点上所有与这次状态变更相关的事务使用的元数据版本与当前元数据版本之差小于 2，则称这个 TiDB 节点获得了该元数据对象的元数据锁。当集群中的所有 TiDB 节点都获得了该元数据对象的元数据锁后，才能进行下一次状态变更。
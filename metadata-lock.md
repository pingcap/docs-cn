---
title: 元数据锁
summary: 介绍 TiDB 中元数据锁的概念、原理和实现细节。
---

# 元数据锁

本文介绍 TiDB 中的元数据锁。

## 概念

TiDB 使用在线异步 schema 变更算法来支持元数据对象的变更。当执行事务时，事务会在开始时获取相应的元数据快照。如果在事务执行期间元数据发生变更，为了保证数据一致性，TiDB 会返回 `Information schema is changed` 错误，事务提交失败。

为了解决这个问题，TiDB v6.3.0 在在线 DDL 算法中引入了元数据锁。为了避免大多数 DML 错误，TiDB 在表元数据变更期间协调 DML 和 DDL 的优先级，使执行 DDL 等待使用旧元数据的 DML 提交。

## 应用场景

TiDB 中的元数据锁适用于所有 DDL 语句，例如：

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
- [`ADD COLUMN`](/sql-statements/sql-statement-add-column.md)
- [`DROP COLUMN`](/sql-statements/sql-statement-drop-column.md)
- [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md)
- [`DROP PARTITION`](/partitioned-table.md#partition-management)
- [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)
- [`EXCHANGE PARTITION`](/partitioned-table.md#partition-management)
- [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)
- [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)

启用元数据锁可能会对 TiDB 中 DDL 任务的执行性能产生一些影响。为了减少影响，以下列出了一些不需要元数据锁的场景：

+ 启用自动提交的 `SELECT` 查询
+ 启用 Stale Read
+ 访问临时表

## 使用方法

从 v6.5.0 开始，TiDB 默认启用元数据锁。当你将现有集群从 v6.4.0 或更早版本升级到 v6.5.0 或更高版本时，TiDB 会自动启用元数据锁。要禁用元数据锁，你可以将系统变量 [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630) 设置为 `OFF`。

## 影响

- 对于 DML，元数据锁不会阻塞其执行，也不会造成任何死锁。
- 当启用元数据锁时，事务中元数据对象的信息在首次访问时确定，之后不会改变。
- 对于 DDL，在更改元数据状态时，DDL 可能会被旧事务阻塞。以下是一个示例：

    | Session 1 | Session 2 |
    |:---------------------------|:----------|
    | `CREATE TABLE t (a INT);`  |           |
    | `INSERT INTO t VALUES(1);` |           |
    | `BEGIN;`                   |           |
    |                            | `ALTER TABLE t ADD COLUMN b INT;` |
    | `SELECT * FROM t;`<br/>（使用表 `t` 的当前元数据版本。返回 `(a=1, b=NULL)` 并锁定表 `t`。）         |           |
    |                            | `ALTER TABLE t ADD COLUMN c INT;`（被 Session 1 阻塞） |

    在可重复读隔离级别下，从事务开始到确定表元数据的时间点之间，如果执行了需要数据变更的 DDL，例如添加索引或更改列类型，DDL 会返回如下错误：

    | Session 1                  | Session 2                                 |
    |:---------------------------|:------------------------------------------|
    | `CREATE TABLE t (a INT);`  |                                           |
    | `INSERT INTO t VALUES(1);` |                                           |
    | `BEGIN;`                   |                                           |
    |                            | `ALTER TABLE t ADD INDEX idx(a);`         |
    | `SELECT * FROM t;`（索引 `idx` 不可用） |                    |
    | `COMMIT;`                  |                                           |
    | `BEGIN;`                   |                                           |
    |                            | `ALTER TABLE t MODIFY COLUMN a CHAR(10);` |
    | `SELECT * FROM t;`（返回 `ERROR 8028 (HY000): public column a has changed`） | |

## 可观察性

TiDB v6.3.0 引入了 `mysql.tidb_mdl_view` 视图，帮助你获取当前被阻塞的 DDL 信息。

> **注意：**
>
> 查询 `mysql.tidb_mdl_view` 视图需要 [`PROCESS` 权限](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)。

以下以为表 `t` 添加索引为例。假设有一个 DDL 语句 `ALTER TABLE t ADD INDEX idx(a)`：

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

从上述输出中可以看到，`SESSION ID` 为 `2199023255957` 的事务阻塞了 `ADD INDEX` DDL。`SQL_DIGEST` 显示了该事务执行的 SQL 语句，即 ``["begin","select * from `t`"]``。要使被阻塞的 DDL 继续执行，你可以使用以下全局 `KILL` 语句来终止 `2199023255957` 事务：

```sql
mysql> KILL 2199023255957;
Query OK, 0 rows affected (0.00 sec)
```

终止事务后，你可以再次查询 `mysql.tidb_mdl_view` 视图。此时，上述事务不会出现在输出中，这意味着 DDL 不再被阻塞。

```sql
SELECT * FROM mysql.tidb_mdl_view\G
Empty set (0.01 sec)
```

## 原理

### 问题描述

TiDB 中的 DDL 操作是在线 DDL 模式。当执行 DDL 语句时，要修改的定义对象的元数据版本可能会经历多个小版本变更。在线异步元数据变更算法只建立了相邻两个小版本之间的兼容性，即两个版本之间的操作不会破坏 DDL 变更对象的数据一致性。

在为表添加索引时，DDL 语句的状态变更如下：None -> Delete Only, Delete Only -> Write Only, Write Only -> Write Reorg, Write Reorg -> Public。

以下事务的提交过程违反了上述约束：

| 事务  | 事务使用的版本  | 集群中的最新版本 | 版本差异 |
|:-----|:-----------|:-----------|:----|
| txn1 | None       | None       | 0   |
| txn2 | DeleteOnly | DeleteOnly | 0   |
| txn3 | WriteOnly  | WriteOnly  | 0   |
| txn4 | None       | WriteOnly  | 2   |
| txn5 | WriteReorg | WriteReorg | 0   |
| txn6 | WriteOnly  | WriteReorg | 1   |
| txn7 | Public     | Public     | 0   |

在上表中，`txn4` 提交时使用的元数据版本与集群中的最新版本相差两个版本。这可能会导致数据不一致。

### 实现细节

元数据锁可以确保 TiDB 集群中所有事务使用的元数据版本最多相差一个版本。为了实现这个目标，TiDB 实现了以下两个规则：

- 执行 DML 时，TiDB 在事务上下文中记录 DML 访问的元数据对象，如表、视图和相应的元数据版本。这些记录在事务提交时被清理。
- 当 DDL 语句改变状态时，最新版本的元数据被推送到所有 TiDB 节点。如果 TiDB 节点上与此状态变更相关的所有事务使用的元数据版本与当前元数据版本的差异小于两个，则认为该 TiDB 节点获得了元数据对象的元数据锁。只有在集群中所有 TiDB 节点都获得元数据对象的元数据锁后，才能执行下一个状态变更。

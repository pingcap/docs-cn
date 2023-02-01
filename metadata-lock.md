---
title: Metadata Lock
summary: Introduce the concept, principles, and implementation details of metadata lock in TiDB.
---

# Metadata Lock

This document introduces the metadata lock in TiDB.

## Concept

TiDB uses the online asynchronous schema change algorithm to support changing metadata objects. When a transaction is executed, it obtains the corresponding metadata snapshot at the transaction start. If the metadata is changed during a transaction, to ensure data consistency, TiDB returns an `Information schema is changed` error and the transaction fails to commit.

To solve the problem, TiDB v6.3.0 introduces metadata lock into the online DDL algorithm. To avoid most DML errors, TiDB coordinates the priority of DMLs and DDLs during table metadata change and makes executing DDLs wait for the DMLs with old metadata to commit.

## Scenarios

The metadata lock in TiDB applies to all DDL statements, such as:

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
- [`ADD COLUMN`](/sql-statements/sql-statement-add-column.md)
- [`DROP COLUMN`](/sql-statements/sql-statement-drop-column.md)
- [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md)
- [`DROP PARTITION`](/partitioned-table.md#partition-management)
- [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)
- [`EXCHANGE PARTITION`](/partitioned-table.md#partition-management)
- [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)
- [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)

Enabling metadata lock might have some performance impact on the execution of the DDL task in TiDB. To reduce the impact, the following lists some scenarios that do not require metadata lock:

+ `SELECT` queries with auto-commit enabled
+ Stale Read is enabled
+ Access temporary tables

## Usage

Starting from v6.5.0, TiDB enables metadata lock by default. When you upgrade your existing cluster from v6.4.0 or earlier to v6.5.0 or later, TiDB automatically enables metadata lock. To disable metadata lock, you can set the system variable [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630) to `OFF`.

## Impact

- For DMLs, metadata lock does not block its execution, nor causes any deadlock.
- When metadata lock is enabled, the information of a metadata object in a transaction is determined on the first access and does not change after that.
- For DDLs, when changing metadata state, DDLs might be blocked by old transactions. The following is an example:

    | Session 1 | Session 2 |
    |:---------------------------|:----------|
    | `CREATE TABLE t (a INT);`  |           |
    | `INSERT INTO t VALUES(1);` |           |
    | `BEGIN;`                   |           |
    |                            | `ALTER TABLE t ADD COLUMN b INT;` |
    | `SELECT * FROM t;`<br/>(Uses the current metadata version of table `t`. Returns `(a=1, b=NULL)` and locks table `t`.)         |           |
    |                            | `ALTER TABLE t ADD COLUMN c INT;` (blocked by Session 1) |

    At the repeatable read isolation level, from the transaction start to the timepoint of determining the metadata of a table, if a DDL that requires data changes is performed, such as adding an index, or changing column types, the DDL returns an error as follows:

    | Session 1                  | Session 2                                 |
    |:---------------------------|:------------------------------------------|
    | `CREATE TABLE t (a INT);`  |                                           |
    | `INSERT INTO t VALUES(1);` |                                           |
    | `BEGIN;`                   |                                           |
    |                            | `ALTER TABLE t ADD INDEX idx(a);`         |
    | `SELECT * FROM t;` (index `idx` is not available) |                    |
    | `COMMIT;`                  |                                           |
    | `BEGIN;`                   |                                           |
    |                            | `ALTER TABLE t MODIFY COLUMN a CHAR(10);` |
    | `SELECT * FROM t;` (returns an error `Information schema is changed`) | |

## Observability

TiDB v6.3.0 introduces the `mysql.tidb_mdl_view` view to help you obtain the information of the current blocked DDL.

> **Note:**
>
> To select the `mysql.tidb_mdl_view` view, the [`PROCESS` privilege](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) is required.

The following takes adding an index for table `t` as an example. Assume that there is a DDL statement `ALTER TABLE t ADD INDEX idx(a)`:

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

From the preceding output, you can see that the transaction whose `SESSION ID` is `2199023255957` blocks the `ADD INDEX` DDL. `SQL_DIGEST` shows the SQL statements executed by this transaction, which is ``["begin","select * from `t`"]``. To make the blocked DDL continue to execute, you can use the following global `KILL` statement to kill the `2199023255957` transaction:

```sql
mysql> KILL 2199023255957;
Query OK, 0 rows affected (0.00 sec)
```

After killing the transaction, you can select the `mysql.tidb_mdl_view` view again. At this time, the preceding transaction is not shown in the output, which means the DDL is not blocked.

```sql
SELECT * FROM mysql.tidb_mdl_view\G
Empty set (0.01 sec)
```

## Principles

### Description of the issue

DDL operations in TiDB are the online DDL mode. When a DDL statement is being executed, the metadata version of the defined object to be modified might go through multiple minor version changes. The online asynchronous metadata change algorithm only establishes that two adjacent minor versions are compatible, that is, operations between two versions do not break data consistency of the object that DDL changes.

When adding an index to a table, the state of the DDL statement changes as follows: None -> Delete Only, Delete Only -> Write Only, Write Only -> Write Reorg, Write Reorg -> Public.

The following commit process of transactions violates the preceding constraint:

| Transaction  | Version used by transaction  | Latest version in the cluster | Version difference |
|:-----|:-----------|:-----------|:----|
| txn1 | None       | None       | 0   |
| txn2 | DeleteOnly | DeleteOnly | 0   |
| txn3 | WriteOnly  | WriteOnly  | 0   |
| txn4 | None       | WriteOnly  | 2   |
| txn5 | WriteReorg | WriteReorg | 0   |
| txn6 | WriteOnly  | WriteReorg | 1   |
| txn7 | Public     | Public     | 0   |

In the preceding table, the metadata version used when `txn4` is committed is two versions different from the latest version in the cluster. This might cause data inconsistency.

### Implementation details

Metadata lock can ensure that the metadata versions used by all transactions in a TiDB cluster differ by one version at most. To achieve this goal, TiDB implements the following two rules:

- When executing a DML, TiDB records metadata objects accessed by the DML in the transaction context, such as tables, views, and corresponding metadata versions. These records are cleaned up when the transaction is committed.
- When a DDL statement changes state, the latest version of metadata is pushed to all TiDB nodes. If the difference between the metadata version used by all transactions related to this state change on a TiDB node and the current metadata version is less than two, the TiDB node is considered to acquire the metadata lock of the metadata object. The next state change can only be executed after all TiDB nodes in the cluster have obtained the metadata lock of the metadata object.

---
title: TIDB_TRX
summary: Learn the `TIDB_TRX` INFORMATION_SCHEMA table.
---

# TIDB_TRX

The `TIDB_TRX` table provides information about the transactions currently being executed on the TiDB node.

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_TRX;
```

The output is as follows:

```sql
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| Field                   | Type                                                            | Null | Key  | Default | Extra |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| ID                      | bigint(21) unsigned                                             | NO   | PRI  | NULL    |       |
| START_TIME              | timestamp(6)                                                    | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)                                                     | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                                                            | YES  |      | NULL    |       |
| STATE                   | enum('Idle','Running','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME      | timestamp(6)                                                    | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS         | bigint(64)                                                      | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES        | bigint(64)                                                      | YES  |      | NULL    |       |
| SESSION_ID              | bigint(21) unsigned                                             | YES  |      | NULL    |       |
| USER                    | varchar(16)                                                     | YES  |      | NULL    |       |
| DB                      | varchar(64)                                                     | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS         | text                                                            | YES  |      | NULL    |       |
| RELATED_TABLE_IDS       | text                                                            | YES  |      | NULL    |       |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
```

The meaning of each column field in the `TIDB_TRX` table is as follows:

* `ID`: The transaction ID, which is the `start_ts` (start timestamp) of the transaction.
* `START_TIME`: The start time of the transaction, which is the physical time corresponding to the `start_ts` of the transaction.
* `CURRENT_SQL_DIGEST`: The digest of the SQL statement currently being executed in the transaction.
* `CURRENT_SQL_DIGEST_TEXT`: The normalized form of the SQL statement currently being executed by the transaction, that is, the SQL statement without arguments and format. It corresponds to `CURRENT_SQL_DIGEST`.
* `STATE`: The current state of the transaction. The possible values ​​include:
    * `Idle`: The transaction is in an idle state, that is, it is waiting for the user to input a query.
    * `Running`: The transaction is executing a query.
    * `LockWaiting`: The transaction is waiting for the pessimistic lock to be acquired. Note that the transaction enters this state at the beginning of the pessimistic locking operation, no matter whether it is blocked by other transactions or not.
    * `Committing`: The transaction is in the process of commit.
    * `RollingBack`: The transaction is being rolled back.
* `WAITING_START_TIME`: When the value of `STATE` is `LockWaiting`, this column shows the start time of the waiting.
* `MEM_BUFFER_KEYS`: The number of keys written into the memory buffer by the current transaction.
* `MEM_BUFFER_BYTES`: The total number of key-value bytes written into the memory buffer by the current transaction.
* `SESSION_ID`: The ID of the session to which this transaction belongs.
* `USER`: The name of the user who performs the transaction.
* `DB`: The current default database name of the session in which the transaction is executed.
* `ALL_SQL_DIGESTS`: The digest list of statements that have been executed by the transaction. The list is shown as a string array in JSON format. Each transaction records at most the first 50 statements. Using the [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests) function, you can convert the information in this column into a list of corresponding normalized SQL statements.
* `RELATED_TABLE_IDS`: The IDs of the tables, views, and other objects that the transaction accesses.

> **Note:**
>
> * Only users with the [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) privilege can obtain the complete information in this table. Users without the PROCESS privilege can only query information of the transactions performed by the current user.
> * The information (SQL digest) in the `CURRENT_SQL_DIGEST` and `ALL_SQL_DIGESTS` columns is the hash value calculated from the normalized SQL statement. The information in the `CURRENT_SQL_DIGEST_TEXT` column and the result returned from the `TIDB_DECODE_SQL_DIGESTS` function are internally queried from the statements summary tables, so it is possible that the corresponding statement cannot be found internally. For the detailed description of SQL digests and the statements summary tables, see [Statement Summary Tables](/statement-summary-tables.md).
> * The [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests) function call has a high overhead. If the function is called to query historical SQL statements for a large number of transactions, the query might take a long time. If the cluster is large with many concurrent transactions, avoid directly using this function on the `ALL_SQL_DIGEST` column while querying the full table of `TIDB_TRX`. This means to avoid an SQL statement like ``SELECT *, tidb_decode_sql_digests(all_sql_digests) FROM TIDB_TRX``.
> * Currently the `TIDB_TRX` table does not support showing information of TiDB internal transactions.

## Example

View the `TIDB_TRX` table:

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_TRX\G
```

The output is as follows:

```sql
*************************** 1. row ***************************
                     ID: 426789913200689153
             START_TIME: 2021-08-04 10:51:54.883000
     CURRENT_SQL_DIGEST: NULL
CURRENT_SQL_DIGEST_TEXT: NULL
                  STATE: Idle
     WAITING_START_TIME: NULL
        MEM_BUFFER_KEYS: 1
       MEM_BUFFER_BYTES: 29
             SESSION_ID: 7
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","04fa858fa491c62d194faec2ab427261cc7998b3f1ccf8f6844febca504cb5e9","b83710fa8ab7df8504920e8569e48654f621cf828afbe7527fd003b79f48da9e"]
*************************** 2. row ***************************
                     ID: 426789921471332353
             START_TIME: 2021-08-04 10:52:26.433000
     CURRENT_SQL_DIGEST: 38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821
CURRENT_SQL_DIGEST_TEXT: update `t` set `v` = `v` + ? where `id` = ?
                  STATE: LockWaiting
     WAITING_START_TIME: 2021-08-04 10:52:35.106568
        MEM_BUFFER_KEYS: 0
       MEM_BUFFER_BYTES: 0
             SESSION_ID: 9
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"]
2 rows in set (0.01 sec)
```

From the query result of this example, you can see that: the current node has two on-going transactions. One transaction is in the idle state (`STATE` is `Idle` and `CURRENT_SQL_DIGEST` is `NULL`), and this transaction has executed 3 statements (there are three records in the `ALL_SQL_DIGESTS` list, which are the digests of the three SQL statements that have been executed). Another transaction is executing a statement and waiting for the lock (`STATE` is `LockWaiting` and `WAITING_START_TIME` shows the start time of the waiting lock). The transaction has executed 2 statements, and the statement currently being executed is in the form of ``"update `t` set `v` = `v` + ? where `id` = ?"``.

```sql
SELECT id, all_sql_digests, tidb_decode_sql_digests(all_sql_digests) AS all_sqls FROM INFORMATION_SCHEMA.TIDB_TRX\G
```

The output is as follows:

```sql
*************************** 1. row ***************************
             id: 426789913200689153
all_sql_digests: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","04fa858fa491c62d194faec2ab427261cc7998b3f1ccf8f6844febca504cb5e9","b83710fa8ab7df8504920e8569e48654f621cf828afbe7527fd003b79f48da9e"]
       all_sqls: ["begin","insert into `t` values ( ... )","update `t` set `v` = `v` + ?"]
*************************** 2. row ***************************
             id: 426789921471332353
all_sql_digests: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"]
       all_sqls: ["begin","update `t` set `v` = `v` + ? where `id` = ?"]
```

This query calls the [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests) function on the `ALL_SQL_DIGESTS` column of the `TIDB_TRX` table, and converts the SQL digest array into an array of normalized SQL statement through the system internal query. This helps you visually obtain the information of the statements that have been historically executed by the transaction. However, note that the preceding query scans the entire table of `TIDB_TRX` and calls the `TIDB_DECODE_SQL_DIGESTS` function for each row. Calling the `TIDB_DECODE_SQL_DIGESTS` function has a high overhead. Therefore, if many concurrent transactions exist in the cluster, try to avoid this type of query.

## CLUSTER_TIDB_TRX

The `TIDB_TRX` table only provides information about the transactions that are being executed on a single TiDB node. If you want to view the information of the transactions that are being executed on all TiDB nodes in the entire cluster, you need to query the `CLUSTER_TIDB_TRX` table. Compared with the query result of the `TIDB_TRX` table, the query result of the `CLUSTER_TIDB_TRX` table includes an extra `INSTANCE` field. The `INSTANCE` field displays the IP address and port of each node in the cluster, which is used to distinguish the TiDB nodes where the transactions are located.

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_TIDB_TRX;
```

The output is as follows:

```sql
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| Field                   | Type                                                            | Null | Key  | Default | Extra |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| INSTANCE                | varchar(64)                                                     | YES  |      | NULL    |       |
| ID                      | bigint(21) unsigned                                             | NO   | PRI  | NULL    |       |
| START_TIME              | timestamp(6)                                                    | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)                                                     | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                                                            | YES  |      | NULL    |       |
| STATE                   | enum('Idle','Running','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME      | timestamp(6)                                                    | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS         | bigint(64)                                                      | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES        | bigint(64)                                                      | YES  |      | NULL    |       |
| SESSION_ID              | bigint(21) unsigned                                             | YES  |      | NULL    |       |
| USER                    | varchar(16)                                                     | YES  |      | NULL    |       |
| DB                      | varchar(64)                                                     | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS         | text                                                            | YES  |      | NULL    |       |
| RELATED_TABLE_IDS       | text                                                            | YES  |      | NULL    |       |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
14 rows in set (0.00 sec)
```

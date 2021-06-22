---
title: TIDB_TRX
summary: Learn the `TIDB_TRX` information_schema table.
---

# TIDB_TRX

The `TIDB_TRX` table provides information about the transactions currently being executed on the TiDB node.

> **Warning:**
>
> * Currently, this is an experimental feature. The definition and behavior of the table structure might have major changes in future releases.
> * Currently, the `TIDB_TRX` table does not support displaying information of TiDB's internal transactions.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tidb_trx;
```

```sql
+--------------------+---------------------------------------------------------+------+------+---------+-------+
| Field              | Type                                                    | Null | Key  | Default | Extra |
+--------------------+---------------------------------------------------------+------+------+---------+-------+
| ID                 | bigint(21) unsigned                                     | NO   | PRI  | NULL    |       |
| START_TIME         | timestamp(6)                                            | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST | varchar(64)                                             | YES  |      | NULL    |       |
| STATE              | enum('Normal','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME | timestamp(6)                                            | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS    | bigint(64)                                              | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES   | bigint(64)                                              | YES  |      | NULL    |       |
| SESSION_ID         | bigint(21) unsigned                                     | YES  |      | NULL    |       |
| USER               | varchar(16)                                             | YES  |      | NULL    |       |
| DB                 | varchar(64)                                             | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS    | text                                                    | YES  |      | NULL    |       |
+--------------------+---------------------------------------------------------+------+------+---------+-------+
```

The meaning of each column field in the `TIDB_TRX` table is as follows:

* `ID`: The transaction ID, which is the `start_ts` (start timestamp) of the transaction.
* `START_TIME`: The start time of the transaction, which is the physical time corresponding to the `start_ts` of the transaction.
* `CURRENT_SQL_DIGEST`: The digest of the SQL statement currently being executed in the transaction.
* `STATE`: The current state of the transaction. The possible values ​​include:
    * `Normal`: The transaction is being executed normally or in an idle state.
    * `LockWaiting`: The transaction is waiting for the pessimistic lock to be acquired. Note that the transaction enters this state at the beginning of the pessimistic locking operation, no matter whether it is blocked by other transactions or not.
    * `Committing`: The transaction is in the process of commit.
    * `RollingBack`: The transaction is being rolled back.
* `WAITING_START_TIME`: When the value of `STATE` is `LockWaiting`, this column shows the start time of the waiting.
* `MEM_BUFFER_KEYS`: The number of keys written into the memory buffer by the current transaction.
* `MEM_BUFFER_BYTES`: The total number of key-value bytes written into the memory buffer by the current transaction.
* `SESSION_ID`: The ID of the session to which this transaction belongs.
* `USER`: The name of the user who performs the transaction.
* `DB`: The current default database name of the session in which the transaction is executed.
* `ALL_SQL_DIGESTS`: The digest list of statements that have been executed in this transaction. For each transaction, the first 50 statements at most are recorded.

## Example

{{< copyable "sql" >}}

```sql
select * from information_schema.tidb_trx\G
```

```sql
*************************** 1. row ***************************
                ID: 425403705115541506
        START_TIME: 2021-06-04 05:59:10.691000
CURRENT_SQL_DIGEST: NULL
             STATE: Normal
WAITING_START_TIME: NULL
   MEM_BUFFER_KEYS: 2
  MEM_BUFFER_BYTES: 48
        SESSION_ID: 7
              USER: root
                DB: test
   ALL_SQL_DIGESTS: [e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5, 04fa858fa491c62d194faec2ab427261cc7998b3f1ccf8f6844febca504cb5e9, f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb2]
1 row in set (0.00 sec)
```

The query result of the above example indicates that a transaction is being executed on the current node (the `STATE` is `Normal`), and this transaction is currently idle (`CURRENT_SQL_DIGEST` is `NULL`). This transaction has executed three statements (there are three records in the `ALL_SQL_DIGESTS` list and they are the digests of the three executed statements).

## CLUSTER_TIDB_TRX

The `TIDB_TRX` table only provides information about the transactions that are being executed on a single TiDB node. If you want to view the information of the transactions that are being executed on all TiDB nodes in the entire cluster, you need to query the `CLUSTER_TIDB_TRX` table. Compared with the query result of the `TIDB_TRX` table, the query result of the `CLUSTER_TIDB_TRX` table contains an extra `INSTANCE` field. The `INSTANCE` field displays the IP address and port of each node in the cluster, which is used to distinguish the TiDB node where the transaction is located.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC cluster_tidb_trx;
```

```sql
+--------------------+---------------------------------------------------------+------+------+---------+-------+
| Field              | Type                                                    | Null | Key  | Default | Extra |
+--------------------+---------------------------------------------------------+------+------+---------+-------+
| INSTANCE           | varchar(64)                                             | YES  |      | NULL    |       |
| ID                 | bigint(21) unsigned                                     | NO   | PRI  | NULL    |       |
| START_TIME         | timestamp(6)                                            | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST | varchar(64)                                             | YES  |      | NULL    |       |
| STATE              | enum('Normal','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME | timestamp(6)                                            | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS    | bigint(64)                                              | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES   | bigint(64)                                              | YES  |      | NULL    |       |
| SESSION_ID         | bigint(21) unsigned                                     | YES  |      | NULL    |       |
| USER               | varchar(16)                                             | YES  |      | NULL    |       |
| DB                 | varchar(64)                                             | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS    | text                                                    | YES  |      | NULL    |       |
+--------------------+---------------------------------------------------------+------+------+---------+-------+
```

## SQL Digest

The `TIDB_TRX` table only records SQL digests, not the original SQL statement.

SQL digest is the hash value after the SQL normalization. To find the original SQL statement corresponding to the SQL digest, perform one of the following operations:

- For the statements executed on the current TiDB node in the recent period of time, you can find the corresponding orginal SQL statement from the SQL digest in `STATEMENTS_SUMMARY` or `STATEMENTS_SUMMARY_HISTORY`.
- For the statements executed on all TiDB nodes in the entire cluster in the recent period of time, you can find the corresponding SQL statement from the SQL digest in `CLUSTER_STATEMENTS_SUMMARY` or `CLUSTER_STATEMENTS_SUMMARY_HISTORY`.

{{< copyable "sql" >}}

```sql
select digest, digest_text from information_schema.statements_summary where digest = "f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb2";
```

```sql
+------------------------------------------------------------------+---------------------------------------+
| digest                                                           | digest_text                           |
+------------------------------------------------------------------+---------------------------------------+
| f7530877a35ae65300c42250abd8bc731bbaf0a7cabc05dab843565230611bb2 | update `t` set `v` = ? where `id` = ? |
+------------------------------------------------------------------+---------------------------------------+
```

For detailed description of SQL digest, `STATEMENTS_SUMMARY`, `STATEMENTS_SUMMARY_HISTORY`, `CLUSTER_STATEMENTS_SUMMARY`, and `CLUSTER_STATEMENTS_SUMMARY_HISTORY` tables, see [Statement Summary Tables](/statement-summary-tables.md).

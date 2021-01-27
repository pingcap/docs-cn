---
title: KILL [TIDB] | TiDB SQL Statement Reference
summary: An overview of the usage of KILL [TIDB] for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-kill/','/docs/dev/reference/sql/statements/kill/']
---

# KILL [TIDB]

The statement `KILL TIDB` is used to terminate connections in TiDB.

## Synopsis

**KillStmt:**

![KillStmt](/media/sqlgram/KillStmt.png)

**KillOrKillTiDB:**

![KillOrKillTiDB](/media/sqlgram/KillOrKillTiDB.png)

## Examples

```sql
mysql> SHOW PROCESSLIST;
+------+------+-----------+------+---------+------+-------+------------------+
| Id   | User | Host      | db   | Command | Time | State | Info             |
+------+------+-----------+------+---------+------+-------+------------------+
|    1 | root | 127.0.0.1 | test | Query   |    0 | 2     | SHOW PROCESSLIST |
|    2 | root | 127.0.0.1 |      | Sleep   |    4 | 2     |                  |
+------+------+-----------+------+---------+------+-------+------------------+
2 rows in set (0.00 sec)

KILL TIDB 2;
Query OK, 0 rows affected (0.00 sec)
```

## MySQL compatibility

* By design, this statement is not compatible with MySQL by default. This helps prevent against a case of a connection being terminated on the wrong TiDB server, because it is common to place multiple TiDB servers behind a load balancer.
* The `KILL TIDB` statement is a TiDB extension. If you are certain that the session you are attempting to kill is on the same TiDB server, set [`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query) in your configuration file.

## Global kill <span class="version-mark">New in v5.0.0-rc</span>

Since v5.0, TiDB provides experimental support for [Global kill](https://github.com/pingcap/tidb/blob/master/docs/design/2020-06-01-global-kill.md). This feature is used to safely terminate any connection between the client and the TiDB server. When this feature is enabled, each TiDB server ensures that each connection ID is globally unique. The client can issue a `KILL` statement to any TiDB server, and the server internally routes the request to the corresponding TiDB instance. This ensures that `KILL` is safe to execute even when the TiDB server is behind a load balancer.

To enable Global Kill, set `enable-global-kill = true` in the `experimental` section of the [TiDB configuration file](/tidb-configuration-file.md#enable-global-kill-new-in-v500-rc).

## Global kill example

Execute the following statement on the TiDB instance `127.0.0.1:10180`:

```sql
SELECT SLEEP(60);
```

Execute the following statements on the TiDB instance `127.0.0.1:10080`:

```sql
SELECT * FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST;
+-----------------+---------------------+------+-----------+--------------------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+----------------------------------------+
| INSTANCE        | ID                  | USER | HOST      | DB                 | COMMAND | TIME | STATE      | INFO                                                 | DIGEST                                                           | MEM  | TxnStart                               |
+-----------------+---------------------+------+-----------+--------------------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+----------------------------------------+
| 127.0.0.1:10180 | 8824324082762776581 | root | 127.0.0.1 | test               | Query   |    2 | autocommit | SELECT SLEEP(60)                                     | b4dae6a771c1d84157dcc302bef38cbff77a7a8ff89ee38302ac3324485454a3 |    0 |                                        |
| 127.0.0.1:10080 |   98041252825530373 | root | 127.0.0.1 | information_schema | Query   |    0 | autocommit | SELECT * FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST | 43113c6fe27fb20eae4a6dc8c43f176f9292fd873dd08f1041debdff6d335cb0 |    0 | 01-15 23:13:20.609(422241527558045697) |
+-----------------+---------------------+------+-----------+--------------------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+----------------------------------------+
2 rows in set (0.07 sec)

KILL 8824324082762776581;
Query OK, 0 rows affected (0.00 sec)
```

## See also

* [SHOW \[FULL\] PROCESSLIST](/sql-statements/sql-statement-show-processlist.md)
* [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)

---
title: KILL [TIDB] | TiDB SQL Statement Reference
summary: An overview of the usage of KILL [TIDB] for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-kill/','/docs/dev/reference/sql/statements/kill/']
---

# KILL [TIDB]

The statement `KILL TIDB` is used to terminate connections in TiDB.

## Synopsis

```ebnf+diagram
KillStmt ::= KillOrKillTiDB ( 'CONNECTION' | 'QUERY' )? NUM

KillOrKillTiDB ::= 'KILL' 'TIDB'?
```

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

## See also

* [SHOW \[FULL\] PROCESSLIST](/sql-statements/sql-statement-show-processlist.md)
* [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)

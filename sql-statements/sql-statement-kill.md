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

* By design, `KILL` is not compatible with MySQL by default. This helps prevent against a case of a connection being terminated on the wrong TiDB server, because it is common to place multiple TiDB servers behind a load balancer.
* DO NOT set [`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query) in your configuration file UNLESS you are certain that clients will be always connected to the same TiDB node. This is because pressing <kbd>ctrl</kbd>+<kbd>c</kbd> in the default MySQL client opens a new connection in which `KILL` is executed. If there are proxies in between, the new connection might be routed to a different TiDB node, which possibly kills a different session.
* The `KILL TIDB` statement is a TiDB extension, which is a different syntax from the MySQL `KILL [CONNECTION|QUERY]` command and the MySQL command-line <kbd>ctrl</kbd>+<kbd>c</kbd> feature. It is safe to use `KILL TIDB` on the same TiDB node.

## See also

* [SHOW \[FULL\] PROCESSLIST](/sql-statements/sql-statement-show-processlist.md)
* [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)

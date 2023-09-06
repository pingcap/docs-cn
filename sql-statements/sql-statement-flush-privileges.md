---
title: FLUSH PRIVILEGES | TiDB SQL Statement Reference
summary: An overview of the usage of FLUSH PRIVILEGES for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-flush-privileges/','/docs/dev/reference/sql/statements/flush-privileges/']
---

# FLUSH PRIVILEGES

The statement `FLUSH PRIVILEGES` instructs TiDB to reload the in-memory copy of privileges from the privilege tables. You must execute this statement after manually editing tables such as `mysql.user`. However, executing this statement is not necessary after using privilege statements like `GRANT` or `REVOKE`. To execute this statement, the `RELOAD` privilege is required.

## Synopsis

```ebnf+diagram
FlushStmt ::=
    'FLUSH' NoWriteToBinLogAliasOpt FlushOption

NoWriteToBinLogAliasOpt ::=
    ( 'NO_WRITE_TO_BINLOG' | 'LOCAL' )?

FlushOption ::=
    'PRIVILEGES'
|   'STATUS'
|    'TIDB' 'PLUGINS' PluginNameList
|    'HOSTS'
|   LogTypeOpt 'LOGS'
|   TableOrTables TableNameListOpt WithReadLockOpt
```

## Examples

```sql
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)
```

## MySQL compatibility

The `FLUSH PRIVILEGES` statement in TiDB is fully compatible with MySQL. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

* [Privilege Management](/privilege-management.md)

</CustomContent>

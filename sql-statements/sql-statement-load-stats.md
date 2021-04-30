---
title: LOAD STATS
summary: An overview of the usage of LOAD STATS for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-load-stats/']
---

# LOAD STATS

The `LOAD STATS` statement is used to load the statistics into TiDB.

## Synopsis

```ebnf+diagram
LoadStatsStmt ::=
    'LOAD' 'STATS' stringLit
```

## Examples

You can access the address `http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}` to download the TiDB instance's statistics.

You can also use `LOAD STATS ${stats_path}` to load the specific statistics file.

The `${stats_path}` can be an absolute path or a relative path. If you use a relative path, the corresponding file is found starting from the path where `tidb-server` is started. Here is an example:

{{< copyable "sql" >}}

```sql
LOAD STATS '/tmp/stats.json';
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Statistics](/statistics.md)

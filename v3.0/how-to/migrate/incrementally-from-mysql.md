---
title: Migrate Incrementally Using Syncer
summary: Use `mydumper`, `loader` and `syncer` tools to migrate data from MySQL to TiDB.
category: how-to
aliases: ['/docs/op-guide/migration-incremental/']
---

# Migrate Incrementally Using Syncer

The [previous guide](/v3.0/how-to/migrate/from-mysql.md) introduces how to import a full database from MySQL to TiDB using `mydumper`/`loader`. This methodology is not recommended for large databases with frequent updates, since it can lead to a larger downtime window during migration. It is instead recommended to use syncer.

Syncer can be [downloaded as part of Enterprise Tools](/v3.0/reference/tools/download.md).

Assuming the data from `t1` and `t2` is already imported to TiDB using `mydumper`/`loader`. Now we hope that any updates to these two tables are replicated to TiDB in real time.

## Obtain the position to replicate

The data exported from MySQL contains a metadata file which includes the position information. Take the following metadata information as an example:

```
Started dump at: 2017-04-28 10:48:10
SHOW MASTER STATUS:
    Log: mysql-bin.000003
    Pos: 930143241
    GTID:

Finished dump at: 2017-04-28 10:48:11
```

The position information (`Pos: 930143241`) needs to be stored in the `syncer.meta` file for `syncer` to replicate:

```bash
# cat syncer.meta
binlog-name = "mysql-bin.000003"
binlog-pos = 930143241
```

> **Note:**
>
> The `syncer.meta` file only needs to be configured once when it is first used. The position will be automatically updated when binlog is replicated.

## Start `syncer`

The `config.toml` file for `syncer`:

```toml
log-level = "info"
log-file = "syncer.log"
log-rotate = "day"

server-id = 101

# The file path for meta:
meta = "./syncer.meta"
worker-count = 16
batch = 1000
flavor = "mysql"

# The testing address for pprof. It can also be used by Prometheus to pull Syncer metrics.
status-addr = ":8271"

# If you set its value to true, Syncer stops and exits when it encounters the DDL operation.
stop-on-ddl = false

# max-retry is used for retry during network interruption.
max-retry = 100

# Specify the database name to be replicated. Support regular expressions. Start with '~' to use regular expressions.
# replicate-do-db = ["~^b.*","s1"]

# Specify the database you want to ignore in replication. Support regular expressions. Start with '~' to use regular expressions.
# replicate-ignore-db = ["~^b.*","s1"]

# skip-ddls skips the ddl statements.
# skip-ddls = ["^OPTIMIZE\\s+TABLE"]

# skip-dmls skips the DML statements. The type value can be 'insert', 'update' and 'delete'.
# The 'delete' statements that skip-dmls skips in the foo.bar table:
# [[skip-dmls]]
# db-name = "foo"
# tbl-name = "bar"
# type = "delete"
#
# The 'delete' statements that skip-dmls skips in all tables:
# [[skip-dmls]]
# type = "delete"
#
# The 'delete' statements that skip-dmls skips in all foo.* tables:
# [[skip-dmls]]
# db-name = "foo"
# type = "delete"

# Specify the db.table to be replicated.
# db-name and tbl-name do not support the `db-name ="dbname, dbname2"` format.
# [[replicate-do-table]]
# db-name ="dbname"
# tbl-name = "table-name"

# [[replicate-do-table]]
# db-name ="dbname1"
# tbl-name = "table-name1"

# Specify the db.table to be replicated. Support regular expressions. Start with '~' to use regular expressions.
# [[replicate-do-table]]
# db-name ="test"
# tbl-name = "~^a.*"

# Specify the database table you want to ignore in replication.
# db-name and tbl-name do not support the `db-name ="dbname, dbname2"` format.
# [[replicate-ignore-table]]
# db-name = "your_db"
# tbl-name = "your_table"

# Specify the database table you want to ignore in replication. Support regular expressions. Start with '~' to use regular expressions.
# [[replicate-ignore-table]]
# db-name ="test"
# tbl-name = "~^a.*"

# The sharding replicating rules support wildcharacter.
# 1. The asterisk character ("*", also called "star") matches zero or more characters,
#    For example, "doc*" matches "doc" and "document" but not "dodo";
#    The asterisk character must be in the end of the wildcard word,
#    and there is only one asterisk in one wildcard word.
# 2. The question mark ("?") matches any single character.
# [[route-rules]]
# pattern-schema = "route_*"
# pattern-table = "abc_*"
# target-schema = "route"
# target-table = "abc"

# [[route-rules]]
# pattern-schema = "route_*"
# pattern-table = "xyz_*"
# target-schema = "route"
# target-table = "xyz"

[from]
host = "127.0.0.1"
user = "root"
password = ""
port = 3306

[to]
host = "127.0.0.1"
user = "root"
password = ""
port = 4000
```

Start `syncer`:

```bash
./bin/syncer -config config.toml
2016/10/27 15:22:01 binlogsyncer.go:226: [info] begin to sync binlog from position (mysql-bin.000003, 1280)
2016/10/27 15:22:01 binlogsyncer.go:130: [info] register slave for master server 127.0.0.1:3306
2016/10/27 15:22:01 binlogsyncer.go:552: [info] rotate to (mysql-bin.000003, 1280)
2016/10/27 15:22:01 syncer.go:549: [info] rotate binlog to (mysql-bin.000003, 1280)
```

## Insert data into MySQL

```bash
INSERT INTO t1 VALUES (4, 4), (5, 5);
```

## Log in TiDB and view the data

```sql
mysql -h127.0.0.1 -P4000 -uroot -p
mysql> select * from t1;
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
|  4 |    4 |
|  5 |    5 |
+----+------+
```

`syncer` outputs the current replicated data statistics every 30 seconds:

```bash
2017/06/08 01:18:51 syncer.go:934: [info] [syncer]total events = 15, total tps = 130, recent tps = 4,
master-binlog = (ON.000001, 11992), master-binlog-gtid=53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-74,
syncer-binlog = (ON.000001, 2504), syncer-binlog-gtid = 53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-17
2017/06/08 01:19:21 syncer.go:934: [info] [syncer]total events = 15, total tps = 191, recent tps = 2,
master-binlog = (ON.000001, 11992), master-binlog-gtid=53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-74,
syncer-binlog = (ON.000001, 2504), syncer-binlog-gtid = 53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-35
```

You can see that by using `syncer`, the updates in MySQL are automatically replicated in TiDB.

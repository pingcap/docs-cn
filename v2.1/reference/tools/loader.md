---
title: Loader Instructions
summary: Use Loader to load data to TiDB.
category: reference
---

# Loader Instructions

## What is Loader?

Loader is a data import tool to load data to TiDB.

It can be [downloaded](/v2.1/reference/tools/download.md) as part of the Enterprise Tools package.

## Why did we develop Loader?

Since tools like mysqldump will take us days to migrate massive amounts of data, we used the [Mydumper/myloader suite](https://github.com/maxbube/mydumper) to multi-thread export and import data. During the process, we found that Mydumper works well. However, as myloader lacks functions of error retry and savepoint, it is inconvenient for us to use. Therefore, we developed loader, which reads the output data files of Mydumper and imports data to TiDB through the MySQL protocol.

## What can Loader do?

+ Multi-thread import data

+ Support table level concurrent import and scattered hot spot write

+ Support concurrent import of a single large table and scattered hot spot write

+ Support Mydumper data format

+ Support error retry

+ Support savepoint

+ Improve the speed of importing data through system variable

## Usage

> **Note:**
>
> - Do not import the `mysql` system database from the MySQL instance to the downstream TiDB instance.
> - If Mydumper uses the `-m` parameter, the data is exported without the table structure and the loader can not import the data.
> - If you use the default `checkpoint-schema` parameter, after importing the data of a database, run `drop database tidb_loader` before you begin to import the next database.
> - It is recommended to specify the `checkpoint-schema = "tidb_loader"` parameter when importing data.

### Parameter description

```
  -L string: the log level setting, which can be set as debug, info, warn, error, fatal (default: "info")

  -P int: the port of TiDB (default: 4000)

  -V boolean: prints version and exit

  -c string: config file

  -checkpoint-schema string: the database name of checkpoint. In the execution process, loader will constantly update this database. After recovering from an interruption, loader will get the process of the last run through this database. (default: "tidb_loader")

  -d string: the storage directory of data that need to import (default: "./")

  -h string: the host of TiDB (default: "127.0.0.1")

  -p string: the account and password of TiDB

  -status-addr string: It can be used by Prometheus to pull Loader metrics, and is also the pprof address of Loader (default: ":8272")

  -t int: the number of thread,increase this as TiKV nodes increase (default: 16)

  -u string: the user name of TiDB (default: "root")
```

### Configuration file

Apart from command line parameters, you can also use configuration files. The format is shown as below:

```toml
# Loader log level, which can be set as "debug", "info", "warn", "error" and "fatal" (default: "info")
log-level = "info"

# Loader log file
log-file = "loader.log"

# Directory of the dump to import (default: "./")
dir = "./"

# It can be used by Prometheus to pull Loader metrics, and is also the pprof address of Loader (default: ":8272").
status-addr = ":8272"

# The checkpoint data is saved to TiDB, and the schema name is defined here.
checkpoint-schema = "tidb_loader"

# Number of threads restoring concurrently for worker pool (default: 16). Each worker restore one file at a time.
pool-size = 16

# The target database information
[db]
host = "127.0.0.1"
user = "root"
password = ""
port = 4000

# `sql_mode` of session level used to connect to the database when loading data. If `sql-mode` is not provided or set to "@DownstreamDefault", the global `sql_mode` for downstream is used.
# sql-mode = ""
# `max-allowed-packet` sets the maximum data packet allowed for database connection, which corresponds to the `max_allowed_packet` in system parameters. If it is set to 0, the global `max_allowed_packet` for downstream is used.
max-allowed-packet = 67108864

# The sharding replicating rules support wildcharacter.
# 1. The asterisk character (*, also called "star") matches zero or more characters,
#    for example, "doc*" matches "doc" and "document" but not "dodo";
#    asterisk character must be in the end of the wildcard word,
#    and there is only one asterisk in one wildcard word.
# 2. The question mark '?' matches exactly one character.
#    [[route-rules]]
#    pattern-schema = "shard_db_*"
#    pattern-table = "shard_table_*"
#    target-schema = "shard_db"
#    target-table = "shard_table"
```

### Usage example

Command line parameter:

```
./bin/loader -d ./test -h 127.0.0.1 -u root -P 4000
```

Or use configuration file "config.toml":

```
./bin/loader -c=config.toml
```

## FAQ

### The scenario of replicating data from sharded tables

Loader supports importing data from sharded tables into one table within one database according to the route-rules. Before replicating, check the following items:

- Whether the sharding rules can be represented using the `route-rules` syntax.
- Whether the sharded tables contain monotone increasing primary keys, or whether there are conflicts in the unique indexes or the primary keys after the combination.

To combine tables, start the `route-rules` parameter in the configuration file of Loader:

- To use the table combination function, it is required to fill the `pattern-schema` and `target-schema`.
- If the `pattern-table` and `target-table` are NULL, the table name is not combined or converted.

```toml
[[route-rules]]
pattern-schema = "example_db"
pattern-table = "table_*"
target-schema = "example_db"
target-table = "table"
```

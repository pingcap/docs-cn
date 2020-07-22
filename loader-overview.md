---
title: Loader Instructions
summary: Use Loader to load data to TiDB.
aliases: ['/docs/dev/loader-overview/','/docs/dev/reference/tools/loader/','/docs/dev/load-misuse-handling/','/docs/dev/reference/tools/error-case-handling/load-misuse-handling/','/tidb/dev/load-misuse-handling']
---

# Loader Instructions

> **Warning:**
>
> Loader is no longer maintained. Its features are completely superseded by [TiDB Lightning TiDB-backend](/tidb-lightning/tidb-lightning-tidb-backend.md). It is strongly recommend to use TiDB Lightning instead.

## What is Loader?

Loader is a data import tool to load data to TiDB.

It can be [downloaded](/download-ecosystem-tools.md) as part of the Enterprise Tools package.

## Why did we develop Loader?

Since tools like mysqldump will take us days to migrate massive amounts of data, we used the [Mydumper/myloader suite](https://github.com/maxbube/mydumper) to multi-thread export and import data. During the process, we found that Mydumper works well. However, as myloader lacks functions of error retry and savepoint, it is inconvenient for us to use. Therefore, we developed loader, which reads the output data files of Mydumper and imports data to TiDB through the MySQL protocol.

## What can Loader do?

+ Multi-threaded data import

+ Support table-level concurrent import and scattered hotspot write

+ Support concurrent import of a single large table and scattered hotspot write

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

  -h string: the host IP of TiDB (default: "127.0.0.1")

  -p string: the account and password of TiDB

  -status-addr string: It can be used by Prometheus to pull Loader metrics, and is also the pprof address of Loader (default: ":8272")

  -t int: the number of threads. Each worker restores one file at a time. (default: 16)

  -u string: the user name of TiDB (default: "root")
```

### Configuration file

Apart from command-line parameters, you can also use configuration files. The format is shown as below:

```toml
# Loader log level, which can be set as "debug", "info", "warn", "error", and "fatal" (default: "info")
log-level = "info"

# Loader log file
log-file = "loader.log"

# Directory of the dump to import (default: "./")
dir = "./"

# It can be used by Prometheus to pull Loader metrics, and is also the pprof address of Loader (default: ":8272").
status-addr = ":8272"

# The checkpoint data is saved to TiDB, and the schema name is defined here.
checkpoint-schema = "tidb_loader"

# Number of threads restoring concurrently for worker pool (default: 16). Each worker restores one file at a time.
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

## Error: ```Try adjusting the `max_allowed_packet` variable```

The following error is reported during full data import:

```
packet for query is too large. Try adjusting the 'max_allowed_packet' variable
```

### Reasons

* Both MySQL client and MySQL/TiDB Server have `max_allowed_packet` quotas. If any of the `max_allowed_packet` quotas is violated, the client receives a corresponding error message. Currently, the latest version of Loader and TiDB Server all have a default `max_allowed_packet` quota of `64M`.
    * Please use the latest version, or the latest stable version of the tool. See the [download page](/download-ecosystem-tools.md).
* The full data import processing module in Loader or DM does not support splitting `dump sqls` files. This is because Mydumper has the simple code implementation, as shown in the code comment `/* Poor man's data dump code */`. To support correctly splitting `dump sqls` files, you need to implement a sound parser based on TiDB parser, but you will encounter the following issues:
    * A large amount of workload.
    * The task is difficult. It is not easy to ensure the correctness.
    * Significant performance reduction.

### Solutions

* For the above reasons, it is recommended to use the `-s, --statement-size` option which Mydumper offers to control the size of `Insert Statement`: `Attempted size of INSERT statement in bytes, default 1000000`.

    According to the default configuration of `--statement-size`, the size of `Insert Statement` that Mydumper generates is as close as `1M`. This default configuration ensures that this error will not occur in most cases.

    Sometimes the following `WARN` log appears during the dump process. The `WARN` log itself does not affect the dump process but indicates that the dumped table might be a wide table.

    ```
    Row bigger than statement_size for xxx
    ```

* If a single row of a wide table exceeds 64M, you need to modify and enable the following two configurations:
    * Execute `set @@global.max_allowed_packet=134217728` (`134217728 = 128M`) in TiDB Server.
    * Add `max-allowed-packet=128M` to db configuration in the Loader configuration file according to your situation, and then restart the progress or task.

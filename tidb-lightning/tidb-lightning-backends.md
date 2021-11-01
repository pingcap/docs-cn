---
title: TiDB Lightning Backends
summary: Learn the backends of TiDB Lightning.
aliases: ['/docs/dev/tidb-lightning/tidb-lightning-tidb-backend/','/docs/dev/reference/tools/tidb-lightning/tidb-backend/','/tidb/dev/tidb-lightning-tidb-backend','/docs/dev/loader-overview/','/docs/dev/reference/tools/loader/','/docs/dev/load-misuse-handling/','/docs/dev/reference/tools/error-case-handling/load-misuse-handling/','/tidb/dev/load-misuse-handling','/tidb/dev/loader-overview/']
---

# TiDB Lightning Backends

The backend determines how TiDB Lightning imports data into the target cluster.

TiDB Lightning supports the following [backends](/tidb-lightning/tidb-lightning-glossary.md#back-end):

+ [Local-backend](#tidb-lightning-local-backend)
+ [Importer-backend](#tidb-lightning-importer-backend)
+ [TiDB-backend](#tidb-lightning-tidb-backend)

The **Local-backend**: `tidb-lightning` first encodes data into key-value pairs, sorts and stores them in a local temporary directory, and *upload* these key-value pairs to each TiKV node *as SST files*. Then, TiKV ingests these *SST files* into the cluster. The implementation of Local-backend is the same with that of Importer-backend but does not rely on the external `tikv-importer` component.

The **Importer-backend**: `tidb-lightning` first encodes the SQL or CSV data into KV pairs, and relies on the external `tikv-importer` program to sort these KV pairs and ingest directly into the TiKV nodes.

The **TiDB-backend**: `tidb-lightning` first encodes these data into SQL `INSERT` statements, and has these statements executed directly on the TiDB node.

| Backend | Local-backend | Importer-backend | TiDB-backend |
|:---|:---|:---|:---|
| Speed | Fast (~500 GB/hr) | Fast (~300 GB/hr) | Slow (~50 GB/hr) |
| Resource usage | High | High | Low |
| Network bandwidth usage| High | Medium | Low |
| ACID respected while importing | No | No | Yes |
| Target tables | Must be empty | Must be empty | Can be populated |
| Additional component required | No | `tikv-importer` | No |
| TiDB versions supported | >= v4.0.0 | All | All |
| TiDB services impacted | Yes | Yes | No |

## How to choose the backend modes

- If the target cluster of data import is v4.0 or later versions, consider using the Local-backend mode first, which is easier to use and has higher performance than that of the other two modes.
- If the target cluster of data import is v3.x or earlier versions, it is recommended to use the Importer-backend mode.
- If the target cluster of data import is in the online production environment, or if the target table of data import already has data on it, it is recommended to use the TiDB-backend mode.

## TiDB Lightning Local-backend

The Local-backend feature is introduced to TiDB Lightning since TiDB v4.0.3. You can use this feature to import data to TiDB clusters of v4.0.0 or above.

### Deployment for Local-backend

To deploy TiDB Lightning in the Local-backend mode, see [TiDB Lightning Deployment](/tidb-lightning/deploy-tidb-lightning.md).

## TiDB Lightning TiDB-backend

> **Note:**
>
> Since TiDB v4.0, PingCAP no longer maintains the [Loader](https://docs.pingcap.com/tidb/v4.0/loader-overview) tool. Since v5.0, the Loader documentation is no longer available. Loader's functionality has been completely replaced by the TiDB-backend of TiDB Lightning, so it is highly recommended to switch to TiDB Lightning.

### Deployment for TiDB-backend

When using the TiDB-backend, deploying `tikv-importer` is not necessary. Compared with the [standard deployment procedure](/tidb-lightning/deploy-tidb-lightning.md), the TiDB-backend deployment has the following two differences:

* All steps involving `tikv-importer` can be skipped.
* The configuration must be changed to declare that the TiDB-backend is used.

#### Hardware requirements

The speed of TiDB Lightning using TiDB-backend is limited by the SQL processing speed of TiDB. Therefore, even a lower-end machine may max out the possible performance. The recommended hardware configuration is:

* 16 logical cores CPU
* An SSD large enough to store the entire data source, preferring higher read speed
* 1 Gigabit network card

#### Manual deployment

You do not need to download and configure `tikv-importer`. You can download TiDB Lightning from [here](/download-ecosystem-tools.md#tidb-lightning).

Before running `tidb-lightning`, add the following lines into the configuration file:

```toml
[tikv-importer]
backend = "tidb"
```

or supplying the `--backend tidb` arguments when executing `tidb-lightning`.

#### Configuration description and samples

This section provides the samples for task configuration in TiDB Lightning.

```toml
# tidb-lightning task configuration

[lightning]
# Checks whether the cluster satisfies the minimum requirement before starting.
check-requirements = true

# Each table is split into one "index engine" to store indices, and multiple
# "data engines" to store row data. These settings control the maximum
# concurrent number for each type of engines.
# Controls the maximum number of tables that can be imported in parallel. For TiDB-backend, the default value is the number of CPU cores.
index-concurrency = 40

# Controls the maximum number of "data engines" allowed to be imported in parallel. The default value is the number of CPU cores. The value should be no less than the value of index-concurrency.
table-concurrency = 40

# The number of concurrent SQL statements executed. It is set to the number of logical CPU cores by default. The bottleneck of TiDB-backend is usually not the CPU. You can increase this value based on the actual load of the downstream cluster to optimize the write speed. At the same time, when adjusting this configuration, it is recommended to adjust the index-concurrency and table-concurrency to the same value.
region-concurrency = 40

# Logging
level = "info"
# The directory to which the log is output. If it is empty (default), the file is saved to /tmp/lightning.log.{timestamp}. If you want the logs to be written to the system standard output, set it to "-".
file = "tidb-lightning.log"

[checkpoint]
# Whether to enable checkpoints.
# While importing data, TiDB Lightning records which tables have been imported, so
# even if TiDB Lightning or some other component crashes, you can start from a known
# good state instead of restarting from scratch.
enable = true

# Where to store the checkpoints.
#  - file (default): store as a local file (requires v2.1.1 or later)
#  - mysql: store into a remote MySQL-compatible database
driver = "file"

# The schema name (database name) to store the checkpoints
# Enabled only when `driver = "mysql"`.
# schema = "tidb_lightning_checkpoint"

# The data source name (DSN) indicating the location of the checkpoint storage.
#
# For the "file" driver, the DSN is a path. If the path is not specified, Lightning would
# default to "/tmp/CHECKPOINT_SCHEMA.pb".
#
# For the "mysql" driver, the DSN is a URL in the form of "USER:PASS@tcp(HOST:PORT)/".
# If the URL is not specified, the TiDB server from the [tidb] section is used to
# store the checkpoints. You should specify a different MySQL-compatible
# database server to reduce the load of the target TiDB cluster.
#dsn = "/tmp/tidb_lightning_checkpoint.pb"

# Whether to keep the checkpoints after all data are imported. If false, the
# checkpoints are deleted. Keeping the checkpoints can aid debugging but
# might leak metadata about the data source.
# keep-after-success = false

[tikv-importer]
# use the TiDB-backend.
backend = "tidb"

# Action to do when trying to insert a duplicated entry in the "tidb" backend.
#  - replace: use new entry to replace the existing entry
#  - ignore: keep the existing entry, and ignore the new entry
#  - error: report error and quit the program
# on-duplicate = "replace"

[mydumper]
# Block size for file reading. Keep it longer than the longest string of
# the data source.
# read-block-size = "64KiB" 

# Minimum size (in terms of source data file) of each batch of import.
# TiDB Lightning splits a large table into multiple data engine files according to this size.
# batch-size = 107_374_182_400 # Byte (default = 100 GB)

# Local source data directory or the URL of the external storage.
data-source-dir = "/data/my_database"

# the input data in a "strict" format speeds up processing.
# "strict-format = true" requires that:
# in CSV, every value cannot contain literal new lines (U+000A and U+000D, or \r and \n) even
# when quoted, which means new lines are strictly used to separate rows.
# "Strict" format allows TiDB Lightning to quickly locate split positions of a large file for parallel processing.
# However, if the input data is not "strict", it may split a valid data in half and
# corrupt the result.
# The default value is false for safety instead of speed.
strict-format = false

# If strict-format is true, TiDB Lightning splits large CSV files into multiple chunks to process in
# parallel. max-region-size is the maximum size of each chunk after splitting.
# max-region-size = 268_435_456 # Byte (default = 256 MB)

# Only import tables if these wildcard rules are matched. See the corresponding section for details.
filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

# Configures how CSV files are parsed.
[mydumper.csv]
# Separator between fields, should be an ASCII character.
separator = ','
# Quoting delimiter, can either be an ASCII character or empty string.
delimiter = '"'
# Whether the CSV files contain a header.
# If `header` is true, the first line will be skipped.
header = true
# Whether the CSV contains any NULL value.
# If `not-null` is true, all columns from CSV cannot be NULL.
not-null = false
# When `not-null` is false (that is, CSV can contain NULL),
# fields equal to this value will be treated as NULL.
null = '\N'
# Whether to interpret backslash escapes inside fields.
backslash-escape = true
# If a line ends with a separator, remove it.
trim-last-separator = false

[tidb]
# Configuration of any TiDB server from the cluster.
host = "172.16.31.1"
port = 4000
user = "root"
password = ""

# The default SQL mode used to parse and execute the SQL statements.
sql-mode = "ONLY_FULL_GROUP_BY,NO_ENGINE_SUBSTITUTION"

# Whether to use TLS for SQL connections. Valid values are:
#  * ""            - force TLS (same as "cluster") if [tidb.security] section is populated, otherwise same as "false"
#  * "false"       - disable TLS
#  * "cluster"     - force TLS and verify the server's certificate with the CA specified in the [tidb.security] section
#  * "skip-verify" - force TLS but do not verify the server's certificate (insecure!)
#  * "preferred"   - same as "skip-verify", but if the server does not support TLS, fallback to unencrypted connection
# tls = ""

# Specifies certificates and keys for TLS-enabled MySQL connections.
# [tidb.security]

# Public certificate of the CA. Set to empty string to disable TLS for SQL.
# ca-path = "/path/to/ca.pem"

# Public certificate of this service. Default to copy of `security.cert-path`
# cert-path = "/path/to/lightning.pem"

# Private key of this service. Default to copy of `security.key-path`
# key-path = "/path/to/lightning.key"

# Configures the background periodic actions.
# Supported units: h (hour), m (minute), s (second).
[cron]

# Duration between which an import progress is printed to the log.
log-progress = "5m"
```

For detailed descriptions of the configuration items, see [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

### Conflict resolution

The TiDB-backend supports importing to an already-populated table. However, the new data might cause a unique key conflict with the old data. You can control how to resolve the conflict by using this task configuration.

```toml
[tikv-importer]
backend = "tidb"
on-duplicate = "replace" # or "error" or "ignore"
```

| Setting | Behavior on conflict | Equivalent SQL statement |
|:---|:---|:---|
| replace | New entries replace old ones | `REPLACE INTO ...` |
| ignore | Keep old entries and ignore new ones | `INSERT IGNORE INTO ...` |
| error | Abort import | `INSERT INTO ...` |

### Migrating from Loader to TiDB Lightning TiDB-backend

If you need to import data into a TiDB cluster, TiDB Lightning using the TiDB-backend can completely replace the functionalities of [Loader](https://docs.pingcap.com/tidb/v4.0/loader-overview). The following list shows how to translate Loader configurations into [TiDB Lightning configurations](/tidb-lightning/tidb-lightning-configuration.md).

<table>
<thead><tr><th>Loader</th><th>TiDB Lightning</th></tr></thead>
<tbody>
<tr><td>

```toml

# log level
log-level = "info"

# The directory to which the log is output
log-file = "loader.log"

# Prometheus
status-addr = ":8272"

# concurrency
pool-size = 16
```

</td><td>

```toml
[lightning]
# log level
level = "info"

# The directory to which the log is output. If this directory is not specified, it defaults to the directory where the command is executed.
file = "tidb-lightning.log"

# Prometheus
pprof-port = 8289

# concurrency (better left as default)
#region-concurrency = 16
```

</td></tr>
<tr><td>

```toml
# checkpoint database
checkpoint-schema = "tidb_loader"
```

</td><td>

```toml
[checkpoint]
# checkpoint storage
enable = true
schema = "tidb_lightning_checkpoint"
# by default the checkpoint is stored in
# a local file, which is more efficient.
# but you could still choose to store the
# checkpoints in the target database with
# this setting:
#driver = "mysql"
```

</td></tr>
<tr><td>

```toml

```

</td><td>

```toml
[tikv-importer]
# use the TiDB-backend
backend = "tidb"
```

</td></tr>
<tr><td>

```toml

# data source directory
dir = "/data/export/"
```

</td><td>

```toml
[mydumper]
# data source directory
data-source-dir = "/data/export"
```

</td></tr>

<tr><td>

```toml
[db]
# TiDB connection parameters
host = "127.0.0.1"
port = 4000

user = "root"
password = ""

#sql-mode = ""
```

</td><td>

```toml
[tidb]
# TiDB connection parameters
host = "127.0.0.1"
port = 4000

# In the TiDB-backend mode, this parameter is optional.
# status-port = 10080
user = "root"
password = ""

#sql-mode = ""
```

</td></tr>
<tr><td>

```toml
# [[route-rules]]
# Table routes
# schema-pattern = "shard_db_*"
# table-pattern = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td><td>

```toml
# [[routes]]
# schema-pattern = "shard_db_*"
# table-pattern = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td></tr>
</tbody>
</table>

## TiDB Lightning Importer-backend

### Deployment for Importer-backend mode

This section describes how to [deploy TiDB Lightning manually](#deploy-tidb-lightning-manually) in the Importer-backend mode:

#### Hardware requirements

`tidb-lightning` and `tikv-importer` are both resource-intensive programs. It is recommended to deploy them into two separate machines.

To achieve the best performance, it is recommended to use the following hardware configuration:

- `tidb-lightning`:

    - 32+ logical cores CPU
    - An SSD large enough to store the entire data source, preferring higher read speed
    - 10 Gigabit network card (capable of transferring at ≥300 MB/s)
    - `tidb-lightning` fully consumes all CPU cores when running, and deploying on a dedicated machine is highly recommended. If not possible, `tidb-lightning` could be deployed together with other components like `tidb-server`, and the CPU usage could be limited via the `region-concurrency` setting.

- `tikv-importer`:

    - 32+ logical cores CPU
    - 40 GB+ memory
    - 1 TB+ SSD, preferring higher IOPS (≥ 8000 is recommended)
        * The disk should be larger than the total size of the top N tables, where `N` = `max(index-concurrency, table-concurrency)`.
    - 10 Gigabit network card (capable of transferring at ≥300 MB/s)
    - `tikv-importer` fully consumes all CPU, disk I/O and network bandwidth when running, and deploying on a dedicated machine is strongly recommended.

If you have sufficient machines, you can deploy multiple `tidb lightning` + `tikv importer` servers, with each working on a distinct set of tables, to import the data in parallel.

#### Deploy TiDB Lightning manually

##### Step 1: Deploy a TiDB cluster

Before importing data, you need to have a deployed TiDB cluster, with the cluster version 2.0.9 or above. It is highly recommended to use the latest version.

You can find deployment instructions in [TiDB Quick Start Guide](/quick-start-with-tidb.md).

#### Step 2: Download the TiDB Lightning installation package

Refer to the [TiDB enterprise tools download page](/download-ecosystem-tools.md#tidb-lightning) to download the TiDB Lightning package (choose the same version as that of the TiDB cluster).

#### Step 3: Start `tikv-importer`

1. Upload `bin/tikv-importer` from the installation package.

2. Configure `tikv-importer.toml`.

    ```toml
    # TiKV Importer configuration file template

    # Log file
    log-file = "tikv-importer.log"
    # Log level: trace, debug, info, warn, error, off.
    log-level = "info"

    # Listening address of the status server.
    status-server-address = "0.0.0.0:8286"

    [server]
    # The listening address of tikv-importer. tidb-lightning needs to connect to
    # this address to write data.
    addr = "0.0.0.0:8287"

    [import]
    # The directory to store engine files.
    import-dir = "/mnt/ssd/data.import/"
    ```

    The above only shows the essential settings. See the [Configuration](/tidb-lightning/tidb-lightning-configuration.md#tikv-importer) section for the full list of settings.

3. Run `tikv-importer`.

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

#### Step 4: Start `tidb-lightning`

1. Upload `bin/tidb-lightning` and `bin/tidb-lightning-ctl` from the tool set.

2. Mount the data source onto the same machine.

3. Configure `tidb-lightning.toml`. For configurations that do not appear in the template below, TiDB Lightning writes a configuration error to the log file and exits.

    ```toml
    [lightning]
    # The concurrency number of data. It is set to the number of logical CPU
    # cores by default. When deploying together with other components, you can
    # set it to 75% of the size of logical CPU cores to limit the CPU usage.
    # region-concurrency =

    # Logging
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # The listening address of tikv-importer. Change it to the actual address.
    addr = "172.16.31.10:8287"

    [mydumper]
    # mydumper local source data directory
    data-source-dir = "/data/my_database"

    [tidb]
    # Configuration of any TiDB server from the cluster
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # Table schema information is fetched from TiDB via this status-port.
    status-port = 10080
    ```

    The above only shows the essential settings. See the [Configuration](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global) section for the full list of settings.

4. Run `tidb-lightning`. If you directly run the command in the command-line, the process might exit because of the SIGHUP signal received. Instead, it's preferable to run a bash script that contains the `nohup` command:

    ```sh
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

---
title: TiDB Lightning Configuration
summary: Learn about the CLI usage and sample configuration in TiDB Lightning.
category: reference
---

# TiDB Lightning Configuration

This document provides samples for global configuration, task configuration, and TiKV Importer configuration in TiDB Lightning, and describes the usage of command-line parameters.

## Configuration files

TiDB Lightning has two configuration classes: "global" and "task", and they have compatible structures. Their distinction arises only when the [server mode](/dev/reference/tools/tidb-lightning/web.md) is enabled. When server mode is disabled (the default), TiDB Lightning will only execute one task, and the same configuration file is used for both global and task configurations.

### TiDB Lightning (Global)

```toml
### tidb-lightning global configuration

[lightning]
# The HTTP port for the web interface and Prometheus metrics pulling (0 to disable).
status-addr = ':8289'

# Toggle server mode and use of the web interface.
# See the "TiDB Lightning Web Interface" section for details.
server-mode = false

# Logging
level = "info"
file = "tidb-lightning.log"
max-size = 128 # MB
max-days = 28
max-backups = 14
```

### TiDB Lightning (Task)

```toml
### tidb-lightning task configuration

[lightning]
# Checks whether the cluster satisfies the minimum requirement before starting.
#check-requirements = true

# The maximum number of engines to be opened concurrently.
# Each table is split into one "index engine" to store indices, and multiple
# "data engines" to store row data. These settings control the maximum
# concurrent number for each type of engines.
# These values affect the memory and disk usage of tikv-importer.
# The sum of these two values must not exceed the max-open-engines setting
# for tikv-importer.
index-concurrency = 2
table-concurrency = 6

# The concurrency number of data. It is set to the number of logical CPU
# cores by default. When deploying together with other components, you can
# set it to 75% of the size of logical CPU cores to limit the CPU usage.
#region-concurrency =

# The maximum I/O concurrency. Excessive I/O concurrency causes an increase in
# I/O latency because the disk's internal buffer is frequently refreshed,
# which causes the cache miss and slows down the read speed. Depending on the storage
# medium, this value might need to be adjusted for optimal performance.
io-concurrency = 5

[checkpoint]
# Whether to enable checkpoints.
# While importing data, TiDB Lightning records which tables have been imported, so
# even if Lightning or another component crashes, you can start from a known
# good state instead of redoing everything.
enable = true
# The schema name (database name) to store the checkpoints.
schema = "tidb_lightning_checkpoint"
# Where to store the checkpoints.
#  - file:  store as a local file.
#  - mysql: store into a remote MySQL-compatible database
driver = "file"
# The data source name (DSN) indicating the location of the checkpoint storage.
# For the "file" driver, the DSN is a path. If the path is not specified, Lightning would
# default to "/tmp/CHECKPOINT_SCHEMA.pb".
# For the "mysql" driver, the DSN is a URL in the form of "USER:PASS@tcp(HOST:PORT)/".
# If the URL is not specified, the TiDB server from the [tidb] section is used to
# store the checkpoints. You should specify a different MySQL-compatible
# database server to reduce the load of the target TiDB cluster.
#dsn = "/tmp/tidb_lightning_checkpoint.pb"
# Whether to keep the checkpoints after all data are imported. If false, the
# checkpoints will be deleted. Keeping the checkpoints can aid debugging but
# will leak metadata about the data source.
#keep-after-success = false

[tikv-importer]
# The listening address of tikv-importer. Change it to the actual address.
addr = "172.16.31.10:8287"

[mydumper]
# Block size for file reading. Keep it longer than the longest string of
# the data source.
read-block-size = 65536 # Byte (default = 64 KB)

# Minimum size (in terms of source data file) of each batch of import.
# TiDB Lightning splits a large table into multiple data engine files according to this size.
batch-size = 107_374_182_400 # Byte (default = 100 GB)

# The engine file needs to be imported sequentially. Due to parallel processing,
# multiple data engines will be imported at nearly the same time, and this
# creates a queue and wastes resources. Therefore, Lightning slightly
# increases the size of the first few batches to properly distribute
# resources. The scale up factor is controlled by this parameter, which
# expresses the ratio of duration between the "import" and "write" steps
# with full concurrency. This can be calculated by using the ratio
# (import duration/write duration) of a single table of size around 1 GB.
# The exact timing can be found in the log. If "import" is faster, the batch
# size variance is smaller, and a ratio of zero means a uniform batch size.
# This value should be in the range (0 <= batch-import-ratio < 1).
batch-import-ratio = 0.75

# mydumper local source data directory.
data-source-dir = "/data/my_database"
# If no-schema is set to true, tidb-lightning assumes that the table skeletons
# already exist on the target TiDB cluster, and will not execute the `CREATE
# TABLE` statements.
no-schema = false
# The character set of the schema files, containing CREATE TABLE statements;
# only supports one of:
#  - utf8mb4: the schema files must be encoded as UTF-8, otherwise Lightning
#             will emit errors
#  - gb18030: the schema files must be encoded as GB-18030, otherwise
#             Lightning will emit errors
#  - auto:    (default) automatically detects whether the schema is UTF-8 or
#             GB-18030. An error is reported if the encoding is neither.
#  - binary:  do not try to decode the schema files
# Note that the *data* files are always parsed as binary regardless of
# schema encoding.
character-set = "auto"

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
# When `not-null` is false (i.e. CSV can contain NULL),
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
# Table schema information is fetched from TiDB via this status-port.
status-port = 10080
# Address of any PD server from the cluster.
pd-addr = "172.16.31.4:2379"
# tidb-lightning imports TiDB as a library and generates some logs itself.
# This setting controls the log level of the TiDB library.
log-level = "error"

# Sets the TiDB session variable to speed up the Checksum and Analyze operations.
# See https://pingcap.com/docs/dev/reference/performance/statistics/#control-analyze-concurrency
# for the meaning of each setting
build-stats-concurrency = 20
distsql-scan-concurrency = 100
index-serial-scan-concurrency = 20
checksum-table-concurrency = 16

# The default SQL mode used to parse and execute the SQL statements.
sql-mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"

# When data importing is complete, tidb-lightning can automatically perform
# the Checksum, Compact and Analyze operations. It is recommended to leave
# these as true in the production environment.
# The execution order: Checksum -> Analyze
[post-restore]
# Performs `ADMIN CHECKSUM TABLE <table>` for each table to verify data integrity.
checksum = true
# If the value is set to `true`, a level-1 compaction is performed
# every time a table is imported.
# The default value is `false`.
level-1-compact = false
# If the value is set to `true`, a full compaction on the whole
# TiKV cluster is performed at the end of the import.
# The default value is `false`.
compact = false
# Performs `ANALYZE TABLE <table>` for each table.
analyze = true

# Configures the background periodic actions.
# Supported units: h (hour), m (minute), s (second).
[cron]
# Duration between which Lightning automatically refreshes the import mode
# status. Should be shorter than the corresponding TiKV setting.
switch-mode = "5m"
# Duration between which an import progress is printed to the log.
log-progress = "5m"

# Table filter options. See the corresponding section for details.
#[black-white-list]
# ...
```

### TiKV Importer

```toml
# TiKV Importer configuration file template.

# Log file.
log-file = "tikv-importer.log"
# Log level: trace, debug, info, warn, error, off.
log-level = "info"

[server]
# The listening address of tikv-importer. tidb-lightning needs to connect to
# this address to write data.
addr = "0.0.0.0:8287"
# Size of the thread pool for the gRPC server.
grpc-concurrency = 16

[metric]
# The Prometheus client push job name.
job = "tikv-importer"
# The Prometheus client push interval.
interval = "15s"
# The Prometheus Pushgateway address.
address = ""

[rocksdb]
# The maximum number of concurrent background jobs.
max-background-jobs = 32

[rocksdb.defaultcf]
# Amount of data to build up in memory before flushing data to the disk.
write-buffer-size = "1GB"
# The maximum number of write buffers that are built up in memory.
max-write-buffer-number = 8

# The compression algorithms used in different levels.
# The algorithm at level-0 is used to compress KV data.
# The algorithm at level-6 is used to compress SST files.
# The algorithms at level-1 to level-5 are unused for now.
compression-per-level = ["lz4", "no", "no", "no", "no", "no", "lz4"]

[rocksdb.writecf]
# (same as above)
compression-per-level = ["lz4", "no", "no", "no", "no", "no", "lz4"]

[import]
# The directory to store engine files.
import-dir = "/mnt/ssd/data.import/"
# Number of threads to handle RPC requests.
num-threads = 16
# Number of concurrent import jobs.
num-import-jobs = 24
# Maximum duration to prepare Regions.
#max-prepare-duration = "5m"
# Split Regions into this size according to the importing data.
#region-split-size = "512MB"
# Stream channel window size. The stream will be blocked on channel full.
#stream-channel-window = 128
# Maximum number of open engines.
max-open-engines = 8
# Maximum upload speed (bytes per second) from Importer to TiKV.
# upload-speed-limit = "512MB"
# Minimum ratio of available space on the target store: `store_available_space`/`store_capacity`.
# Importer pauses uploading SST if the availability ratio of the target store is less than this
# value, to allow enough time for PD to balance Regions.
min-available-ratio = 0.05
```

## Command line parameters

### Usage of `tidb-lightning`

| Parameter | Explanation | Corresponding setting |
|:----|:----|:----|
| --config *file* | Reads global configuration from *file*. If not specified, the default configuration would be used. | |
| -V | Prints program version | |
| -d *directory* | Directory of the data dump to read from | `mydumper.data-source-dir` |
| -L *level* | Log level: debug, info, warn, error, fatal (default = info) | `lightning.log-level` |
| --log-file *file* | Log file path | `lightning.log-file` |
| --status-addr *ip:port* | Listening address of the TiDB Lightning server | `lightning.status-port` |
| --importer *host:port* | Address of TiKV Importer | `tikv-importer.addr` |
| --pd-urls *host:port* | PD endpoint address | `tidb.pd-addr` |
| --tidb-host *host* | TiDB server host | `tidb.host` |
| --tidb-port *port* | TiDB server port (default = 4000) | `tidb.port` |
| --tidb-status *port* | TiDB status port (default = 10080) | `tidb.status-port` |
| --tidb-user *user* | User name to connect to TiDB | `tidb.user` |

If a command line parameter and the corresponding setting in the configuration file are both provided, the command line parameter will be used. For example, running `./tidb-lightning -L debug --config cfg.toml` would always set the log level to "debug" regardless of the content of `cfg.toml`.

## Usage of `tidb-lightning-ctl`

This tool can execute various actions given one of the following parameters:

| Parameter | Explanation |
|:----|:----|
| --compact | Performs a full compaction |
| --switch-mode *mode* | Switches every TiKV store to the given mode: normal, import |
| --import-engine *uuid* | Imports the closed engine file from TiKV Importer into the TiKV cluster |
| --cleanup-engine *uuid* | Deletes the engine file from TiKV Importer |
| --checkpoint-dump *folder* | Dumps current checkpoint as CSVs into the folder |
| --checkpoint-error-destroy *tablename* | Removes the checkpoint and drops the table if it caused error |
| --checkpoint-error-ignore *tablename* | Ignores any error recorded in the checkpoint involving the given table |
| --checkpoint-remove *tablename* | Unconditionally removes the checkpoint of the table |

The *tablename* must either be a qualified table name in the form `` `db`.`tbl` `` (including the backquotes), or the keyword "all".

Additionally, all parameters of `tidb-lightning` described in the section above are valid in `tidb-lightning-ctl`.

## Usage of `tikv-importer`

| Parameter | Explanation | Corresponding setting |
|:----|:----|:----|
| -C, --config *file* | Reads configuration from *file*. If not specified, the default configuration would be used. | |
| -V, --version | Prints program version | |
| -A, --addr *ip:port* | Listening address of the TiKV Importer server | `server.addr` |
| --import-dir *dir* | Stores engine files in this directory | `import.import-dir` |
| --log-level *level* | Log level: trace, debug, info, warn, error, off | `log-level` |
| --log-file *file* | Log file path | `log-file` |

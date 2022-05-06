---
title: DM Advanced Task Configuration File
aliases: ['/docs/tidb-data-migration/dev/task-configuration-file-full/','/docs/tidb-data-migration/dev/dm-portal/']
---

# DM Advanced Task Configuration File

This document introduces the advanced task configuration file of Data Migration (DM), including [global configuration](#global-configuration) and [instance configuration](#instance-configuration).

## Important concepts

For description of important concepts including `source-id` and the DM-worker ID, see [Important concepts](/dm/dm-config-overview.md#important-concepts).

## Task configuration file template (advanced)

The following is the task configuration file template which allows you to perform **advanced** data migration tasks.

```yaml
---

# ----------- Global setting -----------
## ********* Basic configuration *********
name: test                      # The name of the task. Should be globally unique.
task-mode: all                  # The task mode. Can be set to `full`(only migrates full data)/`incremental`(replicates binlogs synchronously)/`all` (replicates both full data and incremental binlogs).
is-sharding: true               # `is-sharding` has been deprecated since v2.0.0, so it is recommended to directly use `shard-mode`
shard-mode: "pessimistic"       # The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic" mode.
                                # After understanding the principles and restrictions of the "optimistic" mode, you can set it to the "optimistic" mode.
meta-schema: "dm_meta"          # The downstream database that stores the `meta` information.
timezone: "Asia/Shanghai"       # The timezone used in SQL Session. By default, DM uses the global timezone setting in the target cluster, which ensures the correctness automatically. A customized timezone does not affect data migration but is unnecessary.
case-sensitive: false           # Determines whether the schema/table is case-sensitive.
online-ddl: true                # Supports automatic processing of upstream "gh-ost" and "pt".
online-ddl-scheme: "gh-ost"     # `online-ddl-scheme` is deprecated, so it is recommended to use `online-ddl`.
clean-dump-file: true           # Whether to clean up the files generated during data dump. Note that these include `metadata` files.
collation_compatible: "loose"   # The mode to sync the default collation in `CREATE` SQL statements. The supported values are "loose" (by default) or "strict". When the value is "strict", DM explicitly appends the corresponding collation of the upstream to the SQL statements; when the value is "loose", DM does not modify the SQL statements. In "strict" mode, if the downstream does not support the default collation in the upstream, the downstream might report an error.
ignore-checking-items: []       # Ignorable checking items. For the complete list of ignorable checking items, see DM precheck: https://docs.pingcap.com/tidb/stable/dm-precheck#ignorable-checking-items.

target-database:                # Configuration of the downstream database instance.
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: "/Q7B9DizNLLTTfiZHv9WoEAKamfpIUs="  # It is recommended to use a password encrypted with `dmctl encrypt`.
  max-allowed-packet: 67108864                  # Sets the "max_allowed_packet" limit of the TiDB client (that is, the limit of the maximum accepted packet) when DM internally connects to the TiDB server. The unit is bytes. (67108864 by default)
                                                # Since DM v2.0.0, this configuration item is deprecated, and DM automatically obtains the "max_allowed_packet" value from TiDB.
  session:                                       # The session variables of TiDB, supported since v1.0.6. For details, go to `https://pingcap.com/docs/stable/system-variables`.
    sql_mode: "ANSI_QUOTES,NO_ZERO_IN_DATE,NO_ZERO_DATE" # Since DM v2.0.0, if this item does not appear in the configuration file, DM automatically fetches a proper value for "sql_mode" from the downstream TiDB. Manual configuration of this item has a higher priority.
    tidb_skip_utf8_check: 1                     # Since DM v2.0.0, if this item does not appear in the configuration file, DM automatically fetches a proper value for "tidb_skip_utf8_check" from the downstream TiDB. Manual configuration of this item has a higher priority.
    tidb_constraint_check_in_place: 0
  security:                       # The TLS configuration of the downstream TiDB
    ssl-ca: "/path/to/ca.pem"
    ssl-cert: "/path/to/cert.pem"
    ssl-key: "/path/to/key.pem"


## ******** Feature configuration set **********
# The routing mapping rule set between the upstream and downstream tables.
routes:
  route-rule-1:                 # The name of the routing mapping rule.
    schema-pattern: "test_*"    # The pattern of the upstream schema name, wildcard characters (*?) are supported.
    table-pattern: "t_*"        # The pattern of the upstream table name, wildcard characters (*?) are supported.
    target-schema: "test"       # The name of the downstream schema.
    target-table: "t"           # The name of the downstream table.
  route-rule-2:
    schema-pattern: "test_*"
    target-schema: "test"

# The binlog event filter rule set of the matched table of the upstream database instance.
filters:
  filter-rule-1:                                # The name of the filtering rule.
    schema-pattern: "test_*"                    # The pattern of the upstream schema name, wildcard characters (*?) are supported.
    table-pattern: "t_*"                        # The pattern of the upstream schema name, wildcard characters (*?) are supported.
    events: ["truncate table", "drop table"]    # What event types to match.
    action: Ignore                              # Whether to migrate (Do) or ignore (Ignore) the binlog that matches the filtering rule.
  filter-rule-2:
    schema-pattern: "test_*"
    events: ["all dml"]
    action: Do

expression-filter:                   # Defines the filter rules for row changes when migrating data. Supports defining multiple rules.
  # Filter the value of inserted `c` in `expr_filter`.`tbl` when it is even.
  even_c:                            # The name of the filter rule.
    schema: "expr_filter"            # The name of upstream database to be matched. Wildcard match or regular match is not supported.
    table: "tbl"                     # The name of upstream table to be matched. Wildcard match or regular match is not supported.
    insert-value-expr: "c % 2 = 0"

# The filter rule set of tables to be migrated from the upstream database instance. You can set multiple rules at the same time.
block-allow-list:                    # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  bw-rule-1:                         # The name of the block allow list rule.
    do-dbs: ["~^test.*", "user"]     # The allow list of upstream schemas needs to be migrated.
    ignore-dbs: ["mysql", "account"] # The block list of upstream schemas needs to be migrated.
    do-tables:                       # The allow list of upstream tables needs to be migrated.
    - db-name: "~^test.*"
      tbl-name: "~^t.*"
    - db-name: "user"
      tbl-name: "information"
  bw-rule-2:                         # The name of the block allow list rule.
    ignore-tables:                   # The block list of upstream tables needs to be migrated.
    - db-name: "user"
      tbl-name: "log"

# Configuration arguments of the dump processing unit.
mydumpers:
  global:                            # The configuration name of the processing unit.
    threads: 4                       # The number of threads that access the upstream when the dump processing unit performs the precheck and exports data from the upstream database (4 by default)
    chunk-filesize: 64               # The size of the file generated by the dump processing unit (64 MB by default).
    extra-args: "--consistency none" # Other arguments of the dump processing unit. You do not need to manually configure table-list in `extra-args`, because it is automatically generated by DM.

# Configuration arguments of the load processing unit.
loaders:
  global:                            # The configuration name of the processing unit.
    pool-size: 16                    # The number of threads that concurrently execute dumped SQL files in the load processing unit (16 by default). When multiple instances are migrating data to TiDB at the same time, slightly reduce the value according to the load.
    # The directory that stores full data exported from the upstream ("./dumped_data" by default).
    # Supoprts a local filesystem path or an Amazon S3 path. For example, "s3://dm_bucket/dumped_data?region=us-west-2&endpoint=s3-website.us-east-2.amazonaws.com&access_key=s3accesskey&secret_access_key=s3secretkey&force_path_style=true"
    dir: "./dumped_data"
    # The import mode during the full import phase. In most cases you don't need to care about this configuration.
    # - "sql" (default). Use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) TiDB-backend mode to import data.
    # - "loader". Use Loader mode to import data. This mode is only for compatibility with features that TiDB Lightning does not support yet. It will be deprecated in the future.
    import-mode: "sql"
    #  Methods to resolve conflicts during the full import phase. You can set it to the following:
    # - "replace" (default). Only supports the import mode "sql". In this method, it uses the new data to replace the existing data.
    # - "ignore". Only supports the import mode "sql". It keeps the existing data, and ignores the new data.
    # - "error". Only supports the import mode "loader". It reports errors when inserting duplicated data, and then stops the replication task.
    on-duplicate: "replace"

# Configuration arguments of the sync processing unit.
syncers:
  global:                            # The configuration name of the processing unit.
    worker-count: 16                 # The number of concurrent threads that apply binlogs which have been transferred to the local (16 by default). Adjusting this parameter has no effect on the concurrency of upstream pull logs, but has a significant effect on the downstream database.
    batch: 100                       # The number of SQL statements in a transaction batch that the sync processing unit replicates to the downstream database (100 by default). Generally, it is recommended to set the value less than 500.
    enable-ansi-quotes: true         # Enable this argument if `sql-mode: "ANSI_QUOTES"` is set in the `session`

    # If set to true, `INSERT` statements from upstream are rewritten to `REPLACE` statements, and `UPDATE` statements are rewritten to `DELETE` and `REPLACE` statements. This ensures that DML statements can be imported repeatedly during data migration when there is any primary key or unique index in the table schema.
    safe-mode: false
    # If set to true, DM compacts as many upstream statements on the same rows as possible into a single statements without increasing latency.
    # For example, `INSERT INTO tb(a,b) VALUES(1,1); UPDATE tb SET b=11 WHERE a=1`;` will be compacted to `INSERT INTO tb(a,b) VALUES(1,11);`, where "a" is the primary key
    # `UPDATE tb SET b=1 WHERE a=1; UPDATE tb(a,b) SET b=2 WHERE a=1;` will be compacted to `UPDATE tb(a,b) SET b=2 WHERE a=1;`, where "a" is the primary key
    # `DELETE FROM tb WHERE a=1; INSERT INTO tb(a,b) VALUES(1,1);` will be compacted to `REPLACE INTO tb(a,b) VALUES(1,1);`, where "a" is the primary key
    compact: false
    # If set to true, DM combines as many statements of the same type as possible into a single statement and generates a single SQL statement with multiple rows of data.
    # For example, `INSERT INTO tb(a,b) VALUES(1,1); INSERT INTO tb(a,b) VALUES(2,2);` will become `INSERT INTO tb(a,b) VALUES(1,1),(2,2);`
    # `UPDATE tb SET b=11 WHERE a=1; UPDATE tb(a,b) set b=22 WHERE a=2;` will become `INSERT INTO tb(a,b) VALUES(1,11),(2,22) ON DUPLICATE KEY UPDATE a=VALUES(a), b= VALUES(b);`, where "a" is the primary key
    # `DELETE FROM tb WHERE a=1; DELETE FROM tb WHERE a=2` will become `DELETE FROM tb WHERE (a) IN (1),(2)`, where "a" is the primary key
    multiple-rows: true

# ----------- Instance configuration -----------
mysql-instances:
  -
    source-id: "mysql-replica-01"                   # The `source-id` in source.toml.
    meta:                                           # The position where the binlog replication starts when `task-mode` is `incremental` and the downstream database checkpoint does not exist. If the checkpoint exists, the checkpoint is used.

      binlog-name: binlog.000001
      binlog-pos: 4
      binlog-gtid: "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"  # You need to set this argument if you specify `enable-gtid: true` for the source of the incremental task.

    route-rules: ["route-rule-1", "route-rule-2"]   # The name of the mapping rule between the table matching the upstream database instance and the downstream database.
    filter-rules: ["filter-rule-1", "filter-rule-2"]                 # The name of the binlog event filtering rule of the table matching the upstream database instance.
    block-allow-list:  "bw-rule-1"                  # The name of the block and allow lists filtering rule of the table matching the upstream database instance. Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
    expression-filters: ["even_c"]                  # Use expression filter rule named even_c.
    mydumper-config-name: "global"                  # The name of the mydumpers configuration.
    loader-config-name: "global"                    # The name of the loaders configuration.
    syncer-config-name: "global"                    # The name of the syncers configuration.

  -
    source-id: "mysql-replica-02"                   # The `source-id` in source.toml.
    mydumper-thread: 4                              # The number of threads that the dump processing unit uses for dumping data. `mydumper-thread` corresponds to the `threads` configuration item of the mydumpers configuration. `mydumper-thread` has overriding priority when the two items are both configured.
    loader-thread: 16                               # The number of threads that the load processing unit uses for loading data. `loader-thread` corresponds to the `pool-size` configuration item of the loaders configuration. `loader-thread` has overriding priority when the two items are both configured. When multiple instances are migrating data to TiDB at the same time, reduce the value according to the load.
    syncer-thread: 16                               # The number of threads that the sync processing unit uses for replicating incremental data. `syncer-thread` corresponds to the `worker-count` configuration item of the syncers configuration. `syncer-thread` has overriding priority when the two items are both configured. When multiple instances are migrating data to TiDB at the same time, reduce the value according to the load.
```

## Configuration order

1. Edit the [global configuration](#global-configuration).
2. Edit the [instance configuration](#instance-configuration) based on the global configuration.

## Global configuration

### Basic configuration

Refer to the comments in the [template](#task-configuration-file-template-advanced) to see more details. Detailed explanations about `task-mode` are as follows:

- Description: the task mode that can be used to specify the data migration task to be executed.
- Value: string (`full`, `incremental`, or `all`).
    - `full` only makes a full backup of the upstream database and then imports the full data to the downstream database.
    - `incremental`: Only replicates the incremental data of the upstream database to the downstream database using the binlog. You can set the `meta` configuration item of the instance configuration to specify the starting position of incremental replication.
    - `all`: `full` + `incremental`. Makes a full backup of the upstream database, imports the full data to the downstream database, and then uses the binlog to make an incremental replication to the downstream database starting from the exported position during the full backup process (binlog position).

### Feature configuration set

Arguments in each feature configuration set are explained in the comments in the [template](#task-configuration-file-template-advanced).

| Parameter        | Description                                    |
| :------------ | :--------------------------------------- |
| `routes` | The routing mapping rule set between the upstream and downstream tables. If the names of the upstream and downstream schemas and tables are the same, this item does not need to be configured. See [Table Routing](/dm/dm-key-features.md#table-routing) for usage scenarios and sample configurations. |
| `filters` | The binlog event filter rule set of the matched table of the upstream database instance. If binlog filtering is not required, this item does not need to be configured. See [Binlog Event Filter](/dm/dm-key-features.md#binlog-event-filter) for usage scenarios and sample configurations. |
| `block-allow-list` | The filter rule set of the block allow list of the matched table of the upstream database instance. It is recommended to specify the schemas and tables that need to be migrated through this item, otherwise all schemas and tables are migrated. See [Binlog Event Filter](/dm/dm-key-features.md#binlog-event-filter) and [Block & Allow Lists](/dm/dm-key-features.md#block-and-allow-table-lists) for usage scenarios and sample configurations. |
| `mydumpers` | Configuration arguments of dump processing unit. If the default configuration is sufficient for your needs, this item does not need to be configured. Or you can configure `thread` only using `mydumper-thread`. |
| `loaders` | Configuration arguments of load processing unit. If the default configuration is sufficient for your needs, this item does not need to be configured. Or you can configure `pool-size` only using `loader-thread`. |
| `syncers` | Configuration arguments of sync processing unit. If the default configuration is sufficient for your needs, this item does not need to be configured. Or you can configure `worker-count` only using `syncer-thread`. |

## Instance configuration

This part defines the subtask of data migration. DM supports migrating data from one or multiple MySQL instances in the upstream to the same instance in the downstream.

For the configuration details of the above options, see the corresponding part in [Feature configuration set](#feature-configuration-set), as shown in the following table.

| Option | Corresponding part |
| :------ | :------------------ |
| `route-rules` | `routes` |
| `filter-rules` | `filters` |
| `block-allow-list` | `block-allow-list` |
| `mydumper-config-name` | `mydumpers` |
| `loader-config-name` | `loaders` |
| `syncer-config-name` | `syncers`  |

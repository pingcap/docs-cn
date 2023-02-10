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
    # Optional. Used for extracting the source information of sharded schemas and tables and writing the information to the user-defined columns in the downstream. If these options are configured, you need to manually create a merged table in the downstream. For details, see description of table routing in <https://docs.pingcap.com/tidb/dev/dm-table-routing>.
    # extract-table:                                        # Extracts and writes the table name suffix without the t_ part to the c-table column of the merged table. For example, 01 is extracted and written to the c-table column for the sharded table t_01.
    #   table-regexp: "t_(.*)"
    #   target-column: "c_table"
    # extract-schema:                                       # Extracts and writes the schema name suffix without the test_ part to the c_schema column of the merged table. For example, 02 is extracted and written to the c_schema column for the sharded schema test_02.
    #   schema-regexp: "test_(.*)"
    #   target-column: "c_schema"
    # extract-source:                                       # Extracts and writes the source instance information to the c_source column of the merged table. For example, mysql-replica-01 is extracted and written to the c_source column for the data source mysql-replica-01.
    #   source-regexp: "(.*)"
    #   target-column: "c_source"
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
    # Supoprts a local filesystem path or an Amazon S3 path. For example, "s3://dm_bucket/dumped_data?endpoint=s3-website.us-east-2.amazonaws.com&access_key=s3accesskey&secret_access_key=s3secretkey&force_path_style=true"
    dir: "./dumped_data"

    # The import mode during the full import phase. The following modes are supported:
    # - "logical" (default). Uses TiDB Lightning's logical import mode to import data. Document: https://docs.pingcap.com/tidb/stable/tidb-lightning-logical-import-mode
    # - "physical". Uses TiDB Lightning's physical import mode to import data. Document: https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-physical-import-mode
    #   The "physical" mode is still an experimental feature and is not recommended in production.
    import-mode: "logical"
    #  Methods to resolve conflicts in logical import.
    # - "replace" (default). Uses the new data to replace the existing data.
    # - "ignore". Keeps the existing data, and ignores the new data.
    # - "error". Reports errors when inserting duplicated data, and then stops the replication task.
    on-duplicate-logical: "replace"

    #  Methods to resolve conflicts in physical import.
    # - "none". Corresponds to the "none" strategy of conflict detection in TiDB Lightning's physical import.
    #   (https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode-usage#conflict-detection).
    #   Conflicting data is not resolved in this method. "none" has the best performance, but
    #   might lead to inconsistent data in the downstream database.
    # - "manual". Corresponds to the "remove" strategy of conflict detection in TiDB Lightning's physical import.
    #   (https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode-usage#conflict-detection).
    #   When the import encounter conflicting data, DM removes all conflicting records from
    #   the target table and records the data in the `${meta-schema}_${name}.conflict_error_v1`
    #   table. In this configuration file, the conflicting data is recorded in the
    #   `dm_meta_test.conflict_error_v1` table. When the full import phase is completed, the
    #   tasks is paused and you are prompted to query this table and manually resolve the
    #   conflicts. You need to resume the task and enter the incremental phase using the `resume-task` command.
    on-duplicate-physical: "none"
    # The directory used for local KV sorting in the physical import mode. The default value of this
    # configuration is the same as the `dir` configuration. For details, refer to TiDB Lightning document: https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode#environment-requirements
    sorting-dir-physical: "./dumped_data"
    # Disk quota. Corresponds to the disk-quota configuration of TiDB Lightning. For details, refer to TiDB Lightning document: https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode-usage#configure-disk-quota-new-in-v620
    disk-quota-physical: "0"
    # DM performs `ADMIN CHECKSUM TABLE <table>` for each table to verify data integrity after the import.
    # - "required" (default): performs admin checksum after the import. If checksum fails,
    #   DM pauses the task and you need to manually handle the failure.
    # - "optional": performs admin checksum after the import. If checksum fails, DM logs a
    #   warning and continues to migrate data. The task is not paused.
    # - "off": does not perform admin checksum after the import.
    # If checksum fails, the import is abnormal, which means the data is inconsistent or lost.
    # Therefore, it is recommended to always enable checksum.
    checksum-physical: "required"

# Configuration arguments of the sync processing unit.
syncers:
  global:                            # The configuration name of the processing unit.
    worker-count: 16                 # The number of concurrent threads that apply binlogs which have been transferred to the local (16 by default). Adjusting this parameter has no effect on the concurrency of upstream pull logs, but has a significant effect on the downstream database.
    batch: 100                       # The number of SQL statements in a transaction batch that the sync processing unit replicates to the downstream database (100 by default). Generally, it is recommended to set the value less than 500.
    enable-ansi-quotes: true         # Enable this argument if `sql-mode: "ANSI_QUOTES"` is set in the `session`

    # If set to true, `INSERT` statements from upstream are rewritten to `REPLACE` statements, and `UPDATE` statements are rewritten to `DELETE` and `REPLACE` statements. This ensures that DML statements can be imported repeatedly during data migration when there is any primary key or unique index in the table schema.
    safe-mode: false
    # The duration of the automatic safe mode.
    # If this value is not set or set to "", the default value is twice of `checkpoint-flush-interval` (30s by default), which is 60s.
    # If this value is set to "0s", DM reports an error when it automatically enters the safe mode.
    # If this value is set to a normal value, such as "1m30s", when the task pauses abnormally, when DM fails to
    # record safemode_exit_point, or when DM exits unexpectedly, the duration of the automatic safe mode is set to
    # 1 minute 30 seconds.
    safe-mode-duration: "60s"

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

# Configuration arguments of continuous data validation (validator).
validators:
  global:                # Configuration name.
    # full: validates the data in each row is correct.
    # fast: validates whether the row is successfully migrated to the downstream.
    # none: does not validate the data.
    mode: full           # Possible values are "full", "fast", and "none". The default value is "none", which does not validate the data.
    worker-count: 4      # The number of validation workers in the background. The default value is 4.
    row-error-delay: 30m # If a row cannot pass the validation within the specified time, it will be marked as an error row. The default value is 30m, which means 30 minutes.

# ----------- Instance configuration -----------
mysql-instances:
  -
    source-id: "mysql-replica-01"                   # The `source-id` in source.toml.
    meta:                                           # The position where the binlog replication starts when `task-mode` is `incremental` and the downstream database checkpoint does not exist. If the checkpoint exists, the checkpoint is used. If neither the `meta` configuration item nor the downstream database checkpoint exists, the migration starts from the latest binlog position of the upstream.

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
    validator-config-name: "global"                 # The name of the validators configuration.

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
| `routes` | The routing mapping rule set between the upstream and downstream tables. If the names of the upstream and downstream schemas and tables are the same, this item does not need to be configured. See [Table Routing](/dm/dm-table-routing.md) for usage scenarios and sample configurations. |
| `filters` | The binlog event filter rule set of the matched table of the upstream database instance. If binlog filtering is not required, this item does not need to be configured. See [Binlog Event Filter](/dm/dm-binlog-event-filter.md) for usage scenarios and sample configurations. |
| `block-allow-list` | The filter rule set of the block allow list of the matched table of the upstream database instance. It is recommended to specify the schemas and tables that need to be migrated through this item, otherwise all schemas and tables are migrated. See [Binlog Event Filter](/dm/dm-binlog-event-filter.md) and [Block & Allow Lists](/dm/dm-block-allow-table-lists.md) for usage scenarios and sample configurations. |
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

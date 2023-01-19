---
title: Data Migration Task Configuration Guide
summary: Learn how to configure a data migration task in Data Migration (DM).
---

# Data Migration Task Configuration Guide

This document introduces how to configure a data migration task in Data Migration (DM).

## Configure data sources to be migrated

Before configuring the data sources to be migrated for the task, you need to first make sure that DM has loaded the configuration files of the corresponding data sources. The following are some operation references:

- To view the data source, you can refer to [Check the data source configuration](/dm/dm-manage-source.md#check-data-source-configurations).
- To create a data source, you can refer to [Create data source](/dm/migrate-data-using-dm.md#step-3-create-data-source).
- To generate a data source configuration file, you can refer to [Source configuration file introduction](/dm/dm-source-configuration-file.md).

The following example of `mysql-instances` shows how to configure data sources that need to be migrated for the data migration task:

```yaml
---

## ********* Basic configuration *********
name: test             # The name of the task. Should be globally unique.

## ******** Data source configuration **********
mysql-instances:
  - source-id: "mysql-replica-01"  # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
  - source-id: "mysql-replica-02"  # Migrate data from the data source whose `source-id` is `mysql-replica-02`.
```

## Configure the downstream TiDB cluster

The following example of `target-database` shows how to configure the target TiDB cluster to be migrated to for the data migration task:

```yaml
---

## ********* Basic configuration *********
name: test             # The name of the task. Should be globally unique.

## ******** Data source configuration **********
mysql-instances:
  - source-id: "mysql-replica-01"  # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
  - source-id: "mysql-replica-02"  # Migrate data from the data source whose `source-id` is `mysql-replica-02`.

## ******** Downstream TiDB database configuration **********
target-database:       # Configuration of target TiDB database.
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""         # If the password is not null, it is recommended to use a password encrypted with dmctl.
```

## Configure tables to be migrated

> **Note:**
>
> If you do not need to filter specific tables or migrate specific tables, skip this configuration.

To configure the block and allow list of data source tables for the data migration task, perform the following steps:

1. Configure a global filter rule set of the block and allow list in the task configuration file.

    ```yaml
    block-allow-list:
      bw-rule-1:                           # The name of the block and allow list rule.
        do-dbs: ["test.*", "user"]         # The allow list of upstream schemas to be migrated. Wildcard characters (*?) are supported. You only need to configure either `do-dbs` or `ignore-dbs`. If both fields are configured, only `do-dbs` takes effect.
        # ignore-dbs: ["mysql", "account"] # The block list of upstream schemas to be migrated. Wildcard characters (*?) are supported.
        do-tables:                         # The allow list of upstream tables to be migrated. You only need to configure either `do-tables` or `ignore-tables`. If both fields are configured, only `do-tables` takes effect.
        - db-name: "test.*"
          tbl-name: "t.*"
        - db-name: "user"
          tbl-name: "information"
      bw-rule-2:                          # The name of the block allow list rule.
        ignore-tables:                    # The block list of data source tables needs to be migrated.
        - db-name: "user"
          tbl-name: "log"
    ```

    For detailed configuration rules, see [Block and allow table lists](/dm/dm-block-allow-table-lists.md).

2. Reference the block and allow list rules in the data source configuration to filter tables to be migrated.

    ```yaml
    mysql-instances:
      - source-id: "mysql-replica-01"  # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
        block-allow-list:  "bw-rule-1" # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
      - source-id: "mysql-replica-02"  # Migrate data from the data source whose `source-id` is `mysql-replica-02`.
        block-allow-list:  "bw-rule-2" # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
    ```

## Configure binlog events to be migrated

> **Note:**
>
> If you do not need to filter specific binlog events of certain schemas or tables, skip this configuration.

To configure the filters of binlog events for the data migration task, perform the following steps:

1. Configure a global filter rule set of binlog events in the task configuration file.

    ```yaml
    filters:                                        # The filter rule set of data source binlog events. You can set multiple rules at the same time.
      filter-rule-1:                                # The name of the filtering rule.
        schema-pattern: "test_*"                    # The pattern of the data source schema name. Wildcard characters (*?) are supported.
        table-pattern: "t_*"                        # The pattern of the data source table name. Wildcard characters (*?) are supported.
        events: ["truncate table", "drop table"]    # The event types to be filtered out in schemas or tables that match the `schema-pattern` or the `table-pattern`.
        action: Ignore                              # Whether to migrate (Do) or ignore (Ignore) the binlog that matches the filtering rule.
      filter-rule-2:
        schema-pattern: "test"
        events: ["all dml"]
        action: Do
    ```

    For detailed configuration rules, see [Binlog event filter](/dm/dm-binlog-event-filter.md).

2. Reference the binlog event filtering rules in the data source configuration to filter specified binlog events of specified tables or schemas in the data source.

    ```yaml
    mysql-instances:
      - source-id: "mysql-replica-01"    # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
        block-allow-list:  "bw-rule-1"   # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
        filter-rules: ["filter-rule-1"]  # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
      - source-id: "mysql-replica-02"    # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
        block-allow-list:  "bw-rule-2"   # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
        filter-rules: ["filter-rule-2"]  # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
    ```

## Configure the mapping of data source tables to downstream TiDB tables

> **Note:**
>
> - If you do not need to migrate a certain table of the data source to the table with a different name in the downstream TiDB instance, skip this configuration.
>
> - If it is a shard merge task, you **must** set mapping rules in the task configuration file.

To configure the routing mapping rules for migrating data source tables to specified downstream TiDB tables, perform the following steps:

1. Configure a global routing mapping rule set in the task configuration file.

    ```yaml
    routes:                           # The routing mapping rule set between the data source tables and downstream TiDB tables. You can set multiple rules at the same time.
      route-rule-1:                   # The name of the routing mapping rule.
        schema-pattern: "test_*"      # The pattern of the upstream schema name. Wildcard characters (*?) are supported.
        table-pattern: "t_*"          # The pattern of the upstream table name. Wildcard characters (*?) are supported.
        target-schema: "test"         # The name of the downstream TiDB schema.
        target-table: "t"             # The name of the downstream TiDB table.
      route-rule-2:
        schema-pattern: "test_*"
        target-schema: "test"
    ```

    For detailed configuration rules, see [Table Routing](/dm/dm-table-routing.md).

2. Reference the routing mapping rules in the data source configuration to filter tables to be migrated.

    ```yaml
    mysql-instances:
      - source-id: "mysql-replica-01"                     # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
        block-allow-list:  "bw-rule-1"                    # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
        filter-rules: ["filter-rule-1"]                   # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
        route-rules: ["route-rule-1", "route-rule-2"]     # The name of the routing mapping rule. You can configure multiple rules here.
      - source-id: "mysql-replica-02"                     # Migrate data from the data source whose `source-id` is `mysql-replica-02`.
        block-allow-list:  "bw-rule-2"                    # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
        filter-rules: ["filter-rule-2"]                   # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
    ```

## Configure a shard merge task

> **Note:**
>
> - If you need to migrate sharding DDL statements in a shard merge scenario, you **must** explicitly configure the `shard-mode` field. Otherwise, **DO NOT** configure `shard-mode` at all.
>
> - Migrating sharding DDL statements is likely to cause many issues. Make sure you understand the principles and restrictions of DM migrating DDL statements before using this feature, and you **must** use this feature with caution.

The following example shows how to configure the task as a shard merge task:

```yaml
---

## ********* Basic information *********
name: test                      # The name of the task. Should be globally unique.
shard-mode: "pessimistic"       # The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic" mode. After getting a deep understanding of the principles and restrictions of the "optimistic" mode, you can set it to the "optimistic" mode.
```

## Other configurations

The following is an overall task configuration example of this document. The complete task configuration template can be found in [DM task configuration file full introduction](/dm/task-configuration-file-full.md).

```yaml
---

## ********* Basic configuration *********
name: test                      # The name of the task. Should be globally unique.
shard-mode: "pessimistic"       # The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic" mode. After getting a deep understanding of the principles and restrictions of the "optimistic" mode, you can set it to the "optimistic" mode.
task-mode: all                  # The task mode. Can be set to `full`(only migrates full data)/`incremental`(replicates binlog synchronously)/`all` (replicates both full and incremental binlogs).
timezone: "UTC"               # The timezone used in SQL Session. By default, DM uses the global timezone setting in the target cluster, which ensures the correctness automatically. A customized timezone does not affect data migration but is unnecessary.

## ******** Data source configuration **********
mysql-instances:
  - source-id: "mysql-replica-01"                   # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
    block-allow-list:  "bw-rule-1"                  # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
    filter-rules: ["filter-rule-1"]                 # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
    route-rules: ["route-rule-1", "route-rule-2"]   # The name of the routing mapping rule. You can configure multiple rules here.
  - source-id: "mysql-replica-02"                   # Migrate data from the data source whose `source-id` is `mysql-replica-02`.
    block-allow-list:  "bw-rule-2"                  # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
    filter-rules: ["filter-rule-2"]                 # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
    route-rules: ["route-rule-2"]                   # The name of the routing mapping rule. You can configure multiple rules here.

## ******** Downstream TiDB instance configuration **********
target-database:       # Configuration of the downstream database instance.
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""         # If the password is not null, it is recommended to use a password encrypted with dmctl.

## ******** Feature configuration set **********
# The filter rule set of tables to be migrated from the upstream database instance. You can set multiple rules at the same time.
block-allow-list:                      # Use black-white-list if the DM version is earlier than v2.0.0-beta.2.
  bw-rule-1:                           # The name of the block and allow list rule.
    do-dbs: ["test.*", "user"]         # The allow list of upstream schemas to be migrated. Wildcard characters (*?) are supported. You only need to configure either `do-dbs` or `ignore-dbs`. If both fields are configured, only `do-dbs` takes effect.
    # ignore-dbs: ["mysql", "account"] # The block list of upstream schemas to be migrated. Wildcard characters (*?) are supported.
    do-tables:                         # The allow list of upstream tables to be migrated. You only need to configure either `do-tables` or `ignore-tables`. If both fields are configured, only `do-tables` takes effect.
    - db-name: "test.*"
      tbl-name: "t.*"
    - db-name: "user"
      tbl-name: "information"
  bw-rule-2:                         # The name of the block allow list rule.
    ignore-tables:                   # The block list of data source tables needs to be migrated.
    - db-name: "user"
      tbl-name: "log"

# The filter rule set of data source binlog events.
filters:                                        # You can set multiple rules at the same time.
  filter-rule-1:                                # The name of the filtering rule.
    schema-pattern: "test_*"                    # The pattern of the data source schema name. Wildcard characters (*?) are supported.
    table-pattern: "t_*"                        # The pattern of the data source table name. Wildcard characters (*?) are supported.
    events: ["truncate table", "drop table"]    # The event types to be filtered out in schemas or tables that match the `schema-pattern` or the `table-pattern`.
    action: Ignore                              # Whether to migrate (Do) or ignore (Ignore) the binlog that matches the filtering rule.
  filter-rule-2:
    schema-pattern: "test"
    events: ["all dml"]
    action: Do

# The routing mapping rule set between the data source and target TiDB instance tables.
routes:                           # You can set multiple rules at the same time.
  route-rule-1:                   # The name of the routing mapping rule.
    schema-pattern: "test_*"      # The pattern of the data source schema name. Wildcard characters (*?) are supported.
    table-pattern: "t_*"          # The pattern of the data source table name. Wildcard characters (*?) are supported.
    target-schema: "test"         # The name of the downstream TiDB schema.
    target-table: "t"             # The name of the downstream TiDB table.
  route-rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

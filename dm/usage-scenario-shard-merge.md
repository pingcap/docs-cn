---
title: Data Migration Shard Merge Scenario
summary: Learn how to use Data Migration to migrate data in the shard merge scenario.
aliases: ['/docs/tidb-data-migration/dev/usage-scenario-shard-merge/']
---

# Data Migration Shard Merge Scenario

This document shows how to use Data Migration (DM) to migrate data to the downstream TiDB in the shard merge scenario.

The example used in this document is a simple scenario where sharded schemas and sharded tables of two data source MySQL instances need to be migrated to a downstream TiDB cluster.

For other scenarios, you can refer to [Best Practices of Data Migration in the Shard Merge Scenario](/dm/shard-merge-best-practices.md).

## Data source instances

Assume that the data source structures are as follows:

- Instance 1

    | Schema | Tables |
    |:------|:------|
    | user  | information, log_bak |
    | store_01 | sale_01, sale_02 |
    | store_02 | sale_01, sale_02 |

- Instance 2

    | Schema | Tables |
    |:------|:------|
    | user  | information, log_bak |
    | store_01 | sale_01, sale_02 |
    | store_02 | sale_01, sale_02 |

## Migration requirements

1. Merge the `user`.`information` tables to the downstream `user`.`information` table in TiDB.
2. Merge the `store_{01|02}`.`sale_{01|02}` tables in the above instances to the downstream `store`.`sale` table in TiDB.
3. Replicate `user` and `store_{01|02}` schemas but do not replicate the `user`.`log_bak` tables in the above instances.
4. Filter out all the delete operations in the `store_{01|02}`.`sale_{01|02}` table of the above instances and filter out the `drop database` operation in shemas.

The expected downstream schema after migration is as follows:

| Schema | Tables |
|:------|:------|
| user | information |
| store | sale |

## Conflict check across sharded tables

Because migration requirements #1 and #2 involve the DM Shard Merge feature, data from multiple tables might cause conflicts between the primary keys or the unique keys. You need to check these sharded tables. For details, refer to [Handle conflicts between primary keys or unique indexes across multiple sharded tables](/dm/shard-merge-best-practices.md#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables). In this example:

The table schema of `user`.`information` is

```sql
CREATE TABLE `information` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `data` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

In the above structure, column `id` is the primary key and column `uid` is the unique index. Column `id` has auto-increment attribute and if the ranges of tables overlap, data conflicts might occur. Column `uid` can ensure only a unique index exists globally. So, you can avoid column `id` by following the steps in the section [Remove the `PRIMARY KEY` attribute from the column](/dm/shard-merge-best-practices.md#remove-the-primary-key-attribute-from-the-column).

The table schema of `store_{01|02}`.`sale_{01|02}` is

```sql
CREATE TABLE `sale_01` (
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`sid`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

In the above structure, `sid` is the shard key, which can ensure that the same `sid` only exists in one sharded table. So no data conflict is caused and you do not need to perform extra operations.

## Migration solution

- To satisfy the migration requirements #1, you do not need to configure the [table routing rule](/dm/dm-key-features.md#table-routing). You need to manually create a table based on the requirements in the section [Remove the `PRIMARY KEY` attribute from the column](/dm/shard-merge-best-practices.md#remove-the-primary-key-attribute-from-the-column):

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE `information` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `uid` bigint(20) DEFAULT NULL,
      `name` varchar(255) DEFAULT NULL,
      `data` varchar(255) DEFAULT NULL,
      INDEX (`id`),
      UNIQUE KEY `uid` (`uid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```
    
    And skip precheck in the configuration file:
    
    {{< copyable "" >}}

    ```yaml
    ignore-checking-items: ["auto_increment_ID"]
    ```

- To satisfy the migration requirement #2, configure the [table routing rule](/dm/dm-key-features.md#table-routing) as follows:

    {{< copyable "" >}}

    ```yaml
    routes:
      ...
      store-route-rule:
        schema-pattern: "store_*"
        target-schema: "store"
      sale-route-rule:
        schema-pattern: "store_*"
        table-pattern: "sale_*"
        target-schema: "store"
        target-table:  "sale"
    ```

- To satisfy the migration requirements #3, configure the [Block and allow table lists](/dm/dm-key-features.md#block-and-allow-table-lists) as follows:

    {{< copyable "" >}}

    ```yaml
    block-allow-list:
      log-bak-ignored:
        do-dbs: ["user", "store_*"]
        ignore-tables:
        - db-name: "user"
          tbl-name: "log_bak"
    ```

- To satisfy the migration requirement #4, configure the [binlog event filter rule](/dm/dm-key-features.md#binlog-event-filter) as follows:

    {{< copyable "" >}}

    ```yaml
    filters:
      ...
      sale-filter-rule:     # filter out all deletion operations of all tables under store_* schema
        schema-pattern: "store_*"
        table-pattern: "sale_*"
        events: ["truncate table", "drop table", "delete"]
        action: Ignore
      store-filter-rule:   # filter out the deletion operation of store_* schema
        schema-pattern: "store_*"
        events: ["drop database"]
        action: Ignore
    ```

## Migration task configuration

The complete configuration of the migration task is shown as follows. For more details, see [Data Migration Task Configuration Guide](/dm/dm-task-configuration-guide.md).

{{< copyable "" >}}

```yaml
name: "shard_merge"
task-mode: all                      # full data migration + incremental data migration
meta-schema: "dm_meta"
ignore-checking-items: ["auto_increment_ID"]

target-database:
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""

mysql-instances:
  -
    source-id: "instance-1"  # The ID of the data source and can be obtained from the data source configuration
    route-rules: ["store-route-rule", "sale-route-rule"] # Applies to the table route rules of this data source
    filter-rules: ["store-filter-rule" , "sale-filter-rule"] # Applies to the binlog event filter rules of this data source
    block-allow-list:  "log-bak-ignored"  # Applies to the block and allow lists of this data source
  -
    source-id: "instance-2"
    route-rules: ["store-route-rule", "sale-route-rule"]
    filter-rules: ["store-filter-rule", "sale-filter-rule"]
    block-allow-list:  "log-bak-ignored"

# Other common configs shared by all instances

routes:
  store-route-rule:
    schema-pattern: "store_*"
    target-schema: "store"
  sale-route-rule:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    target-schema: "store"
    target-table:  "sale"

filters:
  sale-filter-rule:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  store-filter-rule:
    schema-pattern: "store_*"
    events: ["drop database"]
    action: Ignore

block-allow-list:
  log-bak-ignored:
    do-dbs: ["user", "store_*"]
    ignore-tables:
    - db-name: "user"
      tbl-name: "log_bak"
```

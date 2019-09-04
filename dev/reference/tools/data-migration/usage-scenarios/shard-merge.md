---
title: Data Migration Shard Merge Scenario
summary: Learn how to use Data Migration to replicate data in the shard merge scenario.
category: reference
---

# Data Migration Shard Merge Scenario

This document shows how to use Data Migration (DM) in the shard merge scenario where the sharded schemas and sharded tables data of three upstream MySQL instances need to be replicated to a downstream TiDB cluster.

## Upstream instances

Assume that the upstream schemas are as follows:

- Instance 1

    | Schema | Tables|
    |:------|:------|
    | user  | information, log_north, log_bak |
    | store_01 | sale_01, sale_02 |
    | store_02 | sale_01, sale_02 |

- Instance 2

    | Schema | Tables|
    |:------|:------|
    | user  | information, log_east, log_bak |
    | store_01 | sale_01, sale_02 |
    | store_02 | sale_01, sale_02 |

- Instance 3

    | Schema | Tables|
    |:------|:------|
    | user  | information, log_south, log_bak |
    | store_01 | sale_01, sale_02 |
    | store_02 | sale_01, sale_02 |

## Replication requirements

1. Merge the `user`.`information` table of three upstream instances to the downstream `user`.`information` table in TiDB.
2. Merge the `user`.`log_{north|south|east}` table of three upstream instances to the downstream `user`.`log_{north|south|east}` table in TiDB.
3. Merge the `store_{01|02}`.`sale_{01|02}` table of three upstream instances to the downstream `store`.`sale` table in TiDB.
4. Filter out all the deletion operations in the `user`.`log_{north|south|east}` table of three upstream instances.
5. Filter out all the deletion operations in the `user`.`information` table of three upstream instances.
6. Filter out all the deletion operations in the `store_{01|02}`.`sale_{01|02}` table of three upstream instances.
7. Filter out the `user`.`log_bak` table of three upstream instances.
8. Because the `store_{01|02}`.`sale_{01|02}` tables have auto-increment primary keys of the bigint type, the conflict occurs when these tables are merged into TiDB. So you need to modify the auto-increment primary keys to avoid the conflict.

## Downstream instances

Assume that the downstream schema after replication is as follows:

| Schema | Tables |
|:------|:------|
| user | information, log_north, log_east, log_south|
| store | sale |

## Replication solution

- To satisfy the replication Requirements #1 and #2, configure the [table routing rule](/dev/reference/tools/data-migration/features/overview.md#table-routing) as follows:

    ```yaml
    routes:
      ...
      user-route-rule:
        schema-pattern: "user"
        target-schema: "user"
    ```

- To satisfy the replication Requirement #3, configure the [table routing rule](/dev/reference/tools/data-migration/features/overview.md#table-routing) as follows:

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

- To satisfy the replication Requirements #4 and #5, configure the [binlog event filtering rule](/dev/reference/tools/data-migration/features/overview.md#binlog-event-filtering) as follows:

    ```yaml
    filters:
      ...
      user-filter-rule:
        schema-pattern: "user"
        events: ["truncate table", "drop table", "delete", "drop database"]
        action: Ignore
    ```

    > **Note:**
    >
    > The replication Requirements #4, #5 and #7 indicate that all the deletion operations in the `user` schema are filtered out, so a schema level filtering rule is configured here. However, the deletion operations of future tables in the `user` schema will also be filtered out.

- To satisfy the replication Requirement #6, configure the [binlog event filter rule](/dev/reference/tools/data-migration/features/overview.md#binlog-event-filter) as follows:

    ```yaml
    filters:
      ...
      sale-filter-rule:
        schema-pattern: "store_*"
        table-pattern: "sale_*"
        events: ["truncate table", "drop table", "delete"]
        action: Ignore
      store-filter-rule:
        schema-pattern: "store_*"
        events: ["drop database"]
        action: Ignore
    ```

- To satisfy the replication Requirement #7, configure the [black and white table lists](/dev/reference/tools/data-migration/features/overview.md#black-and-white-table-lists) as follows:

    ```yaml
    black-white-list:
      log-bak-ignored:
        ignore-tales:
        - db-name: "user"
          tbl-name: "log_bak"
    ```

- To satisfy the replication Requirement #8, configure the [column mapping rule](/dev/reference/tools/data-migration/features/overview.md#column-mapping) as follows:

    ```yaml
    column-mappings:
      instance-1-sale:
        schema-pattern: "store_*"
        table-pattern: "sale_*"
        expression: "partition id"
        source-column: "id"
        target-column: "id"
        arguments: ["1", "store", "sale", "_"]
      instance-2-sale:
        schema-pattern: "store_*"
        table-pattern: "sale_*"
        expression: "partition id"
        source-column: "id"
        target-column: "id"
        arguments: ["2", "store", "sale", "_"]
      instance-3-sale:
        schema-pattern: "store_*"
        table-pattern: "sale_*"
        expression: "partition id"
        source-column: "id"
        target-column: "id"
        arguments: ["3", "store", "sale", "_"]
    ```

## Replication task configuration

The complete configuration of the replication task is shown as below. For more details, see [Data Migration Task Configuration File](/dev/reference/tools/data-migration/configure/task-configuration-file.md).

```yaml
name: "shard_merge"
task-mode: all
meta-schema: "dm_meta"
remove-meta: false

target-database:
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""

mysql-instances:
  -
    source-id: "instance-1"
    route-rules: ["user-route-rule", "store-route-rule", "sale-route-rule"]
    filter-rules: ["user-filter-rule", "store-filter-rule" , "sale-filter-rule"]
    column-mapping-rules: ["instance-1-sale"]
    black-white-list:  "log-bak-ignored"
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"

  -
    source-id: "instance-2"
    route-rules: ["user-route-rule", "store-route-rule", "sale-route-rule"]
    filter-rules: ["user-filter-rule", "store-filter-rule" , "sale-filter-rule"]
    column-mapping-rules: ["instance-2-sale"]
    black-white-list:  "log-bak-ignored"
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"
  -
    source-id: "instance-3"
    route-rules: ["user-route-rule", "store-route-rule", "sale-route-rule"]
    filter-rules: ["user-filter-rule", "store-filter-rule" , "sale-filter-rule"]
    column-mapping-rules: ["instance-3-sale"]
    black-white-list:  "log-bak-ignored"
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"

# Other common configs shared by all instances.

routes:
  user-route-rule:
    schema-pattern: "user"
    target-schema: "user"
  store-route-rule:
    schema-pattern: "store_*"
    target-schema: "store"
  sale-route-rule:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    target-schema: "store"
    target-table:  "sale"

filters:
  user-filter-rule:
    schema-pattern: "user"
    events: ["truncate table", "drop table", "delete", "drop database"]
    action: Ignore
  sale-filter-rule:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  store-filter-rule:
    schema-pattern: "store_*"
    events: ["drop database"]
    action: Ignore

black-white-list:
  log-bak-ignored:
    ignore-tales:
    - db-name: "user"
      tbl-name: "log_bak"

column-mappings:
  instance-1-sale:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    expression: "partition id"
    source-column: "id"
    target-column: "id"
    arguments: ["1", "store", "sale", "_"]
  instance-2-sale:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    expression: "partition id"
    source-column: "id"
    target-column: "id"
    arguments: ["2", "store", "sale", "_"]
  instance-3-sale:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    expression: "partition id"
    source-column: "id"
    target-column: "id"
    arguments: ["3", "store", "sale", "_"]

mydumpers:
  global:
    threads: 4
    chunk-filesize: 64
    skip-tz-utc: true

loaders:
  global:
    pool-size: 16
    dir: "./dumped_data"

syncers:
  global:
    worker-count: 16
    batch: 100
    max-retry: 100
```

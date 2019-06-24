---
title: Data Migration Simple Usage Scenario
summary: Learn how to use Data Migration to replicate data in a simple scenario.
category: reference
aliases: ['/docs/tools/dm/simple-synchronization-scenario/', '/docs/dev/reference/tools/data-migration/usage-scenarios/simple-synchronization/']
---

# Data Migration Simple Usage Scenario

This document shows how to use Data Migration (DM) in a simple data replication scenario where the data of three upstream MySQL instances needs to be replicated to a downstream TiDB cluster (no sharding data).

## Upstream instances

Assume that the upstream schemas are as follows:

- Instance 1

    | Schema | Tables|
    |:------|:------|
    | user  | information, log|
    | store | store_bj, store_tj |
    | log   | messages |

- Instance 2

    | Schema | Tables|
    |:------|:------|
    | user  | information, log|
    | store | store_sh, store_sz |
    | log   | messages |

- Instance 3

    | Schema | Tables|
    |:------|:------|
    | user  | information, log|
    | store | store_gz, store_sz |
    | log   | messages |

## Replication requirements

1. Do not merge the `user` schema.
    1. Replicate the `user` schema of instance 1 to the `user_north` of TiDB.
    2. Replicate the `user` schema of instance 2 to the `user_east` of TiDB.
    3. Replicate the `user` schema of instance 3 to the `user_south` of TiDB.
    4. Never delete the table `log`.
2. Replicate the upstream `store` schema to the downstream `store` schema without merging tables.
    1. `store_sz` exists in both instances 2 and 3, which is replicated to `store_suzhou` and `store_shenzhen` respectively.
    2. Never delete `store`.
3. The `log` schema needs to be filtered out.

## Downstream instances

Assume that the schemas replicated to the downstream are as follows:

| Schema | Tables|
|:------|:------|
| user_north | information, log|
| user_east  | information, log|
| user_south | information, log|
| store | store_bj, store_tj, store_sh, store_suzhou, store_gz, store_shenzhen |

## Replication solution

- To satisfy replication Requirements #1-i, #1-ii and #1-iii, configure the [table routing rules](/reference/tools/data-migration/features/overview.md#table-routing) as follows:

    ```yaml
    routes:
      ...
      instance-1-user-rule:
        schema-pattern: "user"
        target-schema: "user_north"
      instance-2-user-rule:
        schema-pattern: "user"
        target-schema: "user_east"
      instance-3-user-rule:
        schema-pattern: "user"
        target-schema: "user_south"
    ```

- To satisfy the replication Requirement #2-i, configure the [table routing rules](/reference/tools/data-migration/features/overview.md#table-routing) as follows:

    ```yaml
    routes:
      ...
      instance-2-store-rule:
        schema-pattern: "store"
        table-pattern: "store_sz"
        target-schema: "store"
        target-table:  "store_suzhou"
      instance-3-store-rule:
        schema-pattern: "store"
        table-pattern: "store_sz"
        target-schema: "store"
        target-table:  "store_shenzhen"
    ```

- To satisfy the replication Requirement #1-iv, configure the [binlog filtering rules](/reference/tools/data-migration/features/overview.md#binlog-event-filtering) as follows:

    ```yaml
    filters:
      ...
      log-filter-rule:
        schema-pattern: "user"
        table-pattern: "log"
        events: ["truncate table", "drop table", "delete"]
        action: Ignore
      user-filter-rule:
        schema-pattern: "user"
        events: ["drop database"]
        action: Ignore
    ```

- To satisfy the replication Requirement #2-ii, configure the [binlog filtering rule](/reference/tools/data-migration/features/overview.md#binlog-event-filtering) as follows:

    ```yaml
    filters:
      ...
      store-filter-rule:
        schema-pattern: "store"
        events: ["drop database", "truncate table", "drop table", "delete"]
        action: Ignore
    ```

    > **Note:**
    >
    > `store-filter-rule` is different from `log-filter-rule & user-filter-rule`. `store-filter-rule` is a rule for the whole `store` schema, while `log-filter-rule` and `user-filter-rule` are rules for the `log` table in the `user` schema.

- To satisfy the replication Requirement #3, configure the [black and white lists](/reference/tools/data-migration/features/overview.md#black-and-white-table-lists) as follows:

    ```yaml
    black-white-list:
      log-ignored:
        ignore-dbs: ["log"]
    ```

## Replication task configuration

The complete replication task configuration is shown below. For more details, see [configuration explanations](/reference/tools/data-migration/configure/task-configuration-file.md).

```yaml
name: "one-tidb-slave"
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
    route-rules: ["instance-1-user-rule"]
    filter-rules: ["log-filter-rule", "user-filter-rule", "store-filter-rule"]
    black-white-list:  "log-ignored"
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"
  -
    source-id: "instance-2"
    route-rules: ["instance-2-user-rule", instance-2-store-rule]
    filter-rules: ["log-filter-rule", "user-filter-rule", "store-filter-rule"]
    black-white-list:  "log-ignored"
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"
  -
    source-id: "instance-3"
    route-rules: ["instance-3-user-rule", instance-3-store-rule]
    filter-rules: ["log-filter-rule", "user-filter-rule", "store-filter-rule"]
    black-white-list:  "log-ignored"
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"

# other common configs shared by all instances

routes:
  instance-1-user-rule:
    schema-pattern: "user"
    target-schema: "user_north"
  instance-2-user-rule:
    schema-pattern: "user"
    target-schema: "user_east"
  instance-3-user-rule:
    schema-pattern: "user"
    target-schema: "user_south"
  instance-2-store-rule:
    schema-pattern: "store"
    table-pattern: "store_sz"
    target-schema: "store"
    target-table:  "store_suzhou"
  instance-3-store-rule:
    schema-pattern: "store"
    table-pattern: "store_sz"
    target-schema: "store"
    target-table:  "store_shenzhen"

filters:
  log-filter-rule:
    schema-pattern: "user"
    table-pattern: "log"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  user-filter-rule:
    schema-pattern: "user"
    events: ["drop database"]
    action: Ignore
  store-filter-rule:
    schema-pattern: "store"
    events: ["drop database", "truncate table", "drop table", "delete"]
    action: Ignore

black-white-list:
  log-ignored:
    ignore-dbs: ["log"]

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

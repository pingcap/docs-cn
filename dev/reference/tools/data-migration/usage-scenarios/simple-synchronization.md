---
title: Data Migration 简单使用场景
category: reference
---

# Data Migration 简单使用场景

本文介绍了 DM 工具的一个简单使用场景（非分库分表合并场景）：将三个上游 MySQL 实例的数据同步到一个下游 TiDB 集群中。

## 上游实例

假设上游结构为：

- 实例 1

    | Schema | Tables |
    |:------|:------|
    | user  | information, log |
    | store | store_bj, store_tj |
    | log   | messages |

- 实例 2

    | Schema | Tables |
    |:------|:------|
    | user  | information, log |
    | store | store_sh, store_sz |
    | log   | messages |

- 实例 3

    | Schema | Tables |
    |:------|:------|
    | user  | information, log |
    | store | store_gz, store_sz |
    | log   | messages |

## 同步要求

1. 不合并 `user` 库。

    1. 将实例 1 中的 `user` 库同步到下游 TiDB 的 `user_north` 库中。

    2. 将实例 2 中的 `user` 库同步到下游 TiDB 的 `user_east` 库中。

    3. 将实例 3 中的 `user` 库同步到下游 TiDB 的 `user_south` 库中。

    4. 任何情况下都不删除 `log` 表的任何数据。

2. 将上游 `store` 库同步到下游 `store` 库中，且同步过程中不合并表。

    1. 实例 2 和实例 3 中都存在 `store_sz` 表，且这两个 `store_sz` 表分别被同步到下游的 `store_suzhou` 表和 `store_shenzhen` 表中。

    2. 任何情况下都不删除 `store` 库的任何数据。

3. `log` 库需要被过滤掉。

## 下游实例

假设下游结构为：

| Schema | Tables |
|:------|:------|
| user_north | information, log |
| user_east  | information, log |
| user_south | information, log |
| store | store_bj, store_tj, store_sh, store_suzhou, store_gz, store_shenzhen |

## 同步方案

- 为了满足[同步要求](#同步要求)中第一点的前三条要求，需要配置以下 [table routing 规则](/dev/reference/tools/data-migration/features/overview.md#table-routing)：

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

- 为了满足[同步要求](#同步要求)中第二点的第一条要求，需要配置以下 [table routing 规则](/dev/reference/tools/data-migration/features/overview.md#table-routing)：

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

- 为了满足[同步要求](#同步要求)中第一点的第四条要求，需要配置以下 [binlog event filter 规则](/dev/reference/tools/data-migration/features/overview.md#binlog-event-filter)：

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

- 为了满足[同步要求](#同步要求)中第二点的第二条要求，需要配置以下 [binlog event filter 规则](/dev/reference/tools/data-migration/features/overview.md#binlog-event-filter)：

    ```yaml
    filters:
      ...
      store-filter-rule:
        schema-pattern: "store"
        events: ["drop database", "truncate table", "drop table", "delete"]
        action: Ignore
    ```

    > **注意：**
    >
    > `store-filter-rule` 不同于 `log-filter-rule` 和 `user-filter-rule`。`store-filter-rule` 是针对整个 `store` 库的规则，而 `log-filter-rule` 和 `user-filter-rule` 是针对 `user` 库中 `log` 表的规则。

- 为了满足[同步要求](#同步要求)中的第三点要求，需要配置以下 [black & white table lists 规则](/dev/reference/tools/data-migration/features/overview.md#black--white-table-lists)：

    ```yaml
    black-white-list:
      log-ignored:
        ignore-dbs: ["log"]
    ```

## 同步任务配置

以下是完整的同步任务配置，详见[配置介绍](/dev/reference/tools/data-migration/configure/task-configuration-file.md)。

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
    filter-rules: ["log-filter-rule", "user-filter-rule" , "store-filter-rule"]
    black-white-list:  "log-ignored"
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"
  -
    source-id: "instance-2"
    route-rules: ["instance-2-user-rule", instance-2-store-rule]
    filter-rules: ["log-filter-rule", "user-filter-rule" , "store-filter-rule"]
    black-white-list:  "log-ignored"
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"
  -
    source-id: "instance-3"
    route-rules: ["instance-3-user-rule", instance-3-store-rule]
    filter-rules: ["log-filter-rule", "user-filter-rule" , "store-filter-rule"]
    black-white-list:  "log-ignored"
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"

# 所有实例的共有配置

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

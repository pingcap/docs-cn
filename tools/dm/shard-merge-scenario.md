---
title: DM 分片合并场景
summary: 学习分片合并场景下如何使用 DM 同步数据
category: tools
---

# Data Migration 分片合并场景

本文介绍如何在分片合并场景中使用 Data Migration (DM)。使用场景中，三个上游 MySQL 实例的分片结构和分表数据需要同步至下游 TiDB 集群。

## 上游实例

假设上游库结构如下：

- 实例 1

    | 库 | 表 |
    |:------|:------|
    | user  | information, log_north, log_bak |
    | store_01 | sale_01, sale_02 |
    | store_02 | sale_01, sale_02 |

- 实例 2

    | 库 | 表 |
    |:------|:------|
    | user  | information, log_east, log_bak |
    | store_01 | sale_01, sale_02 |
    | store_02 | sale_01, sale_02 |

- 实例 3

    | 库 | 表 |
    |:------|:------|
    | user  | information, log_south, log_bak |
    | store_01 | sale_01, sale_02 |
    | store_02 | sale_01, sale_02 |

## 同步需求

1. 合并三个上游实例中的 `user`.`information` 表至下游 TiDB 中的 `user`.`information` 表。
2. 合并三个上游实例中的 `user`.`log_{north|south|east}` 表至下游TiDB中的 `user`.`log_{north|south|east}` 表。
3. 合并三个上游实例中的 `store_{01|02}`.`sale_{01|02}` 表至下游TiDB中的 `store`.`sale` 表。
4. 从三个上游实例中的 `user`.`log_{north|south|east}` 表中过滤掉所有删除操作。
5. 从三个上游实例中的 `user`.`information` 表中过滤掉所有删除操作。
6. 从三个上游实例中的  `store_{01|02}`.`sale_{01|02}` 表中过滤掉所有删除操作。
7. 过滤掉三个上游实例中的 `user`.`log_bak` 表。
8. 因为 `store_{01|02}`.`sale_{01|02}` 表带有长整型的自增主键，将这些表合并至 TiDB 时会引发合并冲突。您需要修改相应自增主键以避免冲突。

## 下游实例

假设同步后下游库结构如下：

| 库 | 表 |
|:------|:------|
| user | information, log_north, log_east, log_south|
| store | sale |

## 同步方案

- 要满足同步需求 #1 和 #2, 配置 [表路由规则](/tools/dm/data-synchronization-features.md#表路由) 如下：

    ```yaml
    routes:
      ...
      user-route-rule:
        schema-pattern: "user"
        target-schema: "user"
    ```

- 要满足同步要求 #3, 配置 [表路由规则](/tools/dm/data-synchronization-features.md#表路由) 如下：

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

- 要满足同步要求 #4 和 #5, 配置 [binlog 事件过滤规则](/tools/dm/data-synchronization-features.md#binlog-event-filtering) 如下：

    ```yaml
    filters:
      ...
      user-filter-rule:
        schema-pattern: "user"
        events: ["truncate table", "drop table", "delete"， "drop database"]
        action: Ignore
    ```

    > **注意：** 同步要求 #4、#5 和 #7 中，所有对 `user` 库的删除操作都要被过滤，所以此处配置了库级别的过滤规则。但需要注意的是，`user` 库将来出现表的删除操作也都会被过滤。

- 要满足同步要求 #6, 配置 [binlog 事件过滤规则](/tools/dm/data-synchronization-features.md#binlog-event-filtering) 如下：

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

- 要满足同步要求 #7, 配置 [黑白表名单](/tools/dm/data-synchronization-features.md#black-and-white-table-lists) 如下：

    ```yaml
    black-white-list:
      log-bak-ignored:
        ignore-tales:
        - db-name: "user"
          tbl-name: "log_bak"
    ```

- 要满足同步要求 #8, 配置 [列值转换规则](/tools/dm/data-synchronization-features.md#column-mapping) 如下：

    ```yaml
    column-mappings:
      instance-1-sale:
        schema-pattern: "store_*"
        table-pattern: "sale_*"
        expression: "partition id"
        source-column: "id"
        target-column: "id"
        arguments: ["1", "store_", "sale_"]
      instance-2-sale:
        schema-pattern: "store_*"
        table-pattern: "sale_*"
        expression: "partition id"
        source-column: "id"
        target-column: "id"
        arguments: ["2", "store_", "sale_"]
      instance-3-sale:
        schema-pattern: "store_*"
        table-pattern: "sale_*"
        expression: "partition id"
        source-column: "id"
        target-column: "id"
        arguments: ["3", "store_", "sale_"]
    ```

## 同步任务配置

同步任务的完整配置如下。更多信息，请参考 [Data Migration 任务配置文件](/tools/dm/task-configuration-file-intro.md).

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

# 所有实例共享的其他通用配置

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
    events: ["truncate table", "drop table", "delete"， "drop database"]
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
    arguments: ["1", "store_", "sale_"]
  instance-2-sale:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    expression: "partition id"
    source-column: "id"
    target-column: "id"
    arguments: ["2", "store_", "sale_"]
  instance-3-sale:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    expression: "partition id"
    source-column: "id"
    target-column: "id"
    arguments: ["3", "store_", "sale_"]

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

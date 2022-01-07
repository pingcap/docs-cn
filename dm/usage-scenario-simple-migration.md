---
title: 多数据源合并迁移到 TiDB
aliases: ['/docs-cn/tidb-data-migration/dev/usage-scenario-simple-replication/']
---

# 多数据源合并迁移到 TiDB

本文介绍了 DM 工具的一个简单使用场景：将三个数据源 MySQL 实例的数据迁移到一个下游 TiDB 集群中。

## 数据源实例

假设数据源结构为：

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

## 迁移要求

1. 不合并 `user` 库。

    1. 将实例 1 中的 `user` 库迁移到下游 TiDB 的 `user_north` 库中。

    2. 将实例 2 中的 `user` 库迁移到下游 TiDB 的 `user_east` 库中。

    3. 将实例 3 中的 `user` 库迁移到下游 TiDB 的 `user_south` 库中。

    4. 任何情况下都不删除 `user.log` 表的任何数据。

2. 将数据源 `store` 库迁移到下游 `store` 库中，且迁移过程中不合并表。

    1. 实例 2 和实例 3 中都存在 `store_sz` 表，且这两个 `store_sz` 表分别被迁移到下游的 `store_suzhou` 表和 `store_shenzhen` 表中。

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

## 迁移方案

- 为了满足[迁移要求](#迁移要求)中第一点的前三条要求，需要配置以下 [table routing 规则](/dm/dm-key-features.md#table-routing)：

    {{< copyable "" >}}

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

- 为了满足[迁移要求](#迁移要求)中第二点的第一条要求，需要配置以下 [table routing 规则](/dm/dm-key-features.md#table-routing)：

    {{< copyable "" >}}

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

- 为了满足[迁移要求](#迁移要求)中第一点的第四条要求，需要配置以下 [binlog event filter 规则](/dm/dm-key-features.md#binlog-event-filter)：

    {{< copyable "" >}}

    ```yaml
    filters:
      ...
      log-filter-rule:                 # 过滤掉 user.log 表的任何删除操作
        schema-pattern: "user"
        table-pattern: "log"
        events: ["truncate table", "drop table", "delete"]
        action: Ignore
      user-filter-rule:                # 过滤掉删除 user 库操作
        schema-pattern: "user"
        events: ["drop database"]
        action: Ignore
    ```

- 为了满足[迁移要求](#迁移要求)中第二点的第二条要求，需要配置以下 [binlog event filter 规则](/dm/dm-key-features.md#binlog-event-filter)：

    {{< copyable "" >}}

    ```yaml
    filters:
      ...
      store-filter-rule:            # 过滤掉删除 store 库，以及 store 库下面任何表的所有删除操作
        schema-pattern: "store"
        events: ["drop database", "truncate table", "drop table", "delete"]
        action: Ignore
    ```

    > **注意：**
    >
    > `store-filter-rule` 不同于 `log-filter-rule` 和 `user-filter-rule`。`store-filter-rule` 是针对整个 `store` 库的规则，而 `log-filter-rule` 和 `user-filter-rule` 是针对 `user` 库中 `log` 表的规则。

- 为了满足[迁移要求](#迁移要求)中的第三点要求，需要配置以下 [Block & Allow Lists](/dm/dm-key-features.md#block--allow-table-lists)：

    {{< copyable "" >}}

    ```yaml
    block-allow-list:   # 通过黑白名单，过滤掉 log 库的所有操作
      log-ignored:
        ignore-dbs: ["log"]
    ```

## 迁移任务配置

以下是完整的迁移任务配置，更多详情请参阅 [数据迁移任务配置向导](/dm/dm-task-configuration-guide.md)。

{{< copyable "" >}}

```yaml
name: "one-tidb-slave"
task-mode: all                           # 进行全量数据迁移 + 增量数据迁移
meta-schema: "dm_meta"

target-database:
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""

mysql-instances:
  -
    source-id: "instance-1"    # 数据源 ID，可以从数据源配置中获取
    route-rules: ["instance-1-user-rule"]  # 应用于该数据源的 table route 规则
    filter-rules: ["log-filter-rule", "user-filter-rule" , "store-filter-rule"]  # 应用于该数据源的 binlog event filter 规则
    block-allow-list:  "log-ignored"  # 应用于该数据源的 Block & Allow Lists 规则
  -
    source-id: "instance-2"
    route-rules: ["instance-2-user-rule", instance-2-store-rule]
    filter-rules: ["log-filter-rule", "user-filter-rule" , "store-filter-rule"]
    block-allow-list:  "log-ignored"
  -
    source-id: "instance-3"
    route-rules: ["instance-3-user-rule", instance-3-store-rule]
    filter-rules: ["log-filter-rule", "user-filter-rule" , "store-filter-rule"]
    block-allow-list:  "log-ignored"

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
```

---
title: TiDB Data Migration 数据迁移任务配置向导
---

# TiDB Data Migration 数据迁移任务配置向导

本文档介绍如何配置 TiDB Data Migration (DM) 的数据迁移任务。

## 配置需要迁移的数据源

配置需要迁移的数据源之前，首先应该确认已经在 DM 创建相应数据源：

- 查看数据源可以参考[查看数据源配置](/dm/dm-manage-source.md#查看数据源配置)
- 创建数据源可以参考[在 DM 创建数据源](/dm/migrate-data-using-dm.md#第-3-步创建数据源)
- 数据源配置可以参考[数据源配置文件介绍](/dm/dm-source-configuration-file.md)

仿照下面的 `mysql-instances:` 示例定义数据迁移任务需要同步的单个或者多个数据源。

```yaml
---

## ********* 任务信息配置 *********
name: test             # 任务名称，需要全局唯一

## ******** 数据源配置 **********
mysql-instances:
  - source-id: "mysql-replica-01"  # 从 source-id = mysql-replica-01 的数据源迁移数据
  - source-id: "mysql-replica-02"  # 从 source-id = mysql-replica-02 的数据源迁移数据
```

## 配置迁移的目标 TiDB 集群

仿照下面的 `target-database:` 示例定义迁移的目标 TiDB 集群。

```yaml
---

## ********* 任务信息配置 *********
name: test             # 任务名称，需要全局唯一

## ******** 数据源配置 **********
mysql-instances:
  - source-id: "mysql-replica-01"  # 从 source-id = mysql-replica-01 的数据源迁移数据
  - source-id: "mysql-replica-02"  # 从 source-id = mysql-replica-02 的数据源迁移数据

## ******** 目标 TiDB 配置 **********
target-database:       # 目标 TiDB 配置
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""         # 如果密码不为空，则推荐使用经过 dmctl 加密的密文
```

## 配置需要迁移的表

如果不需要过滤或迁移特定表，可以跳过该项配置。

配置从数据源迁移表的黑白名单，则需要添加两个定义，详细配置规则参考 [Block & Allow Lists](/dm/dm-block-allow-table-lists.md)：

1. 定义全局的黑白名单规则

    ```yaml
    block-allow-list:
      bw-rule-1:                           # 规则名称
        do-dbs: ["test.*", "user"]         # 迁移哪些库，支持通配符 "*" 和 "?"，do-dbs 和 ignore-dbs 只需要配置一个，如果两者同时配置只有 do-dbs 会生效
        # ignore-dbs: ["mysql", "account"] # 忽略哪些库，支持通配符 "*" 和 "?"
        do-tables:                         # 迁移哪些表，do-tables 和 ignore-tables 只需要配置一个，如果两者同时配置只有 do-tables 会生效
        - db-name: "test.*"
          tbl-name: "t.*"
        - db-name: "user"
          tbl-name: "information"
      bw-rule-2:                          # 规则名称
        ignore-tables:                    # 忽略哪些表
        - db-name: "user"
          tbl-name: "log"
    ```

2. 在数据源配置中引用黑白名单规则，过滤该数据源需要迁移的表

    ```yaml
    mysql-instances:
        - source-id: "mysql-replica-01"  # 从 source-id = mysql-replica-01 的数据源迁移数据
          block-allow-list:  "bw-rule-1" # 黑白名单配置名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
        - source-id: "mysql-replica-02"  # 从 source-id = mysql-replica-02 的数据源迁移数据
          block-allow-list:  "bw-rule-2" # 黑白名单配置名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
    ```

## 配置需要过滤的操作

如果不需要过滤特定库或者特定表的特定操作，可以跳过该项配置。

配置过滤特定操作，则需要添加两个定义，详细配置规则参考 [Binlog Event Filter](/dm/dm-binlog-event-filter.md)：

1. 定义全局的数据源操作过滤规则

    ```yaml
    filters:                                        # 定义过滤数据源特定操作的规则，可以定义多个规则
      filter-rule-1:                                # 规则名称
        schema-pattern: "test_*"                    # 匹配数据源的库名，支持通配符 "*" 和 "?"
        table-pattern: "t_*"                        # 匹配数据源的表名，支持通配符 "*" 和 "?"
        events: ["truncate table", "drop table"]    # 匹配上 schema-pattern 和 table-pattern 的库或者表的操作类型
        action: Ignore                              # 迁移（Do）还是忽略(Ignore)
      filter-rule-2:
        schema-pattern: "test"
        events: ["all dml"]
        action: Do
    ```

2. 在数据源配置中引用数据源操作过滤规则，过滤该数据源的指定库或表的指定操作

    ```yaml
    mysql-instances:
      - source-id: "mysql-replica-01"    # 从 source-id = mysql-replica-01 的数据源迁移数据
        block-allow-list:  "bw-rule-1"   # 黑白名单配置名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
        filter-rules: ["filter-rule-1"]  # 过滤数据源特定操作的规则，可以配置多个过滤规则
      - source-id: "mysql-replica-02"    # 从 source-id = mysql-replica-02 的数据源迁移数据
        block-allow-list:  "bw-rule-2"   # 黑白名单配置名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
        filter-rules: ["filter-rule-2"]  # 过滤数据源特定操作的规则，可以配置多个过滤规则
    ```

## 配置需要数据源表到目标 TiDB 表的映射

如果不需要将数据源表路由到不同名的目标 TiDB 表，可以跳过该项配置。分库分表合并迁移的场景必须配置该规则。

配置数据源表迁移到目标 TiDB 表的路由规则，则需要添加两个定义，详细配置规则参考 [Table Routing](/dm/dm-table-routing.md)：

1. 定义全局的路由规则

    ```yaml
    routes:                           # 定义数据源表迁移到目标 TiDB 表的路由规则，可以定义多个规则
      route-rule-1:                   # 规则名称
        schema-pattern: "test_*"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
        table-pattern: "t_*"          # 匹配数据源的表名，支持通配符 "*" 和 "?"
        target-schema: "test"         # 目标 TiDB 库名
        target-table: "t"             # 目标 TiDB 表名
      route-rule-2:
        schema-pattern: "test_*"
        target-schema: "test"
    ```

2. 在数据源配置中引用路由规则，过滤该数据源需要迁移的表

    ```yaml
    mysql-instances:
      - source-id: "mysql-replica-01"                     # 从 source-id = mysql-replica-01 的数据源迁移数据
        block-allow-list:  "bw-rule-1"                    # 黑白名单配置名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
        filter-rules: ["filter-rule-1"]                   # 过滤数据源特定操作的规则，可以配置多个过滤规则
        route-rules: ["route-rule-1", "route-rule-2"]     # 数据源表迁移到目标 TiDB 表的路由规则，可以定义多个规则
      - source-id: "mysql-replica-02"                     # 从 source-id = mysql-replica-02 的数据源迁移数据
        block-allow-list:  "bw-rule-2"                    # 黑白名单配置名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
        filter-rules: ["filter-rule-2"]                   # 过滤数据源特定操作的规则，可以配置多个过滤规则
    ```

## 配置是否进行分库分表合并

如果是分库分表合并的数据迁移场景，并且需要同步分库分表的 DDL，则必须显式配置 `shard-mode`，否则不要配置该选项。

分库分表 DDL 同步问题特别多，请确认了解 DM 同步分库分表 DDL 的原理和限制后，谨慎使用。

```yaml
---

## ********* 任务信息配置 *********
name: test                      # 任务名称，需要全局唯一
shard-mode: "pessimistic"       # 默认值为 "" 即无需协调。如果为分库分表合并任务，请设置为悲观协调模式 "pessimistic"。在深入了解乐观协调模式的原理和使用限制后，也可以设置为乐观协调模式 "optimistic"
```

## 其他配置

下面是本数据迁移任务配置向导的完整示例。完整的任务配置参见 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)。

```yaml
---

## ********* 任务信息配置 *********
name: test                      # 任务名称，需要全局唯一
shard-mode: "pessimistic"       # 默认值为 "" 即无需协调。如果为分库分表合并任务，请设置为悲观协调模式 "pessimistic"。在深入了解乐观协调模式的原理和使用限制后，也可以设置为乐观协调模式 "optimistic"
task-mode: all                  # 任务模式，可设为 "full" - "只进行全量数据迁移"、"incremental" - "Binlog 实时同步"、"all" - "全量 + Binlog 迁移"
# timezone: "UTC"               # 指定数据迁移任务时 SQL Session 使用的时区。DM 默认使用目标库的全局时区配置进行数据迁移，并且自动确保同步数据的正确性。使用自定义时区依然可以确保整个流程的正确性，但一般不需要手动指定。

## ******** 数据源配置 **********
mysql-instances:
  - source-id: "mysql-replica-01"                   # 从 source-id = mysql-replica-01 的数据源迁移数据
    block-allow-list:  "bw-rule-1"                  # 黑白名单配置名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
    filter-rules: ["filter-rule-1"]                 # 过滤数据源特定操作的规则，可以配置多个过滤规则
    route-rules: ["route-rule-1", "route-rule-2"]   # 数据源表迁移到目标 TiDB 表的路由规则，可以定义多个规则
  - source-id: "mysql-replica-02"                   # 从 source-id = mysql-replica-02 的数据源迁移数据
    block-allow-list:  "bw-rule-2"                  # 黑白名单配置名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
    filter-rules: ["filter-rule-2"]                 # 过滤数据源特定操作的规则，可以配置多个过滤规则
    route-rules: ["route-rule-2"]                   # 数据源表迁移到目标 TiDB 表的路由规则，可以定义多个规则

## ******** 目标 TiDB 配置 **********
target-database:       # 目标 TiDB 配置
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""         # 如果密码不为空，则推荐使用经过 dmctl 加密的密文

## ******** 功能配置 **********
block-allow-list:                      # 定义数据源迁移表的过滤规则，可以定义多个规则。如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
  bw-rule-1:                           # 规则名称
    do-dbs: ["test.*", "user"]         # 迁移哪些库，支持通配符 "*" 和 "?"，do-dbs 和 ignore-dbs 只需要配置一个，如果两者同时配置只有 do-dbs 会生效
    # ignore-dbs: ["mysql", "account"] # 忽略哪些库，支持通配符 "*" 和 "?"
    do-tables:                         # 迁移哪些表，do-tables 和 ignore-tables 只需要配置一个，如果两者同时配置只有 do-tables 会生效
    - db-name: "test.*"
      tbl-name: "t.*"
    - db-name: "user"
      tbl-name: "information"
  bw-rule-2:                         # 规则名称
    ignore-tables:                   # 忽略哪些表
    - db-name: "user"
      tbl-name: "log"

filters:                                        # 定义过滤数据源特定操作的规则，可以定义多个规则
  filter-rule-1:                                # 规则名称
    schema-pattern: "test_*"                    # 匹配数据源的库名，支持通配符 "*" 和 "?"
    table-pattern: "t_*"                        # 匹配数据源的表名，支持通配符 "*" 和 "?"
    events: ["truncate table", "drop table"]    # 匹配上 schema-pattern 和 table-pattern 的库或者表的操作类型
    action: Ignore                              # 迁移（Do）还是忽略(Ignore)
  filter-rule-2:
    schema-pattern: "test"
    events: ["all dml"]
    action: Do

routes:                           # 定义数据源表迁移到目标 TiDB 表的路由规则，可以定义多个规则
  route-rule-1:                   # 规则名称
    schema-pattern: "test_*"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
    table-pattern: "t_*"          # 匹配数据源的表名，支持通配符 "*" 和 "?"
    target-schema: "test"         # 目标 TiDB 库名
    target-table: "t"             # 目标 TiDB 表名
  route-rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

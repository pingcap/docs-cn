---
title: 分表合并迁移到 TiDB
aliases: ['/docs-cn/tidb-data-migration/dev/usage-scenario-shard-merge/']
---

# 分表合并迁移到 TiDB

本文介绍如何在分库分表合并场景中使用 Data Migration (DM) 将上游数据迁移至下游 TiDB 集群。

下面介绍了一个简单的场景，两个数据源 MySQL 实例的分库和分表数据需要迁移至下游 TiDB 集群。更多详情请参阅[分表合并数据迁移最佳实践](/dm/shard-merge-best-practices.md)。

## 数据源实例

假设数据源结构如下：

- 实例 1

    | Schema | Tables |
    |:------|:------|
    | user  | information, log_bak |
    | store_01 | sale_01, sale_02 |
    | store_02 | sale_01, sale_02 |

- 实例 2

    | Schema | Tables |
    |:------|:------|
    | user  | information, log_bak |
    | store_01 | sale_01, sale_02 |
    | store_02 | sale_01, sale_02 |

## 迁移需求

1. `user`.`information` 需要合并到下游 TiDB 中的 `user`.`information` 表。
2. 实例中的 `store_{01|02}`.`sale_{01|02}` 表合并至下游 TiDB 中的 `store`.`sale` 表。
3. 同步 `user`，`store_{01|02}` 库，但不同步两个实例的 `user`.`log_bak` 表。
4. 过滤掉两个实例中 `store_{01|02}`.`sale_{01|02}` 表的所有删除操作，并过滤该库的 `drop database` 操作。

预期迁移后下游库结构如下：

| Schema | Tables |
|:------|:------|
| user | information |
| store | sale |

## 分表数据冲突检查

迁移需求 #1 和 #2 涉及合库合表，来自多张分表的数据可能引发主键或唯一索引的数据冲突。这需要我们检查这几组分表数据的业务特点，详情请见[跨分表数据在主键或唯一索引冲突处理](/dm/shard-merge-best-practices.md#跨分表数据在主键或唯一索引冲突处理)。在本示例中：

`user`.`information` 表结构为

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

其中 `id` 列为主键，`uid` 列为唯一索引。`id` 列具有自增属性，多个分表范围重复会引发数据冲突。 `uid` 可以保证全局满足唯一索引，因此可以按照参考[去掉自增主键的主键属性](/dm/shard-merge-best-practices.md#去掉自增主键的主键属性)中介绍的操作绕过 `id` 列。

`store_{01|02}`.`sale_{01|02}` 的表结构为

```sql
CREATE TABLE `sale_01` (
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`sid`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

其中 `sid` 是分片键，可以保证同一个 `sid` 只会划分到一个分表中，因此不会引发数据冲突，无需进行额外操作。

## 迁移方案

- 要满足迁移需求 #1，无需配置 [table routing 规则](/dm/dm-key-features.md#table-routing)。按照[去掉自增主键的主键属性](/dm/shard-merge-best-practices.md#去掉自增主键的主键属性)的要求，在下游手动建表。
    
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
    
    并在配置文件中跳过前置检查
    
    {{< copyable "" >}}

    ```yaml
    ignore-checking-items: ["auto_increment_ID"]
    ```

- 要满足迁移需求 #2，配置 [table routing 规则](/dm/dm-key-features.md#table-routing)如下：

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

- 要满足迁移需求 #3，配置 [Block & Allow Lists](/dm/dm-key-features.md#block--allow-table-lists) 如下：

    {{< copyable "" >}}

    ```yaml
    block-allow-list:
      log-bak-ignored:
        do-dbs: ["user", "store_*"]
        ignore-tables:
        - db-name: "user"
          tbl-name: "log_bak"
    ```

- 要满足迁移需求 #4，配置 [Binlog event filter 规则](/dm/dm-key-features.md#binlog-event-filter)如下：

    {{< copyable "" >}}

    ```yaml
    filters:
      ...
      sale-filter-rule:     # 过滤掉 store_* 库下面任何表的任何删除操作
        schema-pattern: "store_*"
        table-pattern: "sale_*"
        events: ["truncate table", "drop table", "delete"]
        action: Ignore
      store-filter-rule:   # 过滤掉删除 store_* 库的操作
        schema-pattern: "store_*"
        events: ["drop database"]
        action: Ignore
    ```

## 迁移任务配置

迁移任务的完整配置如下，更多详情请参阅[数据迁移任务配置向导](/dm/dm-task-configuration-guide.md)。

{{< copyable "" >}}

```yaml
name: "shard_merge"
task-mode: all                                   # 进行全量数据迁移 + 增量数据迁移
meta-schema: "dm_meta"
ignore-checking-items: ["auto_increment_ID"]

target-database:
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""

mysql-instances:
  -
    source-id: "instance-1"        # 数据源 ID，可以从数据源配置中获取
    route-rules: ["store-route-rule", "sale-route-rule"] # 应用于该数据源的 table route 规则
    filter-rules: ["store-filter-rule", "sale-filter-rule"] # 应用于该数据源的 binlog event filter 规则
    block-allow-list:  "log-bak-ignored" # 应用于该数据源的 Block & Allow Lists 规则
  -
    source-id: "instance-2"
    route-rules: ["store-route-rule", "sale-route-rule"]
    filter-rules: ["store-filter-rule", "sale-filter-rule"]
    block-allow-list:  "log-bak-ignored"

# 所有实例共享的其他通用配置

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

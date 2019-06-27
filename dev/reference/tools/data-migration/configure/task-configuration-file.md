---
title: DM 任务配置文件介绍
category: reference
---

# DM 任务配置文件介绍

本文档主要介绍 Data Migration (DM) 的任务配置文件 [`task.yaml`](https://github.com/pingcap/dm/blob/master/dm/master/task.yaml)，包含[全局配置](#全局配置) 和[实例配置](#实例配置) 两部分。

关于各配置项的功能和配置，请参阅[数据同步功能](/reference/tools/data-migration/features/overview.md)。

## 关键概念

关于包括 `source-id` 和 DM-worker ID 在内的关键概念的介绍，请参阅[关键概念](/reference/tools/data-migration/configure/overview.md#关键概念)。

## 配置顺序

1. 编辑[全局配置](#全局配置)。
2. 根据全局配置编辑[实例配置](#实例配置)。

## 全局配置

### 基础信息配置

```yaml
name: test                      # 任务名称，需要全局唯一。
task-mode: all                  # 任务模式，可设为 "full"、"incremental"、"all"。
is-sharding: true               # 是否为分库分表合并任务。
meta-schema: "dm_meta"          # 下游储存 `meta` 信息的数据库。
remove-meta: false              # 是否在任务同步开始前移除该任务名对应的 `meta`（`checkpoint` 和 `onlineddl`）。
enable-heartbeat: false         # 是否开启 `heartbeat` 功能。

target-database:                # 下游数据库实例配置。
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""                  # 如果不为空则需经过 dmctl 加密
```

`task-mode`

- 描述：任务模式，可以通过任务模式来指定需要执行的数据迁移工作。
- 值为字符串（`full`，`incremental` 或 `all`）。
    - `full`：只全量备份上游数据库，然后将数据全量导入到下游数据库。
    - `incremental`：只通过 binlog 把上游数据库的增量修改同步到下游数据库, 可以设置实例配置的 `meta` 配置项来指定增量同步开始的位置。
    - `all`：`full` + `incremental`。先全量备份上游数据库，将数据全量导入到下游数据库，然后从全量数据备份时导出的位置信息 (binlog position) 开始通过 binlog 增量同步数据到下游数据库。

### 功能配置集

全局配置主要包含下列功能配置集。

```yaml
routes:                                             # 上游和下游表之间的路由 table routing 规则集。
  route-rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  route-rule-2:
    schema-pattern: "test_*"
    target-schema: "test"

filters:                                            # 上游数据库实例匹配的表的 binlog event filter 规则集。
  filter-rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    action: Ignore
  filter-rule-2:
    schema-pattern: "test_*"
    events: ["all dml"]                             # 只执行 schema `test_*` 下面所有的 DML event。
    action: Do

black-white-list:                                   # 该上游数据库实例匹配的表的 black & white list 过滤规则集。
  bw-rule-1:
    do-dbs: ["~^test.*", "user"]
    ignore-dbs: ["mysql", "account"]
    do-tables:
    - db-name: "~^test.*"
      tbl-name: "~^t.*"
    - db-name: "user"
      tbl-name: "information"
    ignore-tables:
    - db-name: "user"
      tbl-name: "log"

column-mappings:                                    # 上游数据库实例匹配的表的 column mapping 规则集。
  cm-rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    expression: "partition id"
    source-column: "id"
    target-column: "id"
    arguments: ["1", "test", "t", "_"]
  cm-rule-2:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    expression: "partition id"
    source-column: "id"
    target-column: "id"
    arguments: ["2", "test", "t", "_"]

mydumpers:                                          # mydumper 处理单元运行配置参数。
  global:
    mydumper-path: "./mydumper"                     # mydumper binary 文件地址，这个无需设置，会由 Ansible 部署程序自动生成。
    threads: 16                                     # mydumper 从上游数据库实例导出数据的线程数量。
    chunk-filesize: 64                              # mydumper 生成的数据文件大小，单位为 MB。
    skip-tz-utc: true
    extra-args: "-B test -T t1,t2 --no-locks"

loaders:                                            # loader 处理单元运行配置参数。
  global:
    pool-size: 16                                   # loader 并发执行 mydumper 的 SQL 文件的线程数量。
    dir: "./dumped_data"                            # loader 读取 mydumper 输出文件的地址，同实例对应的不同任务必须不同（mydumper 会根据这个地址输出 SQL 文件）。

syncers:                                            # syncer 处理单元运行配置参数。
  global:
    worker-count: 16                                # syncer 并发同步 binlog event 的线程数量。
    batch: 1000                                     # syncer 同步到下游数据库的一个事务批次 SQL 语句数。
    max-retry: 100                                  # syncer 同步到下游数据库出错的事务的重试次数（仅限于 DML 操作）。
```

## 示例配置

本小节定义具体的数据同步子任务，DM 支持从单个或者多个上游 MySQL 实例同步数据到同一个下游数据库实例。

```yaml
mysql-instances:
  -
    source-id: "mysql-replica-01"           # 上游实例或者复制组 ID，参考 `inventory.ini` 的 `source_id` 或者 `dm-master.toml` 的 `source-id` 配置。
    meta:                                   # `task-mode` 为 `incremental` 且下游数据库的 `checkpoint` 不存在时 binlog 同步开始的位置; 如果 checkpoint 存在，则以 `checkpoint` 为准。
      binlog-name: binlog-00001
      binlog-pos: 4

    route-rules: ["route-rule-1", "route-rule-2"]    # 该上游数据库实例匹配的表到下游数据库的 table routing 规则名称。
    filter-rules: ["filter-rule-1"]                  # 该上游数据库实例匹配的表的 binlog event filter 规则名称。
    column-mapping-rules: ["cm-rule-1"]              # 该上游数据库实例匹配的表的 column mapping 规则名称。
    black-white-list:  "bw-rule-1"                   # 该上游数据库实例匹配的表的 black & white list 过滤规则名称。

    mydumper-config-name: "global"          # mydumper 配置名称。
    loader-config-name: "global"            # loader 配置名称。
    syncer-config-name: "global"            # syncer 配置名称。

  -
    source-id: "mysql-replica-02"           # 上游实例或者复制组 ID，参考 `inventory.ini` 的 `source_id` 或者 `dm-master.toml` 的 `source-id` 配置。
    mydumper-config-name: "global"          # mydumper 配置名称。
    loader-config-name: "global"            # loader 配置名称。
    syncer-config-name: "global"            # syncer 配置名称。
```

关于以上配置项的更多配置细节，参见[功能配置集](#功能配置集)的相关配置项，对应关系如下：

| 配置项 | 相关配置项 |
| :------ | :------------------ |
| `route-rules` | `routes` |
| `filter-rules` | `filters` |
| `column-mapping-rules` | `column-mappings` |
| `black-white-list` | `black-white-list` |
| `mydumper-config-name` | `mydumpers` |
| `loader-config-name` | `loaders` |
| `syncer-config-name` | `syncers`  |

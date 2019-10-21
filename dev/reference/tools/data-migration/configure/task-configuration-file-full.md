---
title: DM 任务完整配置文件介绍
category: reference
---

# DM 任务配置文件介绍

本文档主要介绍 Data Migration (DM) 的任务完整的配置文件 [`task.yaml`](https://github.com/pingcap/dm/blob/master/dm/master/task.yaml)，包含[全局配置](#全局配置) 和[实例配置](#实例配置) 两部分。

关于各配置项的功能和配置，请参阅[数据同步功能](/dev/reference/tools/data-migration/features/overview.md)。

## 关键概念

关于包括 `source-id` 和 DM-worker ID 在内的关键概念的介绍，请参阅[关键概念](/dev/reference/tools/data-migration/configure/overview.md#关键概念)。

## 完整配置文件示例

下面是一个完整的配置文件示例，通过该示例可以完成复杂的数据同步功能。

```yaml
---

# ----------- 全局配置 -----------
## ********* 基本信息配置 *********
name: test                      # 任务名称，需要全局唯一
task-mode: all                  # 任务模式，可设为 "full"、"incremental"、"all"
is-sharding: true               # 是否为分库分表合并任务
meta-schema: "dm_meta"          # 下游储存 `meta` 信息的数据库
remove-meta: false              # 是否在任务同步开始前移除该任务名对应的 `meta`（`checkpoint` 和 `onlineddl` 等）。
enable-heartbeat: false         # 是否开启 `heartbeat` 功能

target-database:                # 下游数据库实例配置
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""                  # 如果不为空则需经过 dmctl 加密


## ******** 功能配置集 **********

routes:                           # 上游和下游表之间的路由 table routing 规则集
  route-rule-1:                   # 配置名称
    schema-pattern: "test_*"      # 库名匹配规则，支持通配符 "*" 和 "?"
    table-pattern: "t_*"          # 表名匹配规则，支持通配符 "*" 和 "?"
    target-schema: "test"         # 目标库名称
    target-table: "t"             # 目标表名称
  route-rule-2:
    schema-pattern: "test_*"
    target-schema: "test"

filters:                                        # 上游数据库实例匹配的表的 binlog event filter 规则集
  filter-rule-1:                                # 配置名称
    schema-pattern: "test_*"                    # 库名匹配规则，支持通配符 "*" 和 "?"
    table-pattern: "t_*"                        # 表名匹配规则，支持通配符 "*" 和 "?"
    events: ["truncate table", "drop table"]    # 匹配哪些 event 类型
    action: Ignore                              # 对与符合匹配规则的 binlog 同步（Do）还是忽略(Ignore)
  filter-rule-2:
    schema-pattern: "test_*"
    events: ["all dml"]
    action: Do

black-white-list:                    # 上游数据库实例匹配的表的 black & white list 过滤规则集
  bw-rule-1:                         # 配置名称
    do-dbs: ["~^test.*", "user"]     # 同步哪些库
    ignore-dbs: ["mysql", "account"] # 忽略哪些库
    do-tables:                       # 同步哪些表
    - db-name: "~^test.*"
      tbl-name: "~^t.*"
    - db-name: "user"
      tbl-name: "information"
    ignore-tables:                   # 忽略哪些表
    - db-name: "user"
      tbl-name: "log"

mydumpers:                           # mydumper 处理单元运行配置参数
  global:                            # 配置名称
    mydumper-path: "./bin/mydumper"  # mydumper binary 文件地址，默认值为 "./bin/mydumper"
    threads: 4                       # mydumper 从上游数据库实例导出数据的线程数量，默认值为 4
    chunk-filesize: 64               # mydumper 生成的数据文件大小，默认值为 64，单位为 MB
    skip-tz-utc: true                # 忽略对时间类型数据进行时区转化，默认值为 true
    extra-args: "--no-locks"         # mydumper 的其他参数，在 v1.0.2 版本中 DM 会自动生成 table-list 配置，在其之前的版本仍然需要人工配置

loaders:                             # loader 处理单元运行配置参数
  global:                            # 配置名称
    pool-size: 16                    # loader 并发执行 mydumper 的 SQL 文件的线程数量，默认值为 16
    dir: "./dumped_data"             # loader 读取 mydumper 输出文件的地址，同实例对应的不同任务必须不同（mydumper 会根据这个地址输出 SQL 文件），默认值为 "./dumped_data"

syncers:                             # syncer 处理单元运行配置参数
  global:                            # 配置名称
    worker-count: 16                 # syncer 并发同步 binlog event 的线程数量，默认值为 16
    batch: 100                       # syncer 同步到下游数据库的一个事务批次 SQL 语句数，默认值为 100

# ----------- 实例配置 -----------
mysql-instances:
  -
    source-id: "mysql-replica-01"           # 上游实例或者复制组 ID，参考 `inventory.ini` 的 `source_id` 或者 `dm-master.toml` 的 `source-id` 配置
    meta:                                   # `task-mode` 为 `incremental` 且下游数据库的 `checkpoint` 不存在时 binlog 同步开始的位置; 如果 checkpoint 存在，则以 `checkpoint` 为准
      binlog-name: binlog.000001
      binlog-pos: 4

    route-rules: ["route-rule-1", "route-rule-2"]  # 该上游数据库实例匹配的表到下游数据库的 table routing 规则名称
    filter-rules: ["filter-rule-1"]                # 该上游数据库实例匹配的表的 binlog event filter 规则名称
    black-white-list:  "bw-rule-1"                 # 该上游数据库实例匹配的表的 black & white list 过滤规则名称

    mydumper-config-name: "global"          # mydumper 配置名称
    loader-config-name: "global"            # loader 配置名称
    syncer-config-name: "global"            # Syncer 配置名称

  -
    source-id: "mysql-replica-02"  # 上游实例或者复制组 ID，参考 `inventory.ini` 的 `source_id` 或者 `dm-master.toml` 的 `source-id` 配置
    mydumper-thread: 4             # mydumper 用于导出数据的线程数量，等同于 mydumper 处理单元配置中的 `threads`，在 v1.0.2 版本引入
    loader-thread: 16              # loader 用于导入数据的线程数量，等同于 loader 处理单元配置中的 `pool-size`, 在 v1.0.2 版本引入
    syncer-thread: 16              # syncer 用于同步增量数据的线程数量，等同于 syncer 处理单元配置中的 `worker-count`，在 v1.0.2 版本引入
```

## 配置顺序

通过上面的配置文件示例，可以看出配置文件总共分为两个部分：`全局配置`和`实例配置`，其中`全局配置`又分为`基本信息配置`和`实例配置`，配置顺序如下：

1. 编辑[全局配置](#全局配置)。
2. 根据全局配置编辑[实例配置](#实例配置)。

## 全局配置

### 任务基本信息配置

配置任务的基本信息，配置项的说明参见以上示例配置文件中的注释。其中 `task-mode` 需要特殊说明：

`task-mode`

- 描述：任务模式，可以通过任务模式来指定需要执行的数据迁移工作。
- 值为字符串（`full`，`incremental` 或 `all`）。
    - `full`：只全量备份上游数据库，然后将数据全量导入到下游数据库。
    - `incremental`：只通过 binlog 把上游数据库的增量修改同步到下游数据库, 可以设置实例配置的 `meta` 配置项来指定增量同步开始的位置。
    - `all`：`full` + `incremental`。先全量备份上游数据库，将数据全量导入到下游数据库，然后从全量数据备份时导出的位置信息 (binlog position) 开始通过 binlog 增量同步数据到下游数据库。

### 功能配置集

全局配置主要包含下列功能配置集：

`routes`：上游和下游表之间的路由 table routing 规则集。如果上游与下游的库名、表名一致，则不需要配置该项。使用场景及示例配置参见 [Table Routing](/dev/reference/tools/data-migration/features/overview.md#table-routing)

`filters`：上游数据库实例匹配的表的 binlog event filter 规则集。如果不需要对 binlog 进行过滤，则不需要配置该项。使用场景及示例配置参见 [Binlog Event Filter](/dev/reference/tools/data-migration/features/overview.md#binlog-event-filter)

`black-white-list`：该上游数据库实例匹配的表的 black & white list 过滤规则集。建议通过该项指定需要同步的库和表，否则会同步所有的库和表。使用场景及示例配置参见 [Black & White Lists](/dev/reference/tools/data-migration/features/overview.md#black--white-table-lists)

`mydumpers`：mydumper 处理单元运行配置参数。如果默认配置可以满足需求，则不需要配置该项，也可以只使用 `mydumper-thread` 对 `thread` 配置项单独进行配置。

`loaders`：loader 处理单元运行配置参数。如果默认配置可以满足需求，则不需要配置该项，也可以只使用 `loader-thread` 对 `pool-size` 配置项单独进行配置。

`syncers`：syncer 处理单元运行配置参数。如果默认配置可以满足需求，则不需要配置该项，也可以只使用 `syncer-thread` 对 `worker-count` 配置项单独进行配置。

各个功能配置集的参数及解释参见[完整配置文件示例](#完整配置文件示例)中的注释说明。

## 实例配置

本小节定义具体的数据同步子任务，DM 支持从单个或者多个上游 MySQL 实例同步数据到同一个下游数据库实例。

在该项配置中设置数据同步子任务中各个功能对应的配置集中的配置名称，关于这些配置项的更多配置细节，参见[功能配置集](#功能配置集)的相关配置项，对应关系如下：

| 配置项 | 相关配置项 |
| :------ | :------------------ |
| `route-rules` | `routes` |
| `filter-rules` | `filters` |
| `black-white-list` | `black-white-list` |
| `mydumper-config-name` | `mydumpers` |
| `loader-config-name` | `loaders` |
| `syncer-config-name` | `syncers`  |

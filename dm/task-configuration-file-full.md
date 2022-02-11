---
title: DM 任务完整配置文件介绍
---

# DM 任务完整配置文件介绍

本文档主要介绍 Data Migration (DM) 的任务完整的配置文件，包含[全局配置](#全局配置) 和[实例配置](#实例配置) 两部分。

关于各配置项的功能和配置，请参阅[数据迁移功能](/dm/dm-overview.md#基本功能)。

## 关键概念

关于包括 `source-id` 和 DM-worker ID 在内的关键概念的介绍，请参阅[关键概念](/dm/dm-config-overview.md#关键概念)。

## 完整配置文件示例

下面是一个完整的配置文件示例，通过该示例可以完成复杂的数据迁移功能。

```yaml
---

# ----------- 全局配置 -----------
## ********* 基本信息配置 *********
name: test                      # 任务名称，需要全局唯一
task-mode: all                  # 任务模式，可设为 "full" - "只进行全量数据迁移"、"incremental" - "Binlog 实时同步"、"all" - "全量 + Binlog 实时同步"
is-sharding: true               # 该配置项从 DM v2.0.0 起弃用，其功能被 `shard-mode` 取代，建议使用 `shard-mode` 代替 `is-sharding`
shard-mode: "pessimistic"       # 任务协调模式，可选的模式有 ""、"pessimistic、"optimistic"。默认值为 "" 即无需协调。如果是分库分表合并任务，请设置为悲观协调模式 "pessimistic"。
                                # 在 v2.0.6 版本后乐观模式逐渐成熟，深入了解乐观协调模式的原理和使用限制后，也可以设置为乐观协调模式 "optimistic"
meta-schema: "dm_meta"          # 下游储存 `meta` 信息的数据库
# timezone: "Asia/Shanghai"     # 指定数据迁移任务时 SQL Session 使用的时区。DM 默认使用目标库的全局时区配置进行数据迁移，并且自动确保同步数据的正确性。使用自定义时区依然可以确保整个流程的正确性，但一般不需要手动指定。

case-sensitive: false           # schema/table 是否大小写敏感
online-ddl: true                # 支持上游 "gh-ost" 、"pt" 的自动处理
online-ddl-scheme: "gh-ost"     # `online-ddl-scheme` 在未来将会被弃用，建议使用 `online-ddl` 代替 `online-ddl-scheme`
clean-dump-file: true           # 是否清理 dump 阶段产生的文件，包括 metadata 文件、建库建表 SQL 文件以及数据导入 SQL 文件
collation_compatible: "loose"   # 同步 CREATE 语句中缺省 Collation 的方式，可选 "loose" 和 "strict"，默认为 "loose"。"loose" 模式不会显式补充上游缺省的 Collation，"strict" 会显式补充上游缺省的 Collation。当使用 "strict" 模式，但下游不支持上游缺省的 Collation 时，下游可能会报错。 

target-database:                # 下游数据库实例配置
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: "/Q7B9DizNLLTTfiZHv9WoEAKamfpIUs="  # 推荐使用经 `dmctl encrypt` 加密后的密码
  max-allowed-packet: 67108864                  # 设置 DM 内部连接 TiDB 服务器时，TiDB 客户端的 "max_allowed_packet" 限制（即接受的最大数据包限制），单位为字节，默认 67108864 (64 MB)
                                                # 该配置项从 DM v2.0.0 起弃用，DM 会自动获取连接 TiDB 的 "max_allowed_packet"
  session:                                      # 设置 TiDB 的 session 变量，在 v1.0.6 版本引入。更多变量及解释参见 `https://docs.pingcap.com/zh/tidb/stable/system-variables`
    sql_mode: "ANSI_QUOTES,NO_ZERO_IN_DATE,NO_ZERO_DATE" # 从 DM v2.0.0 起，如果配置文件中没有出现该项，DM 会自动从下游 TiDB 中获得适合用于 "sql_mode" 的值。手动配置该项具有更高优先级
    tidb_skip_utf8_check: 1                              # 从 DM v2.0.0 起，如果配置文件中没有出现该项，DM 会自动从下游 TiDB 中获得适合用于 "tidb_skip_utf8_check" 的值。手动配置该项具有更高优先级
    tidb_constraint_check_in_place: 0
  security:                       # 下游 TiDB TLS 相关配置
    ssl-ca: "/path/to/ca.pem"
    ssl-cert: "/path/to/cert.pem"
    ssl-key: "/path/to/key.pem"

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
    action: Ignore                              # 对与符合匹配规则的 binlog 迁移（Do）还是忽略(Ignore)
  filter-rule-2:
    schema-pattern: "test_*"
    events: ["all dml"]
    action: Do

expression-filter:                   # 定义数据源迁移行变更的过滤规则，可以定义多个规则
  # 过滤 `expr_filter`.`tbl` 的 c 为偶数的插入
  even_c:                            # 规则名称
    schema: "expr_filter"            # 要匹配的上游数据库库名，不支持通配符匹配或正则匹配
    table: "tbl"                     # 要匹配的上游表名，不支持通配符匹配或正则匹配
    insert-value-expr: "c % 2 = 0"

block-allow-list:                    # 定义数据源迁移表的过滤规则，可以定义多个规则。如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
  bw-rule-1:                         # 规则名称
    do-dbs: ["~^test.*", "user"]     # 迁移哪些库
    ignore-dbs: ["mysql", "account"] # 忽略哪些库
    do-tables:                       # 迁移哪些表
    - db-name: "~^test.*"
      tbl-name: "~^t.*"
    - db-name: "user"
      tbl-name: "information"
  bw-rule-2:                         # 规则名称
    ignore-tables:                   # 忽略哪些表
    - db-name: "user"
      tbl-name: "log"

mydumpers:                           # dump 处理单元的运行配置参数
  global:                            # 配置名称
    threads: 4                       # dump 处理单元从上游数据库实例导出数据的线程数量，默认值为 4
    chunk-filesize: 64               # dump 处理单元生成的数据文件大小，默认值为 64，单位为 MB
    extra-args: "--consistency none" # dump 处理单元的其他参数，不需要在 extra-args 中配置 table-list，DM 会自动生成

loaders:                             # load 处理单元的运行配置参数
  global:                            # 配置名称
    pool-size: 16                    # load 处理单元并发执行 dump 处理单元的 SQL 文件的线程数量，默认值为 16，当有多个实例同时向 TiDB 迁移数据时可根据负载情况适当调小该值
    dir: "./dumped_data"             # dump 处理单元输出 SQL 文件的目录，同时也是 load 处理单元读取文件的目录。该配置项的默认值为 "./dumped_data"。同实例对应的不同任务必须配置不同的目录


syncers:                             # sync 处理单元的运行配置参数
  global:                            # 配置名称
    worker-count: 16                 # 应用已传输到本地的 binlog 的并发线程数量，默认值为 16。调整此参数不会影响上游拉取日志的并发，但会对下游产生显著压力。
    batch: 100                       # sync 迁移到下游数据库的一个事务批次 SQL 语句数，默认值为 100，建议一般不超过 500。
    enable-ansi-quotes: true         # 若 `session` 中设置 `sql-mode: "ANSI_QUOTES"`，则需开启此项

    # 设置为 true，则将来自上游的 `INSERT` 改写为 `REPLACE`，将 `UPDATE` 改写为 `DELETE` 与 `REPLACE`，保证在表结构中存在主键或唯一索引的条件下迁移数据时可以重复导入 DML。
    safe-mode: false
    # 设置为 true，DM 会在不增加延迟的情况下，尽可能地将上游对同一条数据的多次操作压缩成一次操作。
    # 如 INSERT INTO tb(a,b) VALUES(1,1); UPDATE tb SET b=11 WHERE a=1; 会被压缩成 INSERT INTO tb(a,b) VALUES(1,11); 其中 a 为主键
    # 如 UPDATE tb SET b=1 WHERE a=1; UPDATE tb(a,b) SET b=2 WHERE a=1; 会被压缩成 UPDATE tb(a,b) SET b=2 WHERE a=1; 其中 a 为主键
    # 如 DELETE FROM tb WHERE a=1; INSERT INTO tb(a,b) VALUES(1,1); 会被压缩成 REPLACE INTO tb(a,b) VALUES(1,1); 其中 a 为主键
    compact: false
    # 设置为 true，DM 会尽可能地将多条同类型的语句合并到一条语句中，生成一条带多行数据的 SQL 语句。
    # 如 INSERT INTO tb(a,b) VALUES(1,1); INSERT INTO tb(a,b) VALUES(2,2); 会变成 INSERT INTO tb(a,b) VALUES(1,1),(2,2);
    # 如 UPDATE tb SET b=11 WHERE a=1; UPDATE tb(a,b) set b=22 WHERE a=2; 会变成 INSERT INTO tb(a,b) VALUES(1,11),(2,22) ON DUPLICATE KEY UPDATE a=VALUES(a), b=VALUES(b); 其中 a 为主键
    # 如 DELETE FROM tb WHERE a=1; DELETE FROM tb WHERE a=2 会变成 DELETE FROM tb WHERE (a) IN (1),(2)；其中 a 为主键
    multiple-rows: false

# ----------- 实例配置 -----------
mysql-instances:
  -
    source-id: "mysql-replica-01"           # 对应 source.toml 中的 `source-id`
    meta:                                   # `task-mode` 为 `incremental` 且下游数据库的 `checkpoint` 不存在时 binlog 迁移开始的位置; 如果 checkpoint 存在，则以 `checkpoint` 为准
      binlog-name: binlog.000001
      binlog-pos: 4
      binlog-gtid: "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"  # 对于 source 中指定了 `enable-gtid: true` 的增量任务，需要指定该值

    route-rules: ["route-rule-1", "route-rule-2"]    # 该上游数据库实例匹配的表到下游数据库的 table routing 规则名称
    filter-rules: ["filter-rule-1", "filter-rule-2"] # 该上游数据库实例匹配的表的 binlog event filter 规则名称
    block-allow-list:  "bw-rule-1"                   # 该上游数据库实例匹配的表的 block-allow-list 过滤规则名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
    expression-filters: ["even_c"]                   # 使用名为 even_c 的表达式过滤规则

    mydumper-config-name: "global"          # mydumpers 配置的名称
    loader-config-name: "global"            # loaders 配置的名称
    syncer-config-name: "global"            # syncers 配置的名称

  -
    source-id: "mysql-replica-02"  # 对应 source.toml 中的 `source-id`
    mydumper-thread: 4             # dump 处理单元用于导出数据的线程数量，等同于 mydumpers 配置中的 `threads`，当同时指定它们时 `mydumper-thread` 优先级更高
    loader-thread: 16              # load 处理单元用于导入数据的线程数量，等同于 loaders 配置中的 `pool-size`，当同时指定它们时 `loader-thread` 优先级更高。当有多个实例同时向 TiDB 迁移数据时可根据负载情况适当调小该值
    syncer-thread: 16              # sync 处理单元用于复制增量数据的线程数量，等同于 syncers 配置中的 `worker-count`，当同时指定它们时 `syncer-thread` 优先级更高。当有多个实例同时向 TiDB 迁移数据时可根据负载情况适当调小该值
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
    - `incremental`：只通过 binlog 把上游数据库的增量修改复制到下游数据库, 可以设置实例配置的 `meta` 配置项来指定增量复制开始的位置。
    - `all`：`full` + `incremental`。先全量备份上游数据库，将数据全量导入到下游数据库，然后从全量数据备份时导出的位置信息 (binlog position) 开始通过 binlog 增量复制数据到下游数据库。

### 功能配置集

全局配置主要包含下列功能配置集：

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `routes` | 上游和下游表之间的路由 table routing 规则集。如果上游与下游的库名、表名一致，则不需要配置该项。使用场景及示例配置参见 [Table Routing](/dm/dm-key-features.md#table-routing) |
| `filters` | 上游数据库实例匹配的表的 binlog event filter 规则集。如果不需要对 binlog 进行过滤，则不需要配置该项。使用场景及示例配置参见 [Binlog Event Filter](/dm/dm-key-features.md#binlog-event-filter) |
| `block-allow-list` | 该上游数据库实例匹配的表的 block & allow lists 过滤规则集。建议通过该项指定需要迁移的库和表，否则会迁移所有的库和表。使用场景及示例配置参见 [Block & Allow Lists](/dm/dm-key-features.md#block--allow-table-lists) |
| `mydumpers` | dump 处理单元的运行配置参数。如果默认配置可以满足需求，则不需要配置该项，也可以只使用 `mydumper-thread` 对 `thread` 配置项单独进行配置。 |
| `loaders` | load 处理单元的运行配置参数。如果默认配置可以满足需求，则不需要配置该项，也可以只使用 `loader-thread` 对 `pool-size` 配置项单独进行配置。 |
| `syncers` | sync 处理单元的运行配置参数。如果默认配置可以满足需求，则不需要配置该项，也可以只使用 `syncer-thread` 对 `worker-count` 配置项单独进行配置。 |

各个功能配置集的参数及解释参见[完整配置文件示例](#完整配置文件示例)中的注释说明。

## 实例配置

本小节定义具体的数据迁移子任务，DM 支持从单个或者多个上游 MySQL 实例迁移数据到同一个下游数据库实例。

在该项配置中设置数据迁移子任务中各个功能对应的配置集中的配置名称，关于这些配置项的更多配置细节，参见[功能配置集](#功能配置集)的相关配置项，对应关系如下：

| 配置项 | 相关配置项 |
| :------ | :------------------ |
| `route-rules` | `routes` |
| `filter-rules` | `filters` |
| `block-allow-list` | `block-allow-list` |
| `mydumper-config-name` | `mydumpers` |
| `loader-config-name` | `loaders` |
| `syncer-config-name` | `syncers`  |

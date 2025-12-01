---
title: DM 任务完整配置文件介绍
summary: 本文介绍了 Data Migration (DM) 的任务完整配置文件，包括全局配置和实例配置两部分。全局配置包括任务基本信息配置和功能配置集，功能配置集包括路由规则、过滤规则、block-allow-list、mydumpers、loaders 和 syncers。实例配置定义了具体的数据迁移子任务，包括路由规则、过滤规则、block-allow-list、mydumpers、loaders 和 syncers 的配置名称。
---

# DM 任务完整配置文件介绍

本文档主要介绍 Data Migration (DM) 的任务完整的配置文件，包含[全局配置](#全局配置)和[实例配置](#实例配置)两部分。

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
shard-mode: "pessimistic"       # 任务协调模式，可选的模式有 ""、"pessimistic、"optimistic"。默认值为 "" 即无需协调。如果是分库分表合并任务，请设置为悲观协调模式 "pessimistic"。
                                # 在 v2.0.6 版本后乐观模式逐渐成熟，深入了解乐观协调模式的原理和使用限制后，也可以设置为乐观协调模式 "optimistic"
strict-optimistic-shard-mode: false # 仅在乐观协调模式下生效，限制乐观协调模式的行为，默认值为 false。在 v7.2.0 中引入，详见 https://docs.pingcap.com/zh/tidb/v7.2/feature-shard-merge-optimistic
meta-schema: "dm_meta"          # 下游储存 `meta` 信息的数据库
# timezone: "Asia/Shanghai"     # 指定数据迁移任务时 SQL Session 使用的时区。DM 默认使用目标库的全局时区配置进行数据迁移，并且自动确保同步数据的正确性。使用自定义时区依然可以确保整个流程的正确性，但一般不需要手动指定。

case-sensitive: false           # schema/table 是否大小写敏感
online-ddl: true                # 支持上游 "gh-ost" 、"pt" 的自动处理
online-ddl-scheme: "gh-ost"     # `online-ddl-scheme` 已被弃用，建议使用 `online-ddl`。
clean-dump-file: true           # 是否清理 dump 阶段产生的文件，包括 metadata 文件、建库建表 SQL 文件以及数据导入 SQL 文件
collation_compatible: "loose"   # 同步 CREATE 语句中缺省 Collation 的方式，可选 "loose" 和 "strict"，默认为 "loose"。"loose" 模式不会显式补充上游缺省的 Collation，"strict" 会显式补充上游缺省的 Collation。当使用 "strict" 模式，但下游不支持上游缺省的 Collation 时，下游可能会报错。
ignore-checking-items: []       # 忽略检查项。可用值请参考 precheck 说明：https://docs.pingcap.com/zh/tidb/stable/dm-precheck。

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
    sql_require_primary_key: OFF   # 在 session 级别控制表是否必须有主键。DM 任务创建期间，会在 TiDB 创建几个元数据表，其中有些表是无主键表。如果开启该参数，这些无主键的元数据表就无法被创建出来，导致 DM 任务创建失败。因此，需要将该参数设置为 `OFF`。
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
    # 可选配置：提取各分库分表的源信息，并写入下游用户自建的列，用于标识合表中各行数据的来源。如果配置该项，需要提前在下游手动创建合表，具体可参考 “table routing 文档” <https://docs.pingcap.com/zh/tidb/dev/dm-table-routing>。
    # extract-table:                                        # 提取分表去除 t_ 的后缀信息，并写入下游合表 c_table 列，例如，t_01 分表的数据会提取 01 写入下游 c_table 列
    #   table-regexp: "t_(.*)"
    #   target-column: "c_table"
    # extract-schema:                                       # 提取分库去除 test_ 的后缀信息，并写入下游合表 c_schema 列，例如，test_02 分库的数据会提取 02 写入下游 c_schema 列
    #   schema-regexp: "test_(.*)"
    #   target-column: "c_schema"
    # extract-source:                                       # 提取数据库源实例信息写入 c_source 列，例如，mysql-replica-01 数据源实例的数据会提取 mysql-replica-01 写入下游 c_source 列
    #   source-regexp: "(.*)"
    #   target-column: "c_source"
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
    threads: 4                       # dump 处理单元从上游数据库实例导出数据和 check-task 访问上游的线程数量，默认值为 4
    chunk-filesize: 64               # dump 处理单元生成的数据文件大小，默认值为 64，单位为 MB
    extra-args: "--consistency auto" # dump 处理单元的其他参数，不需要在 extra-args 中配置 table-list，DM 会自动生成

loaders:                             # load 处理单元的运行配置参数
  global:                            # 配置名称
    pool-size: 16                    # load 处理单元并发执行 dump 处理单元的 SQL 文件的线程数量，默认值为 16，当有多个实例同时向 TiDB 迁移数据时可根据负载情况适当调小该值

    # 保存上游全量导出数据的目录。该配置项的默认值为 "./dumped_data"。
    # 支持配置为本地文件系统路径，也支持配置为 Amazon S3 路径，如: s3://dm_bucket/dumped_data?endpoint=s3-website.us-east-2.amazonaws.com&access_key=s3accesskey&secret_access_key=s3secretkey&force_path_style=true
    dir: "./dumped_data"

    # 全量阶段数据导入的模式。可以设置为如下几种模式：
    # - "logical"(默认)。使用 TiDB Lightning 逻辑导入模式进行导入。文档：https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-logical-import-mode
    # - "physical"。使用 TiDB Lightning 物理导入模式进行导入。文档：https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-physical-import-mode
    #   当前 "physical" 为实验特性，不建议在生产环境中使用。
    import-mode: "logical"
    # 逻辑导入模式针对冲突数据的解决方式：
    # - "replace"（默认值）。表示用最新数据替代已有数据。
    # - "ignore"。保留已有数据，忽略新数据。
    # - "error"。插入重复数据时报错并停止同步任务。
    on-duplicate-logical: "replace"
    # 物理导入模式针对冲突数据的解决方式：
    # - "none"（默认）。对应 TiDB Lightning 物理导入模式冲突数据检测的 "none" 选项 
    # (https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-physical-import-mode-usage#冲突数据检测)，
    # 表示遇到冲突数据时不进行处理。该模式性能最佳，但下游数据库会遇到数据索引不一致的问题。
    # - "manual"。对应 TiDB Lightning 物理导入模式冲突数据检测的 "replace" 选项 
    # (https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-physical-import-mode-usage#冲突数据检测)。
    # 在遇到冲突数据时将所有相互冲突的数据删除，并记录在 ${meta-schema}_${name}.conflict_error_v3 表中。
    # 在本配置文件中，会记录在 dm_meta_test.conflict_error_v3 表中。全量导入阶段结束后，任务
    # 会暂停并提示用户查询这张表并按照文档进行手动处理。使用 resume-task 命令让任务恢复运行并
    # 进入到增量同步阶段。
    on-duplicate-physical: "none"
    # 物理导入模式用作本地排序的目录位置，该选项的默认值与 dir 配置项一致。具体说明可以参见 TiDB Lightning 对存储空间的需求：https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-physical-import-mode#运行环境需求
    sorting-dir-physical: "./dumped_data"
    # 磁盘空间限制，对应 TiDB Lightning disk-quota 配置。具体说明参见文档：https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-physical-import-mode-usage#磁盘资源配额-从-v620-版本开始引入
    disk-quota-physical: "0"
    # 物理导入模式在导入完成一张表后，对每一个表执行 `ADMIN CHECKSUM TABLE <table>` 进行数据校验的配置：
    # - "required"（默认值）。表示导入完成后进行数据校验，如果校验失败会让任务暂停，需要用户手动处理。
    # - "optional"。表示导入完成后进行数据校验，如果校验失败会打印 warn 日志，任务不会暂停。
    # - "off"。表示导入完成后不进行数据校验。
    # Checksum 对比失败通常表示导入异常（数据丢失或数据不一致），因此建议总是开启 Checksum。
    checksum-physical: "required"
    # 配置在 CHECKSUM 结束后是否对所有表执行 `ANALYZE TABLE <table>` 操作。
    # - "required"（默认值）。表示导入完成后进行 ANALYZE 操作，ANALYZE 操作失败时任务暂停，需要用户手动处理。
    # - "optional"。表示导入完成后进行 ANALYZE 操作，ANALYZE 操作失败时输出警告日志，任务不会暂停。
    # - "off"。表示导入完成后不进行 ANALYZE 操作。
    # ANALYZE 只影响统计数据，在大部分场景下建议不开启 ANALYZE。
    analyze: "off"
    # 物理导入模式向 TiKV 写入 KV 数据的并发度。当 dm-worker 和 TiKV 网络传输速度超过万兆时，可适当增加这个值。
    # range-concurrency: 16
    # 物理导入模式向 TiKV 发送 KV 数据时是否启用压缩。目前仅支持 Gzip 压缩算法，可填写 "gzip" 或 "gz"。默认不启用压缩。
    # compress-kv-pairs: ""
    # PD server 的地址，填一个即可。该值为空时，默认使用 TiDB 查询到的 PD 地址信息。
    # pd-addr: "192.168.0.1:2379"

syncers:                             # sync 处理单元的运行配置参数
  global:                            # 配置名称
    worker-count: 16                 # 应用已传输到本地的 binlog 的并发线程数量，默认值为 16。调整此参数不会影响上游拉取日志的并发，但会对下游产生显著压力。
    batch: 100                       # sync 迁移到下游数据库的一个事务批次 SQL 语句数，默认值为 100，建议一般不超过 500。
    enable-ansi-quotes: true         # 若 `session` 中设置 `sql-mode: "ANSI_QUOTES"`，则需开启此项

    # 设置为 true，则将来自上游的 `INSERT` 改写为 `REPLACE`，将 `UPDATE` 改写为 `DELETE` 与 `REPLACE`，保证在表结构中存在主键或唯一索引的条件下迁移数据时可以重复导入 DML。
    safe-mode: false
    # 自动安全模式的持续时间
    # 如不设置或者设置为 ""，则默认为 `checkpoint-flush-interval`（默认为 30s）的两倍，即 60s。
    # 如设置为 "0s"，则在 DM 自动进入安全模式的时候报错。
    # 如设置为正常值，例如 "1m30s"，则在该任务异常暂停、记录 `safemode_exit_point` 失败、或是 DM 进程异常退出时，把安全模式持续时间调整为 1 分 30 秒。详情可见[自动开启安全模式](https://docs.pingcap.com/zh/tidb/stable/dm-safe-mode#自动开启)。
    safe-mode-duration: "60s"
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

validators:              # 增量数据校验的运行配置参数
  global:                # 配置名称
    # full：校验每一行中每一列数据是否正确
    # fast：仅校验这一行是否有成功迁移到下游
    # none：不校验
    mode: full           # 可选填 full，fast 和 none，默认是 none，即不开启校验。
    worker-count: 4      # 后台校验的 validation worker 数量，默认是 4 个
    row-error-delay: 30m # 某一行多久没有校验通过会被标记为 error row，默认是 30 分钟

# ----------- 实例配置 -----------
mysql-instances:
  -
    source-id: "mysql-replica-01"           # 对应 source.toml 中的 `source-id`
    meta:                                   # `task-mode` 为 `incremental` 且下游数据库的 `checkpoint` 不存在时 binlog 迁移开始的位置; 如果 checkpoint 存在，则以 `checkpoint` 为准。如果 `meta` 项和下游数据库的 `checkpoint` 都不存在，则从上游当前最新的 binlog 位置开始迁移
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
    validator-config-name: "global"         # validators 配置的名称
  -
    source-id: "mysql-replica-02"  # 对应 source.toml 中的 `source-id`
    mydumper-thread: 4             # dump 处理单元用于导出数据的线程数量，等同于 mydumpers 配置中的 `threads`，当同时指定它们时 `mydumper-thread` 优先级更高
    loader-thread: 16              # load 处理单元用于导入数据的线程数量，等同于 loaders 配置中的 `pool-size`，当同时指定它们时 `loader-thread` 优先级更高。当有多个实例同时向 TiDB 迁移数据时可根据负载情况适当调小该值
    syncer-thread: 16              # sync 处理单元用于复制增量数据的线程数量，等同于 syncers 配置中的 `worker-count`，当同时指定它们时 `syncer-thread` 优先级更高。当有多个实例同时向 TiDB 迁移数据时可根据负载情况适当调小该值
```

## 配置顺序

通过上面的配置文件示例，可以看出配置文件总共分为两个部分：`全局配置`和`实例配置`，其中`全局配置`又分为`基本信息配置`和`功能配置集`。配置顺序如下：

1. 编辑[全局配置](#全局配置)。
2. 根据全局配置编辑[实例配置](#实例配置)。

## 全局配置

### 任务基本信息配置

配置任务的基本信息，配置项的说明参见以上示例配置文件中的注释。其中 `task-mode` 需要特殊说明：

`task-mode`

- 描述：任务模式，可以通过任务模式来指定需要执行的数据迁移工作。
- 值为字符串（`full`，`incremental` 或 `all`）。
    - `full`：只全量备份上游数据库，然后将数据全量导入到下游数据库。
    - `incremental`：只通过 binlog 把上游数据库的增量修改复制到下游数据库，可以设置实例配置的 `meta` 配置项来指定增量复制开始的位置。
    - `all`：`full` + `incremental`。先全量备份上游数据库，将数据全量导入到下游数据库，然后从全量数据备份时导出的位置信息 (binlog position) 开始通过 binlog 增量复制数据到下游数据库。

### 功能配置集

全局配置主要包含下列功能配置集：

#### `routes`

- 上游和下游表之间的路由 table routing 规则集。如果上游与下游的库名、表名一致，则不需要配置该项。使用场景及示例配置参见 [Table Routing](/dm/dm-table-routing.md)。

#### `filters`

- 上游数据库实例匹配的表的 binlog event filter 规则集。如果不需要对 binlog 进行过滤，则不需要配置该项。使用场景及示例配置参见 [Binlog Event Filter](/dm/dm-binlog-event-filter.md)。

#### `block-allow-list`

- 该上游数据库实例匹配的表的 block & allow lists 过滤规则集。建议通过该项指定需要迁移的库和表，否则会迁移所有的库和表。使用场景及示例配置参见 [Block & Allow Lists](/dm/dm-block-allow-table-lists.md)。

#### `mydumpers`

- dump 处理单元的运行配置参数。如果默认配置可以满足需求，则不需要配置该项，也可以只使用 `mydumper-thread` 对 `thread` 配置项单独进行配置。

#### `loaders`

- load 处理单元的运行配置参数。如果默认配置可以满足需求，则不需要配置该项，也可以只使用 `loader-thread` 对 `pool-size` 配置项单独进行配置。

#### `syncers`

- sync 处理单元的运行配置参数。如果默认配置可以满足需求，则不需要配置该项，也可以只使用 `syncer-thread` 对 `worker-count` 配置项单独进行配置。

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

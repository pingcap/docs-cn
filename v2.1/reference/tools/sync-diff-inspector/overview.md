---
title: sync-diff-inspector 用户文档
category: tools
aliases: ['/docs-cn/v2.1/reference/tools/sync-diff-inspector/']
---

# sync-diff-inspector 用户文档

sync-diff-inspector 是一个用于校验 MySQL／TiDB 中两份数据是否一致的工具。该工具提供了修复数据的功能（适用于修复少量不一致的数据）。

主要功能：

* 对比表结构和数据
* 如果数据不一致，则生成用于修复数据的 SQL 语句
* 支持[不同库名或表名的数据校验](/reference/tools/sync-diff-inspector/route-diff.md)
* 支持[分库分表场景下的数据校验](/reference/tools/sync-diff-inspector/shard-diff.md)
* 支持 [TiDB 主从集群的数据校验](/reference/tools/sync-diff-inspector/tidb-diff.md)

GitHub 地址：[sync-diff-inspector](https://github.com/pingcap/tidb-tools/tree/master/sync_diff_inspector)

下载地址：[tidb-enterprise-tools-latest-linux-amd64](https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz)

## sync-diff-inspector 的使用

### 使用限制

* 目前不支持在线校验，需要保证上下游校验的表中没有数据写入，或者保证某个范围内的数据不再变更，通过配置 `range` 来校验这个范围内的数据。

* 不支持 JSON、BIT、BINARY、BLOB 等类型的数据，在校验时需要设置 `ignore-columns` 忽略检查这些类型的数据。

* FLOAT、DOUBLE 等浮点数类型在 TiDB 和 MySQL 中的实现方式不同，在计算 checksum 时可能存在差异，如果发现因为这些类型的数据导致的数据校验不一致，需要设置 `ignore-columns` 忽略这些列的检查。

### 数据库权限

sync-diff-inspector 需要获取表结构信息、查询数据、建 checkpoint 库保存断点信息，需要的数据库权限如下：

- 上游数据库

    - SELECT（查数据进行对比）

    - SHOW_DATABASES (查看库名)

    - RELOAD (查看表结构)

- 下游数据库
  
    - SELECT （查数据进行对比）

    - CREATE （创建 checkpoint 库和表）

    - DELETE （删除 checkpoint 表中的信息）

    - INSERT  （写入 checkpoint 表）

    - UPDATE（修改 checkpoint 表）

    - SHOW_DATABASES (查看库名)

    - RELOAD (查看表结构)

### 配置文件说明

sync-diff-inspector 的配置总共分为三个部分：

- Global config: 通用配置，包括日志级别、划分 chunk 的大小、校验的线程数量等。
- Tables config: 配置校验哪些表，如果有的表在上下游有一定的映射关系或者有一些特殊要求，则需要对指定的表进行配置。
- Databases config: 配置上下游数据库实例。

下面是一个完整配置文件的说明：

``` toml
# Diff Configuration.

######################### Global config #########################

# 日志级别，可以设置为 info、debug
log-level = "info"

# sync-diff-inspector 根据主键／唯一键／索引将数据划分为多个 chunk，
# 对每一个 chunk 的数据进行对比。使用 chunk-size 设置 chunk 的大小
chunk-size = 1000

# 检查数据的线程数量
check-thread-count = 4

# 抽样检查的比例，如果设置为 100 则检查全部数据
sample-percent = 100

# 通过计算 chunk 的 checksum 来对比数据，如果不开启则逐行对比数据
use-checksum = true

# 如果设置为 true 则只会通过计算 checksum 来校验数据，如果上下游的 checksum 不一致也不会查出数据再进行校验
only-use-checksum = false

# 是否使用上次校验的 checkpoint，如果开启，则只校验上次未校验以及校验失败的 chunk
use-checkpoint = true

# 不对比数据
ignore-data-check = false

# 不对比表结构
ignore-struct-check = false

# 保存用于修复数据的 sql 的文件名称
fix-sql-file = "fix.sql"

######################### Tables config #########################

# 如果需要对比大量的不同库名或者表名的表的数据，可以通过 table-rule 来设置映射关系。可以只配置 schema 或者 table 的映射关系，也可以都配置
#[[table-rules]]
    # schema-pattern 和 table-pattern 支持通配符 *?
    #schema-pattern = "test_*"
    #table-pattern = "t_*"
    #target-schema = "test"
    #target-table = "t"

# 配置需要对比的*目标数据库*中的表
[[check-tables]]
    # 目标库中数据库的名称
    schema = "test"

    # 需要检查的表
    tables = ["test1", "test2", "test3"]

    # 支持使用正则表达式配置检查的表，需要以‘~’开始，
    # 下面的配置会检查所有表名以‘test’为前缀的表
    # tables = ["~^test.*"]
    # 下面的配置会检查配置库中所有的表
    # tables = ["~^"]

# 对部分表进行特殊的配置，配置的表必须包含在 check-tables 中
[[table-config]]
    # 目标库中数据库的名称
    schema = "test"

    # 表名
    table = "test3"

    # 指定用于划分 chunk 的列，如果不配置该项，sync-diff-inspector 会选取一个合适的列（主键／唯一键／索引）
    index-field = "id"

    # 指定检查的数据的范围，需要符合 sql 中 where 条件的语法
    range = "age > 10 AND age < 20"

    # 如果是对比多个分表与总表的数据，则设置为 true
    is-sharding = false

    # 在某些情况下字符类型的数据的排序会不一致，通过指定 collation 来保证排序的一致，
    # 需要与数据库中 charset 的设置相对应
    # collation = "latin1_bin"

    # 忽略某些列的检查，例如 sync-diff-inspector 目前还不支持的一些类型（json，bit，blob 等），
    # 或者是浮点类型数据在 TiDB 和 MySQL 中的表现可能存在差异，可以使用 ignore-columns 忽略检查这些列
    # ignore-columns = ["name"]

# 下面是一个对比不同库名和表名的两个表的配置示例
[[table-config]]
    # 目标库名
    schema = "test"

    # 目标表名
    table = "test2"

    # 非分库分表场景，设置为 false
    is-sharding = false

    # 源数据的配置
    [[table-config.source-tables]]
        # 源库的实例 id
        instance-id = "source-1"
        # 源数据库的名称
        schema = "test"
        # 源表的名称
        table  = "test1"

######################### Databases config #########################

# 源数据库实例的配置
[[source-db]]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = "123456"
    # 源数据库实例的 id，唯一标识一个数据库实例
    instance-id = "source-1"
    # 使用 TiDB 的 snapshot 功能，如果开启的话会使用历史数据进行对比
    # snapshot = "2016-10-08 16:45:26"

# 目标数据库实例的配置
[target-db]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = "123456"
    # 使用 TiDB 的 snapshot 功能，如果开启的话会使用历史数据进行对比
    # snapshot = "2016-10-08 16:45:26"
```

### 运行 sync-diff-inspector

执行如下命令：

``` bash
./bin/sync_diff_inspector --config=./config.toml
```

该命令最终会在日志中输出一个检查报告，说明每个表的检查情况。如果数据存在不一致的情况，sync-diff-inspector 会生成 SQL 修复不一致的数据，并将这些 SQL 语句保存到 `fix.sql` 文件中。

### 注意事项

* sync-diff-inspector 在校验数据时会消耗一定的服务器资源，需要避免在业务高峰期间校验。
* TiDB 使用的 collation 为 `utf8_bin`。如果对 MySQL 和 TiDB 的数据进行对比，需要注意 MySQL 中表的 collation 设置。如果表的主键／唯一键为 varchar 类型，且 MySQL 中 collation 设置与 TiDB 不同，可能会因为排序问题导致最终校验结果不正确，需要在 sync-diff-inspector 的配置文件中增加 collation 设置。
* sync-diff-inspector 会优先使用 TiDB 的统计信息来划分 chunk，需要尽量保证统计信息精确，可以在**业务空闲期**手动执行 `analyze table {table_name}`。
* table-rule 的规则需要特殊注意，例如设置了 `schema-pattern="test1"`，`target-schema="test2"`，会对比 source 中的 `test1` 库和 target 中的 `test2` 库；如果 source 中有 `test2` 库，该库也会和 target 中的 `test2` 库进行对比。
* 生成的 `fix.sql` 仅作为修复数据的参考，需要确认后再执行这些 SQL 修复数据。

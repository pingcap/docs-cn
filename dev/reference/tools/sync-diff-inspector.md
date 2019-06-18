---
title: sync-diff-inspector 用户文档
category: tools
aliases: ['/docs-cn/tools/sync-diff-inspector/']
---

# sync-diff-inspector 用户文档

## sync-diff-inspector 简介

sync-diff-inspector 是一个用于校验 MySQL／TiDB 中两份数据是否一致的工具，该工具提供了修复数据的功能（适用于修复少量不一致的数据）。

主要功能：

* 对比表结构和数据
* 如果数据不一致，则生成用于修复数据的 SQL
* 支持多个表的数据与单个表数据的比较（针对分库分表同步数据到总表的场景）
* 支持不同库名／表名的数据的比较

GitHub 地址：[sync-diff-inspector](https://github.com/pingcap/tidb-tools/tree/master/sync_diff_inspector)

下载地址：[tidb-enterprise-tools-latest-linux-amd64](https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz)

## sync-diff-inspector 的使用

### 通用配置文件说明

``` toml
# Diff Configuration.

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

# 不对比数据
ignore-data-check = false

# 不对比表结构
ignore-struct-check = false

# 保存用于修复数据的 sql 的文件名称
fix-sql-file = "fix.sql"

# 如果需要使用 TiDB 的统计信息划分 chunk，需要设置 tidb-instance-id，值为 source-db 或者 target-db 中配置的 instance-id 的值
# tidb-instance-id = "target-1"

# 如果需要对比大量的不同库名或者表名的表的数据，可以通过 table-rule 来设置映射关系。可以只配置 schema 或者 table 的映射关系，也可以都配置
#[[table-rules]]
# schema-pattern 和 table-pattern 支持正则表达式
#schema-pattern = "test_*"
#table-pattern = "t_*"
#target-schema = "test"
#target-table = "t"

# 配置需要对比的目标数据库中的表
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

# 忽略某些列的检查，但是这些列仍然可以用于划分 chunk、对检查的数据进行排序
# ignore-columns = ["name"]

# 移除某些列，检查时会将这些列从表结构中移除，既不会检查这些列的数据，
# 也不会用这些列做 chunk 的划分，或者用于对数据进行排序
# remove-columns = ["name"]

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

# 源数据库实例的配置
[[source-db]]
host = "127.0.0.1"
port = 3306
user = "root"
password = ""
# 源数据库实例的 id，唯一标识一个数据库实例
instance-id = "source-1"
# 使用 TiDB 的 snapshot 功能，如果开启的话会使用历史数据进行对比
# snapshot = "2016-10-08 16:45:26"

# 目标数据库实例的配置
[target-db]
host = "127.0.0.1"
port = 4000
user = "root"
password = ""
# 使用 TiDB 的 snapshot 功能，如果开启的话会使用历史数据进行对比
# snapshot = "2016-10-08 16:45:26"
```

### 分库分表场景下数据对比的配置示例

假设有两个 MySQL 实例，使用同步工具同步到一个 TiDB 中，场景如图所示：

![shard-table-sync](../media/shard-table-sync.png)

如果需要检查同步后数据是否一致，可以使用如下的配置对比数据：

``` toml
# diff Configuration.

# 配置需要对比的目标数据库中的表
[[check-tables]]
# 库的名称
schema = "test"

# table list which need check in target database. 
# in sharding mode, you must set config for every table in table-config, otherwise will not check the table.
# 需要检查的表的名称
tables = ["test"]


# 配置该表对应的分表的相关配置
[[table-config]]
# 目标库的名称
schema = "test"

# 目标库中表的名称
table = "test"

# 为分库分表场景下数据的对比，设置为 true
is-sharding = true

# 源数据表的配置
[[table-config.source-tables]]
# 源数据库实例的 id
instance-id = "source-1"
schema = "test"
table  = "test1"

[[table-config.source-tables]]
# 源数据库实例的 id
instance-id = "source-1"
schema = "test"
table  = "test2"

[[table-config.source-tables]]
# 源数据库实例的 id
instance-id = "source-2"
schema = "test"
table  = "test3"

# 源数据库实例的配置
[[source-db]]
host = "127.0.0.1"
port = 3306
user = "root"
password = ""
instance-id = "source-1"

# 源数据库实例的配置
[[source-db]]
host = "127.0.0.2"
port = 3306
user = "root"
password = ""
instance-id = "source-2"

# 目标数据库实例的配置
[target-db]
host = "127.0.0.3"
port = 4000
user = "root"
password = ""
instance-id = "target-1"
```

### 运行 sync-diff-inspector

执行如下命令：

``` bash
./bin/sync_diff_inspector --config=./config.toml
```

该命令最终会在日志中输出一个检查报告，说明每个表的检查情况。如果数据存在不一致的情况，sync-diff-inspector 会生成 SQL 修复不一致的数据，并将这些 SQL 语句保存到 `fix.sql` 文件中。

### 注意

* TiDB 使用的 collation 为 `utf8_bin`，如果对 MySQL 和 TiDB 的数据进行对比，需要注意 MySQL 中表的 collation 设置。如果表的主键／唯一键为 varchar 类型，且 MySQL 中 collation 设置与 TiDB 不同，可能会因为排序问题导致最终校验结果不正确，需要在 sync-diff-inspector 的配置文件中增加 collation 设置。
* 如果设置了 `tidb-instance-id` 使用 TiDB 的统计信息来划分 chunk，需要尽量保证统计信息精确，可以在*业务空闲期*手动执行 `analyze table {table_name}`。
* table-rule 的规则需要特殊注意，例如设置了 `schema-pattern="test1"`，`target-schema="test2"`，会对比 source 中的 `test1` 库和 target 中的 `test2` 库；如果 source 中有 `test2` 库，该库也会和 target 中的 `test2` 库进行对比。

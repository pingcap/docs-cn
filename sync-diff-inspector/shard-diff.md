---
title: 分库分表场景下的数据校验
---

# 分库分表场景下的数据校验

sync-diff-inspector 支持对分库分表场景进行数据校验。例如有多个 MySQL 实例，使用同步工具 DM 同步到一个 TiDB 中，用户可以使用 sync-diff-inspector 对上下游数据进行校验。

## 使用 table-config 进行配置

使用 `table-config` 对 `table-0` 进行特殊配置，设置 `is-sharding=true`，并且在 `table-config.source-tables` 中配置上游表信息。这种配置方式需要对所有分表进行设置，适合上游分表数量较少，且分表的命名规则没有规律的场景。场景如图所示：

![shard-table-sync-1](/media/shard-table-sync-1.png)

sync-diff-inspector 完整的示例配置如下：

```toml
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

# 配置需要对比的目标数据库中的表
[[check-tables]]
    # 库的名称
    schema = "test"

    # 需要检查的表的名称
    tables = ["table-0"]

# 配置该表对应的分表的相关配置
[[table-config]]
    # 目标库的名称
    schema = "test"

    # 目标库中表的名称
    table = "table-0"

    # 为分库分表场景下数据的对比，设置为 true
    is-sharding = true

    # 源数据表的配置
    [[table-config.source-tables]]
    # 源数据库实例的 id
    instance-id = "MySQL-1"
    schema = "test"
    table  = "table-1"

    [[table-config.source-tables]]
    # 源数据库实例的 id
    instance-id = "MySQL-1"
    schema = "test"
    table  = "test-2"

    [[table-config.source-tables]]
    # 源数据库实例的 id
    instance-id = "MySQL-2"
    schema = "test"
    table  = "table-3"

######################### Databases config #########################

# 源数据库实例的配置
[[source-db]]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = "123456"
    instance-id = "MySQL-1"

# 源数据库实例的配置
[[source-db]]
    host = "127.0.0.2"
    port = 3306
    user = "root"
    password = "123456"
    instance-id = "MySQL-2"

# 目标数据库实例的配置
[target-db]
    host = "127.0.0.3"
    port = 4000
    user = "root"
    password = "123456"
    instance-id = "target-1"
```

## 使用 table-rules 进行配置

当上游分表较多，且所有分表的命名都符合一定的规则时，则可以使用 `table-rules` 进行配置。场景如图所示：

![shard-table-sync-2](/media/shard-table-sync-2.png)

sync-diff-inspector 完整的示例配置如下：

```
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

# 配置需要对比的目标数据库中的表
[[check-tables]]
    # 库的名称
    schema = "test"

    # 需要检查的表的名称
    tables = ["table-0"]

# 通过 table-rule 来设置上游分表与下游总表的映射关系。可以只配置 schema 或者 table 的映射关系，也可以都配置
[[table-rules]]
    # schema-pattern 和 table-pattern 支持通配符 *?
    # 在 source-db 中配置的上游数据库中所有满足 schema-pattern 和 table-pattern 规则的表都为 target-schema.target-table 的分表
    schema-pattern = "test"
    table-pattern = "table-*"
    target-schema = "test"
    target-table = "table-0"

######################### Databases config #########################

# 源数据库实例的配置
[[source-db]]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = "123456"
    instance-id = "MySQL-1"

# 源数据库实例的配置
[[source-db]]
    host = "127.0.0.2"
    port = 3306
    user = "root"
    password = "123456"
    instance-id = "MySQL-2"

# 目标数据库实例的配置
[target-db]
    host = "127.0.0.3"
    port = 4000
    user = "root"
    password = "123456"
    instance-id = "target-1"

```
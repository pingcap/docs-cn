---
title: 分库分表场景下的数据校验
---

# 分库分表场景下的数据校验

sync-diff-inspector 支持对分库分表场景进行数据校验。例如有多个 MySQL 实例，当你使用同步工具 [TiDB DM](https://docs.pingcap.com/zh/tidb-data-migration/stable/overview) 同步到一个 TiDB 时，可以使用 sync-diff-inspector 对上下游数据进行校验。

## 使用 datasource config 进行配置

使用 `Datasource config` 对 `table-0` 进行特殊配置，设置对应 `rules`，配置上游表与下游表的映射关系。这种配置方式需要对所有分表进行设置，适合上游分表数量较少，且分表的命名规则没有规律的场景。场景如图所示：

![shard-table-sync-1](/media/shard-table-sync-1.png)

sync-diff-inspector 完整的示例配置如下：

```toml
# Diff Configuration.

######################### Global config #########################

# 检查数据的线程数量，上下游数据库的连接数会略大于该值
check-thread-count = 4

# 如果开启，若表存在不一致，则输出用于修复的 SQL 语句
export-fix-sql = true

# 只对比表结构而不对比数据
check-struct-only = false


######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule1"]

[data-sources.mysql2]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule2"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""

########################### Routes ###########################
[routes.rule1]
schema-pattern = "test"        # 匹配数据源的库名，支持通配符 "*" 和 "?"
table-pattern = "table-[1-2]"  # 匹配数据源的表名，支持通配符 "*" 和 "?"
target-schema = "test"         # 目标库名
target-table = "table-0"       # 目标表名

[routes.rule2]
schema-pattern = "test"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
table-pattern = "table-3"    # 匹配数据源的表名，支持通配符 "*" 和 "?"
target-schema = "test"       # 目标库名
target-table = "table-0"     # 目标表名

######################### Task config #########################
[task]
    output-dir = "./output"

    source-instances = ["mysql1", "mysql2"]

    target-instance = "tidb0"

    # 需要比对的下游数据库的表，每个表需要包含数据库名和表名，两者由 `.` 隔开
    target-check-tables = ["test.table-0"]
```

当上游分表较多，且所有分表的命名都符合一定的规则时，则可以使用 `table-rules` 进行配置。场景如图所示：

![shard-table-sync-2](/media/shard-table-sync-2.png)

sync-diff-inspector 完整的示例配置如下：

```toml
# Diff Configuration.

######################### Global config #########################

# 检查数据的线程数量，上下游数据库的连接数会略大于该值
check-thread-count = 4

# 如果开启，若表存在不一致，则输出用于修复的 SQL 语句
export-fix-sql = true

# 只对比表结构而不对比数据
check-struct-only = false


######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule1"]

[data-sources.mysql2]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule1"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""

########################### Routes ###########################
[routes.rule1]
schema-pattern = "test"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
table-pattern = "table-*"    # 匹配数据源的表名，支持通配符 "*" 和 "?"
target-schema = "test"       # 目标库名
target-table = "table-0"     # 目标表名

######################### Task config #########################
[task]
    output-dir = "./output"

    source-instances = ["mysql1", "mysql2"]

    target-instance = "tidb0"

    # 需要比对的下游数据库的表，每个表需要包含数据库名和表名，两者由 `.` 隔开
    target-check-tables = ["test.table-0"]
```

## 注意事项

如果上游数据库有 `test`.`table-0` 也会被下游数据库匹配到。
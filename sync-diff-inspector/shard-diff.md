---
title: 分库分表场景下的数据校验
aliases: ['/docs-cn/dev/sync-diff-inspector/shard-diff/','/docs-cn/dev/reference/tools/sync-diff-inspector/shard-diff/']
---

# 分库分表场景下的数据校验

sync-diff-inspector 支持对分库分表场景进行数据校验。例如有多个 MySQL 实例，使用同步工具 DM 同步到一个 TiDB 中，用户可以使用 sync-diff-inspector 对上下游数据进行校验。

## 使用 databases config 进行配置

使用 `databases configs` 对 `table-0` 进行特殊配置，设置对应 `rules`，配置上游表与下游表的映射关系。这种配置方式需要对所有分表进行设置，适合上游分表数量较少，且分表的命名规则没有规律的场景。场景如图所示：

![shard-table-sync-1](/media/shard-table-sync-1.png)

sync-diff-inspector 完整的示例配置如下：

```toml
# Diff Configuration.

######################### Global config #########################

log-level = "info"

# how many goroutines are created to check data
check-thread-count = 4

# sampling check percent, for example 10 means only check 10% data
sample-percent = 100

# set true if just want compare data by checksum, will skip select data when checksum is not equal.
use-checksum = false

# set true will continue check from the latest checkpoint
use-checkpoint = true

# ignore check table's data
ignore-data-check = false

# ignore check table's struct
ignore-struct-check = false


######################### Databases config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule1"]
    # remove comment if use tidb's snapshot data
    # snapshot = "2016-10-08 16:45:26"

[data-sources.mysql2]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule2"]
    # remove comment if use tidb's snapshot data
    # snapshot = "2016-10-08 16:45:26"

[data-sources.tidb]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
    # remove comment if use tidb's snapshot data
    # snapshot = "2016-10-08 16:45:26"

[routes.rule1]
schema-pattern = "test"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
table-pattern = "table-[1-2]"          # 匹配数据源的表名，支持通配符 "*" 和 "?"
target-schema = "test"         # 目标库名
target-table = "table-0" # 目标表名

[routes.rule2]
schema-pattern = "test"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
table-pattern = "table-3"          # 匹配数据源的表名，支持通配符 "*" 和 "?"
target-schema = "test"         # 目标库名
target-table = "table-0" # 目标表名

######################### Task config #########################
[task]
    # 1 fix sql: fix-target-TIDB1.sql
    # 2 log: sync-diff.log
    # 3 summary: summary.txt
    # 4 checkpoint: a dir
    output-dir = "./output"

    source-instances = ["mysql1", "mysql2"]

    target-instance = ["tidb"]

    # tables need to check. *Include `schema` and `table`. Use `.` to split*
    target-check-tables = ["test.tabale-0"]
```

当上游分表较多，且所有分表的命名都符合一定的规则时，则可以使用 `table-rules` 进行配置。场景如图所示：

![shard-table-sync-2](/media/shard-table-sync-2.png)

sync-diff-inspector 完整的示例配置如下：

```
# Diff Configuration.

######################### Global config #########################

log-level = "info"

# how many goroutines are created to check data
check-thread-count = 4

# sampling check percent, for example 10 means only check 10% data
sample-percent = 100

# set true if just want compare data by checksum, will skip select data when checksum is not equal.
use-checksum = false

# set true will continue check from the latest checkpoint
use-checkpoint = true

# ignore check table's data
ignore-data-check = false

# ignore check table's struct
ignore-struct-check = false


######################### Databases config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule1"]
    # remove comment if use tidb's snapshot data
    # snapshot = "2016-10-08 16:45:26"

[data-sources.mysql2]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule1"]
    # remove comment if use tidb's snapshot data
    # snapshot = "2016-10-08 16:45:26"

[data-sources.tidb]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
    # remove comment if use tidb's snapshot data
    # snapshot = "2016-10-08 16:45:26"

[routes.rule1]
schema-pattern = "test"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
table-pattern = "table-*"          # 匹配数据源的表名，支持通配符 "*" 和 "?"
target-schema = "test"         # 目标库名
target-table = "table-0" # 目标表名

######################### Task config #########################
[task]
    # 1 fix sql: fix-target-TIDB1.sql
    # 2 log: sync-diff.log
    # 3 summary: summary.txt
    # 4 checkpoint: a dir
    output-dir = "./output"

    source-instances = ["mysql1", "mysql2"]

    target-instance = ["tidb"]

    # tables need to check. *Include `schema` and `table`. Use `.` to split*
    target-check-tables = ["test.table-0"]

```
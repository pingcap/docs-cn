---
title: sync-diff-inspector 用户文档
aliases: ['/docs-cn/dev/sync-diff-inspector/sync-diff-inspector-overview/','/docs-cn/dev/reference/tools/sync-diff-inspector/overview/']
---

# sync-diff-inspector 用户文档

[sync-diff-inspector](https://github.com/pingcap/tidb-tools/tree/master/sync_diff_inspector) 是一个用于校验 MySQL／TiDB 中两份数据是否一致的工具。该工具提供了修复数据的功能（适用于修复少量不一致的数据）。

主要功能：

* 对比表结构和数据
* 如果数据不一致，则生成用于修复数据的 SQL 语句
* 支持[不同库名或表名的数据校验](/sync-diff-inspector/route-diff.md)
* 支持[分库分表场景下的数据校验](/sync-diff-inspector/shard-diff.md)
* 支持 [TiDB 主从集群的数据校验](/sync-diff-inspector/upstream-downstream-diff.md)

可通过以下方式下载 sync-diff-inspector：

+ Binary 包。点击 [tidb-enterprise-tools-nightly-linux-amd64](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.tar.gz) 进行下载。
+ Docker 镜像。执行以下命令进行下载：

    {{< copyable "shell-regular" >}}

    ```shell
    docker pull pingcap/tidb-enterprise-tools
    ```

## sync-diff-inspector 的使用

### 使用限制

* 对于 MySQL 和 TiDB 之间的数据同步不支持在线校验，需要保证上下游校验的表中没有数据写入，或者保证某个范围内的数据不再变更，通过配置 `range` 来校验这个范围内的数据。

* 不支持 JSON、BIT、BINARY、BLOB 等类型的数据，在校验时需要设置 `ignore-columns` 忽略检查这些类型的数据。

* FLOAT、DOUBLE 等浮点数类型在 TiDB 和 MySQL 中的实现方式不同，在计算 checksum 时会分别取6位和15位有效数字。如果不使用该特性，需要设置 `ignore-columns` 忽略这些列的检查。

* 支持对不包含主键或者唯一索引的表进行校验，但是如果数据不一致，生成的用于修复的 SQL 可能无法正确修复数据。

### 数据库权限

sync-diff-inspector 需要获取表结构信息、查询数据，需要的数据库权限如下：

- 上游数据库

    - SELECT（查数据进行对比）

    - SHOW_DATABASES（查看库名）

    - RELOAD（查看表结构）

- 下游数据库

    - SELECT（查数据进行对比）

    - SHOW_DATABASES（查看库名）

    - RELOAD（查看表结构）

### 配置文件说明

sync-diff-inspector 的配置总共分为三个部分：

- Global config: 通用配置，包括日志级别、划分 chunk 的大小、校验的线程数量等。
- Tables config: 配置校验哪些表，如果有的表在上下游有一定的映射关系或者有一些特殊要求，则需要对指定的表进行配置。
- Databases config: 配置上下游数据库实例。

下面是一个完整配置文件的说明：

```toml
# Diff Configuration.

######################### Global config #########################

# 日志级别，可以设置为 info、debug
log-level = "info"

# 检查数据的线程数量，上下游数据库的连接数会略大于该值
check-thread-count = 4

# 抽样检查的比例，如果设置为 100 则检查全部数据
sample-percent = 100

# 通过计算 chunk 的 checksum 来对比数据，如果不开启则逐行对比数据
use-checksum = true

# 是否使用上次校验的 checkpoint，如果开启，则只校验上次未校验以及校验失败的 chunk
use-checkpoint = true

# 不对比数据
ignore-data-check = false

# 不对比表结构
ignore-struct-check = false


######################### Databases config #########################
[data-sources]
[data-sources.mysql1] # mysql1 是该数据库实例唯一标识的id，用于下面task.source-instances/task.target-instance中
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    # 使用 TiDB 的 snapshot 功能，如果开启的话会使用历史数据进行对比
    # snapshot = "2016-10-08 16:45:26"

[data-sources.tidb]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
    # remove comment if use tidb's snapshot data
    # snapshot = "2016-10-08 16:45:26"

# 对部分表进行特殊的配置，配置的表必须包含在 task.target-check-tables 中
[table-configs]
[table-configs.config1] # config1 是该配置的唯一标识id，用于下面task.target-configs中
# 目标数据库名称
schema = "schama1"
# 目标表名称
table = "table"
# 指定检查的数据的范围，需要符合 sql 中 where 条件的语法
range = "age > 10 AND age < 20"
# 指定用于划分 chunk 的列，如果不配置该项，sync-diff-inspector 会选取一个合适的列（主键／唯一键／索引）
index-fields = ""
# 忽略某些列的检查，例如 sync-diff-inspector 目前还不支持的一些类型（json，bit，blob 等），
# 或者是浮点类型数据在 TiDB 和 MySQL 中的表现可能存在差异，可以使用 ignore-columns 忽略检查这些列
ignore-columns = ["",""]
# 指定划分该表的chunk的大小
chunk-size = 0

# 如果需要对比大量的不同库名或者表名的表的数据，或者用于校验上游多个分表与下游总表的数据，可以通过 table-rule 来设置映射关系
# 可以只配置 schema 或者 table 的映射关系，也可以都配置
[routes]
[routes.rule1]
schema-pattern = "test_*"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
table-pattern = "t_*"          # 匹配数据源的表名，支持通配符 "*" 和 "?"
target-schema = "test"         # 目标库名
target-table = "t" # 目标表名

[routes.rule2]
schema-pattern = "test2_*"      # 匹配数据源的库名，支持通配符 "*" 和 "?"
table-pattern = "t2_*"          # 匹配数据源的表名，支持通配符 "*" 和 "?"
target-schema = "test2"         # 目标库名
target-table = "t2" # 目标表名

######################### Task config #########################
# 配置需要对比的*目标数据库*中的表
[task]
    # output-dir 会保存如下信息
    # 1 检查出错误后生成的修复SQL，按chunk划分文件
    # 2 log: sync-diff.log 保存日志信息
    # 3 summary: summary.txt 保存总结
    # 4 checkpoint: a dir 保存断点续传信息
    output-dir = "./output"

    # 上游数据库，内容是data-sources声明的唯一标识id，下同
    source-instances = ["mysql1"]

    # 下游数据库
    target-instance = ["tidb"]

    # 需要比对的下游数据库的表，每个表需要包含数据库名和表名，两者由`.`隔开
    target-check-tables = ["schema*.table*", "!c.*", "test2.t2"]

    # 对部分表的额外配置
    target-configs= ["config1"]
```

### 运行 sync-diff-inspector

执行如下命令：

{{< copyable "shell-regular" >}}

```bash
./bin/sync_diff_inspector --config=./config.toml
```

该命令最终会在`config.toml`中的`output-dir`输出目录输出本次比对的检查报告`summary.txt`和日志`sync_diff.log`。在输出目录下还会生成由`config.toml`文件内容哈希值命名的文件夹，该文件夹下包括断点续传checkpoint结点信息以及数据存在不一致时生成的SQL修复数据。

#### 日志

sync-diff-inspector 的日志存放在`${output}/sync_diff.log`中，其中`${output}`是`config.toml`文件中`output-dir`的值。

#### 校验进度

sync-diff-inspector 会在运行时定期（间隔 10s）输出校验进度到checkpoint中(位于`${output}/${config_hash}/checkpoint/sync_diff_checkpoints.pb`中，其中`${output}`是`config.toml`文件中`output-dir`的值，`${config_hash}`是`config.toml`文件内容的哈希值。)，格式如下：

```checkpoint
{
    "chunk-info":{
        "state":"success",
        "chunk-range":{
            "index":{
                "table-index":0,
                "bucket-index-left":0,
                "bucket-index-right":1,
                "chunk-index":2,
                "chunk-count":200,
            },
            "type":2,
            "bounds":[
                {
                    "column":"id",
                    "lower":"87486",
                    "upper":"93285",
                    "has-lower":true,
                    "has-upper":true,
                },
            ],
            "is-first":false,
            "is-last":false,
            "where":"((((`id` \u003e ?)) AND ((`id` \u003c= ?))) AND TRUE)",
            "args":["87486","93285"],
        },
        "index-id":0,
    },
    "report-info":{
        "Result":"fail",
        "PassNum":0,
        "FailedNum":0,
        "table-results":{
            "sbtest":{
                "sbtest99":{
                    "schma":"sbtest",
                    "table":"sbtest99",
                    "struct-equal":true,
                    "data-equal":true,
                    "meet-error":null,
                    "chunk-result":{
                        "0:0-0:0:200":{
                            "rows-add":0,
                            "rows-delete":0,
                            "rows-count":42317,
                        },
                        "0:0-0:1:200":{
                            "rows-add":0,
                            "rows-delete":0,
                            "rows-count":45169,
                        },
                        "0:0-0:2:200":{
                            "rows-add":0,
                            "rows-delete":0,
                            "rows-count":5799,
                        },
                    },
                },
            },
        },
        "start-time":"0001-01-01T00:00:00Z",
        "time-duration":10030869563,
        "TotalSize":0,
        "SourceConfig":null,
        "TargetConfig":null,
    },
}
```

checkpoint主要分为两块内容：

- chunk-info: 保存chunk的所有信息，chunk按照一定顺序被排列，checkpoint保证文件中的chunk及其之前的所有chunk都已经被比对过。
    
    - state: 保存该chunk比对是否出现error

    - chunk-range: 保存该chunk在表中的范围

        - index: 作为chunk的唯一标识和排序依据。例子表示该chunk位于第一个表`(table-index=0)`，包括了bucketID=0`(bucket-index-left=0)`到bukcetID=1`(bucket-index-right=1)`的范围，这段范围被划分为5个chunks`(chunk-count=2)`，该chunk位于第一个`(chunk-index=200)`。

        - type: 表示该chunk是由哪种方式划分的。type=0表示通过了TiDB的buckets信息来划分。

        - bounds: 表示该chunk的范围，注意bounds是有顺序的，不同bounds的顺序表示不同的范围。

        - where: 由bounds转化的SQL语句的where。

        - args: 按顺序填充where中的`?`。

    - index-id: 如果使用了索引，则该值标志该chunk使用哪一个index

- report-info: 保存chunk的比对的统计结果

    - Result: 比对的结果

    - PassNum:

    - FailNum:

    - table-results: 存放各个表的比对统计结果，例子表示表`hb_test.t_order_shard`表结果比较和数据比较都不对，在chunk`0:0-0:0:5`(由chunk.index唯一标识)共比对了4431行，0行缺失和0行多余。

#### 校验结果

当校验结束时，sync-diff-inspector 会输出一份校验报告，位于`${output}/summary.txt`中，其中`${output}`是`config.toml`文件中`output-dir`的值。

```summary
+---------------------+--------------------+----------------+
|        TABLE        | STRUCTURE EQUALITY | DATA DIFF ROWS |
+---------------------+--------------------+----------------+
| `sbtest`.`sbtest99` | true               | +97/-97        |
| `sbtest`.`sbtest96` | true               | +0/-101        |
+---------------------+--------------------+----------------+
Time Cost: 16.75370462s
Average Speed: 113.277149MB/s
```

- TABLE: 该列表示对应的数据库及表名

- STRUCTURE EQUALITY: 表结构是否相同

- DATA DIFF ROWS: 即rowAdd/rowDelete，表示该表修复需要增加/删除的行数

#### SQL修复

校验过程中遇到不同的行，会生成修复数据的SQL语句。一个chunk如果出现数据不一致，就会生成一个以`chunk.Index`命名的sql文件。文件位于`${output}/${config_hash}/fix-on-${instance}`文件夹下。其中`${instance}`为`config.toml`中`task.target-instance`的值。

一个sql文件会包含该chunk的所属表以及表示的范围信息。对每个修复SQL语句，有三种情况：

- 下游数据库缺失行，则是REPLACE语句
- 下游数据库冗余行，则是DELETE语句
- 下游数据库行部分数据不一致，则是REPLACE语句，但会在sql文件中通过注释的方法标明不同的列

```SQL
-- table: sbtest.sbtest99
-- range in sequence: (3690708) < (id) <= (3720581)
/*
  DIFF COLUMNS ╏   `K`   ╏                `C`                 ╏               `PAD`       
╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
  source data  ╏ 2501808 ╏ 'hello'                            ╏ 'world'                
╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
  target data  ╏ 5003616 ╏ '0709824117-9809973320-4456050422' ╏ '1714066100-7057807621-1425865505'  
╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
*/
REPLACE INTO `sbtest`.`sbtest99`(`id`,`k`,`c`,`pad`) VALUES (3700000,2501808,'hello','world');
```

### 注意事项

* sync-diff-inspector 在校验数据时会消耗一定的服务器资源，需要避免在业务高峰期间校验。
* TiDB 使用的 collation 为 `utf8_bin`。如果对 MySQL 和 TiDB 的数据进行对比，需要注意 MySQL 中表的 collation 设置。如果表的主键／唯一键为 varchar 类型，且 MySQL 中 collation 设置与 TiDB 不同，可能会因为排序问题导致最终校验结果不正确，需要在 sync-diff-inspector 的配置文件中增加 collation 设置。
* sync-diff-inspector 会优先使用 TiDB 的统计信息来划分 chunk，需要尽量保证统计信息精确，可以在**业务空闲期**手动执行 `analyze table {table_name}`。
* table-rule 的规则需要特殊注意，例如设置了 `schema-pattern="test1"`，`target-schema="test2"`，会对比 source 中的 `test1` 库和 target 中的 `test2` 库；如果 source 中有 `test2` 库，该库也会和 target 中的 `test2` 库进行对比。
* 生成的 `fix.sql` 仅作为修复数据的参考，需要确认后再执行这些 SQL 修复数据。

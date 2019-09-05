---
title: Reparo 使用文档
category: reference
aliases: ['/docs-cn/tools/binlog/reparo/']
---

# Reparo 使用文档

Reparo 是 TiDB Binlog 的一个配套工具，用于增量的恢复。使用 TiDB Binlog 中的 Drainer 将 binlog 按照 protobuf 格式输出到文件，通过这种方式来备份增量数据。当需要恢复增量数据时，使用 Reparo 解析文件中的 binlog，并将其应用到 TiDB／MySQL 中。

下载链接：[tidb-binlog-cluster-latest-linux-amd64.tar.gz](http://download.pingcap.org/tidb-binlog-cluster-latest-linux-amd64.tar.gz)

## Reparo 使用

### 命令行参数说明

```
Usage of Reparo:
-L string
    日志输出信息等级设置：debug, info, warn, error, fatal (默认值：info)。
-V 打印版本信息。
-config string
    配置文件路径，如果指定了配置文件，Reparo 会首先读取配置文件的配置；如果对应的配置在命令行参数里面也存在，Reparo 就会使用命令行参数的配置来覆盖配置文件里面的。
-data-dir string
    Drainer 输出的 protobuf 格式 binlog 文件的存储路径 (默认值： data.drainer)。
-dest-type string
    下游服务类型。 取值为 print, mysql（默认值：print）。当值为 print 时，只做解析打印到标准输出，不执行 SQL；如果为 mysql，则需要在配置文件内配置 host、port、user、password 等信息。
-log-file string
    log 文件路径。
-log-rotate string
    log 文件切换频率，取值为 hour、day。
-start-datetime string
    用于指定开始恢复的时间点，格式为 “2006-01-02 15:04:05”。如果不设置该参数则从最早的 binlog 文件开始恢复。
-stop-datetime string
    用于指定结束恢复的时间点，格式同上。如果不设置该参数则恢复到最后一个 binlog 文件。
-safe-mode bool
    指定是否开启安全模式，开启后可支持反复同步。

```

### 配置文件说明

```toml
# Drainer 输出的 protobuf 格式 binlog 文件的存储路径。
data-dir = "./data.drainer"

# 使用索引文件来搜索 ts 的位置，当设置了 `start-ts` 时设置该参数，文件的路径为 {data-dir}/{index-name}。
# index-name = "binlog.index"
# log-file = ""
# log-rotate = "hour"

# 日志输出信息等级设置：debug, info, warn, error, fatal (默认值：info)。
log-level = "info"

# 使用 start-datetime 和 stop-datetime 来选择恢复指定时间范围内的 binlog，格式为 “2006-01-02 15:04:05”。
# start-datetime = ""
# stop-datetime = ""

# start-tso、stop-tso 分别对应 start-datetime 和 stop-datetime，也是用于恢复指定时间范围内的 binlog，用 tso 的值来设置。如果已经设置了 start-datetime 和 stop-datetime，就不需要再设置 start-tso 和 stop-tso。
# start-tso = 0
# stop-tso = 0

# 下游服务类型。 取值为 print, mysql（默认值：print）。当值为 print 时，只做解析打印到标准输出，不执行 SQL；如果为 mysql，则需要在 [dest-db] 中配置 host、port、user、password 等信息。
dest-type = "mysql"

# 安全模式配置。取值为 true 或 false（默认值：false）。当值为 true 时，Reparo 会将 update 语句拆分为 delete + replace 语句。
safe-mode = false

# replicate-do-db 和 replicate-do-table 用于指定恢复的库和表，replicate-do-db 的优先级高于 replicate-do-table。支持使用正则表达式来配置，需要以 '~' 开始声明使用正则表达式。
# 注：replicate-do-db 和 replicate-do-table 使用方式与 Drainer 的使用方式一致。
# replicate-do-db = ["~^b.*","s1"]
# [[replicate-do-table]]
# db-name ="test"
# tbl-name = "log"
# [[replicate-do-table]]
# db-name ="test"
# tbl-name = "~^a.*"

# 如果 dest-type 设置为 mysql, 需要配置 dest-db。
[dest-db]
host = "127.0.0.1"
port = 3309
user = "root"
password = ""
```

### 启动示例

```
./bin/reparo -config reparo.toml
```

> **注意：**
>
> - data-dir 用于指定 Drainer 输出的 binlog 文件目录。
> - start-datatime 和 start-tso 效果一样，只是时间格式上的区别，用于指定开始恢复的时间点；如果不指定，则默认在第一个 binlog 文件开始恢复。
> - stop-datetime 和 stop-tso 效果一样，只是时间格式上的区别，用于指定结束恢复的时间点；如果不指定，则恢复到最后一个 binlog 文件的结尾。
> - dest-type 指定目标类型，取值为 `mysql`、`print`。 当值为 `mysql` 时，可以恢复到 MySQL/TiDB 等使用或兼容 MySQL 协议的数据库，需要在配置下面的 [dest-db] 填写数据库信息；当取值为 `print` 的时候，只是打印 binlog 信息，通常用于 debug，以及查看 binlog 的内容，此时不需要填写 `[dest-db]`。
> - replicate-do-db 用于指定恢复的库，不指定的话，则全部都恢复。
> - replicate-do-table 用于指定要恢复的表，不指定的话，则全部都恢复。

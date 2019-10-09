---
title: Loader 使用文档
category: reference
---

# Loader 使用文档

## Loader 简介

Loader 是由 PingCAP 开发的数据导入工具，用于向 TiDB 中导入数据。

Loader 包含在 tidb-enterprise-tools 安装包中，可[在此下载](/v2.1/reference/tools/download.md)。

## 为什么我们要做这个工具

当数据量比较大的时候，如果用 mysqldump 这样的工具迁移数据会比较慢。我们尝试了 [Mydumper/myloader 套件](https://github.com/maxbube/mydumper)，能够多线程导出和导入数据。在使用过程中，Mydumper 问题不大，但是 myloader 由于缺乏出错重试、断点续传这样的功能，使用起来很不方便。所以我们开发了 loader，能够读取 Mydumper 的输出数据文件，通过 MySQL protocol 向 TiDB/MySQL 中导入数据。

## Loader 有哪些优点

* 多线程导入
* 支持表级别的并发导入，分散写入热点
* 支持对单个大表并发导入，分散写入热点
* 支持 Mydumper 数据格式
* 出错重试
* 断点续导
* 通过 system variable 优化 TiDB 导入数据速度

## 使用方法

### 注意事项

请勿使用 loader 导入 MySQL 实例中 `mysql` 系统数据库到下游 TiDB。

如果 Mydumper 使用 -m 参数，会导出不带表结构的数据，这时 loader 无法导入数据。

如果使用默认的 `checkpoint-schema` 参数，在导完一个 database 数据库后，请 `drop database tidb_loader` 后再开始导入下一个 database。

推荐数据库开始导入的时候，明确指定 `checkpoint-schema = "tidb_loader"` 参数。

### 参数说明

```
  -L string
      log 级别设置，可以设置为 debug, info, warn, error, fatal (默认为 "info")
  -P int
      TiDB/MySQL 的端口 (默认为 4000)
  -V
      打印 loader 版本
  -c string
      指定配置文件启动 loader
  -checkpoint-schema string
      checkpoint 数据库名，loader 在运行过程中会不断的更新这个数据库，在中断并恢复后，会通过这个库获取上次运行的进度 (默认为 "tidb_loader")
  -d string
       需要导入的数据存放路径 (default "./")
  -h string
       TiDB 服务 host IP  (default "127.0.0.1")
  -p string
      TiDB 账户密码
  -status-addr string
      Prometheus 可以通过该地址拉取 Loader metrics, 也是 Loader 的 pprof 调试地址 (默认为 ":8272")。
  -t int
      线程数 (默认为 16). 每个线程同一时刻只能操作一个数据文件。
  -u string
      TiDB 的用户名 (默认为 "root")
```

### 配置文件

除了使用命令行参数外，还可以使用配置文件来配置，配置文件的格式如下：

```toml
# 日志输出等级；可以设置为 debug, info, warn, error, fatal (默认为 "info")
log-level = "info"

# 指定 loader 日志目录
log-file = "loader.log"

# 需要导入的数据存放路径 (default "./")
dir = "./"

## Prometheus 可以通过该地址拉取 Loader metrics, 也是 Loader 的 pprof 调试地址 (默认为 ":8272")。
status-addr = ":8272"

# checkpoint 数据库名，loader 在运行过程中会不断的更新这个数据库，在中断并恢复后，
# 会通过这个库获取上次运行的进度 (默认为 "tidb_loader")
checkpoint-schema = "tidb_loader"

# 线程数 (默认为 16). 每个线程同一时刻只能操作一个数据文件。
pool-size = 16

# 目标数据库信息
[db]
host = "127.0.0.1"
user = "root"
password = ""
port = 4000

# 导入数据时数据库连接所使用的 session 级别的 `sql_mode`。如果 `sql-mode` 的值没有提供或者设置为 "@DownstreamDefault"，会使用下游 global 级别的 `sql_mode`。
# sql-mode = ""
# `max-allowed-packet` 设置数据库连接允许的最大数据包大小，对应于系统参数中的 `max_allowed_packet`。 如果设置为 0，会使用下游数据库 global 级别的 `max_allowed_packet`。
max-allowed-packet = 67108864

# sharding 同步规则，采用 wildcharacter
# 1\. 星号字符 (*) 可以匹配零个或者多个字符,
#    例子, doc* 匹配 doc 和 document, 但是和 dodo 不匹配;
#    星号只能放在 pattern 结尾，并且一个 pattern 中只能有一个
# 2\. 问号字符 (?) 匹配任一一个字符

# [[route-rules]]
# pattern-schema = "shard_db_*"
# pattern-table = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

### 使用示例

通过命令行参数：

```bash
./bin/loader -d ./test -h 127.0.0.1 -u root -P 4000
```

或者使用配置文件 "config.toml":

```bash
./bin/loader -c=config.toml
```

## FAQ

### 合库合表场景案例说明

根据配置文件的 route-rules 可以支持将分库分表的数据导入到同一个库同一个表中，但是在开始前需要检查分库分表规则：

+ 是否可以利用 route-rules 的语义规则表示
+ 分表中是否包含唯一递增主键，或者合并后是否包含数据上有冲突的唯一索引或者主键

Loader 需要配置文件中开启 route-rules 参数以提供合库合表功能

+ 如果使用该功能，必须填写 `pattern-schema` 与 `target-schema`
+ 如果 `pattern-table` 与 `target-table` 为空，将不进行表名称合并或转换

```toml
[[route-rules]]
pattern-schema = "example_db"
pattern-table = "table_*"
target-schema = "example_db"
target-table = "table"
```

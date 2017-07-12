---
title: Loader 使用文档
category: advanced
---

# Loader 使用文档

## Loader 是什么

是由 PingCAP 开发的数据导入工具，可以用于向 TiDB 中导入数据，也可以用于向 MySQL 中导入数据。

[Binary 下载](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz)

## 为什么我们要做这个东西

当数据量比较大的时候，如果用 mysqldump 这样的工具迁移数据会比较慢。我们尝试了 Percona 的 mydumper/myloader 套件，能够多线程导出和导入数据。在使用过程中，mydumper 问题不大，但是 myloader 由于缺乏出错重试、断点续传这样的功能，使用起来很不方便。所以我们开发了 loader，能够读取 mydumper 的输出数据文件，通过 mysql protocol 向 TiDB/MySQL 中导入数据。

## Loader 有哪些优点

* 多线程导入

* 支持表级别的并发导入，分散写入热点

* 支持对单个大表并发导入，分散写入热点

* 支持 mydumper 数据格式

* 出错重试

* 断点续导

* 通过 system variable 优化 TiDB 导入数据速度

## 使用方法

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
      Directory of the dump to import (default "./")
  -h string
      The host to connect to (default "127.0.0.1")
  -p string
      TiDB/MySQL 账户密码
  -pprof-addr string
      Loader 的 pprof 地址，用于对 Loader 进行性能调试 (默认为 ":10084")
  -skip-unique-check 
      是否跳过 unique index 检查，0 表示不跳过，1 表示跳过（能够提高导入数据的速度），注意只有在向 TiDB 中导入数据时，才需要打开这个选项 (默认为1)
  -t int
      单个线程池的线程数 (默认为 4)，一个线程池同一时刻只能对一个表进行导入
  -u string
      TiDB/MySQL 的用户名 (默认为 "root")
```

### 配置文件

除了使用命令行参数外，还可以使用配置文件来配置，配置文件的格式如下：

```toml
# Loader log level
log-level = "info"

# Loader log file
log-file = ""

# Directory of the dump to import
dir = "./"

# Loader pprof addr
pprof-addr = ":10084"

# We saved checkpoint data to tidb, which schema name is defined here.
checkpoint-schema = "tidb_loader"

# Number of threads restoring concurrently for worker pool. Each worker restore one file at a time, increase this as TiKV nodes increase
pool-size = 16

# Skip unique index check
skip-unique-check = 0

# An alternative database to restore into
#alternative-db = ""
# Database to restore
#source-db = ""

# DB config
[db]
host = "127.0.0.1"
user = "root"
password = ""
port = 4000

# [[route-rules]]
# pattern-schema = "shard_db_*"
# pattern-table = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

### 使用示例

通过命令行参数：

    ./bin/loader -d ./test -h 127.0.0.1 -u root -P 4000

或者使用配置文件 "config.toml":

    ./bin/loader -c=config.toml

### 注意事项

如果使用默认的 `checkpoint-schema` 参数，在导完一个 database 数据库后，请 `drop database tidb_loader` 后再开始导入下一个 database。  
推荐数据库开始导入的时候，明确指定`checkpoint-schema = "tidb_loader"`参数。



---
title: Loader 使用文档
category: advanced
---

# Loader 使用文档

## Loader 是什么

是由 PingCAP 开发的数据导入工具，可以用于向 TiDB 中导入数据，也可以用于向 MySQL 中导入数据。

[Binary 下载](http://download.pingcap.org/tidb-tools-latest-linux-amd64.tar.gz)

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
  -d string
        需要导入的数据存放路径 (默认为 "./")
  -h string
        TiDB/MySQL 的 host (默认为 "127.0.0.1")
  -checkpoint string
        checkpoint 文件位置，loader 在运行过程中会不断的更新这个文件，在中断并恢复后，会通过这个文件获取上次运行的进度 (默认为 "loader.checkpoint")
  -skip-unique-check
       是否跳过 unique index 检查，0 表示不跳过，1 表示跳过（能够提高导入数据的速度），注意只有在向 TiDB 中导入数据时，才需要打开这个选项 (默认为1)
  -p string
        TiDB/MySQL 账户密码
  -pprof-addr string
        Loader 的 pprof 地址，用于对 Loader 进行性能调试 (默认为 ":10084")
  -t int
        单个线程池的线程数 (默认为 4)，一个线程池同一时刻只能对一个表进行导入
  -pc int
        线程池的个数（默认值 8），启动多个线程池可以支持表级别的并发，分散写入的热点问题，能够充分利用整个集群的所有 TiKV 节点的资源，提升导入数据的速度
  -file-num-per-block int
        一个逻辑块包含的数据文件个数（默认值 64），如果导入的是一个比较大的表（例如 100GB），Loader 支持将该表分成多个逻辑块，然后将不同逻辑块分给不同的线程池进行并发导入，分散写入热点，充分利用整个集群的所有 TiKV 节点的资源，提升导入数据的速度。
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

# Loader saved checkpoint
checkpoint = "loader.checkpoint"

# Loader pprof addr
pprof-addr = ":10084"

# Number of threads for each pool
pool-size = 4

# Number of pools
pool-count = 8

# Skip unique index check 注意如果不是向 TiDB 中导入数据，请将这个设为 0
skip-unique-check = 1

# DB config
[db]
host = "127.0.0.1"
user = "root"
password = ""
port = 4000
```

### 使用示例

通过命令行参数：

    ./bin/loader -d ./test -h 127.0.0.1 -u root -P 4000

或者使用配置文件 "config.toml":

    ./bin/loader -c=config.toml

### 注意事项

如果使用默认的 checkpoint 文件，在导完一个 database 数据后，请删除 loader.checkpoint 后再开始导入下一个 database。推荐每个数据库导入的时候，明确指定 checkpoint 文件名。



---
title: 备份恢复
category: advanced
---

# 备份恢复

## 概述


该文档详细介绍了如何对 TiDB 进行备份恢复。本文档暂时只考虑全量备份与恢复。

这里我们假定 TiDB 服务信息如下：

|Name|Address|Port|User|Password|
|----|-------|----|----|--------|
|TiDB|127.0.0.1|4000|root|*|


在这个备份恢复过程中，我们会用到下面的工具:

- mydumper 从 MySQL 导出数据
- loader 导入数据到 TiDB
- pump 用户生成binlog文件
- drainer 用于增量导入到新 TIDB

### 两种迁移场景

- 第一种场景：只全量导入历史数据 （需要 mydumper + loader）；
- 第二种场景：全量导入历史数据后，通过增量的方式同步新的数据 （需要 pump + drainer + mydumper + loader ） 。该场景需要提前部署PUMP服务，并用 drainer 获取 `TS & binlog` 信息后，再做数据导出。根据源库数据量大小需要调整 pump gc 参数。


### 下载 TiDB 工具集 (Linux)

```bash
# 下载 tool 压缩包
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256
# 解开压缩包
tar -xzf tidb-enterprise-tools-latest-linux-amd64.tar.gz
cd tidb-enterprise-tools-latest-linux-amd64
```


## 使用 `mydumper`/`loader` 全量导入数据

`mydumper` 是一个强大的数据迁移工具，具体可以参考 [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper)。

我们使用 `mydumper` 从 TiDB 导出数据进行备份，然后用 `loader` 将其导入到 TiDB 里面进行恢复。

> 注意：虽然 TiDB 也支持使用 MySQL 官方的 `mysqldump` 工具来进行数据的备份恢复工作，但相比于 `mydumper` / `loader`，性能会慢很多，大量数据的备份恢复会花费很多时间，这里我们并不推荐。

### `mydumper`/`loader` 全量备份恢复最佳实践
为了快速的备份恢复数据 (特别是数据量巨大的库), 可以参考下面建议

* 使用 mydumper 导出来的数据文件尽可能的小, 最好不要超过 64M, 可以设置参数 -F 64 
* loader的 -t 参数可以根据 tikv 的实例个数以及负载进行评估调整，例如 3个 tikv 的场景， 此值可以设为 3 *（1 ～ n)；当 tikv 负载过高，loader 以及 tidb 日志中出现大量 `backoffer.maxSleep 15000ms is exceeded` 可以适当调小该值，当 tikv 负载不是太高的时候，可以适当调大该值。

#### 某次导入示例，以及相关的配置
 - mydumper 导出后总数据量 214G，单表 8 列，20 亿行数据
 - 集群拓扑
     - TIKV * 12
     - TIDB * 4 
     - PD * 3
 - mydumper -F 设置为 16, loader -t 参数 64
 
结果：导入时间 11 小时左右，19.4 G/小时

### 从 TiDB 备份数据

我们使用 `mydumper` 从 TiDB 备份数据，如下:

```bash
./bin/mydumper -h 127.0.0.1 -P 4000 -u root -t 16 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```

上面，我们使用 `-B test` 表明是对 `test` 这个 database 操作，然后用 `-T t1,t2` 表明只导出 `t1`，`t2` 两张表。

`-t 16` 表明使用 16 个线程去导出数据。`-F 64` 是将实际的 table 切分成多大的 chunk，这里就是 64MB 一个 chunk。

`--skip-tz-utc` 添加这个参数忽略掉 TiDB 与导数据的机器之间时区设置不一致的情况，禁止自动转换。



### 向 TiDB 恢复数据

我们使用 `loader` 将之前导出的数据导入到 TiDB，完成恢复操作。Loader 的下载和具体的使用方法见 [Loader 使用文档](../tools/loader.md)

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 32 -d ./var/test
```

导入成功之后，我们可以用 MySQL 官方客户端进入 TiDB，查看:

```sql
mysql -h127.0.0.1 -P4000 -uroot

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| t2             |
+----------------+

mysql> select * from t1;
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
+----+------+

mysql> select * from t2;
+----+------+
| id | name |
+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
+----+------+
```


## 使用 `mydumper`/`loader`/`drainer` 增量导入数据


### 下载 TiDB  (Linux)

```bash
# 下载 tool 压缩包
wget http://download.pingcap.org/tidb-binlog-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-binlog-latest-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-binlog-latest-linux-amd64.sha256
# 解开压缩包
tar -xzf tidb-binlog-latest-linux-amd64.tar.gz
cd tidb-binlog-latest-linux-amd64
```

### 数据导出前检查

- 检查 tidb 数据量大小
	- grafana PD 面板 `Current Storage Size` ，集群如果是 3 副本，需要用这个值除 3 。
	- 副本数通过 pd-ctl 查看

- 检查 pump 服务 gc 参数，默认为 7 天。
	- ansible 部署的 tidb 集群，已设置为 3 天。

- 全量导出数据前，先使用以下命令获取 `TS & binlog` 信息
    - ./drainer -pd-urls="http://127.0.0.1:2379" -gen-savepoint -d ./config
		- `-pd-urls` 为源库 tidb 集群 pd 地址
		- `-d` 指定存放savepoint目录，目录必须为空
		- `-gen-savepoint` 获取 savepoint 文件,记录了当前 tso 与 pump file 时间

### 全量导出 导入

> 参考第一种场景即可


### 增量同步

#### 配置 drainer 服务

配置文件

```toml
# drainer Configuration.

# drainer 提供服务的地址(默认 "127.0.0.1:8249",线上同步时需要修改为本机 IP:prot )
addr = "127.0.0.1:8249"

# 向 pd 查询在线 pump 的时间间隔 (默认 10，单位 秒)
detect-interval = 10

# drainer 数据存储位置路径 (默认 "data.drainer")
data-dir = "data.drainer"

# pd 集群节点的地址 (默认 "http://127.0.0.1:2379",线上同步时请正确配置 PD 地址)
pd-urls = "http://127.0.0.1:2379"

# syncer Configuration.
[syncer]

# db 过滤列表 (默认 "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test"),   
# 不支持对 ignore schemas 的 table 进行 rename DDL 操作
ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"

# 输出到下游数据库一个事务的 sql 数量 (default 1)
txn-batch = 1

# 同步下游的并发数，该值设置越高同步的吞吐性能越好 (default 1)
worker-count = 1

disable-dispatch = true

# drainer 下游服务类型 (默认为 mysql)
# valid values are "mysql", "pb"
db-type = "mysql"

##replicate-do-db priority over replicate-do-table if have same db name
##and we support regex expression , start with '~' declare use regex expression.

#replicate-do-db = ["~^b.*","s1"]
#[[replicate-do-table]]
#db-name ="test"
#tbl-name = "log"

#[[replicate-do-table]]
#db-name ="test"
#tbl-name = "~^a.*"

# the downstream mysql protocol database
[syncer.to]
host = "127.0.0.1"
user = "root"
password = ""
port = 3306

# uncomment this if you want to use pb as db-type
# [syncer.to]
# dir = "data.drainer"
 ```   

#### 启动 drainer 服务


```bash
./bin/drainer -config drainer.toml
```

#### 监测数据同步

- 在 grafana 导入 drainer.json 监控面板
- 观察 `synchronization delay` metrics 

---
title: 数据迁移
category: advanced
---

# 数据迁移

## 概述

该文档详细介绍了如何将 MySQL 的数据迁移到 TiDB。

这里我们假定 MySQL 以及 TiDB 服务信息如下：

|Name|Address|Port|User|Password|
|----|-------|----|----|--------|
|MySQL|127.0.0.1|3306|root|*|
|TiDB|127.0.0.1|4000|root|*|

在这个数据迁移过程中，我们会用到下面四个工具:

- checker 检查 schema 能否被 TiDB 兼容
- mydumper 从 MySQL 导出数据
- loader 导入数据到 TiDB
- syncer 增量同步 MySQL 数据到 TiDB

## 两种迁移场景

- 第一种场景：只全量导入历史数据 （需要 checker + mydumper + loader）；
- 第二种场景：全量导入历史数据后，通过增量的方式同步新的数据 （需要 checker + mydumper + loader + syncer）。该场景需要提前开启 binlog 且格式必须为 ROW。


## MySQL 开启 binlog

**注意： 只有上文提到的第二种场景才需要在 dump 数据之前先开启 binlog**

+   MySQL 开启 binlog 功能，参考 [Setting the Replication Master Configuration](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html)
+   Binlog 格式必须使用 `ROW` format，这也是 MySQL 5.7 之后推荐的 binlog 格式，可以使用如下语句打开:

    ```sql
    SET GLOBAL binlog_format = ROW;
    ```


## 使用 checker 进行 Schema 检查

在迁移之前，我们可以使用 TiDB 的 checker 工具，来预先检查 TiDB 是否能支持需要迁移的 table schema。如果 check 某个 table schema 失败，表明 TiDB 当前并不支持，我们不能对该 table 里面的数据进行迁移。checker 包含在 TiDB 工具集里面，我们可以直接下载。

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

### 使用 checker 检查的一个示范

+   在 MySQL 的 test database 里面创建几张表，并插入数据:

    ```sql
    USE test;
    CREATE TABLE t1 (id INT, age INT, PRIMARY KEY(id)) ENGINE=InnoDB;
    CREATE TABLE t2 (id INT, name VARCHAR(256), PRIMARY KEY(id)) ENGINE=InnoDB;

    INSERT INTO t1 VALUES (1, 1), (2, 2), (3, 3);
    INSERT INTO t2 VALUES (1, "a"), (2, "b"), (3, "c");
    ```

+   使用 checker 检查 test database 里面所有的 table

    ```bash
    ./bin/checker -host 127.0.0.1 -port 3306 -user root test
    2016/10/27 13:11:49 checker.go:48: [info] Checking database test
    2016/10/27 13:11:49 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
    2016/10/27 13:11:49 checker.go:63: [info] Checking table t1
    2016/10/27 13:11:49 checker.go:69: [info] Check table t1 succ
    2016/10/27 13:11:49 checker.go:63: [info] Checking table t2
    2016/10/27 13:11:49 checker.go:69: [info] Check table t2 succ
    ```

+   使用 checker 检查 test database 里面某一个 table

    这里，假设我们只需要迁移 table `t1`。

    ```bash
    ./bin/checker -host 127.0.0.1 -port 3306 -user root test t1
    2016/10/27 13:13:56 checker.go:48: [info] Checking database test
    2016/10/27 13:13:56 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
    2016/10/27 13:13:56 checker.go:63: [info] Checking table t1
    2016/10/27 13:13:56 checker.go:69: [info] Check table t1 succ
    Check database succ!
    ```

### 一个无法迁移的 table 例子

我们在 MySQL 里面创建如下表：

```sql
CREATE TABLE t_error (
  c timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

使用 `checker` 进行检查，会报错，表明我们没法迁移 `t_error` 这张表。

```bash
./bin/checker -host 127.0.0.1 -port 3306 -user root test t_error
2016/10/27 13:19:28 checker.go:48: [info] Checking database test
2016/10/27 13:19:28 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
2016/10/27 13:19:28 checker.go:63: [info] Checking table t_error
2016/10/27 13:19:28 checker.go:67: [error]
Check table t_error failed with err: line 1 column 56 near ") ON UPDATE CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=latin1"
github.com/pingcap/tidb/parser/yy_parser.go:111:
github.com/pingcap/tidb/parser/yy_parser.go:124:
/home/jenkins/workspace/WORKFLOW_TOOLS_BUILDING/go/src/ \
github.com/pingcap/tidb-tools/checker/checker.go:122:  parse CREATE TABLE `t_error` (
  `c` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 error
/home/jenkins/workspace/WORKFLOW_TOOLS_BUILDING/go/src/ \
github.com/pingcap/tidb-tools/checker/checker.go:114:
2016/10/27 13:19:28 main.go:68: [error] Check database test with 1 errors and 0 warnings.
```

## 使用 `mydumper`/`loader` 全量导入数据

`mydumper` 是一个更强大的数据迁移工具，具体可以参考 [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper)。

我们使用 `mydumper` 从 MySQL 导出数据，然后用 `loader` 将其导入到 TiDB 里面。

> 注意：虽然 TiDB 也支持使用 MySQL 官方的 `mysqldump` 工具来进行数据的迁移工作，但相比于 `mydumper` / `loader`，性能会慢很多，大量数据的迁移会花费很多时间，这里我们并不推荐。

### `mydumper`/`loader` 全量导入数据最佳实践
为了快速的迁移数据 (特别是数据量巨大的库), 可以参考下面建议

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

### 从 MySQL 导出数据

我们使用 `mydumper` 从 MySQL 导出数据，如下:

```bash
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```

上面，我们使用 `-B test` 表明是对 `test` 这个 database 操作，然后用 `-T t1,t2` 表明只导出 `t1`，`t2` 两张表。

`-t 16` 表明使用 16 个线程去导出数据。`-F 64` 是将实际的 table 切分成多大的 chunk，这里就是 64MB 一个 chunk。

`--skip-tz-utc` 添加这个参数忽略掉 MySQL 与导数据的机器之间时区设置不一致的情况，禁止自动转换。

> 注意：在阿里云等一些需要 `super privilege` 的云上面，`mydumper` 需要加上 `--no-locks` 参数，否则会提示没有权限操作。

### 向 TiDB 导入数据

我们使用 `loader` 将之前导出的数据导入到 TiDB。Loader 的下载和具体的使用方法见 [Loader 使用文档](../tools/loader.md)

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

## 使用 `syncer` 增量导入数据

上面我们介绍了如何使用 `mydumper`/`loader` 将 MySQL 的数据全量导入到 TiDB，但如果后续 MySQL 的数据有更新，我们仍然希望快速导入，使用全量的方式就不合适了。

TiDB 提供 `syncer` 工具能方便的将 MySQL 的数据增量的导入到 TiDB 里面。

`syncer` 属于 TiDB 企业版工具集，如何获取可以参考 [下载 TiDB 企业版工具集](#下载-tidb-企业版工具集-linux)。

### 下载 TiDB 企业版工具集 (Linux)

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

假设我们之前已经使用 `mydumper`/`loader` 导入了 `t1` 和 `t2` 两张表的一些数据，现在我们希望这两张表的任何更新，都是实时的同步到 TiDB 上面。

### 获取同步 position

如上文所提，mydumper 导出的数据目录里面有一个 `metadata` 文件，里面就包含了我们所需的 position 信息。

medadata 文件信息内容举例：

```
Started dump at: 2017-04-28 10:48:10
SHOW MASTER STATUS:
	Log: mysql-bin.000003
	Pos: 930143241
	GTID:

Finished dump at: 2017-04-28 10:48:11
```

我们将 position 相关的信息保存到一个 `syncer.meta` 文件里面，用于 `syncer` 的同步:

```bash
# cat syncer.meta
binlog-name = "mysql-bin.000003"
binlog-pos = 930143241
```

注意：`syncer.meta` 只需要第一次使用的时候配置，后续 `syncer` 同步新的 binlog 之后会自动将其更新到最新的 position。

### 启动 `syncer`

`syncer` 的配置文件 `config.toml`:

```toml
log-level = "info"

server-id = 101

# meta 文件地址
meta = "./syncer.meta"
worker-count = 1
batch = 1

# pprof 调试地址, Prometheus 也可以通过该地址拉取 syncer metrics
status-addr = ":10081"

skip-sqls = ["ALTER USER", "CREATE USER"]

# 支持白名单过滤, 指定只同步的某些库和某些表, 例如:

# 指定同步 db1 和 db2 下的所有表
replicate-do-db = ["db1","db2"]

# 指定同步 db1.table1
[[replicate-do-table]]
db-name ="db1"
tbl-name = "table1"

# 指定同步 db3.table2
[[replicate-do-table]]
db-name ="db3"
tbl-name = "table2"
# 支持正则，以~开头表示使用正则
# 同步所有以 test 开头的库
replicate-do-db = ["~^test.*"]

# sharding 同步规则，采用 wildcharacter
# 1. 星号字符 (*) 可以匹配零个或者多个字符,
#    例子, doc* 匹配 doc 和 document, 但是和 dodo 不匹配;
#    星号只能放在 pattern 结尾，并且一个 pattern 中只能有一个
# 2. 问号字符 (?) 匹配任一一个字符
[[route-rules]]
pattern-schema = "route_*"
pattern-table = "abc_*"
target-schema = "route"
target-table = "abc"

[[route-rules]]
pattern-schema = "route_*"
pattern-table = "xyz_*"
target-schema = "route"
target-table = "xyz"

[from]
host = "127.0.0.1"
user = "root"
password = ""
port = 3306

[to]
host = "127.0.0.1"
user = "root"
password = ""
port = 4000
```

启动 `syncer`:

```bash
./bin/syncer -config config.toml
2016/10/27 15:22:01 binlogsyncer.go:226: [info] begin to sync binlog from position (mysql-bin.000003, 1280)
2016/10/27 15:22:01 binlogsyncer.go:130: [info] register slave for master server 127.0.0.1:3306
2016/10/27 15:22:01 binlogsyncer.go:552: [info] rotate to (mysql-bin.000003, 1280)
2016/10/27 15:22:01 syncer.go:549: [info] rotate binlog to (mysql-bin.000003, 1280)
```

### 在 MySQL 插入新的数据

```sql
INSERT INTO t1 VALUES (4, 4), (5, 5);
```

登录到 TiDB 查看：

```sql
mysql -h127.0.0.1 -P4000 -uroot -p
mysql> select * from t1;
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
|  4 |    4 |
|  5 |    5 |
+----+------+
```

`syncer` 每隔 30s 会输出当前的同步统计，如下


```bash
2017/06/08 01:18:51 syncer.go:934: [info] [syncer]total events = 15, total tps = 130, recent tps = 4,
master-binlog = (ON.000001, 11992), master-binlog-gtid=53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-74,
syncer-binlog = (ON.000001, 2504), syncer-binlog-gtid = 53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-17
2017/06/08 01:19:21 syncer.go:934: [info] [syncer]total events = 15, total tps = 191, recent tps = 2,
master-binlog = (ON.000001, 11992), master-binlog-gtid=53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-74,
syncer-binlog = (ON.000001, 2504), syncer-binlog-gtid = 53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-35
```

可以看到，使用 `syncer`，我们就能自动的将 MySQL 的更新同步到 TiDB。





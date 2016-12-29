# 数据迁移

## 概述

该文档详细介绍了如何将 MySQL 的数据迁移到 TiDB。

这里我们假定 MySQL 以及 TiDB 服务信息如下:

|Name|Address|Port|User|Password|
|----|-------|----|----|--------|
|MySQL|127.0.0.1|3306|root||
|TiDB|127.0.0.1|4000|root||

## 使用 checker 进行 Schema 检查

在迁移之前，我们可以使用 TiDB 的 `checker` 工具，来预先检查 TiDB 是否能支持需要迁移的 table schema。如果 check 某个 table schema 失败，表明 TiDB 当前并不支持，我们不能对该 table 里面的数据进行迁移。`checker` 包含在 TiDB 工具集里面，我们可以直接下载。

### 下载 TiDB 工具集

#### Linux

```bash
# 下载 tool 压缩包
wget http://download.pingcap.org/tidb-tools-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-tools-latest-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-tools-latest-linux-amd64.sha256
# 解开压缩包
tar -xzf tidb-tools-latest-linux-amd64.tar.gz
cd tidb-tools-latest-linux-amd64
```

### 使用 `checker` 检查的一个示范

+ 在 MySQL 的 test database 里面创建几张表，并插入数据:

```bash
USE test;
CREATE TABLE t1 (id INT, age INT, PRIMARY KEY(id)) ENGINE=InnoDB;
CREATE TABLE t2 (id INT, name VARCHAR(256), PRIMARY KEY(id)) ENGINE=InnoDB;

INSERT INTO t1 VALUES (1, 1), (2, 2), (3, 3);
INSERT INTO t2 VALUES (1, "a"), (2, "b"), (3, "c");
```

+ 使用 `checker` 检查 test database 里面所有的 table

```bash
./bin/checker -host 127.0.0.1 -port 3306 -user root test
2016/10/27 13:11:49 checker.go:48: [info] Checking database test
2016/10/27 13:11:49 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
2016/10/27 13:11:49 checker.go:63: [info] Checking table t1
2016/10/27 13:11:49 checker.go:69: [info] Check table t1 succ
2016/10/27 13:11:49 checker.go:63: [info] Checking table t2
2016/10/27 13:11:49 checker.go:69: [info] Check table t2 succ
```

+ 使用 `checker` 检查 test database 里面某一个 table

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
2016/10/27 13:19:28 checker.go:67: [error] Check table t_error failed with err: line 1 column 56 near ") ON UPDATE CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=latin1"
github.com/pingcap/tidb/parser/yy_parser.go:111:
github.com/pingcap/tidb/parser/yy_parser.go:124:
/home/jenkins/workspace/WORKFLOW_TOOLS_BUILDING/go/src/github.com/pingcap/tidb-tools/checker/checker.go:122:  parse CREATE TABLE `t_error` (
  `c` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 error
/home/jenkins/workspace/WORKFLOW_TOOLS_BUILDING/go/src/github.com/pingcap/tidb-tools/checker/checker.go:114:
2016/10/27 13:19:28 main.go:68: [error] Check database test with 1 errors and 0 warnings.
```

## 使用 `mydumper`/`loader` 全量导入数据

我们使用 `mydumper` 从 MySQL 导出数据，然后用 `loader` 将其导入到 TiDB 里面。

**注意，虽然我们也支持使用 MySQL 官方的  `mysqldump` 工具来进行数据的迁移工作，但相比于 `mydumper`/`loader`，性能会慢很多，对于大量数据的迁移会花费很多时间，这里我们并不推荐。**

### 从 MySQL 导出数据
`mydumper` 是一个更强大的数据迁移工具，具体可以参考 [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper)。

#### 下载 Binary

##### Linux

```bash
# 下载 mydumper 压缩包
wget http://download.pingcap.org/mydumper-linux-amd64.tar.gz
wget http://download.pingcap.org/mydumper-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c mydumper-linux-amd64.sha256
# 解开压缩包
tar -xzf mydumper-linux-amd64.tar.gz
cd mydumper-linux-amd64
```

#### 从 MySQL 导出数据

我们使用 `mydumper` 从 MySQL 导出数据，如下:

```bash
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 128 -B test -T t1,t2 -o ./var/test
```

上面，我们使用 `-B test` 表明是对 `test` 这个 database 操作，然后用 `-T t1,t2` 表明只导出 `t1`，`t2` 两张表。

`-t 16` 表明使用 16 个线程去导出数据。`-F 128` 是将实际的 table 切分成多大的 chunk，这里就是 128MB 一个 chunk。

**注意：在阿里云一些需要 `super privilege` 的云上面，`mydumper` 需要加上 `--no-locks` 参数，否则会提示没有权限操作。**

### 向 TiDB 导入数据

我们使用 `loader` 将之前导出的数据导入到 TiDB。Loader 的下载和具体的使用方法见 [Loader 使用文档](../tools/loader.md)

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 4 -q 1 -d ./var/test
```

这里 `-q 1` 表明每个事务包含多少个 query，默认是 1，在像 TiDB 中导入数据时，推荐用默认值。

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

上面我们介绍了如何使用 `mydumper`/`myloader` 将 MySQL 的数据全量导入到 TiDB，但如果后续 MySQL 的数据有更新，我们仍然希望快速导入，使用全量的方式就不合适了。

TiDB 提供 `syncer` 工具能方便的将 MySQL 的数据增量的导入到 TiDB 里面。

`syncer` 也属于 TiDB 工具集，如何获取可以参考 [下载 TiDB 工具集](#下载-tidb-工具集)。

假设我们之前已经使用 `mydumper`/`myloader` 导入了 `t1` 和 `t2` 两张表的一些数据，现在我们希望这两张表的任何更新，都是实时的同步到 TiDB 上面。

### MySQL 开启 binlog

在使用 `syncer` 之前，我们必须保证：

+ MySQL 开启 binlog 功能，参考 [Setting the Replication Master Configuration](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html)
+ Binlog 格式必须使用 `row` format，这也是 MySQL 5.7 之后推荐的 binlog 格式，可以使用如下语句打开:

```sql
SET GLOBAL binlog_format = ROW;
```

### 获取同步 position

我们通过 `show master status` 得到当前 binlog 的 position，`syncer` 的初始同步位置就是从这个地方开始。

```sql
show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000003 |     1280 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
```

我们将 position 相关的信息保存到一个 `syncer.meta` 文件里面，用于 `syncer` 的同步:

```bash
# cat syncer.meta
binlog-name = "mysql-bin.000003"
binlog-pos = 1280
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

pprof-addr = ":10081"

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

```bash
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
2016/10/27 15:22:31 syncer.go:668: [info] [syncer]total events = 1, insert = 1, update = 0, delete = 0, total tps = 0, recent tps = 0, binlog name = mysql-bin.000003, binlog pos = 1280.
2016/10/27 15:23:01 syncer.go:668: [info] [syncer]total events = 2, insert = 2, update = 0, delete = 0, total tps = 0, recent tps = 0, binlog name = mysql-bin.000003, binlog pos = 1538.
```

可以看到，使用 `syncer`，我们就能自动的将 MySQL 的更新同步到 TiDB。





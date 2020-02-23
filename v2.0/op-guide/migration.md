---
title: 数据迁移
category: advanced
---

# 数据迁移

## 使用 `mydumper`/`loader` 全量导入数据

`mydumper` 是一个更强大的数据迁移工具，具体可以参考 [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper)。

我们使用 `mydumper` 从 MySQL 导出数据，然后用 `loader` 将其导入到 TiDB 里面。

> 注意：虽然 TiDB 也支持使用 MySQL 官方的 `mysqldump` 工具来进行数据的迁移工作，但相比于 `mydumper` / `loader`，性能会慢很多，大量数据的迁移会花费很多时间，这里我们并不推荐。

### `mydumper`/`loader` 全量导入数据最佳实践

为了快速的迁移数据 (特别是数据量巨大的库), 可以参考下面建议

* mydumper 导出数据至少要拥有 `SELECT` , `RELOAD` , `LOCK TABLES` 权限
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

> 注意：目前 TiDB 支持 UTF8mb4 [字符编码](../sql/character-set-support.md)，假设 mydumper 导出数据为 latin1 字符编码，请使用 `iconv -f latin1 -t utf-8 $file -o /data/imdbload/$basename` 命令转换，$file 为已有文件，$basename 为转换后文件。

> 注意：如果 mydumper 使用 -m 参数，会导出不带表结构的数据，这时 loader 无法导入数据。

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
binlog-gtid = "2bfabd22-fff7-11e6-97f7-f02fa73bcb01:1-23,61ccbb5d-c82d-11e6-ac2e-487b6bd31bf7:1-4"
```

+ 注意：`syncer.meta` 只需要第一次使用的时候配置，后续 `syncer` 同步新的 binlog 之后会自动将其更新到最新的 position。

+ 注意： 如果使用 binlog position 同步则只需要配置 binlog-name binlog-pos; 使用 gtid 同步则需要设置 gtid，且启动 syncer 时带有 `--enable-gtid`

### 启动 `syncer`

启动 syncer 服务之前请详细阅读 [Syncer 增量导入](../tools/syncer.md )

`syncer` 的配置文件 `config.toml`:

```toml
log-level = "info"

server-id = 101

## meta 文件地址
meta = "./syncer.meta"

worker-count = 16
batch = 10

## pprof 调试地址, Prometheus 也可以通过该地址拉取 syncer metrics
## 将 127.0.0.1 修改为相应主机 IP 地址
status-addr = "127.0.0.1:10086"

## 跳过 DDL 或者其他语句，格式为 **前缀完全匹配**，如: `DROP TABLE ABC`,则至少需要填入`DROP TABLE`.
# skip-sqls = ["ALTER USER", "CREATE USER"]

## 在使用 route-rules 功能后，
## replicate-do-db & replicate-ignore-db 匹配合表之后(target-schema & target-table )数值
## 优先级关系: replicate-do-db --> replicate-do-table --> replicate-ignore-db --> replicate-ignore-table
## 指定要同步数据库名；支持正则匹配，表达式语句必须以 `~` 开始
#replicate-do-db = ["~^b.*","s1"]

## 指定要同步的 db.table 表
## db-name 与 tbl-name 不支持 `db-name ="dbname，dbname2"` 格式
#[[replicate-do-table]]
#db-name ="dbname"
#tbl-name = "table-name"

#[[replicate-do-table]]
#db-name ="dbname1"
#tbl-name = "table-name1"

## 指定要同步的 db.table 表；支持正则匹配，表达式语句必须以 `~` 开始
#[[replicate-do-table]]
#db-name ="test"
#tbl-name = "~^a.*"

## 指定**忽略**同步数据库；支持正则匹配，表达式语句必须以 `~` 开始
#replicate-ignore-db = ["~^b.*","s1"]

## 指定**忽略**同步数据库
## db-name & tbl-name 不支持 `db-name ="dbname，dbname2"` 语句格式
#[[replicate-ignore-table]]
#db-name = "your_db"
#tbl-name = "your_table"

## 指定要**忽略**同步数据库名；支持正则匹配，表达式语句必须以 `~` 开始
#[[replicate-ignore-table]]
#db-name ="test"
#tbl-name = "~^a.*"

# sharding 同步规则，采用 wildcharacter
# 1. 星号字符 (*) 可以匹配零个或者多个字符,
#    例子, doc* 匹配 doc 和 document, 但是和 dodo 不匹配;
#    星号只能放在 pattern 结尾，并且一个 pattern 中只能有一个
# 2. 问号字符 (?) 匹配任一一个字符

#[[route-rules]]
#pattern-schema = "route_*"
#pattern-table = "abc_*"
#target-schema = "route"
#target-table = "abc"

#[[route-rules]]
#pattern-schema = "route_*"
#pattern-table = "xyz_*"
#target-schema = "route"
#target-table = "xyz"

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

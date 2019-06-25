---
title: 增量数据复制
category: how-to
aliases: ['/docs-cn/op-guide/migration/']
---

# 增量数据复制

[全量迁移](/how-to/migrate/from-mysql.md)文档中介绍了如何使用 `mydumper`/`loader` 将 MySQL 的数据全量导入到 TiDB，但如果后续 MySQL 的数据有更新，仍然希望快速导入，就不适合使用全量的方式。因此，TiDB 提供了 `syncer` 工具，可以方便地将 MySQL 的数据增量的导入到 TiDB 里面。

`syncer` 属于 TiDB 企业版工具集，如何获取可以参考 [下载 TiDB 企业版工具集](#下载-tidb-企业版工具集-linux)。

## 下载 TiDB 企业版工具集 (Linux)

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

## 获取同步 position

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

> **注意：**
>
> - `syncer.meta` 只需要第一次使用的时候配置，后续 `syncer` 同步新的 binlog 之后会自动将其更新到最新的 position。
> - 如果使用 binlog position 同步则只需要配置 binlog-name binlog-pos; 使用 gtid 同步则需要设置 gtid，且启动 syncer 时带有 `--enable-gtid`。

## 启动 `syncer`

启动 syncer 服务之前请详细阅读 [Syncer 增量导入](/tools/syncer.md )

`syncer` 的配置文件 `config.toml`:

```toml
log-level = "info"
log-file = "syncer.log"
log-rotate = "day"

server-id = 101

## meta 文件地址
meta = "./syncer.meta"
worker-count = 16
batch = 1000
flavor = "mysql"

## pprof 调试地址，Prometheus 也可以通过该地址拉取 Syncer metrics
status-addr = ":8271"

## 如果设置为 true，Syncer 遇到 DDL 语句时就会停止退出
stop-on-ddl = false

## 跳过 DDL 语句，格式为 **前缀完全匹配**，如：`DROP TABLE ABC` 至少需要填入 `DROP TABLE`
# skip-ddls = ["ALTER USER", "CREATE USER"]

## 在使用 route-rules 功能后，
## replicate-do-db & replicate-ignore-db 匹配合表之后 (target-schema & target-table) 数值
## 优先级关系: replicate-do-db --> replicate-do-table --> replicate-ignore-db --> replicate-ignore-table
## 指定要同步数据库名；支持正则匹配，表达式语句必须以 `~` 开始
#replicate-do-db = ["~^b.*","s1"]

## 指定 **忽略** 同步数据库；支持正则匹配，表达式语句必须以 `~` 开始
#replicate-ignore-db = ["~^b.*","s1"]

# skip-dmls 支持跳过 DML binlog events，type 字段的值可为：'insert'，'update' 和 'delete'
# 跳过 foo.bar 表的所有 delete 语句
# [[skip-dmls]]
# db-name = "foo"
# tbl-name = "bar"
# type = "delete"
#
# 跳过所有表的 delete 语句
# [[skip-dmls]]
# type = "delete"
#
# 跳过 foo.* 表的 delete 语句
# [[skip-dmls]]
# db-name = "foo"
# type = "delete"

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

## 指定 **忽略** 同步数据库
## db-name & tbl-name 不支持 `db-name ="dbname，dbname2"` 语句格式
#[[replicate-ignore-table]]
#db-name = "your_db"
#tbl-name = "your_table"

## 指定要 **忽略** 同步数据库名；支持正则匹配，表达式语句必须以 `~` 开始
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

## 在 MySQL 插入新的数据

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

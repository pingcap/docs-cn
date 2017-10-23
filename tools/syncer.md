---
title: Syncer 使用文档
category: advanced
---

# Syncer 使用文档

## syncer 架构
![syncer 架构](../media/syncer-architecture.png)

## 下载 TiDB 工具集 (Linux)

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

## Syncer 部署位置

Syncer 可以部署在任一台可以连通对应的 MySQL 和 TiDB 集群的机器上，推荐部署在 TiDB 集群。

## `syncer` 增量导入数据示例

### 设置同步开始的 position

设置 syncer 的 meta 文件, 这里假设 meta 文件是 `syncer.meta`:

```bash
# cat syncer.meta
binlog-name = "mysql-bin.000003"
binlog-pos = 930143241
binlog-gtid = "2bfabd22-fff7-11e6-97f7-f02fa73bcb01:1-23,61ccbb5d-c82d-11e6-ac2e-487b6bd31bf7:1-4"
```

+ 注意： `syncer.meta` 只需要第一次使用的时候配置，后续 `syncer` 同步新的 binlog 之后会自动将其更新到最新的 position
+ 注意： 如果使用 binlog position 同步则只需要配置 binlog-name binlog-pos; 使用 gtid 同步则需要设置 gtid，且启动 syncer 时带有 `--enable-gtid`

### 启动 `syncer`

`syncer` 的命令行参数说明:

```
Usage of syncer:
  -L string
      日志等级: debug, info, warn, error, fatal (默认为 "info")
  -V  
      输出 syncer 版本
  -auto-fix-gtid
      当 mysql master/slave 切换时，自动修复 gtid 信息
  -b int
      batch 事务大小 (默认 10)
  -c int
      syncer 处理 batch 线程数 (默认 16)
  -config string
      指定配置文件启动 sycner 
  -enable-gtid
      使用 gtid 模式启动 syncer 
  -log-file string
      日志文件路劲
  -log-rotate string
      指定日志切割类型, hour/day (默认 "day")
  -meta string
      指定 syncer 上有 meta 信息文件  (默认 "syncer.meta")
  -safe-mode
      启用 syncer 安全模式
  -server-id int
     指定 MySQL slave sever-ID (默认 101)
  -status-addr string
      指定 syncer metric 信息 IP:Port
```

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

## 跳过 DDL 或者其他语句，格式为**前缀完全匹配**，如: `DROP TABLE ABC`,则至少需要填入`DROP TABLE`.
# skip-sqls = ["ALTER USER", "CREATE USER"]

## 指定要同步数据库名；支持匹配，必须以 `~` 开始， 星号字符 (*) 可以匹配零个或者多个字符。
#replicate-do-db = ["~^b.*","s1"]

## 指定要同步的 db.table 表；支持匹配，必须以 `~` 开始， 星号字符 (*) 可以匹配零个或者多个字符。
## dn-name 与 tbl-name 不支持 `db-name ="dbname，dbname2"` 格式
#[[replicate-do-table]]
#db-name ="dbname"
#tbl-name = "table-name"

#[[replicate-do-table]]
#db-name ="dbname1"
#tbl-name = "table-name1"

#[[replicate-do-table]]
#db-name ="test"
#tbl-name = "~^a.*"

## 指定要**忽略**同步数据库名；支持匹配，必须以 `~` 开始， 星号字符 (*) 可以匹配零个或者多个字符。
#replicate-ignore-db = ["~^b.*","s1"]

## 指定要**忽略**同步数据库名；支持匹配，必须以 `~` 开始， 星号字符 (*) 可以匹配零个或者多个字符。
#[[replicate-ignore-table]]
#db-name = "your_db"
#tbl-name = "your_table"

## 指定要**忽略**同步数据库名；支持匹配，必须以 `~` 开始， 星号字符 (*) 可以匹配零个或者多个字符。
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

-----

## FAQ 

### sharding 同步支持

根据上面的 route-rules 可以支持将分库分表的数据导入到同一个库同一个表中，但是在开始前需要检查分库分表规则
+   是否可以利用 route-rule 的语义规则表示
+   分表中是否包含唯一递增主键，或者合并后数据上有冲突的唯一索引或者主键

![sharding](../media/syncer-sharding.png)

#### 1. 分库分表同步示例

则只需要在所有 mysql 实例下面，启动 syncer, 并且设置以下 route-rule

```toml
[[route-rules]]
pattern-schema = "example_db"
pattern-table = "table_*"
target-schema = "example_db"
target-table = "table"
```

#### 2. 指定分库分表同步示例

则只需要在所有 mysql 实例下面，启动 syncer, 并且设置以下 route-rule

```toml
## replicate-do-table 需要填入 target-schema 与 target-table 信息。
[replicate-do-table]
db-name = "example_db"
table-name = "table"

[[route-rules]]
pattern-schema = "example_db"
pattern-table = "table_*"
target-schema = "example_db"
target-table = "table"
```

## 监控方案

Syncer 使用开源时序数据库 Prometheus 作为监控和性能指标信息存储方案，使用 Grafana 作为可视化组件进行展示，配合 AlertManager 来实现报警。其方案如下图

![monitor_scheme](../media/syncer-monitor-scheme.png)

### 配置 Syncer 监控

 Prometheus 添加 syncer job 信息，将以下内容刷新到 prometheus 配置文件，重启 prometheus


```
  - job_name: 'syncer_ops' // 任务名字，区分数据上报
    static_configs:
      - targets: ['10.1.1.4:10086'] // syncer 监听地址与端口，通知 prometheus 获取 syncer 的监控数据。
```

#### Grafana 配置

+   进入 Grafana Web 界面（默认地址: http://localhost:3000 ，默认账号: admin 密码: admin）

+   导入 dashboard 配置文件

    点击 Grafana Logo -> 点击 Dashboards -> 点击 Import -> 选择需要的 Dashboard [配置文件](https://github.com/pingcap/docs/tree/master/etc)上传 -> 选择对应的 data source

### syncer 同步前检查

1.  源库 server-id 检查

	-   可通过以下命令查看 server-id:
	-   如果结果为空或者为 0，请设置为大于或者等于 ≥ 1 的正整数。 
	-   syncer 配置文件中 server-id 在 mysql server-id 上添加一个随机正整数，且不能在 mysql 主备或集群内重复。

    ```
    mysql> show global variables like 'server_id';
    +---------------+-------  
    | Variable_name | Value |
    +---------------+-------+
    | server_id     | 1     |
    +---------------+-------+
    1 row in set (0.01 sec)
    ```

1.  检查 Binlog 相关参数

	-   检查 MySQL 是否开启 binlog
	-   可以用如下命令确认是否开启了 binlog
	-   如果结果是 log_bin = OFF，需要开启。开启方式请参考[官方文档](https://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html)

    ```
    mysql> show global variables like 'log_bin'
    +--------------------+---------+
    | Variable_name | Value  |
    +--------------------+---------+
    | log_bin             | ON      |
    +--------------------+---------+
    1 row in set (0.00 sec)
    ```



1.  检查 MySQL binlog 格式是否为 ROW

	-   可以用如下命令检查 binlog 格式：

    ```
    mysql> show global variables like 'binlog_format';
    +--------------------+----------+
    | Variable_name | Value   |
    +--------------------+----------+
    | binlog_format   | ROW   |
    +--------------------+----------+
    1 row in set (0.00 sec)
    ```
	-   如果发现 binlog 格式是其他格式，可以通过如下命令设置为 ROW：
	-   如果 MySQL 有链接，建立重启 MySQL 服务。

    ```
    mysql> set global binlog_format=ROW;
    mysql>  flush logs;
    Query OK, 0 rows affected (0.01 sec)
    ```

1.  检查 MySQL binlog_row_image  是否为 FULL

	-   可以用如下命令检查 binlog_row_image

    ```
    mysql> show global variables like 'binlog_row_image';
    +--------------------------+---------+
    | Variable_name        | Value  |
    +--------------------------+---------+
    | binlog_row_image   | FULL  |
    +--------------------------+----------+
    1 row in set (0.01 sec)
    ```
	-   如果 binlog_row_image 结果不为 FULL，请设置为 FULL。设置方式如下：

    ```
    mysql> set global binlog_row_image = FULL;
    Query OK, 0 rows affected (0.01 sec)
    ```
  
1.  检查上下游同步用户权限

	-   需要上游 MySQL 同步账号至少赋予以下权限：
	-   ` select , reload , replication slave , replication client `


1.  检查 GTID 与 POS 相关信息

	-   使用以下语句查看 binlog 内容
	-   `show binlog events in 'mysql-bin.000023' from 136676560 limit 10;`


### syncer 工具数据流程

sycner 匹配规则优先级




### Syncer 性能调优

Syncer 获取一批 events 放置到 batch 中，然后由 syncer 将相应 batch 提交到 tidb 数据库。

可以根据 TiDB 集群规模机型调整 `worker-count = 16` & `batch = 10` 参数，
batch 提交时间可以观察 syncer dashboard 中的 `syncer_txn_costs_gauge_in_second` , 单位为秒。如果 metric current 比较大，将 batch 调小。

因此可以套取一个简单的公式为 `1/(transaction cost) * batch * worker-count`


### syncer 常见错误

1. [如何跳过错误语句](https://github.com/pingcap/tidb/issues/4865)
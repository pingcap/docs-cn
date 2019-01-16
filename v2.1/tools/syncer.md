---
title: Syncer 使用文档
category: tools
---

# Syncer 使用文档

## Syncer 简介

Syncer 是一个数据导入工具，能方便地将 MySQL 的数据增量导入到 TiDB。

Syncer 属于 TiDB 企业版工具集，如何获取可参考[下载 TiDB 企业版工具集](#下载-tidb-企业版工具集-linux)。

## Syncer 架构

![syncer 架构](../media/syncer-architecture.png)

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

## Syncer 部署位置

Syncer 可以部署在任一台可以连通对应的 MySQL 和 TiDB 集群的机器上，推荐部署在 TiDB 集群。

## Syncer 增量导入数据示例

使用前请详细阅读 [Syncer 同步前预检查](#syncer-同步前检查)

### 设置同步开始的 position

设置 Syncer 的 meta 文件, 这里假设 meta 文件是 `syncer.meta`:

```bash
# cat syncer.meta
binlog-name = "mysql-bin.000003"
binlog-pos = 930143241
binlog-gtid = "2bfabd22-fff7-11e6-97f7-f02fa73bcb01:1-23,61ccbb5d-c82d-11e6-ac2e-487b6bd31bf7:1-4"
```

> **注：** 
>
> - `syncer.meta` 只需要第一次使用的时候配置，后续 Syncer 同步新的 binlog 之后会自动将其更新到最新的 position。
> - 如果使用 binlog position 同步则只需要配置 binlog-name binlog-pos; 使用 gtid 同步则需要设置 gtid，且启动 Syncer 时带有 `--enable-gtid`。

### 启动 Syncer

Syncer 的命令行参数说明：

```
Usage of syncer:
  -L string
      日志等级: debug, info, warn, error, fatal (默认为 "info")
  -V  
      输出 syncer 版本；默认 false
  -auto-fix-gtid
      当 mysql master/slave 切换时，自动修复 gtid 信息；默认 false
  -b int
      batch 事务大小 (默认 10)
  -c int
      syncer 处理 batch 线程数 (默认 16)
  -config string
      指定相应配置文件启动 sycner 服务；如 `--config config.toml` 
  -enable-gtid
      使用 gtid 模式启动 syncer；默认 false，开启前需要上游 MySQL 开启 GTID 功能
  -log-file string
      指定日志文件目录；如 `--log-file ./syncer.log`
  -log-rotate string
      指定日志切割周期, hour/day (默认 "day")
  -meta string
      指定 syncer 上游 meta 信息文件  (默认与配置文件相同目录下 "syncer.meta")
  -server-id int
     指定 MySQL slave sever-id (默认 101)
  -status-addr string
      指定 syncer metric 信息; 如 `--status-addr 127:0.0.1:10088`
```

Syncer 的配置文件 `config.toml`：

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

# 注意: skip-sqls 已经废弃, 请使用 skip-ddls.
# skip-ddls 可以跳过与 TiDB 不兼容的 DDL 语句，支持正则语法。
# skip-ddls = ["^CREATE\\s+USER"]

# 注意: skip-events 已经废弃, 请使用 skip-dmls 
# skip-dmls 用于跳过 DML 语句. type 字段取值为 'insert', 'update', 'delete'。
# 下面的例子为跳过 foo.bar 表的所有 delete 语句。
# [[skip-dmls]]
# db-name = "foo"
# tbl-name = "bar"
# type = "delete"
# 
# 下面的例子为跳过所有表的 delete 语句。
# [[skip-dmls]]
# type = "delete"
# 
# 下面的例子为跳过 foo 库中所有表的 delete 语句。 
# [[skip-dmls]]
# db-name = "foo"
# type = "delete"

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

启动 Syncer：

```bash
./bin/syncer -config config.toml

2016/10/27 15:22:01 binlogsyncer.go:226: [info] begin to sync binlog from position (mysql-bin.000003, 1280)
2016/10/27 15:22:01 binlogsyncer.go:130: [info] register slave for master server 127.0.0.1:3306
2016/10/27 15:22:01 binlogsyncer.go:552: [info] rotate to (mysql-bin.000003, 1280)
2016/10/27 15:22:01 syncer.go:549: [info] rotate binlog to (mysql-bin.000003, 1280)
```

### 在 MySQL 中插入新的数据

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

Syncer 每隔 30s 会输出当前的同步统计，如下所示：

```bash
2017/06/08 01:18:51 syncer.go:934: [info] [syncer]total events = 15, total tps = 130, recent tps = 4,
master-binlog = (ON.000001, 11992), master-binlog-gtid=53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-74,
syncer-binlog = (ON.000001, 2504), syncer-binlog-gtid = 53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-17
2017/06/08 01:19:21 syncer.go:934: [info] [syncer]total events = 15, total tps = 191, recent tps = 2,
master-binlog = (ON.000001, 11992), master-binlog-gtid=53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-74,
syncer-binlog = (ON.000001, 2504), syncer-binlog-gtid = 53ea0ed1-9bf8-11e6-8bea-64006a897c73:1-35
```

由上述示例可见，使用 Syncer 可以自动将 MySQL 的更新同步到 TiDB。

## Syncer 配置说明

### 指定数据库同步

本部分将通过实际案例描述 Syncer 同步数据库参数的优先级关系。

- 如果使用 route-rules 规则，参考 [Sharding 同步支持](#sharding-同步支持) 
- 优先级：replicate-do-db --> replicate-do-table --> replicate-ignore-db --> replicate-ignore-table

```toml
# 指定同步 ops 数据库
# 指定同步以 ti 开头的数据库
replicate-do-db = ["ops","~^ti.*"]

# china 数据库下有 guangzhou / shanghai / beijing 等多张表，只同步 shanghai 与 beijing 表。
# 指定同步 china 数据库下 shanghai 表
[[replicate-do-table]]
db-name ="china"
tbl-name = "shanghai"

# 指定同步 china 数据库下 beijing 表
[[replicate-do-table]]
db-name ="china"
tbl-name = "beijing"

# ops 数据库下有 ops_user / ops_admin / weekly 等数据表，只需要同步 ops_user 表。
# 因 replicate-do-db 优先级比 replicate-do-table 高，所以此处设置只同步 ops_user 表无效，实际工作会同步 ops 整个数据库
[[replicate-do-table]]
db-name ="ops"
tbl-name = "ops_user"

# history 数据下有 2017_01 2017_02 ... 2017_12 / 2016_01  2016_02 ... 2016_12  等多张表,只需要同步 2017 年的数据表
[[replicate-do-table]]
db-name ="history"
tbl-name = "~^2017_.*"

# 忽略同步 ops 与 fault 数据库
# 忽略同步以 www 开头的数据库
## 因 replicate-do-db 优先级比 replicate-ignore-db 高，所以此处忽略同步 ops 不生效。
replicate-ignore-db = ["ops","fault","~^www"]

# fault 数据库下有 faults / user_feedback / ticket 等数据表
# 忽略同步 user_feedback 数据表
# 因 replicate-ignore-db 优先级比 replicate-ignore-table 高，所以此处设置只同步 user_feedback 表无效，实际工作会同步 fault 整个数据库
[[replicate-ignore-table]]
db-name = "fault"
tbl-name = "user_feedback"

# order 数据下有 2017_01 2017_02 ... 2017_12 / 2016_01  2016_02 ... 2016_12  等多张表,忽略 2016 年的数据表
[[replicate-ignore-table]]
db-name ="order"
tbl-name = "~^2016_.*"
```

### Sharding 同步支持

根据配置文件的 route-rules，支持将分库分表的数据导入到同一个库同一个表中，但是在开始前需要检查分库分表规则，如下：

- 是否可以利用 route-rules 的语义规则表示
- 分表中是否包含唯一递增主键，或者合并后是否包含数据上有冲突的唯一索引或者主键

暂时对 DDL 支持不完善。

![sharding](../media/syncer-sharding.png)

#### 分库分表同步示例

1. 只需在所有 MySQL 实例下面，启动 Syncer, 并设置 route-rules。
2. `replicate-do-db` & `replicate-ignore-db` 与 route-rules 同时使用场景下，`replicate-do-db` & `replicate-ignore-db` 需要指定 route-rules 中 `target-schema` & `target-table` 的内容。

```toml
# 场景如下:
# 数据库A 下有 order_2016 / history_2016 等多个数据库
# 数据库B 下有 order_2017 / history_2017 等多个数据库
# 指定同步数据库A  order_2016 数据库，数据表如下 2016_01 2016_02 ... 2016_12 
# 指定同步数据表B  order_2017 数据库，数据表如下 2017_01 2017_02 ... 2017_12
# 表内使用 order_id 作为主键，数据之间主键不冲突
# 忽略同步 history_2016 与 history_2017 数据库
# 目标库需要为 order ，目标数据表为 order_2017 / order_2016

# Syncer 获取到上游数据后，发现 route-rules 规则启用，先做合库合表操作，再进行 do-db & do-table 判定
## 此处需要设置 target-schema & target-table 判定需要同步的数据库
[[replicate-do-table]]
db-name ="order"
tbl-name = "order_2016"

[[replicate-do-table]]
db-name ="order"
tbl-name = "order_2017"

[[route-rules]]
pattern-schema = "order_2016"
pattern-table = "2016_??"
target-schema = "order"
target-table = "order_2016"

[[route-rules]]
pattern-schema = "order_2017"
pattern-table = "2017_??"
target-schema = "order"
target-table = "order_2017"
```

### Syncer 同步前检查

1. 源库 server-id 检查

    - 可通过以下命令查看 server-id 
    - 结果为空或者为 0，Syncer 无法同步数据
    - Syncer server-id 与 MySQL server-id 不能相同，且在 MySQL cluster 中唯一

    ```sql
    mysql> show global variables like 'server_id';
    +---------------+-------  
    | Variable_name | Value |
    +---------------+-------+
    | server_id     | 1     |
    +---------------+-------+
    1 row in set (0.01 sec)
    ```

2. 检查 Binlog 相关参数

    - 检查 MySQL 是否开启 binlog
    - 可以用如下命令确认是否开启了 binlog
    - 如果结果是 log_bin = OFF，需要开启。开启方式请参考[官方文档](https://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html)

    ```sql
    mysql> show global variables like 'log_bin';
    +--------------------+---------+
    | Variable_name | Value  |
    +--------------------+---------+
    | log_bin             | ON      |
    +--------------------+---------+
    1 row in set (0.00 sec)
    ```

3. 检查 MySQL binlog 格式是否为 ROW

    - 可以用如下命令检查 binlog 格式：

    ```sql
    mysql> show global variables like 'binlog_format';
    +--------------------+----------+
    | Variable_name | Value   |
    +--------------------+----------+
    | binlog_format   | ROW   |
    +--------------------+----------+
    1 row in set (0.00 sec)
    ```

    - 如果发现 binlog 格式是其他格式，可以通过如下命令设置为 ROW：
    - 如果 MySQL 有连接，建议重启 MySQL 服务或者杀掉所有连接。

    ```sql
    mysql> set global binlog_format=ROW;
    mysql>  flush logs;
    Query OK, 0 rows affected (0.01 sec)
    ```

4. 检查 MySQL `binlog_row_image` 是否为 FULL

    - 可以用如下命令检查 `binlog_row_image`

    ```sql
    mysql> show global variables like 'binlog_row_image';
    +--------------------------+---------+
    | Variable_name        | Value  |
    +--------------------------+---------+
    | binlog_row_image   | FULL  |
    +--------------------------+----------+
    1 row in set (0.01 sec)
    ```

    - 如果 binlog_row_image 结果不为 FULL，请设置为 FULL。设置方式如下：

    ```sql
    mysql> set global binlog_row_image = FULL;
    Query OK, 0 rows affected (0.01 sec)
    ```
5. 检查 mydumper 用户权限

    - mydumper 导出数据至少拥有以下权限：`select, reload`
    - mydumper 操作对象为 RDS 时，可以添加 `--no-locks` 参数，避免申请 `reload` 权限

6. 检查上下游同步用户权限

    - 需要上游 MySQL 同步账号至少赋予以下权限：
        
        ```
        select , replication slave , replication client
        ```
    
    - 下游 TiDB 可暂时采用 root 同权限账号

7. 检查 GTID 与 POS 相关信息

    - 使用以下语句查看 binlog 内容：
        
        ```sql
        show binlog events in 'mysql-bin.000023' from 136676560 limit 10;
        ```

## 监控方案

Syncer 使用开源时序数据库 Prometheus 作为监控和性能指标信息存储方案，使用 Grafana 作为可视化组件进行展示，配合 AlertManager 来实现报警。其方案如下图所示：

![monitor_scheme](../media/syncer-monitor-scheme.png)

### 配置 Syncer 监控与告警

Syncer 对外提供 metric 接口，需要 Prometheus 主动获取数据。配置 Syncer 监控与告警的操作步骤如下：

1. 在 Prometheus 中添加 Syncer job 信息，将以下内容刷新到 Prometheus 配置文件，重启 Prometheus 后生效。

    ```yaml
        - job_name: 'syncer_ops' // 任务名字，区分数据上报
          static_configs:
            - targets: ['10.1.1.4:10086'] // Syncer 监听地址与端口，通知 Prometheus 获取 Syncer 的监控数据。
    ```

2. 配置 Prometheus [告警](https://prometheus.io/docs/alerting/alertmanager/)，将以下内容刷新到 `alert.rule` 配置文件，重启 Prometheus 后生效。

    ```
    # syncer
    ALERT syncer_status
      IF  syncer_binlog_file{node='master'} - ON(instance, job) syncer_binlog_file{node='syncer'} > 1
      FOR 1m
      LABELS {channels="alerts", env="test-cluster"}
      ANNOTATIONS {
      summary = "syncer status error",
      description="alert: syncer_binlog_file{node='master'} - ON(instance, job) syncer_binlog_file{node='syncer'} > 1 instance: {{     $labels.instance }} values: {{ $value }}",
      }
    ```

#### Grafana 配置

+ 进入 Grafana Web 界面（默认地址: http://localhost:3000 ，默认账号: admin 密码: admin）

+ 导入 dashboard 配置文件

    点击 Grafana Logo -> 点击 Dashboards -> 点击 Import -> 选择需要的 Dashboard [配置文件](https://github.com/pingcap/docs/tree/master/etc)上传 -> 选择对应的 data source

### Grafana Syncer metrics 说明 

#### title: binlog events

- metrics: `irate(syncer_binlog_events_total[1m])`
- info: Syncer 已经同步到的 master binlog 相关信息统计，主要有 `query`，`rotate`，`update_rows`，`write_rows`，`delete_rows` 五种类型

#### title: syncer_binlog_file

- metrics: `syncer_binlog_file`
- info: Syncer 同步 master binlog 的文件数量

#### title: binlog pos

- metrics: `syncer_binlog_pos`
- info: Syncer 同步当前 master binlog 的 binlog-pos 信息

#### title: syncer_gtid

- metrics: `syncer_gtid`
- info: Syncer 同步当前 master binlog 的 binlog-gtid 信息

#### title: syncer_binlog_file

- metrics: `syncer_binlog_file{node="master"} - ON(instance, job) syncer_binlog_file{node="syncer"}`
- info: 上游与下游同步时，相差的 binlog 文件数量，正常状态为 0，表示数据正在实时同步。数值越大，表示相差的 binlog 文件数量越多。

#### title: binlog skipped events

- metrics: `irate(syncer_binlog_skipped_events_total[1m])`
- info: Syncer 同步 master binlog 文件时跳过执行 SQL 的数量统计。跳过 SQL 语句格式由 `syncer.toml` 文件中的 `skip-sqls` 参数控制。

#### title: syncer_txn_costs_gauge_in_second

- metrics: `syncer_txn_costs_gauge_in_second`
- info: Syncer 处理一个 batch 的时间，单位为秒

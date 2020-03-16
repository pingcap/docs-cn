---
title: Sql Dignosis Schema
category: reference
---

# SQL DIAGNOSIS
SQL 诊断功能是由 TiDB 4.0 引入的新特性，主要用于提升 TiDB 问题定位效率，相较于 4.0 版本之前，不同的信息需要使用不同工具获取的异构方式，
新的 SQL 诊断对这些离散的信息进行了整体设计，它通过将系统的各种维度信息通过系统表的方式向上层提供了一致的接口方式以及监控汇总与自动诊断，方便了用户对于集群信息的查询。

SQL 诊断共分三大块：
* **集群信息表**：TiDB 4.0 诊断功能为原先离散的各节点实例信息提供了一致的获取方式，它将整个集群的集群拓扑、硬件信息、软件信息、内核参数、监控、系统信息、慢查询、Statements、日志完全打通，让使用者能够统一使用 SQL 查询。
* **集群监控与汇总**：TiDB 4.0 诊断系统添加了集群监控系统表，所有表都在 metrics_schema 中，可以通过 SQL 的方式查询监控，相对于原先的可视化监控，SQL 查询监控的好处在于可以对整个集群的所有监控进行关联查询，并对比不同时间段的结果，迅速找出性能瓶颈。
且由于 TiDB 集群的监控指标数量较大，SQL 诊断还提供了监控汇总表，从而让用户能以一种更加便捷的方式从众多监控中找出异常的监控项。
* **诊断结果表**：尽管用户可以手动执行 SQL 来查询集群信息表和集群监控表与汇总表来发现集群问题，但自动挡总是更香的，所以 SQL 诊断利用已有的基础信息表提供了诊断相关的系统表来自动执行诊断。


## 集群信息表
集群信息表包括集群拓扑、集群配置、集群硬件、内核参数、系统负载、日志、集群监控等，这些集群表将一个集群中的所有节点实例的信息都汇聚到了一起，让用户仅通过一条 SQL 就能查询整个集群相关信息。
新增的集群信息表如下：

* 集群拓扑表 `information_schema.cluster_info` 主要是用于获取集群当前的拓扑信息，以及各个节点的版本、版本对应的 Git Hash、启动时间、运行时间信息。
* 集群配置表 `information_schema.cluster_config` 用于获取集群当前所有节点的配置，TiDB 4.0 之前的版本必须逐个访问各个节点的 HTTP API。
* 集群硬件表 `information_schema.cluster_hardware` 主要用于快速查询集群硬件信息。
* 集群负载表 `information_schema.cluster_load` 主要用于查询集群不同节点的不同硬件类型的负载信息。
* 内核参数表 `information_schema.cluster_systeminfo` 主要用于查询集群不同节点的内核配置信息，目前支持查询 sysctl 的信息。
* 集群日志表 `information_schema.cluster_log` 表主要用于集群日志查询，通过将查询条件下推到各个节点，降低日志查询对集群的影响，性能影响小于等 grep 命令。

TiDB 4.0 之前的以下系统表，只能查看当前节点，TiDB 4.0 实现了对应的集群表，可以在单个 TiDB 节点上拥有整个集群的全局视图。
这些表目前都位于 information_schema 中，查询形式上与其他 information_schema 系统表一致。

## CLUSTER_INFO 表

集群拓扑表 `CLUSTER_INFO` 提供了集群当前的拓扑信息，以及各个节点的版本、版本对应的 Git Hash、启动时间、运行时间信息。

```
mysql> desc cluster_info;
+----------------+-------------+------+------+---------+-------+
| Field          | Type        | Null | Key  | Default | Extra |
+----------------+-------------+------+------+---------+-------+
| TYPE           | varchar(64) | YES  |      | NULL    |       |
| INSTANCE       | varchar(64) | YES  |      | NULL    |       |
| STATUS_ADDRESS | varchar(64) | YES  |      | NULL    |       |
| VERSION        | varchar(64) | YES  |      | NULL    |       |
| GIT_HASH       | varchar(64) | YES  |      | NULL    |       |
| START_TIME     | varchar(32) | YES  |      | NULL    |       |
| UPTIME         | varchar(32) | YES  |      | NULL    |       |
+----------------+-------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

字段解释：

* TYPE：节点类型，目前节点的类型为 pd/tikv/tidb，节点类型始终为小写
* INSTANCE：实例地址，始终为 IP:PORT 格式的字符串
* STATUS_ADDRESS：HTTP API 服务地址，部分 tikv-ctl / pd-ctl / tidb-ctl 命令会使用到 HTTP API，会使用这个地址，用户也可以通过这个地址获取一些额外的集群信息，具体 HTTP API 参考官方文档
* VERSION：对应节点的语义版本号，TiDB 版本为了兼容 MySQL 的版本号，以 ${mysql-version}-${tidb-version} 方式展示
* GIT_HASH：对应节点版本编译时的 git commit hash，主要用于识别两个节点是否是绝对一致的版本
* START_TIME：对应节点的启动时间
* UPTIME：对应节点已经运行的时间

```sql
mysql> select * from cluster_info;
+------+-----------------+-----------------+----------------------------------------+------------------------------------------+---------------------------+--------------+
| TYPE | INSTANCE        | STATUS_ADDRESS  | VERSION                                | GIT_HASH                                 | START_TIME                | UPTIME       |
+------+-----------------+-----------------+----------------------------------------+------------------------------------------+---------------------------+--------------+
| tidb | 127.0.0.1:4000  | 127.0.0.1:10080 | 5.7.25-TiDB-v4.0.0-beta-195-gb5ea3232a | b5ea3232afa970f00db7a0fb13ed10857db1912e | 2020-03-02T16:27:28+08:00 | 4m18.845924s |
| pd   | 127.0.0.1:2379  | 127.0.0.1:2379  | 4.1.0-alpha                            | 4b9bcbc1425c96848042b6d700eb63f84e72b338 | 2020-03-02T16:27:17+08:00 | 4m29.845928s |
| tikv | 127.0.0.1:20160 | 127.0.0.1:20180 | 4.1.0-alpha                            | 7c4202a1c8faf60eda659dfe0e64e31972488e78 | 2020-03-02T16:27:28+08:00 | 4m18.845929s |
+------+-----------------+-----------------+----------------------------------------+------------------------------------------+---------------------------+--------------+
3 rows in set (0.01 sec)
```


## CLUSTER_CONFIG 表

集群配置表 `CLUSTER_CONFIG` 用于获取集群当前所有节点的配置，而 TiDB 4.0 之前的版本必须通过逐个访问各个节点的 HTTP API 的形式才能收集到所有节点配置。

```
mysql> desc cluster_config;
+----------+--------------+------+------+---------+-------+
| Field    | Type         | Null | Key  | Default | Extra |
+----------+--------------+------+------+---------+-------+
| TYPE     | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE | varchar(64)  | YES  |      | NULL    |       |
| KEY      | varchar(256) | YES  |      | NULL    |       |
| VALUE    | varchar(128) | YES  |      | NULL    |       |
+----------+--------------+------+------+---------+-------+
4 rows in set (0.00 sec)
```

字段解释：

* TYPE：对应于节点信息表 `information_schema.cluster_info`  中的 TYPE 字段，可取值为 tidb/pd/tikv，且均为小写
* INSTANCE：对应于节点信息表 `information_schema.cluster_info`  中的 STATUS_ADDRESS 字段
* KEY：配置项名
* VALUE：配置项值

具体示例，查询 TiKV 节点的 `coprocessor` 相关配置：

```sql
mysql> select * from cluster_config where type='tikv' and `key` like 'coprocessor%';
+------+-----------------+-----------------------------------+----------+
| TYPE | INSTANCE        | KEY                               | VALUE    |
+------+-----------------+-----------------------------------+----------+
| tikv | 127.0.0.1:20160 | coprocessor.batch-split-limit     | 10       |
| tikv | 127.0.0.1:20160 | coprocessor.region-max-keys       | 1.44e+06 |
| tikv | 127.0.0.1:20160 | coprocessor.region-max-size       | 144MiB   |
| tikv | 127.0.0.1:20160 | coprocessor.region-split-keys     | 960000   |
| tikv | 127.0.0.1:20160 | coprocessor.region-split-size     | 96MiB    |
| tikv | 127.0.0.1:20160 | coprocessor.split-region-on-table | false    |
+------+-----------------+-----------------------------------+----------+
6 rows in set (1.04 sec)
```

## CLUSTER_HARDWARE
集群硬件表 `CLUSTER_HARDWARE` 提供了集群各节点实例的硬件信息。

```field
mysql> desc cluster_hardware;
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE    | varchar(64)  | YES  |      | NULL    |       |
| DEVICE_TYPE | varchar(64)  | YES  |      | NULL    |       |
| DEVICE_NAME | varchar(64)  | YES  |      | NULL    |       |
| NAME        | varchar(256) | YES  |      | NULL    |       |
| VALUE       | varchar(128) | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

字段解释：

* TYPE：对应于节点信息表 `information_schema.cluster_info`  中的 TYPE 字段，可取值为 tidb/pd/tikv，且均为小写
* INSTANCE：对应于节点信息表 `information_schema.cluster_info`  中的 STATUS_ADDRESS 字段
* DEVICE_TYPE：硬件类型，目前可以查询的硬件类型有 cpu/memory/disk/net
* DEVICE_NAME：硬件名，对于不同的 DEVICE_TYPE，取值不同
  * cpu：硬件名为 cpu
  * memory：硬件名为 memory
  * disk：磁盘名
  * net：NIC 名
* NAME：硬件不同的信息名，比如 cpu 有 `cpu-logical-cores`/`cpu-physical-cores`，可以通过 `select name from cluster_hardware where device_type='cpu' group by name` 来查询不同硬件类型支持的 NAME
* VALUE：对应硬件信息的值，比如磁盘容量，CPU 核数

具体示例，查询集群的 CPU 信息：

```sql
mysql> select * from cluster_hardware where device_type='cpu' and device_name='cpu' and name like '%cores';
+------+-----------------+-------------+-------------+--------------------+-------+
| TYPE | INSTANCE        | DEVICE_TYPE | DEVICE_NAME | NAME               | VALUE |
+------+-----------------+-------------+-------------+--------------------+-------+
| tidb | 127.0.0.1:10080 | cpu         | cpu         | cpu-logical-cores  | 8     |
| tidb | 127.0.0.1:10080 | cpu         | cpu         | cpu-physical-cores | 4     |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | cpu-logical-cores  | 8     |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | cpu-physical-cores | 4     |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | cpu-logical-cores  | 8     |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | cpu-physical-cores | 4     |
+------+-----------------+-------------+-------------+--------------------+-------+
6 rows in set (0.26 sec)
```

## CLUSTER_LOAD
集群负载表 `CLUSTER_LOAD` 提供了集群不同节点的不同硬件类型的当前负载信息。

```field
mysql> desc cluster_load;
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE    | varchar(64)  | YES  |      | NULL    |       |
| DEVICE_TYPE | varchar(64)  | YES  |      | NULL    |       |
| DEVICE_NAME | varchar(64)  | YES  |      | NULL    |       |
| NAME        | varchar(256) | YES  |      | NULL    |       |
| VALUE       | varchar(128) | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

字段解释：
* TYPE：对应于节点信息表 `information_schema.cluster_info`  中的 TYPE 字段，可取值为 tidb/pd/tikv，且均为小写。
* INSTANCE：对应于节点信息表 `information_schema.cluster_info`  中的 STATUS_ADDRESS 字段。
* DEVICE_TYPE：硬件类型，目前可以查询的硬件类型有 cpu/memory/disk/net。
* DEVICE_NAME：硬件名，对于不同的 DEVICE_TYPE，取值不同。
  * cpu：硬件名为 cpu。
  * disk：磁盘名。
  * net：NIC 名。
  * memory：硬件名为 memory。
* NAME：不同负载类型，比如 cpu 有 `load1/load5/load15` 分别表示 CPU 在 1min/5min/15min 中的平均负载，可以通过 `select name from cluster_load where device_type='cpu' group by name` 来查询不同硬件类型支持的 NAME。
* VALUE：对应硬件负载的值，比如 CPU 的 1min/5min/15min 平均负载。


具体示例，查询集群的 CPU 负载信息：

```sql
mysql> select * from cluster_load where device_type='cpu' and device_name='cpu';
+------+-----------------+-------------+-------------+--------+---------------+
| TYPE | INSTANCE        | DEVICE_TYPE | DEVICE_NAME | NAME   | VALUE         |
+------+-----------------+-------------+-------------+--------+---------------+
| tidb | 127.0.0.1:10080 | cpu         | cpu         | load1  | 1.94          |
| tidb | 127.0.0.1:10080 | cpu         | cpu         | load5  | 2.16          |
| tidb | 127.0.0.1:10080 | cpu         | cpu         | load15 | 2.24          |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load1  | 1.94          |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load5  | 2.16          |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load15 | 2.24          |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | load1  | 1.94287109375 |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | load5  | 2.15576171875 |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | load15 | 2.2421875     |
+------+-----------------+-------------+-------------+--------+---------------+
9 rows in set (0.52 sec)
```

## CLUSTER_SYSTEMINFO
集群负载表 `CLUSTER_SYSTEMINFO` 主要用于查询集群不同节点的内核配置信息，目前支持查询 sysctl 的信息。

```field
mysql> desc cluster_systeminfo;
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE    | varchar(64)  | YES  |      | NULL    |       |
| SYSTEM_TYPE | varchar(64)  | YES  |      | NULL    |       |
| SYSTEM_NAME | varchar(64)  | YES  |      | NULL    |       |
| NAME        | varchar(256) | YES  |      | NULL    |       |
| VALUE       | varchar(128) | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

字段解释：

* TYPE：对应于节点信息表 `information_schema.cluster_info` 中的 TYPE 字段，可取值为 tidb/pd/tikv，且均为小写。
* INSTANCE：对应于节点信息表 `information_schema.cluster_info`  中的 STATUS_ADDRESS 字段。
* SYSTEM_TYPE：系统类型，目前可以查询的系统类型有 system。
* SYSTEM_NAME：目前可以查询的 SYSTEM_NAME 为 sysctl。
* NAME：sysctl 对应的配置名。
* VALUE：sysctl 对应配置项的值。

```sql
mysql> select * from cluster_systeminfo where name like '%fd%';
+------+-----------------+-------------+-------------+-------------------------------+-------+
| TYPE | INSTANCE        | SYSTEM_TYPE | SYSTEM_NAME | NAME                          | VALUE |
+------+-----------------+-------------+-------------+-------------------------------+-------+
| tidb | 127.0.0.1:10080 | system      | sysctl      | net.inet6.ip6.maxifdefrouters | 16    |
| tidb | 127.0.0.1:10080 | system      | sysctl      | net.necp.client_fd_count      | 98    |
| tidb | 127.0.0.1:10080 | system      | sysctl      | net.necp.observer_fd_count    | 0     |
| pd   | 127.0.0.1:2379  | system      | sysctl      | net.inet6.ip6.maxifdefrouters | 16    |
| pd   | 127.0.0.1:2379  | system      | sysctl      | net.necp.client_fd_count      | 98    |
| pd   | 127.0.0.1:2379  | system      | sysctl      | net.necp.observer_fd_count    | 0     |
+------+-----------------+-------------+-------------+-------------------------------+-------+
6 rows in set (0.04 sec)
```

## CLUSTER_LOG
集群日志表 `CLUSTER_LOG` 表主要用于集群日志查询，通过将查询条件下推到各个节点，降低日志查询对集群的影响，**性能影响小于 grep 命令**。

```field
mysql> desc cluster_log;
+----------+---------------------------+------+------+---------+-------+
| Field    | Type                      | Null | Key  | Default | Extra |
+----------+---------------------------+------+------+---------+-------+
| TIME     | varchar(32)               | YES  |      | NULL    |       |
| TYPE     | varchar(64)               | YES  |      | NULL    |       |
| INSTANCE | varchar(64)               | YES  |      | NULL    |       |
| LEVEL    | varchar(8)                | YES  |      | NULL    |       |
| MESSAGE  | var_string(1024) unsigned | YES  |      | NULL    |       |
+----------+---------------------------+------+------+---------+-------+
5 rows in set (0.00 sec)
```

字段解释：
* TIME：日志打印时间。
* TYPE：对应于节点信息表 `information_schema.cluster_info` 中的 TYPE 字段，可取值为 tidb/pd/tikv，且均为小写。
* INSTANCE：对应于节点信息表 `information_schema.cluster_info` 中的 INSTANCE 字段。
* LEVEL：日志级别。
* MESSAGE：日志内容。

> **注意事项：**
>日志表的所有字段都会下推到对应节点执行，所以为了降低使用集群日志表的开销，需尽可能地指定更多的条件，比如 select * from cluter_log where instance='tikv-1' 只会在 tikv-1 执行日志搜索。
>message 字段支持 like 和 regexp 正则表达式，对应的 pattern 会编译为 regexp，同时指定多个 message 条件，相当于 grep 命令的 pipeline 形式，例如：select * from cluster_log where message like 'coprocessor%' and message regexp '.*slow.*' 相当于在集群所有节点执行 grep 'coprocessor' xxx.log | grep -E '.*slow.*'。

在TiDB 4.0 之前要获取集群的日志需要逐个登录各个节点汇总日志。TiDB 4.0 有了集群日志表后，可以更高效地提供一个全局时间有序的日志搜索结果，对于全链路事件跟踪提供便利的手段，比如按照某一个 region id 搜索日志，可以查询该 region 生命周期的所有日志，类似的通过慢日志的 txn id 搜索全链路日志，可以查询该事务在各个节点扫描的 key 数量以及流量等信息。

## 集群监控表

TiDB 4.0 诊断系统添加了集群监控系统表，所有表都在 `metrics_schema` 中，可以通过 SQL 的方式查询监控，SQL 查询监控的好处在于可以对整个集群的所有监控进行关联查询，
并对比不同时间段的结果，迅速找出性能瓶颈。由于目前添加的系统表数量较多，本文不对各个表进行逐个解释。用户可以通过 `information_schema.metrics_tables` 查询这些表的相关信息。

```field
mysql> desc metrics_tables;
+------------+-----------------+------+------+---------+-------+
| Field      | Type            | Null | Key  | Default | Extra |
+------------+-----------------+------+------+---------+-------+
| TABLE_NAME | varchar(64)     | YES  |      | NULL    |       |
| PROMQL     | varchar(64)     | YES  |      | NULL    |       |
| LABELS     | varchar(64)     | YES  |      | NULL    |       |
| QUANTILE   | double unsigned | YES  |      | NULL    |       |
| COMMENT    | varchar(256)    | YES  |      | NULL    |       |
+------------+-----------------+------+------+---------+-------+
5 rows in set (0.00 sec)
```

表 `metrics_tables` 的字段解释：
* TABLE_NAME：对应于 metrics_schema 中的表名。
* PROMQL：监控表的主要原理是将 SQL 映射成 PromQL，并将 Promethues 结果转换成 SQL 查询结果。这个字段是 PromQL 的表达式模板，获取监控表数据时使用查询条件改写模板中的变量，生成最终的查询表达式。
* LABELS：监控定义的 label，每一个 label 会对应监控表中的一列，SQL 中如果包含对应列的过滤，对应的 PromQL 也会改变。
* QUANTILE：百分位，对于直方图类型的监控数据，指定一个默认百分位，如果值为 0，表示该监控表对应的监控不是直方图。
* COMMENT：是对这个监控表的解释。

监控表示例:

`tidb_query_duration` 的表结构如下，从表的 COMMENT 中可以看出，这个表的是用来查询 TiDB query 执行的百分位时间，如 P999，P99，P90 的查询耗时，单位是秒。

```sql
metrics_schema> show create table tidb_query_duration;
+---------------------+--------------------------------------------------------------------------------------------------------------------+
| Table               | Create Table                                                                                                       |
+---------------------+--------------------------------------------------------------------------------------------------------------------+
| tidb_query_duration | CREATE TABLE `tidb_query_duration` (                                                                               |
|                     |   `time` datetime unsigned DEFAULT NULL,                                                                           |
|                     |   `instance` varchar(512) DEFAULT NULL,                                                                            |
|                     |   `sql_type` varchar(512) DEFAULT NULL,                                                                            |
|                     |   `quantile` double unsigned DEFAULT NULL,                                                                         |
|                     |   `value` double unsigned DEFAULT NULL                                                                             |
|                     | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='The quantile of TiDB query durations(second)' |
+---------------------+--------------------------------------------------------------------------------------------------------------------+
```

比如 tikv_admin_apply 有三个 label，对应的表也会有三个额外的列
```sql
mysql> desc metrics_schema.tikv_admin_apply;
+----------+-------------------+------+------+---------+-------+
| Field    | Type              | Null | Key  | Default | Extra |
+----------+-------------------+------+------+---------+-------+
| time     | datetime unsigned | YES  |      | NULL    |       |
| instance | varchar(512)      | YES  |      | NULL    |       |
| type     | varchar(512)      | YES  |      | NULL    |       |
| status   | varchar(512)      | YES  |      | NULL    |       |
| value    | double unsigned   | YES  |      | NULL    |       |
+----------+-------------------+------+------+---------+-------+
5 rows in set (0.00 sec)
```

下面是查询当前时间的 P90 的 TiDB Query 耗时，可以看出，Select 类似的 Query 的 P90 耗时是 0.0384 秒，internal 类型的 P90 耗时是 0.00327。instance 字段是 TiDB 示例的地址。
```
metrics_schema> select * from tidb_query_duration where value is not null and time=now() and quantile=0.90;
+---------------------+-------------------+----------+----------+------------------+
| time                | instance          | sql_type | quantile | value            |
+---------------------+-------------------+----------+----------+------------------+
| 2020-03-08 13:34:40 | 172.16.5.40:10089 | Select   | 0.9      | 0.0384           |
| 2020-03-08 13:34:40 | 172.16.5.40:10089 | internal | 0.9      | 0.00327692307692 |
+---------------------+-------------------+----------+----------+------------------+
```

监控表 session 变量：

* tidb_metric_query_step：查询的分辨率步长。从 Promethues 的 query_range 数据时需要指定 start，end，step，其中 step 会使用该变量的值
* tidb_metric_query_range_duration：查询监控时，会将 PROMQL 中的 $RANGE_DURATION 替换成该变量的值，默认值是 60 秒

## 监控汇总表

由于 TiDB 集群的监控指标数量较大，因此为了方便用户能更加便捷地从众多监控中找出异常的监控项，TiDB 4.0 提供了监控汇总表：

* information_schema.metrics_summary
* information_schema.metrics_summary_by_label

这两张表用于汇总所有监控数据，以提升用户对各个监控指标进行排查的效率。
两者不同在于 information_schema.metrics_summary_by_label 会对不同的 label 使用区分统计。

```field
mysql> desc metrics_summary;
+--------------+-----------------------+------+------+---------+-------+
| Field        | Type                  | Null | Key  | Default | Extra |
+--------------+-----------------------+------+------+---------+-------+
| METRICS_NAME | varchar(64)           | YES  |      | NULL    |       |
| QUANTILE     | double unsigned       | YES  |      | NULL    |       |
| SUM_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| AVG_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| MIN_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| MAX_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| COMMENT      | varchar(256)          | YES  |      | NULL    |       |
+--------------+-----------------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

字段解释：

* METRICS_NAME：监控表名
* QUANTILE：百分位，可以通过 SQL 语句指定 QUANTILE，例如
  * select * from metrics_summary where quantile=0.99 指定查看百分位为 0.99 的数据
  * select * from metrics_summary where quantile in (0.80, 0.99, 0.99, 0.999) 同时查看百分位为 0.80, 0.99, 0.99, 0.999 的数据
* SUM_VALUE / AVG_VALUE / MIN_VALUE / MAX_VALUE
* COMMENT：对应监控的解释

具体查询示例：
以查询 ['2020-03-08 13:23:00', '2020-03-08 13:33:00') 时间范围内 TiDB 集群中平均耗时最高的 3 组监控项为例。通过直接查询 information_schema.metrics_summary 表，并通过 /*+ time_range() */ 这个 hint 来指定时间范围来构造以下 SQL：

```
mysql> select /*+ time_range('2020-03-08 13:23:00','2020-03-08 13:33:00') */ *
       from information_schema.`METRICS_SUMMARY`
       where metrics_name like 'tidb%duration'
         and avg_value > 0
         and quantile = 0.99
       order by avg_value desc
       limit 3\G
***************************[ 1. row ]***************************
METRICS_NAME | tidb_get_token_duration
QUANTILE     | 0.99
SUM_VALUE    | 8.972509
AVG_VALUE    | 0.996945
MIN_VALUE    | 0.996515
MAX_VALUE    | 0.997458
COMMENT      |  The quantile of Duration (us) for getting token, it should be small until concurrency limit is reached(second)
***************************[ 2. row ]***************************
METRICS_NAME | tidb_query_duration
QUANTILE     | 0.99
SUM_VALUE    | 0.269079
AVG_VALUE    | 0.007272
MIN_VALUE    | 0.000667
MAX_VALUE    | 0.01554
COMMENT      | The quantile of TiDB query durations(second)
***************************[ 3. row ]***************************
METRICS_NAME | tidb_kv_request_duration
QUANTILE     | 0.99
SUM_VALUE    | 0.170232
AVG_VALUE    | 0.004601
MIN_VALUE    | 0.000975
MAX_VALUE    | 0.013
COMMENT      | The quantile of kv requests durations by store
```

类似的，查询 metrics_summary_by_label 监控汇总表结果如下：

```
mysql> select /*+ time_range('2020-03-08 13:23:00','2020-03-08 13:33:00') */ *
       from information_schema.`METRICS_SUMMARY_BY_LABEL`
       where metrics_name like 'tidb%duration'
         and avg_value > 0
         and quantile = 0.99
       order by avg_value desc
       limit 10\G
***************************[ 1. row ]***************************
INSTANCE     | 172.16.5.40:10089
METRICS_NAME | tidb_get_token_duration
LABEL        |
QUANTILE     | 0.99
SUM_VALUE    | 8.972509
AVG_VALUE    | 0.996945
MIN_VALUE    | 0.996515
MAX_VALUE    | 0.997458
COMMENT      |  The quantile of Duration (us) for getting token, it should be small until concurrency limit is reached(second)
***************************[ 2. row ]***************************
INSTANCE     | 172.16.5.40:10089
METRICS_NAME | tidb_query_duration
LABEL        | Select
QUANTILE     | 0.99
SUM_VALUE    | 0.072083
AVG_VALUE    | 0.008009
MIN_VALUE    | 0.007905
MAX_VALUE    | 0.008241
COMMENT      | The quantile of TiDB query durations(second)
***************************[ 3. row ]***************************
INSTANCE     | 172.16.5.40:10089
METRICS_NAME | tidb_query_duration
LABEL        | Rollback
QUANTILE     | 0.99
SUM_VALUE    | 0.072083
AVG_VALUE    | 0.008009
MIN_VALUE    | 0.007905
MAX_VALUE    | 0.008241
COMMENT      | The quantile of TiDB query durations(second)
```

前文提到 `metrics_summary_by_label` 表结构相对于 `metrics_summary` 多了一列 LABEL, 以上面查询结果的第 2, 3 行为例：分别表示 `tidb_query_duration` 的 Select/Rollback 类型的语句平均耗时非常高。

除以上示例之外，监控汇总表可以通过两个时间段的全链路监控对比，迅速找出监控数据变化最大的模块，快速定位瓶颈，以下对比两个时间段的所有监控（其中 t1 为 baseline），并按照差别最大的监控排序：

* 时间段 t1 : ("2020-03-03 17:08:00", "2020-03-03 17:11:00")
* 时间段 t2 : ("2020-03-03 17:18:00", "2020-03-03 17:21:00")
对两个时间段的监控按照 METRICS_NAME 进行 join，并按照差值排序。其中 TIME_RANGE 是用于指定查询时间的 Hint。

从上述查询结果可以看出：
* t1 时间段内的 tikv_region_average_written_bytes （region 的平均写入字节数） 比 t2 时间段高了 17.6 倍
* t1 时间段内的 tikv_region_average_written_keys （region 的平均写入 keys 数） 比 t2 时间段高了 8.8 倍
* t1 时间段内的 tidb_kv_write_size （tidb 每个事务写入的 kv 大小） 比 t2 时间段高了 1.96 倍

通过以上结果可以轻易看出 t1 时间段的写入要比 t2 时间段高。

反过来，查询 t2.avg_value / t1.avg_value 差异最大的 10 个监控项:
```
mysql> SELECT 
         t2.avg_value / t1.avg_value AS ratio,
         t1.metrics_name,
         t1.avg_value,
         t2.avg_value,
         t2.comment
       FROM 
         (
           SELECT /*+ time_range("2020-03-03 17:08:00", "2020-03-03 17:11:00")*/
             * 
           FROM information_schema.metrics_summary
         ) t1 
         JOIN
         (
           SELECT /*+ time_range("2020-03-03 17:18:00", "2020-03-03 17:21:00")*/
             * 
           FROM information_schema.metrics_summary
         ) t2
         ON t1.metrics_name = t2.metrics_name 
       ORDER BY 
         ratio DESC limit 10;
+----------------+-----------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
| ratio          | metrics_name                            | avg_value      | avg_value        | comment                                                                                     |
+----------------+-----------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
| 5865.59537065  | tidb_slow_query_cop_process_total_time  |       0.016333 |        95.804724 | The total time of TiDB slow query statistics with slow query total cop process time(second) |
| 3648.74109023  | tidb_distsql_partial_scan_key_total_num |   10865.666667 |  39646004.4394   | The total num of distsql partial scan key numbers                                          |
|  267.002351165 | tidb_slow_query_cop_wait_total_time     |       0.003333 |         0.890008 | The total time of TiDB slow query statistics with slow query total cop wait time(second)    |
|  192.43267836  | tikv_cop_total_response_total_size      | 2515333.66667  | 484032394.445    |                                                                                             |
|  192.43267836  | tikv_cop_total_response_size            |   41922.227778 |   8067206.57408  |                                                                                             |
|  152.780296296 | tidb_distsql_scan_key_total_num         |    5304.333333 |    810397.618317 | The total num of distsql scan numbers                                                      |
|  126.042290167 | tidb_distsql_execution_total_time       |       0.421622 |        53.142143 | The total time of distsql execution(second)                                                 |
|  105.164020657 | tikv_cop_scan_details                   |     134.450733 |     14139.379665 |                                                                                             |
|  105.164020657 | tikv_cop_scan_details_total             |    8067.043981 |    848362.77991  |                                                                                             |
|  101.635495394 | tikv_cop_total_kv_cursor_operations     |    1070.875    |    108838.91113  |                                                                                             |
+----------------+-----------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
```

上面查询结果表示：

* t2 时间段内的 tidb_slow_query_cop_process_total_time （tidb 慢查询中的 cop process 耗时 ） 比 t1 时间段高了 5865 倍
* t2 时间段内的 tidb_distsql_partial_scan_key_total_num（tidb 的 distsql 请求扫描key 的数量） 比 t1 时间段高了 3648 倍
* t2 时间段内的 tikv_cop_total_response_size（tikv 的 cop 请求结果的大小 ） 比 t1 时间段高了 192 倍
* t2 时间段内的 tikv_cop_scan_details（tikv 的 cop 请求的 scan ） 比 t1 时间段高了 105 倍

通过上面两个时间段对比查询可以大致了解集群在这 2 个时间段的负载情况。t2 时间段的 Cop 请求要比 t2 时间段高很多，导致 TiKV 的 Copprocessor 过载，出现了 cop task 等待，可以猜测可能是 t2 时间段出现了一些大查询，或者是查询较多的负载。

实际上，在 t1 ~ t2 整个时间段内都在跑 go-ycsb 的压测，然后在 t2 时间段跑了 20 个 tpch 的查询，所以是因为 tpch 大查询导致了很多的 cop 请求。

## 诊断结果表

前面介绍了集群信息表和集群监控表，并通过 SQL 演示了如何通过查询这些表来发现集群问题，比如通过 information_schema.cluster_config 发现集群不同节点配置不一致，通过 information_schema.cluster_info 发现是否存在组件版本不一样。
不过手动执行固定模式的 SQL 排查集群问题是低效的，为了进一步优化用户体验，方便用户使用，于是我们利用已有的基础信息表提供了诊断相关的系统表来自动执行诊断：

* information_schema.inspection_result
* information_schema.inspection_summary

该诊断功能可以帮助用户快速发现问题，减少用户的重复性手动工作。可使用 SQL select * from information_schema.inspection_result 来触发内部的诊断。

## INSPECTION_RESULT

TiDB 内置了一些诊断规则，用于检测系统中的故障以及隐患。

诊断结果表 `information_schema.inspection_result` 用于展示对系统的诊断结果，诊断是惰性触发，使用 SQL select * from inspection_result 会触发所有的诊断规则对系统进行诊断，并会在结果集中展示系统中的故障或风险。

诊断结果表 `information_schema.inspection_result` 的表结构如下：
```
mysql> desc inspection_result;
+-----------+--------------+------+------+---------+-------+
| Field     | Type         | Null | Key  | Default | Extra |
+-----------+--------------+------+------+---------+-------+
| RULE      | varchar(64)  | YES  |      | NULL    |       |
| ITEM      | varchar(64)  | YES  |      | NULL    |       |
| TYPE      | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE  | varchar(64)  | YES  |      | NULL    |       |
| VALUE     | varchar(64)  | YES  |      | NULL    |       |
| REFERENCE | varchar(64)  | YES  |      | NULL    |       |
| SEVERITY  | varchar(64)  | YES  |      | NULL    |       |
| DETAILS   | varchar(256) | YES  |      | NULL    |       |
+-----------+--------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

字段解释：
* RULE：诊断规则，目前实现了
  * config：配置一致性检测，如果同一个配置在不同节点不同，会生成 warning 级别的诊断结果
  * version：版本一致性检测，如果同一类型的节点版本不同，会生成 critical 级别的诊断结果
  * current-load：如果当前系统负载太高，会生成对应的 warning 诊断结果
  * critical-error：系统各个模块定义了严重的错误，如果某一个严重错误在对应时间段内超过阈值，会生成 warning 诊断结果
  * threshold-check：诊断系统会对大量指标进行阈值判断，如果超过阈值会生成对应的诊断信息
* ITEM：每一个规则会对不同的项进行诊断，这个用来表示对应规则下面的具体诊断项。
* TYPE：诊断的实例类型，可能是 tidb/tikv/pd
* INSTANCE：诊断的具体实例
* VALUE：针对这个诊断项得到的值
* REFERENCE：针对这个诊断项的参考值（阈值），如果 VALUE 和阈值差距比较大，就会产生对应的结果
* SEVERITY：严重程度，warning/critical
* DETAILS：诊断的详细信息，可能包含进一步调查的 SQL 或文档链接

诊断模块内部包含一系列的规则，这些规则会通过查询已有的监控表和集群信息表，对结果和预先设定的阈值进行对比，如果结果超过阈值或低于阈值将生成 warning / critical 的结果，并在 details 列中提供进一步信息。

查询已有的诊断规则:

```
mysql> select * from inspection_rules where type='inspection';
+-----------------+------------+---------+
| NAME            | TYPE       | COMMENT |
+-----------------+------------+---------+
| config          | inspection |         |
| version         | inspection |         |
| current-load    | inspection |         |
| critical-error  | inspection |         |
| threshold-check | inspection |         |
+-----------------+------------+---------+
5 rows in set (0.00 sec)
```

以上的监控汇总表是按照集群所有的监控进行汇总，但是在部分场景下我们只想要关注特定链路或模块的监控汇总，比如当前 Coprocessor 配置的线程池为 8，
如果 Coprocessor 的 CPU 使用率达到了 750%，可以确定这里有风险，或者可能提前成为瓶颈。但是部分监控会因为用户的 workload 不同而差异较大，所以难以定义确定的阈值。这部分场景问题排查也非常重要，所以新建了 `inspection_summary` 来进行链路汇总。

诊断汇总表 `information_schema.inspection_summary` 的表结构如下：

```
mysql> desc inspection_summary;
+--------------+-----------------------+------+------+---------+-------+
| Field        | Type                  | Null | Key  | Default | Extra |
+--------------+-----------------------+------+------+---------+-------+
| RULE         | varchar(64)           | YES  |      | NULL    |       |
| INSTANCE     | varchar(64)           | YES  |      | NULL    |       |
| METRICS_NAME | varchar(64)           | YES  |      | NULL    |       |
| LABEL        | varchar(64)           | YES  |      | NULL    |       |
| QUANTILE     | double unsigned       | YES  |      | NULL    |       |
| AVG_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| MIN_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| MAX_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
+--------------+-----------------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

字段解释：

* RULE：汇总规则，由于规则在持续添加，以下列表可能已经过时，最新的规则列表可以通过 select * from inspection_rules where type='summary' 查询
* INSTANCE：监控的具体实例
* METRIC_NAME：监控表
* QUANTILE：对于包含 QUANTILE 的监控表有效，可以通过谓词下推指定多个百分位，比如 `select * from inspection_summary where rule='ddl' and quantile in (0.80, 0.90, 0.99, 0.999)` 来汇总 ddl 相关监控，查询百分位为 80/90/99/999 的结果。 AVG_VALUE/MIN_VALUE/MAX_VALUE 分别表示聚合的平均、最小、最大值。

> **注意事项：**
>
>由于汇总所有结果有一定开销，所以 `information_summary` 中的规则是惰性触发的，即通过 SQL 的谓词中显示指定的 rule 才会运行。比如 `select * from inspection_summary` 语句会得到一个空的结果集。`select * from inspection_summary where rule in ('read-link', 'ddl')` 会汇总读链路和 DDL 相关的监控。

使用示例:

诊断结果表和诊断监控汇总表都可以通过 hint 的方式指定诊断的时间范围，比如 select /*+ time_range('2020-03-07 12:00:00','2020-03-07 13:00:00') */ * from inspection_summary 对2020-03-07 12:00:00 - 2020-03-07 13:00:00 时间段的监控汇总。和监控汇总表一样，通过两个不同时间段的数据进行对比，快速发现差异较大的监控项。以下为一个例子：
```
诊断集群在时间段 "2020-01-16 16:00:54.933", "2020-01-16 16:10:54.933" 的故障:

mysql> SELECT 
         t1.avg_value / t2.avg_value AS ratio, 
         t1.*, 
         t2.* 
       FROM 
         (
           SELECT 
             /*+ time_range("2020-01-16 16:00:54.933", "2020-01-16 16:10:54.933")*/ * 
           FROM inspection_summary WHERE rule='read-link'
         ) t1 
         JOIN
         (
           SELECT 
             /*+ time_range("2020-01-16 16:10:54.933","2020-01-16 16:20:54.933")*/ *
           FROM inspection_summary WHERE rule='read-link'
         ) t2
         ON t1.metrics_name = t2.metrics_name 
         and t1.instance = t2.instance 
         and t1.label = t2.label 
       ORDER BY 
         ratio DESC;
```

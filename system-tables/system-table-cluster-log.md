---
title: CLUSTER_LOG
summary: 了解 TiDB 集群日志表 `CLUSTER_LOG`。
category: reference
aliases: ['/docs-cn/dev/reference/system-databases/cluster-log/']
---

# CLUSTER_LOG

集群日志表 `CLUSTER_LOG` 表用于查询集群当前所有 TiDB/PD/TiKV 节点日志。它通过将查询条件下推到各个节点，降低了日志查询对集群的影响。该表的查询性能优于 grep 命令。

TiDB 4.0 版本之前，要获取集群的日志，用户需要逐个登录各个节点汇总日志。TiDB 4.0 的集群日志表提供了一个全局且时间有序的日志搜索结果，为跟踪全链路事件提供了便利的手段。例如按照某一个 `region id` 搜索日志，可以查询该 Region 生命周期内的所有日志；类似地，通过慢日志的 `txn id` 搜索全链路日志，可以查询该事务在各个节点扫描的 key 数量以及流量等信息。

{{< copyable "sql" >}}

```sql
desc information_schema.cluster_log;
```

```
+----------+------------------+------+------+---------+-------+
| Field    | Type             | Null | Key  | Default | Extra |
+----------+------------------+------+------+---------+-------+
| TIME     | varchar(32)      | YES  |      | NULL    |       |
| TYPE     | varchar(64)      | YES  |      | NULL    |       |
| INSTANCE | varchar(64)      | YES  |      | NULL    |       |
| LEVEL    | varchar(8)       | YES  |      | NULL    |       |
| MESSAGE  | var_string(1024) | YES  |      | NULL    |       |
+----------+------------------+------+------+---------+-------+
5 rows in set (0.00 sec)
```

字段解释：

* `TIME`：日志打印时间。
* `TYPE`：节点的类型，可取值为 `tidb`，`pd` 和 `tikv`。
* `INSTANCE`：节点的服务地址。
* `LEVEL`：日志级别。
* `MESSAGE`：日志内容。

> **注意：**
>
> + 日志表的所有字段都会下推到对应节点执行，所以为了降低使用集群日志表的开销，需尽可能地指定更多的条件。例如 `select * from cluter_log where instance='tikv-1'` 只会在 `tikv-1` 上执行日志搜索。
>
> + `message` 字段支持 `like` 和 `regexp` 正则表达式，对应的 pattern 会编译为 `regexp`。同时指定多个 `message` 条件，相当于 `grep` 命令的 `pipeline` 形式，例如：`select * from cluster_log where message like 'coprocessor%' and message regexp '.*slow.*'` 相当于在集群所有节点执行 `grep 'coprocessor' xxx.log | grep -E '.*slow.*'`。

查询某个 DDL 的执行过程示例如下：

{{< copyable "sql" >}}

```sql
select * from information_schema.cluster_log where message like '%ddl%' and message like '%job%58%' and type='tidb' and time > '2020-03-27 15:39:00';
```

```
+-------------------------+------+------------------+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| TIME                    | TYPE | INSTANCE         | LEVEL | MESSAGE                                                                                                                                                                                                                                                                                                                                     |
+-------------------------+------+------------------+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 2020/03/27 15:39:36.140 | tidb | 172.16.5.40:4008 | INFO  | [ddl_worker.go:253] ["[ddl] add DDL jobs"] ["batch count"=1] [jobs="ID:58, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:57, RowCount:0, ArgLen:1, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0; "]                                                                       |
| 2020/03/27 15:39:36.140 | tidb | 172.16.5.40:4008 | INFO  | [ddl.go:457] ["[ddl] start DDL job"] [job="ID:58, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:57, RowCount:0, ArgLen:1, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0"] [query="create table t3 (a int, b int,c int)"]                                                   |
| 2020/03/27 15:39:36.879 | tidb | 172.16.5.40:4009 | INFO  | [ddl_worker.go:554] ["[ddl] run DDL job"] [worker="worker 1, tp general"] [job="ID:58, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:57, RowCount:0, ArgLen:0, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0"]                                                             |
| 2020/03/27 15:39:36.936 | tidb | 172.16.5.40:4009 | INFO  | [ddl_worker.go:739] ["[ddl] wait latest schema version changed"] [worker="worker 1, tp general"] [ver=35] ["take time"=52.165811ms] [job="ID:58, Type:create table, State:done, SchemaState:public, SchemaID:1, TableID:57, RowCount:0, ArgLen:1, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0"] |
| 2020/03/27 15:39:36.938 | tidb | 172.16.5.40:4009 | INFO  | [ddl_worker.go:359] ["[ddl] finish DDL job"] [worker="worker 1, tp general"] [job="ID:58, Type:create table, State:synced, SchemaState:public, SchemaID:1, TableID:57, RowCount:0, ArgLen:0, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0"]                                                      |
| 2020/03/27 15:39:36.140 | tidb | 172.16.5.40:4009 | INFO  | [ddl_worker.go:253] ["[ddl] add DDL jobs"] ["batch count"=1] [jobs="ID:58, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:57, RowCount:0, ArgLen:1, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0; "]                                                                       |
| 2020/03/27 15:39:36.140 | tidb | 172.16.5.40:4009 | INFO  | [ddl.go:457] ["[ddl] start DDL job"] [job="ID:58, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:57, RowCount:0, ArgLen:1, start time: 2020-03-27 15:39:36.129 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:0"] [query="create table t3 (a int, b int,c int)"]                                                   |
| 2020/03/27 15:39:37.141 | tidb | 172.16.5.40:4008 | INFO  | [ddl.go:489] ["[ddl] DDL job is finished"] [jobID=58]                                                                                                                                                                                                                                                                                       |
+-------------------------+------+------------------+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

上面查询结果表示：

+ 用户将 DDL JOB ID 为 `58` 的请求发给 `172.16.5.40:4008` TiDB 节点。
+ `172.16.5.40:4009` TiDB 节点处理这个 DDL 请求，说明此时 `172.16.5.40:4009` 节点是 DDL owner。
+ DDL JOB ID 为 58 的请求处理完成。

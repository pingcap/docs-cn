---
title: 慢查询日志
---

# 慢查询日志

TiDB 会将执行时间超过 [slow-threshold](/tidb-configuration-file.md#slow-threshold)（默认值为 300 毫秒）的语句输出到 [slow-query-file](/tidb-configuration-file.md#slow-query-file)（默认值："tidb-slow.log"）日志文件中，用于帮助用户定位慢查询语句，分析和解决 SQL 执行的性能问题。

TiDB 默认启用慢查询日志，可以修改配置 [`enable-slow-log`](/tidb-configuration-file.md#enable-slow-log) 来启用或禁用它。

## 日志示例

```sql
# Time: 2019-08-14T09:26:59.487776265+08:00
# Txn_start_ts: 410450924122144769
# User@Host: root[root] @ localhost [127.0.0.1]
# Conn_ID: 3086
# Exec_retry_time: 5.1 Exec_retry_count: 3
# Query_time: 1.527627037
# Parse_time: 0.000054933
# Compile_time: 0.000129729
# Rewrite_time: 0.000000003 Preproc_subqueries: 2 Preproc_subqueries_time: 0.000000002
# Process_time: 0.07 Request_count: 1 Total_keys: 131073 Process_keys: 131072 Prewrite_time: 0.335415029 Commit_time: 0.032175429 Get_commit_ts_time: 0.000177098 Local_latch_wait_time: 0.106869448 Write_keys: 131072 Write_size: 3538944 Prewrite_region: 1
# DB: test
# Is_internal: false
# Digest: 50a2e32d2abbd6c1764b1b7f2058d428ef2712b029282b776beb9506a365c0f1
# Stats: t:pseudo
# Num_cop_tasks: 1
# Cop_proc_avg: 0.07 Cop_proc_p90: 0.07 Cop_proc_max: 0.07 Cop_proc_addr: 172.16.5.87:20171
# Cop_wait_avg: 0 Cop_wait_p90: 0 Cop_wait_max: 0 Cop_wait_addr: 172.16.5.87:20171
# Cop_backoff_regionMiss_total_times: 200 Cop_backoff_regionMiss_total_time: 0.2 Cop_backoff_regionMiss_max_time: 0.2 Cop_backoff_regionMiss_max_addr: 127.0.0.1 Cop_backoff_regionMiss_avg_time: 0.2 Cop_backoff_regionMiss_p90_time: 0.2
# Cop_backoff_rpcPD_total_times: 200 Cop_backoff_rpcPD_total_time: 0.2 Cop_backoff_rpcPD_max_time: 0.2 Cop_backoff_rpcPD_max_addr: 127.0.0.1 Cop_backoff_rpcPD_avg_time: 0.2 Cop_backoff_rpcPD_p90_time: 0.2
# Cop_backoff_rpcTiKV_total_times: 200 Cop_backoff_rpcTiKV_total_time: 0.2 Cop_backoff_rpcTiKV_max_time: 0.2 Cop_backoff_rpcTiKV_max_addr: 127.0.0.1 Cop_backoff_rpcTiKV_avg_time: 0.2 Cop_backoff_rpcTiKV_p90_time: 0.2
# Mem_max: 525211
# Disk_max: 65536
# Prepared: false
# Plan_from_cache: false
# Succ: true
# Plan: tidb_decode_plan('ZJAwCTMyXzcJMAkyMAlkYXRhOlRhYmxlU2Nhbl82CjEJMTBfNgkxAR0AdAEY1Dp0LCByYW5nZTpbLWluZiwraW5mXSwga2VlcCBvcmRlcjpmYWxzZSwgc3RhdHM6cHNldWRvCg==')
use test;
insert into t select * from t;
```

## 字段含义说明

> **注意：**
>
> 慢查询日志中所有时间相关字段的单位都是 **“秒”**

Slow Query 基础信息：

* `Time`：表示日志打印时间。
* `Query_time`：表示执行这个语句花费的时间。
* `Parse_time`：表示这个语句在语法解析阶段花费的时间。
* `Compile_time`：表示这个语句在查询优化阶段花费的时间。
* `Query`：表示 SQL 语句。慢日志里面不会打印 `Query`，但映射到内存表后，对应的字段叫 `Query`。
* `Digest`：表示 SQL 语句的指纹。
* `Txn_start_ts`：表示事务的开始时间戳，也是事务的唯一 ID，可以用这个值在 TiDB 日志中查找事务相关的其他日志。
* `Is_internal`：表示是否为 TiDB 内部的 SQL 语句。`true` 表示 TiDB 系统内部执行的 SQL 语句，`false` 表示用户执行的 SQL 语句。
* `Index_ids`：表示语句涉及到的索引的 ID。
* `Succ`：表示语句是否执行成功。
* `Backoff_time`：表示语句遇到需要重试的错误时在重试前等待的时间。常见的需要重试的错误有以下几种：遇到了 lock、Region 分裂、`tikv server is busy`。
* `Plan`：表示语句的执行计划，用 `select tidb_decode_plan('xxx...')` SQL 语句可以解析出具体的执行计划。
* `Prepared`：表示这个语句是否是 `Prepare` 或 `Execute` 的请求。
* `Plan_from_cache`：表示这个语句是否命中了执行计划缓存。
* `Rewrite_time`：表示这个语句在查询改写阶段花费的时间。
* `Preproc_subqueries`：表示这个语句中被提前执行的子查询个数，如 `where id in (select if from t)` 这个子查询就可能被提前执行。
* `Preproc_subqueries_time`：表示这个语句中被提前执行的子查询耗时。
* `Exec_retry_count`：表示这个语句执行的重试次数。一般出现在悲观事务中，上锁失败时重试执行该语句。
* `Exec_retry_time`：表示这个语句的重试执行时间。例如某个查询一共执行了三次（前两次失败），则 `Exec_retry_time` 表示前两次的执行时间之和，`Query_time` 减去 `Exec_retry_time` 则为最后一次执行时间。

和事务执行相关的字段：

* `Prewrite_time`：表示事务两阶段提交中第一阶段（prewrite 阶段）的耗时。
* `Commit_time`：表示事务两阶段提交中第二阶段（commit 阶段）的耗时。
* `Get_commit_ts_time`：表示事务两阶段提交中第二阶段（commit 阶段）获取 commit 时间戳的耗时。
* `Local_latch_wait_time`：表示事务两阶段提交中第二阶段（commit 阶段）发起前在 TiDB 侧等锁的耗时。
* `Write_keys`：表示该事务向 TiKV 的 Write CF 写入 Key 的数量。
* `Write_size`：表示事务提交时写 key 或 value 的总大小。
* `Prewrite_region`：表示事务两阶段提交中第一阶段（prewrite 阶段）涉及的 TiKV Region 数量。每个 Region 会触发一次远程过程调用。

和内存使用相关的字段：

* `Mem_max`：表示执行期间 TiDB 使用的最大内存空间，单位为 byte。

和硬盘使用相关的字段：

* `Disk_max`: 表示执行期间 TiDB 使用的最大硬盘空间，单位为 byte。

和 SQL 执行的用户相关的字段：

* `User`：表示执行语句的用户名。
* `Conn_ID`：表示用户的链接 ID，可以用类似 `con:3` 的关键字在 TiDB 日志中查找该链接相关的其他日志。
* `DB`：表示执行语句时使用的 database。

和 TiKV Coprocessor Task 相关的字段：

* `Request_count`：表示这个语句发送的 Coprocessor 请求的数量。
* `Total_keys`：表示 Coprocessor 扫过的 key 的数量。
* `Process_time`：执行 SQL 在 TiKV 的处理时间之和，因为数据会并行的发到 TiKV 执行，这个值可能会超过 `Query_time`。
* `Wait_time`：表示这个语句在 TiKV 的等待时间之和，因为 TiKV 的 Coprocessor 线程数是有限的，当所有的 Coprocessor 线程都在工作的时候，请求会排队；当队列中有某些请求耗时很长的时候，后面的请求的等待时间都会增加。
* `Process_keys`：表示 Coprocessor 处理的 key 的数量。相比 total_keys，processed_keys 不包含 MVCC 的旧版本。如果 processed_keys 和 total_keys 相差很大，说明旧版本比较多。
* `Cop_proc_avg`：cop-task 的平均执行时间。
* `Cop_proc_p90`：cop-task 的 P90 分位执行时间。
* `Cop_proc_max`：cop-task 的最大执行时间。
* `Cop_proc_addr`：执行时间最长的 cop-task 所在地址。
* `Cop_wait_avg`：cop-task 的平均等待时间。
* `Cop_wait_p90`：cop-task 的 P90 分位等待时间。
* `Cop_wait_max`：cop-task 的最大等待时间。
* `Cop_wait_addr`：等待时间最长的 cop-task 所在地址。
* `Cop_backoff_{backoff-type}_total_times`：因某种错误造成的 backoff 总次数。
* `Cop_backoff_{backoff-type}_total_time`：因某种错误造成的 backoff 总时间。
* `Cop_backoff_{backoff-type}_max_time`：因某种错误造成的最大 backoff 时间。
* `Cop_backoff_{backoff-type}_max_addr`：因某种错误造成的最大 backoff 时间的 cop-task 地址。
* `Cop_backoff_{backoff-type}_avg_time`：因某种错误造成的平均 backoff 时间。
* `Cop_backoff_{backoff-type}_p90_time`：因某种错误造成的 P90 分位 backoff 时间。

## 相关系统变量

* [tidb_slow_log_threshold](/system-variables.md#tidb_slow_log_threshold)：设置慢日志的阈值，执行时间超过阈值的 SQL 语句将被记录到慢日志中。默认值是 300 ms。
* [tidb_query_log_max_len](/system-variables.md#tidb_query_log_max_len)：设置慢日志记录 SQL 语句的最大长度。默认值是 4096 byte。
* [tidb_redact_log](/system-variables.md#tidb_redact_log)：设置慢日志记录 SQL 时是否将用户数据脱敏用 `?` 代替。默认值是 0 ，即关闭该功能。
* [tidb_enable_collect_execution_info](/system-variables.md#tidb_enable_collect_execution_info)：设置是否记录执行计划中各个算子的物理执行信息，默认值是 `1`。该功能对性能的影响约为 3%。开启该项后查看 `Plan` 的示例如下：

```sql
> select tidb_decode_plan('jAOIMAk1XzE3CTAJMQlmdW5jczpjb3VudChDb2x1bW4jNyktPkMJC/BMNQkxCXRpbWU6MTAuOTMxNTA1bXMsIGxvb3BzOjIJMzcyIEJ5dGVzCU4vQQoxCTMyXzE4CTAJMQlpbmRleDpTdHJlYW1BZ2dfOQkxCXQRSAwyNzY4LkgALCwgcnBjIG51bTogMQkMEXMQODg0MzUFK0hwcm9jIGtleXM6MjUwMDcJMjA2HXsIMgk1BWM2zwAAMRnIADcVyAAxHcEQNQlOL0EBBPBbCjMJMTNfMTYJMQkzMTI4MS44NTc4MTk5MDUyMTcJdGFibGU6dCwgaW5kZXg6aWR4KGEpLCByYW5nZTpbLWluZiw1MDAwMCksIGtlZXAgb3JkZXI6ZmFsc2UJMjUBrgnQVnsA');
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb_decode_plan('jAOIMAk1XzE3CTAJMQlmdW5jczpjb3VudChDb2x1bW4jNyktPkMJC/BMNQkxCXRpbWU6MTAuOTMxNTA1bXMsIGxvb3BzOjIJMzcyIEJ5dGVzCU4vQQoxCTMyXzE4CTAJMQlpbmRleDpTdHJlYW1BZ2dfOQkxCXQRSAwyNzY4LkgALCwgcnBjIG51bTogMQkMEXMQODg0MzUFK0hwcm9jIGtleXM6MjUwMDcJMjA2HXsIMg |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|     id                    task    estRows               operator info                                                  actRows    execution info                                                                  memory       disk                              |
|     StreamAgg_17          root    1                     funcs:count(Column#7)->Column#5                                1          time:10.931505ms, loops:2                                                       372 Bytes    N/A                               |
|     └─IndexReader_18      root    1                     index:StreamAgg_9                                              1          time:10.927685ms, loops:2, rpc num: 1, rpc time:10.884355ms, proc keys:25007    206 Bytes    N/A                               |
|       └─StreamAgg_9       cop     1                     funcs:count(1)->Column#7                                       1          time:11ms, loops:25                                                             N/A          N/A                               |
|         └─IndexScan_16    cop     31281.857819905217    table:t, index:idx(a), range:[-inf,50000), keep order:false    25007      time:11ms, loops:25                                                             N/A          N/A                               |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

在性能测试中可以关闭自动收集算子的执行信息：

{{< copyable "sql" >}}

```sql
set @@tidb_enable_collect_execution_info=0;
```

`Plan` 字段显示的格式和 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 或者 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 大致一致。可以查看 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 或者 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 文档了解更多关于执行计划的信息。

更多详细信息，可以参见 [TiDB 专用系统变量和语法](/system-variables.md)。

## 慢日志内存映射表

用户可通过查询 `INFORMATION_SCHEMA.SLOW_QUERY` 表来查询慢查询日志中的内容，表中列名和慢日志中字段名一一对应，表结构可查看 [`SLOW_QUERY` 表](/information-schema/information-schema-slow-query.md)中的介绍。

> **注意：**
>
> 每次查询 `SLOW_QUERY` 表时，TiDB 都会去读取和解析一次当前的慢查询日志。

TiDB 4.0 中，`SLOW_QUERY` 已经支持查询任意时间段的慢日志，即支持查询已经被 rotate 的慢日志文件的数据。用户查询时只需要指定 `TIME` 时间范围即可定位需要解析的慢日志文件。如果查询不指定时间范围，则仍然只解析当前的慢日志文件，示例如下：

不指定时间范围时，只会解析当前 TiDB 正在写入的慢日志文件的慢查询数据：

{{< copyable "sql" >}}

```sql
select count(*),
       min(time),
       max(time)
from slow_query;
```

```
+----------+----------------------------+----------------------------+
| count(*) | min(time)                  | max(time)                  |
+----------+----------------------------+----------------------------+
| 122492   | 2020-03-11 23:35:20.908574 | 2020-03-25 19:16:38.229035 |
+----------+----------------------------+----------------------------+
```

指定查询 `2020-03-10 00:00:00` 到 `2020-03-11 00:00:00` 时间范围后，会定位指定时间范围内的慢日志文件后解析慢查询数据：

{{< copyable "sql" >}}

```sql
select count(*),
       min(time),
       max(time)
from slow_query
where time > '2020-03-10 00:00:00'
  and time < '2020-03-11 00:00:00';
```

```
+----------+----------------------------+----------------------------+
| count(*) | min(time)                  | max(time)                  |
+----------+----------------------------+----------------------------+
| 2618049  | 2020-03-10 00:00:00.427138 | 2020-03-10 23:00:22.716728 |
+----------+----------------------------+----------------------------+
```

> **注意：**
>
> 如果指定时间范围内的慢日志文件被删除，或者并没有慢查询，则查询结果会返回空。

TiDB 4.0 中新增了 [`CLUSTER_SLOW_QUERY`](/information-schema/information-schema-slow-query.md#cluster_slow_query-table) 系统表，用来查询所有 TiDB 节点的慢查询信息，表结构在 `SLOW_QUERY` 的基础上多增加了 `INSTANCE` 列，表示该行慢查询信息来自的 TiDB 节点地址。使用方式和 [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md) 系统表一样。

关于查询 `CLUSTER_SLOW_QUERY` 表，TiDB 会把相关的计算和判断下推到其他节点执行，而不是把其他节点的慢查询数据都取回来在一台 TiDB 上执行。

## 查询 `SLOW_QUERY`/`CLUSTER_SLOW_QUERY` 示例

### 搜索 Top N 的慢查询

查询 Top 2 的用户慢查询。`is_internal=false` 表示排除 TiDB 内部的慢查询，只看用户的慢查询：

{{< copyable "sql" >}}

```sql
select query_time, query
from information_schema.slow_query
where is_internal = false  -- 排除 TiDB 内部的慢查询 SQL
order by query_time desc
limit 2;
```

输出样例：

```
+--------------+------------------------------------------------------------------+
| query_time   | query                                                            |
+--------------+------------------------------------------------------------------+
| 12.77583857  | select * from t_slim, t_wide where t_slim.c0=t_wide.c0;          |
|  0.734982725 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c0; |
+--------------+------------------------------------------------------------------+
```

### 搜索某个用户的 Top N 慢查询

下面例子中搜索 test 用户执行的慢查询 SQL，且按执行消耗时间逆序排序显式前 2 条：

{{< copyable "sql" >}}

```sql
select query_time, query, user
from information_schema.slow_query
where is_internal = false  -- 排除 TiDB 内部的慢查询 SQL
  and user = "test"        -- 查找的用户名
order by query_time desc
limit 2;
```

输出样例：

```
+-------------+------------------------------------------------------------------+----------------+
| Query_time  | query                                                            | user           |
+-------------+------------------------------------------------------------------+----------------+
| 0.676408014 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c1; | test           |
+-------------+------------------------------------------------------------------+----------------+
```

### 根据 SQL 指纹搜索同类慢查询

在得到 Top N 的慢查询 SQL 后，可通过 SQL 指纹继续搜索同类慢查询 SQL。

先获取 Top N 的慢查询和对应的 SQL 指纹：

{{< copyable "sql" >}}

```sql
select query_time, query, digest
from information_schema.slow_query
where is_internal = false
order by query_time desc
limit 1;
```

输出样例：

```
+-------------+-----------------------------+------------------------------------------------------------------+
| query_time  | query                       | digest                                                           |
+-------------+-----------------------------+------------------------------------------------------------------+
| 0.302558006 | select * from t1 where a=1; | 4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa |
+-------------+-----------------------------+------------------------------------------------------------------+
```

再根据 SQL 指纹搜索同类慢查询：

{{< copyable "sql" >}}

```sql
select query, query_time
from information_schema.slow_query
where digest = "4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa";
```

输出样例：

```
+-----------------------------+-------------+
| query                       | query_time  |
+-----------------------------+-------------+
| select * from t1 where a=1; | 0.302558006 |
| select * from t1 where a=2; | 0.401313532 |
+-----------------------------+-------------+
```

### 搜索统计信息为 pseudo 的慢查询 SQL 语句

{{< copyable "sql" >}}

```sql
select query, query_time, stats
from information_schema.slow_query
where is_internal = false
  and stats like '%pseudo%';
```

输出样例：

```
+-----------------------------+-------------+---------------------------------+
| query                       | query_time  | stats                           |
+-----------------------------+-------------+---------------------------------+
| select * from t1 where a=1; | 0.302558006 | t1:pseudo                       |
| select * from t1 where a=2; | 0.401313532 | t1:pseudo                       |
| select * from t1 where a>2; | 0.602011247 | t1:pseudo                       |
| select * from t1 where a>3; | 0.50077719  | t1:pseudo                       |
| select * from t1 join t2;   | 0.931260518 | t1:407872303825682445,t2:pseudo |
+-----------------------------+-------------+---------------------------------+
```

### 查询执行计划发生变化的慢查询

由于统计信息过时，或者统计信息因为误差无法精确反映数据的真实分布情况时，可能导致同类型 SQL 的执行计划发生改变导致执行变慢，可以用以下 SQL 查询哪些 SQL 具有不同的执行计划：

{{< copyable "sql" >}}

```sql
select count(distinct plan_digest) as count,
       digest,
       min(query)
from cluster_slow_query
group by digest
having count > 1
limit 3\G
```

输出样例：

```
***************************[ 1. row ]***************************
count      | 2
digest     | 17b4518fde82e32021877878bec2bb309619d384fca944106fcaf9c93b536e94
min(query) | SELECT DISTINCT c FROM sbtest25 WHERE id BETWEEN ? AND ? ORDER BY c [arguments: (291638, 291737)];
***************************[ 2. row ]***************************
count      | 2
digest     | 9337865f3e2ee71c1c2e740e773b6dd85f23ad00f8fa1f11a795e62e15fc9b23
min(query) | SELECT DISTINCT c FROM sbtest22 WHERE id BETWEEN ? AND ? ORDER BY c [arguments: (215420, 215519)];
***************************[ 3. row ]***************************
count      | 2
digest     | db705c89ca2dfc1d39d10e0f30f285cbbadec7e24da4f15af461b148d8ffb020
min(query) | SELECT DISTINCT c FROM sbtest11 WHERE id BETWEEN ? AND ? ORDER BY c [arguments: (303359, 303458)];
```

然后可以用查询结果中的 SQL 指纹进一步查询不同的 plan

{{< copyable "sql" >}}

```sql
select min(plan),
       plan_digest
from cluster_slow_query
where digest='17b4518fde82e32021877878bec2bb309619d384fca944106fcaf9c93b536e94'
group by plan_digest\G
```

输出样例：

```
*************************** 1. row ***************************
  min(plan):    Sort_6                  root    100.00131380758702      sbtest.sbtest25.c:asc
        └─HashAgg_10            root    100.00131380758702      group by:sbtest.sbtest25.c, funcs:firstrow(sbtest.sbtest25.c)->sbtest.sbtest25.c
          └─TableReader_15      root    100.00131380758702      data:TableRangeScan_14
            └─TableScan_14      cop     100.00131380758702      table:sbtest25, range:[502791,502890], keep order:false
plan_digest: 6afbbd21f60ca6c6fdf3d3cd94f7c7a49dd93c00fcf8774646da492e50e204ee
*************************** 2. row ***************************
  min(plan):    Sort_6                  root    1                       sbtest.sbtest25.c:asc
        └─HashAgg_12            root    1                       group by:sbtest.sbtest25.c, funcs:firstrow(sbtest.sbtest25.c)->sbtest.sbtest25.c
          └─TableReader_13      root    1                       data:HashAgg_8
            └─HashAgg_8         cop     1                       group by:sbtest.sbtest25.c,
              └─TableScan_11    cop     1.2440069558121831      table:sbtest25, range:[472745,472844], keep order:false
```

### 查询集群各个 TIDB 节点的慢查询数量

{{< copyable "sql" >}}

```sql
select instance, count(*) from information_schema.cluster_slow_query where time >= "2020-03-06 00:00:00" and time < now() group by instance;
```

输出样例：

```
+---------------+----------+
| instance      | count(*) |
+---------------+----------+
| 0.0.0.0:10081 | 124      |
| 0.0.0.0:10080 | 119771   |
+---------------+----------+
```

### 查询仅出现在异常时间段的慢日志

假如发现 `2020-03-10 13:24:00` ~ `2020-03-10 13:27:00` 的 QPS 降低或者延迟上升等问题，可能是由于突然出现大查询导致的，可以用下面 SQL 查询仅出现在异常时间段的慢日志，其中 `2020-03-10 13:20:00` ~ `2020-03-10 13:23:00` 为正常时间段。

{{< copyable "sql" >}}

```sql
SELECT * FROM
    (SELECT /*+ AGG_TO_COP(), HASH_AGG() */ count(*),
         min(time),
         sum(query_time) AS sum_query_time,
         sum(Process_time) AS sum_process_time,
         sum(Wait_time) AS sum_wait_time,
         sum(Commit_time),
         sum(Request_count),
         sum(process_keys),
         sum(Write_keys),
         max(Cop_proc_max),
         min(query),min(prev_stmt),
         digest
    FROM information_schema.CLUSTER_SLOW_QUERY
    WHERE time >= '2020-03-10 13:24:00'
            AND time < '2020-03-10 13:27:00'
            AND Is_internal = false
    GROUP BY  digest) AS t1
WHERE t1.digest NOT IN
    (SELECT /*+ AGG_TO_COP(), HASH_AGG() */ digest
    FROM information_schema.CLUSTER_SLOW_QUERY
    WHERE time >= '2020-03-10 13:20:00'
            AND time < '2020-03-10 13:23:00'
    GROUP BY  digest)
ORDER BY  t1.sum_query_time DESC limit 10\G
```

输出样例：

```
***************************[ 1. row ]***************************
count(*)           | 200
min(time)          | 2020-03-10 13:24:27.216186
sum_query_time     | 50.114126194
sum_process_time   | 268.351
sum_wait_time      | 8.476
sum(Commit_time)   | 1.044304306
sum(Request_count) | 6077
sum(process_keys)  | 202871950
sum(Write_keys)    | 319500
max(Cop_proc_max)  | 0.263
min(query)         | delete from test.tcs2 limit 5000;
min(prev_stmt)     |
digest             | 24bd6d8a9b238086c9b8c3d240ad4ef32f79ce94cf5a468c0b8fe1eb5f8d03df
```

## 解析其他的 TiDB 慢日志文件

TiDB 通过 session 变量 `tidb_slow_query_file` 控制查询 `INFORMATION_SCHEMA.SLOW_QUERY` 时要读取和解析的文件，可通过修改改 session 变量的值来查询其他慢查询日志文件的内容：

{{< copyable "sql" >}}

```sql
set tidb_slow_query_file = "/path-to-log/tidb-slow.log"
```

## 用 `pt-query-digest` 工具分析 TiDB 慢日志

可以用 `pt-query-digest` 工具分析 TiDB 慢日志。

> **注意：**
>
> 建议使用 pt-query-digest 3.0.13 及以上版本。

示例如下：

{{< copyable "shell" >}}

```shell
pt-query-digest --report tidb-slow.log
```

输出样例：

```
# 320ms user time, 20ms system time, 27.00M rss, 221.32M vsz
# Current date: Mon Mar 18 13:18:51 2019
# Hostname: localhost.localdomain
# Files: tidb-slow.log
# Overall: 1.02k total, 21 unique, 0 QPS, 0x concurrency _________________
# Time range: 2019-03-18-12:22:16 to 2019-03-18-13:08:52
# Attribute          total     min     max     avg     95%  stddev  median
# ============     ======= ======= ======= ======= ======= ======= =======
# Exec time           218s    10ms     13s   213ms    30ms      1s    19ms
# Query size       175.37k       9   2.01k  175.89  158.58  122.36  158.58
# Commit time         46ms     2ms     7ms     3ms     7ms     1ms     3ms
# Conn ID               71       1      16    8.88   15.25    4.06    9.83
# Process keys     581.87k       2 103.15k  596.43  400.73   3.91k  400.73
# Process time         31s     1ms     10s    32ms    19ms   334ms    16ms
# Request coun       1.97k       1      10    2.02    1.96    0.33    1.96
# Total keys       636.43k       2 103.16k  652.35  793.42   3.97k  400.73
# Txn start ts     374.38E       0  16.00E 375.48P   1.25P  89.05T   1.25P
# Wait time          943ms     1ms    19ms     1ms     2ms     1ms   972us
.
.
.
```

### 定位问题语句的方法

并不是所有 SLOW_QUERY 的语句都是有问题的。会造成集群整体压力增大的，是那些 process_time 很大的语句。wait_time 很大，但 process_time 很小的语句通常不是问题语句，是因为被问题语句阻塞，在执行队列等待造成的响应时间过长。

## `admin show slow` 命令

除了获取 TiDB 日志，还有一种定位慢查询的方式是通过 `admin show slow` SQL 命令：

{{< copyable "sql" >}}

```sql
admin show slow recent N;
```

{{< copyable "sql" >}}

```sql
admin show slow top [internal | all] N;
```

`recent N` 会显示最近的 N 条慢查询记录，例如：

{{< copyable "sql" >}}

```sql
admin show slow recent 10;
```

`top N` 则显示最近一段时间（大约几天）内，最慢的查询记录。如果指定 `internal` 选项，则返回查询系统内部 SQL 的慢查询记录；如果指定 `all` 选项，返回系统内部和用户 SQL 汇总以后的慢查询记录；默认只返回用户 SQL 中的慢查询记录。

{{< copyable "sql" >}}

```sql
admin show slow top 3;
admin show slow top internal 3;
admin show slow top all 5;
```

由于内存限制，保留的慢查询记录的条数是有限的。当命令查询的 `N` 大于记录条数时，返回的结果记录条数会小于 `N`。

输出内容详细说明，如下：

| 列名 | 描述 |
|:------|:---- |
| start | SQL 语句执行开始时间 |
| duration | SQL 语句执行持续时间 |
| details | 执行语句的详细信息 |
| succ | SQL 语句执行是否成功，1: 成功，0: 失败 |
| conn_id | session 连接 ID |
| transcation_ts | 事务提交的 commit ts |
| user | 执行该语句的用户名 |
| db | 执行该 SQL 涉及到 database |
| table_ids | 执行该 SQL 涉及到表的 ID |
| index_ids | 执行该 SQL 涉及到索引 ID |
| internal | 表示为 TiDB 内部的 SQL 语句 |
| digest | 表示 SQL 语句的指纹 |
| sql | 执行的 SQL 语句 |

---
title: 慢查询日志
category: user guide
---

# 慢查询日志

一条不合理的 SQL 语句会导致整个集群压力增大，响应变慢。对于这种问题，需要用慢查询日志来定位有问题的语句，解决性能问题。

### 获取日志

TiDB 会将执行时间超过 [slow-threshold](../op-guide/tidb-config-file.md#slow-threshold) 的语句默认单独输出到 [slow-query-file](../op-guide/tidb-config-file.md#slow-query-file) 文件中 ，并对慢日志的格式做了兼容，可以用 `pt-query-digest` 直接分析慢日志 文件。`slow-threshold` 可以通过配置文件修改，默认是 300ms。`slow-query-file` 默认是 `tidb-slow.log` 。

### 示例

```sql
# Time: 2019-03-18-12:10:19.513961 +0800
# Txn_start_ts: 407078752230047745
# User: root@127.0.0.1
# Conn_ID: 1
# Query_time: 16.479155653
# Process_time: 5.634 Wait_time: 0.002 Request_count: 2 Total_keys: 20002 Process_keys: 20000
# DB: test
# Index_ids: [1]
# Is_internal: false
# Digest: 3635413fe0c8e1aa8307f4f018fe1a9325ea0b97452500106d3f6783fcb65e33
select * from t_slim, t_wide where t_slim.c0=t_wide.c0;
```

### 字段解析

* `Time`：表示日志打印时间。
* `Txn_start_ts`：表示事务的开始时间戳，也是事务的 ID, 可以用这个值在日志中 grep 出事务相关的日志。
* `User`：表示执行语句的用户名
* `Conn_ID`：表示 connection ID，即 session ID, 可以用类似 `con:3 ` 的关键字在  TiDB 日志中 grep 出 session ID 为 3 的日志。
* `Query_time`：表示执行这个语句花费的时间。只有执行时间超过 slow-threshold 的语句才会输出这个日志。
* `Process_time`：执行 SQL  在 TiKV 的处理时间之和，因为数据会并行的发到 TiKV 执行，这个值可能会超过 `Query_time`。
* `Wait_time`：表示这个语句在 TiKV 的等待时间之和，因为 TiKV 的 Coprocessor 线程数是有限的，当所有的 Coprocessor 线程都在工作的时候，请求会排队，当队列中有某些请求耗时很长的时候，后面的请求的等待时间都会增加。
* `Backoff_time`：表示语句遇到需要重试的错误时在重试前等待的时间，常见的需要重试的错误有以下几种：遇到了 lock、Region 分裂、`tikv server is busy`。
* `Request_count`：表示这个语句发送的 Coprocessor 请求的数量。
* `Total_keys`：表示 Coprocessor 扫过的 key 的数量。
* `Process_keys`：表示 Coprocessor 处理的 key 的数量。相比 total_keys，processed_keys 不包含 MVCC 的旧版本。如果 processed_keys 和 total_keys 相差很大，说明旧版本比较多。
* `DB`：表示当前的 database。
* `Index_ids` ：表示语句涉及到的索引的 ID
* `Is_internal`：表示是否是 TiDB 内部 SQL。true 为TiDB 内部执行的SQL, 比如 analyze，load variable 等；false 为用户执行的 SQL 。
* `Digest`： 表示 SQL 语句的指纹
* `Query`：表示 SQL 语句。

### 慢日志内存映射表 
为了方便用 SQL 查询定位慢查询，TiDB 将慢日志内容解析后映射到 `INFORMATION_SCHEMA.SLOW_QUERY` 表中，表中 column 名和慢日志中记录的字段名一一对应 。

```sql
tidb > show create table INFORMATION_SCHEMA.SLOW_QUERY;
+------------+-------------------------------------------------------------+
| Table      | Create Table                                                |
+------------+-------------------------------------------------------------+
| SLOW_QUERY | CREATE TABLE `SLOW_QUERY` (                                 |
|            |   `Time` timestamp UNSIGNED NULL DEFAULT NULL,              |
|            |   `Txn_start_ts` bigint(20) UNSIGNED DEFAULT NULL,          |
|            |   `User` varchar(64) DEFAULT NULL,                          |
|            |   `Conn_ID` bigint(20) UNSIGNED DEFAULT NULL,               |
|            |   `Query_time` double UNSIGNED DEFAULT NULL,                |
|            |   `Process_time` double UNSIGNED DEFAULT NULL,              |
|            |   `Wait_time` double UNSIGNED DEFAULT NULL,                 |
|            |   `Backoff_time` double UNSIGNED DEFAULT NULL,              |
|            |   `Request_count` bigint(20) UNSIGNED DEFAULT NULL,         |
|            |   `Total_keys` bigint(20) UNSIGNED DEFAULT NULL,            |
|            |   `Process_keys` bigint(20) UNSIGNED DEFAULT NULL,          |
|            |   `DB` varchar(64) DEFAULT NULL,                            |
|            |   `Index_ids` varchar(100) DEFAULT NULL,                    |
|            |   `Is_internal` tinyint(1) UNSIGNED DEFAULT NULL,           |
|            |   `Digest` varchar(64) DEFAULT NULL,                        |
|            |   `Query` varchar(4096) DEFAULT NULL                        |
|            | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+------------+-------------------------------------------------------------+
```

#### 查询 SLOW_QUERY 示例

下面示例展示如何通过查询 SLOW_QUERY 表来定位慢查询。

```sql
/* 查询用户执行的SQL, 且按执行消耗时间排序 */
tidb > select `Query_time`, query from INFORMATION_SCHEMA.`SLOW_QUERY` where `Is_internal`=false order by `Query_time` desc limit 2;
+--------------+------------------------------------------------------------------+
| Query_time   | query                                                            |
+--------------+------------------------------------------------------------------+
| 12.77583857  | select * from t_slim, t_wide where t_slim.c0=t_wide.c0;          |
|  0.734982725 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c0; |
+--------------+------------------------------------------------------------------+
2 rows in set
Time: 0.012s
/* 查询 test 用户执行的SQL, 且按执行消耗时间排序*/
tidb > select `Query_time`, query,  user from INFORMATION_SCHEMA.`SLOW_QUERY` where `Is_internal`=false and user like "test%" order by `Query_time` desc limit 2;
+-------------+------------------------------------------------------------------+----------------+
| Query_time  | query                                                            | user           |
+-------------+------------------------------------------------------------------+----------------+
| 0.676408014 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c1; | test@127.0.0.1 |
+-------------+------------------------------------------------------------------+----------------+
1 row in set
Time: 0.014s
/* 设置慢日志文件路径，方便解析其他的慢日志文件，tidb_slow_query_file 变量的作用域是 session */
mysql test@127.0.0.1:test> set tidb_slow_query_file="/path-to-log/tidb-slow.log"
Query OK, 0 rows affected
Time: 0.001s
```

#### 实现细节

`INFORMATION_SCHEMA.SLOW_QUERY` 表里面的内容是通过实时解析 TiDB 慢日志里面的内容得到的。每次查询这个表时都会去读取慢日志文件里面的内容，然后解析。

####  用 pt-query-digest 工具分析 TiDB 慢日志

可以用 pt-query-digest  工具分析 TiDB 慢日志，下面是示例。

```shell
$ pt-query-digest --report tidb-slow.log
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
# Write keys           978       2     477   69.86  463.90  161.64    1.96
# Write size        89.12k     138  43.67k   6.37k  42.34k  14.76k  136.99
.
.
.
```

### 定位问题语句的方法

并不是所有 SLOW_QUERY 的语句都是有问题的。会造成集群整体压力增大的，是那些 process_time 很大的语句。wait_time 很大，但 process_time 很小的语句通常不是问题语句，是因为被问题语句阻塞，在执行队列等待造成的响应时间过长。

### `admin show slow` 命令

除了获取 TiDB 日志，还有一种定位慢查询的方式是通过 `admin show slow` SQL 命令：

```sql
admin show slow recent N
admin show slow top [internal | all] N
```

`recent N` 会显示最近的 N 条慢查询记录，例如：

```sql
admin show slow recent 10
```

`top N` 则显示最近一段时间（大约几天）内，最慢的查询记录。如果指定 `internal` 选项，则返回查询系统内部 SQL 的慢查询记录；如果指定 `all` 选项，返回系统内部和用户 SQL 汇总以后的慢查询记录；默认只返回用户 SQL 中的慢查询记录。

```sql
admin show slow top 3
admin show slow top internal 3
admin show slow top all 5
```

由于内存限制，保留的慢查询记录的条数是有限的。当命令查询的 `N` 大于记录条数时，返回的结果记录条数会小于 `N`。

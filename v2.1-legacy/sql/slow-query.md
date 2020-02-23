---
title: 慢查询日志
category: user guide
---

# 慢查询日志

一条不合理的 SQL 语句会导致整个集群压力增大，响应变慢。对于这种问题，需要用慢查询日志来定位有问题的语句，解决性能问题。

### 获取日志

通过在 TiDB 的日志文件上 grep `SLOW_QUERY` 这个关键字，可以得到执行时间超过 [slow-threshold](../op-guide/tidb-config-file.md#slow-threshold) 的语句日志。

`slow-threshold` 可以通过配置文件修改，默认是 300ms。如果配置了 [slow-query-file](../op-guide/tidb-config-file.md#slow-query-file)，慢查询日志会全部写在这个文件里。

### 示例

```
2018/08/20 19:52:08.632 adapter.go:363: [warning] [SLOW_QUERY] cost_time:18.647928814s
process_time:1m6.768s wait_time:12m11.212s backoff_time:600ms request_count:2058
total_keys:1869712 processed_keys:1869710 succ:true con:3 user:root@127.0.0.1
txn_start_ts:402329674704224261 database:test table_ids:[31],index_ids:[1],
sql:select count(c) from sbtest1 use index (k_1)
```

### 字段解析

#### cost_time

表示执行这个语句花费的时间。只有执行时间超过 slow-threshold 的语句才会输出这个日志。

#### process_time

表示这个语句在 TiKV 的处理时间之和，因为数据会并行的发到 TiKV 执行，这个值可能会超过 cost_time。

#### wait_time

表示这个语句在 TiKV 的等待时间之和，因为 TiKV 的 Coprocessor 线程数是有限的，当所有的 Coprocessor 线程都在工作的时候，请求会排队，当队列中有某些请求耗时很长的时候，后面的请求的等待时间都会增加。

#### backoff_time

表示语句遇到需要重试的错误时在重试前等待的时间，常见的需要重试的错误有以下几种：遇到了 lock、Region 分裂、`tikv server is busy`。

#### request_count

表示这个语句发送的 Coprocessor 请求的数量。

#### total_keys

表示 Coprocessor 扫过的 key 的数量

#### processed_keys

表示 Coprocessor 处理的 key 的数量。相比 total_keys，processed_keys 不包含 MVCC 的旧版本。如果 processed_keys 和 total_keys 相差很大，说明旧版本比较多。

#### succ

表示请求是否执行成功

#### con

表示 connection ID，即 session ID, 可以用类似 `con:3 ` 的关键字在日志中 grep 出 session ID 为 3 的日志。

#### user

表示执行语句的用户名

#### txn_start_ts

表示事务的开始时间戳，也是事务的 ID, 可以用这个值在日志中 grep 出事务相关的日志。

#### database

表示当前的 database

#### table_ids

表示语句涉及到的表的 ID

#### index_ids

表示语句涉及到的索引的 ID

#### sql

表示 SQL 语句

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

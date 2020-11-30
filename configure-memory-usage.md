---
title: TiDB 内存控制文档
aliases: ['/docs-cn/dev/configure-memory-usage/','/docs-cn/dev/how-to/configure/memory-control/']
---

# TiDB 内存控制文档

目前 TiDB 已经能够做到追踪单条 SQL 查询过程中的内存使用情况，当内存使用超过一定阈值后也能采取一些操作来预防 OOM 或者排查 OOM 原因。在 TiDB 的配置文件中，我们可以使用如下配置来控制内存使用超阈值时 TiDB 的行为：

{{< copyable "" >}}

```
# Valid options: ["log", "cancel"]
oom-action = "log"
```

- 如果上面的配置项使用的是 "log"，那么当一条 SQL 的内存使用超过一定阈值（由 session 变量 `tidb_mem_quota_query` 来控制）后，TiDB 会在 log 文件中打印一条 LOG，然后这条 SQL 继续执行，之后如果发生了 OOM 可以在 LOG 中找到对应的 SQL。
- 如果上面的配置项使用的是 "cancel"，那么当一条 SQL 的内存使用超过一定阈值后，TiDB 会立即中断这条 SQL 的执行并给客户端返回一个 error，error 信息中会详细写明这条 SQL 执行过程中各个占用内存比较多的物理执行算子的内存使用情况。

## 如何配置一条 SQL 执行过程中的内存使用阈值

可以在配置文件中设置每个 Query 默认的 Memory Quota，例如将其设置为 32GB：

{{< copyable "" >}}

```
mem-quota-query = 34359738368
```

此外还可通过如下几个 session 变量来控制一条 Query 中的内存使用，大多数用户只需要设置 `tidb_mem_quota_query` 即可，其他变量是高级配置，大多数用户不需要关心：

| 变量名                            | 作用                                              | 单位  | 默认值    |
|:-----------------------------------|:---------------------------------------------------|:-------|:-----------|
| tidb_mem_quota_query              | 配置整条 SQL 的内存使用阈值                       | Byte  | 32 << 30  |
| tidb_mem_quota_hashjoin           | 配置 Hash Join 的内存使用阈值                     | Byte  | 32 << 30  |
| tidb_mem_quota_mergejoin          | 配置 Merge Join 的内存使用阈值                    | Byte  | 32 << 30  |
| tidb_mem_quota_sort               | 配置 Sort 的内存使用阈值                          | Byte  | 32 << 30  |
| tidb_mem_quota_topn               | 配置 TopN 的内存使用阈值                          | Byte  | 32 << 30  |
| tidb_mem_quota_indexlookupreader  | 配置 Index Lookup Reader 的内存使用阈值           | Byte  | 32 << 30  |
| tidb_mem_quota_indexlookupjoin    | 配置 Index Lookup Join 的内存使用阈值             | Byte  | 32 << 30  |
| tidb_mem_quota_nestedloopapply    | 配置 Nested Loop Apply 的内存使用阈值             | Byte  | 32 << 30  |

几个使用例子：

配置整条 SQL 的内存使用阈值为 8GB：

{{< copyable "sql" >}}

```sql
set @@tidb_mem_quota_query = 8 << 30;
```

配置整条 SQL 的内存使用阈值为 8MB：

{{< copyable "sql" >}}

```sql
set @@tidb_mem_quota_query = 8 << 20;
```

配置整条 SQL 的内存使用阈值为 8KB：

{{< copyable "sql" >}}

```sql
set @@tidb_mem_quota_query = 8 << 10;
```

## 如何配置 tidb-server 实例使用内存的阈值

可以在配置文件中设置 tidb-server 实例的 memory-quota。相关配置项为 [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota) 。

例如，配置 tidb-server 实例内存使用总量，将其设置成为 32GB:

{{< copyable "sql" >}}

```sql
[performance]
server-memory-quota = 34359738368
```

当 tidb 内存使用到达 32GB 时，其需要继续申请内存的 sql 会被 cancel。
> **注意：**
>
> `server-memory-quota` 默认值为 0，表示无内存限制。

## 如何配置 tidb-server 实例使用内存的报警功能

TiDB 内存使用占总内存的比例超过一定阈值时会报警。可以在配置文件中设置 tidb 内存使用占总内存的报警比例。相关配置项为 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio) 。

触发报警的条件分两种：

1. 如果 `server-memory-quota` 被设置，则会以 `server-memory-quota` 为总内存限制。当 tidb-server 内存使用超过 `server-memory-quota * memory-usage-alarm-ratio` 时，触发报警。
2. 如果 `server-memory-quota` 未被设置，则会以系统内存为总内存限制。当系统内存使用量超过`系统总内存 * memory-usage-alarm-ratio`，触发报警。

当触发报警时，TiDB 会将当前正在执行的所有 SQL 语句中内存使用最高的 10 条语句和运行时间最长的 10 条语句以及 heap profile 记录到目录 [`tmp-storage-path/record`](/tidb-configuration-file.md#tmp-storage-path) 中，并输出一条包含关键字 `tidb-server has the risk of OOM` 的日志。触发报警的间隔时间为 10s，只有在内存使用低于阈值超过 10s 后再次超过阈值，报警功能才会再次触发。另外，为了防止输出文件过多，TiDB 只会保留记录的最后 5 组信息。

使用例子：

1.配置报警比例为 0.8：

{{< copyable "sql" >}}

```sql
mem-quota-query = 34359738368  // 将单条 SQL 内存限制调高，以便于构造占用内存较大的 SQL
[performance]
memory-usage-alarm-ratio = 0.8
```

2.创建单表 `create table t(a int);` 并插入 1000 条数据。

3.执行 `explain analyze select * from t t1 join t t1 join t t3 order by t1.a`。该 SQL 会输出 1000000000 条记录，占用巨大的内存，导致 tidb OOM。

4.检查 tidb.log 文件，其中会记录系统总内存，系统当前内存使用量，tidb-server 实例内存使用量以及信息记录的目录。

{{< copyable "sql" >}}

```sql
[2020/11/30 15:25:17.252 +08:00] [WARN] [memory_usage_alarm.go:141] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"] ["is server-memory-quota set"=false] ["system memory total"=33682427904] ["system memory usage"=27142864896] ["tidb-server memory usage"=22417922896] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/1000_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]
```

5.检查信息记录的目录，可以得到一组文件,其中包括 `goroutinue+time`、`heap+time`、`running_sql+time` 三个文件。其中 running_sql 文件会以 [`expensive-queries`](/identify-expensive-queries.md) 的形式来记录。

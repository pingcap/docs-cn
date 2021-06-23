---
title: TiDB 内存控制文档
aliases: ['/docs-cn/dev/configure-memory-usage/','/docs-cn/dev/how-to/configure/memory-control/']
---

# TiDB 内存控制文档

目前 TiDB 已经能够做到追踪单条 SQL 查询过程中的内存使用情况，当内存使用超过一定阈值后也能采取一些操作来预防 OOM 或者排查 OOM 原因。在 TiDB 的配置文件中，我们可以使用如下配置来控制内存使用超阈值时 TiDB 的行为：

{{< copyable "" >}}

```
# Valid options: ["log", "cancel"]
oom-action = "cancel"
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
| tidb_mem_quota_query              | 配置整条 SQL 的内存使用阈值                       | Byte  | 1 << 30 (1G)  |
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

可以在配置文件中设置 tidb-server 实例的内存使用阈值。相关配置项为 [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-从-v409-版本开始引入) 。

例如，配置 tidb-server 实例的内存使用总量，将其设置成为 32 GB：

{{< copyable "" >}}

```toml
[performance]
server-memory-quota = 34359738368
```

在该配置下，当 tidb-server 实例内存使用到达 32 GB 时，正在执行的 SQL 语句会被随机强制终止，直至 tidb-server 实例内存使用下降到 32 GB 以下。被强制终止的 SQL 操作会向客户端返回 `Out Of Global Memory Limit!` 错误信息。

> **警告：**
>
> + `server-memory-quota` 目前为实验性特性，不建议在生产环境中使用。
> + `server-memory-quota` 默认值为 0，表示无内存限制。

## tidb-server 内存占用过高时的报警

默认配置下，tidb-server 实例会在机器内存使用达到总内存量的 80% 时打印报警日志，并记录相关状态文件。该内存使用率可以通过配置项 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-从-v409-版本开始引入) 进行设置。具体报警规则请参考该配置项的说明部分。

注意，当触发一次报警后，只有在内存使用率连续低于阈值超过 10 秒并再次达到阈值时，才会再次触发报警。此外，为避免报警时产生的状态文件积累过多，目前只会保留最近 5 次报警时所生成的状态文件。

下例通过构造一个占用大量内存的 SQL 语句触发报警，对该报警功能进行演示：

1. 配置报警比例为 `0.8`：

    {{< copyable "" >}}

    ```toml
    mem-quota-query = 34359738368  // 将单条 SQL 内存限制调高，以便于构造占用内存较大的 SQL
    [performance]
    memory-usage-alarm-ratio = 0.8
    ```

2. 创建单表 `CREATE TABLE t(a int);` 并插入 1000 行数据。

3. 执行 `select * from t t1 join t t1 join t t3 order by t1.a`。该 SQL 语句会输出 1000000000 条记录，占用巨大的内存，进而触发报警。

4. 检查 `tidb.log` 文件，其中会记录系统总内存、系统当前内存使用量、tidb-server 实例的内存使用量以及状态文件所在目录。

    ```
    [2020/11/30 15:25:17.252 +08:00] [WARN] [memory_usage_alarm.go:141] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"] ["is server-memory-quota set"=false] ["system memory total"=33682427904] ["system memory usage"=27142864896] ["tidb-server memory usage"=22417922896] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/1000_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]
    ```

    以上 Log 字段的含义如下：

    * `is server-memory-quota set`：表示配置项 [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-从-v409-版本开始引入) 是否被设置
    * `system memory total`：表示当前系统的总内存
    * `system memory usage`：表示当前系统的内存使用量
    * `tidb-server memory usage`：表示 tidb-server 实例的内存使用量
    * `memory-usage-alarm-ratio`：表示配置项 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-从-v409-版本开始引入) 的值
    * `record path`：表示状态文件存放的目录

5. 通过访问状态文件所在目录（该示例中的目录为 `/tmp/1000_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record`），可以得到一组文件，其中包括 `goroutinue`、`heap`、`running_sql` 3 个文件，文件以记录状态文件的时间为后缀。这 3 个文件分别用来记录报警时的 goroutine 栈信息，堆内存使用状态，及正在运行的 SQL 信息。其中 `running_sql` 文件内的日志格式请参考 [`expensive-queries`](/identify-expensive-queries.md)。

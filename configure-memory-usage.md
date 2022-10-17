---
title: TiDB 内存控制文档
aliases: ['/docs-cn/dev/configure-memory-usage/','/docs-cn/dev/how-to/configure/memory-control/']
---

# TiDB 内存控制文档

目前 TiDB 已经能够做到追踪单条 SQL 查询过程中的内存使用情况，当内存使用超过一定阈值后也能采取一些操作来预防 OOM 或者排查 OOM 原因。你可以使用系统变量 [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-从-v610-版本开始引入) 来控制查询超过内存限制后所采取的操作：

- 如果变量值为 `LOG`，那么当一条 SQL 的内存使用超过一定阈值（由 session 变量 `tidb_mem_quota_query` 控制）后，这条 SQL 会继续执行，但 TiDB 会在 log 文件中打印一条 LOG。
- 如果变量值为 `CANCEL`，那么当一条 SQL 的内存使用超过一定阈值后，TiDB 会立即中断这条 SQL 的执行，并给客户端返回一个错误，错误信息中会详细写明在这条 SQL 执行过程中占用内存的各个物理执行算子的内存使用情况。

## 如何配置一条 SQL 执行过程中的内存使用阈值

使用系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 来配置一条 SQL 执行过程中的内存使用阈值，单位为字节。例如：

配置整条 SQL 的内存使用阈值为 8GB：

{{< copyable "sql" >}}

```sql
SET tidb_mem_quota_query = 8 << 30;
```

配置整条 SQL 的内存使用阈值为 8MB：

{{< copyable "sql" >}}

```sql
SET tidb_mem_quota_query = 8 << 20;
```

配置整条 SQL 的内存使用阈值为 8KB：

{{< copyable "sql" >}}

```sql
SET tidb_mem_quota_query = 8 << 10;
```

## 如何配置 tidb-server 实例使用内存的阈值

可以通过系统变量 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit) 设置 tidb-server 实例的内存使用阈值。

例如，配置 tidb-server 实例的内存使用总量，将其设置成为 32 GB：

{{< copyable "" >}}

```sql
SET GLOBAL tidb_server_memory_limit = "32GB";
```

设置该变量后，当 tidb-server 实例的内存用量到达 32 GB 时，TiDB 会依次终止正在执行的 SQL 操作中内存用量最大的 SQL 操作，直至 tidb-server 实例内存使用下降到 32 GB 以下。被强制终止的 SQL 操作会向客户端返回 `Out Of Memory Quota!` 错误信息。

当前 `tidb_server_memory_limit` **不终止**以下 SQL 操作：

- DDL 操作
- INSERT、UPDATE、DELETE 操作
- 包含窗口函数和公共表表达式的 SQL 操作

> **警告：**
>
> + TiDB 在启动过程中不保证 `tidb_server_memory_limit` 限制。 如果操作系统的空闲内存不足，TiDB 仍有可能引发 OOM。 你需要保证 TiDB 实例的可用内存。
> + 在内存控制过程中，TiDB 的整体内存使用量可能会略微超过 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 的限制。
> + `server-memory-quota` 配置项自 v6.4.0 起被废弃。为了保证兼容性，在 v6.4.0 或更高版本的集群中，`server-memory-quota` 会在单个实例中覆盖 `tidb_server_memory_limit`。如果集群在升级至 v6.4.0 或更高版本前没有配置 `server-memory-quota`，则 tidb-server 实例内存用量限制的阈值取值来自 `tidb_server_memory_limit`。

在 tidb-server 实例内存用量到达总内存的一定比例时（比例由系统变量 [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-从-v640-版本开始引入) 控制）, tidb-server 会尝试主动触发一次 Golang GC 以缓解内存压力。为了避免实例内存在阈值上下范围不断波动导致频繁 GC 进而带来的性能问题，该 GC 方式 1 分钟最多只会触发 1 次。

## 使用 INFORMATION_SCHEMA 系统表查看当前 tidb-server 的内存用量

要查看当前实例或集群的内存使用情况，你可以查询系统表 `INFORMATION_SCHEMA.(CLUSTER_)MEMORY_USAGE`。

{{< copyable "" >}}

```sql
USE INFORMATION_SCHEMA;
SELECT * FROM CLUSTER_MEMORY_USAGE;
```
```
+-----------------+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
| INSTANCE        | MEMORY_TOTAL | MEMORY_LIMIT | MEMORY_CURRENT | MEMORY_MAX_USED | CURRENT_OPS | SESSION_KILL_LAST   | SESSION_KILL_TOTAL | GC_LAST             | GC_TOTAL | DISK_USAGE | QUERY_FORCE_DISK |
+-----------------+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
| 127.0.0.1:10080 |  33674170368 |  10737418240 |     5097644032 |     10826604544 | NULL        | 2022-10-17 22:47:47 |                  1 | 2022-10-17 22:47:47 |       20 |          0 |                0 |
| 127.0.0.1:10081 |  33674170368 |  10737418240 |       66519040 |     10880237568 | NULL        | 2022-10-17 22:46:25 |                  1 | 2022-10-17 22:48:25 |       33 |          0 |                0 |
+-----------------+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
2 rows in set (0.002 sec)
```

字段含义说明：

- instance: 实例信息。只有 CLUSTER_ 表存在该字段
- memory_total: TiDB 的可用内存总量，单位为 byte。
- memory_limit: TIDB 的内存使用限制，单位为 byte。其值和 tidb_server_memory_limit 相同。
- memory_current: TiDB 当前的内存使用量，单位为 byte。
- memory_max_used: 从 TiDB 启动到当前的最大内存使用量，单位为 byte。
- current_ops: “shrinking” | null。“shrinking” 表示 TiDB 正在实施收缩内存的操作。
- session_kill_last: 上一次终止会话的时间戳
- session_kill_total: 从 TiDB 启动到当前累计终止会话的次数
- gc_last: 上一次由内存使用引发 Golang GC 的时间戳
- gc_total: 从 TiDB 启动到当前累计由内存使用引发 Golang GC 的次数
- disk_usage: 当前数据落盘的硬盘使用量，单位为 byte。
- query_force_disk: 从 TiDB 启动到当前累计的落盘次数

可以通过查询系统表 INFORMATION_SCHEMA.(CLUSTER_)MEMORY_USAGE_OPS_HISTORY 来查询本实例（集群）内存相关的操作和执行依据（每个实例保留最近50条记录）。

{{< copyable "" >}}

```sql
USE INFORMATION_SCHEMA;
SELECT * FROM CLUSTER_MEMORY_USAGE_OPS_HISTORY;
```
```
+-----------------+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
| INSTANCE        | TIME                | OPS         | MEMORY_LIMIT | MEMORY_CURRENT | PROCESSID           | MEM        | DISK | CLIENT          | DB   | USER | SQL_DIGEST                                                       | SQL_TEXT                                                             |
+-----------------+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
| 127.0.0.1:10081 | 2022-10-17 22:46:25 | SessionKill |  10737418240 |    10880237568 | 6718275530455515543 | 7905028235 |    0 | 127.0.0.1:34394 | test | root | 146b3d812852663a20635fbcf02be01688f52c8d433dafec0d496a14f0b59df6 | desc analyze select * from t t1 join t t2 on t1.a=t2.a order by t1.a |
| 127.0.0.1:10080 | 2022-10-17 22:47:47 | SessionKill |  10737418240 |    10826604544 | 1461220166988726681 | 7083888090 |    0 | 127.0.0.1:56912 | test | root | a46176e39847c128268109d3b6f23ff6dff28a5316d66851f0a1e008df74dc16 | desc analyze select * from t t1 join t t2 on t1.a=t2.a order by t2.a |
+-----------------+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
2 rows in set (0.002 sec)
```

字段含义说明：

- instance: 实例信息。只有 CLUSTER_ 表存在该字段
- time: 终止对会话的时间戳
- ops: “SessionKill”
- memory_limit: TiDB 当时的内存使用限制，单位为 byte。其值和 tidb_server_memory_limit 相同
- memory_current: TiDB 当时的内存使用量，单位为 byte。
- processid: 被终止的会话的客户连接 ID
- mem: 被终止的会话已使用的内存使用量，单位是 byte。
- disk: 被终止的会话已使用的硬盘使用量，单位是 byte。
- client: 被终止的会话的客户连接的地址
- db: 被终止的会话连接的数据库名
- user: 被终止的会话的用户名
- sql_digest: 被终止的会话正在执行 SQL 的 digest
- sql_text: 被终止的会话正在执行 SQL。

## tidb-server 内存占用过高时的报警

默认配置下，tidb-server 实例会在机器内存使用达到总内存量的 80% 时打印报警日志，并记录相关状态文件。该内存使用率可以通过配置项 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-从-v409-版本开始引入) 进行设置。具体报警规则请参考该配置项的说明部分。

注意，当触发一次报警后，只有在内存使用率连续低于阈值超过 10 秒并再次达到阈值时，才会再次触发报警。此外，为避免报警时产生的状态文件积累过多，目前只会保留最近 5 次报警时所生成的状态文件。

下例通过构造一个占用大量内存的 SQL 语句触发报警，对该报警功能进行演示：

1. 配置报警比例为 `0.8`：

    {{< copyable "" >}}

    ```toml
    mem-quota-query = 34359738368
    [performance]
    memory-usage-alarm-ratio = 0.8
    ```

2. 创建单表 `CREATE TABLE t(a int);` 并插入 1000 行数据。

3. 执行 `select * from t t1 join t t2 join t t3 order by t1.a`。该 SQL 语句会输出 1000000000 条记录，占用巨大的内存，进而触发报警。

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

## tidb-server 其它内存控制策略

### 流量控制

- TiDB 支持对读数据算子的动态内存控制功能。读数据的算子默认启用 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 所允许的最大线程数来读取数据。当单条 SQL 语句的内存使用每超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 一次，读数据的算子就会停止一个线程。
- 流控行为由参数 [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action) 控制。
- 当流控被触发时，会在日志中打印一条包含关键字 `memory exceeds quota, destroy one token now` 的日志。

### 数据落盘

TiDB 支持对执行算子的数据落盘功能。当 SQL 的内存使用超过 Memory Quota 时，tidb-server 可以通过落盘执行算子的中间数据，缓解内存压力。支持落盘的算子有：Sort、MergeJoin、HashJoin、HashAgg。

- 落盘行为由参数 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)、[`oom-use-tmp-storage`](/tidb-configuration-file.md#oom-use-tmp-storage)、[`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path)、[`tmp-storage-quota`](/tidb-configuration-file.md#tmp-storage-quota) 共同控制。
- 当落盘被触发时，TiDB 会在日志中打印一条包含关键字 `memory exceeds quota, spill to disk now` 或 `memory exceeds quota, set aggregate mode to spill-mode` 的日志。
- Sort、MergeJoin、HashJoin 落盘是从 v4.0.0 版本开始引入的，HashAgg 落盘是从 v5.2.0 版本开始引入的。
- 当包含 Sort、MergeJoin 或 HashJoin 的 SQL 语句引起内存 OOM 时，TiDB 默认会触发落盘。当包含 HashAgg 算子的 SQL 语句引起内存 OOM 时，TiDB 默认不触发落盘，请设置系统变量 `tidb_executor_concurrency = 1` 来触发 HashAgg 落盘功能。

> **注意：**
>
> + HashAgg 落盘功能目前不支持 distinct 聚合函数。使用 distinct 函数且内存占用过大时，无法进行落盘。

本示例通过构造一个占用大量内存的 SQL 语句，对 HashAgg 落盘功能进行演示：

1. 将 SQL 语句的 Memory Quota 配置为 1GB（默认 1GB）：

    {{< copyable "sql" >}}

    ```sql
    SET tidb_mem_quota_query = 1 << 30;
    ```

2. 创建单表 `CREATE TABLE t(a int);` 并插入 256 行不同的数据。

3. 尝试执行以下 SQL 语句：

    {{< copyable "sql" >}}

    ```sql
    [tidb]> explain analyze select /*+ HASH_AGG() */ count(*) from t t1 join t t2 join t t3 group by t1.a, t2.a, t3.a;
    ```

    该 SQL 语句占用大量内存，返回 Out of Memory Quota 错误。

    ```sql
    ERROR 1105 (HY000): Out Of Memory Quota![conn_id=3]
    ```

4. 设置系统变量 `tidb_executor_concurrency` 将执行器的并发度调整为 1。在此配置下，内存不足时 HashAgg 会自动尝试触发落盘。

    {{< copyable "sql" >}}

    ```sql
    SET tidb_executor_concurrency = 1;
    ```

5. 执行相同的 SQL 语句，不再返回错误，可以执行成功。从详细的执行计划可以看出，HashAgg 使用了 600MB 的硬盘空间。

    {{< copyable "sql" >}}

    ```sql
    [tidb]> explain analyze select /*+ HASH_AGG() */ count(*) from t t1 join t t2 join t t3 group by t1.a, t2.a, t3.a;
    ```

    ```sql
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    | id                              | estRows     | actRows  | task      | access object | execution info                                                                                                                                                      | operator info                                                   | memory    | disk     |
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    | HashAgg_11                      | 204.80      | 16777216 | root      |               | time:1m37.4s, loops:16385                                                                                                                                           | group by:test.t.a, test.t.a, test.t.a, funcs:count(1)->Column#7 | 1.13 GB   | 600.0 MB |
    | └─HashJoin_12                   | 16777216.00 | 16777216 | root      |               | time:21.5s, loops:16385, build_hash_table:{total:267.2µs, fetch:228.9µs, build:38.2µs}, probe:{concurrency:1, total:35s, max:35s, probe:35s, fetch:962.2µs}         | CARTESIAN inner join                                            | 8.23 KB   | 4 KB     |
    |   ├─TableReader_21(Build)       | 256.00      | 256      | root      |               | time:87.2µs, loops:2, cop_task: {num: 1, max: 150µs, proc_keys: 0, rpc_num: 1, rpc_time: 145.1µs, copr_cache_hit_ratio: 0.00}                                       | data:TableFullScan_20                                           | 885 Bytes | N/A      |
    |   │ └─TableFullScan_20          | 256.00      | 256      | cop[tikv] | table:t3      | tikv_task:{time:23.2µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    |   └─HashJoin_14(Probe)          | 65536.00    | 65536    | root      |               | time:728.1µs, loops:65, build_hash_table:{total:307.5µs, fetch:277.6µs, build:29.9µs}, probe:{concurrency:1, total:34.3s, max:34.3s, probe:34.3s, fetch:278µs}      | CARTESIAN inner join                                            | 8.23 KB   | 4 KB     |
    |     ├─TableReader_19(Build)     | 256.00      | 256      | root      |               | time:126.2µs, loops:2, cop_task: {num: 1, max: 308.4µs, proc_keys: 0, rpc_num: 1, rpc_time: 295.3µs, copr_cache_hit_ratio: 0.00}                                    | data:TableFullScan_18                                           | 885 Bytes | N/A      |
    |     │ └─TableFullScan_18        | 256.00      | 256      | cop[tikv] | table:t2      | tikv_task:{time:79.2µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    |     └─TableReader_17(Probe)     | 256.00      | 256      | root      |               | time:211.1µs, loops:2, cop_task: {num: 1, max: 295.5µs, proc_keys: 0, rpc_num: 1, rpc_time: 279.7µs, copr_cache_hit_ratio: 0.00}                                    | data:TableFullScan_16                                           | 885 Bytes | N/A      |
    |       └─TableFullScan_16        | 256.00      | 256      | cop[tikv] | table:t1      | tikv_task:{time:71.4µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    9 rows in set (1 min 37.428 sec)
    ```
